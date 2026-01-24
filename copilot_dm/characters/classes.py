"""Character classes for D&D 5E 2024 (levels 1-3 only)."""

from typing import Optional
from ..rules.abilities import Ability, Skill
from ..rules.spells import get_spell_slots_by_level


class CharacterClass:
    """Base class for character classes."""
    
    def __init__(
        self,
        name: str,
        hit_die: str,
        primary_ability: list[Ability],
        saving_throw_proficiencies: list[Ability],
        skill_choices: list[Skill],
        num_skill_choices: int,
        armor_proficiencies: list[str],
        weapon_proficiencies: list[str],
        features_by_level: dict[int, list[str]],
        spellcasting_ability: Optional[Ability] = None,
    ):
        self.name = name
        self.hit_die = hit_die
        self.primary_ability = primary_ability
        self.saving_throw_proficiencies = saving_throw_proficiencies
        self.skill_choices = skill_choices
        self.num_skill_choices = num_skill_choices
        self.armor_proficiencies = armor_proficiencies
        self.weapon_proficiencies = weapon_proficiencies
        self.features_by_level = features_by_level
        self.spellcasting_ability = spellcasting_ability


# Fighter - PHB 2024
FIGHTER = CharacterClass(
    name="Fighter",
    hit_die="1d10",
    primary_ability=[Ability.STRENGTH, Ability.DEXTERITY],
    saving_throw_proficiencies=[Ability.STRENGTH, Ability.CONSTITUTION],
    skill_choices=[
        Skill.ACROBATICS, Skill.ANIMAL_HANDLING, Skill.ATHLETICS,
        Skill.HISTORY, Skill.INSIGHT, Skill.INTIMIDATION,
        Skill.PERCEPTION, Skill.SURVIVAL,
    ],
    num_skill_choices=2,
    armor_proficiencies=["Light", "Medium", "Heavy", "Shields"],
    weapon_proficiencies=["Simple", "Martial"],
    features_by_level={
        1: [
            "Fighting Style: Choose one (Archery, Defense, Dueling, Great Weapon Fighting, Protection, Two-Weapon Fighting)",
            "Second Wind: Bonus action to regain 1d10 + Fighter level HP (once per short/long rest)",
            "Weapon Mastery: Gain mastery with 3 weapons",
        ],
        2: [
            "Action Surge: Take one additional action on your turn (once per short/long rest)",
            "Tactical Mind: When you fail an ability check, you can expend a use of Second Wind to add 1d10 to the check",
        ],
        3: [
            "Martial Archetype: Choose a subclass (Champion, Battle Master, Eldritch Knight, etc.)",
        ],
    },
)

# Rogue - PHB 2024
ROGUE = CharacterClass(
    name="Rogue",
    hit_die="1d8",
    primary_ability=[Ability.DEXTERITY],
    saving_throw_proficiencies=[Ability.DEXTERITY, Ability.INTELLIGENCE],
    skill_choices=[
        Skill.ACROBATICS, Skill.ATHLETICS, Skill.DECEPTION,
        Skill.INSIGHT, Skill.INTIMIDATION, Skill.INVESTIGATION,
        Skill.PERCEPTION, Skill.PERFORMANCE, Skill.PERSUASION,
        Skill.SLEIGHT_OF_HAND, Skill.STEALTH,
    ],
    num_skill_choices=4,
    armor_proficiencies=["Light"],
    weapon_proficiencies=["Simple", "Hand Crossbow", "Longsword", "Rapier", "Shortsword"],
    features_by_level={
        1: [
            "Expertise: Choose two skills you're proficient in; your proficiency bonus is doubled for those skills",
            "Sneak Attack: Once per turn, deal an extra 1d6 damage when you hit with a finesse or ranged weapon and have advantage",
            "Thieves' Cant: You know a secret mix of dialect, jargon, and code",
            "Weapon Mastery: Gain mastery with 2 weapons",
        ],
        2: [
            "Cunning Action: Bonus action to Dash, Disengage, or Hide",
            "Sneak Attack: Increases to 2d6",
        ],
        3: [
            "Roguish Archetype: Choose a subclass (Thief, Assassin, Arcane Trickster, etc.)",
            "Sneak Attack: Increases to 2d6",
            "Steady Aim: Bonus action to gain advantage on your next attack (if you haven't moved this turn)",
        ],
    },
)

# Cleric - PHB 2024
CLERIC = CharacterClass(
    name="Cleric",
    hit_die="1d8",
    primary_ability=[Ability.WISDOM],
    saving_throw_proficiencies=[Ability.WISDOM, Ability.CHARISMA],
    skill_choices=[
        Skill.HISTORY, Skill.INSIGHT, Skill.MEDICINE,
        Skill.PERSUASION, Skill.RELIGION,
    ],
    num_skill_choices=2,
    armor_proficiencies=["Light", "Medium", "Shields"],
    weapon_proficiencies=["Simple"],
    features_by_level={
        1: [
            "Spellcasting: You can cast cleric spells using Wisdom as your spellcasting ability",
            "Divine Domain: Choose a domain (Life, Light, War, etc.)",
            "Channel Divinity: Use divine energy for effects (1/rest at level 1)",
        ],
        2: [
            "Channel Divinity: Gain Turn Undead feature",
            "Harness Divine Power: Bonus action to regain an expended spell slot (once per long rest)",
        ],
        3: [
            "Domain Spells: Gain additional spells from your chosen domain",
        ],
    },
    spellcasting_ability=Ability.WISDOM,
)

# Wizard - PHB 2024
WIZARD = CharacterClass(
    name="Wizard",
    hit_die="1d6",
    primary_ability=[Ability.INTELLIGENCE],
    saving_throw_proficiencies=[Ability.INTELLIGENCE, Ability.WISDOM],
    skill_choices=[
        Skill.ARCANA, Skill.HISTORY, Skill.INSIGHT,
        Skill.INVESTIGATION, Skill.MEDICINE, Skill.RELIGION,
    ],
    num_skill_choices=2,
    armor_proficiencies=[],
    weapon_proficiencies=["Daggers", "Darts", "Slings", "Quarterstaffs", "Light Crossbows"],
    features_by_level={
        1: [
            "Spellcasting: You can cast wizard spells using Intelligence as your spellcasting ability",
            "Arcane Recovery: Once per day during a short rest, recover spell slots (max half your wizard level rounded up)",
            "Ritual Casting: You can cast wizard spells as rituals if they have the ritual tag",
        ],
        2: [
            "Scholar: You gain Expertise in Arcana and History skills",
        ],
        3: [
            "Arcane Tradition: Choose a school of magic (Evocation, Abjuration, etc.)",
        ],
    },
    spellcasting_ability=Ability.INTELLIGENCE,
)

# Dictionary for easy lookup
CLASS_CATALOG: dict[str, CharacterClass] = {
    "Fighter": FIGHTER,
    "Rogue": ROGUE,
    "Cleric": CLERIC,
    "Wizard": WIZARD,
}


def get_character_class(name: str) -> Optional[CharacterClass]:
    """Get a character class by name."""
    return CLASS_CATALOG.get(name)


def get_proficiency_bonus(level: int) -> int:
    """Get proficiency bonus for a character level."""
    if level <= 4:
        return 2
    elif level <= 8:
        return 3
    elif level <= 12:
        return 4
    elif level <= 16:
        return 5
    else:
        return 6
