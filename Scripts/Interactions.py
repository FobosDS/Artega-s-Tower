import pygame

class Interaction_Manager:
    def __init__(self):
        self.interactive_objects = []

    def handle_input(self, player_rect, keys):
        if keys[pygame.K_e]:
            for obj in self.interactive_objects:
                if obj.interactive_rect.colliderect(player_rect):
                    obj.perform_action()
                    break