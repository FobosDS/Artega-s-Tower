import pygame
from Settings import *
from Player_Control import Player
from Ray_Casting import ray_casting
from Objects import Sprite
from Objects_Archive import ESD, ISD, SSD
from Interactions import Interaction_Manager, Interactive_Sprite
def main():

    pygame.init()

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Artega's Tower")

    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)

    clock = pygame.time.Clock()

    objects_list = [
        Sprite(*ESD["artega_states"]["cast"])
    ]

    interactive_objects_list = [
        Interactive_Sprite(*ISD["pedestal"])
    ]

    all_objects_list = objects_list + interactive_objects_list

    player = Player()
    interaction_manager = Interaction_Manager()

    player.objects = all_objects_list
    interaction_manager.interactive_objects = interactive_objects_list

    running = True

    while running:

        dt = min(clock.tick(FPS) / 1000, 0.05)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_e:
                    interaction_manager.handle_input(player.rect, {pygame.K_e: True})

        player.movement(dt)
        screen.fill(black)
        
        pygame.draw.rect(screen, light_black, (0, 0, width, half_height))
        pygame.draw.rect(screen, dark_gray, (0, half_height, width, half_height))

        ray_casting(player, screen, all_objects_list)  

        pygame.display.flip()

    pygame.event.set_grab(False)
    pygame.mouse.set_visible(True)
    pygame.quit()
        
main()    



