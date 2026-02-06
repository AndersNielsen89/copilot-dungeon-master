"""Repository for storing web sessions."""

from __future__ import annotations

import asyncio
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
    lock: asyncio.Lock = field(default_factory=asyncio.Lock)


class SessionRepository:
    """In-memory session store.
    
    Warning:
        Sessions are stored in process memory and will be lost on restart.
        This implementation is not compatible with multiple Uvicorn workers
        (each worker maintains its own session map). For production use with
        multiple workers, replace with a shared backing store (e.g., Redis).
        
        To enforce single-worker mode, run uvicorn with --workers=1.
    """

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
