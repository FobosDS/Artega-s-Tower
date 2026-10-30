import pygame
import math
from Settings import *
from Game_Manager import MapManager
from Sprites_Archive import WTD

z_buffer = [0.0] * numRays

map_manager = MapManager()
walls_rects = map_manager.walls
walls_grid = map_manager.walls_grid

textures = {}
for symbol, path in WTD.items():
    try:
        img = pygame.image.load(path).convert()
        img = pygame.transform.scale(img, (texture_size, texture_size))
        textures[symbol] = img
    except Exception as e:
        print(f"Ошибка текстуры {symbol}: {e}")
        textures[symbol] = None

def render_background(screen):
    pygame.draw.rect(screen, light_black, (0, 0, width, half_height))
    pygame.draw.rect(screen, dark_gray, (0, half_height, width, half_height))

def render_walls(player, screen):
    x, y = player.x, player.y
    
    for ray in range(numRays):
        ray_angle = player.angle - halfFov + ray * deltaAngle
        
        ray_dir_x = math.cos(ray_angle)
        ray_dir_y = math.sin(ray_angle)
        
        if abs(ray_dir_x) < 1e-9: ray_dir_x = 1e-9
        if abs(ray_dir_y) < 1e-9: ray_dir_y = 1e-9

        map_x = int(x // tile_size)
        map_y = int(y // tile_size)

        delta_dist_x = abs(tile_size / ray_dir_x)
        delta_dist_y = abs(tile_size / ray_dir_y)

        if ray_dir_x < 0:
            step_x = -1
            side_dist_x = (x - map_x * tile_size) / abs(ray_dir_x)
        else:
            step_x = 1
            side_dist_x = ((map_x + 1) * tile_size - x) / ray_dir_x

        if ray_dir_y < 0:
            step_y = -1
            side_dist_y = (y - map_y * tile_size) / abs(ray_dir_y)
        else:
            step_y = 1
            side_dist_y = ((map_y + 1) * tile_size - y) / ray_dir_y

        hit = False
        side = 0
        hit_symbol = "H"
        
        while not hit:
            if side_dist_x < side_dist_y:
                side_dist_x += delta_dist_x
                map_x += step_x
                side = 0
            else:
                side_dist_y += delta_dist_y
                map_y += step_y
                side = 1

            if 0 <= map_y < len(walls_grid) and 0 <= map_x < len(walls_grid[0]):
                symbol = walls_grid[map_y][map_x]
                if symbol in textures:
                    hit = True
                    hit_symbol = symbol
            else:
                hit = True
                hit_symbol = "H"
            
            #for wall in walls_rects:
            #    if wall.collidepoint(map_x * tile_size, map_y * tile_size):
            #        hit = True
            #        break
            #if map_x < 0 or map_x >= 24 or map_y < 0 or map_y >= 16:
            #    hit = True
            #    side_dist_x = maxDepth
            #    break

        pos_x = x / tile_size
        pos_y = y / tile_size

        if side == 0:
            perp_dist = (map_x - pos_x + (1 - step_x) / 2) / ray_dir_x
        else:
            perp_dist = (map_y - pos_y + (1 - step_y) / 2) / ray_dir_y

        perp_dist = max(0.1, perp_dist)
        
        z_buffer[ray] = perp_dist

        wall_h = min(height / perp_dist, height * 3)
        top = half_height - wall_h / 2
        wall_x = ray * scale

        wall_texture = textures.get(hit_symbol)
        
        if wall_texture:
            if side == 0:
                wall_x_hit = pos_y + perp_dist * ray_dir_y
            else:
                wall_x_hit = pos_x + perp_dist * ray_dir_x
            
            wall_x_hit -= int(wall_x_hit)
            tex_x = int(wall_x_hit * texture_size)
            tex_x = max(0, min(texture_size - 1, tex_x))

            texture_slice = wall_texture.subsurface((tex_x, 0, 1, texture_size))
            texture_slice = pygame.transform.scale(texture_slice, (int(scale) + 1, int(wall_h)))
            
            shade = max(0.15, 1.0 - perp_dist / maxDepth)
            if side == 1: shade *= 0.7
            
            if shade < 0.99:
                dark_surface = pygame.Surface(texture_slice.get_size(), pygame.SRCALPHA)
                dark_surface.fill((0, 0, 0, int(255 * (1 - shade))))
                texture_slice.blit(dark_surface, (0, 0))
            
            screen.blit(texture_slice, (wall_x, top))
        else:
            shade = max(0.15, 1.0 - perp_dist / maxDepth)
            color = (int(light_gray[0] * shade), int(light_gray[1] * shade), int(light_gray[2] * shade))
            pygame.draw.rect(screen, color, (wall_x, top, scale + 1, wall_h))

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

        transform_y_cells = transform_y / tile_size

        sprite_screen_x = int((width / 2) * (1 + transform_x / transform_y))
        
        sprite_height = abs(int((height * sprite.scale * sprites_scale) / transform_y))
        if sprite_height > height: 
            sprite_height = height
        if sprite_height < 2: 
            continue
            
        sprite_width = int(sprite_height * sprite.aspect)

        draw_start_y = half_height - sprite_height // 2
        draw_start_y += int(sprite_height * 0.2)
        draw_start_x = -sprite_width // 2 + sprite_screen_x

        center_stripe = max(0, min(width - 1, sprite_screen_x))
        ray_index = int(center_stripe / scale)
        
        if 0 <= ray_index < numRays and transform_y_cells < z_buffer[ray_index]:
            scaled = pygame.transform.scale(sprite.image, (sprite_width, sprite_height))
            screen.blit(scaled, (draw_start_x, draw_start_y))

def render_scene(player, screen, objects, interactive_objects, enemies, projectile_manager):
    screen.fill(black)
    render_background(screen)
    render_walls(player, screen)
    
    all_sprites = objects + interactive_objects + enemies + projectile_manager.projectiles
    
    render_sprites(player, screen, all_sprites)