"""User input prompts and menus."""

from rich.console import Console
from rich.prompt import Prompt, Confirm, IntPrompt
from typing import Optional, List

console = Console()


def prompt_text(prompt: str, default: Optional[str] = None) -> str:
    """Prompt for text input."""
    return Prompt.ask(prompt, default=default)


def prompt_choice(prompt: str, choices: List[str], default: Optional[str] = None) -> str:
    """Prompt for a choice from a list."""
    return Prompt.ask(prompt, choices=choices, default=default)


def prompt_number(prompt: str, default: Optional[int] = None) -> int:
    """Prompt for a number."""
    return IntPrompt.ask(prompt, default=default)


def prompt_confirm(prompt: str, default: bool = True) -> bool:
    """Prompt for yes/no confirmation."""
    return Confirm.ask(prompt, default=default)


def display_menu(title: str, options: List[str]) -> int:
    """
    Display a menu and return the selected index.
    
    Returns:
        Index of the selected option (0-based)
    """
    console.print(f"\n[bold cyan]{title}[/bold cyan]")
    for i, option in enumerate(options, 1):
        console.print(f"  {i}. {option}")
    
    while True:
        try:
            choice = IntPrompt.ask("\nSelect an option", default=1)
            if 1 <= choice <= len(options):
                return choice - 1
            else:
                console.print(f"[red]Please enter a number between 1 and {len(options)}[/red]")
        except Exception:
            console.print("[red]Invalid input. Please enter a number.[/red]")


def prompt_action(available_actions: List[str]) -> str:
    """
    Prompt for a combat action.
    
    Returns:
        The selected action as a string
    """
    console.print("\n[bold yellow]What do you do?[/bold yellow]")
    for i, action in enumerate(available_actions, 1):
        console.print(f"  {i}. {action}")
    
    console.print(f"  {len(available_actions) + 1}. Other (describe your action)")
    
    while True:
        try:
            choice = IntPrompt.ask("\nYour action")
            if 1 <= choice <= len(available_actions):
                return available_actions[choice - 1]
            elif choice == len(available_actions) + 1:
                return prompt_text("Describe your action")
            else:
                console.print(f"[red]Please enter a number between 1 and {len(available_actions) + 1}[/red]")
        except Exception:
            console.print("[red]Invalid input. Please enter a number.[/red]")


def wait_for_enter(message: str = "Press Enter to continue...") -> None:
    """Wait for user to press Enter."""
    Prompt.ask(message, default="")
