"""Bestiary of monsters appropriate for levels 1-3."""

from .monster import Monster
from ..rules.abilities import Ability


# CR 1/8 - Perfect for level 1
GOBLIN = Monster(
    name="Goblin",
    size="Small",
    creature_type="Humanoid (Goblinoid)",
    alignment="Neutral Evil",
    challenge_rating=0.25,
    xp_value=50,
    
    # Abilities
    strength=8,
    dexterity=14,
    constitution=10,
    intelligence=10,
    wisdom=8,
    charisma=8,
    
    # Combat stats
    armor_class=15,  # Leather + shield
    max_hp=7,
    current_hp=7,
    hit_dice="2d6",
    speed=30,
    
    # Skills
    skill_bonuses={"Stealth": 6},
    passive_perception=9,
    
    # Senses
    darkvision=60,
    
    # Languages
    languages=["Common", "Goblin"],
    
    # Traits
    traits=[
        {"name": "Nimble Escape", "description": "The goblin can take the Disengage or Hide action as a bonus action on each of its turns."},
    ],
    
    # Actions
    actions=[
        {
            "name": "Scimitar",
            "type": "melee",
            "attack_bonus": 4,
            "damage": "1d6+2",
            "damage_type": "slashing",
            "reach": 5,
        },
        {
            "name": "Shortbow",
            "type": "ranged",
            "attack_bonus": 4,
            "damage": "1d6+2",
            "damage_type": "piercing",
            "range": "80/320",
        },
    ],
)

# CR 1/4
WOLF = Monster(
    name="Wolf",
    size="Medium",
    creature_type="Beast",
    alignment="Unaligned",
    challenge_rating=0.25,
    xp_value=50,
    
    # Abilities
    strength=12,
    dexterity=15,
    constitution=12,
    intelligence=3,
    wisdom=12,
    charisma=6,
    
    # Combat stats
    armor_class=13,
    max_hp=11,
    current_hp=11,
    hit_dice="2d8+2",
    speed=40,
    
    # Skills
    skill_bonuses={"Perception": 3, "Stealth": 4},
    passive_perception=13,
    
    # Traits
    traits=[
        {"name": "Keen Hearing and Smell", "description": "The wolf has advantage on Wisdom (Perception) checks that rely on hearing or smell."},
        {"name": "Pack Tactics", "description": "The wolf has advantage on attack rolls against a creature if at least one of the wolf's allies is within 5 feet of the creature and the ally isn't incapacitated."},
    ],
    
    # Actions
    actions=[
        {
            "name": "Bite",
            "type": "melee",
            "attack_bonus": 4,
            "damage": "2d4+2",
            "damage_type": "piercing",
            "reach": 5,
            "special": "If the target is a creature, it must succeed on a DC 11 Strength saving throw or be knocked prone.",
        },
    ],
)

# CR 1/2
ORC = Monster(
    name="Orc",
    size="Medium",
    creature_type="Humanoid (Orc)",
    alignment="Chaotic Evil",
    challenge_rating=0.5,
    xp_value=100,
    
    # Abilities
    strength=16,
    dexterity=12,
    constitution=16,
    intelligence=7,
    wisdom=11,
    charisma=10,
    
    # Combat stats
    armor_class=13,  # Hide armor
    max_hp=15,
    current_hp=15,
    hit_dice="2d8+6",
    speed=30,
    
    # Skills
    skill_bonuses={"Intimidation": 2},
    passive_perception=10,
    
    # Senses
    darkvision=60,
    
    # Languages
    languages=["Common", "Orc"],
    
    # Traits
    traits=[
        {"name": "Aggressive", "description": "As a bonus action, the orc can move up to its speed toward a hostile creature that it can see."},
    ],
    
    # Actions
    actions=[
        {
            "name": "Greataxe",
            "type": "melee",
            "attack_bonus": 5,
            "damage": "1d12+3",
            "damage_type": "slashing",
            "reach": 5,
        },
        {
            "name": "Javelin",
            "type": "melee_or_ranged",
            "attack_bonus": 5,
            "damage": "1d6+3",
            "damage_type": "piercing",
            "reach": 5,
            "range": "30/120",
        },
    ],
)

# CR 1/2
ZOMBIE = Monster(
    name="Zombie",
    size="Medium",
    creature_type="Undead",
    alignment="Neutral Evil",
    challenge_rating=0.25,
    xp_value=50,
    
    # Abilities
    strength=13,
    dexterity=6,
    constitution=16,
    intelligence=3,
    wisdom=6,
    charisma=5,
    
    # Combat stats
    armor_class=8,
    max_hp=22,
    current_hp=22,
    hit_dice="3d8+9",
    speed=20,
    
    # Saves
    saving_throw_bonuses={Ability.WISDOM: 0},
    
    # Immunities
    damage_immunities=["poison"],
    condition_immunities=["poisoned"],
    
    # Senses
    darkvision=60,
    passive_perception=8,
    
    # Languages
    languages=["Understands languages it knew in life but can't speak"],
    
    # Traits
    traits=[
        {"name": "Undead Fortitude", "description": "If damage reduces the zombie to 0 HP, it must make a Constitution saving throw with a DC of 5 + the damage taken, unless the damage is radiant or from a critical hit. On a success, the zombie drops to 1 HP instead."},
    ],
    
    # Actions
    actions=[
        {
            "name": "Slam",
            "type": "melee",
            "attack_bonus": 3,
            "damage": "1d6+1",
            "damage_type": "bludgeoning",
            "reach": 5,
        },
    ],
)

# CR 1
GIANT_SPIDER = Monster(
    name="Giant Spider",
    size="Large",
    creature_type="Beast",
    alignment="Unaligned",
    challenge_rating=1,
    xp_value=200,
    
    # Abilities
    strength=14,
    dexterity=16,
    constitution=12,
    intelligence=2,
    wisdom=11,
    charisma=4,
    
    # Combat stats
    armor_class=14,
    max_hp=26,
    current_hp=26,
    hit_dice="4d10+4",
    speed=30,
    
    # Skills
    skill_bonuses={"Stealth": 7},
    passive_perception=10,
    
    # Senses
    blindsight=10,
    darkvision=60,
    
    # Traits
    traits=[
        {"name": "Spider Climb", "description": "The spider can climb difficult surfaces, including upside down on ceilings, without needing to make an ability check."},
        {"name": "Web Sense", "description": "While in contact with a web, the spider knows the exact location of any other creature in contact with the same web."},
        {"name": "Web Walker", "description": "The spider ignores movement restrictions caused by webbing."},
    ],
    
    # Actions
    actions=[
        {
            "name": "Bite",
            "type": "melee",
            "attack_bonus": 5,
            "damage": "1d8+3",
            "damage_type": "piercing",
            "reach": 5,
            "special": "Plus 2d8 poison damage (DC 11 CON save for half).",
        },
        {
            "name": "Web",
            "type": "ranged",
            "attack_bonus": 5,
            "damage": "0",
            "damage_type": "special",
            "range": "30/60",
            "special": "Target is restrained by webbing (DC 12 STR check to escape, AC 10, 5 HP, vulnerable to fire).",
        },
    ],
)

# CR 1
BUGBEAR = Monster(
    name="Bugbear",
    size="Medium",
    creature_type="Humanoid (Goblinoid)",
    alignment="Chaotic Evil",
    challenge_rating=1,
    xp_value=200,
    
    # Abilities
    strength=15,
    dexterity=14,
    constitution=13,
    intelligence=8,
    wisdom=11,
    charisma=9,
    
    # Combat stats
    armor_class=16,  # Hide armor + shield
    max_hp=27,
    current_hp=27,
    hit_dice="5d8+5",
    speed=30,
    
    # Skills
    skill_bonuses={"Stealth": 6, "Survival": 2},
    passive_perception=10,
    
    # Senses
    darkvision=60,
    
    # Languages
    languages=["Common", "Goblin"],
    
    # Traits
    traits=[
        {"name": "Brute", "description": "A melee weapon deals one extra die of its damage when the bugbear hits with it (included in the attack)."},
        {"name": "Surprise Attack", "description": "If the bugbear surprises a creature and hits it with an attack during the first round of combat, the target takes an extra 7 (2d6) damage from the attack."},
    ],
    
    # Actions
    actions=[
        {
            "name": "Morningstar",
            "type": "melee",
            "attack_bonus": 4,
            "damage": "2d8+2",
            "damage_type": "piercing",
            "reach": 5,
        },
        {
            "name": "Javelin",
            "type": "melee_or_ranged",
            "attack_bonus": 4,
            "damage": "2d6+2",
            "damage_type": "piercing",
            "reach": 5,
            "range": "30/120",
        },
    ],
)

# CR 2 - Boss for level 1-2 party
OGRE = Monster(
    name="Ogre",
    size="Large",
    creature_type="Giant",
    alignment="Chaotic Evil",
    challenge_rating=2,
    xp_value=450,
    
    # Abilities
    strength=19,
    dexterity=8,
    constitution=16,
    intelligence=5,
    wisdom=7,
    charisma=7,
    
    # Combat stats
    armor_class=11,  # Hide armor
    max_hp=59,
    current_hp=59,
    hit_dice="7d10+21",
    speed=40,
    
    # Senses
    darkvision=60,
    passive_perception=8,
    
    # Languages
    languages=["Common", "Giant"],
    
    # Actions
    actions=[
        {
            "name": "Greatclub",
            "type": "melee",
            "attack_bonus": 6,
            "damage": "2d8+4",
            "damage_type": "bludgeoning",
            "reach": 5,
        },
        {
            "name": "Javelin",
            "type": "melee_or_ranged",
            "attack_bonus": 6,
            "damage": "2d6+4",
            "damage_type": "piercing",
            "reach": 5,
            "range": "30/120",
        },
    ],
)

# CR 2
WEREWOLF = Monster(
    name="Werewolf",
    size="Medium",
    creature_type="Humanoid (Human, Shapechanger)",
    alignment="Chaotic Evil",
    challenge_rating=3,
    xp_value=700,
    
    # Abilities
    strength=15,
    dexterity=13,
    constitution=14,
    intelligence=10,
    wisdom=11,
    charisma=10,
    
    # Combat stats
    armor_class=12,  # Natural armor (hybrid/wolf form)
    max_hp=58,
    current_hp=58,
    hit_dice="9d8+18",
    speed=30,
    
    # Skills
    skill_bonuses={"Perception": 4, "Stealth": 3},
    passive_perception=14,
    
    # Immunities
    damage_immunities=["Bludgeoning, Piercing, and Slashing from nonmagical attacks not made with silvered weapons"],
    
    # Senses
    darkvision=60,
    
    # Languages
    languages=["Common (can't speak in wolf form)"],
    
    # Traits
    traits=[
        {"name": "Shapechanger", "description": "The werewolf can use its action to polymorph into a wolf-humanoid hybrid or into a wolf, or back into its true form (humanoid). Its statistics are the same in each form."},
        {"name": "Keen Hearing and Smell", "description": "The werewolf has advantage on Wisdom (Perception) checks that rely on hearing or smell."},
    ],
    
    # Actions
    actions=[
        {
            "name": "Multiattack (Hybrid form only)",
            "type": "special",
            "description": "The werewolf makes two attacks: one with its bite and one with its claws or spear.",
        },
        {
            "name": "Bite (Wolf or Hybrid form only)",
            "type": "melee",
            "attack_bonus": 4,
            "damage": "1d8+2",
            "damage_type": "piercing",
            "reach": 5,
            "special": "Target must succeed on a DC 12 CON save or be cursed with werewolf lycanthropy.",
        },
        {
            "name": "Claws (Hybrid form only)",
            "type": "melee",
            "attack_bonus": 4,
            "damage": "2d4+2",
            "damage_type": "slashing",
            "reach": 5,
        },
        {
            "name": "Spear (Humanoid form only)",
            "type": "melee_or_ranged",
            "attack_bonus": 4,
            "damage": "1d6+2",  # 1d8+2 if two-handed
            "damage_type": "piercing",
            "reach": 5,
            "range": "20/60",
        },
    ],
)

# Bestiary catalog
BESTIARY: dict[str, Monster] = {
    "Goblin": GOBLIN,
    "Wolf": WOLF,
    "Orc": ORC,
    "Zombie": ZOMBIE,
    "Giant Spider": GIANT_SPIDER,
    "Bugbear": BUGBEAR,
    "Ogre": OGRE,
    "Werewolf": WEREWOLF,
}


def get_monster(name: str) -> Monster:
    """Get a monster by name (returns a copy)."""
    if name not in BESTIARY:
        raise ValueError(f"Monster '{name}' not found in bestiary")
    return BESTIARY[name].model_copy(deep=True)


def list_monsters() -> list[str]:
    """List all available monster names."""
    return list(BESTIARY.keys())


def get_monsters_by_cr(max_cr: float) -> list[str]:
    """Get all monsters with CR at or below the specified value."""
    return [name for name, monster in BESTIARY.items() if monster.challenge_rating <= max_cr]
