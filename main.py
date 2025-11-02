import random
import time
import tkinter as tk
from tkinter import messagebox, ttk
import threading

class Player:
    def __init__(self):
        self.health = 100
        self.max_health = 100
        self.defense = 0
        self.base_attack = 5  # 基础攻击力
        self.attack_bonus = 0  # 额外攻击力（来自药水等）
        self.attack = self.base_attack + self.attack_bonus  # 总攻击力
        self.stamina = 100
        self.max_stamina = 100
        self.gold = 0
        self.day = 1
        self.tags = []
        self.monsters_defeated = 0
        self.bosses_defeated = 0
        # 修复：添加"health"和"defense"键到items_bought字典
        self.items_bought = {"attack": 0, "stamina": 0, "mystery": 0, "health": 0, "defense": 0}
        self.escapes_attempted = 0
        self.escapes_successful = 0
        self.start_of_day_stats = None
        self.rest_count_today = 0  # 记录今天休息的次数
        self.has_explored_today = False  # 记录今天是否探索过
        
    def update_attack(self):
        """更新总攻击力"""
        self.attack = self.base_attack + self.attack_bonus
        
    def save_day_start(self):
        """保存当天开始时的状态"""
        self.start_of_day_stats = {
            'health': self.health,
            'stamina': self.stamina,
            'defense': self.defense,
            'gold': self.gold,
            'tags': self.tags.copy(),
            'day': self.day,
            'base_attack': self.base_attack,
            'attack_bonus': self.attack_bonus,
            'rest_count_today': self.rest_count_today,
            'has_explored_today': self.has_explored_today
        }
    
    def restore_day_start(self):
        """恢复到当天开始时的状态"""
        if self.start_of_day_stats:
            self.health = self.start_of_day_stats['health']
            self.stamina = self.start_of_day_stats['stamina']
            self.defense = self.start_of_day_stats['defense']
            self.gold = self.start_of_day_stats['gold']
            self.tags = self.start_of_day_stats['tags'].copy()
            self.day = self.start_of_day_stats['day']
            self.base_attack = self.start_of_day_stats['base_attack']
            self.attack_bonus = self.start_of_day_stats['attack_bonus']
            self.rest_count_today = self.start_of_day_stats['rest_count_today']
            self.has_explored_today = self.start_of_day_stats['has_explored_today']
            self.update_attack()
    
    def add_tag(self, tag):
        if tag not in self.tags:
            self.tags.append(tag)
    
    def get_stats_text(self):
        """获取玩家状态的双语文本"""
        chinese = f"=== 冒险者状态 ===\n"
        chinese += f"❤️ 生命: {self.health}/{self.max_health} | 🏃 耐力: {self.stamina}/{self.max_stamina}\n"
        chinese += f"⚔️ 攻击: {self.attack} (基础:{self.base_attack} + 加成:{self.attack_bonus}) | 🛡️ 防御: {self.defense} | 🪙 金币: {self.gold}\n"
        chinese += f"📅  天数: {self.day} | 🏷️ 称号: {', '.join(self.tags) if self.tags else '无'}\n"
        chinese += f"🎯 击败: {self.monsters_defeated}怪物 {self.bosses_defeated}首领"
        
        english = f"=== Adventurer Status ===\n"
        english += f"❤️ Health: {self.health}/{self.max_health} | 🏃 Stamina: {self.stamina}/{self.max_stamina}\n"
        english += f"⚔️ Attack: {self.attack} (Base:{self.base_attack} + Bonus:{self.attack_bonus}) | 🛡️ Defense: {self.defense} | 🪙 Gold: {self.gold}\n"
        english += f"📅 Day: {self.day} | 🏷️ Tags: {', '.join(self.tags) if self.tags else 'None'}\n"
        english += f"🎯 Defeated: {self.monsters_defeated} monsters, {self.bosses_defeated} bosses"
        
        return chinese + "\n\n" + english

class Monster:
    def __init__(self, day, is_boss=False):
        self.day = day
        self.is_boss = is_boss
        
        if is_boss:
            if day == 10:  # 最终BOSS
                # 调整最终BOSS属性，使其更平衡
                self.health = 500  # 从1000降低到500
                self.attack = 50   # 从100降低到50
                self.defense = 30  # 从100降低到30
                self.name = "黑暗魔龙 / Dark Magic Dragon"
                self.gold_reward = 0
            else:  # 小BOSS
                self.health = 150 + (day * 20)  # 稍微降低小BOSS强度
                self.attack = 12 + (day * 2)    # 稍微降低小BOSS攻击力
                self.defense = min(3 + (day * 1), self.attack - 5)
                self.name = f"第{day}天首领 / Day {day} Boss"
                self.gold_reward = 10  # 增加小BOSS金币奖励
        else:
            # 调整怪物数值，使第一天遇到的怪物可以击败
            self.health = 30 + (day * 5)  # 降低基础生命值
            self.attack = 8 + (day * 1)   # 降低基础攻击力
            self.defense = min(day, self.attack - 3)  # 调整防御计算
            names = [
                "森林狼 / Forest Wolf", 
                "黑暗蜘蛛 / Dark Spider", 
                "变异藤蔓 / Mutated Vine", 
                "幽灵 / Ghost"
            ]
            self.name = random.choice(names)
            self.gold_reward = 3  # 增加普通怪物金币奖励
    
    def get_stats_text(self):
        """获取怪物状态的双语文本"""
        chinese = f"=== {self.name.split(' / ')[0]} ===\n"
        chinese += f"❤️ 生命: {self.health} | ⚔️ 攻击: {self.attack} | 🛡️ 防御: {self.defense}"
        
        english = f"=== {self.name.split(' / ')[1]} ===\n"
        english += f"❤️ Health: {self.health} | ⚔️ Attack: {self.attack} | 🛡️ Defense: {self.defense}"
        
        return chinese + "\n\n" + english

class Shop:
    def __init__(self, player):
        self.items = self.generate_items()
        
        # 如果玩家金币少于3，不显示商店
        self.available = player.gold >= 3
    
    def is_available(self):
        """检查商店是否可用"""
        return self.available
    
    def generate_items(self):
        items = [
            {"name": "生命药水 / Health Potion", "effect": "health_50", "cost": 2, "type": "health", "desc": "增加50最大生命值 / Increases Max HP by 50"},
            {"name": "力量药水 / Strength Potion", "effect": "attack_10", "cost": 2, "type": "attack", "desc": "增加10攻击 / Increases Attack by 10"},
            {"name": "超级生命药水 / Super Health Potion", "effect": "health_20_percent", "cost": 5, "type": "health", "desc": "增加20%最大生命值 / Increases Max HP by 20%"},
            {"name": "超级力量药水 / Super Strength Potion", "effect": "attack_20_percent", "cost": 5, "type": "attack", "desc": "增加20%攻击 / Increases Attack by 20%"},
            {"name": "防御药水 / Defense Potion", "effect": "defense_5", "cost": 3, "type": "defense", "desc": "增加5防御 / Increases Defense by 5"},
            {"name": "耐力药水 / Stamina Potion", "effect": "stamina_full", "cost": 5, "type": "stamina", "desc": "恢复全部耐力 / Fully restores Stamina"},
            {"name": "神秘药水 / Mystery Potion", "effect": "mystery", "cost": 5, "type": "mystery", "desc": "增加100最大生命值或增加20攻击 / Increases Max HP by 100 or increases Attack by 20"},
            {"name": "狂暴药水 / Berserker Potion", "effect": "berserk", "cost": 5, "type": "attack", "desc": "增加15攻击，减少3防御 / Increases Attack by 15, decreases Defense by 3"}
        ]
        
        common_items = [item for item in items if item["type"] not in ["mystery", "attack"]]
        rare_items = [item for item in items if item["type"] in ["mystery", "attack"]]
        
        selected = random.sample(common_items, 2) + random.sample(rare_items, 1)
        random.shuffle(selected)
        return selected
    
    def get_items_text(self):
        """获取商店物品的双语文本，金币靠右对齐"""
        if not self.available:
            return "商店已关闭... / Shop is closed..."
            
        text = "=== 商店 / Shop ===\n"
        for i, item in enumerate(self.items, 1):
            # 使用字符串格式化使金币靠右对齐，保持固定宽度
            text += f"{i}. {item['name']:<30} - {item['cost']:>2} 🪙\n"
            text += f"   {item['desc']}\n"
        text += "0. 离开商店 / Exit Shop"
        return text
    
    def buy_item(self, player, choice):
        if 1 <= choice <= len(self.items):
            item = self.items[choice-1]
            if player.gold >= item['cost']:
                player.gold -= item['cost']
                self.apply_effect(player, item)
                player.items_bought[item['type']] += 1
                
                chinese = f"购买了 {item['name'].split(' / ')[0]}!"
                english = f"Purchased {item['name'].split(' / ')[1]}!"
                return True, chinese + "\n" + english
            else:
                chinese = "金币不足!"
                english = "Not enough gold!"
                return False, chinese + "\n" + english
        return False, ""
    
    def apply_effect(self, player, item):
        effect = item['effect']
        if effect == "health_50":
            player.max_health += 50
            player.health += 50
        elif effect == "attack_10":
            player.attack_bonus += 10
            player.update_attack()
        elif effect == "health_20_percent":
            increase = int(player.max_health * 0.2)
            player.max_health += increase
            player.health += increase
        elif effect == "attack_20_percent":
            increase = int(player.attack * 0.2)
            player.attack_bonus += increase
            player.update_attack()
        elif effect == "defense_5":
            player.defense += 5
        elif effect == "stamina_full":
            player.stamina = player.max_stamina
        elif effect == "mystery":
            if random.choice([True, False]):
                player.max_health += 100
                player.health += 100
            else:
                player.attack_bonus += 20
                player.update_attack()
        elif effect == "berserk":
            # 修改狂暴药水数值：攻击力+15，防御力-3
            player.attack_bonus += 15
            player.defense = max(0, player.defense - 3)
            player.update_attack()

class TravelingMerchant:
    def __init__(self, player):
        self.items = [
            {"name": "愚者药水 / Fool's Potion", "effect": "fool", "cost": 5, "desc": "生命-10, 攻击+30 / HP-10, ATK+30"},
            {"name": "神秘药水 / Mystic Potion", "effect": "mystic", "cost": 5, "desc": "增加100最大生命值 或 攻击+20 / Increases Max HP by 100 or ATK+20"},
            {"name": "狂人药水 / Madman Potion", "effect": "madman", "cost": 5, "desc": "攻击+30, 防御-5 / ATK+30, DEF-5"},
            {"name": "黑暗魔法药水 / Dark Magic Potion", "effect": "dark_magic", "cost": 5, "desc": "增加100最大生命值, 攻击+50 / Increases Max HP by 100, ATK+50"}
        ]
        
        # 如果玩家金币少于3，不显示商人
        self.available = player.gold >= 3
    
    def is_available(self):
        """检查商人是否可用"""
        return self.available
    
    def get_items_text(self):
        """获取旅行商人物品的双语文本，金币靠右对齐"""
        if not self.available:
            return "旅行商人不在... / Traveling Merchant is not available..."
            
        text = "=== 旅行商人 / Traveling Merchant ===\n"
        text += "稀有药水目录 / Rare Potion Catalog:\n"
        for i, item in enumerate(self.items, 1):
            # 使用字符串格式化使金币靠右对齐，保持固定宽度
            text += f"{i}. {item['name']:<30} - {item['cost']:>2} 🪙\n"
            text += f"   {item['desc']}\n"
        text += "0. 离开 / Leave"
        return text
    
    def buy_item(self, player, choice):
        if 1 <= choice <= len(self.items):
            item = self.items[choice-1]
            if player.gold >= item['cost']:
                player.gold -= item['cost']
                self.apply_effect(player, item)
                
                chinese = f"购买了 {item['name'].split(' / ')[0]}!"
                english = f"Purchased {item['name'].split(' / ')[1]}!"
                return True, chinese + "\n" + english
            else:
                chinese = "金币不足!"
                english = "Not enough gold!"
                return False, chinese + "\n" + english
        return False, ""
    
    def apply_effect(self, player, item):
        effect = item['effect']
        if effect == "fool":
            # 修改愚者药水数值：生命值减少10，攻击力+30
            player.health = max(1, player.health - 10)
            player.attack_bonus += 30
            player.update_attack()
            player.add_tag("愚者 / Fool")
        elif effect == "mystic":
            if random.choice([True, False]):
                player.max_health += 100
                player.health += 100
            else:
                player.attack_bonus += 20
                player.update_attack()
        elif effect == "madman":
            # 修改狂人药水数值：攻击力+30，防御-5
            player.attack_bonus += 30
            player.defense = max(0, player.defense - 5)
            player.update_attack()
        elif effect == "dark_magic":
            player.max_health += 100
            player.health += 100
            player.attack_bonus += 50
            player.update_attack()
            if "愚者 / Fool" in player.tags:
                player.add_tag("愚昧的黑暗法师 / Foolish Dark Mage")
            else:
                player.add_tag("黑暗法师 / Dark Mage")
                
class BattleSystem:
    @staticmethod
    def calculate_damage(player, monster):
        """计算战斗伤害 - 修复计算逻辑"""
        # 确保有效攻击至少为1
        player_effective_attack = max(1, player.attack - monster.defense)
        monster_effective_attack = max(1, monster.attack - player.defense)
        
        # 计算玩家需要多少回合击败怪物
        rounds_to_kill_monster = (monster.health + player_effective_attack - 1) // player_effective_attack
        
        # 计算玩家会受到的总伤害
        player_damage = rounds_to_kill_monster * monster_effective_attack
        
        return player_damage
    
    @staticmethod
    def predict_battle(player, monster):
        """预测战斗结果 - 修复预测逻辑"""
        damage_taken = BattleSystem.calculate_damage(player, monster)
        remaining_health = player.health - damage_taken
        
        chinese = f"战斗预测:\n"
        chinese += f"预计受到伤害: {damage_taken}\n"
        chinese += f"预计剩余生命: {max(0, remaining_health)}"
        if remaining_health <= 0:
            chinese += f" (这场战斗很危险，你可能会死亡!)"
        
        english = f"Battle Prediction:\n"
        english += f"Expected damage taken: {damage_taken}\n"
        english += f"Expected remaining health: {max(0, remaining_health)}"
        if remaining_health <= 0:
            english += f" (This Battle is very dangerous, you may meet DEATH!)"
        
        return chinese + "\n\n" + english
    
    @staticmethod
    def fight(player, monster):
        """进行战斗 - 修复战斗逻辑，移除额外的耐力消耗"""
        damage_taken = BattleSystem.calculate_damage(player, monster)
        player.health -= damage_taken
        # 移除战斗时的耐力消耗，因为探索森林时已经消耗了20点耐力
        # player.stamina = max(0, player.stamina - 20)  # 注释掉这一行
        
        if player.health > 0:
            player.gold += monster.gold_reward
            
            if monster.is_boss:
                player.bosses_defeated += 1
                chinese = f"你击败了 {monster.name.split(' / ')[0]}!\n受到伤害: {damage_taken}\n剩余生命: {player.health}\n击败了首领! 获得{monster.gold_reward}金币!"
                english = f"You defeated {monster.name.split(' / ')[1]}!\nDamage taken: {damage_taken}\nRemaining health: {player.health}\nDefeated the boss! Gained {monster.gold_reward} gold!"
            else:
                player.monsters_defeated += 1
                chinese = f"你击败了 {monster.name.split(' / ')[0]}!\n受到伤害: {damage_taken}\n剩余生命: {player.health}\n获得{monster.gold_reward}金币!"
                english = f"You defeated {monster.name.split(' / ')[1]}!\nDamage taken: {damage_taken}\nRemaining health: {player.health}\nGained {monster.gold_reward} gold!"
            
            return True, chinese + "\n\n" + english
        else:
            player.health = 0  # 确保生命值不会变成负数
            chinese = f"战斗失败... 被 {monster.name.split(' / ')[0]} 击败"
            english = f"Battle lost... Defeated by {monster.name.split(' / ')[1]}"
            return False, chinese + "\n" + english
    
    @staticmethod
    def attempt_escape(player):
        """尝试逃跑 - 修复耐力消耗"""
        player.escapes_attempted += 1
        # 逃跑消耗10点耐力，这是合理的，因为逃跑是额外的行动
        player.stamina = max(0, player.stamina - 10)  # 确保耐力不会变成负数
        
        if random.choice([True, False]):
            player.escapes_successful += 1
            chinese = "成功逃脱!"
            english = "Successfully escaped!"
            return True, chinese + "\n" + english
        else:
            chinese = "逃脱失败!"
            english = "Escape failed!"
            return False, chinese + "\n" + english

class EventSystem:
    @staticmethod
    def get_random_event(player):
        """获取随机事件，考虑玩家金币数量"""
        # 基础事件概率
        events = [
            ("monster", 0.35),      # 怪物遭遇
            ("trap", 0.15),         # 陷阱
            ("dark_ruin", 0.1),     # 黑暗遗迹
            ("shop", 0.15),         # 商店
            ("merchant", 0.1),      # 旅行商人
            ("nothing", 0.09),      # 无事发生
            ("time_leap", 0.06)     # 时间穿越
        ]
        
        # 如果玩家金币少于3，移除商店和商人事件
        if player.gold < 3:
            # 创建新的事件列表，排除商店和商人
            filtered_events = []
            total_prob = 0
            
            for event, prob in events:
                if event not in ["shop", "merchant"]:
                    filtered_events.append((event, prob))
                    total_prob += prob
            
            # 重新归一化概率，使总和为1
            if total_prob > 0:
                normalized_events = []
                for event, prob in filtered_events:
                    normalized_prob = prob / total_prob
                    normalized_events.append((event, normalized_prob))
                events = normalized_events
            else:
                # 如果没有合适的事件，默认返回怪物
                events = [("monster", 1.0)]
        
        # 根据概率随机选择事件
        rand = random.random()
        cumulative = 0
        for event, prob in events:
            cumulative += prob
            if rand <= cumulative:
                return event
        
        return "nothing"  # 默认返回"nothing"
    
    @staticmethod
    def handle_event(event_type, player):
        """处理事件，考虑玩家金币数量"""
        if event_type == "monster":
            return EventSystem.monster_encounter(player)
        elif event_type == "trap":
            return EventSystem.trap_encounter(player)
        elif event_type == "dark_ruin":
            return EventSystem.dark_ruin_encounter(player)
        elif event_type == "shop":
            # 检查玩家是否有足够金币
            if player.gold < 3:
                # 替换为无事发生
                chinese = "你看到一家商店，但因为没有足够的金币，你决定不进去..."
                english = "You see a shop, but without enough gold, you decide not to enter..."
                return "continue", chinese + "\n" + english, None
            else:
                return EventSystem.shop_encounter(player)
        elif event_type == "merchant":
            # 检查玩家是否有足够金币
            if player.gold < 3:
                # 替换为无事发生
                chinese = "你遇到一个旅行商人，但因为没有足够的金币，他忽略了你..."
                english = "You encounter a traveling merchant, but without enough gold, he ignores you..."
                return "continue", chinese + "\n" + english, None
            else:
                return EventSystem.merchant_encounter(player)
        elif event_type == "time_leap":
            return EventSystem.time_leap_encounter(player)
        else:
            chinese = "你在森林中漫步，但什么都没发生..."
            english = "You wander through the forest, but nothing happens..."
            return "continue", chinese + "\n" + english, None
    
    @staticmethod
    def monster_encounter(player):
        """遇到怪物"""
        monster = Monster(player.day)
        chinese = f"⚠️ 你遇到了 {monster.name.split(' / ')[0]}! ⚠️"
        english = f"⚠️ You encountered {monster.name.split(' / ')[1]}! ⚠️"
        return "monster", chinese + "\n" + english, monster
    
    @staticmethod
    def trap_encounter(player):
        """遇到陷阱"""
        damage = int(player.health * 0.1)
        player.health = max(1, player.health - damage)
        player.stamina = max(0, player.stamina - 10)
        chinese = f"💥 你触发了一个陷阱!\n失去 {damage} 生命和 10 耐力!"
        english = f"💥 You triggered a trap!\nLost {damage} HP and 10 Stamina!"
        return "continue", chinese + "\n" + english, None
    
    @staticmethod
    def dark_ruin_encounter(player):
        """黑暗遗迹事件"""
        if random.choice([True, False]):
            player.gold += 10
            chinese = "🏛️ 你发现了一处黑暗遗迹...\n✨ 找到了10金币!"
            english = "🏛️ You discover a dark ruin...\n✨ Found 10 gold!"
        else:
            effect = random.choice(["health", "attack", "stamina"])
            if effect == "health":
                player.max_health = player.max_health + 50
                chinese = "🏛️ 你发现了一处黑暗遗迹...\n✨ 黑暗魔法生效! 增加了50生命上限!"
                english = "🏛️ You discover a dark ruin...\n✨ Dark magic takes effect! Enhanced 50 Max-HP!"
            elif effect == "attack":
                player.attack += 10
                chinese = "🏛️ 你发现了一处黑暗遗迹...\n✨ 黑暗魔法生效! 攻击力增加了10!"
                english = "🏛️ You discover a dark ruin...\n✨ Dark magic takes effect! Attack increased by 10!"
            else:
                player.stamina = 100
                chinese = "🏛️ 你发现了一处黑暗遗迹...\n✨ 黑暗魔法生效! 恢复了全部耐力!"
                english = "🏛️ You discover a dark ruin...\n✨ Dark magic takes effect! Restored all Stamina!"
        return "continue", chinese + "\n" + english, None
    
    @staticmethod
    def shop_encounter(player):
        """商店事件"""
        shop = Shop(player)
        chinese = "🏪 您遇到了野外商店，您可以选择购买物品"
        english = "🏪 You encountered a wild shop, you can choose to buy items"
        return "shop", chinese + "\n" + english, shop
    
    @staticmethod
    def merchant_encounter(player):
        """旅行商人事件"""
        merchant = TravelingMerchant(player)
        chinese = "🧙 你遇到了一个旅行商人，他出售更加强力的稀有药水!"
        english = "🧙 You encountered a traveling merchant, he sells rare potions.!"
        return "merchant", chinese + "\n" + english, merchant

    @staticmethod
    def time_leap_encounter(player):
        """时间穿越事件"""
        # 保存当前状态，以便在需要时恢复
        original_day = player.day
        original_health = player.health
        original_max_health = player.max_health
        original_attack = player.attack
        original_base_attack = player.base_attack
        original_attack_bonus = player.attack_bonus
        original_defense = player.defense
        
        # 故事文本
        chinese = "❄️ 你在森林深处发现了一块散发着寒光的水晶碎片...\n\n"
        chinese += "当你触摸它时，一道耀眼的光芒将你包围！\n"
        chinese += "时间开始扭曲，周围的景象快速变化...\n\n"
        chinese += "当你再次睁开眼时，发现自己已经来到了第9天！\n"
        chinese += "神圣冰晶的力量融入了你的身体，赋予了你强大的力量！\n\n"
        chinese += "增益效果:\n"
        chinese += "- 最大生命值提升至800\n"
        chinese += "- 攻击力提升至150\n"
        chinese += "- 防御力提升至40\n"
        chinese += "- 耐力完全恢复\n\n"
        chinese += "你感到自己已经准备好面对最终的挑战！"
        
        english = "❄️ You discover a crystal shard emitting a cold light deep in the forest...\n\n"
        english += "As you touch it, a blinding light envelops you!\n"
        english += "Time begins to distort, the surroundings rapidly change...\n\n"
        english += "When you open your eyes again, you find yourself on Day 9!\n"
        english += "The power of the sacred ice crystal has merged with your body, granting you immense power!\n\n"
        english += "Bonus Effects:\n"
        english += "- Max HP increased to 800\n"
        english += "- Attack increased to 150\n"
        english += "- Defense increased to 40\n"
        english += "- Stamina fully restored\n\n"
        english += "You feel ready for the final challenge!"
        
        # 应用属性提升
        player.day = 9
        player.max_health = 800
        player.health = 800
        player.base_attack = 100  # 基础攻击力
        player.attack_bonus = 50  # 额外攻击力
        player.update_attack()
        player.defense = 40
        player.stamina = player.max_stamina
        
        # 添加特殊标签
        player.add_tag("时间旅行者 / Time Traveler")
        player.add_tag("冰晶守护者 / Crystal Guardian")
        
        # 保存穿越前的状态，以便玩家选择返回
        player.time_leap_original_stats = {
            'day': original_day,
            'health': original_health,
            'max_health': original_max_health,
            'base_attack': original_base_attack,
            'attack_bonus': original_attack_bonus,
            'defense': original_defense
        }
        
        return "time_leap", chinese + "\n\n" + english, None

class DarkForestGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("黑暗森林 / Dark Forest")
        self.root.geometry("840x600")
        self.root.configure(bg='#ffffff')
        
        self.player = Player()
        self.battle_system = BattleSystem()
        self.event_system = EventSystem()
        self.game_over = False
        
        self.current_event = None
        self.current_monster = None
        self.current_shop = None
        self.current_merchant = None
        
        # 每日消息字典
        self.daily_messages = {
            1: {
                "chinese": "第一天：你踏入黑暗森林。空气中弥漫着诡异的气息，远处似乎有低沉的咆哮在回荡。",
                "english": "Day 1: You step into the Dark Forest. The air is filled with an eerie aura, and distant low roars seem to echo."
            },
            2: {
                "chinese": "第二天：夜色更深，树影摇晃。你找到一块符文石，散发微光，指引着前行的方向。",
                "english": "Day 2: The night grows darker, tree shadows sway. You find a runestone emitting a faint glow, guiding your way forward."
            },
            3: {
                "chinese": "第三天：黑藤封路，腐臭弥漫。你点燃火焰，开出一条狭窄的小径，深处传来呢喃。",
                "english": "Day 3: Black vines block the path, a foul stench permeates. You light a flame, clearing a narrow path, whispers come from the depths."
            },
            4: {
                "chinese": "第四天：废墟中的祭坛闪烁微光。你的名字在古老石碑上浮现，命运似乎早已注定。",
                "english": "Day 4: An altar in the ruins flickers with a faint light. Your name appears on an ancient stone tablet, as if fate was predestined."
            },
            5: {
                "chinese": "第五天：森林中的阴影开始模仿你。它们的呼吸与步伐，与现实重叠，令人不寒而栗。",
                "english": "Day 5: Shadows in the forest begin to mimic you. Their breathing and footsteps overlap with reality, sending chills down your spine."
            },
            6: {
                "chinese": "第六天：你在月光下找到同伴的徽章。风声低语：‘继续前进，不要停下。’",
                "english": "Day 6: You find a companion's insignia under the moonlight. The wind whispers: 'Keep going, don't stop.'"
            },
            7: {
                "chinese": "第七天：黑暗侵蚀心智，你几乎忘了为何而来。那跳动的圣光提醒你——希望尚存。",
                "english": "Day 7: Darkness erodes your mind, you almost forget why you came. The pulsating holy light reminds you - hope still remains."
            },
            8: {
                "chinese": "第八天：血月升起，暗影王的领地展现眼前。空气中弥漫腐败与魔力的气息。",
                "english": "Day 8: The blood moon rises, the Shadow King's domain unfolds before your eyes. The air is filled with the scent of decay and magic."
            },
            9: {
                "chinese": "第九天：三盏灵魂灯点亮，照亮终极祭坛。地面震动，一股庞大的存在苏醒了。",
                "english": "Day 9: Three soul lamps light up, illuminating the ultimate altar. The ground trembles, a massive presence awakens."
            },
            10: {
                "chinese": "第十天：黑暗魔龙咆哮着从深渊升起！这是最后的战斗——唯有胜者，才能迎来黎明！",
                "english": "Day 10: The Dark Magic Dragon roars as it rises from the abyss! This is the final battle - only the victor will greet the dawn!"
            }
        }
        
        self.setup_gui()
        self.show_intro()  # 显示介绍页面而不是直接开始游戏
        
    def show_intro(self):
        """显示游戏介绍页面"""
        self.current_event = "intro"
        
        message = "🌲 黑暗森林 / Dark Forest 🌲\n\n"
        message += "背景: 在一片古老的大陆上，被黑暗力量笼罩的森林吸引了无数勇士...\n"
        message += "Backstory: On an ancient continent, a forest shrouded in dark forces lured countless warriors...\n\n"
        message += "这片森林充满了危险与机遇，只有最勇敢的冒险者才能揭开它的秘密。\n"
        message += "This forest is full of dangers and opportunities, only the bravest adventurers can uncover its secrets."
        
        self.show_message(message)
        self.clear_buttons()
        self.set_button(2, "开始游戏\nStart Game", tk.NORMAL)  # 将开始按钮放在中间位置
    
    def handle_intro(self, choice):
        """处理介绍页面的按钮点击"""
        if choice == 2:  # 开始游戏按钮
            self.start_game()
            
    def setup_gui(self):
        """设置GUI界面"""
        # 标题
        title_label = tk.Label(
            self.root, 
            text="🌲 黑暗森林 / Dark Forest 🌲", 
            font=("Arial", 20, "bold"),
            fg="#0F5FA1",
            bg="#ffffff"
        )
        title_label.pack(pady=10)
        
        # 状态显示区域
        self.stats_frame = tk.Frame(self.root, bg='#1e1e1e')  # 文本框背景保持黑色
        self.stats_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.stats_text = tk.Text(
            self.stats_frame, 
            height=6, 
            width=80,
            font=("Arial", 12),
            bg='#1e1e1e',
            fg='#ffffff',
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.stats_text.pack(fill=tk.BOTH, expand=True)
        
        # 事件显示区域
        self.event_frame = tk.Frame(self.root, bg='#1e1e1e')  # 文本框背景保持黑色
        self.event_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.event_text = tk.Text(
            self.event_frame, 
            height=10, 
            width=80,
            font=("Arial", 14),
            bg='#1e1e1e',
            fg='#ffffff',
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.event_text.pack(fill=tk.BOTH, expand=True)
        
        # 选项按钮区域 - 增加按钮行的高度
        self.buttons_frame = tk.Frame(self.root, bg='#1e1e1e', height=80)  # 增加按钮框架高度
        self.buttons_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=10)
        self.buttons_frame.pack_propagate(False)  # 防止框架被内容压缩
        
        self.buttons = []
        for i in range(5):  # 5个按钮
            btn = tk.Button(
                self.buttons_frame,
                text="",
                font=("Arial", 12),  # 增加默认字体大小
                bg="#0F6B4C",
                fg='white',
                height=3,  # 增加按钮高度
                # 不设置固定宽度，使用expand和fill来动态调整
                command=lambda i=i: self.on_button_click(i)
            )
            btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2)
            self.buttons.append(btn)
            
        # 绑定窗口大小变化事件
        self.root.bind('<Configure>', self.on_window_resize)
        
    def on_window_resize(self, event):
        """窗口大小变化时的回调函数"""
        # 动态调整按钮字体大小
        window_width = self.root.winfo_width()
        # 增加字体大小范围，确保按钮文本清晰可见
        base_font_size = max(10, min(14, window_width // 60))
        
        for btn in self.buttons:
            btn.configure(font=("Arial", base_font_size))
            
    def update_ui_color(self):
        """根据耐力值更新UI背景颜色"""
        stamina = self.player.stamina
        
        if stamina >= 60:
            # 白天 - 白色背景
            bg_color = '#ffffff'
        elif stamina >= 20:
            # 黄昏 - 橙黄色背景
            bg_color = '#FFA500'
        else:
            # 夜晚 - 藏青色背景
            bg_color = '#191970'
        
        # 更新主窗口背景色
        self.root.configure(bg=bg_color)
        
        # 更新标题背景色
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Label) and "黑暗森林" in widget.cget("text"):
                widget.configure(bg=bg_color)
    
    def update_stats(self):
        """更新状态显示"""
        self.stats_text.config(state=tk.NORMAL)
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(1.0, self.player.get_stats_text())
        self.stats_text.config(state=tk.DISABLED)
        
        # 更新UI颜色
        self.update_ui_color()
    
    def show_message(self, message):
        """显示消息，替换中部文本框内容"""
        self.event_text.config(state=tk.NORMAL)
        self.event_text.delete(1.0, tk.END)
        self.event_text.insert(1.0, message)
        self.event_text.config(state=tk.DISABLED)
        # 强制更新GUI
        self.root.update()
        
        # 更新UI颜色
        self.update_ui_color()
    
    def clear_buttons(self):
        """清除按钮文本"""
        for btn in self.buttons:
            btn.config(text="", state=tk.DISABLED)
    
    def set_button(self, index, text, state=tk.NORMAL):
        """设置按钮文本和状态"""
        if index < len(self.buttons):
            self.buttons[index].config(text=text, state=state)
    
    def on_button_click(self, button_index):
        """按钮点击事件处理"""
        print(f"Button clicked: {button_index}, current_event: {self.current_event}, game_over: {self.game_over}")  # 调试信息
        
        # 如果游戏结束，只处理失败屏幕的按钮
        if self.game_over and self.current_event != "defeat":
            return
            
        if self.current_event == "intro":
            self.handle_intro(button_index)
        elif self.current_event == "main":
            self.handle_main_menu(button_index)
        elif self.current_event == "monster":
            self.handle_monster_event(button_index)
        elif self.current_event == "shop":
            self.handle_shop_event(button_index)
        elif self.current_event == "merchant":
            self.handle_merchant_event(button_index)
        elif self.current_event == "rest":
            self.handle_rest_event(button_index)
        elif self.current_event == "battle_result":
            self.handle_battle_result(button_index)
        elif self.current_event == "defeat":
            self.handle_defeat(button_index)
        elif self.current_event == "event_result":
            self.handle_event_result(button_index)
        elif self.current_event == "camp_rest_result":
            self.handle_camp_rest_result(button_index)
        elif self.current_event == "time_leap":  # 添加时间穿越事件处理
            self.handle_time_leap_event(button_index)
        elif self.current_event == "time_leap_choice":  # 添加时间穿越选择处理
            self.handle_time_leap_choice(button_index)
        elif self.current_event == "merchant_purchase_result":  # 添加商人购买结果处理
            self.handle_merchant_purchase_result(button_index)
        elif self.current_event == "shop_purchase_result":  # 添加商店购买结果处理
            self.handle_shop_purchase_result(button_index)
        elif self.current_event == "short_rest_result":  # 添加短暂休息结果处理
            self.handle_short_rest_result(button_index)
        elif self.current_event == "boss_defeated":  # 添加小BOSS击败处理
            self.handle_boss_defeated(button_index)
        elif self.current_event == "final_boss_strategy":  # 添加最终BOSS策略选择处理
            self.handle_final_boss_strategy(button_index)
        elif self.current_event == "final_boss_battle":  # 添加最终BOSS战斗处理
            self.handle_final_boss_battle(button_index)
        elif self.current_event == "final_boss_result":  # 添加最终BOSS结果处理
            self.handle_final_boss_result(button_index)
        elif self.current_event == "merchant_insufficient_gold":  # 添加旅行商人金币不足处理
            self.handle_merchant_insufficient_gold(button_index)
        elif self.current_event == "shop_insufficient_gold":  # 添加商店金币不足处理
            self.handle_shop_insufficient_gold(button_index)
    
    def start_game(self):
        """开始游戏"""
        self.player.save_day_start()
        # 直接进入主菜单，不再显示第一天的消息
        self.show_main_menu()
    
    def show_main_menu(self):
        """显示主菜单，包含当天故事"""
        self.current_event = "main"
        self.game_over = False  # 确保游戏状态重置
        self.update_stats()
        self.update_tags()
        
        # 获取当天故事
        day = self.player.day
        if day in self.daily_messages:
            daily_msg = self.daily_messages[day]["chinese"] + "\n\n" + self.daily_messages[day]["english"]
        else:
            daily_msg = f"第{day}天 / Day {day}"
        
        # 第九天添加决战提示
        if day == 9:
            daily_msg += "\n\n" + "="*50 + "\n\n"
            daily_msg += "第十天即将迎来决战，请做好准备！\n"
            daily_msg += "The final battle approaches on Day 10, prepare yourself!"
        
        # 添加菜单选项
        menu_msg = "\n\n" + "="*50 + "\n\n"
        menu_msg += "选择行动 / Choose action:"
        
        # 组合消息
        full_message = daily_msg + menu_msg
        self.show_message(full_message)
        
        self.clear_buttons()
        
        self.set_button(0, "1. 探索森林\nExplore Forest", tk.NORMAL)
        self.set_button(1, "2. 休息\nRest", tk.NORMAL)
        self.set_button(2, "3. 查看状态\nView Stats", tk.NORMAL)
        self.set_button(3, "4. 退出游戏\nExit Game", tk.NORMAL)
        # 第5个按钮留空
        self.set_button(4, "", tk.DISABLED)
    
    def handle_main_menu(self, choice):
        """处理主菜单选择"""
        if choice == 0:  # 探索森林
            self.explore_forest()
        elif choice == 1:  # 休息
            self.show_rest_options()
        elif choice == 2:  # 查看状态
            self.update_stats()
            message = "当前状态已更新 / Status updated"
            self.show_message(message)
        elif choice == 3:  # 退出游戏
            self.root.quit()
    
    def explore_forest(self):
        """探索森林"""
        if self.player.stamina >= 20:
            self.player.stamina -= 20  # 探索森林消耗20点耐力
            self.player.has_explored_today = True  # 标记今天已经探索过
            
            # 第十天直接进入最终BOSS战斗
            if self.player.day == 10:
                self.final_boss_battle()
                return
                
            event_type = self.event_system.get_random_event(self.player)
            result = self.event_system.handle_event(event_type, self.player)
            
            self.current_event = result[0]
            self.show_message(result[1])
            
            if self.current_event == "monster":
                self.current_monster = result[2]
                self.show_monster_options()
            elif self.current_event == "shop":
                self.current_shop = result[2]
                self.show_shop_options()
            elif self.current_event == "merchant":
                self.current_merchant = result[2]
                self.show_merchant_options()
            elif self.current_event == "time_leap":
                # 时间穿越事件，显示继续按钮
                self.current_event = "time_leap"
                self.clear_buttons()
                self.set_button(2, "继续\nContinue", tk.NORMAL)
            else:
                # 其他事件显示"继续游戏"按钮，而不是自动返回
                self.current_event = "event_result"
                self.clear_buttons()
                self.set_button(2, "继续游戏\nContinue", tk.NORMAL)
        else:
            message = "耐力不足，无法探索! / Not enough stamina to explore!"
            self.show_message(message)
            self.root.after(2000, self.show_main_menu)
    
    def final_boss_battle(self):
        """最终BOSS战斗"""
        self.current_monster = Monster(self.player.day, is_boss=True)
        
        # 显示战斗策略选择界面
        self.current_event = "final_boss_strategy"
        
        message = "!!! 最终BOSS战 !!! / !!! FINAL BOSS BATTLE !!!\n\n"
        message += self.current_monster.get_stats_text() + "\n\n"
        message += "选择战斗策略 / Choose battle strategy:\n\n"
        message += "1. 猛攻 - 增加80%攻击力 / Fierce Attack - Increase attack by 80%\n"
        message += "2. 防御 - 增加50%防御力 / Defense - Increase defense by 50%\n"
        message += "3. 闪避 - 增加30%闪避率 / Dodge - Increase dodge rate by 30%\n"
        message += "4. 狂暴 - 增加100%攻击力，减少20%防御力 / Berserk - Increase attack by 100%, decrease defense by 20%"
        
        self.show_message(message)
        
        self.clear_buttons()
        self.set_button(0, "1. 猛攻\nFierce Attack", tk.NORMAL)
        self.set_button(1, "2. 防御\nDefense", tk.NORMAL)
        self.set_button(2, "3. 闪避\nDodge", tk.NORMAL)
        self.set_button(3, "4. 狂暴\nBerserk", tk.NORMAL)
        # 第5个按钮留空
        self.set_button(4, "", tk.DISABLED)

    def handle_final_boss_strategy(self, choice):
        """处理最终BOSS策略选择"""
        # 保存原始属性
        original_attack = self.player.attack
        original_defense = self.player.defense
        
        # 应用策略效果
        if choice == 0:  # 猛攻
            self.player.attack = int(self.player.attack * 1.8)
            strategy_name = "猛攻 / Fierce Attack"
        elif choice == 1:  # 防御
            self.player.defense = int(self.player.defense * 1.5)
            strategy_name = "防御 / Defense"
        elif choice == 2:  # 闪避
            # 闪避策略：有30%几率完全躲避攻击
            strategy_name = "闪避 / Dodge"
            # 这里我们通过修改战斗系统来实现闪避效果
        elif choice == 3:  # 狂暴
            self.player.attack = int(self.player.attack * 2.0)
            self.player.defense = int(self.player.defense * 0.8)
            strategy_name = "狂暴 / Berserk"
        
        # 显示战斗过程
        self.current_event = "final_boss_battle"
        
        message = f"你选择了 {strategy_name} 策略!\n\n"
        message += "勇士与恶龙展开了激烈的战斗.......\n"
        message += "战斗持续了很久........\n"
        message += "但最后......\n\n"
        
        message += f"You chose the {strategy_name.split(' / ')[1]} strategy!\n\n"
        message += "The warrior and the evil dragon engaged in a fierce battle.......\n"
        message += "The battle lasted for a long time........\n"
        message += "But in the end......"
        
        self.show_message(message)
        
        self.clear_buttons()
        self.set_button(2, "点击继续\nClick to Continue", tk.NORMAL)

    def handle_final_boss_battle(self, choice):
        """处理最终BOSS战斗继续按钮"""
        # 进行战斗 - 最终BOSS战斗也不消耗额外耐力
        success, message = self.battle_system.fight(self.player, self.current_monster)
        
        # 显示战斗结果
        self.current_event = "final_boss_result"
        
        battle_result_message = message + "\n\n"
        if success:
            battle_result_message += "你成功击败了黑暗魔龙！\n"
            battle_result_message += "黑暗森林的阴霾散去，世界重获光明！\n"
            battle_result_message += "胜利！\n\n"
            battle_result_message += "最终统计 / Final Stats:\n"
            battle_result_message += f"总天数 / Total Days: {self.player.day}\n"
            battle_result_message += f"击败怪物 / Monsters Defeated: {self.player.monsters_defeated}\n"
            battle_result_message += f"击败首领 / Bosses Defeated: {self.player.bosses_defeated}\n"
            battle_result_message += f"最终称号 / Final Tags: {', '.join(self.player.tags)}\n\n"
            
            battle_result_message += "You successfully defeated the Dark Magic Dragon!\n"
            battle_result_message += "The gloom of the Dark Forest dissipates, and the world regains its light!\n"
            battle_result_message += "Victory!\n\n"
            battle_result_message += "Final Statistics:\n"
            battle_result_message += f"Total Days: {self.player.day}\n"
            battle_result_message += f"Monsters Defeated: {self.player.monsters_defeated}\n"
            battle_result_message += f"Bosses Defeated: {self.player.bosses_defeated}\n"
            battle_result_message += f"Final Tags: {', '.join(self.player.tags)}\n"
        else:
            battle_result_message += "你被黑暗魔龙击败了...\n"
            battle_result_message += "世界被黑暗吞噬...\n"
            battle_result_message += "失败...\n\n"
            
            battle_result_message += "You were defeated by the Dark Magic Dragon...\n"
            battle_result_message += "The world is swallowed by darkness...\n"
            battle_result_message += "Defeat...\n"
        
        self.show_message(battle_result_message)
        
        self.clear_buttons()
        if success:
            self.set_button(2, "胜利！点击退出\nVictory! Click to Exit", tk.NORMAL)
        else:
            self.set_button(0, "重新开始今天\nRestart Day", tk.NORMAL)
            self.set_button(1, "重新开始游戏\nRestart Game", tk.NORMAL)
            self.set_button(2, "退出游戏\nExit Game", tk.NORMAL)

    def handle_final_boss_result(self, choice):
        """处理最终BOSS战斗结果"""
        if choice == 2:  # 胜利退出或失败退出
            if self.player.health > 0:  # 胜利
                self.root.quit()
            else:  # 失败退出
                self.root.quit()
        elif choice == 0:  # 重新开始今天
            self.player.restore_day_start()
            self.game_over = False
            self.current_event = "main"
            self.show_main_menu()
        elif choice == 1:  # 重新开始游戏
            # 完全重新初始化游戏
            self.player = Player()
            self.battle_system = BattleSystem()
            self.event_system = EventSystem()
            self.game_over = False
            self.current_event = None
            self.current_monster = None
            self.current_shop = None
            self.current_merchant = None
            
            # 清除并重新设置界面
            for widget in self.root.winfo_children():
                widget.destroy()
            self.setup_gui()
            self.start_game()
    
    def handle_time_leap_event(self, choice):
        """处理时间穿越事件的按钮点击"""
        if choice == 2:  # 继续按钮
            # 显示特殊选项：继续前进或返回原来时间线
            self.show_time_leap_options()
    
    def show_time_leap_options(self):
        """显示时间穿越后的选项"""
        message = "时间穿越完成！你现在处于第9天的时间线。\n\n"
        message += "Time leap completed! You are now in the Day 9 timeline.\n\n"
        message += "选择你的行动 / Choose your action:\n\n"
        message += "1. 继续前进 - 接受命运，迎接最终挑战\n"
        message += "   Continue Forward - Accept your fate, face the final challenge\n\n"
        message += "2. 返回过去 - 使用冰晶剩余能量回到原来的时间\n"
        message += "   Return to Past - Use remaining crystal energy to return to your original time"
        
        self.show_message(message)
        
        self.current_event = "time_leap_choice"
        self.clear_buttons()
        self.set_button(0, "1. 继续前进\nContinue Forward", tk.NORMAL)
        self.set_button(1, "2. 返回过去\nReturn to Past", tk.NORMAL)
    
    def handle_time_leap_choice(self, choice):
        """处理时间穿越选择"""
        if choice == 0:  # 继续前进
            message = "你决定接受冰晶赋予的命运，继续在第9天的时间线前进！\n"
            message += "You decide to accept the fate given by the crystal, continuing in the Day 9 timeline!\n\n"
            message += "黑暗魔龙在等待着你...\n"
            message += "The Dark Magic Dragon awaits you..."
            self.show_message(message)
            self.root.after(3000, self.show_main_menu)
        
        elif choice == 1:  # 返回过去
            # 恢复原始状态
            if hasattr(self.player, 'time_leap_original_stats'):
                stats = self.player.time_leap_original_stats
                self.player.day = stats['day']
                self.player.health = stats['health']
                self.player.max_health = stats['max_health']
                self.player.base_attack = stats['base_attack']
                self.player.attack_bonus = stats['attack_bonus']
                self.player.update_attack()
                self.player.defense = stats['defense']
                
                # 移除时间旅行相关标签
                if "时间旅行者 / Time Traveler" in self.player.tags:
                    self.player.tags.remove("时间旅行者 / Time Traveler")
                if "冰晶守护者 / Crystal Guardian" in self.player.tags:
                    self.player.tags.remove("冰晶守护者 / Crystal Guardian")
                
                # 添加新标签
                self.player.add_tag("时空漫游者 / Temporal Wanderer")
            
            message = "你使用冰晶剩余的能量回到了原来的时间线...\n"
            message += "You use the remaining crystal energy to return to your original timeline...\n\n"
            message += "虽然失去了强大的力量，但这段经历让你更加明智。\n"
            message += "Though you lost the great power, this experience has made you wiser."
            self.show_message(message)
            self.root.after(3000, self.show_main_menu)
            
    def handle_event_result(self, choice):
        """处理事件结果的按钮点击"""
        if choice == 2:  # 继续游戏按钮
            self.show_main_menu()
    
    def handle_shop_insufficient_gold(self, choice):
        """处理商店金币不足的按钮点击"""
        if choice == 2:  # 返回购物按钮
            self.show_shop_options()
        
    def show_monster_options(self):
        """显示怪物遭遇选项"""
        self.clear_buttons()
        
        monster_text = self.current_monster.get_stats_text()
        battle_prediction = self.battle_system.predict_battle(self.player, self.current_monster)
        
        current_message = self.event_text.get(1.0, tk.END) + "\n\n" + monster_text + "\n\n" + battle_prediction
        self.show_message(current_message)
        
        # 战斗按钮始终可用，即使耐力不足
        self.set_button(0, "1. 战斗\nFight", tk.NORMAL)
        
        # 逃跑按钮只在耐力足够时可用
        self.set_button(1, "2. 逃跑\nFlee", tk.NORMAL if self.player.stamina >= 10 else tk.DISABLED)
        
        # 其他按钮留空
        self.set_button(2, "", tk.DISABLED)
        self.set_button(3, "", tk.DISABLED)
        self.set_button(4, "", tk.DISABLED)
    
    def handle_monster_event(self, choice):
        """处理怪物遭遇"""
        if choice == 0:  # 战斗
            success, message = self.battle_system.fight(self.player, self.current_monster)
            self.show_message(message)
            self.current_event = "battle_result"
            self.clear_buttons()
            self.set_button(0, "继续 ▶️\nContinue", tk.NORMAL)
        
        elif choice == 1:  # 逃跑
            if self.player.stamina >= 10:
                success, message = self.battle_system.attempt_escape(self.player)
                self.show_message(message)
                if success:
                    self.root.after(2000, self.show_main_menu)
                else:
                    # 逃跑失败，必须战斗
                    message += "\n\n逃跑失败，被迫战斗! / Escape failed, forced to fight!"
                    success, battle_message = self.battle_system.fight(self.player, self.current_monster)
                    self.show_message(message + "\n" + battle_message)
                    self.current_event = "battle_result"
                    self.clear_buttons()
                    self.set_button(0, "继续 ▶️\nContinue", tk.NORMAL)
            else:
                message = "耐力不足，无法逃跑! / Not enough stamina to flee!"
                self.show_message(message)
                self.root.after(2000, self.show_main_menu)
    
    def handle_merchant_purchase_result(self, choice):
        """处理旅行商人购买结果的按钮点击"""
        if choice == 2:  # 继续购物按钮
            self.show_merchant_options()
    
    def handle_battle_result(self, choice):
        """处理战斗结果"""
        if self.player.health <= 0:
            self.game_over = True
            self.show_defeat_screen()
        else:
            self.check_boss_encounter()
    
    def check_boss_encounter(self):
        """检查BOSS遭遇 - 修复BOSS遭遇逻辑"""
        # 只有在第十天才会触发最终BOSS
        if self.player.day == 10:
            self.boss_battle()
        # 其他天数只有在玩家生命值足够高时才可能遇到小BOSS
        elif self.player.health >= 200 and self.player.day < 10:
            # 增加遇到小BOSS的概率检查
            if random.random() < 0.3:  # 30%概率遇到小BOSS
                self.boss_battle()
            else:
                self.show_main_menu()
        else:
            self.show_main_menu()
    
    def boss_battle(self):
        """BOSS战斗 - 修复BOSS战斗逻辑"""
        if self.player.day == 10:
            boss = Monster(self.player.day, is_boss=True)
            message = "!!! 最终BOSS战 !!! / !!! FINAL BOSS BATTLE !!!\n\n"
        else:
            boss = Monster(self.player.day, is_boss=True)
            message = f"!!! 第{self.player.day}天首领战 !!! / !!! Day {self.player.day} Boss Battle !!!\n\n"
        
        message += boss.get_stats_text() + "\n\n"
        message += self.battle_system.predict_battle(self.player, boss) + "\n\n"
        
        # 检查玩家是否能击败BOSS
        damage_taken = self.battle_system.calculate_damage(self.player, boss)
        if self.player.health <= damage_taken:
            message += "警告: 这场战斗可能会导致死亡! / WARNING: This battle may result in death!\n\n"
        
        message += "你必须战斗! / You must fight!"
        
        self.show_message(message)
        self.current_monster = boss
        
        self.clear_buttons()
        self.set_button(0, "战斗 ⚔️\nFight", tk.NORMAL)
        
        # 直接进入战斗
        success, battle_message = self.battle_system.fight(self.player, boss)
        self.show_message(battle_message)
        
        if success:
            if self.player.day == 10:
                self.victory()
            else:
                # 小BOSS击败后不自动进入下一天，让玩家选择
                message = "击败了首领! / Defeated the boss!"
                self.show_message(message)
                self.current_event = "boss_defeated"
                self.clear_buttons()
                self.set_button(2, "继续游戏\nContinue", tk.NORMAL)
        else:
            self.game_over = True
            self.show_defeat_screen()
    
    def handle_boss_defeated(self, choice):
        """处理小BOSS击败后的选项"""
        if choice == 2:  # 继续游戏按钮
            self.show_main_menu()
    
    def victory(self):
        """胜利结局"""
        message = "\n" + "="*50 + "\n"
        message += "你成功击败了黑暗魔龙！\n"
        message += "黑暗森林的阴霾散去，失去黑暗魔法能量的小怪物们离开了。\n"
        message += "森林获得了新生。\n"
        message += "胜利！\n"
        message += "="*50 + "\n\n"
        
        message += "最终统计 / Final Stats:\n"
        message += f"总天数 / Total Days: {self.player.day}\n"
        message += f"击败怪物 / Monsters Defeated: {self.player.monsters_defeated}\n"
        message += f"击败首领 / Bosses Defeated: {self.player.bosses_defeated}\n"
        message += f"最终称号 / Final Tags: {', '.join(self.player.tags)}\n\n"
        
        message += "5秒后自动退出... / Auto exit in 5 seconds..."
        
        self.show_message(message)
        self.clear_buttons()
        
        self.root.after(5000, self.root.quit)
    
    def show_shop_options(self):
        """显示商店选项"""
        # 确保当前事件设置为shop
        self.current_event = "shop"
        shop_text = self.current_shop.get_items_text()
        self.show_message(shop_text)
        
        self.clear_buttons()
        for i in range(3):
            if i < len(self.current_shop.items):
                item = self.current_shop.items[i]
                # 使用双语按钮文本
                btn_text = f"{i+1}. {item['name'].split(' / ')[0]}\n{item['name'].split(' / ')[1]}"
                self.set_button(i, btn_text, tk.NORMAL)
        
        self.set_button(3, "0. 离开\nExit", tk.NORMAL)
        # 第5个按钮留空
        self.set_button(4, "", tk.DISABLED)
    
    def handle_shop_event(self, choice):
        """处理商店事件"""
        # 确保当前事件是shop，避免状态混乱
        self.current_event = "shop"
        
        if choice == 3:  # 离开
            self.show_main_menu()
        else:
            # 检查商店是否可用
            if not self.current_shop.is_available():
                message = "商店不可用 / Shop is not available"
                self.show_message(message)
                self.root.after(2000, self.show_main_menu)
                return
                    
            success, message = self.current_shop.buy_item(self.player, choice + 1)
            
            if success:
                # 获取购买物品的详细信息
                item = self.current_shop.items[choice]
                effect_message = self.get_item_effect_message(item, self.player)
                
                # 显示购买结果页面
                result_message = message + "\n\n" + effect_message
                self.show_message(result_message)
                
                # 更新状态显示
                self.update_stats()
                
                # 设置当前事件为商店购买结果
                self.current_event = "shop_purchase_result"
                self.clear_buttons()
                self.set_button(2, "继续购物\nContinue Shopping", tk.NORMAL)
            else:
                # 购买失败，显示专门的错误信息页面
                self.show_message(message)
                
                # 更新状态显示
                self.update_stats()
                
                # 设置当前事件为商店金币不足
                self.current_event = "shop_insufficient_gold"
                self.clear_buttons()
                self.set_button(2, "返回购物\nBack to Shopping", tk.NORMAL)
                
    def handle_shop_purchase_result(self, choice):
        """处理商店金币不足的按钮点击"""
        if choice == 2:  # 返回购物按钮
            self.show_shop_options()
            
    def get_item_effect_message(self, item, player):
        """获取物品效果的双语消息"""
        effect = item['effect']
        
        if effect == "health_50":
            chinese = f"增益效果: 最大生命值增加50，当前生命值: {player.health}/{player.max_health}"
            english = f"Effect: Max HP increased by 50, Current HP: {player.health}/{player.max_health}"
        elif effect == "attack_10":
            chinese = f"增益效果: 攻击力增加10，当前攻击力: {player.attack}"
            english = f"Effect: Attack increased by 10, Current Attack: {player.attack}"
        elif effect == "health_20_percent":
            chinese = f"增益效果: 最大生命值增加20%，当前生命值: {player.health}/{player.max_health}"
            english = f"Effect: Max HP increased by 20%, Current HP: {player.health}/{player.max_health}"
        elif effect == "attack_20_percent":
            chinese = f"增益效果: 攻击力增加20%，当前攻击力: {player.attack}"
            english = f"Effect: Attack increased by 20%, Current Attack: {player.attack}"
        elif effect == "defense_5":
            chinese = f"增益效果: 防御力增加5，当前防御力: {player.defense}"
            english = f"Effect: Defense increased by 5, Current Defense: {player.defense}"
        elif effect == "stamina_full":
            chinese = f"增益效果: 耐力完全恢复，当前耐力: {player.stamina}/{player.max_stamina}"
            english = f"Effect: Stamina fully restored, Current Stamina: {player.stamina}/{player.max_stamina}"
        elif effect == "mystery":
            # 神秘药水的效果是随机的，我们需要根据实际效果显示
            if player.max_health > 100:  # 假设初始最大生命值为100
                chinese = f"增益效果: 最大生命值增加100，当前生命值: {player.health}/{player.max_health}"
                english = f"Effect: Max HP increased by 100, Current HP: {player.health}/{player.max_health}"
            else:
                chinese = f"增益效果: 攻击力增加20，当前攻击力: {player.attack}"
                english = f"Effect: Attack increased by 20, Current Attack: {player.attack}"
        elif effect == "berserk":
            chinese = f"增益效果: 攻击力增加15，防御力减少3，当前攻击力: {player.attack}，当前防御力: {player.defense}"
            english = f"Effect: Attack increased by 15, Defense decreased by 3, Current Attack: {player.attack}, Current Defense: {player.defense}"
        elif effect == "fool":
            chinese = f"增益效果: 生命值减少10，攻击力增加30，当前生命值: {player.health}，当前攻击力: {player.attack}"
            english = f"Effect: HP decreased by 10, Attack increased by 30, Current HP: {player.health}, Current Attack: {player.attack}"
        elif effect == "mystic":
            # 神秘药水的效果是随机的，我们需要根据实际效果显示
            if player.max_health > 100:  # 假设初始最大生命值为100
                chinese = f"增益效果: 最大生命值增加100，当前生命值: {player.health}/{player.max_health}"
                english = f"Effect: Max HP increased by 100, Current HP: {player.health}/{player.max_health}"
            else:
                chinese = f"增益效果: 攻击力增加20，当前攻击力: {player.attack}"
                english = f"Effect: Attack increased by 20, Current Attack: {player.attack}"
        elif effect == "madman":
            chinese = f"增益效果: 攻击力增加30，防御力减少5，当前攻击力: {player.attack}，当前防御力: {player.defense}"
            english = f"Effect: Attack increased by 30, Defense decreased by 5, Current Attack: {player.attack}, Current Defense: {player.defense}"
        elif effect == "dark_magic":
            chinese = f"增益效果: 最大生命值增加100，攻击力增加50，当前生命值: {player.health}/{player.max_health}，当前攻击力: {player.attack}"
            english = f"Effect: Max HP increased by 100, Attack increased by 50, Current HP: {player.health}/{player.max_health}, Current Attack: {player.attack}"
        else:
            chinese = "增益效果: 未知效果"
            english = "Effect: Unknown effect"
        
        return chinese + "\n" + english
    
    def show_merchant_options(self):
        """显示旅行商人选项"""
        # 确保当前事件设置为merchant
        self.current_event = "merchant"
        merchant_text = self.current_merchant.get_items_text()
        self.show_message(merchant_text)
        
        self.clear_buttons()
        # 显示4个物品按钮
        for i in range(4):
            if i < len(self.current_merchant.items):
                item = self.current_merchant.items[i]
                # 使用双语按钮文本
                btn_text = f"{i+1}. {item['name'].split(' / ')[0]}\n{item['name'].split(' / ')[1]}"
                self.set_button(i, btn_text, tk.NORMAL)
        
        # 第5个按钮显示离开选项
        self.set_button(4, "0. 离开\nLeave", tk.NORMAL)

    def handle_merchant_event(self, choice):
        """处理旅行商人事件"""
        # 确保当前事件是merchant，避免状态混乱
        self.current_event = "merchant"
        
        if choice == 4:  # 离开按钮 (第5个按钮)
            self.show_main_menu()
        else:
            # 检查商人是否可用
            if not self.current_merchant.is_available():
                message = "商人不可用 / Merchant is not available"
                self.show_message(message)
                self.root.after(2000, self.show_main_menu)
                return
                    
            success, message = self.current_merchant.buy_item(self.player, choice + 1)
            
            if success:
                # 获取购买物品的详细信息
                item = self.current_merchant.items[choice]
                effect_message = self.get_item_effect_message(item, self.player)
                
                # 显示购买结果页面
                result_message = message + "\n\n" + effect_message
                self.show_message(result_message)
                
                # 更新状态显示
                self.update_stats()
                
                # 设置当前事件为商人购买结果
                self.current_event = "merchant_purchase_result"
                self.clear_buttons()
                self.set_button(2, "继续购物\nContinue Shopping", tk.NORMAL)
            else:
                # 购买失败，显示专门的错误信息页面
                self.show_message(message)
                
                # 更新状态显示
                self.update_stats()
                
                # 设置当前事件为商人金币不足
                self.current_event = "merchant_insufficient_gold"
                self.clear_buttons()
                self.set_button(2, "返回购物\nBack to Shopping", tk.NORMAL)
    
    def handle_merchant_insufficient_gold(self, choice):
        """处理旅行商人金币不足的按钮点击"""
        if choice == 2:  # 返回购物按钮
            self.show_merchant_options()
    
    def show_rest_options(self):
        """显示休息选项"""
        self.current_event = "rest"
        
        message = "选择休息方式 / Choose rest option:\n\n"
        message += "1. 短暂休息 - 恢复20点生命，消耗5耐力\n"
        message += "   Short Rest - Restores 20 HP, consumes 5 Stamina\n\n"
        
        # 第十天不显示露营休息选项
        if self.player.day < 10:
            message += "2. 露营休息 - 进入下一天，完全恢复生命和耐力\n"
            message += "   Camp Rest - Advances to next day, fully restores HP and Stamina\n\n"
        else:
            message += "（第十天无法露营休息，必须面对最终战斗）\n"
            message += "(Cannot camp on Day 10, must face the final battle)\n\n"
        
        message += "0. 返回 / Back"
        
        self.show_message(message)
        
        self.clear_buttons()
        self.set_button(0, "1. 短暂休息\nShort Rest", tk.NORMAL if self.player.stamina >= 5 else tk.DISABLED)
        
        # 第十天禁用露营休息按钮
        if self.player.day < 10:
            self.set_button(1, "2. 露营休息\nCamp Rest", tk.NORMAL)
        else:
            self.set_button(1, "2. 露营休息\nCamp Rest", tk.DISABLED)
        
        # 其他按钮留空
        self.set_button(2, "", tk.DISABLED)
        self.set_button(3, "", tk.DISABLED)
        self.set_button(4, "0. 返回\nBack", tk.NORMAL)
    
    
    def handle_rest_event(self, choice):
        """处理休息选项"""
        if choice == 0:  # 短暂休息
            if self.player.stamina >= 5:
                heal_amount = 20  # 固定回复20点生命值
                self.player.health = min(self.player.health + heal_amount, self.player.max_health)
                self.player.stamina -= 5  # 消耗5点耐力
                self.player.rest_count_today += 1  # 增加休息计数
                message = f"恢复了{heal_amount}生命，消耗5耐力 / Restored {heal_amount} HP, consumed 5 Stamina"
                self.show_message(message)
                self.update_stats()
                
                # 不再自动返回，而是显示返回按钮
                self.current_event = "short_rest_result"
                self.clear_buttons()
                self.set_button(2, "返回主界面\nBack to Main", tk.NORMAL)
            else:
                message = "耐力不足! / Not enough Stamina!"
                self.show_message(message)
                self.root.after(2000, self.show_rest_options)
        
        elif choice == 1:  # 露营休息
            # 第十天不允许露营休息
            if self.player.day >= 10:
                message = "第十天无法露营休息，必须面对最终战斗! / Cannot camp on Day 10, must face the final battle!"
                self.show_message(message)
                self.root.after(2000, self.show_rest_options)
                return
                
            # 检查是否满足"懒惰之人"标签条件：耐力值为100时直接扎营休息
            if self.player.stamina == self.player.max_stamina:
                self.player.add_tag("懒惰之人 / Lazy")
            
            # 显示恢复信息，等待用户点击继续
            message = f"进入第{self.player.day+1}天! 生命和耐力完全恢复! / Entering Day {self.player.day+1}! HP and Stamina fully restored!"
            self.show_message(message)
            
            self.current_event = "camp_rest_result"
            self.clear_buttons()
            self.set_button(2, "继续游戏\nContinue", tk.NORMAL)
        
        elif choice == 4:  # 返回 (使用第5个按钮)
            self.show_main_menu()
    
    def handle_short_rest_result(self, choice):
        """处理短暂休息结果的按钮点击"""
        if choice == 2:  # 返回主界面按钮
            self.show_main_menu()
    
    def handle_camp_rest_result(self, choice):
        """处理露营休息结果的按钮点击"""
        if choice == 2:  # 继续游戏按钮
            self.next_day()
    
    def next_day(self):
        """进入下一天，增加基础攻击力"""
        # 检查是否满足"懒惰之人"标签条件：花费全部一天的时间用来休息
        if self.player.rest_count_today >= 3 and not self.player.has_explored_today:
            self.player.add_tag("懒惰之人 / Lazy")
        
        self.player.day += 1
        self.player.base_attack += 5  # 每天增加5点基础攻击力
        self.player.update_attack()   # 更新总攻击力
        self.player.health = self.player.max_health
        self.player.stamina = self.player.max_stamina
        # 每天增加2点防御力
        self.player.defense += 2
        
        # 重置每日计数
        self.player.rest_count_today = 0
        self.player.has_explored_today = False
        
        self.player.save_day_start()
        
        # 直接显示主菜单，不再显示每日消息页面
        self.show_main_menu()
    
    def show_defeat_screen(self):
        """显示失败屏幕 - 修改为第十天也可以重新开始"""
        message = "💀 不幸的是，你永远迷失在这片丛林中... 💀\n\n"
        message += "💀 Unfortunately, you are lost forever in this jungle... 💀"
        
        self.show_message(message)
        
        self.current_event = "defeat"
        self.clear_buttons()
        # 移除对第10天的限制，任何一天都可以重新开始
        self.set_button(0, "1. 重新开始今天 🔄\nRestart Day", tk.NORMAL)
        self.set_button(1, "2. 重新开始游戏 🎮\nRestart Game", tk.NORMAL)
        self.set_button(2, "3. 退出游戏 🚪\nExit Game", tk.NORMAL)
    
    def handle_defeat(self, choice):
        """处理失败选项 - 修改为第十天也可以重新开始"""
        print(f"Handling defeat choice: {choice}")  # 调试信息
        
        if choice == 0:  # 重新开始今天 - 移除对第10天的限制
            self.player.restore_day_start()
            self.game_over = False
            self.current_event = "main"
            message = "重新开始今天... / Restarting the day..."
            self.show_message(message)
            self.update_stats()
            # 直接显示主菜单，不再使用延迟
            self.show_main_menu()
        elif choice == 1:  # 重新开始游戏
            # 完全重新初始化游戏
            self.player = Player()
            self.battle_system = BattleSystem()
            self.event_system = EventSystem()
            self.game_over = False
            self.current_event = None
            self.current_monster = None
            self.current_shop = None
            self.current_merchant = None
            
            # 清除并重新设置界面
            for widget in self.root.winfo_children():
                widget.destroy()
            self.setup_gui()
            self.start_game()
        elif choice == 2:  # 退出游戏
            self.root.quit()
    
    def update_tags(self):
        """更新玩家标签"""
        if self.player.escapes_attempted >= 10 and "懦夫 / Coward" not in self.player.tags:
            self.player.add_tag("懦夫 / Coward")
        
        if self.player.gold >= 50 and "守财奴 / Miser" not in self.player.tags:
            self.player.add_tag("守财奴 / Miser")
        
        # 修改称号条件：使用3次药水即可获得称号
        if self.player.items_bought["attack"] >= 3 and "狂战士 / Berserker" not in self.player.tags:
            self.player.add_tag("狂战士 / Berserker")
        
        if self.player.items_bought["stamina"] >= 3 and "坦克 / Tank" not in self.player.tags:
            self.player.add_tag("坦克 / Tank")
        
        if self.player.items_bought["mystery"] >= 3 and "神秘学者 / Mystic" not in self.player.tags:
            self.player.add_tag("神秘学者 / Mystic")
        
        # 添加对健康药水和防御药水的检查
        if self.player.items_bought["health"] >= 3 and "生命守护者 / Life Guardian" not in self.player.tags:
            self.player.add_tag("生命守护者 / Life Guardian")
        
        if self.player.items_bought["defense"] >= 3 and "铁壁 / Iron Wall" not in self.player.tags:
            self.player.add_tag("铁壁 / Iron Wall")
    
    def run(self):
        """运行游戏"""
        self.root.mainloop()

# 运行游戏
if __name__ == "__main__":
    game = DarkForestGUI()
    game.run()