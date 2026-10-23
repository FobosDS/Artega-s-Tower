import pygame

class Input_Manager:
    def __init__(self, player, interaction_manager):
        self.player = player
        self.interaction_manager = interaction_manager

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False

                if event.key == pygame.K_e:
                    self.interaction_manager.handle_input(
                        self.player.rect, {pygame.K_e: True}
                    )

                if event.key == pygame.K_f:
                    self.player.stats.use_potion()

                if event.key == pygame.K_r:
                    self.player.stats.use_scroll()

        return True