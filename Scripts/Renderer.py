import pygame
import math
from Settings import *
from Map import create_map

map = create_map()
z_buffer = [0.0] * numRays

def render_walls(player, screen):
    #render walls
    x, y = player.x, player.y
    angle = player.angle - halfFov
    for ray in range(numRays):
        sin_a = math.sin(angle)
        cos_a = math.cos(angle)
        if abs(sin_a) < 1e-9: sin_a = 1e-9
        if abs(cos_a) < 1e-9: cos_a = 1e-9

        depth = maxDepth
        #find wall hit
        for wall in map:
            tx1 = (wall.left - x) / cos_a
            tx2 = (wall.right - x) / cos_a
            ty1 = (wall.top - y) / sin_a
            ty2 = (wall.bottom - y) / sin_a
            t_enter = max(min(tx1, tx2), min(ty1, ty2))
            t_exit = min(max(tx1, tx2), max(ty1, ty2))
            if t_enter <= t_exit and t_exit >= 0:
                t = t_enter if t_enter > 0 else t_exit
                if t < depth:
                    depth = t

        #fish-eye correction
        depth *= math.cos(player.angle - angle)
        if depth < 0.0001: depth = 0.0001
        z_buffer[ray] = depth

        #height and color
        wall_h = min(projCoeff / depth, height * 20)
        top = half_height - wall_h / 2
        wall_x = ray * scale
        shade = max(0.15, 1.0 - depth / maxDepth)
        color = (int(light_gray[0] * shade), int(light_gray[1] * shade), int(light_gray[2] * shade))
        pygame.draw.rect(screen, color, (wall_x, top, scale + 1, wall_h))
        angle += deltaAngle

def render_sprites(player, screen, sprites):
    #render sprites
    sorted_sprites = sorted(sprites, key=lambda s: (s.x - player.x)**2 + (s.y - player.y)**2, reverse=True)
    dir_x = math.cos(player.angle)
    dir_y = math.sin(player.angle)
    plane_x = -dir_y * math.tan(halfFov)
    plane_y = dir_x * math.tan(halfFov)

    for sprite in sorted_sprites:
        #camera transform
        sprite_x = sprite.x - player.x
        sprite_y = sprite.y - player.y
        inv_det = 1.0 / (plane_x * dir_y - dir_x * plane_y)
        transform_x = inv_det * (dir_y * sprite_x - dir_x * sprite_y)
        transform_y = inv_det * (-plane_y * sprite_x + plane_x * sprite_y)
        if transform_y <= 0.1: continue

        #position and size
        sprite_screen_x = int((width / 2) * (1 + transform_x / transform_y))
        sprite_height = abs(int((projCoeff * sprite.scale * sprites_scale) / transform_y))
        if sprite_height > height * 2: sprite_height = height * 2
        if sprite_height < 2: continue
        sprite_width = int(sprite_height * sprite.aspect)

        #align to floor
        wall_h = abs(int(projCoeff / transform_y))
        floor_level = half_height + wall_h // 2
        draw_start_y = floor_level - sprite_height
        draw_start_x = -sprite_width // 2 + sprite_screen_x

        #Z-buffer check
        center_stripe = max(0, min(width - 1, sprite_screen_x))
        ray_index = int(center_stripe / scale)
        if 0 <= ray_index < numRays and transform_y < z_buffer[ray_index]:
            scaled = pygame.transform.scale(sprite.image, (sprite_width, sprite_height))
            screen.blit(scaled, (draw_start_x, draw_start_y))

def render_scene(player, screen, objects, interactive_objects):
    render_walls(player, screen)
    render_sprites(player, screen, objects + interactive_objects)