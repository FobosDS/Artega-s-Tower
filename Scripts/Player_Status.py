from Settings import *

class Player_Stats():
    def __init__(self):
        #current stats
        self.hp = base_hp
        self.sp = base_sp
        self.durability = base_durability
        self.potions = base_potions
        self.gold = base_gold
        self.scrolls = base_scrolls
        self.weapon_level = 1
        self.hp_level = 1
        self.sp_level = 1

        self.max_hp = base_hp * self.hp_level
        self.max_sp = base_sp * self.sp_level
        self.max_potions = base_potions * self.hp_level
        self.amount = self.max_hp * potion_heal_percent
        self.attack_damage = base_attack_damage * self.weapon_level
        self.default_attack_damage = base_attack_damage * self.weapon_level

        #keys
        self.is_dungeon_key = False
        self.is_mausoleum_key = False
        self.is_archive_key = False
        self.is_hall_key = False
        self.is_chest_key1 = False
        self.is_chest_key2 = False

        #effects
        #poison
        self.is_poisoned = False

        self.poison_time_left = 0
        self.poison_tick_timer = 0
        
        #paralich
        self.is_paraliched = False
        self.paralich_time_left = 0

        #enchantment
        self.is_enchanted = False
        self.enchantment_time_left = 0

    def heal(self, amount):
        self.hp = min(self.hp + amount, self.max_hp)

    def use_potion(self):
        if self.potions > 0:
            self.heal(self.amount)
            self.potions = max(self.potions - 1, 0)

    def use_scroll(self):
        if self.scrolls > 0 and not self.is_enchanted:
            self.apply_enchantment()
            self.scrolls = max(self.scrolls - 1, 0)
            return True
        return False

    def level_up(self, stat):

        #pick up crimson heart
        if stat == "hp":
            if self.hp_level >= max_hp_level:
                return False
            self.hp_level += 1
            self.max_hp = base_hp * self.hp_level
            self.max_potions = base_potions * self.hp_level
            self.amount = self.max_hp * potion_heal_percent
            self.hp = self.max_hp
            return True
        
        #pick up vampire's lungs
        if stat == "sp":
            if self.sp_level >= max_sp_level:
                return False
            self.sp_level += 1
            self.max_sp = base_sp * self.sp_level
            self.sp = self.max_sp
            return True

        #pick up Andre's blacksmith's box
        if stat == "weapon":
            if self.weapon_level >= max_weapon_level:
                return False
            self.weapon_level += 1
            self.default_attack_damage = base_attack_damage * self.weapon_level
            if self.is_enchanted:
                self.attack_damage = int(self.default_attack_damage * enchantment_multiplier)
            else:
                self.attack_damage = self.default_attack_damage
            return True

        return False

    #weapon + repair
    def get_attack_damage(self):
        if self.durability <= 0:
            return 0
        durability_factor = max(0.1, self.durability / self.max_durability)
        return int(self.attack_damage * durability_factor)

    def use_weapon(self):
        damage = self.get_attack_damage()
        self.durability = max(self.durability - durability_loss, 0)
        return damage

    def repair_weapon(self, amount):
        self.durability = min(self.durability + amount, self.max_durability)
    
    def take_damage(self, damage):
        self.hp = max(self.hp - damage, 0)

    def is_dead(self):
        return self.hp <= 0 

    #effects functions
    def apply_poison(self):
        self.is_poisoned = True
        self.poison_time_left = poison_duration
        self.poison_tick_timer = poison_interval

    def apply_paralich(self):
        self.is_paraliched = True
        self.paralich_time_left = paralich_duration

    def apply_enchantment(self):
        if not self.is_enchanted:
            self.is_enchanted = True
            self.enchantment_time_left = enchantment_duration
            self.attack_damage = int(self.default_attack_damage * enchantment_multiplier)

    def update_effects(self, dt):
        #poison
        if self.is_poisoned:
            self.poison_time_left -= dt
            self.poison_tick_timer -= dt

            if self.poison_tick_timer <= 0:
                damage = int(self.max_hp * poison_damage_percent)
                self.take_damage(damage)
                self.poison_tick_timer = poison_interval

            if self.poison_time_left <= 0:
                self.is_poisoned = False
                self.poison_time_left = 0
                self.poison_tick_timer = 0

        #paralich
        if self.is_paraliched:
            self.paralich_time_left -= dt
            if self.paralich_time_left <= 0:
                self.is_paraliched = False
                self.paralich_time_left = 0

        #enchantment
        if self.is_enchanted:
            self.enchantment_time_left -= dt
            if self.enchantment_time_left <= 0:
                self.is_enchanted = False
                self.enchantment_time_left = 0
                self.attack_damage = self.default_attack_damage

