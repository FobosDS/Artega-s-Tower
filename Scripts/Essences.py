ESSENCE_ORDER = ["ghoul", "gargoyle", "vampire", "darkness"]

ESSENCES = {
    "ghoul": {
        "name": "Сущность гуля",
        "color": (110, 170, 90),
        "desc": "Повышает устойчивость организма к ядам"
    },
    "gargoyle": {
        "name": "Сущность горгульи",
        "color": (150, 150, 175),
        "desc": "Дает способность делать двойной рывок"
    },
    "vampire": {
        "name": "Сущность вампира",
        "color": (175, 45, 65),
        "desc": "Убийство живых существ лечит"
    },
    "darkness": {
        "name": "Сущность тьмы",
        "color": (95, 60, 135),
        "desc": "Спасает от смерти и повышает урон тьмой"
    }
}

floor_elite = {
    2: "ghoul",
    3: "gargoyle",
    4: "vampire"
}


class Essence_Hub:
    def __init__(self):
        self.owned = []
        self.darkness_save_used = False

    def has(self, key):
        return key in self.owned

    def grant(self, key):
        if key in self.owned:
            return False
        self.owned.append(key)
        return True

    def owned_list(self):
        return [k for k in ESSENCE_ORDER if k in self.owned]

    def try_darkness_save(self, base_stats):     
        if self.darkness_save_used or "darkness" not in self.owned:
            return False
        if base_stats.hp <= 1:                 
            return False
        self.darkness_save_used = True
        return True
