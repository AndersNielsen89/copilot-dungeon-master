"""Species (races) for D&D 5E 2024."""

from typing import Optional
from ..rules.abilities import Ability


class Species:
    """Base class for character species."""
    
    def __init__(
        self,
        name: str,
        speed: int,
        size: str,
        traits: list[str],
        languages: list[str],
    ):
        self.name = name
        self.speed = speed
        self.size = size
        self.traits = traits
        self.languages = languages


# PHB 2024 species (no ASI bonuses - those come from background/class)

HUMAN = Species(
    name="Human",
    speed=30,
    size="Medium",
    traits=[
        "Resourceful: You gain Heroic Inspiration whenever you finish a Long Rest.",
        "Skillful: You gain proficiency in one skill of your choice.",
        "Versatile: You gain an Origin feat of your choice.",
    ],
    languages=["Common", "One additional language of your choice"],
)

ELF = Species(
    name="Elf",
    speed=30,
    size="Medium",
    traits=[
        "Darkvision: You can see in dim light within 60 feet as if it were bright light, and in darkness as if it were dim light.",
        "Elven Lineage: You have advantage on saving throws against being charmed, and magic can't put you to sleep.",
        "Fey Ancestry: You count as a Fey creature.",
        "Keen Senses: You have proficiency in the Perception skill.",
        "Trance: You don't need to sleep, and magic can't put you to sleep. You can finish a long rest in 4 hours.",
    ],
    languages=["Common", "Elven"],
)

DWARF = Species(
    name="Dwarf",
    speed=25,  # Not reduced by heavy armor
    size="Medium",
    traits=[
        "Darkvision: You can see in dim light within 60 feet as if it were bright light, and in darkness as if it were dim light.",
        "Dwarven Resilience: You have advantage on saving throws against poison and resistance to poison damage.",
        "Dwarven Toughness: Your hit point maximum increases by 1, and it increases by 1 again whenever you gain a level.",
        "Forge Wise: Your walking speed is not reduced by wearing Heavy Armor.",
        "Stonecunning: Whenever you make an Intelligence (History) check related to the origin of stonework, you are considered proficient and add double your proficiency bonus.",
    ],
    languages=["Common", "Dwarvish"],
)

HALFLING = Species(
    name="Halfling",
    speed=30,
    size="Small",
    traits=[
        "Brave: You have advantage on saving throws against being frightened.",
        "Halfling Nimbleness: You can move through the space of any creature that is a size larger than you.",
        "Luck: When you roll a 1 on a d20 for an attack roll, ability check, or saving throw, you can reroll the die and must use the new roll.",
        "Naturally Stealthy: You can attempt to hide even when you are obscured only by a creature that is at least one size larger than you.",
    ],
    languages=["Common", "Halfling"],
)

TIEFLING = Species(
    name="Tiefling",
    speed=30,
    size="Medium",
    traits=[
        "Darkvision: You can see in dim light within 60 feet as if it were bright light, and in darkness as if it were dim light.",
        "Fiendish Legacy: You are resistant to fire damage.",
        "Otherworldly Presence: You know the Thaumaturgy cantrip. Starting at 3rd level, you can cast Hellish Rebuke once per long rest as a 2nd-level spell. Charisma is your spellcasting ability for these spells.",
    ],
    languages=["Common", "Infernal"],
)

# Dictionary for easy lookup
SPECIES_CATALOG: dict[str, Species] = {
    "Human": HUMAN,
    "Elf": ELF,
    "Dwarf": DWARF,
    "Halfling": HALFLING,
    "Tiefling": TIEFLING,
}


def get_species(name: str) -> Optional[Species]:
    """Get a species by name."""
    return SPECIES_CATALOG.get(name)
