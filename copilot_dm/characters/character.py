"""Character data model for D&D 5E 2024."""

from typing import Optional
from pydantic import BaseModel, Field

from ..rules.abilities import Ability, Skill
from ..rules.conditions import ConditionTracker
from ..rules.spells import SpellSlots


class Character(BaseModel):
    """Represents a D&D 5E 2024 character."""
    
    # Basic Info
    name: str
    level: int = 1
    character_class: str
    species: str
    background: str = ""
    
    # Ability Scores
    strength: int = 10
    dexterity: int = 10
    constitution: int = 10
    intelligence: int = 10
    wisdom: int = 10
    charisma: int = 10
    
    # Hit Points
    max_hp: int
    current_hp: int
    temp_hp: int = 0
    hit_dice: str  # e.g., "1d10"
    hit_dice_remaining: int
    
    # Combat Stats
    armor_class: int
    initiative_bonus: int = 0
    speed: int = 30
    
    # Proficiencies
    proficiency_bonus: int = 2
    saving_throw_proficiencies: list[Ability] = Field(default_factory=list)
    skill_proficiencies: list[Skill] = Field(default_factory=list)
    skill_expertise: list[Skill] = Field(default_factory=list)
    armor_proficiencies: list[str] = Field(default_factory=list)
    weapon_proficiencies: list[str] = Field(default_factory=list)
    
    # Equipment
    weapons: list[dict] = Field(default_factory=list)
    armor: Optional[dict] = None
    shield: bool = False
    inventory: list[str] = Field(default_factory=list)
    gold: int = 0
    
    # Spellcasting (if applicable)
    spellcasting_ability: Optional[Ability] = None
    spell_slots: Optional[SpellSlots] = None
    spells_known: list[str] = Field(default_factory=list)
    cantrips_known: list[str] = Field(default_factory=list)
    
    # Features & Traits
    class_features: list[str] = Field(default_factory=list)
    species_traits: list[str] = Field(default_factory=list)
    
    # Status
    conditions: ConditionTracker = Field(default_factory=ConditionTracker)
    death_saves_successes: int = 0
    death_saves_failures: int = 0
    
    # Flavor
    personality: str = ""
    backstory: str = ""
    
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
    
    def get_all_ability_scores(self) -> dict[Ability, int]:
        """Get all ability scores as a dict."""
        return {
            Ability.STRENGTH: self.strength,
            Ability.DEXTERITY: self.dexterity,
            Ability.CONSTITUTION: self.constitution,
            Ability.INTELLIGENCE: self.intelligence,
            Ability.WISDOM: self.wisdom,
            Ability.CHARISMA: self.charisma,
        }
    
    def is_proficient_in_skill(self, skill: Skill) -> bool:
        """Check if character is proficient in a skill."""
        return skill in self.skill_proficiencies
    
    def has_expertise_in_skill(self, skill: Skill) -> bool:
        """Check if character has expertise in a skill."""
        return skill in self.skill_expertise
    
    def get_skill_modifier(self, skill: Skill) -> int:
        """
        Get the total modifier for a skill check.
        
        This includes the ability modifier plus proficiency bonus (if proficient)
        or double proficiency bonus (if expertise). Works for ALL skills,
        whether the character is proficient or not.
        """
        from ..rules.abilities import calculate_modifier
        
        # Get the ability modifier for this skill's associated ability
        ability_score = self.get_ability_score(skill.ability)
        modifier = calculate_modifier(ability_score)
        
        # Add proficiency bonus if proficient
        if self.has_expertise_in_skill(skill):
            modifier += self.proficiency_bonus * 2
        elif self.is_proficient_in_skill(skill):
            modifier += self.proficiency_bonus
        
        return modifier
    
    def is_proficient_in_save(self, ability: Ability) -> bool:
        """Check if character is proficient in a saving throw."""
        return ability in self.saving_throw_proficiencies
    
    def take_damage(self, damage: int) -> int:
        """
        Apply damage to character.
        
        Returns:
            Actual damage taken (after temp HP)
        """
        if damage <= 0:
            return 0
        
        # Temp HP absorbs damage first
        if self.temp_hp > 0:
            if damage <= self.temp_hp:
                self.temp_hp -= damage
                return 0
            else:
                damage -= self.temp_hp
                self.temp_hp = 0
        
        # Apply remaining damage to HP
        self.current_hp = max(0, self.current_hp - damage)
        return damage
    
    def heal(self, healing: int) -> int:
        """
        Heal character.
        
        Returns:
            Actual HP restored
        """
        if healing <= 0 or self.current_hp >= self.max_hp:
            return 0
        
        old_hp = self.current_hp
        self.current_hp = min(self.max_hp, self.current_hp + healing)
        return self.current_hp - old_hp
    
    def is_alive(self) -> bool:
        """Check if character is alive."""
        return self.current_hp > 0 or self.death_saves_failures < 3
    
    def is_conscious(self) -> bool:
        """Check if character is conscious."""
        return self.current_hp > 0
    
    def short_rest(self, hit_dice_spent: int = 1) -> int:
        """
        Take a short rest and spend hit dice.
        
        Returns:
            HP restored
        """
        if hit_dice_spent <= 0 or self.hit_dice_remaining <= 0:
            return 0
        
        from ..rules.dice import roll_damage
        from ..rules.abilities import calculate_modifier
        
        dice_to_spend = min(hit_dice_spent, self.hit_dice_remaining)
        healing = 0
        
        for _ in range(dice_to_spend):
            roll = roll_damage(self.hit_dice)
            con_mod = calculate_modifier(self.constitution)
            healing += max(1, roll.total + con_mod)
        
        self.hit_dice_remaining -= dice_to_spend
        return self.heal(healing)
    
    def long_rest(self) -> None:
        """Take a long rest (restore HP, HD, spell slots)."""
        # Restore all HP
        self.current_hp = self.max_hp
        
        # Restore hit dice (up to half, minimum 1)
        max_hit_dice = self.level
        dice_to_restore = max(1, max_hit_dice // 2)
        self.hit_dice_remaining = min(max_hit_dice, self.hit_dice_remaining + dice_to_restore)
        
        # Reset death saves
        self.death_saves_successes = 0
        self.death_saves_failures = 0
        
        # Restore spell slots
        if self.spell_slots:
            self.spell_slots.long_rest()
    
    class Config:
        arbitrary_types_allowed = True
