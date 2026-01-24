"""Game state management."""

from typing import Optional
from pydantic import BaseModel, Field

from ..characters.character import Character
from .combat import CombatEncounter


class GameState(BaseModel):
    """Tracks the current game state."""
    
    # Player character
    player: Optional[Character] = None
    
    # Current combat
    current_combat: Optional[CombatEncounter] = None
    
    # Campaign progress
    current_scene: str = "intro"
    scenes_completed: list[str] = Field(default_factory=list)
    
    # Story flags
    story_flags: dict[str, bool] = Field(default_factory=dict)
    
    # Game mode
    in_combat: bool = False
    
    class Config:
        arbitrary_types_allowed = True
    
    def set_player(self, character: Character) -> None:
        """Set the player character."""
        self.player = character
    
    def start_combat(self, encounter: CombatEncounter) -> None:
        """Start a combat encounter."""
        self.current_combat = encounter
        self.in_combat = True
        encounter.start_combat()
    
    def end_combat(self) -> None:
        """End the current combat."""
        if self.current_combat:
            self.current_combat.end_combat()
        self.in_combat = False
        self.current_combat = None
    
    def complete_scene(self, scene_id: str) -> None:
        """Mark a scene as completed."""
        if scene_id not in self.scenes_completed:
            self.scenes_completed.append(scene_id)
    
    def set_flag(self, flag: str, value: bool = True) -> None:
        """Set a story flag."""
        self.story_flags[flag] = value
    
    def get_flag(self, flag: str) -> bool:
        """Get a story flag value."""
        return self.story_flags.get(flag, False)
    
    def player_short_rest(self, hit_dice_spent: int = 1) -> int:
        """Player takes a short rest."""
        if self.player:
            return self.player.short_rest(hit_dice_spent)
        return 0
    
    def player_long_rest(self) -> None:
        """Player takes a long rest."""
        if self.player:
            self.player.long_rest()
