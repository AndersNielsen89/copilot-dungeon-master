"""Dice rolling mechanics for D&D 5E 2024."""

import random
from enum import Enum
from typing import Literal


class DiceType(Enum):
    """Standard D&D dice types."""
    D4 = 4
    D6 = 6
    D8 = 8
    D10 = 10
    D12 = 12
    D20 = 20
    D100 = 100


class RollType(Enum):
    """Type of roll (normal, advantage, disadvantage)."""
    NORMAL = "normal"
    ADVANTAGE = "advantage"
    DISADVANTAGE = "disadvantage"


class DiceRoll:
    """Result of a dice roll."""
    
    def __init__(
        self,
        dice: DiceType,
        num_dice: int = 1,
        modifier: int = 0,
        roll_type: RollType = RollType.NORMAL,
    ):
        self.dice = dice
        self.num_dice = num_dice
        self.modifier = modifier
        self.roll_type = roll_type
        self.rolls: list[int] = []
        self.total: int = 0
        
        self._execute_roll()
    
    def _execute_roll(self) -> None:
        """Execute the dice roll."""
        if self.roll_type == RollType.ADVANTAGE and self.dice == DiceType.D20:
            roll1 = random.randint(1, self.dice.value)
            roll2 = random.randint(1, self.dice.value)
            self.rolls = [roll1, roll2]
            self.total = max(roll1, roll2) + self.modifier
        elif self.roll_type == RollType.DISADVANTAGE and self.dice == DiceType.D20:
            roll1 = random.randint(1, self.dice.value)
            roll2 = random.randint(1, self.dice.value)
            self.rolls = [roll1, roll2]
            self.total = min(roll1, roll2) + self.modifier
        else:
            self.rolls = [random.randint(1, self.dice.value) for _ in range(self.num_dice)]
            self.total = sum(self.rolls) + self.modifier
    
    def is_critical(self) -> bool:
        """Check if this is a natural 20 (critical hit)."""
        return self.dice == DiceType.D20 and 20 in self.rolls
    
    def is_fumble(self) -> bool:
        """Check if this is a natural 1 (critical miss)."""
        return self.dice == DiceType.D20 and all(r == 1 for r in self.rolls)
    
    def __str__(self) -> str:
        """String representation of the roll."""
        roll_str = " + ".join(str(r) for r in self.rolls)
        if self.modifier != 0:
            mod_str = f" + {self.modifier}" if self.modifier > 0 else f" - {abs(self.modifier)}"
            return f"{roll_str}{mod_str} = {self.total}"
        return f"{roll_str} = {self.total}"
    
    def __repr__(self) -> str:
        return f"DiceRoll({self.num_dice}d{self.dice.value}+{self.modifier}: {self.total})"


def roll_d20(
    modifier: int = 0,
    roll_type: RollType = RollType.NORMAL,
) -> DiceRoll:
    """Roll a d20 with optional modifier and advantage/disadvantage."""
    return DiceRoll(DiceType.D20, 1, modifier, roll_type)


def roll_dice(
    dice: DiceType,
    num_dice: int = 1,
    modifier: int = 0,
) -> DiceRoll:
    """Roll any type of dice."""
    return DiceRoll(dice, num_dice, modifier)


def roll_damage(damage_dice: str) -> DiceRoll:
    """
    Roll damage from a damage string like '1d8+3' or '2d6'.
    
    Args:
        damage_dice: Damage string in format like '1d8+3', '2d6', '3d10-1'
    
    Returns:
        DiceRoll result
    """
    # Parse damage string
    parts = damage_dice.lower().replace(" ", "").replace("-", "+-")
    dice_part = parts.split("+")[0]
    modifier = 0
    
    if "+" in parts:
        modifier_parts = parts.split("+")[1:]
        modifier = sum(int(p) for p in modifier_parts if p)
    
    # Parse dice (e.g., "2d6")
    num, die = dice_part.split("d")
    num_dice = int(num) if num else 1
    die_value = int(die)
    
    # Map to DiceType
    dice_type = {
        4: DiceType.D4,
        6: DiceType.D6,
        8: DiceType.D8,
        10: DiceType.D10,
        12: DiceType.D12,
        20: DiceType.D20,
        100: DiceType.D100,
    }.get(die_value)
    
    if not dice_type:
        raise ValueError(f"Invalid dice type: d{die_value}")
    
    return DiceRoll(dice_type, num_dice, modifier)
