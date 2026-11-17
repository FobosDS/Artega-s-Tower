import pygame
from Settings import *
from Sprites_Archive import RD, WTD, floor_names
import math

class Tab_Overlay:
    def __init__(self, game):
        self.game = game
        self.visible = False

        self.header_font = pygame.font.Font(None, 30)
        self.name_font = pygame.font.Font(None, 24)
        self.desc_font = pygame.font.Font(None, 18)

        self.left_rect = pygame.Rect(rings_panel_x, rings_panel_y, rings_panel_w, rings_panel_h)
        self.right_rect = pygame.Rect(map_panel_x, map_panel_y, map_panel_w, map_panel_h)
        self.icon_size = 36

        self.ring_icons = {}
        for r, data in RD.items():
            img = pygame.image.load(data["sprite"]).convert_alpha()
            self.ring_icons[r] = pygame.transform.scale(img, (self.icon_size, self.icon_size))

    def toggle(self):
        self.visible = not self.visible

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB and not getattr(event, "repeat", False):
            self.toggle()
            return True
        return False

    def _wrap_text(self, text, font, max_w):
        words = text.split()
        lines, line = [], ""
        for word in words:
            test = (line + " " + word).strip()
            if font.size(test)[0] <= max_w:
                line = test
            else:
                if line:
                    lines.append(line)
                line = word
        if line:
            lines.append(line)
        return lines

    def draw_rings_panel(self, screen):
        if not self.visible:
            return 
        
        rect = self.left_rect
        pygame.draw.rect(screen, panel_bg, rect)
        pygame.draw.rect(screen, panel_border, rect, 2)

        header = self.header_font.render("Кольца Оскара", True, white)
        screen.blit(header, (rect.x + 15, rect.y + 12))

        rings = self.game.player.stats.base.rings
        y = rect.y + 48
        inner_w = rect.w - 30

        if not rings:
            note = self.name_font.render("Кольца не надеты", True, white)
            screen.blit(note, (rect.x + 15, y))
            return

        for r in rings:
            data = RD[r]
            screen.blit(self.ring_icons[r], (rect.x + 15, y - 12))

            name = self.name_font.render(data["name"], True, white)
            screen.blit(name, (rect.x + 15 + self.icon_size + 10, y))

            desc = data.get("desc", "Описание не найдено")
            ty = y + 36
            for line in self._wrap_text(desc, self.desc_font, inner_w):
                surf = self.desc_font.render(line, True, white)
                screen.blit(surf, (rect.x + 15, ty))
                ty += 20
            y = ty + 14   

    def draw_map_panel(self, screen):
        if not self.visible: 
            return
        
        rect = self.right_rect
        pygame.draw.rect(screen, panel_bg, rect)
        pygame.draw.rect(screen, panel_border, rect, 2)

        floor = self.game.player.stats.current_floor
        title = floor_names.get(floor, f"Этаж {floor}")

        header = self.header_font.render(title, True, white)
        screen.blit(header, (rect.x + 15, rect.y + 12))

        walls_grid = self.game.map_manager.walls_grid
        rows = len(walls_grid)
        cols = len(walls_grid[0])
        cell = min((rect.w - 30) / cols, (rect.h - 50) / rows)
        offset_x = rect.x + (rect.w - cell * cols) // 2
        offset_y = rect.y + 40 + (rect.h - 50 - cell * rows) // 2

        for row_i, row in enumerate(walls_grid):
            for col_i, ch in enumerate(row):
                if ch in WTD:
                    pygame.draw.rect(screen, map_wall_color,
                                     (offset_x + col_i * cell,
                                      offset_y + row_i * cell,
                                      max(1, cell - 1), max(1, cell - 1)))

def draw_prompt(screen, text):
    if not text:
        return
    font = pygame.font.Font(None, 28)
    surf = font.render(text, True, white)
    rect = surf.get_rect(midbottom=(half_width, half_height+100))
    screen.blit(surf, rect)

class ToastMessage:
    def __init__(self, x, y, font_size=22, max_lines=3):
        self.x = x
        self.y = y
        self.font = pygame.font.Font(None, font_size)
        self.line_height = self.font.get_height() + 6  
        self.max_lines = max_lines

        self.pending = []   
        self.active = []    
        self.duration = 3
        self.fade_time = 0.5

    def set_message(self, text):
        if not text:
            return
        if len(self.active) < self.max_lines:
            self.active.append({"text": text, "timer": self.duration + self.fade_time})
        else:
            self.pending.append(text)

    def update(self, dt):
        for m in self.active:
            m["timer"] -= dt
        self.active[:] = [m for m in self.active if m["timer"] > 0]

        while self.pending and len(self.active) < self.max_lines:
            self.active.append({"text": self.pending.pop(0),
                                "timer": self.duration + self.fade_time})

    def draw(self, screen):
        newest_index = len(self.active) - 1
        for i, m in enumerate(self.active):
            alpha = 255
            if m["timer"] < self.fade_time:
                alpha = int(255 * (m["timer"] / self.fade_time))
            surf = self.font.render(m["text"], True, white)
            surf.set_alpha(alpha)
            line_y = self.y - (newest_index - i) * self.line_height
            rect = surf.get_rect(midleft=(self.x, line_y))
            screen.blit(surf, rect)


class Icon:
    def __init__(self, path, x, y, scale=0.5):
        self.base_image = pygame.image.load(path).convert_alpha()
        self.scale = scale
        
        w, h = self.base_image.get_size()
        self.image = pygame.transform.scale(self.base_image, (int(w * scale), int(h * scale)))
        self.w, self.h = self.image.get_size()
        
        self.x = x
        self.y = y
        self.font = pygame.font.Font(None, 17)
        
        self._last_floor = -1
    def change_image(self, new_path):
        self.base_image = pygame.image.load(new_path).convert_alpha()
        w, h = self.base_image.get_size()
        self.image = pygame.transform.scale(self.base_image, (int(w * self.scale), int(h * self.scale)))
        self.w, self.h = self.image.get_size()

    def draw(self, screen, text_list=None, active=True):
        if not active:
            return

        offset_x = (slot_size - self.w) // 2
        offset_y = (slot_size - self.h) // 2
        draw_x = self.x + offset_x
        draw_y = self.y + offset_y
        
        screen.blit(self.image, (draw_x, draw_y))

        if text_list:
            text_x = draw_x + self.w + 5  
            text_y = draw_y + self.h - (len(text_list) * 15)
            for text in text_list:
                if text:
                    surf = self.font.render(str(text), True, white)
                    rect = surf.get_rect(topright=(text_x, text_y))
                    screen.blit(surf, rect)
                    text_y += 15

def create_icons():
    icons = {}
    
    icons["potion"] = Icon(icons_folder + "potion.png", slot_potion_x, slot_potion_y)
    
    icons["scroll"] = Icon(icons_folder + "scroll.png", slot_scroll_x, slot_left_y,scale=0.3)
    icons["whetstone"] = Icon(icons_folder + "whetstone.png", slot_whetstone_x, slot_left_y, scale=0.55)
    icons["gold"] = Icon(icons_folder + "gold.png", slot_gold_x, slot_left_y + 48, scale=0.4)
    icons["weapon"] = Icon(icons_folder + "lv1_sword.png", slot_weapon_x, slot_left_y + 46, scale=0.32) 
    
    icons["hp_lvl"] = Icon(icons_folder + "heart.png", slot_hp_lvl_x, slot_hp_lvl_y, scale=0.45)
    icons["sp_lvl"] = Icon(icons_folder + "lungs.png", slot_sp_lvl_x, slot_sp_lvl_y, scale=0.4)
    
    icons["chest_key1"] = Icon(icons_folder + "chest_key1.png", slot_chest_key1_x, slot_keys_y + 44, scale=0.44)
    icons["chest_key2"] = Icon(icons_folder + "chest_key2.png", slot_chest_key2_x, slot_keys_y + 92, scale=0.44)
    icons["floor_key"] = Icon(floor_key_icons[0], slot_floor_key_x, slot_keys_y, scale=0.44)
    
    return icons
      
def load_interface(scale_factor):
    try:
        sprite = pygame.image.load(sprites_folder + "interface.png").convert_alpha()
        img_w, img_h = sprite.get_size()
        new_width = int(img_w * scale_factor)
        new_height = int(img_h * scale_factor)
        return pygame.transform.scale(sprite, (new_width, new_height))
    except:
        return None

def draw_circle_bar(screen, cx, cy, radius, value, max_value, fill_color, bg_color, hl_color, hl_offset_x):
    #background
    pygame.draw.circle(screen, bg_color, (cx, cy), radius)

    #sphere
    if max_value > 0 and value > 0:
        ratio = min(1.0, value / max_value)
        current_radius = int(radius * ratio)
        if current_radius > 0:
            pygame.draw.circle(screen, fill_color, (cx, cy), current_radius)

    #highlight
    hl_x = cx + int(radius * hl_offset_x)
    hl_y = cy - int(radius * 0.35)
    hl_radius = max(1, int(radius * 0.18))
    pygame.draw.circle(screen, hl_color, (hl_x, hl_y), hl_radius)

def draw_status_indicators(screen, stats):
    #poison
    color = poison_on if stats.effects.is_poisoned else poison_off
    pygame.draw.circle(screen, color, (indicator_x - indicator_spacing, indicator_y), indicator_radius)

    #paralysis
    color = paralysis_on if stats.effects.is_paralyzed else paralysis_off
    pygame.draw.circle(screen, color, (indicator_x + indicator_spacing, indicator_y), indicator_radius)

    #enchantment
    color = enchant_on if stats.combat.is_enchanted else enchant_off
    pygame.draw.circle(screen, color, (indicator_x, indicator_y - 42), indicator_radius)

def draw_hud(screen, stats, icons, interface):
    #hp
    draw_circle_bar(
        screen, cx=hud_x, cy=hud_y,
        radius=hud_radius,
        value=stats.base.hp, max_value=stats.base.max_hp,
        fill_color=hp_red, bg_color=(80, 0, 0),
        hl_color=hp_highlight, hl_offset_x=0.35
    )

    #sp
    draw_circle_bar(
        screen, cx=hud_x + hud_spacing, cy=hud_y,
        radius=hud_radius,
        value=stats.base.sp, max_value=stats.base.max_sp,
        fill_color=sp_green, bg_color=(0, 80, 0),
        hl_color=sp_highlight, hl_offset_x=-0.35
    )

    draw_status_indicators(screen, stats)

    if interface:
        screen.blit(interface, (interface_x, interface_y))

    icons["potion"].draw(screen, text_list=[str(stats.base.potions)])
    
    #left panel
    icons["scroll"].draw(screen, text_list=[str(stats.base.scrolls)])
    icons["whetstone"].draw(screen, text_list=[str(stats.combat.whetstones)])
    icons["gold"].draw(screen, text_list=[str(stats.base.gold)])
    
    #weapon
    if not hasattr(icons["weapon"], "_last_weapon_lvl") or icons["weapon"]._last_weapon_lvl != stats.combat.weapon_level:
        if stats.combat.weapon_level == 1:
            icons["weapon"].change_image(icons_folder + "lv1_sword.png")
        elif stats.combat.weapon_level == 2:
            icons["weapon"].change_image(icons_folder + "lv2_sword.png")
        elif stats.combat.weapon_level == 3 or stats.combat.weapon_level == 4 or stats.combat.weapon_level == 5:
            icons["weapon"].change_image(icons_folder + "lv3_sword.png")
        icons["weapon"]._last_weapon_lvl = stats.combat.weapon_level
        
    icons["weapon"].draw(screen, text_list=[str(stats.combat.durability), stats.combat.weapon_level])

    #right panel
    icons["hp_lvl"].draw(screen, text_list=[stats.base.hp_level])
    icons["sp_lvl"].draw(screen, text_list=[stats.base.sp_level])

    #keys
    icons["chest_key1"].draw(screen, active=stats.is_chest_key1)
    icons["chest_key2"].draw(screen, active=stats.is_chest_key2)
    floor_index = max(0, min(stats.current_floor - 1, len(floor_key_icons) - 1))
    if icons["floor_key"]._last_floor != floor_index:
        icons["floor_key"].change_image(floor_key_icons[floor_index])
        icons["floor_key"]._last_floor = floor_index
    icons["floor_key"].draw(screen, active=stats.is_floor_key)
    