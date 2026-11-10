import random
from Settings import *
from Sprites_Archive import RD

#items
potion = "potion"
scroll = "scroll"
whetstone = "whetstone"
gold = "gold"
heart = "heart"
lungs = "lungs"
weapon_crate = "weapon_crate"
chest_key_base = "chest_key_base"
chest_key_rare = "chest_key_rare"
floor_key = "floor_key"
ring = "ring"

item_names = {
    potion:"Зелье жизни",
    scroll:"Свиток тьмы",
    whetstone:"Точильный камень",
    gold:"Золото",
    heart:"Сердце монстра",
    lungs:"Легкие вампира",
    weapon_crate:"Оружейный ящик Андре",
    chest_key_base:"Ключ от сундука",
    chest_key_rare:"Ключ от тайника Артеги",
    floor_key:"Ключ от этажа",
    ring: "Кольцо"
}

#loot tables
shelf_loot = [
    (None, 40), (gold, 24), (potion, 14), (scroll, 8), 
    (whetstone, 6), (chest_key_base, 5), (chest_key_rare, 3)
]

enemy_loot = {
    "ghoul":[
        (None, 61), (potion, 18), (scroll, 2), 
        (whetstone, 3), (chest_key_base, 5),
        (chest_key_rare, 3),  (floor_key, 8)
    ],

    "gargoyle":[
        (None, 40), (potion, 24), (scroll, 4), 
        (whetstone, 12), (chest_key_base, 6),
        (chest_key_rare, 4), (floor_key, 10)
    ],

    "vampire":[
        (None, 20), (potion, 26), (scroll, 26), 
        (whetstone, 2), (chest_key_base, 7),
        (chest_key_rare, 5), (floor_key, 14)
    ]
}

chest_base_loot = [
    (gold, 40), (potion, 26), 
    (scroll, 18), (whetstone, 16)
]

chest_rare_loot = [
    
]

merchant_unique_goods = [
    (heart, 120), (lungs, 120),
    (weapon_crate, 120), (ring, 160)
]

merchant_base_goods = [
    (potion, 30), (scroll, 60), (whetstone, 90)
]

cell_unique_items = {
    1: heart,
    2: lungs,
    3: weapon_crate,
    4: ring
}

def roll_weighted(table):
    if not table:
        return None
    total = sum(w for _, w in table)
    r = random.uniform(0, total)
    upto = 0
    for item, weight in table:
        upto += weight
        if upto >= r:
            return item
    return table[-1][0]

def get_item_name(item):
    if item == ring:
        return "Случайное кольцо"
    return item_names.get(item, "?")

def roll_enemy_loot(enemy_type):
    return roll_weighted(enemy_loot.get(enemy_type, enemy_loot["ghoul"]))

def roll_shelf_loot():
    return roll_weighted(shelf_loot)

def roll_chest_base_loot():
    return roll_weighted(chest_base_loot)

floor_rings = {
    1: ["ring_fugitive", "ring_merchant"],
    2: ["ring_dragon", "ring_dreamer"],
    3: ["ring_genius", "ring_murderer"],
    4: ["ring_warrior", "ring_aristocrat"],
}

def get_floor_rings(floor):
    return floor_rings.get(floor, [])

