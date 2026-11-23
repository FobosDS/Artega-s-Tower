import pygame
from Settings import *
from Projectile import ProjectileManager, Projectile_View
from Map import drawed_maps, set_floor_map
from Objects import Rare_Chest, Merchant, Shelf, Decoration, RingPickup, Barrier, Stairs, Altar, Chest, Gold_Heap, Food
from Sprites_Archive import ISD, WTD, RD, floor_names, SH, floor_decorations, floor_walls, floor_walls_default
import Items_Hub
import math                                
from UI import ToastMessage, Death_Screen, Artega_Scene
from Magic import Magic_System 


class MapManager:
    def __init__(self, floor=1):
        self.walls = []
        self.walls_grid = []
        self.enemy_spawns = []
        self.player_spawn = (half_width, half_height)
        self.objects = []
        self.interactive_objects = []
        self.barriers = []
        self.room_barrier_map = {}
        
        self.create_map(floor)

    def create_map(self, floor, tile=tile_size):
        self.walls.clear()
        self.walls_grid.clear()
        self.enemy_spawns.clear()
        self.interactive_objects.clear()
        self.barriers.clear()
        self.enemy_barrier = {}

        if floor not in drawed_maps or not drawed_maps[floor]:
            floor = 1
        set_floor_map(floor)
        drawed_map = drawed_maps[floor]

        for row, line in enumerate(drawed_map):
            grid_row = []
            for col, ch in enumerate(line):
                grid_ch = ch
                if ch == "W":                                      
                    variants = floor_walls.get(floor, floor_walls_default)
                    if not variants:
                        variants = floor_walls_default
                    v = ((col * 31 + row * 17) * 7 + floor * 13) % 100
                    acc = 0
                    grid_ch = f"W_{floor}_{variants[-1][0]}"
                    for name, wgt, _path in variants:
                        acc += wgt
                        if v < acc:
                            grid_ch = f"W_{floor}_{name}"
                            break
                if ch == "H":
                    idx = (col * 31 + row * 17) % len(SH)   
                    grid_ch = f"H{idx}" 
                grid_row.append(grid_ch)
                
                x = col * tile
                y = row * tile
                center_x = x + tile // 2
                center_y = y + tile // 2
                
                if ch in WTD:
                    self.walls.append(pygame.Rect(x, y, tile, tile))
                    if ch == "H":
                        self.interactive_objects.append(Shelf(center_x, center_y))
                    elif ch == "E":   
                        self.interactive_objects.append(Stairs(center_x, center_y))
                    elif ch == "J":   
                        b = Barrier(center_x, center_y)
                        self.barriers.append(b)
                        self.interactive_objects.append(b)

                #enemies  
                elif ch == "1":
                    self.enemy_spawns.append(("ghoul", center_x, center_y))
                elif ch == "2":
                    self.enemy_spawns.append(("gargoyle", center_x, center_y))

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

                elif ch == "P":
                    self.player_spawn = (center_x, center_y)
                elif ch == "D":
                    if floor_decorations.get(floor):
                        self.objects.append(Decoration(center_x, center_y, floor))
                elif ch == "S":  
                    self.interactive_objects.append(Altar(center_x, center_y))
                elif ch == "C":
                    self.interactive_objects.append(Chest(center_x, center_y))
                elif ch == "G":
                    self.interactive_objects.append(Gold_Heap(center_x, center_y))
                elif ch == "F":
                    self.interactive_objects.append(Food(center_x, center_y))
                
            self.walls_grid.append(grid_row)

        for i, obj in enumerate(self.interactive_objects):
            obj.obj_id = i

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
    def __init__(self, screen, player, weapon, interface, icons, interaction_manager, sound_manager):
        self.screen = screen
        self.player = player
        self.weapon = weapon
        self.interface = interface
        self.icons = icons
        
        self.map_manager = MapManager(self.player.stats.current_floor)

        self._sync_renderer_map()  

        self.enemy_manager = EnemyManager()
        self.magic_system = Magic_System() 
        self.cutscene = Artega_Scene()
        
        player.x, player.y = self.map_manager.player_spawn
        player.rect.center = (player.x, player.y)
        
        self.objects = self.map_manager.objects
        self.interactive_objects = self.map_manager.interactive_objects

        self.toast = ToastMessage(half_width - 420, height - 180)
        self.death_screen = Death_Screen()

        self.rings_to_drop = []

        self.interaction_manager = interaction_manager

        self.sound_manager = sound_manager
        self.interaction_manager = interaction_manager

        from UI import Tab_Overlay
        self.tab_overlay = Tab_Overlay(self)
        self.tab_overlay.visible = False
        
        from Ghoul import Ghoul
        from Gargoyle import Gargoyle
        for idx, (enemy_type, ex, ey) in enumerate(self.map_manager.enemy_spawns):
            enemy = None
            if enemy_type == "ghoul":
                enemy = Ghoul(ex, ey, "Assets/Sprites/Enemies/Ghoul/gh_front_stand.png", 0.8, 30)
            elif enemy_type == "gargoyle":
                enemy = Gargoyle(ex, ey, "Assets/Sprites/Enemies/Gargoyle/ga_front2.png", 0.8, 30)
            if enemy is not None:
                enemy.enemy_id = idx
                self.enemy_manager.add_enemy(enemy)
                
    def spawn_ring_pickup(self, ring_type, x, y, needs_manual=True):
        pickup = RingPickup(x, y, ring_type)
        self.interactive_objects.append(pickup)
        return pickup

    def give_ring_to_player(self, ring_type):
        return self.player.stats.base.add_ring(ring_type)  

    def drop_ring(self, ring_type, x, y):
        self.spawn_ring_pickup(ring_type, x, y)
        self.player.stats.notify(f"Оскар уронил на пол: {RD[ring_type]['name']}")

    def update(self, dt):
        if self.cutscene.active:                                
            self.cutscene.update(dt)
            if self.cutscene.done and not self.cutscene.notified:
                self.cutscene.notified = True
                self.player.stats.notify(
                    "Оскар, будучи глухонемым, понял речь Артеги...Он дрожит от ужаса!")
            return
        
        if self.death_screen.active:                               
            self.sound_manager.update(dt)
            self.death_screen.update(dt)
            return

        if self.player.stats.base.is_dead():                       
            if not self.death_screen.active:
                self.death_screen.start()
                self.sound_manager.play_death_music()              
            return
        
        self.sound_manager.update(dt)
        self.interaction_manager.update_prompt(self.player.rect, self.player.stats)
        while self.player.stats.pending_messages:
            self.toast.set_message(self.player.stats.pending_messages.pop(0))

        self.toast.update(dt)

        prev_alive = len(self.enemy_manager.enemies)

        self.player.movement(dt, self.objects + self.interactive_objects)
        self.player.stats.update_effects(dt)
        self.enemy_manager.update(dt, self.player)
        self.enemy_manager.projectile_manager.update(dt, self.player, self.weapon)
        self.weapon.update(dt, (self.player.x, self.player.y), self.player.angle, self.player.is_sprinting)
        self.magic_system.update(dt, self.player, self.enemy_manager.enemies)

        if prev_alive > 0 and len(self.enemy_manager.enemies) == 0:
            if not self.player.stats.is_floor_key:
                self.player.stats.is_floor_key = True
                self.toast.set_message("Потеряв всякую надежду выбраться из башни, Оскар находит на трупе врага...Ключ от этажа!")

        while self.rings_to_drop:
            ring_type = self.rings_to_drop.pop(0)
            self.spawn_ring_pickup(ring_type, self.player.x + 30, self.player.y)

        displaced = self.player.stats.last_displaced_ring

        if displaced is not None:
            self.player.stats.last_displaced_ring = None
            drop_x = self.player.x + math.cos(self.player.angle) * 30
            drop_y = self.player.y + math.sin(self.player.angle) * 30
            hitbox = pygame.Rect(drop_x - 5, drop_y - 5, 10, 10)
            if any(hitbox.colliderect(w) for w in self.map_manager.walls):
                drop_x, drop_y = self.player.x, self.player.y  
            self.drop_ring(displaced, drop_x, drop_y)

        for obj in self.interactive_objects[:]:
            if not isinstance(obj, RingPickup):
                continue
            if not obj.taken:
                continue
            self.interactive_objects.remove(obj)

        if self.player.stats.request_save:
            self.player.stats.request_save = False
            self.save_game()

        if self.player.stats.request_next_floor:
            self.player.stats.request_next_floor = False
            self.next_floor()

    def next_floor(self):
        next_floor_num = self.player.stats.current_floor + 1

        self.player.stats.current_floor = next_floor_num
        self.cutscene.maybe_trigger(self.player.stats)

        self.player.stats.is_chest_key1 = False
        self.player.stats.is_chest_key2 = False
        self.player.stats.is_floor_key = False

        self.map_manager = MapManager(self.player.stats.current_floor)

        self._sync_renderer_map()  

        self.objects = self.map_manager.objects
        self.interactive_objects = self.map_manager.interactive_objects
        self.interaction_manager.interactive_objects = self.interactive_objects

        self.player.x, self.player.y = self.map_manager.player_spawn
        self.player.rect.center = (self.player.x, self.player.y)

        self.enemy_manager.enemies.clear()
        from Ghoul import Ghoul
        from Gargoyle import Gargoyle
        for idx, (enemy_type, ex, ey) in enumerate(self.map_manager.enemy_spawns):
            enemy = None
            if enemy_type == "ghoul":
                enemy = Ghoul(ex, ey, "Assets/Sprites/Enemies/Ghoul/gh_front_stand.png", 0.8, 30)
            elif enemy_type == "gargoyle":
                enemy = Gargoyle(ex, ey, "Assets/Sprites/Enemies/Gargoyle/ga_front2.png", 0.8, 30)
            if enemy is not None:
                enemy.enemy_id = idx
                self.enemy_manager.add_enemy(enemy)
        self.weapon.enemies = self.enemy_manager.enemies

        self.sound_manager.set_floor_music(self.player.stats.current_floor)
        self.toast.set_message(f"Оскар поднялся на {floor_names[self.player.stats.current_floor]}!")

    def save_game(self):
        import json

        enemies_alive = [e.enemy_id for e in self.enemy_manager.enemies if not e.is_dead]

        objects_state = []

        for obj in self.interactive_objects:
            state = {"id": getattr(obj, "obj_id", -1), "type": type(obj).__name__}
            if isinstance(obj, Shelf):
                state["used"] = obj.is_action_perfomed
            elif isinstance(obj, Rare_Chest):
                state["open"] = obj.is_open
            elif isinstance(obj, Merchant):
                state["unique_item"] = obj.unique_item
                state["trades_done"] = obj.trades_done
                state["price"] = obj.price
            elif isinstance(obj, Barrier):
                state["broken"] = obj.broken
            elif isinstance(obj, Gold_Heap):
                state["taken"] = obj.taken
            elif isinstance(obj, Food):
                state["taken"] = obj.taken
            else:
                continue
            objects_state.append(state)

        data = {
            "floor": self.player.stats.current_floor,
            "hp": self.player.stats.base.hp,
            "sp": self.player.stats.base.sp,
            "gold": self.player.stats.base.gold,
            "potions": self.player.stats.base.potions,
            "scrolls": self.player.stats.base.scrolls,
            "whetstones": self.player.stats.combat.whetstones,
            "weapon_level": self.player.stats.combat.weapon_level,
            "durability": self.player.stats.combat.durability,
            "hp_level": self.player.stats.base.hp_level,
            "sp_level": self.player.stats.base.sp_level,
            "rings": list(self.player.stats.base.rings),
            "dark_shards": self.player.stats.base.dark_shards,
            "is_chest_key1": self.player.stats.is_chest_key1,
            "is_chest_key2": self.player.stats.is_chest_key2,
            "is_floor_key": self.player.stats.is_floor_key,
            "enemies_alive": enemies_alive,
            "objects_state": objects_state,
            "artega_done": self.cutscene.done
        }
        with open(save_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        self.toast.set_message("Оскар получил благословение хозяина башни. Прогресс сохранен!")

    def apply_world_state(self):
        import json, os
        if not os.path.exists(save_file):
            return

        with open(save_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.cutscene.done = data.get("artega_done", False)

        alive = set(data.get("enemies_alive", []))
        self.enemy_manager.enemies[:] = [
            e for e in self.enemy_manager.enemies
            if getattr(e, "enemy_id", -1) in alive
        ]
        self.weapon.enemies = self.enemy_manager.enemies

        state_by_id = {s["id"]: s for s in data.get("objects_state", [])}

        to_remove = []
        for obj in self.interactive_objects:
            s = state_by_id.get(getattr(obj, "obj_id", -1))
            if s is None:
                continue

            if isinstance(obj, Shelf):
                obj.is_action_perfomed = s.get("used", obj.is_action_perfomed)
            elif isinstance(obj, Rare_Chest):
                obj.is_open = s.get("open", obj.is_open)
                if obj.is_open:
                    obj.image = pygame.image.load(ISD["rare_chest"]["open"]).convert_alpha()
            elif isinstance(obj, Merchant):
                obj.unique_item = s.get("unique_item", obj.unique_item)   
                obj.trades_done = s.get("trades_done", obj.trades_done)   
                obj.price = s.get("price", obj.price)
            elif isinstance(obj, Barrier):
                if s.get("broken", False):                                        
                    obj.break_barrier()
            elif isinstance(obj, Gold_Heap):                     
                obj.taken = s.get("taken", obj.taken)
            elif isinstance(obj, Food):                     
                obj.taken = s.get("taken", obj.taken)            
            elif isinstance(obj, RingPickup):
                if s["taken"]:
                    to_remove.append(obj)
                else:
                    obj.ring_type = s["ring_type"]
                    obj.x = s["x"]
                    obj.y = s["y"]
                    obj.rect.center = (obj.x, obj.y)

        for obj in to_remove:
            self.interactive_objects.remove(obj)

    def draw(self):
        from Renderer import render_scene
        render_scene(
            self.player, self.screen,
            self.objects, self.interactive_objects,
            self.enemy_manager.enemies,
            Projectile_View(self.enemy_manager.projectile_manager,
                            self.magic_system.projectile_manager),  
            self.map_manager.walls_grid,
            self.player.stats.current_floor
        )
        self.weapon.draw(self.screen)
        
        loaded = getattr(self.player.stats.combat, "magic_shots_loaded", 0)   
        if loaded > 0:
            alpha = int(magic_overlay_max_alpha * loaded / magic_shots_at_max)
            veil = pygame.Surface((width, height), pygame.SRCALPHA)
            veil.fill((*magic_overlay_color, alpha))
            self.screen.blit(veil, (0, 0))
        
        from UI import draw_hud, draw_prompt
        draw_hud(self.screen, self.player.stats, self.icons, self.interface)
        self.toast.draw(self.screen)
        draw_prompt(self.screen, self.interaction_manager.current_prompt)

        self.tab_overlay.draw_rings_panel(self.screen)
        self.tab_overlay.draw_map_panel(self.screen)

        if self.death_screen.active:                              
            self.death_screen.draw(self.screen)

        self.cutscene.draw(self.screen) 

    def _sync_renderer_map(self):
        import Renderer
        Renderer.map_manager.walls[:] = self.map_manager.walls
        Renderer.map_manager.walls_grid[:] = self.map_manager.walls_grid
        self.player.map[:] = self.map_manager.walls