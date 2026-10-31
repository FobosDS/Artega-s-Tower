import pygame
import random
from Sprites_Archive import ISD, SSD

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
        pass

class Rare_Chest(Interactive_Sprite):
    def __init__(self, x, y):
        # Берем закрытый сундук из архива
        image_path = ISD["rare_chest"]["close"]
        super().__init__(x, y, image_path, scale=0.8, collision_radius=18)
        self.is_open = False
    
    def perform_action(self):
        if not self.is_open:
            print("Сундук открыт! Вы нашли золото.")
            self.is_open = True
            # Меняем картинку на открытую (если есть)
            self.image = pygame.image.load(ISD["rare_chest"]["open"]).convert_alpha()
            # Здесь можно добавить логику выдачи золота игроку
        else:
            print("Сундук уже пуст.")

class Merchant(Interactive_Sprite):
    def __init__(self, x, y):
        # Берем первого торговца из архива
        image_path = ISD["merchant"]["merchant1"]
        super().__init__(x, y, image_path, scale=0.9, collision_radius=18)
    
    def perform_action(self):
        print("Торговец: 'Что желаешь купить?'")
        # Здесь в будущем откроется меню магазина

class Decoration(Sprite):
    def __init__(self, x, y):
        random_key = random.choice(list(SSD.keys()))
        image_path = SSD[random_key]

        super().__init__(x, y, image_path, scale=0.7, collision_radius=10)
        print(f"Создана декорация: {random_key}")