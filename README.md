# StratSim - 2D Strategy Simulation Game

A comprehensive country management and diplomacy simulation game built with Python and Pygame. Take control of a fictional nation and guide it through economic challenges, political upheavals, and international relations.

## Features

### Core Country Management
- **Economy**: Manage taxes, GDP, budget allocation, inflation, unemployment, and trade
- **Population**: Monitor happiness, health, education, growth rates, and demographic changes
- **Government**: Choose between democracy, monarchy, dictatorship, and republic systems
- **Political System**: Navigate elections, political parties, corruption, and public opinion

### Diplomacy & Foreign Relations
- **International Relations**: Engage with AI-controlled nations
- **Diplomatic Actions**: Improve relations, sign trade deals, form alliances, declare wars
- **Economic Warfare**: Impose sanctions, provide foreign aid
- **Dynamic Consequences**: Every action affects your economy and public morale

### Dynamic World
- **Procedural Generation**: Randomly generated world with unique countries
- **AI Nations**: Each country has distinct traits, goals, and decision-making patterns
- **Random Events**: Natural disasters, economic booms, technological breakthroughs, political scandals
- **Real-time Simulation**: Countries evolve independently with interconnected relationships

### Gameplay Mechanics
- **Government Types**: Each system affects corruption resistance, stability, and economic growth
- **Budget Management**: Allocate spending across healthcare, education, military, infrastructure, and welfare
- **Political Events**: Handle protests, coups, corruption scandals, and elections
- **Resource Management**: Leverage natural resources like oil, minerals, agriculture, and technology

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone or download the game files**
   ```bash
   # Navigate to the game directory
   cd stratsim-game
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the game**
   ```bash
   python main.py
   ```

## How to Play

### Basic Controls

#### Mouse Controls
- **Left Click**: Select countries on the map
- **UI Interaction**: Click buttons, drag sliders, use dropdowns

#### Keyboard Shortcuts
- **Space**: Pause/unpause the game
- **1**: Overview tab
- **2**: Economy tab  
- **3**: Diplomacy tab
- **4**: Government tab
- **+/=**: Increase game speed

### Game Interface

#### Map Area (Left Side)
- **Country Visualization**: Countries appear as colored circles
- **Size**: Circle size represents population
- **Colors**: Country colors change based on status (war, instability, etc.)
- **Relations**: Lines between countries show diplomatic relationships
- **Player Country**: Highlighted with green border

#### Control Panel (Right Side)

**Overview Tab**
- View selected country's basic statistics
- Monitor population, GDP, happiness, and stability
- Government approval ratings

**Economy Tab**
- **Tax Rate Slider**: Adjust taxation (affects revenue and approval)
- **Budget Allocation**: Distribute spending across key sectors
  - Healthcare: Improves population health and satisfaction
  - Education: Boosts long-term growth and literacy
  - Military: Affects diplomatic standing and war capability
  - Infrastructure: Enhances economic growth
  - Welfare: Increases population happiness

**Diplomacy Tab**
- **Country Selection**: Choose which nation to interact with
- **Diplomatic Actions**:
  - Improve Relations: Send diplomats and cultural exchanges
  - Trade Deal: Boost both economies through commerce
  - Alliance: Form military and economic partnerships
  - Declare War: Military conflict with economic consequences
  - Peace Treaty: End ongoing conflicts
  - Sanctions: Economic punishment for hostile nations
  - Foreign Aid: Improve relations through economic assistance

**Government Tab**
- **Government Type**: Change your political system
- **Laws Display**: View active legislation and policies
- **Political Parties**: Monitor party popularity and ideology

### Winning Strategies

#### Economic Development
- Balance tax rates - too high reduces happiness, too low limits government funding
- Invest in education and infrastructure for long-term growth
- Maintain trade relationships for economic benefits
- Monitor inflation and unemployment carefully

#### Political Stability
- Keep population happiness above 60% to avoid unrest
- Different government types have unique advantages:
  - Democracy: Higher corruption resistance, moderate growth
  - Monarchy: Greater stability, traditional legitimacy
  - Dictatorship: Faster economic changes, higher instability risk
  - Republic: Balanced approach with regular elections

#### International Relations
- Build alliances for mutual protection and economic benefits
- Trade deals provide significant economic boosts
- War is costly but can provide territorial/resource gains
- Use sanctions strategically against hostile neighbors

### Game Events

The game features dynamic events that can dramatically affect your nation:

- **Economic Events**: Market crashes, economic booms, resource discoveries
- **Political Events**: Corruption scandals, successful reforms, coup attempts
- **Social Events**: Protests, epidemics, immigration waves
- **Natural Events**: Disasters that affect population and economy

## Technical Details

### Architecture
- **Modular Design**: Separated economy, population, government, and diplomacy systems
- **Event-Driven**: UI components communicate through callback systems
- **Real-time Simulation**: All countries update simultaneously
- **Extensible**: Easy to add new features, events, and government types

### Game Balance
- Realistic economic relationships between taxation, spending, and growth
- Government types based on historical advantages and disadvantages
- Diplomatic actions have meaningful consequences
- Random events add unpredictability without breaking game balance

## Troubleshooting

### Common Issues

**Game won't start**
- Ensure Python 3.7+ is installed
- Verify pygame installation: `pip install pygame`
- Check that all game files are in the correct directory structure

**Poor Performance**
- Reduce game speed if experiencing lag
- Close other applications to free memory
- Ensure graphics drivers are updated

**Gameplay Questions**
- Experiment with different strategies
- Watch the event log for important notifications
- Use the pause function to study situations carefully

## Development

The game is built with modularity in mind. Key components:

- `game/models/`: Core simulation systems (economy, population, government)
- `game/ui/`: User interface components and screens
- `game/world.py`: World generation and map management
- `game/constants.py`: Game balance and configuration
- `main.py`: Entry point and main game loop

## Future Enhancements

Potential additions for future versions:
- Technology research trees
- Environmental challenges and climate change
- More complex military system with unit management
- Cultural and religious systems
- Advanced AI diplomacy with personalities
- Multiplayer support
- Save/load game functionality
- More detailed economic sectors
- Historical scenarios and campaigns

---

Enjoy building your nation and navigating the complex world of international politics!
