import pygame
import math
from Settings import *
from Map import create_map
from Collisions import check_collision

class Player:
    def __init__(self):
        self.x, self.y = pl_pos
        self.angle = pl_angle
        self.rect = pygame.Rect(pl_rect)
        self.map = create_map()
        self.dash_time_left = 0.0
        self.dash_cooldown_left = 0.0
        self.dash_dir = pygame.Vector2(0, 0)

    def collides(self, test_rect, objects):
        return check_collision(test_rect, self.map, objects)

    def move_with_collision(self, dx, dy, objects):
        if dx != 0:
            self.x += dx
            self.rect.center = (self.x, self.y)
            if self.collides(self.rect, objects):
                self.x -= dx
                self.rect.center = (self.x, self.y)
        if dy != 0:
            self.y += dy
            self.rect.center = (self.x, self.y)
            if self.collides(self.rect, objects):
                self.y -= dy
                self.rect.center = (self.x, self.y)

    def rotate_to_mouse(self):
        dx, _ = pygame.mouse.get_rel()
        self.angle += dx * mouse_sensitivity
        self.angle %= 2 * math.pi

    def dash(self, dt, move, forward):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.dash_cooldown_left <= 0 and self.dash_time_left <= 0:
            self.dash_dir = move if move.length_squared() > 0 else forward
            self.dash_time_left = dash_duration
            self.dash_cooldown_left = dash_cooldown
        if self.dash_time_left > 0:
            self.dash_time_left = max(0.0, self.dash_time_left - dt)
            speed = pl_speed * dash_speed_multiplier
            dx = self.dash_dir.x * speed * dt
            dy = self.dash_dir.y * speed * dt
        else:
            speed = pl_speed
            if keys[pygame.K_LSHIFT]:
                speed *= sprint_speed_multiplier
            dx = move.x * speed * dt
            dy = move.y * speed * dt
        if self.dash_cooldown_left > 0:
            self.dash_cooldown_left = max(0.0, self.dash_cooldown_left - dt)
        return dx, dy

    def movement(self, dt, objects):
        self.rotate_to_mouse()
        keys = pygame.key.get_pressed()
        cos_a = math.cos(self.angle)
        sin_a = math.sin(self.angle)
        forward = pygame.Vector2(cos_a, sin_a)
        right = pygame.Vector2(-sin_a, cos_a)
        move = pygame.Vector2(0, 0)
        if keys[pygame.K_w]: move += forward
        if keys[pygame.K_s]: move -= forward
        if keys[pygame.K_d]: move += right
        if keys[pygame.K_a]: move -= right
        if move.length_squared() > 0:
            move = move.normalize()
        dx, dy = self.dash(dt, move, forward)
        self.move_with_collision(dx, dy, objects)