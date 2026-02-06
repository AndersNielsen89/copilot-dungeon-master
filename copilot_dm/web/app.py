"""FastAPI web server for Copilot DM."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .repositories.session_repository import SessionRepository
from .routes.sessions import create_session_router
from .services.session_service import SessionService


def create_app() -> FastAPI:
    """Build the FastAPI application."""
    app = FastAPI(title="Copilot DM API")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://localhost:3000",
            "http://127.0.0.1:3000",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    session_repository = SessionRepository()
    session_service = SessionService(session_repository)

    app.include_router(create_session_router(session_service))

    @app.on_event("shutdown")
    async def shutdown_sessions() -> None:
        await session_service.shutdown()

    return app


app = create_app()
