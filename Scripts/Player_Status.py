from Settings import *
from Sprites_Archive import RD
import Items_Hub


class Base_Stats:
    def __init__(self):
        self.hp = base_hp
        self.sp = base_sp + sp_bonus
        self.gold = base_gold
        self.potions = base_potions
        self.scrolls = base_scrolls
        self.dark_shards = base_dark_shards

        self.hp_level = base_hp_level
        self.sp_level = base_sp_level

        self.max_hp = base_hp * self.hp_level
        self.max_sp = base_sp + self.sp_level * sp_bonus
        self.max_potions = base_potions + self.hp_level
        self.amount = self.max_hp * potion_heal_percent

        self.sp_regen = base_sp_regen + self.sp_level * sp_regen_bonus
        self.sp_regen_delay = base_sp_regen_delay - self.sp_level * sp_regen_delay_bonus
        self.sp_regen_timer = 0

        self.rings = []
        self.max_rings = 2

        self.combat_ref = None
        self.owner = None

    def heal(self, amount):
        self.hp = min(self.hp + amount, self.max_hp)

    def take_damage(self, damage):
        ess = getattr(self, "essences", None)                
        if ess is not None and ess.try_darkness_save(self, damage):  
            self.hp = 1
            return
        self.hp = max(self.hp - damage, 0)

    def add_potion(self, count):
        self.potions = min(self.potions + count, self.max_potions)

    def add_scroll(self, count):
        self.scrolls = min(self.scrolls + count, max_scrolls)

    def add_gold(self, count):
        self.gold = min(self.gold + count, max_gold)

    def add_ring(self, ring_type):
        if ring_type in self.rings:
            return None
        displaced = None
        if len(self.rings) >= self.max_rings:
            displaced = self.rings.pop(0)
            self.on_ring_removed(displaced)
        self.rings.append(ring_type)
        self.on_ring_added(ring_type)
        return displaced  

    def add_dark_shard(self, count=1):
        self.dark_shards = min(self.dark_shards + count, max_dark_shards)
        return self.dark_shards

    def is_dead(self):
        return self.hp <= 0

    def level_up_hp(self):
        if self.hp_level >= max_hp_level:
            return False
        self.hp_level += 1
        self.max_hp = base_hp * self.hp_level
        self.max_potions = base_potions + self.hp_level
        self.amount = self.max_hp * potion_heal_percent
        self.hp = self.max_hp
        self.recalc_limits()
        return True

    def has_sp(self, amount):
        return self.sp >= amount

    def use_sp(self, amount):
        if self.sp >= amount:
            self.sp -= amount
            self.sp_regen_timer = self.sp_regen_delay
            return True
        return False

    def regen_sp(self, dt):
        if self.sp_regen_timer > 0:
            self.sp_regen_timer -= dt
        else:
            self.sp = min(self.sp + self.sp_regen * dt, self.max_sp)

    def add_sp(self, amount):
        self.sp = min(self.sp + amount, self.max_sp)

    def level_up_sp(self):
        if self.sp_level >= max_sp_level:
            return False
        self.sp_level += 1
        self.max_sp = base_sp + self.sp_level * sp_bonus
        self.sp = self.max_sp
        self.sp_regen = base_sp_regen + self.sp_level * sp_regen_bonus
        self.sp_regen_delay = base_sp_regen_delay - self.sp_level * sp_regen_delay_bonus
        return True

    def recalc_limits(self):
        bonus_hp = 0
        for r in self.rings:
            eff = Items_Hub.ring_effects.get(r, {})
            if eff.get("type") == "hp_fullheal":
                bonus_hp += eff.get("hp_levels", 0)
            if eff.get("type") == "flat_levels":
                bonus_hp += eff.get("hp", 0)
        self.max_hp = base_hp * (self.hp_level + bonus_hp)
        self.max_potions = base_potions + (self.hp_level + bonus_hp)
        self.amount = self.max_hp * potion_heal_percent
        self.hp = min(self.hp, self.max_hp)

    def on_ring_added(self, ring_type):
        eff = Items_Hub.ring_effects.get(ring_type, {})
        if eff.get("type") == "flat_levels":
            for _ in range(eff.get("weapon", 0)):
                self._force_level_up_weapon()
            for _ in range(eff.get("sp", 0)):
                self._force_level_up_sp()
        self.recalc_limits()

    def on_ring_removed(self, ring_type):
        eff = Items_Hub.ring_effects.get(ring_type, {})
        if eff.get("type") == "flat_levels":
            for _ in range(eff.get("weapon", 0)):
                self._force_level_down_weapon()
            for _ in range(eff.get("sp", 0)):
                self._force_level_down_sp()
        self.recalc_limits()

    def _force_level_up_weapon(self):
        if self.combat_ref is not None:
            self.combat_ref.level_up_weapon()

    def _force_level_down_weapon(self):
        if self.combat_ref is not None and self.combat_ref.weapon_level > base_weapon_level:
            self.combat_ref.weapon_level -= 1
            self.combat_ref.default_attack_damage = base_attack_damage * self.combat_ref.weapon_level
            if self.combat_ref.is_enchanted:
                self.combat_ref.attack_damage = int(self.combat_ref.default_attack_damage * enchantment_multiplier)
            else:
                self.combat_ref.attack_damage = self.combat_ref.default_attack_damage

    def _force_level_up_sp(self):
        if self.sp_level < max_sp_level:
            self.level_up_sp()

    def _force_level_down_sp(self):
        if self.sp_level > base_sp_level:
            self.sp_level -= 1
            self.max_sp = base_sp + self.sp_level * sp_bonus
            self.sp = min(self.sp, self.max_sp)
            self.sp_regen = base_sp_regen + self.sp_level * sp_regen_bonus
            self.sp_regen_delay = base_sp_regen_delay - self.sp_level * sp_regen_delay_bonus


class Combat_Stats:
    def __init__(self):
        self.weapon_level = base_weapon_level
        self.durability = base_durability
        self.whetstones = base_whetstones
        self.default_attack_damage = base_attack_damage * self.weapon_level
        self.attack_damage = self.default_attack_damage

        self.is_enchanted = False
        self.enchantment_time_left = 0

        self.magic_shots_loaded = 0        
        self.magic_shots_damage = 0        
        self.magic_shot_timer = 0

    def get_attack_damage(self):
        factor = self.durability / max_durability
        if factor > 0.94:
            factor = 1
        if factor < 0.1:
            factor = 0.1
        return int(self.attack_damage * factor)

    def use_weapon(self):
        damage = self.get_attack_damage()
        self.durability = max(self.durability - durability_loss, 0)
        return damage

    def repair_weapon(self):
        self.durability = max_durability

    def use_whetstone(self):
        if self.whetstones > 0:
            self.repair_weapon()
            self.whetstones = max(self.whetstones - 1, 0)
            return True
        return False

    def add_whetstone(self, count):
        self.whetstones = min(self.whetstones + count, max_whetstones)

    def apply_enchantment(self, duration):
        if not self.is_enchanted:
            self.is_enchanted = True
            self.enchantment_time_left = duration
            self.attack_damage = int(self.default_attack_damage * enchantment_multiplier)

    def force_apply_enchantment(self, duration):
        self.is_enchanted = True
        self.enchantment_time_left = duration
        self.attack_damage = int(self.default_attack_damage * enchantment_multiplier)

    def level_up_weapon(self):
        if self.weapon_level >= max_weapon_level:
            return False
        self.weapon_level += 1
        self.default_attack_damage = base_attack_damage * self.weapon_level
        if self.is_enchanted:
            self.attack_damage = int(self.default_attack_damage * enchantment_multiplier)
        else:
            self.attack_damage = self.default_attack_damage
        return True

    def update_enchantment(self, dt):
        if self.is_enchanted:
            self.enchantment_time_left -= dt
            if self.enchantment_time_left <= 0:
                self.is_enchanted = False
                self.enchantment_time_left = 0
                self.attack_damage = self.default_attack_damage


class Effects:
    def __init__(self):
        self.is_poisoned = False
        self.poison_time_left = 0
        self.poison_tick_timer = 0

        self.is_paralyzed = False
        self.paralysis_time_left = 0

    def try_apply_poison(self, stats):
        if self._status_shield_block(stats):
            return False
        self.apply_poison(stats)                             
        return True

    def try_apply_paralysis(self, stats):
        if self._status_shield_block(stats):
            return False
        self.apply_paralysis(stats)                          
        return True

    def _ghoul_mult(self, stats):                            
        ess = getattr(stats, "essences", None) if stats is not None else None
        return 0.5 if (ess is not None and ess.has("ghoul")) else 1.0

    def _status_shield_block(self, stats):
        if not any(Items_Hub.ring_effects.get(r, {}).get("type") == "status_shield" for r in stats.base.rings):
            return False
        if stats.ring_shield_cd > 0:
            return False
        stats.ring_shield_cd = Items_Hub.ring_effects["ring_dragon"]["recharge"]
        return True

    def apply_poison(self, stats=None):                      
        mult = self._ghoul_mult(stats)
        self.is_poisoned = True
        self.poison_time_left = poison_duration * mult
        self.poison_tick_timer = poison_interval

    def apply_paralysis(self, stats=None):                  
        mult = self._ghoul_mult(stats)
        self.is_paralyzed = True
        self.paralysis_time_left = paralysis_duration * mult

    def update(self, dt, stats):                             
        base_stats = stats.base
        ess = getattr(stats, "essences", None)
        ghoul = ess is not None and ess.has("ghoul")
        if self.is_poisoned:
            self.poison_time_left -= dt
            self.poison_tick_timer -= dt
            if self.poison_tick_timer <= 0:
                damage = int(base_stats.max_hp * poison_damage_percent * (0.5 if ghoul else 1.0))
                base_stats.take_damage(damage)
                self.poison_tick_timer = poison_interval
            if self.poison_time_left <= 0:
                self.is_poisoned = False
                self.poison_time_left = 0
                self.poison_tick_timer = 0

        if self.is_paralyzed:
            self.paralysis_time_left -= dt
            if self.paralysis_time_left <= 0:
                self.is_paralyzed = False
                self.paralysis_time_left = 0


class Player_Stats:
    def __init__(self):
        self.base = Base_Stats()
        self.combat = Combat_Stats()
        self.effects = Effects()

        self.base.combat_ref = self.combat
        self.base.owner = self

        self.is_floor_key = False
        self.is_chest_key1 = False
        self.is_chest_key2 = False

        self.current_floor = 1

        self.pending_messages = []

        self.ring_shield_cd = 0.0
        self.berserk_time_left = 0.0
        self.berserk_cooldown_left = 0.0
        self.berserk_weapon_gain = 0

        self.last_displaced_ring = None

        self.request_save = False
        self.request_next_floor = False
        self.killed_in_room = {}

        self.pending_messages = []
        self.essences = None   
        self.base.essences = None  

    def get_speed_multiplier(self):
        mult = 1.0
        for r in self.base.rings:
            eff = Items_Hub.ring_effects.get(r, {})
            if eff.get("type") in ("speed_sp", "speed_range"):
                mult *= eff.get("speed", 1.0)
        if self.berserk_time_left > 0:
            mult *= Items_Hub.ring_effects["ring_murderer"]["speed"]
        return mult

    def get_sp_cost_multiplier(self):
        for r in self.base.rings:
            eff = Items_Hub.ring_effects.get(r, {})
            if eff.get("type") == "speed_sp":
                return eff.get("sp", 1.0)
        return 1.0

    def get_price_multiplier(self):
        for r in self.base.rings:
            eff = Items_Hub.ring_effects.get(r, {})
            if eff.get("type") == "trade_loot":
                return eff.get("price", 1.0)
        return 1.0

    def get_loot_bonus(self):
        for r in self.base.rings:
            eff = Items_Hub.ring_effects.get(r, {})
            if eff.get("type") == "trade_loot":
                return eff.get("loot", 1.0)
        return 1.0

    def get_effect_duration_multiplier(self):
        mult = 1.0
        for r in self.base.rings:
            eff = Items_Hub.ring_effects.get(r, {})
            if eff.get("type") == "duration_x":
                mult *= eff.get("mult", 1.0)
        return mult

    def get_attack_range_multiplier(self):
        mult = 1.0
        for r in self.base.rings:
            eff = Items_Hub.ring_effects.get(r, {})
            if eff.get("type") == "speed_range":
                mult *= eff.get("range", 1.0)
        return mult

    def get_attack_speed_multiplier(self):
        if self.berserk_time_left > 0:
            return Items_Hub.ring_effects["ring_murderer"]["attack_speed"]
        return 1.0

    def _try_activate_berserk(self):
        if "ring_murderer" not in self.base.rings:
            return False
        if self.berserk_cooldown_left > 0 or self.berserk_time_left > 0:
            return False
        eff = Items_Hub.ring_effects["ring_murderer"]
        if self.base.hp < self.base.max_hp * 0.9:
            return False

        self.base.take_damage(int(self.base.max_hp * 0.9))
        self.berserk_time_left = eff["duration"]
        self.berserk_cooldown_left = eff["cooldown"]

        self.combat.force_apply_enchantment(eff["duration"] * self.get_effect_duration_multiplier())

        self.berserk_weapon_gain = 0
        for _ in range(eff["weapon_levels"]):
            if self.combat.level_up_weapon():
                self.berserk_weapon_gain += 1

        self.notify("Оскар впал в кровавую ярость!")
        return True

    def _end_berserk(self):
        for _ in range(self.berserk_weapon_gain):
            if self.combat.weapon_level > base_weapon_level:
                self.combat.weapon_level -= 1
                self.combat.default_attack_damage = base_attack_damage * self.combat.weapon_level
                if self.combat.is_enchanted:
                    self.combat.attack_damage = int(self.combat.default_attack_damage * enchantment_multiplier)
                else:
                    self.combat.attack_damage = self.combat.default_attack_damage
        self.berserk_weapon_gain = 0

    def use_potion(self):
        if self.base.potions > 0:
            if not self.effects.is_poisoned and not self.effects.is_paralyzed:
                if any(Items_Hub.ring_effects.get(r, {}).get("type") == "hp_fullheal" for r in self.base.rings):
                    self.base.hp = self.base.max_hp
                else:
                    self.base.heal(self.base.amount)
            else:
                if self.effects.is_poisoned:
                    self.effects.is_poisoned = False
                    self.effects.poison_time_left = 0
                    self.effects.poison_tick_timer = 0
                if self.effects.is_paralyzed:
                    self.effects.is_paralyzed = False
                    self.effects.paralysis_time_left = 0
            self.base.potions = max(self.base.potions - 1, 0)
            return True
        return False

    def use_scroll(self):
        if self.base.scrolls > 0 and not self.combat.is_enchanted:
            dur = enchantment_duration * self.get_effect_duration_multiplier()
            self.combat.apply_enchantment(dur)
            self.base.scrolls = max(self.base.scrolls - 1, 0)
            return True
        return False

    def update_effects(self, dt):
        self.effects.update(dt, self)
        self.combat.update_enchantment(dt)
        self.base.regen_sp(dt)
        if self.ring_shield_cd > 0:
            self.ring_shield_cd = max(0.0, self.ring_shield_cd - dt)
        if self.berserk_cooldown_left > 0:
            self.berserk_cooldown_left = max(0.0, self.berserk_cooldown_left - dt)
        if self.berserk_time_left > 0:
            self.berserk_time_left = max(0.0, self.berserk_time_left - dt)
            if self.berserk_time_left <= 0:
                self._end_berserk()

    def notify(self, msg):
        if msg:
            self.pending_messages.append(msg)

    def give_item(self, item, amount=1, give_ring=None):
        if item is None:
            return ""
        if item == "potion":
            self.base.add_potion(amount)
            return "Зелье жизни"
        if item == "scroll":
            self.base.add_scroll(amount)
            return "Свиток тьмы"
        if item == "whetstone":
            self.combat.add_whetstone(amount)
            return "Точильный камень"
        if item == "gold":
            return ""
        if item == "dark_shard":
            if self.base.add_dark_shard(amount) >= max_dark_shards:
                return "Осколок тьмы (макс.)"
            return "Осколок тьмы"
        if item == "heart":
            if self.base.level_up_hp():
                return "Сердце монстра. Оскар сожрал его и стал крепче!"
            return ""
        if item == "lungs":
            if self.base.level_up_sp():
                return "Легкие вампира. Оскар сожрал их и стал выносливее!"
            return ""
        if item == "weapon_crate":
            if self.combat.level_up_weapon():
                return "Оружейный ящик Андре. Инструменты помогли Оскару улучшить свое оружие!"
            return ""
        if item == "chest_key_base":
            if not self.is_chest_key1:
                self.is_chest_key1 = True
                return "Ключ от сундука"
            return ""
        if item == "chest_key_rare":
            if not self.is_chest_key2:
                self.is_chest_key2 = True
                return "Ключ от тайника Артеги"
            return ""
        if item == "floor_key":
            if not self.is_floor_key:
                self.is_floor_key = True
                return "Ключ от этажа"
            return ""
        if item == "ring":
            return self.give_ring(give_ring)
        return "Кольцо"
    
    def give_ring(self, give_ring):
        chosen = None
        for r in Items_Hub.get_floor_rings(self.current_floor):
            if r not in self.base.rings:
                chosen = r
                break
        if chosen is None:
            available = [r for r in RD.keys() if r not in self.base.rings]
            if not available:
                return ""
            chosen = available[0]
        if give_ring is not None:
            self.last_displaced_ring = give_ring(chosen)
        else:
            self.last_displaced_ring = self.base.add_ring(chosen)
        return f"{RD[chosen]['name']}"