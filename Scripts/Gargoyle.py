import pygame
import math
import random
from Settings import *
from Enemy import Enemy
from Projectile import Projectile
from Sprites_Archive import ESD

class Gargoyle(Enemy):
    def __init__(self, x, y, image_path, scale=1.0, collision_radius=20):
        super().__init__(x, y, image_path, scale, collision_radius)
        
        self.hp = 80
        self.speed = 18
        self.attack_range = 25
        self.attack_damage = 11
        self.gold_drop = gargoyle_gold_drop
        self.enemy_type = "gargoyle"
        
        self.state = "idle"
        self.state_timer = 0
        self.attack_timer = 0
        self.attack_direction = 0
        self.locked_view = None
        
        self.idle_center = (x, y)
        self.idle_radius = 60
        self.idle_angle = random.uniform(0, 2 * math.pi)
        self.idle_speed = 15
        
        self.windup_time = 0.5
        self.attack_time = 0.3
        self.recovery_time = 1.0
        
        self.dive_cooldown = 10
        self.dive_timer = 0
        self.dive_prep_time = 0.4
        self.dive_duration = 0.8
        self.dive_time_left = 0
        self.dive_speed = 250
        self.dive_damage = 1
        
        self.projectiles = []
        self.echo_cooldown = 20
        self.echo_timer = 0
        self.echo_waves_left = 0
        self.echo_wave_timer = 0
        self.echo_projectile_count = 8
        self.echo_spread = 2 * math.pi / self.echo_projectile_count
        
        self.is_statue = False
        self.statue_trigger_hp = self.max_hp * 0.2
        self.statue_duration = 2.0
        self.fall_damage = 100
        self.fall_radius = 100
        
        self.aggro_range = 150
        self.is_aggro = False
        self.flight_height = 90
        
        g_data = ESD["gargoyle"]
        
        def load_scaled(path):
            img = pygame.image.load(path).convert_alpha()
            w, h = img.get_size()
            return pygame.transform.scale(img, (int(w * scale), int(h * scale)))
        
        self.sprites = {
            "front": {
                "stand": load_scaled(g_data["f_stand"]),
                "move": [load_scaled(g_data["f_move1"]), load_scaled(g_data["f_move2"])],
                "attack": load_scaled(g_data["f_attack"]),
                "echo": load_scaled(g_data["f_echo"]),
                "dive": load_scaled(g_data["f_dive"])
            },
            "side": {
                "stand": load_scaled(g_data["s_stand"]),
                "move": [load_scaled(g_data["s_move1"]), load_scaled(g_data["s_move2"])],
                "attack": load_scaled(g_data["s_attack"]),
                "echo": load_scaled(g_data["s_echo"]),
                "dive": load_scaled(g_data["s_dive"])
            },
            "back": {
                "stand": load_scaled(g_data["b_stand"]),
                "move": [load_scaled(g_data["b_move1"]), load_scaled(g_data["b_move2"])],
                "attack": load_scaled(g_data["b_attack"]),
                "echo": load_scaled(g_data["b_echo"]),
                "dive": load_scaled(g_data["b_dive"])
            }
        }
        
        self.img_hit = load_scaled(g_data["hit"])
        self.img_statue = load_scaled(g_data["statue"])
        self.img_fall = load_scaled(g_data["fall"])
        self.img_death = load_scaled(g_data["death"])
        self.projectile_img = g_data["proj"]
        
        self.image = self.sprites["front"]["stand"]
        
        self.current_move_frame = 0
        self.anim_timer = 0
        self.anim_speed = 0.25
        self.hit_timer = 0

    def update(self, dt, player, all_enemies):
        if self.is_dead:
            self.drop_loot()
            self.image = self.img_death
            return

        self.player = player
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.hypot(dx, dy)

        if self.attack_timer > 0: self.attack_timer -= dt
        if self.state_timer > 0: self.state_timer -= dt
        if self.hit_timer > 0: self.hit_timer -= dt
        if self.dive_timer > 0: self.dive_timer -= dt
        if self.echo_timer > 0: self.echo_timer -= dt
        if self.echo_wave_timer > 0: self.echo_wave_timer -= dt

        target_angle = math.atan2(dy, dx)
        
        if self.state in ["windup", "attack", "dive_prep", "diving", "echo_prep", "echo_attack"]:
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
            current_angle = target_angle
            self.attack_direction = target_angle
            self.locked_view = None
            angle_diff = abs(player.angle - current_angle)
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

        if self.hp <= self.statue_trigger_hp and not self.is_statue and not self.is_dead:
            self.state = "stone"
            self.is_statue = True
            self.state_timer = self.statue_duration
            self.image = self.img_statue
            return

        if self.state == "idle":
            self.image = sprites["stand"]
            self.idle_angle += 0.5 * dt
            target_x = self.idle_center[0] + math.cos(self.idle_angle) * self.idle_radius
            target_y = self.idle_center[1] + math.sin(self.idle_angle) * self.idle_radius
            self.move_towards(target_x, target_y, self.idle_speed, dt, all_enemies)
            
            if self.can_see_player(player):
                self.is_aggro = True
                self.state = "chase"

        elif self.state == "chase":
            if not self.is_aggro:
                if self.can_see_player(player):
                    self.is_aggro = True
                else:
                    self.state = "idle"
                    return
            
            if self.is_aggro:
                if distance < 100 and self.echo_timer <= 0:
                    self.state = "echo_prep"
                    self.state_timer = 0.5
                    self.echo_timer = self.echo_cooldown
                    self.echo_waves_left = 3
                    self.attack_direction = target_angle
                elif 40 < distance < 350 and self.dive_timer <= 0:
                    self.state = "dive_prep"
                    self.state_timer = self.dive_prep_time
                    self.dive_timer = self.dive_cooldown
                    self.attack_direction = target_angle
                elif distance <= self.attack_range and self.attack_timer <= 0:
                    self.state = "windup"
                    self.state_timer = self.windup_time
                    self.attack_direction = target_angle
                elif distance > self.attack_range:
                    self.anim_timer += dt
                    if self.anim_timer >= self.anim_speed:
                        self.anim_timer = 0.0
                        self.current_move_frame = (self.current_move_frame + 1) % 2
                    self.image = sprites["move"][self.current_move_frame]
                    self.move_towards(player.x, player.y, self.speed, dt, all_enemies)

        elif self.state == "windup":
            self.image = sprites["attack"]
            if self.state_timer <= 0:
                self.state = "attack"
                self.state_timer = self.attack_time

        elif self.state == "attack":
            if self.state_timer <= 0:
                dx_attack = player.x - self.x
                dy_attack = player.y - self.y
                angle_to_player = math.atan2(dy_attack, dx_attack)
                
                angle_diff_attack = abs(self.attack_direction - angle_to_player)
                if angle_diff_attack > math.pi:
                    angle_diff_attack = 2 * math.pi - angle_diff_attack
                
                if distance <= self.attack_range + 10 and angle_diff_attack < math.pi / 4:
                    player.stats.base.take_damage(self.attack_damage)
                    
                self.state = "recovery"
                self.state_timer = self.recovery_time

        elif self.state == "recovery":
            self.image = sprites["stand"]
            if self.state_timer <= 0:
                self.state = "chase"
                self.attack_timer = 1

        elif self.state == "dive_prep":
            self.image = sprites["dive"]
            if self.state_timer <= 0:
                self.state = "diving"
                self.dive_time_left = self.dive_duration

        elif self.state == "diving":
            self.image = sprites["dive"]
            self.dive_time_left -= dt
            
            move_x = math.cos(self.attack_direction) * self.dive_speed * dt
            move_y = math.sin(self.attack_direction) * self.dive_speed * dt
            
            new_x = self.x + move_x
            if not self.is_wall(new_x, self.y):
                self.x = new_x
                self.rect.center = (self.x, self.y)
            else:
                self.state = "recovery"
                self.state_timer = self.recovery_time
                return
                
            new_y = self.y + move_y
            if not self.is_wall(self.x, new_y):
                self.y = new_y
                self.rect.center = (self.x, self.y)
            else:
                self.state = "recovery"
                self.state_timer = self.recovery_time
                return

            if distance <= self.attack_range + 15:
                player.stats.base.take_damage(self.dive_damage)
            
            if self.dive_time_left <= 0:
                self.state = "recovery"
                self.state_timer = self.recovery_time

        elif self.state == "echo_prep":
            self.image = sprites["echo"]
            if self.state_timer <= 0:
                for i in range(self.echo_projectile_count):
                    angle = self.echo_spread * i
                    proj = Projectile(self.x, self.y, 
                                      self.x + math.cos(angle) * 100, 
                                      self.y + math.sin(angle) * 100, 
                                      self.projectile_img)
                    proj.effect = "paralysis"
                    proj.speed = 180
                    self.projectiles.append(proj)
                
                self.echo_waves_left -= 1
                self.echo_wave_timer = 0.5
                self.state = "echo_attack"

        elif self.state == "echo_attack":
            self.image = sprites["echo"]
            if self.echo_wave_timer <= 0:
                if self.echo_waves_left > 0:
                    for i in range(self.echo_projectile_count):
                        angle = self.echo_spread * i + (self.echo_waves_left * 0.2)
                        proj = Projectile(self.x, self.y, 
                                          self.x + math.cos(angle) * 100, 
                                          self.y + math.sin(angle) * 100, 
                                          self.projectile_img)
                        proj.effect = "paralysis"
                        proj.speed = 180
                        self.projectiles.append(proj)
                    
                    self.echo_waves_left -= 1
                    self.echo_wave_timer = 0.5
                else:
                    self.state = "recovery"
                    self.state_timer = self.recovery_time

        elif self.state == "stone":
            self.image = self.img_statue
            if self.state_timer <= 0:
                self.state = "falling"
                self.state_timer = 0.5  
                self.image = self.img_fall  
                self.attack_direction = target_angle
                
        elif self.state == "falling":
            self.image = self.img_fall  
            if self.state_timer <= 0:
                if distance <= self.fall_radius:
                    player.stats.base.take_damage(self.fall_damage)
                self.drop_loot()
                self.is_dead = True
                self.state = "dead"

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
        if self.state in ["windup", "attack"]:
            amount = int(amount * 0) 
        
        super().take_damage(amount)
        
        if not self.is_dead:
            self.hit_timer = 0.2