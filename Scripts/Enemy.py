import math
from Settings import *
from Objects import Sprite
from Map import drawed_map
from random import randint
from Sprites_Archive import WTD
import Items_Hub

class Enemy(Sprite):
    def __init__(self, x, y, image_path, scale=1.0, collision_radius=14):
        super().__init__(x, y, image_path, scale, collision_radius)

        self.hp = 30
        self.max_hp = self.hp
        self.gold_drop = (1, 2)
        self.is_dead = False
        self.radius = collision_radius
        self.speed = 10
        
        self.player = None 

        self.enemy_type = "ghoul"
        self.has_dropped = False

        self.room_id = None
        self.barrier_id = None

    def update(self, dt, player, all_enemies):
        pass

    def is_wall(self, x, y):
        col = int(x // tile_size)
        row = int(y // tile_size)
        
        if row < 0 or row >= len(drawed_map) or col < 0 or col >= len(drawed_map[0]):
            return True
        return drawed_map[row][col] in WTD

    def move_towards(self, target_x, target_y, speed, dt, all_enemies):
        dx = target_x - self.x
        dy = target_y - self.y
        dist = math.hypot(dx, dy)
        
        min_dist = self.radius + 15
        if dist < min_dist:
            return

        move_x = (dx / dist) * speed * dt
        move_y = (dy / dist) * speed * dt

        new_x = self.x + move_x
        if not self.is_wall(new_x, self.y) and not self.collides_with_enemies(new_x, self.y, all_enemies):
            self.x = new_x
            self.rect.center = (self.x, self.y)

        new_y = self.y + move_y
        if not self.is_wall(self.x, new_y) and not self.collides_with_enemies(self.x, new_y, all_enemies):
            self.y = new_y
            self.rect.center = (self.x, self.y)

    def collides_with_enemies(self, x, y, all_enemies):
        for other in all_enemies:
            if other is self or other.is_dead:
                continue
            dist = math.hypot(other.x - x, other.y - y)
            if dist < (self.radius + other.radius) * 0.8:
                return True
        return False

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.hp = 0
            self.is_dead = True
    
    def drop_loot(self):
        if self.has_dropped:
            return
        if self.player is None:
            return
        self.has_dropped = True

        amount = randint(*self.gold_drop)
        self.player.stats.base.add_gold(amount)

        item = Items_Hub.roll_enemy_loot(self.enemy_type, self.player.stats.get_loot_bonus())
        if item is not None:
            self.player.stats.give_item(item)
            self.player.stats.notify(Items_Hub.colored_pickup("Оскар подобрал: ", item))

        if self.room_id is not None and self.player is not None:
            self.player.stats.killed_in_room[self.room_id] = \
                self.player.stats.killed_in_room.get(self.room_id, 0) + 1