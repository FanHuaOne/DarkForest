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





---

## 功能亮点

### 1. 角色系统
- **属性管理**：生命值、耐力、攻击、防御、金币  
- **成长机制**：基础攻击每日增加，可通过药水提升属性  
- **称号系统**：根据玩家行为解锁特殊称号  
- **状态保存**：每日状态备份与恢复功能  

### 2. 战斗系统
- **智能预测**：战前伤害预测和风险评估  
- **策略选择**：多种战斗策略（猛烈攻击、防御、闪避、狂暴）  
- **平衡机制**：动态计算攻击和防御数值  
- **BOSS 战**：特殊 BOSS 战斗机制  

### 3. 经济系统
- **货币系统**：金币为主要交易货币  
- **商店系统**：常规商店与流动商人双轨系统  
- **道具分类**：
  - 生命药水（普通/超级）  
  - 攻击药水（普通/超级/狂暴）  
  - 防御药水  
  - 耐力药水  
  - 神秘药水（随机效果）  

### 4. 事件系统
- **随机遭遇**：怪物、陷阱、黑暗遗迹、商店、商人、时间跳跃  
- **动态概率**：根据玩家状态调整事件触发概率  
- **特殊事件**：时间跳跃提供剧情分支选择  

### 5. 时间系统
- **天数机制**：完整 10 天剧情进程  
- **昼夜循环**：UI 颜色根据耐力值变化  
- **休息机制**：双模式休息系统（短暂休息和营地休息）  

---

## 游戏机制详述

### 核心玩法循环
探索森林 → 遭遇事件 → 战斗/交易 → 状态恢复 → 进入下一天

### 平衡设计
- **属性成长**：每日基础攻击 +5，防御 +2  
- **耐力消耗**：探索 (-20)、逃跑 (-10)、短暂休息 (-5)  
- **难度曲线**：怪物属性随天数线性增长  
- **资源管理**：金币获取与消耗保持平衡  

### 特殊系统

#### 1. 双语支持
- 完整中英文界面和文本  
- 文化适配的游戏内容  

#### 2. 称号成就
- **战斗类**：狂战士、坦克  
- **行为类**：懦夫、守财奴、懒人  
- **特殊类**：时光旅行者、黑暗法师  

#### 3. 剧情叙事
- 每日独特故事背景  
- 渐进式世界观揭示  
- 多结局系统（胜利/失败）  

---

## 技术特性

### 1. GUI 设计
- 响应式布局，适配不同屏幕尺寸  
- 动态色彩主题（白天/黄昏/夜晚）  
- 直观状态显示与交互反馈  

### 2. 代码架构
- 高内聚、低耦合的模块化设计  
- 战斗系统与 GUI 逻辑分离  
- 类结构易于扩展与维护  

### 3. 异常处理
- 完整的输入验证  
- 游戏状态一致性检查  
- 优雅的错误恢复机制  

---

## 安装与运行

### 系统要求
- Python 3.6 及以上  
- Tkinter（通常随 Python 自带）  

### 运行命令
```bash
python main.py
