"""Spell mechanics and spell slot tracking."""

from typing import Optional
from pydantic import BaseModel


class SpellSlots(BaseModel):
    """Tracks spell slots for a spellcaster."""
    level_1: int = 0
    level_2: int = 0
    level_3: int = 0
    level_4: int = 0
    level_5: int = 0
    level_6: int = 0
    level_7: int = 0
    level_8: int = 0
    level_9: int = 0
    
    level_1_used: int = 0
    level_2_used: int = 0
    level_3_used: int = 0
    level_4_used: int = 0
    level_5_used: int = 0
    level_6_used: int = 0
    level_7_used: int = 0
    level_8_used: int = 0
    level_9_used: int = 0
    
    def get_available(self, level: int) -> int:
        """Get available spell slots for a given level."""
        total = getattr(self, f"level_{level}")
        used = getattr(self, f"level_{level}_used")
        return max(0, total - used)
    
    def use_slot(self, level: int) -> bool:
        """
        Use a spell slot of the given level.
        
        Returns:
            True if slot was available and used, False if no slots available
        """
        if self.get_available(level) > 0:
            setattr(self, f"level_{level}_used", getattr(self, f"level_{level}_used") + 1)
            return True
        return False
    
    def restore_slot(self, level: int) -> bool:
        """
        Restore one spell slot of the given level.
        
        Returns:
            True if slot was restored, False if already at max
        """
        used = getattr(self, f"level_{level}_used")
        if used > 0:
            setattr(self, f"level_{level}_used", used - 1)
            return True
        return False
    
    def long_rest(self) -> None:
        """Restore all spell slots (long rest)."""
        for level in range(1, 10):
            setattr(self, f"level_{level}_used", 0)
    
    def short_rest(self) -> None:
        """Handle short rest (no spell slot restoration in base 5E)."""
        pass


def get_spell_slots_by_level(caster_level: int, caster_class: str) -> SpellSlots:
    """
    Get spell slots for a character based on class and level.
    
    PHB 2024 spell slot progression.
    
    Args:
        caster_level: Character's level in the spellcasting class
        caster_class: Class name (e.g., "Wizard", "Cleric", "Fighter")
    
    Returns:
        SpellSlots object with appropriate slots
    """
    slots = SpellSlots()
    
    # Full casters (Wizard, Cleric, Druid, Sorcerer, Bard)
    full_caster_slots = {
        1: (2, 0, 0, 0, 0),
        2: (3, 0, 0, 0, 0),
        3: (4, 2, 0, 0, 0),
        4: (4, 3, 0, 0, 0),
        5: (4, 3, 2, 0, 0),
        6: (4, 3, 3, 0, 0),
        7: (4, 3, 3, 1, 0),
        8: (4, 3, 3, 2, 0),
        9: (4, 3, 3, 3, 1),
        10: (4, 3, 3, 3, 2),
    }
    
    # Half casters (Ranger, Paladin)
    half_caster_slots = {
        2: (2, 0, 0, 0, 0),
        3: (3, 0, 0, 0, 0),
        5: (4, 2, 0, 0, 0),
        7: (4, 3, 0, 0, 0),
        9: (4, 3, 2, 0, 0),
    }
    
    # Third casters (Eldritch Knight Fighter, Arcane Trickster Rogue)
    third_caster_slots = {
        3: (2, 0, 0, 0, 0),
        4: (3, 0, 0, 0, 0),
        7: (4, 2, 0, 0, 0),
        10: (4, 3, 0, 0, 0),
    }
    
    full_casters = ["Wizard", "Cleric", "Druid", "Sorcerer", "Bard"]
    half_casters = ["Ranger", "Paladin"]
    third_casters = ["Eldritch Knight", "Arcane Trickster"]
    
    if caster_class in full_casters:
        slot_progression = full_caster_slots
    elif caster_class in half_casters:
        slot_progression = half_caster_slots
    elif caster_class in third_casters:
        slot_progression = third_caster_slots
    else:
        return slots  # Non-caster
    
    # Find the appropriate level
    for level in sorted(slot_progression.keys(), reverse=True):
        if caster_level >= level:
            slot_values = slot_progression[level]
            slots.level_1 = slot_values[0]
            if len(slot_values) > 1:
                slots.level_2 = slot_values[1]
            if len(slot_values) > 2:
                slots.level_3 = slot_values[2]
            if len(slot_values) > 3:
                slots.level_4 = slot_values[3]
            if len(slot_values) > 4:
                slots.level_5 = slot_values[4]
            break
    
    return slots


def calculate_spell_save_dc(
    spellcasting_ability_score: int,
    proficiency_bonus: int,
) -> int:
    """
    Calculate spell save DC.
    
    DC = 8 + proficiency bonus + spellcasting ability modifier
    """
    from .abilities import calculate_modifier
    return 8 + proficiency_bonus + calculate_modifier(spellcasting_ability_score)


def calculate_spell_attack_bonus(
    spellcasting_ability_score: int,
    proficiency_bonus: int,
) -> int:
    """
    Calculate spell attack bonus.
    
    Bonus = proficiency bonus + spellcasting ability modifier
    """
    from .abilities import calculate_modifier
    return proficiency_bonus + calculate_modifier(spellcasting_ability_score)
