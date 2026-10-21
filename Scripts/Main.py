import pygame
from Settings import *
from Player_Control import Player
from Ray_Casting import ray_casting
from Sprites import Sprite

def main():

    pygame.init()

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Artega's Tower")

    #endless mouse
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)

    clock = pygame.time.Clock()

    sprites_list = [
        Sprite(600, 400, sprites_folder + "pedestal.png", 0.6),
    ]

    player = Player()

    running = True

    while running:

        dt = min(clock.tick(FPS) / 1000, 0.05)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        print(round(clock.get_fps()))

        player.movement(dt)
        screen.fill(black)

        pygame.draw.rect(screen, light_black, (0, 0, width, half_height))
        pygame.draw.rect(screen, dark_gray, (0, half_height, width, half_height))

        ray_casting(player, screen, sprites_list)  

        pygame.display.flip()

        clock.tick(FPS)
main()    



