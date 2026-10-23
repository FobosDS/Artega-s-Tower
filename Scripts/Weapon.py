import pygame
import math
from Settings import *
from Objects_Archive import WSD

class Weapon:
    def __init__(self, player_stats):
        #load attack frames
        self.attack_frames = []
        for path in WSD["sword_attack"]:
            img = pygame.image.load(path).convert_alpha()
            w, h = img.get_size()
            scale = (height * weapon_scale) / h
            self.attack_frames.append(pygame.transform.scale(
                img, (int(w * scale), int(h * scale))
            ))

        #load block frame
        block_path = WSD["sword_block"]
        block_img = pygame.image.load(block_path).convert_alpha()
        w, h = block_img.get_size()
        scale = (height * weapon_scale) / h
        self.block_frame = pygame.transform.scale(
            block_img, (int(w * scale), int(h * scale))
        )

        self.current_frame = 0
        self.attack_timer = 0.0
        self.block_timer = 0.0
        self.reload_timer = 0.0

        self.is_attacking = False
        self.is_blocking = False
        self.is_reloading = False

        self.x = weapon_base_x
        self.y = weapon_base_y
        self.last_position = None

        self.block_active = False

        self.phase = 0.0
        self.walk_amp = 0.0
        self.target_amp = 0.0

        self.player_stats = player_stats

    def attack(self):
        if not self.is_attacking and not self.is_blocking and not self.is_reloading:
            if self.player_stats.base.use_sp(sp_cost_attack):
                self.is_attacking = True
                self.current_frame = 0
                self.attack_timer = 0.0
                return True
        return False

    def block(self):
        if not self.is_attacking and not self.is_blocking and not self.is_reloading:
            if self.player_stats.base.use_sp(sp_cost_block):
                self.is_blocking = True
                self.block_active = True
                self.block_timer = 0.0
            return True
        return False

    def update(self, dt, pl_pos, is_sprinting=False):
        #swing
        if self.last_position is None:
            self.last_position = pl_pos
        dx = pl_pos[0] - self.last_position[0]
        dy = pl_pos[1] - self.last_position[1]
        is_moving = (dx*dx + dy*dy) > 0.25
        self.last_position = pl_pos

        self.target_amp = 1.0 if is_moving else 0.0
        self.walk_amp += (self.target_amp - self.walk_amp) * min(1.0, weapon_amp_lerp * dt)

        if self.walk_amp > 0.01:
            freq = weapon_walk_freq * (weapon_sprint_freq_multiplier if is_sprinting else 1.0)
            self.phase += freq * dt * self.walk_amp
        else:
            self.phase = 0.0

        x_offset = math.sin(self.phase) * weapon_max_swing_x * self.walk_amp
        y_offset = math.cos(self.phase * 2.0) * weapon_max_swing_y * self.walk_amp * 0.5

        self.x = weapon_base_x + x_offset
        self.y = weapon_base_y + y_offset

        #attack
        if self.is_attacking:
            self.attack_timer += dt
            if self.attack_timer >= animation_duration:
                self.attack_timer = 0.0
                self.current_frame += 1
                if self.current_frame >= len(self.attack_frames):
                    self.current_frame = 0
                    self.is_attacking = False
                    self.is_reloading = True
                    self.reload_timer = 0.0

        #block
        if self.is_blocking:
            self.block_timer += dt
            if self.block_timer >= block_duration:
                self.is_blocking = False
                self.block_active = False
                self.is_reloading = True
                self.reload_timer = 0.0

        #reload
        if self.is_reloading:
            self.reload_timer += dt
            if self.reload_timer >= reload_time:
                self.is_reloading = False

    def draw(self, screen):
        if self.is_attacking:
            current_img = self.attack_frames[self.current_frame]
        elif self.is_blocking:
            current_img = self.block_frame
        else:
            current_img = self.attack_frames[0]
        screen.blit(current_img, (self.x, self.y))

    def reset_animation(self):
        self.current_frame = 0
        self.attack_timer = 0.0
        self.block_timer = 0.0
        self.reload_timer = 0.0
        self.is_attacking = False
        self.is_blocking = False
        self.is_reloading = False
        self.block_active = False

    def check_block(self):
        return self.block_active