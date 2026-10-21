import pygame
import math
from Settings import *
from Map import drawed_map

SHADE_LEVELS = 32
color_cache = []
for k in range(SHADE_LEVELS + 1):
    t = k / SHADE_LEVELS
    s = max(0.15, (1.0 - t) ** 0.5)
    color_cache.append((
        int(light_gray[0] * s),
        int(light_gray[1] * s),
        int(light_gray[2] * s),
    ))

ray_offsets = [-halfFov + i * deltaAngle for i in range(numRays)]
ray_cos = [math.cos(a) for a in ray_offsets]
ray_sin = [math.sin(a) for a in ray_offsets]


def is_wall(map_x, map_y):

    if map_y < 0 or map_y >= len(drawed_map):
        return True
    row = drawed_map[map_y]
    if map_x < 0 or map_x >= len(row):
        return True
    return row[map_x] == "H"


def ray_casting_DDA(player, screen):

    draw_rect = pygame.draw.rect
    n = numRays
    maxD = maxDepth
    h = height
    hh = half_height
    sc = scale
    rc = ray_cos
    rs = ray_sin
    cc = color_cache
    levels = SHADE_LEVELS

    x, y = player.x, player.y
    cos_p = math.cos(player.angle)
    sin_p = math.sin(player.angle)

    for ray in range(n):
        ox = rc[ray]
        oy = rs[ray]
        
        dx = ox * cos_p - oy * sin_p
        dy = ox * sin_p + oy * cos_p
        
        if abs(dx) < 1e-9: dx = 1e-9
        if abs(dy) < 1e-9: dy = 1e-9

        map_x = int(x // tile_size)
        map_y = int(y // tile_size)

        delta_dist_x = abs(tile_size / dx)
        delta_dist_y = abs(tile_size / dy)

        if dx < 0:
            step_x = -1
            side_dist_x = (x - map_x * tile_size) / abs(dx)
        else:
            step_x = 1
            side_dist_x = ((map_x + 1) * tile_size - x) / dx

        if dy < 0:
            step_y = -1
            side_dist_y = (y - map_y * tile_size) / abs(dy)
        else:
            step_y = 1
            side_dist_y = ((map_y + 1) * tile_size - y) / dy

        while True:
            if side_dist_x < side_dist_y:
                dist = side_dist_x
                side_dist_x += delta_dist_x
                map_x += step_x
                side = 0
            else:
                dist = side_dist_y
                side_dist_y += delta_dist_y
                map_y += step_y
                side = 1

            if is_wall(map_x, map_y) or dist > maxD:
                break

        perp_dist = dist * ox 
        if perp_dist < 0.0001:
            perp_dist = 0.0001

        wall_h = (h / perp_dist) * (tile_size / 1.5)
        
        if wall_h > h * 20:
            wall_h = h * 20
            
        top = hh - wall_h * 0.5

        level = int((perp_dist / maxD) * levels)
        if level < 0:
            level = 0
        elif level > levels:
            level = levels
            
        color = cc[level]

        draw_rect(screen, color, (ray * sc, top, sc + 1, wall_h))