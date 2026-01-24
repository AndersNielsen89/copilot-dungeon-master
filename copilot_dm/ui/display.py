"""Rich-based terminal display components."""

import re
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.layout import Layout
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn
from typing import Optional

from ..characters.character import Character
from ..monsters.monster import Monster
from ..game.combat import CombatEncounter, Combatant


console = Console()


def display_title() -> None:
    """Display the game title."""
    title = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║                THE COPILOT DUNGEON MASTER                 ║
║                                                           ║
║        A Solitary D&D 5E Campaign (2024 Rules)            ║
║                                                           ║
║         The Dungeon Remembers. Roll Carefully.            ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝

    """
    console.print(title, style="bold cyan")


def display_character_status(character: Character) -> None:
    """Display character status panel."""
    hp_color = "green" if character.current_hp > character.max_hp // 2 else "yellow"
    if character.current_hp <= character.max_hp // 4:
        hp_color = "red"
    
    status_text = f"""[bold]{character.name}[/bold] - Level {character.level} {character.species} {character.character_class}

[bold]HP:[/bold] [{hp_color}]{character.current_hp}/{character.max_hp}[/{hp_color}]  [bold]AC:[/bold] {character.armor_class}  [bold]Speed:[/bold] {character.speed} ft

[bold]Ability Scores:[/bold]
STR {character.strength} | DEX {character.dexterity} | CON {character.constitution}
INT {character.intelligence} | WIS {character.wisdom} | CHA {character.charisma}
"""
    
    # Add conditions if any
    active_conditions = character.conditions.get_active_conditions()
    if active_conditions:
        status_text += f"\n[bold red]Conditions:[/bold red] {', '.join(c.value for c in active_conditions)}"
    
    panel = Panel(status_text, title="Character Status", border_style="blue")
    console.print(panel)


def display_combat_status(encounter: CombatEncounter) -> None:
    """Display combat status with initiative order."""
    table = Table(title=f"⚔️  Combat - Round {encounter.round_number}", show_header=True, header_style="bold magenta")
    table.add_column("Init", style="cyan", width=6)
    table.add_column("Name", style="white")
    table.add_column("HP", style="green")
    table.add_column("Status", style="yellow")
    
    for combatant in encounter.combatants:
        name = combatant.get_name()
        if combatant == encounter.get_current_combatant():
            name = f"▶ {name}"
        
        current_hp, max_hp = combatant.get_hp()
        hp_display = f"{current_hp}/{max_hp}"
        
        # Status indicators
        status_parts = []
        if not combatant.has_action:
            status_parts.append("Used Action")
        if not combatant.has_bonus_action:
            status_parts.append("Used Bonus")
        if not combatant.has_reaction:
            status_parts.append("No Reaction")
        
        status = ", ".join(status_parts) if status_parts else "Ready"
        
        table.add_row(
            str(combatant.initiative),
            name,
            hp_display,
            status,
        )
    
    console.print(table)


def display_dice_roll(description: str, roll: object, success: Optional[bool] = None) -> None:
    """Display a dice roll with formatting."""
    from ..rules.dice import DiceRoll
    
    if not isinstance(roll, DiceRoll):
        return
    
    result_text = f"[bold]{description}[/bold]\n"
    result_text += f"Roll: {roll}\n"
    
    if roll.is_critical():
        result_text += "[bold green]⭐ CRITICAL HIT! ⭐[/bold green]\n"
    elif roll.is_fumble():
        result_text += "[bold red]💀 CRITICAL MISS! 💀[/bold red]\n"
    
    if success is not None:
        if success:
            result_text += "[bold green]✓ Success![/bold green]"
        else:
            result_text += "[bold red]✗ Failure[/bold red]"
    
    panel = Panel(result_text, border_style="yellow")
    console.print(panel)


def display_damage(target_name: str, damage: int, damage_type: str = "damage") -> None:
    """Display damage dealt."""
    console.print(f"[bold red]💥 {target_name} takes {damage} {damage_type}![/bold red]")


def display_healing(target_name: str, healing: int) -> None:
    """Display healing."""
    console.print(f"[bold green]✨ {target_name} heals {healing} HP![/bold green]")


def display_compact_character_sheet(character: Character) -> None:
    """Display a compact character sheet for combat."""
    from ..rules.abilities import calculate_modifier
    
    hp_color = "green" if character.current_hp > character.max_hp // 2 else "yellow"
    if character.current_hp <= character.max_hp // 4:
        hp_color = "red"
    
    # Calculate modifiers for display
    str_mod = calculate_modifier(character.strength)
    dex_mod = calculate_modifier(character.dexterity)
    con_mod = calculate_modifier(character.constitution)
    int_mod = calculate_modifier(character.intelligence)
    wis_mod = calculate_modifier(character.wisdom)
    cha_mod = calculate_modifier(character.charisma)
    
    def fmt_mod(mod: int) -> str:
        return f"+{mod}" if mod >= 0 else str(mod)
    
    # Build compact display
    lines = []
    lines.append(f"[bold cyan]{character.name}[/bold cyan] │ Lv{character.level} {character.species} {character.character_class} ({character.background})")
    lines.append(f"[{hp_color}]❤️  HP {character.current_hp}/{character.max_hp}[/{hp_color}] │ 🛡️  AC {character.armor_class} │ 👟 Speed {character.speed}ft")
    lines.append(f"STR {fmt_mod(str_mod)} │ DEX {fmt_mod(dex_mod)} │ CON {fmt_mod(con_mod)} │ INT {fmt_mod(int_mod)} │ WIS {fmt_mod(wis_mod)} │ CHA {fmt_mod(cha_mod)}")
    
    # Show skill proficiencies
    if character.skill_proficiencies:
        skill_names = [s.skill_name for s in character.skill_proficiencies]
        expertise_names = [s.skill_name for s in character.skill_expertise] if character.skill_expertise else []
        # Mark expertise with (E)
        skill_display = []
        for name in skill_names:
            if name in expertise_names:
                skill_display.append(f"[bold green]{name}★[/bold green]")
            else:
                skill_display.append(f"[green]{name}[/green]")
        lines.append(f"[dim]Skills:[/dim] {', '.join(skill_display)}")
    
    # Show weapons
    if character.weapons:
        weapon_strs = [f"🗡️  {w.get('name', 'Unknown')}" for w in character.weapons[:2]]
        lines.append(f"[dim]Weapons:[/dim] {', '.join(weapon_strs)}")
    
    # Show conditions
    active_conditions = character.conditions.get_active_conditions()
    if active_conditions:
        lines.append(f"[bold red]⚠️  Conditions:[/bold red] {', '.join(c.value for c in active_conditions)}")
    
    panel = Panel("\n".join(lines), title="⚔️ Combat Stats", border_style="blue", padding=(0, 1))
    console.print(panel)


def display_initiative_roll(character_name: str, roll: object, total: int) -> None:
    """Display initiative roll result."""
    from ..rules.dice import DiceRoll
    
    if isinstance(roll, DiceRoll):
        roll_str = f"d20 ({roll.rolls[0]}) + {roll.modifier} = [bold cyan]{total}[/bold cyan]"
    else:
        roll_str = f"[bold cyan]{total}[/bold cyan]"
    
    console.print(f"🎲 [bold]{character_name}[/bold] rolls initiative: {roll_str}")


def display_initiative_order(combatants: list, current_index: int = 0) -> None:
    """Display the initiative order for combat (hides monster HP)."""
    console.print("\n[bold yellow]═══ Initiative Order ═══[/bold yellow]")
    
    for i, combatant in enumerate(combatants):
        name = combatant.get_name()
        init = combatant.initiative
        
        # Current turn indicator
        marker = "▶ " if i == current_index else "  "
        
        # Only show HP for players
        from ..game.combat import CombatantType
        if combatant.combatant_type == CombatantType.PLAYER:
            current_hp, max_hp = combatant.get_hp()
            hp_color = "green" if current_hp > max_hp // 2 else "yellow"
            if current_hp <= max_hp // 4:
                hp_color = "red"
            hp_str = f" [{hp_color}]({current_hp}/{max_hp} HP)[/{hp_color}]"
        else:
            # Show monster condition hints without exact HP
            current_hp, max_hp = combatant.get_hp()
            if current_hp <= 0:
                hp_str = " [dim](Defeated)[/dim]"
            elif current_hp <= max_hp // 4:
                hp_str = " [red](Badly wounded)[/red]"
            elif current_hp <= max_hp // 2:
                hp_str = " [yellow](Wounded)[/yellow]"
            else:
                hp_str = ""
        
        style = "bold" if i == current_index else ""
        console.print(f"{marker}[{style}]{init:2d} - {name}{hp_str}[/{style}]")
    
    console.print("[bold yellow]═════════════════════════[/bold yellow]\n")


def display_spell_slots(character: Character) -> None:
    """Display available spell slots for the character."""
    if not character.spell_slots:
        return
    
    slots = character.spell_slots
    slot_display = []
    
    for level in range(1, 10):
        total = getattr(slots, f"level_{level}")
        if total > 0:
            available = slots.get_available(level)
            # Show filled/empty circles for slots
            filled = "●" * available
            empty = "○" * (total - available)
            color = "green" if available > 0 else "red"
            slot_display.append(f"[{color}]Lv{level}: {filled}{empty}[/{color}]")
    
    if slot_display:
        panel = Panel(" │ ".join(slot_display), title="✨ Spell Slots", border_style="magenta", padding=(0, 1))
        console.print(panel)


def display_player_roll(
    roll_type: str,
    roll: object,
    target_dc: Optional[int] = None,
    success: Optional[bool] = None,
    hide_dc: bool = False,
) -> None:
    """
    Display a player's roll with result.
    
    Args:
        roll_type: Description of the roll (e.g., "Attack Roll", "Wisdom Saving Throw")
        roll: The DiceRoll object
        target_dc: The DC or AC to beat (optional, can be hidden)
        success: Whether the roll succeeded (optional)
        hide_dc: If True, don't show the target DC
    """
    from ..rules.dice import DiceRoll
    
    if not isinstance(roll, DiceRoll):
        return
    
    # Build roll display
    lines = []
    lines.append(f"[bold]{roll_type}[/bold]")
    
    # Show the roll breakdown
    if roll.roll_type.value == "advantage":
        roll_breakdown = f"d20 ({roll.rolls[0]}, {roll.rolls[1]}) → [cyan]{max(roll.rolls)}[/cyan]"
        lines.append(f"🎲 {roll_breakdown} + {roll.modifier} = [bold cyan]{roll.total}[/bold cyan] [dim](Advantage)[/dim]")
    elif roll.roll_type.value == "disadvantage":
        roll_breakdown = f"d20 ({roll.rolls[0]}, {roll.rolls[1]}) → [cyan]{min(roll.rolls)}[/cyan]"
        lines.append(f"🎲 {roll_breakdown} + {roll.modifier} = [bold cyan]{roll.total}[/bold cyan] [dim](Disadvantage)[/dim]")
    else:
        lines.append(f"🎲 d20 ({roll.rolls[0]}) + {roll.modifier} = [bold cyan]{roll.total}[/bold cyan]")
    
    # Show target DC if provided and not hidden
    if target_dc is not None and not hide_dc:
        lines.append(f"[dim]Target: {target_dc}[/dim]")
    
    # Critical indicators
    if roll.is_critical():
        lines.append("[bold green]⭐ NATURAL 20 - CRITICAL! ⭐[/bold green]")
    elif roll.is_fumble():
        lines.append("[bold red]💀 NATURAL 1 - CRITICAL MISS! 💀[/bold red]")
    
    # Success/Failure
    if success is not None:
        if success:
            lines.append("[bold green]✓ SUCCESS[/bold green]")
        else:
            lines.append("[bold red]✗ FAILURE[/bold red]")
    
    panel = Panel("\n".join(lines), border_style="yellow", padding=(0, 1))
    console.print(panel)


def display_damage_roll(damage_dice: str, roll: object, damage_type: str = "damage", is_critical: bool = False) -> None:
    """Display a damage roll result."""
    from ..rules.dice import DiceRoll
    
    if not isinstance(roll, DiceRoll):
        return
    
    crit_text = " [bold magenta](CRITICAL - doubled!)[/bold magenta]" if is_critical else ""
    roll_str = " + ".join(str(r) for r in roll.rolls)
    
    if roll.modifier != 0:
        mod_str = f" + {roll.modifier}" if roll.modifier > 0 else f" - {abs(roll.modifier)}"
        console.print(f"💥 [bold red]{damage_dice}[/bold red]: {roll_str}{mod_str} = [bold]{roll.total} {damage_type}{crit_text}[/bold]")
    else:
        console.print(f"💥 [bold red]{damage_dice}[/bold red]: {roll_str} = [bold]{roll.total} {damage_type}{crit_text}[/bold]")


def display_your_turn(character: Character) -> None:
    """Display the 'your turn' prompt with character info and spell slots."""
    console.print("\n[bold yellow]═══════════════════════════════════════[/bold yellow]")
    console.print("[bold yellow]           ⚔️  YOUR TURN ⚔️            [/bold yellow]")
    console.print("[bold yellow]═══════════════════════════════════════[/bold yellow]\n")
    
    display_compact_character_sheet(character)
    display_spell_slots(character)


def display_narrative(text: str, style: str = "white") -> None:
    """Display narrative text from the DM."""
    panel = Panel(text, title="🎭 Dungeon Master", border_style="cyan", style=style)
    console.print(panel)


def display_dm_response(text: str) -> None:
    """
    Display DM response formatted for rich terminal display.
    Converts markdown-like formatting to Rich-compatible formatting.
    """
    # Convert markdown to Rich markup
    formatted = _markdown_to_rich(text)
    
    # Display in a panel
    panel = Panel(formatted, title="🎭 Dungeon Master", border_style="cyan")
    console.print(panel)


def _markdown_to_rich(text: str) -> str:
    """Convert common markdown patterns to Rich markup and add icons."""
    result = text
    
    # Convert **bold** to [bold]...[/bold]
    result = re.sub(r'\*\*(.+?)\*\*', r'[bold]\1[/bold]', result)
    
    # Convert *italic* to [italic]...[/italic]
    result = re.sub(r'\*([^*]+?)\*', r'[italic]\1[/italic]', result)
    
    # Convert _italic_ to [italic]...[/italic]
    result = re.sub(r'_([^_]+?)_', r'[italic]\1[/italic]', result)
    
    # Convert `code` to [cyan]...[/cyan]
    result = re.sub(r'`([^`]+?)`', r'[cyan]\1[/cyan]', result)
    
    # Convert markdown headers ### to bold with color
    result = re.sub(r'^### (.+)$', r'[bold yellow]\1[/bold yellow]', result, flags=re.MULTILINE)
    result = re.sub(r'^## (.+)$', r'[bold cyan]\1[/bold cyan]', result, flags=re.MULTILINE)
    result = re.sub(r'^# (.+)$', r'[bold magenta]\1[/bold magenta]', result, flags=re.MULTILINE)
    
    # Convert bullet points - item to • item
    result = re.sub(r'^- (.+)$', r'  • \1', result, flags=re.MULTILINE)
    result = re.sub(r'^\* (.+)$', r'  • \1', result, flags=re.MULTILINE)
    
    # Convert numbered lists
    result = re.sub(r'^(\d+)\. (.+)$', r'  \1. \2', result, flags=re.MULTILINE)
    
    # Convert --- horizontal rules
    result = re.sub(r'^---+$', r'[dim]─────────────────────────────────────────[/dim]', result, flags=re.MULTILINE)
    
    # Remove leftover markdown artifacts like >>> or > for quotes
    result = re.sub(r'^> (.+)$', r'  [dim italic]"\1"[/dim italic]', result, flags=re.MULTILINE)
    
    # Add icons only where they improve readability (currency, combat, items, creatures)
    icon_patterns = [
        # Currency - icons help distinguish different coin types
        (r'\b(\d+)\s*(?:gold|gp)\b', r'💰 \1 gold'),
        (r'\b(\d+)\s*(?:silver|sp)\b', r'🥈 \1 silver'),
        (r'\b(\d+)\s*(?:copper|cp)\b', r'🥉 \1 copper'),
        # Combat actions - icons help emphasize combat events
        (r'\b(attack|attacks|strike|strikes)\b', r'⚔️  \1'),
        (r'\b(damage)\b(?!\s*point)', r'💥 \1'),
        (r'\b(\d+)\s*(?:HP|hit points?|health)\b', r'❤️  \1 HP'),
        (r'\bheal(?:s|ed|ing)?\b', r'💚 heal'),
        # Magic
        (r'\b(spell|spells|cast|casts|magic)\b', r'✨ \1'),
        (r'\b(potion|potions)\b', r'🧪 \1'),
        (r'\b(scroll|scrolls)\b', r'📜 \1'),
        # Weapons & Armor
        (r'\b(sword|blade|longsword|shortsword|greatsword)\b', r'🗡️  \1'),
        (r'\b(bow|crossbow|longbow|shortbow)\b', r'🏹 \1'),
        (r'\b(shield)\b', r'🛡️  \1'),
        (r'\b(armor|armour)\b', r'🛡️  \1'),
        # Creatures
        (r'\b(dragon|dragons)\b', r'🐉 \1'),
        (r'\b(wolf|wolves)\b', r'🐺 \1'),
        (r'\b(spider|spiders)\b', r'🕷️  \1'),
        (r'\b(skeleton|skeletons)\b', r'💀 \1'),
        (r'\b(zombie|zombies|undead)\b', r'🧟 \1'),
        (r'\b(goblin|goblins)\b', r'👺 \1'),
        # Dice/Rolls
        (r'\b(roll|rolls|rolled|d20|d6|d8|d10|d12)\b', r'🎲 \1'),
        # Status indicators - icons help scan for important outcomes
        (r'\b(warning|danger)\b', r'⚠️  \1'),
        (r'\b(death|dead|died|dying)\b', r'💀 \1'),
        # Experience/leveling - notable milestone events
        (r'\b(level up)\b', r'⭐ \1'),
    ]
    
    for pattern, replacement in icon_patterns:
        result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
    
    return result


def display_error(message: str) -> None:
    """Display an error message."""
    console.print(f"[bold red]Error:[/bold red] {message}")


def display_success(message: str) -> None:
    """Display a success message."""
    console.print(f"[bold green]✓[/bold green] {message}")


def clear_screen() -> None:
    """Clear the console screen."""
    console.clear()


def separator() -> None:
    """Print a separator line."""
    console.print("─" * 60, style="dim")
