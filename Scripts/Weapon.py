import pygame
from Settings import *
from Objects_Archive import WSD

class Weapon:
    def __init__(self):
        #load attack frames
        self.attack_frames = []
        for path in WSD["sword_attack"]:
            img = pygame.image.load(path).convert_alpha()
            w, h = img.get_size()
            scale = (height * 0.95) / h
            self.attack_frames.append(pygame.transform.scale(
                img, (int(w * scale), int(h * scale))
            ))
            
        #load block frame
        block_path = WSD["sword_block"]
        block_img = pygame.image.load(block_path).convert_alpha()
        w, h = block_img.get_size()
        scale = (height * 0.95) / h
        self.block_frame = pygame.transform.scale(
            block_img, (int(w * scale), int(h * scale))
        )
        
        self.current_frame = 0
        self.timer = 0
        self.is_attacking = False
        self.is_blocking = False
        self.is_reloading = False
        self.reload_time = 0.5
        
        self.x = 440
        self.y = 40
        self.block_active = False
        self.block_timer = 0

    def attack(self):
        if not self.is_attacking and not self.is_blocking and not self.is_reloading:
            self.is_attacking = True
            self.current_frame = 0
            self.timer = 0
            return True
        return False

    def block(self):
        if not self.is_attacking and not self.is_blocking and not self.is_reloading:
            self.is_blocking = True
            self.block_active = True
            self.block_timer = 0
            return True
        return False

    def update(self, dt):
        if self.is_attacking:
            self.timer += dt
            if self.timer >= animation_duration:
                self.timer = 0
                self.current_frame += 1
                
                if self.current_frame >= len(self.attack_frames):
                    self.current_frame = 0
                    self.is_attacking = False
                    self.is_reloading = True
                    self.timer = 0.0
        
        if self.is_blocking:
            self.block_timer += dt
            if self.block_timer >= block_duration:
                self.is_blocking = False
                self.block_active = False
                self.is_reloading = True
        
        if self.is_reloading:
            self.timer += dt
            if self.timer >= self.reload_time:
                self.is_reloading = False
                self.is_blocking = False
                self.is_attacking = False

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
        self.timer = 0.0
        self.is_attacking = False
        self.is_blocking = False
        self.is_reloading = False
        self.block_active = False
        self.block_timer = 0.0

    def check_block(self):
        return self.block_active
