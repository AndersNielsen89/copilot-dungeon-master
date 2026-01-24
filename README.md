# Copilot DM

A solo D&D 5th Edition (2024 rules) terminal adventure where GitHub Copilot serves as your Dungeon Master.

## ✅ Status: FULLY FUNCTIONAL & TESTED

## Features

- 🎲 **Accurate D&D 5E 2024 Rules**: Complete implementation of dice rolling, ability checks, combat, conditions, and spellcasting
- 🤖 **AI Dungeon Master**: GitHub Copilot narrates your adventure, responds to your choices, and enforces the rules
- ⚔️ **Pre-generated Characters**: Choose from 5 ready-to-play characters (Fighter, Rogue, Cleric, Wizard)
- 🐉 **Complete Adventure**: "The Shadows of Thornhaven" - a 1-2 hour campaign for levels 1-3
- 🎨 **Rich Terminal UI**: Colorful, immersive interface using the Rich library
- ⚔️ **Full Combat System**: Initiative, turn order, action economy, conditions
- 🔧 **Rules Tools**: Precise dice rolls, attacks, and checks

## Prerequisites

1. **Python 3.11+**
2. **GitHub Copilot CLI** - Must be installed and authenticated
   ```bash
   # Install with winget (Windows)
   winget install GitHub.Copilot
   
   # Or via npm
   npm install -g @githubnext/github-copilot-cli
   ```

## Installation

```bash
# Clone or navigate to the project
cd C:\PyPojects\CopilotDM

# Install the package
pip install -e .
```

## Usage

```bash
# Run the game
python -m copilot_dm.main
```

## How to Play

1. **Select Your Character**: Choose from 5 pre-generated heroes
   - Ser Aldric (Human Fighter) - Tank/Melee
   - Whisper (Elf Rogue) - Stealth/Skills
   - Thrain Ironforge (Dwarf Cleric) - Healer/Support
   - Elowen (Human Wizard) - Spellcaster
   - Pippin (Halfling Rogue) - Lucky/Nimble

2. **Tell the DM What You Do**: Type your actions in natural language
3. **Let the AI Respond**: The Copilot DM will narrate the results, roll dice, and guide the story
4. **Make Choices**: Your decisions shape the adventure

### Commands

- Type your action in plain English (e.g., "I attack the goblin" or "I search the room")
- `status` - View your character stats
- `help` - Show available commands
- `quit` - Exit the game

## The Adventure

### The Shadows of Thornhaven

A dark curse has fallen upon the village of Thornhaven. Livestock have been found dead, drained of blood. The local herbalist has gone missing. Something evil stirs in the ancient Thornwood Forest, and only a brave hero can save the day.

**Features:**
- 3-act structure with clear progression
- Mix of combat, roleplay, and exploration
- Multiple encounters with goblins, wolves, zombies, spiders, and more
- Boss fight against a bugbear shaman
- Meaningful choices and consequences

### Rules Implementation

- **PHB 2024 Accurate**: Implements the latest D&D rules
- **Complete Systems**: Dice rolling, ability checks, saving throws, attack rolls, damage, conditions, spell slots
- **8 Monster Types**: From CR 1/8 to CR 3, balanced for solo play
- **5 Character Classes**: Fighter, Rogue, Cleric, Wizard with level 1-3 features
- **5 Species**: Human, Elf, Dwarf, Halfling, Tiefling with PHB 2024 traits

## Troubleshooting

### "GitHub Copilot CLI not found"
Make sure the Copilot CLI Prelease is installed and accessible:
```bash
copilot --version
```

If not found, install it:
```bash
winget install GitHub.Copilot
```

### Connection Issues
The game needs the Copilot CLI Prelease to be authenticated. Run:
```bash
copilot auth login
```

## Development

Built with:
- Python 3.11+
- [GitHub Copilot SDK](https://github.com/github/copilot-sdk) - AI integration
- [Rich](https://github.com/Textualize/rich) - Terminal UI
- [Pydantic](https://docs.pydantic.dev/) - Data validation

## Credits

Created as a demonstration of AI-powered game mastering using GitHub Copilot.

## License

MIT License - See LICENSE file for details
