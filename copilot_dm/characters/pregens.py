"""Pre-generated starter characters for quick play."""

from .character import Character
from ..rules.abilities import Ability, Skill
from ..rules.spells import get_spell_slots_by_level, SpellSlots


# 1. Human Fighter - Ser Aldric the Brave
ALDRIC_FIGHTER = Character(
    name="Ser Aldric",
    level=1,
    character_class="Fighter",
    species="Human",
    background="Soldier",
    
    # Ability scores (standard array + human versatility)
    strength=16,
    dexterity=14,
    constitution=14,
    intelligence=10,
    wisdom=12,
    charisma=8,
    
    # Hit points (1d10 + CON mod)
    max_hp=12,
    current_hp=12,
    hit_dice="1d10",
    hit_dice_remaining=1,
    
    # Combat stats (Chain mail AC 16 + shield +2 = 18)
    armor_class=18,
    speed=30,
    initiative_bonus=2,
    
    # Proficiencies
    proficiency_bonus=2,
    saving_throw_proficiencies=[Ability.STRENGTH, Ability.CONSTITUTION],
    skill_proficiencies=[Skill.ATHLETICS, Skill.INTIMIDATION, Skill.PERCEPTION, Skill.SURVIVAL],
    armor_proficiencies=["Light", "Medium", "Heavy", "Shields"],
    weapon_proficiencies=["Simple", "Martial"],
    
    # Equipment
    weapons=[
        {"name": "Longsword", "damage": "1d8+3", "type": "Melee", "properties": ["Versatile (1d10)"]},
        {"name": "Handaxe", "damage": "1d6+3", "type": "Melee/Ranged", "properties": ["Thrown (20/60)"]},
    ],
    armor={"name": "Chain Mail", "ac": 16, "type": "Heavy"},
    shield=True,
    inventory=["Backpack", "Bedroll", "Rations (5 days)", "Rope (50 ft)", "Tinderbox", "Torch (5)"],
    gold=10,
    
    # Class features
    class_features=[
        "Fighting Style (Defense): +1 AC while wearing armor",
        "Second Wind: Bonus action, regain 1d10+1 HP (1/rest)",
        "Weapon Mastery: Longsword, Handaxe, Javelin",
    ],
    
    # Species traits
    species_traits=[
        "Resourceful: Gain Heroic Inspiration after long rest",
        "Skillful: Extra skill proficiency",
    ],
    
    # Flavor
    personality="Brave and honorable, always ready to defend the weak",
    backstory="A former city guard who left to seek adventure and prove their worth as a true hero.",
)

# 2. Elf Rogue - Whisper
WHISPER_ROGUE = Character(
    name="Whisper",
    level=1,
    character_class="Rogue",
    species="Elf",
    background="Criminal",
    
    # Ability scores
    strength=8,
    dexterity=16,
    constitution=12,
    intelligence=14,
    wisdom=13,
    charisma=10,
    
    # Hit points (1d8 + CON mod)
    max_hp=9,
    current_hp=9,
    hit_dice="1d8",
    hit_dice_remaining=1,
    
    # Combat stats (Leather armor)
    armor_class=14,  # 11 + 3 (DEX)
    speed=30,
    initiative_bonus=3,
    
    # Proficiencies
    proficiency_bonus=2,
    saving_throw_proficiencies=[Ability.DEXTERITY, Ability.INTELLIGENCE],
    skill_proficiencies=[Skill.STEALTH, Skill.SLEIGHT_OF_HAND, Skill.PERCEPTION, Skill.INVESTIGATION, Skill.DECEPTION, Skill.ACROBATICS],
    skill_expertise=[Skill.STEALTH, Skill.SLEIGHT_OF_HAND],  # Expertise
    armor_proficiencies=["Light"],
    weapon_proficiencies=["Simple", "Hand Crossbow", "Longsword", "Rapier", "Shortsword"],
    
    # Equipment
    weapons=[
        {"name": "Rapier", "damage": "1d8+3", "type": "Melee", "properties": ["Finesse"]},
        {"name": "Shortbow", "damage": "1d6+3", "type": "Ranged", "properties": ["Ammunition (80/320)"]},
    ],
    armor={"name": "Leather Armor", "ac": 11, "type": "Light"},
    shield=False,
    inventory=["Thieves' Tools", "Backpack", "Crowbar", "Dark Cloak", "Rations (3 days)", "Arrows (20)"],
    gold=15,
    
    # Class features
    class_features=[
        "Expertise: Double proficiency in Stealth and Sleight of Hand",
        "Sneak Attack: +1d6 damage with advantage or ally nearby",
        "Thieves' Cant: Secret rogue language",
        "Weapon Mastery: Rapier, Shortbow",
    ],
    
    # Species traits
    species_traits=[
        "Darkvision: See in dim light/darkness (60 ft)",
        "Elven Lineage: Advantage vs charm, can't be magically slept",
        "Keen Senses: Proficiency in Perception",
        "Trance: Long rest in 4 hours",
    ],
    
    # Flavor
    personality="Quiet and observant, trusts actions over words",
    backstory="A shadow in the night, seeking redemption for a dark past through noble deeds.",
)

# 3. Dwarf Cleric - Thrain Ironforge
THRAIN_CLERIC = Character(
    name="Thrain Ironforge",
    level=1,
    character_class="Cleric",
    species="Dwarf",
    background="Acolyte",
    
    # Ability scores
    strength=14,
    dexterity=10,
    constitution=14,
    intelligence=10,
    wisdom=16,
    charisma=12,
    
    # Hit points (1d8 + CON mod + Dwarven Toughness)
    max_hp=11,  # 8 + 2 (CON) + 1 (Dwarf)
    current_hp=11,
    hit_dice="1d8",
    hit_dice_remaining=1,
    
    # Combat stats (Scale mail + shield)
    armor_class=16,  # 14 + 0 (DEX) + 2 (shield)
    speed=25,
    initiative_bonus=0,
    
    # Proficiencies
    proficiency_bonus=2,
    saving_throw_proficiencies=[Ability.WISDOM, Ability.CHARISMA],
    skill_proficiencies=[Skill.MEDICINE, Skill.RELIGION, Skill.INSIGHT, Skill.PERSUASION],
    armor_proficiencies=["Light", "Medium", "Shields"],
    weapon_proficiencies=["Simple"],
    
    # Equipment
    weapons=[
        {"name": "Warhammer", "damage": "1d8+2", "type": "Melee", "properties": ["Versatile (1d10)"]},
        {"name": "Light Crossbow", "damage": "1d8", "type": "Ranged", "properties": ["Ammunition (80/320)"]},
    ],
    armor={"name": "Scale Mail", "ac": 14, "type": "Medium"},
    shield=True,
    inventory=["Holy Symbol", "Prayer Book", "Healer's Kit", "Backpack", "Rations (5 days)", "Waterskin"],
    gold=5,
    
    # Spellcasting
    spellcasting_ability=Ability.WISDOM,
    spell_slots=SpellSlots(level_1=2),
    spells_known=["Cure Wounds", "Guiding Bolt", "Bless", "Healing Word"],
    cantrips_known=["Sacred Flame", "Spare the Dying", "Light"],
    
    # Class features
    class_features=[
        "Spellcasting: Wisdom-based divine magic",
        "Divine Domain (Life): Heavy armor proficiency, extra healing",
        "Channel Divinity (1/rest): Preserve Life (heal 5 HP)",
    ],
    
    # Species traits
    species_traits=[
        "Darkvision: See in dim light/darkness (60 ft)",
        "Dwarven Resilience: Advantage vs poison, resist poison damage",
        "Dwarven Toughness: +1 HP per level",
        "Stonecunning: Expertise with stonework history",
    ],
    
    # Flavor
    personality="Stalwart and compassionate, devoted to healing and protecting others",
    backstory="A temple healer who ventured forth to bring divine mercy to the suffering.",
)

# 4. Human Wizard - Elowen the Wise
ELOWEN_WIZARD = Character(
    name="Elowen",
    level=1,
    character_class="Wizard",
    species="Human",
    background="Sage",
    
    # Ability scores
    strength=8,
    dexterity=14,
    constitution=13,
    intelligence=16,
    wisdom=12,
    charisma=10,
    
    # Hit points (1d6 + CON mod)
    max_hp=7,
    current_hp=7,
    hit_dice="1d6",
    hit_dice_remaining=1,
    
    # Combat stats (Mage armor spell or just DEX)
    armor_class=12,  # 10 + 2 (DEX)
    speed=30,
    initiative_bonus=2,
    
    # Proficiencies
    proficiency_bonus=2,
    saving_throw_proficiencies=[Ability.INTELLIGENCE, Ability.WISDOM],
    skill_proficiencies=[Skill.ARCANA, Skill.HISTORY, Skill.INVESTIGATION, Skill.INSIGHT],
    armor_proficiencies=[],
    weapon_proficiencies=["Daggers", "Darts", "Slings", "Quarterstaffs", "Light Crossbows"],
    
    # Equipment
    weapons=[
        {"name": "Quarterstaff", "damage": "1d6-1", "type": "Melee", "properties": ["Versatile (1d8)"]},
        {"name": "Light Crossbow", "damage": "1d8", "type": "Ranged", "properties": ["Ammunition (80/320)"]},
    ],
    armor=None,
    shield=False,
    inventory=["Spellbook", "Component Pouch", "Scholar's Pack", "Ink", "Quill", "Parchment (10)", "Rations (3 days)"],
    gold=10,
    
    # Spellcasting
    spellcasting_ability=Ability.INTELLIGENCE,
    spell_slots=SpellSlots(level_1=2),
    spells_known=["Magic Missile", "Shield", "Mage Armor", "Detect Magic", "Sleep", "Burning Hands"],
    cantrips_known=["Fire Bolt", "Mage Hand", "Prestidigitation"],
    
    # Class features
    class_features=[
        "Spellcasting: Intelligence-based arcane magic",
        "Arcane Recovery: Recover spell slots during short rest (max 1st level)",
        "Ritual Casting: Cast wizard rituals without using slots",
    ],
    
    # Species traits
    species_traits=[
        "Resourceful: Gain Heroic Inspiration after long rest",
        "Skillful: Extra skill proficiency",
    ],
    
    # Flavor
    personality="Curious and analytical, always seeking knowledge and understanding",
    backstory="A scholarly mage who left the safety of the library to test theories in the field.",
)

# 5. Halfling Rogue - Pippin Quickfingers
PIPPIN_ROGUE = Character(
    name="Pippin",
    level=1,
    character_class="Rogue",
    species="Halfling",
    background="Folk Hero",
    
    # Ability scores
    strength=8,
    dexterity=17,
    constitution=14,
    intelligence=10,
    wisdom=13,
    charisma=12,
    
    # Hit points (1d8 + CON mod)
    max_hp=10,
    current_hp=10,
    hit_dice="1d8",
    hit_dice_remaining=1,
    
    # Combat stats
    armor_class=14,  # 11 + 3 (DEX)
    speed=30,
    initiative_bonus=3,
    
    # Proficiencies
    proficiency_bonus=2,
    saving_throw_proficiencies=[Ability.DEXTERITY, Ability.INTELLIGENCE],
    skill_proficiencies=[Skill.STEALTH, Skill.ACROBATICS, Skill.PERCEPTION, Skill.SLEIGHT_OF_HAND, Skill.ANIMAL_HANDLING, Skill.SURVIVAL],
    skill_expertise=[Skill.STEALTH, Skill.PERCEPTION],
    armor_proficiencies=["Light"],
    weapon_proficiencies=["Simple", "Hand Crossbow", "Longsword", "Rapier", "Shortsword"],
    
    # Equipment
    weapons=[
        {"name": "Shortsword", "damage": "1d6+3", "type": "Melee", "properties": ["Finesse", "Light"]},
        {"name": "Dagger", "damage": "1d4+3", "type": "Melee/Ranged", "properties": ["Finesse", "Light", "Thrown (20/60)"]},
    ],
    armor={"name": "Leather Armor", "ac": 11, "type": "Light"},
    shield=False,
    inventory=["Thieves' Tools", "Backpack", "Bell", "Rations (5 days)", "Rope (50 ft)", "Sling"],
    gold=10,
    
    # Class features
    class_features=[
        "Expertise: Double proficiency in Stealth and Perception",
        "Sneak Attack: +1d6 damage with advantage or ally nearby",
        "Thieves' Cant: Secret rogue language",
        "Weapon Mastery: Shortsword, Dagger",
    ],
    
    # Species traits
    species_traits=[
        "Brave: Advantage vs frightened condition",
        "Halfling Nimbleness: Move through larger creatures' spaces",
        "Luck: Reroll natural 1s on d20 rolls",
        "Naturally Stealthy: Hide behind larger creatures",
    ],
    
    # Flavor
    personality="Cheerful and brave, never backs down from a challenge despite their size",
    backstory="A village hero who stood up to local bandits and now seeks greater adventures.",
)

# Pre-gen catalog
PREGENERATED_CHARACTERS: dict[str, Character] = {
    "Ser Aldric (Human Fighter)": ALDRIC_FIGHTER,
    "Whisper (Elf Rogue)": WHISPER_ROGUE,
    "Thrain (Dwarf Cleric)": THRAIN_CLERIC,
    "Elowen (Human Wizard)": ELOWEN_WIZARD,
    "Pippin (Halfling Rogue)": PIPPIN_ROGUE,
}


def get_pregen_character(name: str) -> Character:
    """Get a pre-generated character by name."""
    return PREGENERATED_CHARACTERS[name].model_copy(deep=True)


def list_pregen_characters() -> list[str]:
    """List all available pre-generated character names."""
    return list(PREGENERATED_CHARACTERS.keys())
