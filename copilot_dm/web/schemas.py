"""Request and response schemas for the web API."""

from __future__ import annotations

from pydantic import BaseModel, Field


class StartSessionRequest(BaseModel):
    """Request payload for starting a session."""

    character_name: str


class CharacterSummary(BaseModel):
    """Summary of character information."""

    name: str
    character_class: str = Field(alias="class")
    species: str
    level: int

    class Config:
        populate_by_name = True


class StartSessionResponse(BaseModel):
    """Response payload when starting a session."""

    session_id: str
    intro: str
    character: CharacterSummary


class ActionRequest(BaseModel):
    """Request payload for player actions."""

    action: str


class ActionResponse(BaseModel):
    """Response payload for player actions."""

    response: str
    system_messages: list[str] = Field(default_factory=list)


class PlayerSummary(BaseModel):
    """Summary of the player character."""

    name: str
    character_class: str
    species: str
    level: int


class PlayerStateResponse(BaseModel):
    """Response payload for player state queries."""

    player: PlayerSummary
    hp: dict[str, int]
    armor_class: int
    inventory: list[str]
    prepared_spells: list[str]
    cantrips: list[str]
    adventure_log: list[dict[str, str]]
