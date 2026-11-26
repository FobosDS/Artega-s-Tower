import pygame
import math
import random
from Settings import *
from Enemy import Enemy
from Projectile import Projectile
from Sprites_Archive import ESD


class Vampire(Enemy):
    def __init__(self, x, y, image_path, scale=1.0, collision_radius=14):
        super().__init__(x, y, image_path, scale, collision_radius)

        self.collision_radius = collision_radius

        self.hp = 120
        self.max_hp = 120
        self.speed = 14
        self.attack_range = 40
        self.attack_damage = 22
        self.gold_drop = vampire_gold_drop
        self.enemy_type = "vampire"

        self.state = "chase"
        self.state_timer = 0
        self.attack_timer = 0
        self.attack_direction = 0
        self.locked_view = None

        self.attack_step = 0

        self.projectiles = []
        self.warning_message = None

        self.teleport_cooldown = 15
        self.teleport_timer = 0
        self.bite_damage = 45
        self.bite_radius = 60
        self.bite_windup = 1.0

        self.aggro_range = 140
        self.is_aggro = False

        self.dodge_chance = 0.25
        self.reflect_chance = 0.2
        self.is_dodging = False
        self.dodge_timer = 0
        self.dodge_duration = 0.25
        self.dodge_distance = 90

        self.heal_cooldown = 20
        self.heal_timer = 0
        self.damage_buff = 1
        self.buff_time_left = 0

        self.dash_chance = 0.008
        self.dash_cooldown = 14
        self.dash_windup = 0.4
        self.dash_distance = 260
        self.dash_speed = 750
        self.dash_min_range = 150
        self.dash_max_range = 420
        self.dash_timer = 0
        self.dash_left = 0
        self.dash_dx = 0
        self.dash_dy = 0

       
        self.combo_patterns = [
            ["dash_strike"],                                
            ["lunge"],                                      
            ["strike", "dash_strike"],                      
            ["lunge", "dash_strike", "dash_strike", "rest"] 
        ]
        self.combo_queue = []
        self.quick_windup = 0.15            
        self.quick_dash_distance = 110     
        self.quick_dash_speed = 800        
        self.lunge_windup = 0.35           
        self.lunge_distance = 230          
        self.lunge_speed = 650             
        self.lunge_damage_mult = 1.7        
        self.rest_time = 0.5               
        self.combo_damage_mult = 1.0       

        self.spheres = []  
        self.sphere_sprites = []                 
        self.sphere_max = 3
        self.sphere_spawn_interval = 0.35   
        self.sphere_spawn_timer = 0
        self.sphere_hold_time = 2         
        self.sphere_launch_interval = 0.45  
        self.launch_gap = 0

        self.dying = False
        self.dying_timer = 0
        self.death_duration = 0.9

        v_data = ESD["vampire"]

        def load_scaled(path):
            img = pygame.image.load(path).convert_alpha()
            w, h = img.get_size()
            return pygame.transform.scale(img, (int(w * scale), int(h * scale)))

        self.sprites = {
            "front": {
                "stand": load_scaled(v_data["f_stand"]),
                "walk": [load_scaled(v_data["f_move1"]), load_scaled(v_data["f_move2"])],
                "take": load_scaled(v_data["f_take_rapier"]),
                "attack_pre": load_scaled(v_data["f_attack_pre"]),
                "attack": load_scaled(v_data["f_attack"]),
                "dash": load_scaled(v_data["f_dash"]),
                "cast": load_scaled(v_data["f_cast"])
            },
            "side": {
                "stand": load_scaled(v_data["s_stand"]),
                "walk": [load_scaled(v_data["s_move1"]), load_scaled(v_data["s_move2"])],
                "take": load_scaled(v_data["s_take_rapier"]),
                "attack_pre": load_scaled(v_data["s_attack_pre"]),
                "attack": load_scaled(v_data["s_attack"]),
                "dash": load_scaled(v_data["s_dash"]),
                "cast": load_scaled(v_data["s_cast"])
            },
            "back": {
                "stand": load_scaled(v_data["b_stand"]),
                "walk": [load_scaled(v_data["b_move1"]), load_scaled(v_data["b_move2"])],
                "take": load_scaled(v_data["b_take_rapier"]),
                "attack_pre": load_scaled(v_data["b_attack_pre"]),
                "attack": load_scaled(v_data["b_attack"]),
                "dash": load_scaled(v_data["b_dash"]),
                "cast": load_scaled(v_data["b_cast"])
            }
        }

        self.tp_frames = [
            load_scaled(v_data["tp1"]),
            load_scaled(v_data["tp2"]),
            load_scaled(v_data["tp3"])
        ]
        self.img_hit = load_scaled(v_data["hit"])
        self.img_death = load_scaled(v_data["death"])
        self.img_gone = pygame.Surface((4, 4), pygame.SRCALPHA)   

        #НОВОЕ: картинки сфер из словаря proj
        self.sphere_img_lev = load_scaled(v_data["proj"]["levitating"])
        self.sphere_img_atk = load_scaled(v_data["proj"]["attack"])
        self.proj_throwed_path = v_data["proj"]["throwed"]

        self.image = self.sprites["front"]["stand"]

        self.current_walk_frame = 0
        self.anim_timer = 0.0
        self.anim_speed = 0.22
        self.hit_timer = 0.0

    def update(self, dt, player, all_enemies):
        if self.dying:                                     
            self.dying_timer -= dt
            t = self.death_duration - self.dying_timer
            if t < 0.3:
                self.image = self.tp_frames[0]
            elif t < 0.6:
                self.image = self.tp_frames[1]
            elif t < 0.85:
                self.image = self.tp_frames[2]
            else:
                self.image = self.img_gone
            if self.dying_timer <= 0:
                self.drop_loot()
                self.has_dropped = True
                self.is_dead = True
            return

        if self.is_dead:
            self.image = self.img_gone
            return

        self.player = player
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.hypot(dx, dy)
        target_angle = math.atan2(dy, dx)

        if self.attack_timer > 0: self.attack_timer -= dt
        if self.state_timer > 0: self.state_timer -= dt
        if self.hit_timer > 0: self.hit_timer -= dt
        if self.teleport_timer > 0: self.teleport_timer -= dt
        if self.heal_timer > 0: self.heal_timer -= dt
        if self.dash_timer > 0: self.dash_timer -= dt
        if self.buff_time_left > 0:
            self.buff_time_left -= dt
            if self.buff_time_left <= 0:
                self.damage_buff = 1

        if self.is_dodging:
            self.dodge_timer -= dt
            if self.dodge_timer <= 0:
                self.is_dodging = False
            self.image = self.sprites["side"]["walk"][0]
            return

        if self.state in ["strike_pre", "attack_hit", "quick_dash",
                          "lunge_windup", "lunge_fly", "rest",
                          "cast", "sphere_hold", "sphere_launch",
                          "teleport_out", "teleport_in", "bite",
                          "dash_prepare", "dash"]:
            current_angle = self.attack_direction
            if self.locked_view is None:
                angle_diff = abs(player.angle - current_angle)
                if angle_diff > math.pi:
                    angle_diff = 2 * math.pi - angle_diff
                if angle_diff < math.pi / 4:
                    self.locked_view = "back"
                elif angle_diff > 3 * math.pi / 4:
                    self.locked_view = "front"
                else:
                    self.locked_view = "side"
            view = self.locked_view
        else:
            self.attack_direction = target_angle
            self.locked_view = None
            angle_diff = abs(player.angle - target_angle)
            if angle_diff > math.pi:
                angle_diff = 2 * math.pi - angle_diff
            if angle_diff < math.pi / 4:
                view = "back"
            elif angle_diff > 3 * math.pi / 4:
                view = "front"
            else:
                view = "side"

        sprites = self.sprites[view]

        if self.hit_timer > 0:
            self.image = self.img_hit
            return

        if self.state == "chase":
            if not self.is_aggro and self.can_see_player(player):
                self.is_aggro = True

            if not self.is_aggro:
                self.anim_timer += dt
                if self.anim_timer >= self.anim_speed:
                    self.anim_timer = 0.0
                    self.current_walk_frame = (self.current_walk_frame + 1) % 2
                self.image = sprites["walk"][self.current_walk_frame]
                return

            if self.hp < self.max_hp * 0.5 and self.heal_timer <= 0:
                victim = self.find_ghoul_to_drain(all_enemies)
                if victim is not None:
                    self.drain_ghoul(victim)
                    return

            if (self.teleport_timer <= 0
                    and distance <= self.attack_range + 70
                    and random.random() < 0.03):
                self.warning_message = "Оскар чувствует хладное дыхание сзади"
                self.state = "teleport_out"
                self.state_timer = 0.3
                self.teleport_timer = self.teleport_cooldown
                self.attack_direction = target_angle
                return

            if distance <= self.attack_range + 50 and self.attack_timer <= 0:
                self.rest_time = 1.2 if random.random() < 0.25 else 0.5
                self.combo_queue = list(random.choice(self.combo_patterns))
                self.attack_direction = target_angle
                self.advance_combo()
                return

            if (self.dash_timer <= 0 and self.attack_timer <= 0
                    and self.dash_min_range < distance < self.dash_max_range
                    and random.random() < self.dash_chance):
                self.state = "dash_prepare"
                self.state_timer = self.dash_windup
                self.attack_direction = target_angle
                return

            if 120 < distance < 400 and self.attack_timer <= 0 and random.random() < 0.02:
                self.state = "cast"
                self.spheres.clear()
                self.sphere_sprites.clear()
                self.sphere_spawn_timer = 0
                self.attack_direction = target_angle
                return

            if distance > self.attack_range:
                self.anim_timer += dt
                if self.anim_timer >= self.anim_speed:
                    self.anim_timer = 0.0
                    self.current_walk_frame = (self.current_walk_frame + 1) % 2
                self.image = sprites["walk"][self.current_walk_frame]
                self.move_towards(player.x, player.y, self.speed, dt, all_enemies)
            else:
                self.image = sprites["stand"]

        elif self.state == "strike_pre":                   
            self.image = sprites["attack_pre"]
            if self.state_timer <= 0:
                self.state = "attack_hit"
                self.state_timer = 0.22

        elif self.state == "quick_dash":
            self.image = sprites["dash"]
            step = self.quick_dash_speed * dt
            moved = 0.0
            nx = self.x + self.dash_dx * step
            if (not self.is_wall(nx, self.y)
                    and math.hypot(nx - player.x, self.y - player.y) > self.collision_radius + 18):
                self.x = nx
                moved = step
            ny = self.y + self.dash_dy * step
            if (not self.is_wall(self.x, ny)
                    and math.hypot(self.x - player.x, ny - player.y) > self.collision_radius + 18):
                self.y = ny
                moved = step
            self.rect.center = (self.x, self.y)
            self.dash_left -= moved
            if self.dash_left <= 0 or moved == 0:            
                self.state = "strike_pre"
                self.state_timer = self.quick_windup

        elif self.state == "lunge_windup":                  
            self.image = sprites["attack_pre"]
            if self.state_timer <= 0:
                if distance > 1:
                    self.dash_dx = dx / distance
                    self.dash_dy = dy / distance
                else:
                    self.dash_dx, self.dash_dy = 1.0, 0.0
                self.dash_left = self.lunge_distance
                self.combo_damage_mult = self.lunge_damage_mult
                self.state = "lunge_fly"

        elif self.state == "lunge_fly":
            self.image = sprites["dash"]
            if distance > 1:
                self.dash_dx = dx / distance
                self.dash_dy = dy / distance
            step = self.lunge_speed * dt
            moved = 0.0
            nx = self.x + self.dash_dx * step
            if (not self.is_wall(nx, self.y)
                    and math.hypot(nx - player.x, self.y - player.y) > self.collision_radius + 18):
                self.x = nx
                moved = step
            ny = self.y + self.dash_dy * step
            if (not self.is_wall(self.x, ny)
                    and math.hypot(self.x - player.x, ny - player.y) > self.collision_radius + 18):
                self.y = ny
                moved = step
            self.rect.center = (self.x, self.y)
            self.dash_left -= moved
            if self.dash_left <= 0 or moved == 0 or distance <= self.attack_range:
                self.state = "attack_hit"
                self.state_timer = 0.25

        elif self.state == "attack_hit":                    
            self.image = sprites["attack"]
            if self.state_timer <= 0:
                self.try_attack_player(player, self.attack_damage * self.combo_damage_mult * self.damage_buff, math.pi / 2)
                self.combo_damage_mult = 1.0
                self.advance_combo()

        elif self.state == "rest":                          
            self.image = sprites["stand"]
            if self.state_timer <= 0:
                self.state = "chase"
                self.attack_timer = 0.8

        elif self.state == "cast":
            self.image = sprites["cast"]                       
            self._sync_sphere_sprites(player, distance)        
            if self.sphere_spawn_timer > 0: self.sphere_spawn_timer -= dt
            if len(self.spheres) < self.sphere_max and self.sphere_spawn_timer <= 0:
                self.spheres.append({"img": self.sphere_img_lev, "t": 0.0})
                self.sphere_spawn_timer = self.sphere_spawn_interval
            if len(self.spheres) >= self.sphere_max:
                self.state = "sphere_hold"
                self.state_timer = self.sphere_hold_time

        elif self.state == "sphere_hold":
            self.image = sprites["cast"]
            self._sync_sphere_sprites(player, distance)
            if self.state_timer <= 0:
                self.state = "sphere_launch"
                self.launch_gap = 0.2

        elif self.state == "sphere_launch":
            self.image = sprites["cast"]
            self._sync_sphere_sprites(player, distance)
            if self.launch_gap > 0:
                self.launch_gap -= dt
            elif self.spheres:
                s = self.spheres[0]
                if s["img"] is self.sphere_img_lev:
                    s["img"] = self.sphere_img_atk
                    s["t"] = 0.2
                else:
                    s["t"] -= dt
                    if s["t"] <= 0:
                        proj = Projectile(self.x, self.y - 40, player.x, player.y, self.proj_throwed_path)
                        proj.effect = "blood"
                        proj.speed = 220
                        self.projectiles.append(proj)
                        self.spheres.pop(0)
                        self.sphere_sprites.pop(0)             
                        self.launch_gap = self.sphere_launch_interval
            else:
                self.sphere_sprites = []
                self.state = "chase"
                self.attack_timer = 1.2

        elif self.state == "teleport_out":
            self.image = self.tp_frames[0] if self.state_timer > 0.15 else self.tp_frames[1]
            if self.state_timer <= 0:
                self.state = "teleport_in"
                self.state_timer = 0.1
                placed = False                               
                for ang in (0.0, -0.7, 0.7, -1.4, 1.4):
                    px = player.x - math.cos(player.angle + ang) * 45
                    py = player.y - math.sin(player.angle + ang) * 45
                    if not self.is_wall(px, py):
                        self.x, self.y = px, py
                        self.rect.center = (self.x, self.y)
                        placed = True
                        break

        elif self.state == "teleport_in":
            self.image = self.tp_frames[2]
            if self.state_timer <= 0:
                self.state = "bite"
                self.state_timer = self.bite_windup
                self.attack_direction = math.atan2(player.y - self.y, player.x - self.x)

        elif self.state == "bite":
            self.image = sprites["attack"]
            if self.state_timer <= 0:
                dist_now = math.hypot(player.x - self.x, player.y - self.y)
                if dist_now <= self.bite_radius:
                    player.stats.base.take_damage(self.bite_damage * self.damage_buff)
                    player.stats.effects.try_apply_poison(player.stats)
                    player.stats.effects.try_apply_paralysis(player.stats)
                self.state = "chase"
                self.attack_timer = 1.5

        elif self.state == "dash_prepare":
            self.image = sprites["attack_pre"]
            if self.state_timer <= 0:
                if distance > 1:
                    self.dash_dx = dx / distance
                    self.dash_dy = dy / distance
                else:
                    self.dash_dx, self.dash_dy = 1.0, 0.0
                self.locked_view = None
                self.state = "dash"
                self.dash_left = self.dash_distance

        elif self.state == "dash":
            self.image = sprites["dash"]
            step = self.dash_speed * dt
            moved = 0.0
            nx = self.x + self.dash_dx * step
            if (not self.is_wall(nx, self.y)
                    and math.hypot(nx - player.x, self.y - player.y) > self.collision_radius + 18):
                self.x = nx
                moved = step
            ny = self.y + self.dash_dy * step
            if (not self.is_wall(self.x, ny)
                    and math.hypot(self.x - player.x, ny - player.y) > self.collision_radius + 18):
                self.y = ny
                moved = step
            self.rect.center = (self.x, self.y)
            self.dash_left -= moved
            if self.dash_left <= 0 or moved == 0:
                self.dash_timer = self.dash_cooldown
                self.attack_timer = 1.0
                if distance <= self.attack_range + 20:
                    self.combo_queue = list(random.choice(self.combo_patterns))
                    self.advance_combo()
                else:
                    self.state = "chase"

    def advance_combo(self):                                 
        if not self.combo_queue:
            self.state = "rest"
            self.state_timer = self.rest_time
            return
        move = self.combo_queue.pop(0)
        if move == "strike":
            self.state = "strike_pre"
            self.state_timer = self.quick_windup
        elif move == "dash_strike":
            d = self.player
            ddx = d.x - self.x
            ddy = d.y - self.y
            dist = math.hypot(ddx, ddy) or 1
            self.dash_dx = ddx / dist
            self.dash_dy = ddy / dist
            self.dash_left = self.quick_dash_distance
            self.state = "quick_dash"
        elif move == "lunge":
            self.state = "lunge_windup"
            self.state_timer = self.lunge_windup
        elif move == "rest":
            self.state = "rest"
            self.state_timer = self.rest_time

    def find_ghoul_to_drain(self, all_enemies):
        best = None
        best_dist = 200
        for e in all_enemies:
            if e is self or e.is_dead:
                continue
            if getattr(e, "enemy_type", "") != "ghoul":
                continue
            d = math.hypot(e.x - self.x, e.y - self.y)
            if d < best_dist:
                best_dist = d
                best = e
        return best

    def drain_ghoul(self, ghoul):
        ghoul.hp = 0
        ghoul.is_dead = True
        ghoul.has_dropped = True
        self.hp = min(self.max_hp, self.hp + 60)
        self.damage_buff = 1.5
        self.buff_time_left = 20
        self.heal_timer = self.heal_cooldown

    def can_see_player(self, player):
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.hypot(dx, dy)
        if distance > self.aggro_range:
            return False
        steps = 20
        step_x = dx / steps
        step_y = dy / steps
        for i in range(1, steps):
            check_x = self.x + step_x * i
            check_y = self.y + step_y * i
            if self.is_wall(check_x, check_y):
                return False
        return True

    def take_damage(self, amount):
        if self.dying:
            return
        if self.state in ["strike_pre", "attack_hit", "lunge_windup"]:
            amount = int(amount * 0.6)                         

        if not self.is_dodging and random.random() < self.dodge_chance:
            self.start_dodge()
            return

        super().take_damage(amount)
        if self.is_dead:                                     
            self.is_dead = False
            self.dying = True
            self.dying_timer = self.death_duration
            self.state = "dying"
            return
        if not self.is_dead:
            self.hit_timer = 0.15

    def start_dodge(self):
        self.is_dodging = True
        self.dodge_timer = self.dodge_duration
        if self.player is not None:
            dx = self.player.x - self.x
            dy = self.player.y - self.y
            d = math.hypot(dx, dy)
            if d > 1:
                side_x = self.x - (dx / d) * self.dodge_distance
                side_y = self.y - (dy / d) * self.dodge_distance
                if not self.is_wall(side_x, self.y):
                    self.x = side_x
                    self.rect.center = (self.x, self.y)
                if not self.is_wall(self.x, side_y):
                    self.y = side_y
                    self.rect.center = (self.x, self.y)

    def try_reflect_magic(self):
        return random.random() < self.reflect_chance

    def _sync_sphere_sprites(self, player, distance):
        if not self.spheres:
            self.sphere_sprites = []
            return
        sh = height * self.scale * sprites_scale / max(1.0, distance)
        sph_w, sph_h = self.sphere_img_lev.get_size()
        gap = 2.0 * height * self.scale * sprites_scale * (sph_w / max(1, sph_h)) / width
        perp_x = math.sin(player.angle)     
        perp_y = -math.cos(player.angle)
        while len(self.sphere_sprites) < len(self.spheres):
            self.sphere_sprites.append(Sphere_Sprite(self.x, self.y, self.sphere_img_lev, self.scale))
        for i, (s, sp) in enumerate(zip(self.spheres, self.sphere_sprites)):
            offset = (i - (len(self.spheres) - 1) / 2) * gap
            sp.x = self.x + perp_x * offset
            sp.y = self.y + perp_y * offset
            sp.image = s["img"]            
            sp.flight_height = int(sh * 0.55)

class Sphere_Sprite:
    def __init__(self, x, y, img, scale):
        self.x = x
        self.y = y
        self.image = img
        self.scale = scale
        self.img_w, self.img_h = img.get_size()
        self.aspect = self.img_w / self.img_h
        self.flight_height = 0
