"""Main entry point for the Copilot DM application."""

import asyncio
import sys
from pathlib import Path

from .ui.display import (
    display_title,
    display_character_status,
    display_narrative,
    display_dm_response,
    display_error,
    clear_screen,
    console,
)
from .ui.prompts import display_menu, prompt_text, wait_for_enter, prompt_confirm
from .characters.pregens import list_pregen_characters, get_pregen_character
from .game.state import GameState
from .game.session import DMSession
from .rules.roll_commands import perform_player_roll


def load_system_prompt() -> str:
    """Load the DM system prompt from file."""
    prompt_path = Path(__file__).parent / "data" / "system_prompt.md"
    try:
        return prompt_path.read_text(encoding="utf-8")
    except Exception as e:
        display_error(f"Failed to load system prompt: {e}")
        sys.exit(1)


def load_adventure() -> str:
    """Load the adventure content."""
    adventure_path = Path(__file__).parent / "data" / "adventure.md"
    try:
        return adventure_path.read_text(encoding="utf-8")
    except Exception as e:
        display_error(f"Failed to load adventure: {e}")
        sys.exit(1)


def perform_player_roll(dice_input: str, game_state: GameState) -> str:
    """
    Perform a dice roll for the player.
    
    Supports formats like:
    - "d20" or "1d20" - simple roll
    - "d20+5" - roll with modifier
    - "2d6+3" - multiple dice with modifier
    - "d20 advantage" or "d20 adv" - roll with advantage
    - "d20 disadvantage" or "d20 dis" - roll with disadvantage
    """
    dice_input = dice_input.lower().strip()
    
    # Check for advantage/disadvantage
    roll_type = RollType.NORMAL
    if " advantage" in dice_input or " adv" in dice_input:
        roll_type = RollType.ADVANTAGE
        dice_input = dice_input.replace(" advantage", "").replace(" adv", "").strip()
    elif " disadvantage" in dice_input or " dis" in dice_input:
        roll_type = RollType.DISADVANTAGE
        dice_input = dice_input.replace(" disadvantage", "").replace(" dis", "").strip()
    
    # Handle simple "d20" format (no number prefix)
    if dice_input.startswith("d") and not dice_input[0].isdigit():
        dice_input = "1" + dice_input
    
    try:
        # For d20 rolls with advantage/disadvantage
        if "d20" in dice_input and roll_type != RollType.NORMAL:
            # Parse modifier if present
            modifier = 0
            if "+" in dice_input:
                parts = dice_input.split("+")
                modifier = int(parts[1])
            elif "-" in dice_input:
                parts = dice_input.split("-")
                modifier = -int(parts[1])
            
            result = roll_d20(modifier, roll_type)
            
            roll_type_str = "with advantage" if roll_type == RollType.ADVANTAGE else "with disadvantage"
            output = f"🎲 Rolling d20 {roll_type_str}: {result}"
            
            if result.is_critical():
                output += " [bold green]NATURAL 20![/bold green]"
            elif result.is_fumble():
                output += " [bold red]NATURAL 1![/bold red]"
            
            return output
        else:
            # Use the general roll_damage function for any dice notation
            result = roll_damage(dice_input)
            return f"🎲 Rolling {dice_input}: {result}"
    
    except Exception as e:
        return f"[red]Invalid dice notation: {dice_input}. Try formats like 'd20', '1d8+3', '2d6', 'd20 advantage'[/red]"


def select_character() -> None:
    """Character selection menu."""
    clear_screen()
    display_title()
    
    console.print("\n[bold cyan]Choose Your Hero[/bold cyan]")
    console.print("Select a pre-generated character to begin your adventure:\n")
    
    characters = list_pregen_characters()
    choice = display_menu("Available Characters", characters)
    
    selected_name = characters[choice]
    character = get_pregen_character(selected_name)
    
    # Display character details
    clear_screen()
    display_character_status(character)
    
    console.print(f"\n[bold]Background:[/bold] {character.backstory}")
    console.print(f"[bold]Personality:[/bold] {character.personality}\n")
    
    if not prompt_confirm(f"Play as {character.name}?", default=True):
        return select_character()
    
    return character


async def game_loop(game_state: GameState, dm_session: DMSession) -> None:
    """Main game loop."""
    
    console.print("\n[bold green]Starting your adventure...[/bold green]\n")
    
    # Initial DM introduction
    intro_message = f"""
The adventure begins! I am your Dungeon Master for today's quest.

You are {game_state.player.name}, a {game_state.player.species} {game_state.player.character_class}. 
{game_state.player.backstory}

You've heard rumors of trouble in the small village of Thornhaven - livestock found dead, 
villagers disappearing. The local authorities are offering a reward to any brave soul willing 
to investigate. You arrive at the village as the sun begins to set...

Let's begin! What do you do first?
"""
    
    display_narrative(intro_message)
    
    # Main game loop
    while True:
        try:
            # Get player input
            player_action = prompt_text("\n[bold cyan]Your action[/bold cyan]")
            
            if not player_action.strip():
                continue
            
            # Check for meta commands
            if player_action.lower() in ["quit", "exit", "q"]:
                if prompt_confirm("Are you sure you want to quit?", default=False):
                    console.print("\n[bold yellow]Thanks for playing![/bold yellow]")
                    break
                continue
            
            if player_action.lower() in ["status", "stats", "character"]:
                display_character_status(game_state.player)
                continue
            
            if player_action.lower() in ["help", "?"]:
                console.print("\n[bold]Available Commands:[/bold]")
                console.print("  - Type your action in natural language")
                console.print("  - 'roll <dice>' - Roll dice (e.g., 'roll d20', 'roll 1d8+3', 'roll d20 advantage')")
                console.print("  - 'status' - View character stats")
                console.print("  - 'quit' - End the game")
                console.print("  - 'help' - Show this message\n")
                continue
            
            # Check for roll command
            if player_action.lower().startswith("roll "):
                dice_notation = player_action[5:].strip()
                if dice_notation:
                    roll_result = perform_player_roll(dice_notation)
                    console.print(f"\n{roll_result}\n")
                else:
                    console.print("\n[yellow]Usage: roll <dice> (e.g., 'roll d20', 'roll 2d6+3', 'roll d20 advantage')[/yellow]\n")
                continue
            
            # Send to DM
            console.print("\n[dim]The DM considers your action...[/dim]\n")
            
            # Stream DM response and collect full text
            response_text = ""
            async for chunk in dm_session.send_message_streaming(player_action):
                response_text += chunk
            
            # Display DM response using Rich formatting
            display_dm_response(response_text)
            
            # Check if combat ended or other state changes
            if game_state.current_combat and game_state.current_combat.is_combat_over():
                game_state.end_combat()
                console.print("[bold green]⚔️  Combat has ended![/bold green]\n")
            
            # Check if player died
            if game_state.player and game_state.player.current_hp <= 0:
                console.print("\n[bold red]💀 You have fallen...[/bold red]")
                console.print("Your vision fades to black as consciousness slips away...")
                
                if prompt_confirm("\nWould you like to retry from the last scene?", default=True):
                    # Restore player to half HP
                    game_state.player.current_hp = game_state.player.max_hp // 2
                    console.print("\n[italic]Through sheer force of will, you cling to life...[/italic]\n")
                else:
                    console.print("\n[bold]Your adventure ends here.[/bold]")
                    break
        
        except KeyboardInterrupt:
            console.print("\n\n[dim]Interrupted by user[/dim]")
            if prompt_confirm("Exit the game?", default=False):
                break
        except Exception as e:
            display_error(f"An error occurred: {e}")
            if not prompt_confirm("Continue playing?", default=True):
                break


async def async_main() -> None:
    """Async main function."""
    try:
        # Show title screen
        clear_screen()
        display_title()
        wait_for_enter("\nPress Enter to begin your adventure...")
        
        # Character selection
        character = select_character()
        
        # Initialize game state
        game_state = GameState()
        game_state.set_player(character)
        
        # Load prompts
        system_prompt = load_system_prompt()
        # Note: Adventure details are referenced in system prompt, not included in full
        
        # Create condensed DM instructions
        condensed_prompt = """You are an experienced Dungeon Master running "The Shadows of Thornhaven" - a D&D 5E 2024 solo adventure.

## Your Role
- Narrate vividly but BRIEFLY (2-4 sentences max for descriptions)
- Portray NPCs with distinct personalities
- Keep dialogue SHORT - 1-2 lines per NPC response
- Always end with suggested actions

## Response Format - ALWAYS FOLLOW THIS
1. Brief scene/action description (2-4 sentences)
2. Any NPC dialogue (keep it short!)
3. End with "What do you do?" and 1-3 numbered suggested actions like:
   1. Investigate the noise
   2. Talk to the innkeeper
   3. Draw your weapon

## The Adventure
Thornhaven village: mysterious attacks, missing herbalist Lyssa in Thornwood Forest. Goal: find cursed cave, defeat Grimfang the Bugbear.

## CRITICAL: Skill Checks and Rolls
The CHARACTER STATS section provides ALL skill modifiers. When making ANY check:
1. Roll d20 and ADD the character's modifier from the provided stats
2. Show the COMPLETE calculation: "Intimidation: d20 (14) + 5 = 19 vs DC 15 - SUCCESS!"
3. NEVER ask the player for their modifier - you have it in CHARACTER STATS

Example format for skill checks:
- "Stealth Check: d20 (12) + 4 = 16 vs DC 13 - SUCCESS! You slip past unnoticed."
- "Perception Check: d20 (8) + 2 = 10 vs DC 15 - FAILURE. You don't notice anything unusual."

## Combat Rules
- Roll initiative: "Initiative: d20 (X) + DEX mod = total"
- Player rolls: show dice + modifier, total, SUCCESS/FAILURE
- NEVER reveal monster AC/HP - describe condition only (wounded, badly wounded, near death)
- Player damage taken: show exact numbers "5 slashing damage (HP: 8/13)"

## NPCs (keep dialogue to 1-2 lines)
- Mara (Innkeeper): Warm, worried
- Captain Thorne: Gruff guard
- Sage Elric: Knows forest lore

## Style
- NO markdown (no **, #, etc)
- Keep responses under 150 words
- Use CAPS sparingly for emphasis
- Always suggest at least one action the player can take"""
        
        # Create DM session
        dm_session = DMSession(game_state, condensed_prompt)
        
        console.print("\n[dim]Connecting to your Dungeon Master...[/dim]")
        await dm_session.start_session()
        console.print("[dim]Connected! Your adventure begins...[/dim]\n")
        
        # Run game loop
        await game_loop(game_state, dm_session)
        
        # Cleanup
        await dm_session.close_session()
        
        console.print("\n[bold cyan]Thank you for playing Copilot DM![/bold cyan]")
        console.print("[dim]May your next adventure be even greater...[/dim]\n")
    
    except Exception as e:
        display_error(f"Fatal error: {e}")
        console.print("\n[dim]Press Ctrl+C to exit[/dim]")
        import traceback
        traceback.print_exc()


def main() -> None:
    """Run the Copilot DM game."""
    try:
        asyncio.run(async_main())
    except KeyboardInterrupt:
        console.print("\n\n[bold yellow]Game interrupted. Goodbye![/bold yellow]")
    except Exception as e:
        display_error(f"Failed to start game: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
