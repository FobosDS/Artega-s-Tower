import pygame
from Settings import *
import random
from Sprites_Archive import ISD, DSD, RD, floor_decorations, WTD
import Items_Hub

class Sprite:
    def __init__(self, x, y, image_path, scale=1, collision_radius=None):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image_path).convert_alpha()
        self.scale = scale
        self.img_w, self.img_h = self.image.get_size()
        self.aspect = self.img_w / self.img_h
        self.collision_radius = self.auto_collision_radius() if collision_radius is None \
            else collision_radius
        self.rect = pygame.Rect(
            self.x - self.collision_radius,
            self.y - self.collision_radius,
            self.collision_radius * 2,
            self.collision_radius * 2
        )

    def auto_collision_radius(self, solid_fraction=0.8):
        mask = pygame.mask.from_surface(self.image, 127)        
        rects = mask.get_bounding_rects()
        solid_w = max((r.w for r in rects), default=self.img_w)  
        world_w = self.scale * sprites_scale * solid_w / self.img_h
        return max(10, int(world_w * 0.5 * solid_fraction))

class Interactive_Sprite(Sprite):
    def __init__(self, x, y, image_path, scale=1.0, collision_radius=None, interactive_zone_scale=1.2):  
        super().__init__(x, y, image_path, scale, collision_radius)

        #interaction zone
        r = self.collision_radius                    
        self.interactive_rect = pygame.Rect(
            self.x - r * interactive_zone_scale,
            self.y - r * interactive_zone_scale,
            r * 2 * interactive_zone_scale,
            r * 2 * interactive_zone_scale
        )
        self.is_action_perfomed = False

    def perform_action(self, player_stats, give_ring=None):
        return ""

    def get_prompt(self, player_stats):
        return None

class Chest(Interactive_Sprite):                                  
    def __init__(self, x, y):
        super().__init__(x, y, ISD["chest"]["close"], scale=0.5)
        self.is_open = False
        self.on_floor = True                    
        self.floor_sink = 0.5
        
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
        super().__init__(x, y, image_path, scale=0.8)
        self.is_open = False
        self.unique_item = unique_item
        self.on_floor = True
        self.floor_sink = 0.5
    
    def perform_action(self, player_stats, give_ring=None):
        if self.is_open:
            return "Тайник пуст"
        if not player_stats.is_chest_key2:
            return "Требуется ключ от тайника Артеги"
        self.is_open = True
        self.image = pygame.image.load(ISD["rare_chest"]["open"]).convert_alpha()

        essence_msg = None                                  
        if getattr(self, "essence", None):
            ess = getattr(player_stats, "essences", None)
            if ess is not None and ess.grant(self.essence):
                from Essences import ESSENCES
                info = ESSENCES[self.essence]
                essence_msg = [("Сущность тьмы проникает в Оскара: ", white), (info["name"], info["color"])]

        item = self.unique_item if self.unique_item else Items_Hub.ring
        player_stats.give_item(item, give_ring=give_ring)
        if essence_msg is not None:                        
            return essence_msg
        return Items_Hub.colored_pickup("Оскар нашел в тайнике Артеги: ", item)

    def get_prompt(self, player_stats):                            
            if self.is_open or not player_stats.is_chest_key1:
                return "Осмотреть"
            return "Открыть тайник"    
         
class Merchant(Interactive_Sprite):
    def __init__(self, x, y, unique_item=None):
        super().__init__(x, y, ISD["merchant"], scale=0.9)
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

        super().__init__(x, y, image_path, scale=0.6)

class Altar(Interactive_Sprite):
    def __init__(self, x, y):
        image_path = ISD["altar"]
        super().__init__(x, y, image_path, scale=0.7)

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
        
        self.barrier_zone_depth = 4
        self.barrier_zone_width = 4

        self.wall_rect = None
        self.pulse = 0
        self.cooldown = 0
        self.guardians = set()
        self.armed = False
        self.zone = pygame.Rect(0, 0, 0, 0) 

        self.grid_row = None                               
        self.grid_col = None             

    def bind_wall(self, rect):
        self.wall_rect = rect

    def compute_zone(self, drawed_map, row, col, tile=tile_size):
        
        dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]        
        h = len(drawed_map)
        w = len(drawed_map[0]) if h else 0

        best = None
        for dy, dx in dirs:
            r, c = row + dy, col + dx
            if not (0 <= r < h and 0 <= c < w):
                continue
            if drawed_map[r][c] in WTD:                  
                continue
            r2, c2 = row + dy * 2, col + dx * 2
            open_ahead = 0 <= r2 < h and 0 <= c2 < w and drawed_map[r2][c2] not in WTD
            if best is None or (open_ahead and not best[0]):
                best = (open_ahead, dy, dx)
        if best is None:                                 
            self.zone = pygame.Rect(0, 0, 0, 0)
            return

        _, dy, dx = best
        depth = self.barrier_zone_depth * tile
        width = self.barrier_zone_width * tile
        cx, cy = (col + 0.5) * tile + dx * tile // 2 + dx * depth // 2, \
                 (row + 0.5) * tile + dy * tile // 2 + dy * depth // 2
        if dx != 0:                                      
            self.zone = pygame.Rect(int(cx - depth // 2), int(cy - width // 2), depth, width)
        else:                                            
            self.zone = pygame.Rect(int(cx - width // 2), int(cy - depth // 2), width, depth)

    def update(self, dt, enemies):
        
        if self.broken:
            return None
        self.pulse += dt
        self.cooldown = max(0.0, self.cooldown - dt)

        for e in enemies:                                
            if self.zone.width > 0 and self.zone.colliderect(e.rect) and e not in self.guardians:
                self.guardians.add(e)
                if not self.armed:
                    self.armed = True
                    return "Барьер Артеги блокирует проход! Нужно убить его хранителей!"

        self.guardians.intersection_update(enemies)      

        if self.armed and not self.guardians:        
            self.break_barrier()
            return "Барьер рассеялся!"
        return None

    def perform_action(self, player_stats, give_ring=None):
        if self.broken:
            return "Барьер рассеялся!"
        if self.cooldown <= 0:
            if not self.armed:
                return "Барьер не поддается"
            return f"Хранителей барьера осталось: {len(self.guardians)}"
        return None

    def get_prompt(self, player_stats):
        if self.broken:
            return None
        return "Осмотреть"

    def break_barrier(self):
        self.broken = True
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.interactive_rect = pygame.Rect(0, 0, 0, 0)

    def draw_overlay(self, screen, cam_x, cam_y):
        if self.broken:
            return
        wave = 90 + int(40 * math.sin(self.pulse * 4))
        r = self.wall_rect if self.wall_rect else self.rect
        tile_veil = pygame.Surface((r.w, r.h), pygame.SRCALPHA)
        tile_veil.fill((90, 20, 140, wave))
        screen.blit(tile_veil, (r.x - cam_x, r.y - cam_y))

class Gold_Heap(Interactive_Sprite):                                   
    def __init__(self, x, y):
        super().__init__(x, y, ISD["gold_heap"], scale=0.7)
        self.taken = False
        self.on_floor = True                    
        self.floor_sink = 0.5

    def perform_action(self, player_stats, give_ring=None):
        if self.taken:
            return "Ничего ценного не осталось"
        self.taken = True
        amount = random.randint(*gold_heap_drop_gold)
        player_stats.base.add_gold(amount)
        return f"Оскар собрал {amount} золота"

    def get_prompt(self, player_stats):
        if self.taken:
            return "Осмотреть"
        return "Собрать золото"

class Food(Interactive_Sprite):                                   
    def __init__(self, x, y):
        super().__init__(x, y, ISD["food"], scale=0.7)
        self.taken = False
        self.on_floor = True                    
        self.floor_sink = 0.5
        self.heal_amount = (10, 60)

    def perform_action(self, player_stats, give_ring=None):
        if self.taken:
            return "Все уже съеденно"
        self.taken = True
        amount = random.randint(*self.heal_amount)
        player_stats.base.heal(amount)
        return f"Оскар с жадностью съел пищу и вылечил {amount} здоровья!"

    def get_prompt(self, player_stats):
        if self.taken:
            return "Осмотреть"
        return "Съесть"

class Dark_Crystal(Interactive_Sprite):                                   
    def __init__(self, x, y):
        super().__init__(x, y, ISD["dark_crystal"], scale=0.6)
        self.taken = False
        self.on_floor = True                    
        self.floor_sink = 0.5

    def perform_action(self, player_stats, give_ring=None):
        if self.taken:
            return "Кристалл уже разрушен"
        self.taken = True
        player_stats.base.add_dark_shard()
        return f"Оскар сломал кристалл тьмы и получил его осколок"

    def get_prompt(self, player_stats):
        if self.taken:
            return "Осмотреть"
        return "Отколоть осколок"
