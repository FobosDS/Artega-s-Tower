import pygame
from Settings import *

class Input_Manager:
    def __init__(self, player, interaction_manager, weapon):
        self.player = player
        self.interaction_manager = interaction_manager
        self.weapon = weapon

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == interact_key:
                    self.interaction_manager.handle_input(self.player.rect, {interact_key: True})
                if event.key == potion_key:
                    self.player.stats.use_potion()
                if event.key == scroll_key:
                    self.player.stats.use_scroll()
                if event.key == damage_key:
                    self.player.stats.effects.apply_poison()
                    self.player.stats.effects.apply_paralysis()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.weapon.attack():
                        print("Удар")
                elif event.button == 3:
                    if self.weapon.block():
                        print("Блок")

        return True