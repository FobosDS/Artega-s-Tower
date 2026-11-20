import pygame
from Settings import *
from Player_Control import Player
from Weapon import Weapon
from UI import create_icons, load_interface, MainMenu, PauseMenu, IntroScene
from Controls import Input_Manager
from Interactions import Interaction_Manager
from Game_Manager import Game
from Sound_Manager import Sound_Manager

def load_game(player):
    import json, os
    if not os.path.exists(save_file):
        return
    with open(save_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    player.stats.base.hp = data["hp"]
    player.stats.base.sp = data["sp"]
    player.stats.base.gold = data["gold"]
    player.stats.base.potions = data["potions"]
    player.stats.base.scrolls = data["scrolls"]
    player.stats.combat.whetstones = data["whetstones"]
    player.stats.combat.weapon_level = data["weapon_level"]
    player.stats.combat.default_attack_damage = base_attack_damage * data["weapon_level"]
    player.stats.combat.attack_damage = player.stats.combat.default_attack_damage
    player.stats.combat.durability = data["durability"]
    player.stats.base.hp_level = data["hp_level"]
    player.stats.base.sp_level = data["sp_level"]
    player.stats.base.max_hp = base_hp * data["hp_level"]
    player.stats.base.max_sp = base_sp + data["sp_level"] * sp_bonus
    player.stats.base.rings = list(data["rings"])
    player.stats.base.dark_shards = data["dark_shards"]
    player.stats.is_chest_key1 = data["is_chest_key1"]
    player.stats.is_chest_key2 = data["is_chest_key2"]
    player.stats.is_floor_key = data["is_floor_key"]
    player.stats.current_floor = data["floor"]

def run_game(screen, sound_manager, load_save=False):
    
    player = Player()
    if load_save:
        load_game(player)
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
    input_manager.pause_menu = PauseMenu(screen)
    weapon.enemies = game.enemy_manager.enemies

    if load_save:
        game.apply_world_state()

    clock = pygame.time.Clock()
    running = True

    while running:
        dt = min(clock.tick(FPS) / 1000, 0.05)
        result = input_manager.handle_events(pygame.event.get())
        if result is False:
            return "quit"
        if result == "exit_to_menu":
            return "menu"

        paused = input_manager.pause_menu.visible
        if not paused:
            game.update(dt)

        game.draw()
        input_manager.pause_menu.draw()
        pygame.display.flip()

    return "quit"

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

    menu = MainMenu(screen, sound_manager)

    load_save = False

    in_menu = True

    while in_menu:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            result = menu.handle_event(event)
            if result == "start":
                in_menu = False
                load_save = False
            elif result == "load":
                in_menu = False
                load_save = True 
            elif result == "quit":
                pygame.quit()
                return
        menu.draw()
        pygame.display.flip()

    sound_manager.set_floor_music(1)
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)

    while True:
        outcome = run_game(screen, sound_manager, load_save=load_save)
        load_save = False
        if outcome == "menu":
            sound_manager.set_floor_music(0)
            pygame.mouse.set_visible(True)
            pygame.event.set_grab(False)
            menu = MainMenu(screen, sound_manager)
            in_menu = True
            while in_menu:
                clock.tick(FPS)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    result = menu.handle_event(event)
                    if result == "start":
                        in_menu = False
                        load_save = False
                    elif result == "load":
                        in_menu = False
                        load_save = True
                    elif result == "quit":
                        pygame.quit()
                        return
                menu.draw()
                pygame.display.flip()
            pygame.mouse.set_visible(False)
            pygame.event.set_grab(True)
            sound_manager.set_floor_music(1)
        else:
            break

    pygame.event.set_grab(False)
    pygame.mouse.set_visible(True)
    pygame.quit()

main()