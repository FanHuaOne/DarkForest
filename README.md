Dark Forest - Project Description Document

## Project Overview

**Dark Forest** is a Python-based graphical role-playing game (RPG) that combines strategy, 
adventure, and survival elements. The game uses Tkinter for its graphical user interface, 
supports bilingual display (Chinese/English), and provides players with 
an immersive dark fantasy world experience.

### Core Concept
Players take on the role of an adventurer delving into a mysterious forest shrouded by dark forces,
 embarking on a 10-day adventure journey to ultimately challenge the Dark Magic Dragon.
 The game integrates resource management, combat strategy, random events,
  and character progression systems.

## Technical Architecture

### Development Environment
- **Programming Language**: Python 3.x
- **GUI Framework**: Tkinter
- **Architecture Pattern**: Object-Oriented Design (OOP)
- **Game Type**: Single-player Turn-based RPG

### Core Module Structure
-------------
|--DarkForest
|---- main.py
|
|

## Feature Highlights

### 1. Character System
- **Attribute Management**: Health, Stamina, Attack, Defense, Gold
- **Progression Mechanism**: Base attack increases daily, attribute potion enhancements
- **Title System**: Unlock special tags based on player behavior
- **State Saving**: Daily state backup and restoration functionality

### 2. Combat System
- **Intelligent Prediction**: Pre-battle damage prediction and risk assessment
- **Strategy Selection**: Multiple combat strategies (Fierce Attack, Defense, Dodge, Berserk)
- **Balance Mechanism**: Dynamic calculation of attack and defense
- **BOSS Battles**: Special boss combat mechanics

### 3. Economic System
- **Currency System**: Gold as primary transaction currency
- **Shop System**: Dual-track system with regular shops and traveling merchants
- **Item Categories**:
  - Health Potions (Regular/Super)
  - Attack Potions (Regular/Super/Berserk)
  - Defense Potions
  - Stamina Potions
  - Mystery Potions (Random effects)

### 4. Event System
- **Random Encounters**: Monsters, traps, dark ruins, shops, merchants, time leaps
- **Dynamic Probability**: Event trigger rates adjusted based on player state
- **Special Events**: Time leap providing storyline branching choices

### 5. Time System
- **Day Mechanism**: 10-day complete storyline progression
- **Day-Night Cycle**: UI color changes based on stamina values
- **Rest Mechanism**: Dual-mode rest system (Short Rest and Camp Rest)

## Game Mechanics Detailed

### Core Gameplay Loop

- Explore Forest → Encounter Events → Combat/Trading → State Recovery → Advance to Next Day


### Balance Design
- **Attribute Growth**: Daily base attack +5, defense +2
- **Stamina Consumption**: Exploration (-20), Escape (-10), Short Rest (-5)
- **Difficulty Curve**: Monster attributes scale linearly with days
- **Resource Management**: Balanced gold acquisition and consumption

### Special Systems

#### 1. Bilingual Support
- Complete Chinese/English interface and text
- Culturally adapted game content

#### 2. Title Achievements
- **Combat Class**: Berserker, Tank
- **Behavior Class**: Coward, Miser, Lazy Person
- **Special Class**: Time Traveler, Dark Mage

#### 3. Story Narrative
- Unique daily story backgrounds
- Progressive world-building revelation
- Multiple ending system (Victory/Defeat)

## Technical Features

### 1. GUI Design
- Responsive layout adapting to different screen sizes
- Dynamic color themes (Day/Dusk/Night)
- Intuitive status display and interactive feedback

### 2. Code Architecture
- Modular design with high cohesion and low coupling
- Separation of combat system and GUI logic
- Class structure easy to extend and maintain

### 3. Exception Handling
- Comprehensive input validation
- Game state consistency checking
- Graceful error recovery mechanisms

## Installation & Execution

### System Requirements
- Python 3.6+
- Tkinter (usually included with Python installation)

### Execution Command
```bash
python main.py




