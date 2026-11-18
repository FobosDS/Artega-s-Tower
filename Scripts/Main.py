import pygame
from Settings import *
from Player_Control import Player
from Weapon import Weapon
from UI import create_icons, load_interface, MainMenu, IntroScene
from Controls import Input_Manager
from Interactions import Interaction_Manager
from Game_Manager import Game
from Sound_Manager import Sound_Manager

def run_game(screen, sound_manager):
    
    player = Player()
    weapon = Weapon(player.stats)
    interface = load_interface(interface_scale)
    icons = create_icons()

    interaction_manager = Interaction_Manager()
    input_manager = Input_Manager(player, interaction_manager, weapon)

    sound_manager.set_floor_music(player.stats.current_floor)

    game = Game(screen, player, weapon, interface, icons, interaction_manager, sound_manager)
    interaction_manager.interactive_objects = game.interactive_objects
    interaction_manager.give_ring = game.give_ring_to_player
    input_manager.tab_overlay = game.tab_overlay
    weapon.enemies = game.enemy_manager.enemies

    clock = pygame.time.Clock()
    running = True
    while running:
        dt = min(clock.tick(FPS) / 1000, 0.05)
        if not input_manager.handle_events(pygame.event.get()):
            running = False
        game.update(dt)
        game.draw()
        pygame.display.flip()


def main():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Artega's Tower")
    
    pygame.mouse.set_visible(True)
    pygame.event.set_grab(False)

    sound_manager = Sound_Manager()
    intro = IntroScene(screen)

    clock = pygame.time.Clock()

    while not intro.done:
        dt = min(clock.tick(FPS) / 1000, 0.05)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            intro.handle_event(event)
        intro.update(dt)
        intro.draw()
        pygame.display.flip()

    sound_manager.set_floor_music(0)    

    menu = MainMenu(screen)

    in_menu = True
    
    while in_menu:
        dt = min(clock.tick(FPS) / 1000, 0.05)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_menu = False
                break
            result = menu.handle_event(event)
            if result == "start":
                in_menu = False
            elif result == "quit":
                in_menu = False
                pygame.quit()
                return
        menu.draw()
        pygame.display.flip()

    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)

    run_game(screen, sound_manager)

    pygame.event.set_grab(False)
    pygame.mouse.set_visible(True)
    pygame.quit()


main()