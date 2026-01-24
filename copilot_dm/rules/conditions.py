"""Status conditions for D&D 5E 2024."""

from enum import Enum
from typing import Optional


class Condition(Enum):
    """D&D 5E 2024 conditions."""
    BLINDED = "Blinded"
    CHARMED = "Charmed"
    DEAFENED = "Deafened"
    EXHAUSTION = "Exhaustion"
    FRIGHTENED = "Frightened"
    GRAPPLED = "Grappled"
    INCAPACITATED = "Incapacitated"
    INVISIBLE = "Invisible"
    PARALYZED = "Paralyzed"
    PETRIFIED = "Petrified"
    POISONED = "Poisoned"
    PRONE = "Prone"
    RESTRAINED = "Restrained"
    STUNNED = "Stunned"
    UNCONSCIOUS = "Unconscious"


class ConditionEffect:
    """Information about a condition's effects."""
    
    def __init__(
        self,
        name: str,
        description: str,
        affects_attacks: bool = False,
        affects_saves: bool = False,
        affects_movement: bool = False,
        incapacitated: bool = False,
    ):
        self.name = name
        self.description = description
        self.affects_attacks = affects_attacks
        self.affects_saves = affects_saves
        self.affects_movement = affects_movement
        self.incapacitated = incapacitated


# PHB 2024 condition descriptions
CONDITION_EFFECTS: dict[Condition, ConditionEffect] = {
    Condition.BLINDED: ConditionEffect(
        "Blinded",
        "A blinded creature can't see and fails ability checks that require sight. "
        "Attack rolls against the creature have advantage, and the creature's attack rolls have disadvantage.",
        affects_attacks=True,
    ),
    Condition.CHARMED: ConditionEffect(
        "Charmed",
        "A charmed creature can't attack the charmer or target the charmer with harmful abilities or magical effects. "
        "The charmer has advantage on ability checks to interact socially with the creature.",
        affects_attacks=True,
    ),
    Condition.DEAFENED: ConditionEffect(
        "Deafened",
        "A deafened creature can't hear and fails ability checks that require hearing.",
    ),
    Condition.EXHAUSTION: ConditionEffect(
        "Exhaustion",
        "Exhaustion has 6 levels. Each level imposes cumulative penalties: "
        "1: Disadvantage on ability checks. "
        "2: Speed halved. "
        "3: Disadvantage on attack rolls and saving throws. "
        "4: Hit point maximum halved. "
        "5: Speed reduced to 0. "
        "6: Death.",
        affects_attacks=True,
        affects_saves=True,
        affects_movement=True,
    ),
    Condition.FRIGHTENED: ConditionEffect(
        "Frightened",
        "A frightened creature has disadvantage on ability checks and attack rolls while the source of fear is within line of sight. "
        "The creature can't willingly move closer to the source of its fear.",
        affects_attacks=True,
        affects_movement=True,
    ),
    Condition.GRAPPLED: ConditionEffect(
        "Grappled",
        "A grappled creature's speed becomes 0, and it can't benefit from bonuses to speed. "
        "The condition ends if the grappler is incapacitated.",
        affects_movement=True,
    ),
    Condition.INCAPACITATED: ConditionEffect(
        "Incapacitated",
        "An incapacitated creature can't take actions, bonus actions, or reactions.",
        incapacitated=True,
    ),
    Condition.INVISIBLE: ConditionEffect(
        "Invisible",
        "An invisible creature is impossible to see without special senses. "
        "The creature gains advantage on attack rolls, and attack rolls against it have disadvantage.",
        affects_attacks=True,
    ),
    Condition.PARALYZED: ConditionEffect(
        "Paralyzed",
        "A paralyzed creature is incapacitated and can't move or speak. "
        "Attack rolls against the creature have advantage. "
        "Any attack that hits the creature is a critical hit if the attacker is within 5 feet. "
        "The creature automatically fails Strength and Dexterity saving throws.",
        affects_attacks=True,
        affects_saves=True,
        affects_movement=True,
        incapacitated=True,
    ),
    Condition.PETRIFIED: ConditionEffect(
        "Petrified",
        "A petrified creature is transformed into stone and is incapacitated. "
        "The creature automatically fails Strength and Dexterity saving throws. "
        "Attack rolls against the creature have advantage. "
        "The creature has resistance to all damage and is immune to poison and disease.",
        affects_attacks=True,
        affects_saves=True,
        affects_movement=True,
        incapacitated=True,
    ),
    Condition.POISONED: ConditionEffect(
        "Poisoned",
        "A poisoned creature has disadvantage on attack rolls and ability checks.",
        affects_attacks=True,
    ),
    Condition.PRONE: ConditionEffect(
        "Prone",
        "A prone creature's only movement option is to crawl (costs 1 extra foot per foot moved). "
        "The creature has disadvantage on attack rolls. "
        "Attack rolls against the creature have advantage if the attacker is within 5 feet, otherwise disadvantage.",
        affects_attacks=True,
        affects_movement=True,
    ),
    Condition.RESTRAINED: ConditionEffect(
        "Restrained",
        "A restrained creature's speed becomes 0. "
        "Attack rolls against the creature have advantage, and the creature's attack rolls have disadvantage. "
        "The creature has disadvantage on Dexterity saving throws.",
        affects_attacks=True,
        affects_saves=True,
        affects_movement=True,
    ),
    Condition.STUNNED: ConditionEffect(
        "Stunned",
        "A stunned creature is incapacitated, can't move, and can speak only falteringly. "
        "Attack rolls against the creature have advantage. "
        "The creature automatically fails Strength and Dexterity saving throws.",
        affects_attacks=True,
        affects_saves=True,
        affects_movement=True,
        incapacitated=True,
    ),
    Condition.UNCONSCIOUS: ConditionEffect(
        "Unconscious",
        "An unconscious creature is incapacitated, can't move or speak, and is unaware of its surroundings. "
        "The creature drops whatever it's holding and falls prone. "
        "Attack rolls against the creature have advantage. "
        "Any attack that hits the creature is a critical hit if the attacker is within 5 feet. "
        "The creature automatically fails Strength and Dexterity saving throws.",
        affects_attacks=True,
        affects_saves=True,
        affects_movement=True,
        incapacitated=True,
    ),
}


class ConditionTracker:
    """Tracks active conditions on a creature."""
    
    def __init__(self):
        self.conditions: dict[Condition, Optional[int]] = {}
        self.exhaustion_level: int = 0
    
    def add_condition(self, condition: Condition, duration: Optional[int] = None) -> None:
        """
        Add a condition to the tracker.
        
        Args:
            condition: The condition to add
            duration: Optional duration in rounds (None = indefinite)
        """
        if condition == Condition.EXHAUSTION:
            self.exhaustion_level = min(6, self.exhaustion_level + 1)
        else:
            self.conditions[condition] = duration
    
    def remove_condition(self, condition: Condition) -> None:
        """Remove a condition from the tracker."""
        if condition == Condition.EXHAUSTION:
            self.exhaustion_level = max(0, self.exhaustion_level - 1)
        elif condition in self.conditions:
            del self.conditions[condition]
    
    def has_condition(self, condition: Condition) -> bool:
        """Check if creature has a specific condition."""
        if condition == Condition.EXHAUSTION:
            return self.exhaustion_level > 0
        return condition in self.conditions
    
    def tick_durations(self) -> list[Condition]:
        """
        Tick down all condition durations by 1 round.
        
        Returns:
            List of conditions that expired
        """
        expired = []
        for condition, duration in list(self.conditions.items()):
            if duration is not None:
                new_duration = duration - 1
                if new_duration <= 0:
                    expired.append(condition)
                    del self.conditions[condition]
                else:
                    self.conditions[condition] = new_duration
        return expired
    
    def get_active_conditions(self) -> list[Condition]:
        """Get all active conditions."""
        conditions = list(self.conditions.keys())
        if self.exhaustion_level > 0:
            conditions.append(Condition.EXHAUSTION)
        return conditions
    
    def is_incapacitated(self) -> bool:
        """Check if creature is incapacitated by any condition."""
        for condition in self.get_active_conditions():
            if CONDITION_EFFECTS[condition].incapacitated:
                return True
        return False
