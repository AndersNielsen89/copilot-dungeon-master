"""Copilot tools for DM to enforce D&D 5E 2024 rules."""

from typing import Optional, Literal

from ..rules.dice import roll_d20, roll_dice, roll_damage, RollType, DiceType
from ..rules.abilities import ability_check, saving_throw, skill_check, Skill, Ability, calculate_modifier
from ..rules.combat import attack_roll, damage_roll, calculate_ac
from ..game.state import GameState


def create_dm_tools(game_state: GameState) -> list:
    """Create all DM tools for the Copilot agent."""
    
    tools = []
    
    # Dice rolling tool
    def roll_dice_tool(
        dice_type: Literal["d4", "d6", "d8", "d10", "d12", "d20", "d100"],
        num_dice: int = 1,
        modifier: int = 0,
        advantage: bool = False,
        disadvantage: bool = False,
    ) -> str:
        """Roll dice (d4, d6, d8, d10, d12, d20, d100). Use for any dice roll needed."""
        dice_map = {
            "d4": DiceType.D4,
            "d6": DiceType.D6,
            "d8": DiceType.D8,
            "d10": DiceType.D10,
            "d12": DiceType.D12,
            "d20": DiceType.D20,
            "d100": DiceType.D100,
        }
        
        roll_type = RollType.NORMAL
        if advantage:
            roll_type = RollType.ADVANTAGE
        elif disadvantage:
            roll_type = RollType.DISADVANTAGE
        
        if dice_type == "d20":
            result = roll_d20(modifier, roll_type)
        else:
            result = roll_dice(dice_map[dice_type], num_dice, modifier)
        
        output = f"Rolled {num_dice}{dice_type}"
        if modifier > 0:
            output += f"+{modifier}"
        elif modifier < 0:
            output += f"{modifier}"
        
        if advantage:
            output += " (with advantage)"
        elif disadvantage:
            output += " (with disadvantage)"
        
        output += f": {result}"
        
        if result.is_critical():
            output += " - CRITICAL SUCCESS!"
        elif result.is_fumble():
            output += " - CRITICAL FAILURE!"
        
        return output
    
    tools.append(roll_dice_tool)
    
    # Ability/Skill check tool
    def ability_check_tool(
        ability: Literal["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"],
        dc: int,
        skill: Optional[str] = None,
        advantage: bool = False,
        disadvantage: bool = False,
    ) -> str:
        """
        Make an ability check or skill check for the player character.
        
        For skill checks, provide the skill name (e.g., "Stealth", "Investigation", "Perception").
        The character's proficiency and expertise will be automatically applied.
        """
        if not game_state.player:
            return "Error: No player character set"
        
        ability_map = {
            "Strength": Ability.STRENGTH,
            "Dexterity": Ability.DEXTERITY,
            "Constitution": Ability.CONSTITUTION,
            "Intelligence": Ability.INTELLIGENCE,
            "Wisdom": Ability.WISDOM,
            "Charisma": Ability.CHARISMA,
        }
        
        roll_type = RollType.ADVANTAGE if advantage else (RollType.DISADVANTAGE if disadvantage else RollType.NORMAL)
        ability_obj = ability_map[ability]
        ability_score = game_state.player.get_ability_score(ability_obj)
        
        # If skill specified, do skill check with proficiency
        if skill:
            try:
                skill_key = skill.upper().replace(" ", "_")
                skill_obj = Skill[skill_key]
                proficient = game_state.player.is_proficient_in_skill(skill_obj)
                expertise = game_state.player.has_expertise_in_skill(skill_obj)
                
                roll, success = skill_check(
                    skill_obj,
                    game_state.player.get_all_ability_scores(),
                    game_state.player.proficiency_bonus,
                    proficient,
                    expertise,
                    roll_type,
                    dc,
                )
                
                # Build detailed output showing proficiency
                modifier = calculate_modifier(game_state.player.get_ability_score(skill_obj.ability))
                prof_str = ""
                if expertise:
                    modifier += game_state.player.proficiency_bonus * 2
                    prof_str = " [EXPERTISE +4]"
                elif proficient:
                    modifier += game_state.player.proficiency_bonus
                    prof_str = " [PROFICIENT +2]"
                
                output = f"{game_state.player.name} makes a {skill} check ({ability}){prof_str}: {roll} vs DC {dc}"
            except KeyError:
                return f"Error: Invalid skill '{skill}'. Valid skills: Stealth, Perception, Investigation, Athletics, Acrobatics, etc."
        else:
            # Raw ability check
            roll, success = ability_check(
                ability_score,
                game_state.player.proficiency_bonus,
                False,
                False,
                roll_type,
                dc,
            )
            
            output = f"{game_state.player.name} makes a {ability} check: {roll} vs DC {dc}"
        
        if success:
            output += " - SUCCESS!"
        else:
            output += " - FAILURE"
        
        return output
    
    tools.append(ability_check_tool)
    
    # Saving throw tool
    def saving_throw_tool(
        ability: Literal["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"],
        dc: int,
        target: str = "player",
        advantage: bool = False,
        disadvantage: bool = False,
    ) -> str:
        """Make a saving throw for the player character or a monster."""
        if target.lower() == "player":
            if not game_state.player:
                return "Error: No player character set"
            
            creature = game_state.player
            ability_map = {
                "Strength": Ability.STRENGTH,
                "Dexterity": Ability.DEXTERITY,
                "Constitution": Ability.CONSTITUTION,
                "Intelligence": Ability.INTELLIGENCE,
                "Wisdom": Ability.WISDOM,
                "Charisma": Ability.CHARISMA,
            }
            ability_obj = ability_map[ability]
            ability_score = creature.get_ability_score(ability_obj)
            proficient = creature.is_proficient_in_save(ability_obj)
            
            roll_type = RollType.ADVANTAGE if advantage else (RollType.DISADVANTAGE if disadvantage else RollType.NORMAL)
            
            roll, success = saving_throw(
                ability_score,
                creature.proficiency_bonus,
                proficient,
                roll_type,
                dc,
            )
            
            prof_str = " [PROFICIENT +2]" if proficient else ""
            output = f"{creature.name} makes a {ability} saving throw{prof_str}: {roll} vs DC {dc}"
            
            if success:
                output += " - SUCCESS!"
            else:
                output += " - FAILURE"
            
            return output
        else:
            return "Monster saving throws not yet implemented"
    
    tools.append(saving_throw_tool)
    
    # Attack roll tool
    def attack_roll_tool(
        attacker: str,
        target: str,
        attack_bonus: int,
        target_ac: int,
        advantage: bool = False,
        disadvantage: bool = False,
    ) -> str:
        """Make an attack roll for the player or a monster."""
        roll_type = RollType.ADVANTAGE if advantage else (RollType.DISADVANTAGE if disadvantage else RollType.NORMAL)
        
        roll, hit, critical = attack_roll(attack_bonus, roll_type, target_ac)
        
        output = f"{attacker} attacks {target}: {roll} vs AC {target_ac}"
        
        if critical:
            output += " - CRITICAL HIT!"
        elif hit:
            output += " - HIT!"
        else:
            output += " - MISS"
        
        return output
    
    tools.append(attack_roll_tool)
    
    # Damage roll tool
    def damage_roll_tool(
        damage_dice: str,
        critical: bool = False,
    ) -> str:
        """Roll damage dice (e.g., '1d8+3', '2d6', '3d10-1')."""
        try:
            result = damage_roll(damage_dice, critical)
            output = f"Damage: {result}"
            if critical:
                output += " (CRITICAL - doubled dice)"
            return output
        except Exception as e:
            return f"Error rolling damage: {e}"
    
    tools.append(damage_roll_tool)
    
    # Apply damage tool
    def apply_damage_tool(
        target: str,
        damage: int,
        damage_type: str = "untyped",
    ) -> str:
        """Apply damage to the player character or a creature in combat."""
        if target.lower() == "player" or (game_state.player and target.lower() == game_state.player.name.lower()):
            actual_damage = game_state.player.take_damage(damage)
            output = f"{game_state.player.name} takes {actual_damage} {damage_type} damage. "
            output += f"HP: {game_state.player.current_hp}/{game_state.player.max_hp}"
            
            if game_state.player.current_hp <= 0:
                output += " - DOWN!"
            
            return output
        else:
            # Find target in combat
            if game_state.current_combat:
                combatant = game_state.current_combat.get_combatant_by_name(target)
                if combatant:
                    actual_damage = combatant.creature.take_damage(damage)
                    current_hp, max_hp = combatant.get_hp()
                    output = f"{target} takes {actual_damage} {damage_type} damage. HP: {current_hp}/{max_hp}"
                    
                    if current_hp <= 0:
                        output += " - DEFEATED!"
                    
                    return output
            
            return f"Error: Target '{target}' not found"
    
    tools.append(apply_damage_tool)
    
    # Heal tool
    def heal_tool(
        target: str,
        healing: int,
    ) -> str:
        """Heal the player character or another creature."""
        if target.lower() == "player" or (game_state.player and target.lower() == game_state.player.name.lower()):
            actual_healing = game_state.player.heal(healing)
            output = f"{game_state.player.name} heals {actual_healing} HP. "
            output += f"HP: {game_state.player.current_hp}/{game_state.player.max_hp}"
            return output
        else:
            return f"Healing for '{target}' not yet implemented"
    
    tools.append(heal_tool)
    
    # Get character info tool - includes proficiencies
    def get_character_info_tool() -> str:
        """Get information about the player character (stats, HP, equipment, proficiencies, etc.)."""
        if not game_state.player:
            return "No player character set"
        
        char = game_state.player
        
        # Format saving throw proficiencies
        save_profs = [a.value for a in char.saving_throw_proficiencies]
        
        # Build skill list with ALL skills showing modifier, ability, and proficiency status
        skill_lines = []
        for skill in Skill:
            mod = char.get_skill_modifier(skill)
            mod_str = f"+{mod}" if mod >= 0 else str(mod)
            ability_abbrev = skill.ability.value[:3].upper()
            
            if char.has_expertise_in_skill(skill):
                prof_marker = " [E]"  # Expertise
            elif char.is_proficient_in_skill(skill):
                prof_marker = " [P]"  # Proficient
            else:
                prof_marker = ""
            
            skill_lines.append(f"  {skill.skill_name} ({ability_abbrev}): {mod_str}{prof_marker}")
        
        info = f"""
{char.name} - Level {char.level} {char.species} {char.character_class}
Background: {char.background}

HP: {char.current_hp}/{char.max_hp}
AC: {char.armor_class}
Speed: {char.speed} ft
Proficiency Bonus: +{char.proficiency_bonus}

ABILITY SCORES:
  STR {char.strength} ({'+' if calculate_modifier(char.strength) >= 0 else ''}{calculate_modifier(char.strength)})
  DEX {char.dexterity} ({'+' if calculate_modifier(char.dexterity) >= 0 else ''}{calculate_modifier(char.dexterity)})
  CON {char.constitution} ({'+' if calculate_modifier(char.constitution) >= 0 else ''}{calculate_modifier(char.constitution)})
  INT {char.intelligence} ({'+' if calculate_modifier(char.intelligence) >= 0 else ''}{calculate_modifier(char.intelligence)})
  WIS {char.wisdom} ({'+' if calculate_modifier(char.wisdom) >= 0 else ''}{calculate_modifier(char.wisdom)})
  CHA {char.charisma} ({'+' if calculate_modifier(char.charisma) >= 0 else ''}{calculate_modifier(char.charisma)})

SAVING THROWS (Proficient: {', '.join(save_profs) if save_profs else 'None'}):
  STR: {'+' if calculate_modifier(char.strength) + (char.proficiency_bonus if Ability.STRENGTH in char.saving_throw_proficiencies else 0) >= 0 else ''}{calculate_modifier(char.strength) + (char.proficiency_bonus if Ability.STRENGTH in char.saving_throw_proficiencies else 0)}{'*' if Ability.STRENGTH in char.saving_throw_proficiencies else ''}
  DEX: {'+' if calculate_modifier(char.dexterity) + (char.proficiency_bonus if Ability.DEXTERITY in char.saving_throw_proficiencies else 0) >= 0 else ''}{calculate_modifier(char.dexterity) + (char.proficiency_bonus if Ability.DEXTERITY in char.saving_throw_proficiencies else 0)}{'*' if Ability.DEXTERITY in char.saving_throw_proficiencies else ''}
  CON: {'+' if calculate_modifier(char.constitution) + (char.proficiency_bonus if Ability.CONSTITUTION in char.saving_throw_proficiencies else 0) >= 0 else ''}{calculate_modifier(char.constitution) + (char.proficiency_bonus if Ability.CONSTITUTION in char.saving_throw_proficiencies else 0)}{'*' if Ability.CONSTITUTION in char.saving_throw_proficiencies else ''}
  INT: {'+' if calculate_modifier(char.intelligence) + (char.proficiency_bonus if Ability.INTELLIGENCE in char.saving_throw_proficiencies else 0) >= 0 else ''}{calculate_modifier(char.intelligence) + (char.proficiency_bonus if Ability.INTELLIGENCE in char.saving_throw_proficiencies else 0)}{'*' if Ability.INTELLIGENCE in char.saving_throw_proficiencies else ''}
  WIS: {'+' if calculate_modifier(char.wisdom) + (char.proficiency_bonus if Ability.WISDOM in char.saving_throw_proficiencies else 0) >= 0 else ''}{calculate_modifier(char.wisdom) + (char.proficiency_bonus if Ability.WISDOM in char.saving_throw_proficiencies else 0)}{'*' if Ability.WISDOM in char.saving_throw_proficiencies else ''}
  CHA: {'+' if calculate_modifier(char.charisma) + (char.proficiency_bonus if Ability.CHARISMA in char.saving_throw_proficiencies else 0) >= 0 else ''}{calculate_modifier(char.charisma) + (char.proficiency_bonus if Ability.CHARISMA in char.saving_throw_proficiencies else 0)}{'*' if Ability.CHARISMA in char.saving_throw_proficiencies else ''}

SKILLS ([P]=Proficient, [E]=Expertise):
{chr(10).join(skill_lines)}

EQUIPMENT:
  Weapons: {', '.join(w['name'] for w in char.weapons)}
  Armor: {char.armor['name'] if char.armor else 'None'}
  Shield: {'Yes' if char.shield else 'No'}
  Gold: {char.gold} gp
"""
        
        if char.spells_known:
            slots = char.spell_slots
            slot_info = []
            for level in range(1, 10):
                total = getattr(slots, f"level_{level}")
                if total > 0:
                    available = slots.get_available(level)
                    slot_info.append(f"Lv{level}: {available}/{total}")
            
            info += f"\nSPELLS:"
            info += f"\n  Spell Slots: {', '.join(slot_info)}"
            info += f"\n  Cantrips: {', '.join(char.cantrips_known)}"
            info += f"\n  Prepared: {', '.join(char.spells_known)}"
        
        return info.strip()
    
    tools.append(get_character_info_tool)
    
    return tools
