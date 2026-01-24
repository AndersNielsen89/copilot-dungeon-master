"""Ability scores, modifiers, and ability checks for D&D 5E 2024."""

from enum import Enum
from typing import Optional

from .dice import roll_d20, RollType, DiceRoll


class Ability(Enum):
    """The six D&D ability scores."""
    STRENGTH = "Strength"
    DEXTERITY = "Dexterity"
    CONSTITUTION = "Constitution"
    INTELLIGENCE = "Intelligence"
    WISDOM = "Wisdom"
    CHARISMA = "Charisma"


class Skill(Enum):
    """D&D 5E 2024 skills and their associated abilities."""
    ACROBATICS = ("Acrobatics", Ability.DEXTERITY)
    ANIMAL_HANDLING = ("Animal Handling", Ability.WISDOM)
    ARCANA = ("Arcana", Ability.INTELLIGENCE)
    ATHLETICS = ("Athletics", Ability.STRENGTH)
    DECEPTION = ("Deception", Ability.CHARISMA)
    HISTORY = ("History", Ability.INTELLIGENCE)
    INSIGHT = ("Insight", Ability.WISDOM)
    INTIMIDATION = ("Intimidation", Ability.CHARISMA)
    INVESTIGATION = ("Investigation", Ability.INTELLIGENCE)
    MEDICINE = ("Medicine", Ability.WISDOM)
    NATURE = ("Nature", Ability.INTELLIGENCE)
    PERCEPTION = ("Perception", Ability.WISDOM)
    PERFORMANCE = ("Performance", Ability.CHARISMA)
    PERSUASION = ("Persuasion", Ability.CHARISMA)
    RELIGION = ("Religion", Ability.INTELLIGENCE)
    SLEIGHT_OF_HAND = ("Sleight of Hand", Ability.DEXTERITY)
    STEALTH = ("Stealth", Ability.DEXTERITY)
    SURVIVAL = ("Survival", Ability.WISDOM)
    
    def __init__(self, skill_name: str, ability: Ability):
        self.skill_name = skill_name
        self.ability = ability


def calculate_modifier(ability_score: int) -> int:
    """Calculate ability modifier from ability score."""
    return (ability_score - 10) // 2


def ability_check(
    ability_score: int,
    proficiency_bonus: int = 0,
    proficient: bool = False,
    expertise: bool = False,
    roll_type: RollType = RollType.NORMAL,
    dc: Optional[int] = None,
) -> tuple[DiceRoll, bool]:
    """
    Make an ability check.
    
    Args:
        ability_score: The ability score value
        proficiency_bonus: Character's proficiency bonus
        proficient: Whether character is proficient
        expertise: Whether character has expertise (double proficiency)
        roll_type: Normal, advantage, or disadvantage
        dc: Optional DC to check against
    
    Returns:
        Tuple of (DiceRoll, success) where success is True if DC was met
    """
    modifier = calculate_modifier(ability_score)
    
    if expertise:
        modifier += proficiency_bonus * 2
    elif proficient:
        modifier += proficiency_bonus
    
    roll = roll_d20(modifier, roll_type)
    
    success = roll.total >= dc if dc is not None else False
    
    return roll, success


def saving_throw(
    ability_score: int,
    proficiency_bonus: int = 0,
    proficient: bool = False,
    roll_type: RollType = RollType.NORMAL,
    dc: Optional[int] = None,
) -> tuple[DiceRoll, bool]:
    """
    Make a saving throw.
    
    Args:
        ability_score: The ability score value
        proficiency_bonus: Character's proficiency bonus
        proficient: Whether character is proficient in this save
        roll_type: Normal, advantage, or disadvantage
        dc: Optional DC to check against
    
    Returns:
        Tuple of (DiceRoll, success) where success is True if DC was met
    """
    return ability_check(ability_score, proficiency_bonus, proficient, False, roll_type, dc)


def skill_check(
    skill: Skill,
    ability_scores: dict[Ability, int],
    proficiency_bonus: int = 0,
    proficient: bool = False,
    expertise: bool = False,
    roll_type: RollType = RollType.NORMAL,
    dc: Optional[int] = None,
) -> tuple[DiceRoll, bool]:
    """
    Make a skill check.
    
    Args:
        skill: The skill being checked
        ability_scores: Dict of all ability scores
        proficiency_bonus: Character's proficiency bonus
        proficient: Whether character is proficient in this skill
        expertise: Whether character has expertise in this skill
        roll_type: Normal, advantage, or disadvantage
        dc: Optional DC to check against
    
    Returns:
        Tuple of (DiceRoll, success) where success is True if DC was met
    """
    ability_score = ability_scores[skill.ability]
    return ability_check(ability_score, proficiency_bonus, proficient, expertise, roll_type, dc)
