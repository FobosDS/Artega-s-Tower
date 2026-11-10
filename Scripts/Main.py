import pygame
from Settings import *
from Player_Control import Player
from Weapon import Weapon
from UI import create_icons, load_interface
from Controls import Input_Manager
from Interactions import Interaction_Manager
from Game_Manager import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Artega's Tower")

    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)
    clock = pygame.time.Clock()

    player = Player()
    weapon = Weapon(player.stats)
    interface = load_interface(interface_scale)
    icons = create_icons()
    
    interaction_manager = Interaction_Manager()
    input_manager = Input_Manager(player, interaction_manager, weapon)
    
    game = Game(screen, player, weapon, interface, icons)

    interaction_manager.interactive_objects = game.interactive_objects
    
    weapon.enemies = game.enemy_manager.enemies

    running = True
    
    while running:
        dt = min(clock.tick(FPS) / 1000, 0.05)

        if not input_manager.handle_events(pygame.event.get()):
            running = False
        
        game.update(dt)
        game.draw()

        pygame.display.flip()

    pygame.event.set_grab(False)
    pygame.mouse.set_visible(True)
    pygame.quit()

main()
