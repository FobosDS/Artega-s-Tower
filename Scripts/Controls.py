import pygame
from Settings import bindings

class Input_Manager:
    def __init__(self, player, interaction_manager, weapon):
        self.player = player
        self.interaction_manager = interaction_manager
        self.weapon = weapon
        self.tab_overlay = None
        self.pause_menu = None
        self.magic = None
        self.cutscene = None

    def handle_events(self, events):
        for event in events:
            if self.pause_menu is not None and self.pause_menu.visible:
                result = self.pause_menu.handle_event(event)
                if result == "exit":
                    return "exit_to_menu"
                continue

            if event.type == pygame.QUIT:
                return False

            if self.cutscene is not None and self.cutscene.active:   
                if event.type == pygame.KEYDOWN and event.key in (
                        pygame.K_ESCAPE, pygame.K_SPACE, pygame.K_RETURN):
                    self.cutscene.skip()
                return True

            if self.tab_overlay is not None and self.tab_overlay.handle_event(event):
                continue

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.pause_menu is not None:
                        self.pause_menu.open()
                        continue
                    return False
                if event.key == bindings["interact"]:
                    self.interaction_manager.handle_input(self.player.rect, {bindings["interact"]: True}, self.player.stats)
                if event.key == bindings["potion"]:
                    self.player.stats.use_potion()
                if event.key == bindings["scroll"]:
                    self.player.stats.use_scroll()
                if event.key == bindings["whetstone"]:
                    self.player.stats.combat.use_whetstone()
                if event.key == bindings["berserk"]:
                    self.player.stats._try_activate_berserk()
                if event.key == bindings["inventory"] and self.tab_overlay is not None:
                    self.tab_overlay.toggle()
                if event.key == bindings["magic"]:          
                    if getattr(self.weapon, "is_blocking", False):
                        self.weapon.is_blocking = False          
                    self.notify(self.magic.try_cast(self.player.stats))

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.magic.is_loaded(self.player.stats): 
                        self.magic.fire(self.player)
                    else:
                        self.weapon.attack()
                elif event.button == 3:
                    if self.magic.is_loaded(self.player.stats):  
                        self.notify("Оскара поглощает тьма. Он не в силах использовать меч!")
                    else:
                        self.weapon.block()

        return True

    def notify(self, msg):
        if not msg:
            return
        if hasattr(self.player.stats, "notify"):
            self.player.stats.notify(msg)