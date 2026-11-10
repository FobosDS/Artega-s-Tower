import pygame
from Settings import *
import random
from Sprites_Archive import ISD, SSD, RD
import Items_Hub

class Sprite:
    def __init__(self, x, y, image_path, scale=1, collision_radius=0):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image_path).convert_alpha()
        self.scale = scale
        self.img_w, self.img_h = self.image.get_size()
        self.aspect = self.img_w / self.img_h
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
        self.is_action_perfomed = False

    def perform_action(self, player_stats, give_ring=None):
        return ""

class Rare_Chest(Interactive_Sprite):
    def __init__(self, x, y, unique_item=None):
        image_path = ISD["rare_chest"]["close"]
        super().__init__(x, y, image_path, scale=0.8, collision_radius=14)
        self.is_open = False
        self.unique_item = unique_item
    
    def perform_action(self, player_stats, give_ring=None):
        if self.is_open:
            return "Сундук пуст"
        if not player_stats.is_chest_key2:
            return "Требуется ключ от тайника Артеги"
        self.is_open = True
        self.image = pygame.image.load(ISD["rare_chest"]["open"]).convert_alpha()
        item = self.unique_item if self.unique_item else Items_Hub.ring
        msg = player_stats.give_item(item, give_ring=give_ring)
        return f"Оскар нашел в тайнике чародея: {msg}"
    
class Merchant(Interactive_Sprite):
    def __init__(self, x, y, unique_item=None):
        super().__init__(x, y, ISD["merchant"]["merchant1"], scale=0.9, collision_radius=14)
        self.unique_item = unique_item
        self.trades_done = 0
        if unique_item == Items_Hub.ring:
            self.price = 160
        elif unique_item is not None:
            self.price = 120
        else:
            self.price = Items_Hub.merchant_base_goods[0][1]

    def _current_offer(self):
        if self.unique_item is not None:
            return self.unique_item
        base = Items_Hub.merchant_base_goods
        return base[self.trades_done % len(base)][0]

    def perform_action(self, player_stats, give_ring=None):
        if self.price > max_gold:
            return "Торговец стал настолько алчным, что его товары Оскару больше не по карману!"
        if player_stats.base.gold < self.price:
            return "Оскару не хватает золота"
        
        item = self._current_offer()
        player_stats.base.gold -= self.price
        msg = player_stats.give_item(item, give_ring=give_ring)
        if self.unique_item is not None:
            self.unique_item = None
            self.price = int(Items_Hub.merchant_base_goods[0][1])
            return f"Оскар купил у жадного торгаша: {msg}"
        self.trades_done += 1
        self.price = int(self.price * price_buy_growth)
        return f"Оскар купил у жадного торгаша: {msg}"

class Shelf(Interactive_Sprite):
    def __init__(self, x, y):
        super().__init__(x, y, SSD["box"], scale=1.0, collision_radius=14.5)

    def perform_action(self, player_stats, give_ring=None):
        if self.is_action_perfomed:
            return "Полка пуста"
        self.is_action_perfomed = True
        item = Items_Hub.roll_shelf_loot()
        if item == Items_Hub.gold:
            amount = random.randint(*shelf_gold_drop)
            player_stats.base.add_gold(amount)
            return f"На полке завлялось несколько монет. Оскар получил {amount} золота"
        if item is None:
            return "Полка пуста"
        msg = player_stats.give_item(item, give_ring=give_ring)
        return f"Оскар нашел на полке: {msg}" if msg else "Полка пуста"

class RingPickup(Interactive_Sprite):
    def __init__(self, x, y, ring_type):
        image_path = RD[ring_type]["sprite"]
        super().__init__(x, y, image_path, scale=1.0, collision_radius=12)
        self.ring_type = ring_type

    def perform_action(self, player_stats, give_ring=None):
        if give_ring is not None:
            give_ring(self.ring_type)
        else:
            player_stats.base.add_ring(self.ring_type)
        self.is_action_perfomed = True
        return f"Оскар подобрал с пола: {RD[self.ring_type]['name']}"

class Decoration(Sprite):
    def __init__(self, x, y):
        random_key = random.choice(list(SSD.keys()))
        image_path = SSD[random_key]

        super().__init__(x, y, image_path, scale=0.7, collision_radius=10)
