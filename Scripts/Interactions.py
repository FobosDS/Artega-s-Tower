import pygame
from Objects import Shelf

class Interaction_Manager:
    def __init__(self):
        self.interactive_objects = []
        self.give_ring = None

    def handle_input(self, player_rect, keys, player_stats):
        if not keys[pygame.K_e]:
            return None
        for obj in self.interactive_objects:
            if obj.interactive_rect.colliderect(player_rect):
                msg = obj.perform_action(player_stats, self.give_ring)
                if msg:
                    player_stats.notify(msg)
                self._check_guaranteed_keys(obj, player_stats)
                return msg
        return None

    def _check_guaranteed_keys(self, obj, player_stats):
        if not isinstance(obj, Shelf) or not obj.is_action_perfomed:
            return
        all_shelves = [o for o in self.interactive_objects if isinstance(o, Shelf)]
        if not all_shelves or not all(s.is_action_perfomed for s in all_shelves):
            return
        if not player_stats.is_chest_key1:
            player_stats.is_chest_key1 = True
            player_stats.notify("Когда надежда открыть сундук почти покинула Оскара, на последней полке он находит...Ключ от сундука!")
        if not player_stats.is_chest_key2:
            player_stats.is_chest_key2 = True
            player_stats.notify("Когда надежда открыть таинственный сундук почти покинула Оскара, на последней полке он находит...Ключ от тайника Артеги!")