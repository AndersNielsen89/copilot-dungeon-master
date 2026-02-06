"""Repository for storing web sessions."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable
from uuid import uuid4

from ...game.session import DMSession
from ...game.state import GameState


@dataclass
class SessionState:
    """Holds state for a single web session."""

    game_state: GameState
    dm_session: DMSession
    adventure_log: list[dict[str, str]] = field(default_factory=list)


class SessionRepository:
    """In-memory session store."""

    def __init__(self) -> None:
        self._sessions: dict[str, SessionState] = {}

    def create(self, session_state: SessionState) -> str:
        session_id = str(uuid4())
        self._sessions[session_id] = session_state
        return session_id

    def get(self, session_id: str) -> SessionState | None:
        return self._sessions.get(session_id)

    def list_sessions(self) -> Iterable[SessionState]:
        return self._sessions.values()

    def clear(self) -> None:
        self._sessions.clear()
