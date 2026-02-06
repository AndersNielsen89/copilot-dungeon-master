"""Service layer for Copilot DM web sessions."""

from __future__ import annotations

import asyncio
import json
from datetime import datetime, timezone
from typing import AsyncIterator

from fastapi import HTTPException

from ...characters.pregens import get_pregen_character, list_pregen_characters
from ...game.state import GameState
from ...game.session import DMSession
from ...rules.dice import RollType, roll_d20, roll_damage
from ..prompts import build_condensed_prompt, build_intro
from ..repositories.session_repository import SessionRepository, SessionState
from ..schemas import ActionResponse, PlayerStateResponse, PlayerSummary, StartSessionResponse


class SessionService:
    """Coordinates game sessions for the web API."""

    def __init__(self, repository: SessionRepository) -> None:
        self._repository = repository

    async def start_session(self, character_name: str) -> StartSessionResponse:
        characters = list_pregen_characters()
        if character_name not in characters:
            raise HTTPException(status_code=404, detail="Character not found")

        game_state = GameState()
        character = get_pregen_character(character_name)
        game_state.set_player(character)

        dm_session = DMSession(game_state, build_condensed_prompt())
        await dm_session.start_session()

        session_state = SessionState(game_state=game_state, dm_session=dm_session)
        session_id = self._repository.create(session_state)

        intro = build_intro(character)
        self._append_log(session_state, "dm", intro)

        return StartSessionResponse(
            session_id=session_id,
            intro=intro,
            character={
                "name": character.name,
                "class": character.character_class,
                "species": character.species,
                "level": str(character.level),
            },
        )

    async def send_action(self, session_id: str, action: str) -> ActionResponse:
        session = self._get_session(session_id)
        action = action.strip()
        if not action:
            raise HTTPException(status_code=400, detail="Action cannot be empty")

        self._append_log(session, "player", action)

        if action.lower().startswith("roll "):
            roll_result = self._perform_player_roll(action[5:].strip())
            self._append_log(session, "system", roll_result)
            return ActionResponse(response=roll_result)

        response_text = await session.dm_session.send_message(action)
        self._append_log(session, "dm", response_text)

        system_messages = self._post_response_updates(session)
        for message in system_messages:
            self._append_log(session, "system", message)

        return ActionResponse(response=response_text, system_messages=system_messages)

    async def stream_action(self, session_id: str, action: str) -> AsyncIterator[str]:
        session = self._get_session(session_id)
        action = action.strip()
        if not action:
            raise HTTPException(status_code=400, detail="Action cannot be empty")

        self._append_log(session, "player", action)

        if action.lower().startswith("roll "):
            roll_result = self._perform_player_roll(action[5:].strip())
            self._append_log(session, "system", roll_result)
            yield self._encode_event({"type": "chunk", "content": roll_result})
            yield self._encode_event({"type": "complete"})
            return

        chunks: list[str] = []
        async for chunk in session.dm_session.send_message_streaming(action):
            chunks.append(chunk)
            yield self._encode_event({"type": "chunk", "content": chunk})

        response_text = "".join(chunks)
        self._append_log(session, "dm", response_text)

        system_messages = self._post_response_updates(session)
        for message in system_messages:
            self._append_log(session, "system", message)
            yield self._encode_event({"type": "system", "content": message})

        yield self._encode_event({"type": "complete"})

    def get_player_state(self, session_id: str) -> PlayerStateResponse:
        session = self._get_session(session_id)
        return self._player_state_payload(session)

    async def shutdown(self) -> None:
        close_tasks = [session.dm_session.close_session() for session in self._repository.list_sessions()]
        if close_tasks:
            await asyncio.gather(*close_tasks, return_exceptions=True)
        self._repository.clear()

    def _get_session(self, session_id: str) -> SessionState:
        session = self._repository.get(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        return session

    def _timestamp(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def _append_log(self, session: SessionState, role: str, content: str) -> None:
        session.adventure_log.append({
            "role": role,
            "content": content,
            "timestamp": self._timestamp(),
        })

    def _encode_event(self, payload: dict[str, str]) -> str:
        return f"data: {json.dumps(payload)}\n\n"

    def _player_state_payload(self, session: SessionState) -> PlayerStateResponse:
        if not session.game_state.player:
            raise HTTPException(status_code=400, detail="Player not selected")

        player = session.game_state.player
        return PlayerStateResponse(
            player=PlayerSummary(
                name=player.name,
                character_class=player.character_class,
                species=player.species,
                level=player.level,
            ),
            hp={
                "current": player.current_hp,
                "max": player.max_hp,
                "temp": player.temp_hp,
            },
            armor_class=player.armor_class,
            inventory=player.inventory,
            prepared_spells=player.spells_known,
            cantrips=player.cantrips_known,
            adventure_log=session.adventure_log,
        )

    def _post_response_updates(self, session: SessionState) -> list[str]:
        system_messages: list[str] = []

        if session.game_state.current_combat and session.game_state.current_combat.is_combat_over():
            session.game_state.end_combat()
            system_messages.append("⚔️ Combat has ended!")

        if session.game_state.player and session.game_state.player.current_hp <= 0:
            system_messages.append("💀 You have fallen. You can choose to retry or end the session.")

        return system_messages

    def _perform_player_roll(self, dice_input: str) -> str:
        dice_input = dice_input.lower().strip()

        roll_type = RollType.NORMAL
        if " advantage" in dice_input or " adv" in dice_input:
            roll_type = RollType.ADVANTAGE
            dice_input = dice_input.replace(" advantage", "").replace(" adv", "").strip()
        elif " disadvantage" in dice_input or " dis" in dice_input:
            roll_type = RollType.DISADVANTAGE
            dice_input = dice_input.replace(" disadvantage", "").replace(" dis", "").strip()

        if dice_input.startswith("d") and not dice_input[0].isdigit():
            dice_input = "1" + dice_input

        try:
            if "d20" in dice_input and roll_type != RollType.NORMAL:
                modifier = 0
                if "+" in dice_input:
                    parts = dice_input.split("+")
                    modifier = int(parts[1])
                elif "-" in dice_input:
                    parts = dice_input.split("-")
                    modifier = -int(parts[1])

                result = roll_d20(modifier, roll_type)
                roll_type_str = "with advantage" if roll_type == RollType.ADVANTAGE else "with disadvantage"
                output = f"🎲 Rolling d20 {roll_type_str}: {result}"

                if result.is_critical():
                    output += " [bold green]NATURAL 20![/bold green]"
                elif result.is_fumble():
                    output += " [bold red]NATURAL 1![/bold red]"

                return output

            result = roll_damage(dice_input)
            return f"🎲 Rolling {dice_input}: {result}"
        except Exception:
            return (
                "Invalid dice notation. Try formats like 'd20', '1d8+3', '2d6', "
                "'d20 advantage'."
            )
