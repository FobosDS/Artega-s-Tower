import pygame
from Settings import *
import random
from Sprites_Archive import ISD, DSD, RD, floor_decorations
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

    def get_prompt(self, player_stats):
        return None

class Chest(Interactive_Sprite):                                  
    def __init__(self, x, y):
        y += 50
        super().__init__(x, y, ISD["chest"]["close"], scale=0.5, collision_radius=14)
        self.is_open = False

    def perform_action(self, player_stats, give_ring=None):
        if self.is_open:
            return "Сундук пуст"
        if not player_stats.is_chest_key1:                         
            return "Требуется ключ от сундука"
        self.is_open = True
        self.image = pygame.image.load(ISD["chest"]["open"]).convert_alpha()
        amount = random.randint(*chest_gold_drop)
        player_stats.base.add_gold(amount)
        item = Items_Hub.roll_shelf_loot(player_stats.get_loot_bonus())
        if item is None:
            return f"В сундуке только золото. Оскар получил {amount} золота"
        player_stats.give_item(item, give_ring=give_ring)
        return Items_Hub.colored_pickup(f"Оскар открыл сундук: {amount} золота и ", item)

    def get_prompt(self, player_stats):                            
        if self.is_open or not player_stats.is_chest_key1:
            return "Осмотреть"
        return "Открыть сундук"    

class Rare_Chest(Interactive_Sprite):
    def __init__(self, x, y, unique_item=None):
        image_path = ISD["rare_chest"]["close"]
        super().__init__(x, y, image_path, scale=1, collision_radius=14)
        self.is_open = False
        self.unique_item = unique_item
    
    def perform_action(self, player_stats, give_ring=None):
        if self.is_open:
            return "Тайник пуст"
        if not player_stats.is_chest_key2:
            return "Требуется ключ от тайника Артеги"
        self.is_open = True
        self.image = pygame.image.load(ISD["rare_chest"]["open"]).convert_alpha()
        item = self.unique_item if self.unique_item else Items_Hub.ring
        msg = player_stats.give_item(item, give_ring=give_ring)
        return Items_Hub.colored_pickup("Оскар нашел в тайнике Артеги: ", item)

    def get_prompt(self, player_stats):                            
        if self.is_open or not player_stats.is_chest_key2:
            return "Осмотреть"
        return "Открыть тайник"
         
    
class Merchant(Interactive_Sprite):
    def __init__(self, x, y, unique_item=None):
        super().__init__(x, y, ISD["merchant"], scale=0.9, collision_radius=10)
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
        price = int(self.price * player_stats.get_price_multiplier())
        if price > max_gold:
            return "Торговец стал настолько алчным, что его товары Оскару больше не по карману!"
        if player_stats.base.gold < price:
            return "Оскару не хватает золота"

        item = self._current_offer()
        player_stats.base.gold -= price
        msg = player_stats.give_item(item, give_ring=give_ring)
        if self.unique_item is not None:
            self.unique_item = None
            self.price = int(Items_Hub.merchant_base_goods[0][1])
            return Items_Hub.colored_pickup("Оскар купил у жадного торгаша: ", item)
        self.trades_done += 1
        self.price = int(self.price * price_buy_growth)
        return Items_Hub.colored_pickup("Оскар купил у жадного торгаша: ", item)

    def get_prompt(self, player_stats):
        price = int(self.price * player_stats.get_price_multiplier())
        item = self._current_offer()
        name = Items_Hub.get_item_name(item)
        if price > max_gold:
            return "Товары вам больше не по карману"
        return f"{name}: {price} золота"

class Shelf(Interactive_Sprite):
    def __init__(self, x, y):
        super().__init__(x, y, DSD["box"], scale=1.0, collision_radius=14.5)
        self.hidden = True

        self.empty_shelf_msg = [
            "Полка пуста",
            "Кроме глупых любовных записок на полке ничего нет",
            "Оскар нашел книгу об основах магии тьмы, написанную самим Тьерри! И выкинул ее, так как не умеет читать...",
            "Оскар нашел на полке несколько монет...фальшивых...",
            "Кроме старых склянок на полке ничего нет",
            "На этой очень пыльной и грязной полке ничего не оказалось",
            "Кажется, здесь раньше стояло что-то важное. Обидно",
            "Полка оказалась гнилой и сломалась от прикосновения...На ней ничего не оказалось",
            "Оскар нашел на полке тайник подручного Артеги! Он пуст...",
            "Все ценное с полки давным давно расстаскали",
            "На полке Оскар нашел только пыльный след от какого-то предмета",
            "Кто-то выцарапал на дне полки фразу: «Оставь надежду, всяк сюда входящий». Оскар ничего не смог прочесть",
            "На полке лежать лишь чьи-то высохшие пальцы...жуть...",
            "Единственное богатство здесь пыль. Пыль ценой в золото...Вот бы она могла стать золотом!",
            "Полка выглядит так, будто её уже обыскивал гуль. Дважды",
            "Оскар осмотрел полку, она пуста...Полка победила",
            "Ни еды, ни воды, ни оружия",
            "Тупая пустота, будто снова ночью где-то пропадаю в поисках того, что не найти..."
        ]

    def perform_action(self, player_stats, give_ring=None):
        if self.is_action_perfomed:
            return "Полка пуста"
        self.is_action_perfomed = True
        item = Items_Hub.roll_shelf_loot(player_stats.get_loot_bonus())
        if item == Items_Hub.gold:
            amount = random.randint(*shelf_gold_drop)
            player_stats.base.add_gold(amount)
            return f"На полке завалялось несколько монет. Оскар получил {amount} золота"
        if item is None:
            return random.choice(self.empty_shelf_msg)
        player_stats.give_item(item, give_ring=give_ring)
        return Items_Hub.colored_pickup("Оскар нашел на полке: ", item)

    def get_prompt(self, player_stats):
        return "Осмотреть"

class RingPickup(Interactive_Sprite):
    def __init__(self, x, y, ring_type):
        image_path = RD[ring_type]["sprite"]
        super().__init__(x, y, image_path, scale=0.2, collision_radius=0)
        self.ring_type = ring_type

        self.pickup_radius = 36
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.rect.center = (x, y)
        self.interactive_rect = pygame.Rect(
            x - self.pickup_radius, y - self.pickup_radius,
            self.pickup_radius * 2, self.pickup_radius * 2)

        self.displaced = None    
        self.taken = False       

        self.bob_phase = random.random() 
        self.bob_offset = 0

        self.on_floor = True
        self.floor_sink = ring_floor_sink

    def update(self, dt):
        self.bob_phase = (self.bob_phase + dt * ring_bob_speed) % 1.0
        tri = 1 - abs(2 * self.bob_phase - 1)           
        self.bob_offset = -int(tri * ring_bob_height)

    def perform_action(self, player_stats, give_ring=None):
        player_stats.last_displaced_ring = None
        chosen = self.ring_type
        if give_ring is not None:
            displaced = give_ring(chosen)
        else:
            displaced = player_stats.base.add_ring(chosen)
        player_stats.last_displaced_ring = displaced
        self.taken = True
        return [
            ("Оскар подобрал с пола: ", white),
            (RD[chosen]['name'], color_ring),
        ]

    def get_prompt(self, player_stats):
        return "Подобрать кольцо"
        
class Decoration(Sprite):
    def __init__(self, x, y, floor=1):
        allowed = floor_decorations.get(floor, list(DSD.keys()))
        random_key = random.choice(allowed)
        image_path = DSD[random_key]

        super().__init__(x, y, image_path, scale=0.6, collision_radius=6)

class Altar(Interactive_Sprite):
    def __init__(self, x, y):
        image_path = ISD["altar"]
        super().__init__(x, y, image_path, scale=0.7, collision_radius=14)

    def perform_action(self, player_stats, give_ring=None):
        if player_stats.base.dark_shards < 1:
            return "Алтарь требует тьмы и крови"
        cost = player_stats.base.max_hp // 2
        if player_stats.base.hp - cost <= 0:
            return "Оскар слишком слаб"
        player_stats.base.hp -= cost
        player_stats.base.dark_shards -= 1
        player_stats.request_save = True
        return [
            ("Оскар отдал ", white),
            (f"{cost} здоровья", color_heart),
            (" и осколок тьмы. Прогресс сохранён", white)
        ]

    def get_prompt(self, player_stats):
        if player_stats.base.dark_shards < 1:
            return "Осмотреть"
        return "Сохранить прогресс"

class Stairs(Interactive_Sprite):
    def __init__(self, x, y):
        super().__init__(x, y, DSD["cell_break"], scale=1.0, collision_radius=16)
        self.hidden = True

    def perform_action(self, player_stats, give_ring=None):
        if not player_stats.is_floor_key:
            return "Требуется ключ от этажа"
        player_stats.is_floor_key = False
        player_stats.request_next_floor = True
        return "Оскар поднимается на следующий этаж башни"

    def get_prompt(self, player_stats):
        return "Подняться на следующий этаж"

class Barrier(Interactive_Sprite):
    def __init__(self, x, y):
        super().__init__(x, y, DSD["cell_ghoul"], scale=1.0, collision_radius=14.5)
        self.hidden = True
        self.broken = False
        self.rect = pygame.Rect(x - tile_size // 2, y - tile_size // 2, tile_size, tile_size)
        self.interactive_rect = pygame.Rect(x - tile_size // 2 - 10, y - tile_size // 2 - 10, tile_size + 20, tile_size + 20)

    def perform_action(self, player_stats, give_ring=None):
        if self.broken:
            return "Барьер рассыпался"
        return "Барьер не поддаётся"

    def get_prompt(self, player_stats):                      
        if self.broken:
            return None
        return "Осмотреть"

    def break_barrier(self):
        self.broken = True
        self.rect = pygame.Rect(0, 0, 0, 0)

