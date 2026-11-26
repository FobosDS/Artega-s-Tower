import math
from Settings import *
from Objects import Sprite
from Map import drawed_map
from Sprites_Archive import WTD

class Projectile(Sprite):
    def __init__(self, x, y, target_x, target_y, image_path, speed=200):
        super().__init__(x, y, image_path, scale=1.0, collision_radius=10)
        self.speed = speed
        self.effect = None
        
        dx = target_x - x
        dy = target_y - y
        dist = math.hypot(dx, dy)
        if dist > 0:
            self.dir_x = dx / dist
            self.dir_y = dy / dist
        else:
            self.dir_x = 1
            self.dir_y = 0

    def update(self, dt, player=None):
        self.x += self.dir_x * self.speed * dt
        self.y += self.dir_y * self.speed * dt
        self.rect.center = (self.x, self.y)


class ProjectileManager:
    def __init__(self):
        self.projectiles = []

    def add_projectile(self, projectile):
        self.projectiles.append(projectile)

    def update(self, dt, player, weapon):
        for proj in self.projectiles[:]:
            proj.update(dt, player)
            
            col = int(proj.x // tile_size)
            row = int(proj.y // tile_size)
            
            if (row < 0 or row >= len(drawed_map) or 
                col < 0 or col >= len(drawed_map[0]) or 
                drawed_map[row][col] in WTD):
                self.projectiles.remove(proj)
                continue
            
            if proj.rect.colliderect(player.rect):
                if weapon.try_absorb_projectile(proj, player.x, player.y, player.angle):
                    self.projectiles.remove(proj)
                else:
                    if proj.effect == "poison":
                        player.stats.effects.try_apply_poison(player.stats)
                    elif proj.effect == "paralysis":
                        player.stats.effects.try_apply_paralysis(player.stats)
                    elif proj.effect == "blood":
                        player.stats.effects.try_apply_poison(player.stats)
                        player.stats.effects.try_apply_paralysis(player.stats)
                    elif proj.effect == "death":
                        player.stats.base.take_damage(99999)
                    
                    player.stats.base.take_damage(5)
                    self.projectiles.remove(proj)

    def draw(self, screen, player, z_buffer, render_sprites_func):
        render_sprites_func(player, screen, self.projectiles)

class Magic_Shard_Projectile(Sprite):                       
    def __init__(self, x, y, angle, damage):
        super().__init__(x, y, magic_projectile_image,
                         scale=magic_projectile_scale, collision_radius=0)
        self.dir_x = math.cos(angle)
        self.dir_y = math.sin(angle)
        self.damage = damage
        self.lifetime = magic_projectile_lifetime
        self.is_dead = False
        self.x += self.dir_x * 20
        self.y += self.dir_y * 20
        self.rect.center = (int(self.x), int(self.y))

    def update(self, dt, enemies):
        if self.is_dead:
            return
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.is_dead = True
            return

        self.x += self.dir_x * magic_projectile_speed * dt
        self.y += self.dir_y * magic_projectile_speed * dt
        self.rect.center = (int(self.x), int(self.y))

        col = int(self.x // tile_size)
        row = int(self.y // tile_size)
        if (row < 0 or row >= len(drawed_map) or
                col < 0 or col >= len(drawed_map[0]) or
                drawed_map[row][col] in WTD):
            self.is_dead = True
            return

        for enemy in enemies:
            if getattr(enemy, "is_dead", False):
                continue
            if math.hypot(enemy.x - self.x, enemy.y - self.y) < 20:
                if hasattr(enemy, "take_damage"):
                    enemy.take_damage(self.damage)
                self.is_dead = True
                return

class Magic_Projectile_Manager:                            
    def __init__(self):
        self.projectiles = []

    def fire(self, x, y, angle, damage):
        self.projectiles.append(Magic_Shard_Projectile(x, y, angle, damage))

    def update(self, dt, enemies):
        for proj in self.projectiles[:]:
            proj.update(dt, enemies)
            if proj.is_dead:
                self.projectiles.remove(proj)

class Projectile_View:                                      
    def __init__(self, enemy_manager, magic_manager):
        self.projectiles = (list(enemy_manager.projectiles) +
                            list(magic_manager.projectiles))