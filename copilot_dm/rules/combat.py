"""Combat mechanics including attacks, damage, and initiative."""

from typing import Optional
from .dice import roll_d20, roll_damage, RollType, DiceRoll
from .abilities import calculate_modifier


def initiative_roll(dexterity_score: int, bonus: int = 0) -> DiceRoll:
    """
    Roll initiative.
    
    Args:
        dexterity_score: Character's Dexterity score
        bonus: Additional initiative bonus
    
    Returns:
        DiceRoll result
    """
    modifier = calculate_modifier(dexterity_score) + bonus
    return roll_d20(modifier)


def attack_roll(
    attack_bonus: int,
    roll_type: RollType = RollType.NORMAL,
    target_ac: Optional[int] = None,
) -> tuple[DiceRoll, bool, bool]:
    """
    Make an attack roll.
    
    Args:
        attack_bonus: Total attack bonus (ability mod + proficiency + magic, etc.)
        roll_type: Normal, advantage, or disadvantage
        target_ac: Optional target AC to check if attack hits
    
    Returns:
        Tuple of (DiceRoll, hit, critical) where:
        - hit is True if target_ac was provided and attack meets/exceeds it
        - critical is True if natural 20 was rolled
    """
    roll = roll_d20(attack_bonus, roll_type)
    
    critical = roll.is_critical()
    hit = False
    
    if target_ac is not None:
        # Natural 20 always hits
        if critical:
            hit = True
        # Natural 1 always misses
        elif roll.is_fumble():
            hit = False
        else:
            hit = roll.total >= target_ac
    
    return roll, hit, critical


def damage_roll(
    damage_dice: str,
    critical: bool = False,
) -> DiceRoll:
    """
    Roll damage.
    
    Args:
        damage_dice: Damage string like '1d8+3' or '2d6'
        critical: If True, double the dice (not the modifier)
    
    Returns:
        DiceRoll result
    """
    roll = roll_damage(damage_dice)
    
    if critical:
        # Critical hits double the dice, not the modifier
        # Roll damage twice and add modifier once
        roll2 = roll_damage(damage_dice)
        roll.rolls.extend(roll2.rolls)
        roll.total = sum(roll.rolls) + roll.modifier
    
    return roll


def calculate_ac(
    base_ac: int,
    dexterity_score: int,
    max_dex_bonus: Optional[int] = None,
    shield: bool = False,
    other_bonuses: int = 0,
) -> int:
    """
    Calculate Armor Class.
    
    Args:
        base_ac: Base AC (10 for unarmored, or armor's base AC)
        dexterity_score: Character's Dexterity score
        max_dex_bonus: Maximum Dex bonus allowed (None = unlimited)
        shield: Whether character is using a shield (+2 AC)
        other_bonuses: Other AC bonuses (magic items, spells, etc.)
    
    Returns:
        Total AC
    """
    dex_mod = calculate_modifier(dexterity_score)
    
    if max_dex_bonus is not None:
        dex_mod = min(dex_mod, max_dex_bonus)
    
    ac = base_ac + dex_mod
    
    if shield:
        ac += 2
    
    ac += other_bonuses
    
    return ac


def calculate_attack_bonus(
    ability_score: int,
    proficiency_bonus: int,
    proficient: bool = True,
    magic_bonus: int = 0,
    other_bonuses: int = 0,
) -> int:
    """
    Calculate total attack bonus.
    
    Args:
        ability_score: Relevant ability score (STR for melee, DEX for ranged/finesse)
        proficiency_bonus: Character's proficiency bonus
        proficient: Whether character is proficient with the weapon
        magic_bonus: Magic weapon bonus
        other_bonuses: Other attack bonuses
    
    Returns:
        Total attack bonus
    """
    bonus = calculate_modifier(ability_score)
    
    if proficient:
        bonus += proficiency_bonus
    
    bonus += magic_bonus + other_bonuses
    
    return bonus


def calculate_damage_bonus(
    ability_score: int,
    magic_bonus: int = 0,
    other_bonuses: int = 0,
) -> int:
    """
    Calculate damage bonus.
    
    Args:
        ability_score: Relevant ability score
        magic_bonus: Magic weapon bonus
        other_bonuses: Other damage bonuses
    
    Returns:
        Total damage bonus
    """
    return calculate_modifier(ability_score) + magic_bonus + other_bonuses
