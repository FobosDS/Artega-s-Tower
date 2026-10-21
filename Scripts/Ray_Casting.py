import pygame
import math
from Settings import *
from Map import create_map


map = create_map()


def ray_casting(player, screen):

    x, y = player.x, player.y

    angle = player.angle - halfFov

    for ray in range(numRays):
        sin_a = math.sin(angle)
        cos_a = math.cos(angle)
        if abs(sin_a) < 1e-9:
            sin_a = 1e-9
        if abs(cos_a) < 1e-9:
            cos_a = 1e-9

        depth = maxDepth
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

        depth *= math.cos(player.angle - angle)
        if depth < 0.0001:
            depth = 0.0001

        wall_h = min(projCoeff / depth, height * 20)
        top = half_height - wall_h / 2

        wall_x = ray * scale

        shade = max(0.15, 1.0 - depth / maxDepth)
        color = (int(light_gray[0] * shade), int(light_gray[1] * shade), int(light_gray[2] * shade))

        pygame.draw.rect(screen, color, (wall_x, top, scale + 1, wall_h))

        angle += deltaAngle