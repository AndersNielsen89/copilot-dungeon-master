"""Shared roll command parser for CLI and web API."""

from __future__ import annotations

from .dice import RollType, roll_d20, roll_damage


def perform_player_roll(dice_input: str) -> str:
    """
    Perform a dice roll for the player.
    
    This function is self-contained and does not require game state context.
    Roll results are purely based on the dice notation provided.
    
    Supports formats like:
    - "d20" or "1d20" - simple roll
    - "d20+5" - roll with modifier
    - "2d6+3" - multiple dice with modifier
    - "d20 advantage" or "d20 adv" - roll with advantage
    - "d20 disadvantage" or "d20 dis" - roll with disadvantage
    
    Args:
        dice_input: The dice notation string to parse and roll.
        
    Returns:
        A formatted string describing the roll result.
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
        
        # Use the general roll_damage function for any dice notation
        result = roll_damage(dice_input)
        return f"🎲 Rolling {dice_input}: {result}"
    
    except Exception:
        return (
            "Invalid dice notation. Try formats like 'd20', '1d8+3', '2d6', "
            "'d20 advantage'."
        )
