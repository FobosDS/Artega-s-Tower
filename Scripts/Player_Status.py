from Settings import *

class Base_Stats:
    def __init__(self):
        self.hp = base_hp
        self.sp = base_sp + sp_bonus
        self.gold = base_gold
        self.potions = base_potions
        self.scrolls = base_scrolls

        self.hp_level = base_hp_level
        self.sp_level = base_sp_level

        self.max_hp = base_hp * self.hp_level
        self.max_sp = base_sp + self.sp_level * sp_bonus
        self.max_potions = base_potions * self.hp_level
        self.amount = self.max_hp * potion_heal_percent

        self.sp_regen = base_sp_regen + self.sp_level * sp_regen_bonus
        self.sp_regen_delay = base_sp_regen_delay - self.sp_level * sp_regen_delay_bonus
        self.sp_regen_timer = 0


    def heal(self, amount):
        self.hp = min(self.hp + amount, self.max_hp)

    def take_damage(self, damage):
        self.hp = max(self.hp - damage, 0)

    def add_gold(self, count):
        self.gold = min(self.gold + count, max_gold)

    def is_dead(self):
        return self.hp <= 0

    def level_up_hp(self):
        if self.hp_level >= max_hp_level:
            return False
        self.hp_level += 1
        self.max_hp = base_hp * self.hp_level
        self.max_potions = base_potions * self.hp_level
        self.amount = self.max_hp * potion_heal_percent
        self.hp = self.max_hp
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


class Combat_Stats:
    def __init__(self):
        self.weapon_level = base_weapon_level
        self.durability = base_durability
        self.whetstones = base_whetstones
        self.default_attack_damage = base_attack_damage * self.weapon_level
        self.attack_damage = self.default_attack_damage

        self.is_enchanted = False
        self.enchantment_time_left = 0

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


    def apply_enchantment(self, duration):
        if not self.is_enchanted:
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

    def apply_poison(self):
        self.is_poisoned = True
        self.poison_time_left = poison_duration
        self.poison_tick_timer = poison_interval

    def apply_paralysis(self):
        self.is_paralyzed = True
        self.paralysis_time_left = paralysis_duration

    def update(self, dt, base_stats):
        # poison
        if self.is_poisoned:
            self.poison_time_left -= dt
            self.poison_tick_timer -= dt
            if self.poison_tick_timer <= 0:
                damage = int(base_stats.max_hp * poison_damage_percent)
                base_stats.take_damage(damage)
                self.poison_tick_timer = poison_interval
            if self.poison_time_left <= 0:
                self.is_poisoned = False
                self.poison_time_left = 0
                self.poison_tick_timer = 0

        # paralysis
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

        self.is_floor_key = False
        self.is_chest_key1 = False
        self.is_chest_key2 = False

        self.current_floor = 2

    def use_potion(self):
        if self.base.potions > 0:
            if not self.effects.is_poisoned and not self.effects.is_paralyzed:
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
            self.combat.apply_enchantment(enchantment_duration)
            self.base.scrolls = max(self.base.scrolls - 1, 0)
            return True
        return False

    def update_effects(self, dt):
        self.effects.update(dt, self.base)
        self.combat.update_enchantment(dt)
        self.base.regen_sp(dt)