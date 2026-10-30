import pygame
from Settings import *
from Projectile import ProjectileManager
from Map import drawed_map
from Objects import Sprite, Interactive_Sprite
from Sprites_Archive import ISD, WTD

class MapManager:
    def __init__(self):
        self.walls = []
        self.walls_grid = []
        self.enemy_spawns = []
        self.player_spawn = (half_width, half_height)
        self.objects = []
        self.interactive_objects = []
        
        self.create_map()

    def create_map(self, tile=tile_size):
        for row, line in enumerate(drawed_map):
            grid_row = []
            for col, ch in enumerate(line):
                grid_row.append(ch)
                
                x = col * tile
                y = row * tile
                center_x = x + tile // 2
                center_y = y + tile // 2
                
                if ch in WTD:
                    self.walls.append(pygame.Rect(x, y, tile, tile))
                elif ch == "1":
                    self.enemy_spawns.append(("ghoul", center_x, center_y))
                elif ch == "2":
                    self.enemy_spawns.append(("gargoyle", center_x, center_y))
                elif ch == "P":
                    self.player_spawn = (center_x, center_y)
                
            self.walls_grid.append(grid_row)

class EnemyManager:
    def __init__(self):
        self.enemies = []
        self.projectile_manager = ProjectileManager()

    def add_enemy(self, enemy):
        self.enemies.append(enemy)

    def update(self, dt, player):
        for enemy in self.enemies:
            enemy.update(dt, player, self.enemies)
            
            if hasattr(enemy, 'projectiles'):
                for proj in enemy.projectiles:
                    self.projectile_manager.add_projectile(proj)
                enemy.projectiles.clear()
                
        self.enemies = [e for e in self.enemies if not e.is_dead]

class Game:
    def __init__(self, screen, player, weapon, interface, icons):
        self.screen = screen
        self.player = player
        self.weapon = weapon
        self.interface = interface
        self.icons = icons
        
        self.map_manager = MapManager()
        self.enemy_manager = EnemyManager()
        
        player.x, player.y = self.map_manager.player_spawn
        player.rect.center = (player.x, player.y)
        
        self.objects = self.map_manager.objects
        self.interactive_objects = self.map_manager.interactive_objects
        
        from Ghoul import Ghoul
        from Gargoyle import Gargoyle
        for enemy_type, ex, ey in self.map_manager.enemy_spawns:
            if enemy_type == "ghoul":
                self.enemy_manager.add_enemy(Ghoul(ex, ey, "Assets/Sprites/Enemies/Ghoul/gh_front_stand.png", 0.8, 30))

            if enemy_type == "gargoyle":
                self.enemy_manager.add_enemy(Gargoyle(ex, ey, "Assets/Sprites/Enemies/Gargoyle/ga_front2.png", 0.8, 30))

    def update(self, dt):
        self.player.movement(dt, [])
        self.player.stats.update_effects(dt)
        self.enemy_manager.update(dt, self.player)
        self.enemy_manager.projectile_manager.update(dt, self.player, self.weapon)
        self.weapon.update(dt, (self.player.x, self.player.y), self.player.angle, self.player.is_sprinting)

    def draw(self):
        from Renderer import render_scene
        render_scene(
            self.player, self.screen, 
            self.objects, self.interactive_objects,
            self.enemy_manager.enemies, 
            self.enemy_manager.projectile_manager
        )
        self.weapon.draw(self.screen)
        
        from UI import draw_hud
        draw_hud(self.screen, self.player.stats, self.icons, self.interface)