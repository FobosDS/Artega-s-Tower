import pygame
from Settings import *

def draw_circle_bar(screen, cx, cy, radius, value, max_value, fill_color, bg_color, hl_color, hl_offset_x):
    #background
    pygame.draw.circle(screen, bg_color, (cx, cy), radius)

    #sphere
    if max_value > 0 and value > 0:
        ratio = min(1.0, value / max_value)
        current_radius = int(radius * ratio)
        if current_radius > 0:
            pygame.draw.circle(screen, fill_color, (cx, cy), current_radius)

    #highlight
    hl_x = cx + int(radius * hl_offset_x)
    hl_y = cy - int(radius * 0.35)
    hl_radius = max(1, int(radius * 0.18))
    pygame.draw.circle(screen, hl_color, (hl_x, hl_y), hl_radius)

def draw_hud(screen, stats):
    #hp
    draw_circle_bar(
        screen, cx=hud_x, cy=hud_y,
        radius=hud_radius,
        value=stats.base.hp, max_value=stats.base.max_hp,
        fill_color=hp_red, bg_color=(80, 0, 0),
        hl_color=hp_highlight, hl_offset_x=0.35
    )

    #sp
    draw_circle_bar(
        screen, cx=hud_x + hud_spacing, cy=hud_y,
        radius=hud_radius,
        value=stats.base.sp, max_value=stats.base.max_sp,
        fill_color=sp_green, bg_color=(0, 80, 0),
        hl_color=sp_highlight, hl_offset_x=-0.35
    )