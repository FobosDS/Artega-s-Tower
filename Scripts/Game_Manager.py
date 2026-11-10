import pygame
from Settings import *
from Projectile import ProjectileManager
from Map import drawed_map
from Objects import Rare_Chest, Merchant, Shelf, Decoration, RingPickup
from Sprites_Archive import ISD, WTD
import Items_Hub
from UI import ToastMessage

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
                    if ch in "ABHIKL":
                        self.interactive_objects.append(Shelf(center_x, center_y))
                elif ch == "1":
                    self.enemy_spawns.append(("ghoul", center_x, center_y))
                elif ch == "2":
                    self.enemy_spawns.append(("gargoyle", center_x, center_y))
                elif ch == "P":
                    self.player_spawn = (center_x, center_y)

                #rare chest
                elif ch == "R":
                    self.interactive_objects.append(Rare_Chest(center_x, center_y))
                elif ch == "r":
                    self.interactive_objects.append(Rare_Chest(center_x, center_y, Items_Hub.heart))
                elif ch == "s":
                    self.interactive_objects.append(Rare_Chest(center_x, center_y, Items_Hub.lungs))
                elif ch == "t":
                    self.interactive_objects.append(Rare_Chest(center_x, center_y, Items_Hub.weapon_crate))
                elif ch == "u":
                    self.interactive_objects.append(Rare_Chest(center_x, center_y, Items_Hub.ring))

                #merchant
                elif ch == "M":
                    self.interactive_objects.append(Merchant(center_x, center_y))
                elif ch == "m":
                    self.interactive_objects.append(Merchant(center_x, center_y, Items_Hub.heart))
                elif ch == "n":
                    self.interactive_objects.append(Merchant(center_x, center_y, Items_Hub.lungs))
                elif ch == "o":
                    self.interactive_objects.append(Merchant(center_x, center_y, Items_Hub.weapon_crate))
                elif ch == "p":
                    self.interactive_objects.append(Merchant(center_x, center_y, Items_Hub.ring))

                elif ch == "D":
                    self.objects.append(Decoration(center_x, center_y))
                
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
                
        self.enemies[:] = [e for e in self.enemies if not e.is_dead]

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

        self.toast = ToastMessage(half_width - 420, height - 180)
        
        from Ghoul import Ghoul
        from Gargoyle import Gargoyle
        for enemy_type, ex, ey in self.map_manager.enemy_spawns:
            if enemy_type == "ghoul":
                self.enemy_manager.add_enemy(Ghoul(ex, ey, "Assets/Sprites/Enemies/Ghoul/gh_front_stand.png", 0.8, 30))

            if enemy_type == "gargoyle":
                self.enemy_manager.add_enemy(Gargoyle(ex, ey, "Assets/Sprites/Enemies/Gargoyle/ga_front2.png", 0.8, 30))

    def give_ring_to_player(self, ring_type):
        displaced = self.player.stats.base.add_ring(ring_type)
        if displaced:
            pickup = RingPickup(self.player.x + 30, self.player.y, displaced)
            self.interactive_objects.append(pickup)
        return displaced

    def update(self, dt):
        while self.player.stats.pending_messages:
            self.toast.set_message(self.player.stats.pending_messages.pop(0))

        self.toast.update(dt)

        prev_alive = len(self.enemy_manager.enemies)

        self.player.movement(dt, self.objects + self.interactive_objects)
        self.player.stats.update_effects(dt)
        self.enemy_manager.update(dt, self.player)
        self.enemy_manager.projectile_manager.update(dt, self.player, self.weapon)
        self.weapon.update(dt, (self.player.x, self.player.y), self.player.angle, self.player.is_sprinting)

        if prev_alive > 0 and len(self.enemy_manager.enemies) == 0:
            if not self.player.stats.is_floor_key:
                self.player.stats.is_floor_key = True
                self.toast.set_message("Потеряв всякую надежду выбраться из башни, Оскар находит на трупе врага...Ключ от этажа!")

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
        self.toast.draw(self.screen)