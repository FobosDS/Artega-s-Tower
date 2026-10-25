import pygame

class Sprite:
    def __init__(self, x, y, image_path, scale=1, collision_radius=0):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image_path).convert_alpha()
        self.scale = scale
        self.img_w, self.img_h = self.image.get_size()
        self.aspect = self.img_w / self.img_h
        #sprite hitbox
        self.rect = pygame.Rect(
            self.x - collision_radius,
            self.y - collision_radius,
            collision_radius * 2,
            collision_radius * 2
        )

class Interactive_Sprite(Sprite):
    def __init__(self, x, y, image_path, scale=1.0, collision_radius=0, interactive_zone_scale=1.2):
        super().__init__(x, y, image_path, scale, collision_radius)
        #interaction zone
        self.interactive_rect = pygame.Rect(
            self.x - collision_radius * interactive_zone_scale,
            self.y - collision_radius * interactive_zone_scale,
            collision_radius * 2 * interactive_zone_scale,
            collision_radius * 2 * interactive_zone_scale
        )
        self.is_interactive = True

    def perform_action(self):
        #object action
        print("Взаимодействие")