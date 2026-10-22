import pygame
from Objects import Sprite

class Interactive_Sprite(Sprite):
    def __init__(self, x, y, image_path, scale=1.0, collision_radius=0, interactive_zone_scale=1.2):
        super().__init__(x, y, image_path, scale, collision_radius) 
        
        self.interactive_rect = pygame.Rect(
            self.x - collision_radius * interactive_zone_scale,
            self.y - collision_radius * interactive_zone_scale,
            collision_radius * 2 * interactive_zone_scale,
            collision_radius * 2 * interactive_zone_scale
        )
        self.is_interactive = True
        self.action_performed = False

    def check_interaction(self, player_rect):
        return self.interactive_rect.colliderect(player_rect)

    #action when pressed E near object
    def perform_action(self):
            print(f"Взаимодействие с объектом")

class Interaction_Manager:
    def __init__(self):
        self.interactive_objects = []

    def handle_input(self, player_rect, keys):
        if keys[pygame.K_e]:
            for obj in self.interactive_objects:
                if obj.check_interaction(player_rect):
                    obj.perform_action()
                    break  