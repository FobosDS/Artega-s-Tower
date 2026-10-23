import pygame
from Settings import *
from Player_Control import Player
from Objects import Sprite, Interactive_Sprite
from Objects_Archive import ESD, ISD, SSD
from Interactions import Interaction_Manager
from Renderer import render_scene
from Controls import Input_Manager
from Weapon import Weapon
from UI import draw_hud

def main():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Artega's Tower")
    
    #endless mouse
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
    weapon = Weapon(player.stats)

    interaction_manager = Interaction_Manager()
    interaction_manager.interactive_objects = interactive_objects_list

    input = Input_Manager(player, interaction_manager, weapon)

    running = True
    while running:
        dt = min(clock.tick(FPS) / 1000, 0.05)

        if not input.handle_events(pygame.event.get()):
            running = False
        
        player.movement(dt, all_objects_list)
        
        player.stats.update_effects(dt)
        weapon.update(dt, (player.x, player.y), player.is_sprinting)

        render_scene(player, screen, objects_list, interactive_objects_list)
        weapon.draw(screen)
        draw_hud(screen, player.stats)

        pygame.display.flip()

    #release mouse
    pygame.event.set_grab(False)
    pygame.mouse.set_visible(True)

    pygame.quit()

main()