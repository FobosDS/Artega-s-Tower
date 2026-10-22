import pygame
import math
from Settings import *

z_buffer = [0.0] * numRays

class Sprite:
    def __init__(self, x, y, image_path, scale=1.0, collision_radius=0):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image_path).convert_alpha()
        self.scale = scale
        
        self.img_w, self.img_h = self.image.get_size()
        self.aspect = self.img_w / self.img_h
        
        self.rect = pygame.Rect(
            self.x - collision_radius,
            self.y - collision_radius,
            collision_radius * 2,
            collision_radius * 2
        )

def check_object_collision(test_rect, sprites):
    for sprite in sprites:
        if test_rect.colliderect(sprite.rect):
            return True
    return False


def render_sprites(player, screen, sprites):

    sorted_sprites = sorted(sprites, key=lambda s: (s.x - player.x)**2 + (s.y - player.y)**2, reverse=True)

    dir_x = math.cos(player.angle)
    dir_y = math.sin(player.angle)
    plane_x = -dir_y * math.tan(halfFov)
    plane_y = dir_x * math.tan(halfFov)

    for sprite in sorted_sprites:
        sprite_x = sprite.x - player.x
        sprite_y = sprite.y - player.y

        inv_det = 1.0 / (plane_x * dir_y - dir_x * plane_y)
        transform_x = inv_det * (dir_y * sprite_x - dir_x * sprite_y)
        transform_y = inv_det * (-plane_y * sprite_x + plane_x * sprite_y)

        if transform_y <= 0.1:
            continue

        sprite_screen_x = int((width / 2) * (1 + transform_x / transform_y))
        
        sprite_height = abs(int((projCoeff * sprite.scale * sprites_scale) / transform_y))

        if sprite_height > height * 2:
            sprite_height = height * 2
        if sprite_height < 2:
            continue
            
        sprite_width = int(sprite_height * sprite.aspect)

        wall_height_at_sprite = abs(int(projCoeff / transform_y))
        floor_level = half_height + wall_height_at_sprite // 2
        draw_start_y = floor_level - sprite_height

        draw_start_x = -sprite_width // 2 + sprite_screen_x

        center_stripe = max(0, min(width - 1, sprite_screen_x))
        center_ray_index = int(center_stripe / scale)
        
        if 0 <= center_ray_index < numRays and transform_y < z_buffer[center_ray_index]:
            scaled_image = pygame.transform.scale(sprite.image, (sprite_width, sprite_height))
            screen.blit(scaled_image, (draw_start_x, draw_start_y))
