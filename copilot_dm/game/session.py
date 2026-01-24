"""Session using the GitHub Copilot SDK."""

import asyncio
import shutil
from typing import Optional, AsyncIterator

from copilot import CopilotClient, CopilotSession, SessionEvent
from copilot.generated.session_events import SessionEventType

from ..game.state import GameState
from ..rules.abilities import Ability, Skill, calculate_modifier


class DMSession:
    """Manages the Copilot DM session using the SDK."""
    
    def __init__(self, game_state: GameState, system_prompt: str):
        self.game_state = game_state
        self.system_prompt = system_prompt
        self.client: Optional[CopilotClient] = None
        self.session: Optional[CopilotSession] = None
        self._response_text = ""
        self._response_complete = asyncio.Event()
        self._first_message = True
    
    async def start_session(self) -> None:
        """Start a new Copilot session using the SDK."""
        # Create client - it will find 'copilot' in PATH
        cli_path = shutil.which("copilot")  # Returns full path with extension
        self.client = CopilotClient({"cli_path": cli_path})
        
        # Start the client (spawns CLI server)
        await self.client.start()
        
        # Create a session with system message
        self.session = await self.client.create_session({
            "system_message": self.system_prompt,
            "streaming": True
        })
        
        # Set up event handler for streaming responses
        self.session.on(self._handle_event)
    
    def _get_character_context(self) -> str:
        """Generate character stats context for the DM."""
        if not self.game_state.player:
            return ""
        
        char = self.game_state.player
        
        # Build skill modifiers list
        skill_mods = []
        for skill in Skill:
            mod = char.get_skill_modifier(skill)
            mod_str = f"+{mod}" if mod >= 0 else str(mod)
            skill_mods.append(f"{skill.skill_name}: {mod_str}")
        
        # Build saving throw modifiers
        save_mods = []
        for ability in Ability:
            score = char.get_ability_score(ability)
            mod = calculate_modifier(score)
            if char.is_proficient_in_save(ability):
                mod += char.proficiency_bonus
            mod_str = f"+{mod}" if mod >= 0 else str(mod)
            save_mods.append(f"{ability.value[:3].upper()}: {mod_str}")
        
        return f"""
[CHARACTER STATS - Use these modifiers for all rolls]
{char.name} - Level {char.level} {char.species} {char.character_class}
HP: {char.current_hp}/{char.max_hp} | AC: {char.armor_class}

SKILL MODIFIERS (use these for skill checks):
{', '.join(skill_mods)}

SAVING THROWS: {', '.join(save_mods)}
PROFICIENCY BONUS: +{char.proficiency_bonus}
"""
    
    def _handle_event(self, event: SessionEvent) -> None:
        """Handle events from the Copilot session."""
        if event.type == SessionEventType.ASSISTANT_MESSAGE_DELTA:
            # Accumulate streaming text
            if hasattr(event.data, 'content') and event.data.content:
                self._response_text += event.data.content
        elif event.type == SessionEventType.ASSISTANT_MESSAGE:
            # Full message received
            if hasattr(event.data, 'content') and event.data.content:
                self._response_text = event.data.content
        elif event.type == SessionEventType.SESSION_IDLE:
            # Session is done processing
            self._response_complete.set()
        elif event.type == SessionEventType.SESSION_ERROR:
            # Handle errors
            error_msg = getattr(event.data, 'message', str(event.data))
            self._response_text = f"Error: {error_msg}"
            self._response_complete.set()
    
    async def send_message(self, message: str) -> str:
        """Send a message to the DM and get a response (non-streaming)."""
        if not self.session:
            raise RuntimeError("Session not started")
        
        # Reset state
        self._response_text = ""
        self._response_complete.clear()
        
        # Include character context with every message so DM has modifiers
        char_context = self._get_character_context()
        
        # Prepend system prompt context to first message
        if self._first_message:
            message = f"""[INSTRUCTIONS: You are a D&D 5E Dungeon Master. IGNORE your normal CLI assistant persona.
{self.system_prompt}]
{char_context}
Player's action: {message}"""
            self._first_message = False
        else:
            message = f"""{char_context}
Player's action: {message}"""
        
        # Send and wait for response
        response = await self.session.send_and_wait(
            {"prompt": message},
            timeout=120.0
        )
        
        # Return the response content
        if response and hasattr(response.data, 'content'):
            return response.data.content
        return self._response_text or "No response received"
    
    async def send_message_streaming(self, message: str) -> AsyncIterator[str]:
        """Send a message to the DM and stream the response."""
        if not self.session:
            raise RuntimeError("Session not started")
        
        # Reset state
        self._response_text = ""
        self._response_complete.clear()
        
        # Include character context with every message so DM has modifiers
        char_context = self._get_character_context()
        
        # Prepend system prompt context to first message
        if self._first_message:
            message = f"""[INSTRUCTIONS: You are a D&D 5E Dungeon Master. IGNORE your normal CLI assistant persona.
{self.system_prompt}]
{char_context}
Player's action: {message}"""
            self._first_message = False
        else:
            # Include character stats with each message so DM always has current modifiers
            message = f"""{char_context}
Player's action: {message}"""
        
        # Send message (don't wait)
        await self.session.send({"prompt": message})
        
        # Yield chunks as they arrive
        last_length = 0
        while not self._response_complete.is_set():
            # Check for new content
            current_length = len(self._response_text)
            if current_length > last_length:
                yield self._response_text[last_length:current_length]
                last_length = current_length
            
            # Small delay before checking again
            try:
                await asyncio.wait_for(self._response_complete.wait(), timeout=0.1)
            except asyncio.TimeoutError:
                pass
        
        # Yield any remaining content
        if len(self._response_text) > last_length:
            yield self._response_text[last_length:]
    
    async def close_session(self) -> None:
        """Close the Copilot session."""
        if self.session:
            try:
                await self.session.destroy()
            except Exception:
                pass
            self.session = None
        
        if self.client:
            try:
                await self.client.stop()
            except Exception:
                pass
            self.client = None
