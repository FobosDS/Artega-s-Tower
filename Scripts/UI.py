import pygame
from Settings import *
from Sprites_Archive import RD, WTD, floor_names
import math
from Settings import bindings, key_labels
import os
from Settings import save_file

fonts = {
    "dispater": "Assets/Fonts/DISPATERVF.ttf",
    "demonic": "Assets/Fonts/MB-Demonic_Tale.ttf",
    "deutsche": "Assets/Fonts/Wolgadeutsche.ttf",
    "gothic": "Assets/Fonts/BrahmsGotischCyr.otf",
    "health": "Assets/Fonts/HealthGoth-Regular.ttf"
}

font_cache = {}

def get_font(name, size):
    key = (name, size)
    if key not in font_cache:
        path = fonts.get(name)
        try:
            font_cache[key] = pygame.font.Font(path, size)
        except Exception:
            font_cache[key] = pygame.font.Font(None, size)
    return font_cache[key]

class Tab_Overlay:
    def __init__(self, game):
        self.game = game
        self.visible = False

        self.header_font = get_font("demonic", 30)
        self.name_font = get_font("gothic", 24)
        self.desc_font = get_font("gothic", 18)

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
        else:
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

        shard_font = get_font("gothic", 20)
        shard_text = f"Осколки тьмы: {self.game.player.stats.base.dark_shards} / {max_dark_shards}"
        surf = shard_font.render(shard_text, True, white)
        screen.blit(surf, (rect.x + 15, rect.y + rect.h - 30))
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
        if not walls_grid or not walls_grid[0]:
            return

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
    font = get_font("gothic", 28)
    surf = font.render(text, True, white)
    rect = surf.get_rect(midbottom=(half_width, half_height+100))
    screen.blit(surf, rect)

class ToastMessage:
    def __init__(self, x, y, font_size=20, max_lines=3):
        self.x = x
        self.y = y
        self.font = get_font("gothic", font_size)
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
        self.font = get_font("gothic", 14)
        
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

class MainMenu:
    def __init__(self, screen, sound_manager):
        self.screen = screen
        self.sound_manager = sound_manager
        self.title_font = get_font("demonic", 130)
        self.button_font = get_font("gothic", 32)
        self.small_font = get_font("gothic", 22)

        self.buttons = [
            {"key": "start", "text": "Начать игру"},
            {"key": "settings", "text": "Настройки"},
            {"key": "quit", "text": "Выход"},
        ]

        if os.path.exists(save_file):
            self.buttons.insert(1, {"key": "load", "text": "Загрузить игру"})

        self.selected = 0
        self.show_settings = False

        self.settings_focus = 0
        self.rebinding = None   

        total_h = len(self.buttons) * menu_button_h + (len(self.buttons) - 1) * menu_button_gap
        self.start_y = half_height - total_h // 2 + 60

    def _button_rect(self, index):
        x = half_width - menu_button_w // 2
        y = self.start_y + index * (menu_button_h + menu_button_gap)
        return pygame.Rect(x, y, menu_button_w, menu_button_h)

    def handle_event(self, event):
        if self.show_settings:
            return self._handle_settings(event)
        return self._handle_main(event)

    def _handle_main(self, event):
        if event.type == pygame.MOUSEMOTION:
            for i in range(len(self.buttons)):
                if self._button_rect(i).collidepoint(event.pos):
                    self.selected = i
                    break
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, btn in enumerate(self.buttons):
                if self._button_rect(i).collidepoint(event.pos):
                    return self._activate(btn["key"])
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.buttons)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.buttons)
            elif event.key == pygame.K_RETURN:
                return self._activate(self.buttons[self.selected]["key"])
        return None

    def _activate(self, key):
        if key == "start":
            return "start"
        if key == "load":
            return "load"
        if key == "settings":
            self.show_settings = True
            self.settings_focus = 0
            return None
        if key == "quit":
            return "quit"
        return None

    def _settings_rows(self):
        rows = [
            ("music_vol", "Громкость музыки"),
            ("sfx_vol",   "Громкость звуков"),
        ]
        for action in key_labels:
            rows.append(("bind_" + action, key_labels[action]))
        rows.append(("back", "Назад"))
        return rows

    def _handle_settings(self, event):
        rows = self._settings_rows()

        if self.rebinding is not None:
            if event.type == pygame.KEYDOWN:
                bindings[self.rebinding] = event.key
                self.rebinding = None
            return None

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.show_settings = False
                return "back"
            if event.key == pygame.K_UP:
                self.settings_focus = (self.settings_focus - 1) % len(rows)
            elif event.key == pygame.K_DOWN:
                self.settings_focus = (self.settings_focus + 1) % len(rows)
            elif event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                delta = 0.1 if event.key == pygame.K_RIGHT else -0.1
                kind = rows[self.settings_focus][0]
                if kind == "music_vol":
                    self.sound_manager.change_music_volume(delta)
                elif kind == "sfx_vol":
                    self.sound_manager.change_sfx_volume(delta)
            elif event.key == pygame.K_RETURN:
                kind = rows[self.settings_focus][0]
                if kind.startswith("bind_"):
                    self.rebinding = kind[5:]
                elif kind == "back":
                    self.show_settings = False
                    return "back"

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, (kind, _) in enumerate(rows):
                rect = self._settings_row_rect(i)
                if rect.collidepoint(event.pos):
                    self.settings_focus = i
                    if kind.startswith("bind_"):
                        self.rebinding = kind[5:]
                    elif kind == "back":
                        self.show_settings = False
                        return "back"
        return None

    def _settings_row_rect(self, index):
        y = 200 + index * 40
        return pygame.Rect(half_width - 300, y - 12, 600, 34)

    def draw(self):
        self.screen.fill(menu_bg)
        if self.show_settings:
            self._draw_settings()
        else:
            self._draw_main()

    def _draw_main(self):
        title = self.title_font.render("Artega's Tower", True, menu_title_color)
        self.screen.blit(title, title.get_rect(center=(half_width, 120)))
        for i, btn in enumerate(self.buttons):
            rect = self._button_rect(i)
            color = menu_button_hover if i == self.selected else menu_button_color
            pygame.draw.rect(self.screen, color, rect, border_radius=6)
            pygame.draw.rect(self.screen, menu_title_color, rect, 2, border_radius=6)
            txt = self.button_font.render(btn["text"], True, menu_button_text)
            self.screen.blit(txt, txt.get_rect(center=rect.center))

    def _draw_settings(self):
        title = self.button_font.render("Настройки", True, menu_title_color)
        self.screen.blit(title, title.get_rect(center=(half_width, 120)))

        rows = self._settings_rows()
        for i, (kind, label) in enumerate(rows):
            rect = self._settings_row_rect(i)
            color = menu_button_hover if i == self.settings_focus else menu_button_color
            pygame.draw.rect(self.screen, color, rect, border_radius=4)

            if kind == "music_vol":
                value = f"{int(self.sound_manager.music_volume * 100)}"
            elif kind == "sfx_vol":
                value = f"{int(self.sound_manager.sfx_volume * 100)}"
            elif kind.startswith("bind_"):
                action = kind[5:]
                if self.rebinding == action:
                    value = "Нажмите клавишу..."
                else:
                    value = pygame.key.name(bindings[action])
            else:
                value = ""

            name_surf = self.small_font.render(label, True, menu_button_text)
            self.screen.blit(name_surf, (rect.x + 12, rect.y + 6))
            if value:
                val_surf = self.small_font.render(value, True, menu_title_color)
                self.screen.blit(val_surf, (rect.right - val_surf.get_width() - 12, rect.y + 6))

class IntroScene:
    def __init__(self, screen):
        self.screen = screen
        self.quote_font = get_font("gothic", 34)
        self.author_font = get_font("gothic", 24)

        self.quote = "Исполнение самых сильных наших желаний часто бывает источником величайших наших скорбей"
        self.author = "Луций Анней Сенека"

        self.phase = "in"
        self.timer = 0.0
        self.done = False

        self.fade_in = 2.5
        self.hold = 4.0
        self.fade_out = 2.0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_SPACE, pygame.K_RETURN):
                self.done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.done = True

    def update(self, dt):
        if self.done:
            return
        self.timer += dt

        if self.phase == "in":
            if self.timer >= self.fade_in:
                self.phase = "hold"
                self.timer = 0.0
        elif self.phase == "hold":
            if self.timer >= self.hold:
                self.phase = "out"
                self.timer = 0.0
        elif self.phase == "out":
            if self.timer >= self.fade_out:
                self.done = True

    def _alpha(self):
        if self.phase == "in":
            return int(255 * min(1.0, self.timer / self.fade_in))
        if self.phase == "hold":
            return 255
        if self.phase == "out":
            return int(255 * max(0.0, 1.0 - self.timer / self.fade_out))
        return 0

    def draw(self):
        self.screen.fill((0, 0, 0))

        alpha = self._alpha()
        if alpha <= 0:
            return

        words = self.quote.split()
        lines = []
        current = ""
        max_w = width - 200
        for w in words:
            test = (current + " " + w).strip()
            if self.quote_font.size(test)[0] > max_w:
                lines.append(current)
                current = w
            else:
                current = test
        if current:
            lines.append(current)

        total_h = len(lines) * 40
        y = half_height - total_h // 2 - 20

        for line in lines:
            surf = self.quote_font.render(line, True, (220, 220, 220))
            surf.set_alpha(alpha)
            rect = surf.get_rect(center=(half_width, y))
            self.screen.blit(surf, rect)
            y += 40

        author_surf = self.author_font.render(f" {self.author}", True, (160, 160, 160))
        author_surf.set_alpha(alpha)
        rect = author_surf.get_rect(center=(half_width, y + 20))
        self.screen.blit(author_surf, rect)

class PauseMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = get_font("gothic", 40)
        self.small = get_font("gothic", 22)
        self.visible = False
        self.confirm_exit = False
        self.selected = 0
        self.options = [("resume", "Продолжить"), ("exit", "Выйти в меню")]

    def open(self):
        self.visible = True
        self.confirm_exit = False
        self.selected = 0

    def close(self):
        self.visible = False
        self.confirm_exit = False

    def _option_rect(self, i):
        y = half_height - 40 + i * 70
        return pygame.Rect(half_width - 180, y, 360, 54)

    def handle_event(self, event):
        if not self.visible:
            return None
        if self.confirm_exit:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.confirm_exit = False
                elif event.key in (pygame.K_RETURN, pygame.K_y):
                    return "exit"
                elif event.key in (pygame.K_n,):
                    self.confirm_exit = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                yes = pygame.Rect(half_width - 220, half_height + 20, 200, 54)
                no = pygame.Rect(half_width + 20, half_height + 20, 200, 54)
                if yes.collidepoint(event.pos):
                    return "exit"
                if no.collidepoint(event.pos):
                    self.confirm_exit = False
            return None

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.close()
                return "close"
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                return self._activate(self.options[self.selected][0])

        if event.type == pygame.MOUSEMOTION:
            for i in range(len(self.options)):
                if self._option_rect(i).collidepoint(event.pos):
                    self.selected = i
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, (key, _) in enumerate(self.options):
                if self._option_rect(i).collidepoint(event.pos):
                    return self._activate(key)
        return None

    def _activate(self, key):
        if key == "resume":
            self.close()
            return "close"
        if key == "exit":
            self.confirm_exit = True
            return None
        return None

    def draw(self):
        if not self.visible:
            return
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))

        if self.confirm_exit:
            self._draw_confirm()
            return

        title = self.font.render("Пауза", True, menu_title_color)
        self.screen.blit(title, title.get_rect(center=(half_width, 220)))

        for i, (key, label) in enumerate(self.options):
            rect = self._option_rect(i)
            color = menu_button_hover if i == self.selected else menu_button_color
            pygame.draw.rect(self.screen, color, rect, border_radius=6)
            pygame.draw.rect(self.screen, menu_title_color, rect, 2, border_radius=6)
            txt = self.small.render(label, True, menu_button_text)
            self.screen.blit(txt, txt.get_rect(center=rect.center))

    def _draw_confirm(self):
        box = pygame.Rect(half_width - 300, half_height - 120, 600, 240)
        pygame.draw.rect(self.screen, menu_bg, box, border_radius=10)
        pygame.draw.rect(self.screen, menu_title_color, box, 3, border_radius=10)

        q = self.small.render("Выйти в главное меню?", True, menu_button_text)
        self.screen.blit(q, q.get_rect(center=(half_width, half_height - 50)))

        yes = pygame.Rect(half_width - 220, half_height + 20, 200, 54)
        no = pygame.Rect(half_width + 20, half_height + 20, 200, 54)
        for rect, label in ((yes, "Да"), (no, "Нет")):
            pygame.draw.rect(self.screen, menu_button_hover, rect, border_radius=6)
            pygame.draw.rect(self.screen, menu_title_color, rect, 2, border_radius=6)
            txt = self.small.render(label, True, menu_button_text)
            self.screen.blit(txt, txt.get_rect(center=rect.center))
    