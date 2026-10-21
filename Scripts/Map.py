import pygame
from Settings import tile_size
drawed_map = [
"HHHHHHHHHHHHHHHHHHHHHHHH",
"H......H.H.H...........H",
"H..H...H...H......H....H",
"H..H..............H....H",
"H..HH......H...........H",
"H......HH..H......HHH..H",
"H..H...H...H........H..H",
"HHHHHHHHHH.....H....HHHH",
"H......H.......H.......H",
"H......H...............H",
"H..H...H...HHHH........H",
"H..H..........H....HHHHH",
"H..HH......HHHH........H",
"H......H...H...........H",
"H..H...H...H...........H",
"HHHHHHHHHHHHHHHHHHHHHHHH"
]

def create_map(tile = tile_size):
    real_map = []
    for row, line in enumerate(drawed_map):
        for col, ch in enumerate(line):
            if ch == "H":
                real_map.append(pygame.Rect(col * tile, row * tile, tile, tile))
    return real_map
