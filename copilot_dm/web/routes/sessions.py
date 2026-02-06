"""Route definitions for Copilot DM sessions."""

from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from ..schemas import ActionRequest, ActionResponse, PlayerStateResponse, StartSessionRequest, StartSessionResponse
from ..services.session_service import SessionService


def create_session_router(session_service: SessionService) -> APIRouter:
    """Create a router for session endpoints."""
    router = APIRouter()

    @router.post("/sessions", response_model=StartSessionResponse)
    async def start_session(payload: StartSessionRequest) -> StartSessionResponse:
        return await session_service.start_session(payload.character_name)

    @router.post("/sessions/{session_id}/actions", response_model=ActionResponse)
    async def send_action(session_id: str, payload: ActionRequest) -> ActionResponse:
        return await session_service.send_action(session_id, payload.action)

    @router.post("/sessions/{session_id}/actions/stream")
    async def stream_action(session_id: str, payload: ActionRequest) -> StreamingResponse:
        return StreamingResponse(
            session_service.stream_action(session_id, payload.action),
            media_type="text/event-stream",
        )

    @router.get("/sessions/{session_id}/state", response_model=PlayerStateResponse)
    async def get_player_state(session_id: str) -> PlayerStateResponse:
        return session_service.get_player_state(session_id)

    return router
