import math
from Settings import *
from Objects import Sprite
from Map import drawed_map

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
                drawed_map[row][col] == "H"):
                self.projectiles.remove(proj)
                continue
            
            if proj.rect.colliderect(player.rect):
                if weapon.try_absorb_projectile(proj, player.x, player.y, player.angle):
                    self.projectiles.remove(proj)
                else:
                    if proj.effect == "poison":
                        player.stats.effects.apply_poison()
                    elif proj.effect == "paralysis":
                        player.stats.effects.apply_paralysis()
                    elif proj.effect == "blood":
                        player.stats.effects.apply_poison()
                        player.stats.effects.apply_paralysis()
                    elif proj.effect == "death":
                        player.stats.base.hp = 0
                    
                    player.stats.base.take_damage(5)
                    self.projectiles.remove(proj)

    def draw(self, screen, player, z_buffer, render_sprites_func):
        render_sprites_func(player, screen, self.projectiles)