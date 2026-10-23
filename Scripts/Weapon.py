import pygame
from Settings import *
from Objects_Archive import WSD

class Weapon:
    def __init__(self):
        self.frames = []
        for path in WSD["sword"]:
            img = pygame.image.load(path).convert_alpha()
            w, h = img.get_size()
            scale = (height * 0.95) / h
            self.frames.append(pygame.transform.scale(img, (int(w * scale), int(h * scale))))

        self.current_frame = 0
        self.timer = 0.0
        self.is_attacking = False
        self.is_reloading = False
        
        self.x = 440
        self.y = 40

    def attack(self):
        if not self.is_attacking and not self.is_reloading:
            self.is_attacking = True
            self.current_frame = 1
            self.timer = 0.0
            return True
        return False

    def update(self, dt):
        if self.is_attacking:
            self.timer += dt
            if self.timer >= frame_duration:
                self.timer = 0.0
                self.current_frame += 1
                
                if self.current_frame >= len(self.frames):
                    self.current_frame = 0
                    self.is_attacking = False
                    self.is_reloading = True  
                    self.timer = 0.0
        
        if self.is_reloading:
            self.timer += dt
            if self.timer >= reload_time:
                self.is_reloading = False

    def draw(self, screen):
        current_img = self.frames[self.current_frame]
        screen.blit(current_img, (self.x, self.y))

    def reset_animation(self):
        self.current_frame = 0
        self.timer = 0.0
        self.is_attacking = False