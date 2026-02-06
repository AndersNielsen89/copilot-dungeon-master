"""FastAPI web server for Copilot DM."""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .repositories.session_repository import SessionRepository
from .routes.sessions import create_session_router
from .services.session_service import SessionService


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Manage application lifespan events."""
    # Startup: nothing to do
    yield
    # Shutdown: cleanup sessions
    session_service: SessionService = app.state.session_service
    await session_service.shutdown()


def create_app() -> FastAPI:
    """Build the FastAPI application."""
    app = FastAPI(title="Copilot DM API", lifespan=lifespan)

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
    app.state.session_service = session_service

    app.include_router(create_session_router(session_service))

    return app


app = create_app()
