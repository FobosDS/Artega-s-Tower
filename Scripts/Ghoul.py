import pygame
import math
from Settings import *
from Enemy import Enemy
from Projectile import Projectile
from Sprites_Archive import ESD

class Ghoul(Enemy):
    def __init__(self, x, y, image_path, scale=1.0, collision_radius=12):
        super().__init__(x, y, image_path, scale, collision_radius)
        
        self.hp = 36
        self.speed = 11
        self.attack_range = 25
        self.attack_damage = 19
        self.gold_drop = ghoul_gold_drop
        self.enemy_type = "ghoul"

        self.state = "chase"
        self.state_timer = 0
        self.attack_timer = 0
        
        self.attack_direction = 0
        
        self.windup_time = 0.5
        self.attack_time = 0.3
        self.recovery_time = 1.5
        self.shoot_cooldown = 12
        self.shoot_timer = 0
        self.projectiles = []
        
        self.dash_cooldown = 9
        self.dash_timer = 0
        self.dash_duration = 0.6
        self.dash_time_left = 0
        self.dash_speed = 120
        self.dash_attack_multiplier = 2.3

        self.aggro_range = 120 
        self.is_aggro = False  

        self.locked_view = None
        
        ghoul_data = ESD["ghoul"]
        
        def load_scaled(path):
            img = pygame.image.load(path).convert_alpha()
            w, h = img.get_size()
            return pygame.transform.scale(img, (int(w * scale), int(h * scale)))

        self.sprites = {
            "front": {
                "stand": load_scaled(ghoul_data["f_stand"]),
                "walk": [load_scaled(ghoul_data["f_walk1"]), load_scaled(ghoul_data["f_walk2"])],
                "attack": load_scaled(ghoul_data["f_attack"]),
                "throw": load_scaled(ghoul_data["f_throw"]),
                "dash": [load_scaled(ghoul_data["f_dash1"]), load_scaled(ghoul_data["f_dash2"])]
            },
            "side": {
                "stand": load_scaled(ghoul_data["s_stand"]),
                "walk": [load_scaled(ghoul_data["s_walk1"]), load_scaled(ghoul_data["s_walk2"])],
                "attack": load_scaled(ghoul_data["s_attack"]),
                "throw": load_scaled(ghoul_data["s_throw"]),
                "dash": [load_scaled(ghoul_data["s_dash1"]), load_scaled(ghoul_data["s_dash2"])]
            },
            "back": {
                "stand": load_scaled(ghoul_data["b_stand"]),
                "walk": [load_scaled(ghoul_data["b_walk1"]), load_scaled(ghoul_data["b_walk2"])],
                "attack": load_scaled(ghoul_data["b_attack"]),
                "throw": load_scaled(ghoul_data["b_throw"]),
                "dash": [load_scaled(ghoul_data["b_dash1"]), load_scaled(ghoul_data["b_dash2"])]
            }
        }
        
        self.img_hit = load_scaled(ghoul_data["hit"])
        self.img_death = load_scaled(ghoul_data["death"])
        self.projectile_img = ghoul_data["proj"]
        
        self.image = self.sprites["front"]["stand"]
        
        self.current_walk_frame = 0
        self.anim_timer = 0.0
        self.anim_speed = 0.2
        self.hit_timer = 0.0
        self.dash_frame_timer = 0.0

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
        if self.shoot_timer > 0: self.shoot_timer -= dt
        if self.state_timer > 0: self.state_timer -= dt
        if self.hit_timer > 0: self.hit_timer -= dt
        if self.dash_timer > 0: self.dash_timer -= dt
        
        target_angle = math.atan2(dy, dx)
        
        if self.state in ["windup", "attack", "shoot", "dash", "dashing"]:
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

        if self.state == "chase":
            if self.can_see_player(player):
                self.is_aggro = True
                
            if self.is_aggro:
                if 20 < distance < 150 and self.dash_timer <= 0:
                    self.state = "dash"
                    self.state_timer = 0.3
                    self.dash_timer = self.dash_cooldown
                    self.attack_direction = target_angle
                    self.image = sprites["dash"][0]
            
                elif 60 < distance < 125 and self.shoot_timer <= 0:
                    self.state = "shoot"
                    self.state_timer = 0.4
                    self.shoot_timer = self.shoot_cooldown
                    self.attack_direction = target_angle
                    self.image = sprites["throw"]
            
                elif distance <= self.attack_range and self.attack_timer <= 0:
                    self.state = "windup"
                    self.state_timer = self.windup_time
                    self.attack_direction = target_angle
                    self.image = sprites["attack"]
            
                elif distance > self.attack_range:
                    self.anim_timer += dt
                    if self.anim_timer >= self.anim_speed:
                        self.anim_timer = 0.0
                        self.current_walk_frame = (self.current_walk_frame + 1) % 2
                    self.image = sprites["walk"][self.current_walk_frame]
                    self.move_towards(player.x, player.y, self.speed, dt, all_enemies)

        elif self.state == "dash":
            self.image = sprites["dash"][0]
            if self.state_timer <= 0:
                self.state = "dashing"
                self.dash_time_left = self.dash_duration
        
        elif self.state == "dashing":
            self.dash_time_left -= dt
            self.dash_frame_timer += dt
            frame = 0 if self.dash_frame_timer < 0.15 else 1
            self.image = sprites["dash"][frame]
            
            move_x = math.cos(self.attack_direction) * self.dash_speed * dt
            move_y = math.sin(self.attack_direction) * self.dash_speed * dt
            
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
            
            if self.dash_time_left <= 0:
                self.state = "dash_attack"

        elif self.state == "dash_attack":
            dx_attack = player.x - self.x
            dy_attack = player.y - self.y
            angle_to_player = math.atan2(dy_attack, dx_attack)
                
            angle_diff_attack = abs(self.attack_direction - angle_to_player)
            if angle_diff_attack > math.pi:
                angle_diff_attack = 2 * math.pi - angle_diff_attack
                
            if distance <= self.attack_range + 10 and angle_diff_attack < math.pi / 4:
                player.stats.base.take_damage(self.attack_damage * self.dash_attack_multiplier)
                    
            self.state = "recovery"
            self.state_timer = self.recovery_time


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
                self.attack_timer = 1.5

        elif self.state == "shoot":
            self.image = sprites["throw"]
            if self.state_timer <= 0:
                proj = Projectile(self.x, self.y, player.x, player.y, self.projectile_img)
                proj.effect = "poison"
                proj.speed = 250
                self.projectiles.append(proj)
                self.state = "chase"

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