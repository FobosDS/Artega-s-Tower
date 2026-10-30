import math
from Settings import *
from Objects import Sprite
from Map import drawed_map
from random import randint

class Enemy(Sprite):
    def __init__(self, x, y, image_path, scale=1.0, collision_radius=12):
        super().__init__(x, y, image_path, scale, collision_radius)
        
        self.hp = 30
        self.max_hp = 30
        self.is_dead = False
        self.radius = collision_radius
        self.speed = 30
        
        self.player = None 

    def update(self, dt, player, all_enemies):
        pass

    def is_wall(self, x, y):
        col = int(x // tile_size)
        row = int(y // tile_size)
        
        if row < 0 or row >= len(drawed_map) or col < 0 or col >= len(drawed_map[0]):
            return True
        return drawed_map[row][col] == "H"

    def move_towards(self, target_x, target_y, speed, dt, all_enemies):
        dx = target_x - self.x
        dy = target_y - self.y
        dist = math.hypot(dx, dy)
        
        if dist < 1:
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

    def drop_gold(self, diap, count=0):
        count =randint(*diap)
        self.player.stats.base.add_gold(count)