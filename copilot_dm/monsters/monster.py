"""Monster stat blocks for D&D 5E 2024."""

from typing import Optional
from pydantic import BaseModel, Field
from ..rules.abilities import Ability
from ..rules.conditions import ConditionTracker


class Monster(BaseModel):
    """Represents a D&D 5E 2024 monster or NPC."""
    
    # Basic Info
    name: str
    size: str  # Tiny, Small, Medium, Large, Huge, Gargantuan
    creature_type: str  # Beast, Humanoid, Undead, etc.
    alignment: str = "Unaligned"
    challenge_rating: float  # CR (0.125 = 1/8, 0.25 = 1/4, 0.5 = 1/2, etc.)
    xp_value: int
    
    # Ability Scores
    strength: int = 10
    dexterity: int = 10
    constitution: int = 10
    intelligence: int = 10
    wisdom: int = 10
    charisma: int = 10
    
    # Combat Stats
    armor_class: int
    max_hp: int
    current_hp: int
    hit_dice: str  # e.g., "2d8+2"
    speed: int = 30
    
    # Proficiencies & Bonuses
    proficiency_bonus: int = 2
    saving_throw_bonuses: dict[Ability, int] = Field(default_factory=dict)
    skill_bonuses: dict[str, int] = Field(default_factory=dict)
    
    # Defenses
    damage_resistances: list[str] = Field(default_factory=list)
    damage_immunities: list[str] = Field(default_factory=list)
    condition_immunities: list[str] = Field(default_factory=list)
    damage_vulnerabilities: list[str] = Field(default_factory=list)
    
    # Senses
    darkvision: int = 0  # Range in feet
    blindsight: int = 0
    tremorsense: int = 0
    truesight: int = 0
    passive_perception: int = 10
    
    # Languages
    languages: list[str] = Field(default_factory=list)
    
    # Actions
    actions: list[dict] = Field(default_factory=list)  # List of attack/ability dicts
    bonus_actions: list[dict] = Field(default_factory=list)
    reactions: list[dict] = Field(default_factory=list)
    
    # Special Abilities/Traits
    traits: list[dict] = Field(default_factory=list)
    
    # Status
    conditions: ConditionTracker = Field(default_factory=ConditionTracker)
    
    def get_ability_score(self, ability: Ability) -> int:
        """Get an ability score value."""
        ability_map = {
            Ability.STRENGTH: self.strength,
            Ability.DEXTERITY: self.dexterity,
            Ability.CONSTITUTION: self.constitution,
            Ability.INTELLIGENCE: self.intelligence,
            Ability.WISDOM: self.wisdom,
            Ability.CHARISMA: self.charisma,
        }
        return ability_map[ability]
    
    def take_damage(self, damage: int, damage_type: str = "bludgeoning") -> int:
        """
        Apply damage to monster.
        
        Returns:
            Actual damage taken (after resistances/immunities)
        """
        # Check immunities
        if damage_type.lower() in [d.lower() for d in self.damage_immunities]:
            return 0
        
        # Check resistances
        if damage_type.lower() in [d.lower() for d in self.damage_resistances]:
            damage = damage // 2
        
        # Check vulnerabilities
        if damage_type.lower() in [d.lower() for d in self.damage_vulnerabilities]:
            damage = damage * 2
        
        self.current_hp = max(0, self.current_hp - damage)
        return damage
    
    def heal(self, healing: int) -> int:
        """Heal monster."""
        if healing <= 0 or self.current_hp >= self.max_hp:
            return 0
        
        old_hp = self.current_hp
        self.current_hp = min(self.max_hp, self.current_hp + healing)
        return self.current_hp - old_hp
    
    def is_alive(self) -> bool:
        """Check if monster is alive."""
        return self.current_hp > 0
    
    class Config:
        arbitrary_types_allowed = True
