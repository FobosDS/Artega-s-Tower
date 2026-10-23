from Settings import *

class Base_Stats:
    def __init__(self):
        self.hp = base_hp
        self.sp = base_sp
        self.gold = base_gold
        self.potions = base_potions
        self.scrolls = base_scrolls

        self.hp_level = 1
        self.sp_level = 1

        self.max_hp = base_hp * self.hp_level
        self.max_sp = base_sp * self.sp_level
        self.max_potions = base_potions * self.hp_level
        self.amount = self.max_hp * potion_heal_percent

    def heal(self, amount):
        if self.is_dead():
            return
        self.hp = min(self.hp + amount, self.max_hp)

    def take_damage(self, damage):
        self.hp = max(self.hp - damage, 0)

    def is_dead(self):
        return self.hp <= 0

    def use_potion(self):
        if self.potions > 0:
            self.heal(self.amount)
            self.potions = max(self.potions - 1, 0)
            return True
        return False

    def level_up_hp(self):
        if self.hp_level >= max_hp_level:
            return False
        self.hp_level += 1
        self.max_hp = base_hp * self.hp_level
        self.max_potions = base_potions * self.hp_level
        self.amount = self.max_hp * potion_heal_percent
        self.hp = self.max_hp
        return True

    def level_up_sp(self):
        if self.sp_level >= max_sp_level:
            return False
        self.sp_level += 1
        self.max_sp = base_sp * self.sp_level
        self.sp = self.max_sp
        return True


class Combat_Stats:
    def __init__(self):
        self.weapon_level = 1
        self.durability = base_durability
        self.default_attack_damage = base_attack_damage * self.weapon_level
        self.attack_damage = self.default_attack_damage

        self.is_enchanted = False
        self.enchantment_time_left = 0

    def get_attack_damage(self):
        if self.durability <= 0:
            return 0
        factor = self.durability / base_durability
        return int(self.attack_damage * factor)

    def use_weapon(self):
        damage = self.get_attack_damage()
        self.durability = max(self.durability - durability_loss, 0)
        return damage

    def repair_weapon(self, amount):
        self.durability = min(self.durability + amount, base_durability)

    def apply_enchantment(self):
        if not self.is_enchanted:
            self.is_enchanted = True
            self.enchantment_time_left = enchantment_duration
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

        self.is_dungeon_key = False
        self.is_mausoleum_key = False
        self.is_archive_key = False
        self.is_hall_key = False
        self.is_chest_key1 = False
        self.is_chest_key2 = False

    def use_scroll(self):
        if self.base.scrolls > 0 and not self.combat.is_enchanted:
            self.combat.apply_enchantment()
            self.base.scrolls = max(self.base.scrolls - 1, 0)
            return True
        return False

    def update_effects(self, dt):
        self.effects.update(dt, self.base)
        self.combat.update_enchantment(dt)