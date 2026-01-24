"""Combat encounter management and initiative tracking."""

from typing import Union, Optional
from enum import Enum
from pydantic import BaseModel, Field

from ..characters.character import Character
from ..monsters.monster import Monster
from ..rules.combat import initiative_roll
from ..rules.dice import DiceRoll


class CombatantType(Enum):
    """Type of combatant."""
    PLAYER = "player"
    MONSTER = "monster"
    NPC = "npc"


class Combatant(BaseModel):
    """Wrapper for a creature in combat."""
    creature: Union[Character, Monster]
    combatant_type: CombatantType
    initiative: int = 0
    initiative_roll: Optional[DiceRoll] = None
    
    # Action economy tracking
    has_action: bool = True
    has_bonus_action: bool = True
    has_reaction: bool = True
    movement_remaining: int = 30
    
    # Combat state
    is_surprised: bool = False
    is_hidden: bool = False
    
    class Config:
        arbitrary_types_allowed = True
    
    def reset_turn(self) -> None:
        """Reset action economy at the start of turn."""
        self.has_action = True
        self.has_bonus_action = True
        self.has_reaction = True
        
        # Reset movement based on creature speed
        if isinstance(self.creature, Character):
            self.movement_remaining = self.creature.speed
        else:
            self.movement_remaining = self.creature.speed
    
    def use_action(self) -> bool:
        """Use an action. Returns True if successful."""
        if self.has_action:
            self.has_action = False
            return True
        return False
    
    def use_bonus_action(self) -> bool:
        """Use a bonus action. Returns True if successful."""
        if self.has_bonus_action:
            self.has_bonus_action = False
            return True
        return False
    
    def use_reaction(self) -> bool:
        """Use a reaction. Returns True if successful."""
        if self.has_reaction:
            self.has_reaction = False
            return True
        return False
    
    def use_movement(self, distance: int) -> bool:
        """Use movement. Returns True if successful."""
        if self.movement_remaining >= distance:
            self.movement_remaining -= distance
            return True
        return False
    
    def is_alive(self) -> bool:
        """Check if combatant is alive."""
        return self.creature.is_alive()
    
    def get_name(self) -> str:
        """Get combatant name."""
        return self.creature.name
    
    def get_hp(self) -> tuple[int, int]:
        """Get current and max HP."""
        return (self.creature.current_hp, self.creature.max_hp)


class CombatEncounter(BaseModel):
    """Manages a combat encounter."""
    
    combatants: list[Combatant] = Field(default_factory=list)
    round_number: int = 0
    current_turn_index: int = 0
    is_active: bool = False
    surprise_round: bool = False
    
    class Config:
        arbitrary_types_allowed = True
    
    def add_combatant(
        self,
        creature: Union[Character, Monster],
        combatant_type: CombatantType,
        is_surprised: bool = False,
    ) -> Combatant:
        """Add a combatant to the encounter."""
        combatant = Combatant(
            creature=creature,
            combatant_type=combatant_type,
            is_surprised=is_surprised,
        )
        self.combatants.append(combatant)
        return combatant
    
    def roll_initiative(self) -> None:
        """Roll initiative for all combatants."""
        for combatant in self.combatants:
            if isinstance(combatant.creature, Character):
                dex_score = combatant.creature.dexterity
                bonus = combatant.creature.initiative_bonus
            else:
                dex_score = combatant.creature.dexterity
                bonus = 0
            
            roll = initiative_roll(dex_score, bonus)
            combatant.initiative = roll.total
            combatant.initiative_roll = roll
        
        # Sort by initiative (highest first)
        self.combatants.sort(key=lambda c: c.initiative, reverse=True)
    
    def start_combat(self) -> None:
        """Start the combat encounter."""
        self.is_active = True
        self.round_number = 1
        self.current_turn_index = 0
        
        # Reset all combatants
        for combatant in self.combatants:
            combatant.reset_turn()
    
    def get_current_combatant(self) -> Optional[Combatant]:
        """Get the combatant whose turn it is."""
        if not self.is_active or not self.combatants:
            return None
        return self.combatants[self.current_turn_index]
    
    def next_turn(self) -> Optional[Combatant]:
        """Advance to the next turn."""
        if not self.is_active:
            return None
        
        # Move to next combatant
        self.current_turn_index += 1
        
        # Check if round is complete
        if self.current_turn_index >= len(self.combatants):
            self.current_turn_index = 0
            self.round_number += 1
            
            # Reset reactions for all combatants at start of new round
            for combatant in self.combatants:
                combatant.has_reaction = True
            
            # Tick down condition durations
            for combatant in self.combatants:
                if isinstance(combatant.creature, (Character, Monster)):
                    combatant.creature.conditions.tick_durations()
        
        # Get current combatant and reset their turn
        current = self.get_current_combatant()
        if current:
            current.reset_turn()
        
        return current
    
    def end_turn(self) -> Optional[Combatant]:
        """End the current turn and advance to next."""
        return self.next_turn()
    
    def remove_defeated(self) -> list[Combatant]:
        """Remove defeated combatants from initiative order."""
        defeated = [c for c in self.combatants if not c.is_alive()]
        self.combatants = [c for c in self.combatants if c.is_alive()]
        
        # Adjust current turn index if needed
        if self.current_turn_index >= len(self.combatants) and self.combatants:
            self.current_turn_index = 0
        
        return defeated
    
    def is_combat_over(self) -> bool:
        """Check if combat is over (one side defeated)."""
        if not self.combatants:
            return True
        
        # Check if any players are alive
        players_alive = any(
            c.is_alive() and c.combatant_type == CombatantType.PLAYER
            for c in self.combatants
        )
        
        # Check if any monsters are alive
        monsters_alive = any(
            c.is_alive() and c.combatant_type == CombatantType.MONSTER
            for c in self.combatants
        )
        
        # Combat is over if one side is defeated
        return not (players_alive and monsters_alive)
    
    def end_combat(self) -> None:
        """End the combat encounter."""
        self.is_active = False
    
    def get_initiative_order(self) -> list[tuple[str, int, bool]]:
        """Get initiative order as list of (name, initiative, is_current_turn)."""
        return [
            (
                c.get_name(),
                c.initiative,
                i == self.current_turn_index,
            )
            for i, c in enumerate(self.combatants)
        ]
    
    def get_combatant_by_name(self, name: str) -> Optional[Combatant]:
        """Get a combatant by name."""
        for combatant in self.combatants:
            if combatant.get_name().lower() == name.lower():
                return combatant
        return None
