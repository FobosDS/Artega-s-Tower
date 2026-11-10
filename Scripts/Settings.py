import math
import pygame

#screen settings
#==================================
width = 1200
height = 800
half_width = width // 2
half_height = height // 2
FPS = 60
tile_size = 25
texture_size = 64
#==================================


#player settings
#==================================
#movement
pl_pos = (half_width, half_height)
pl_angle = 0
pl_size = 10
pl_speed = 40
pl_rotation_speed = 5
pl_rect = (half_width, half_height, pl_size, pl_size)

#dash
dash_speed_multiplier = 4
dash_duration = 0.09
dash_cooldown = 1

#run
sprint_speed_multiplier = 1.4

#weapon
animation_duration = 0.1
reload_time = 0.35
block_duration = 0.3
#==================================


#status settings
#==================================
#max status
max_durability = 100
max_gold = 999
max_scrolls = 3
max_whetstones = 4
max_weapon_level = 5
max_hp_level = 6
max_sp_level = 5

#sp
sp_cost_dash = 10          
sp_cost_sprint_per_sec = 8
sp_cost_attack = 30    
sp_cost_block = 20
sp_bonus = 16
sp_regen_bonus = 6
sp_regen_delay_bonus = 0.11

#base stats
base_hp = 100         
base_sp = 100 - sp_bonus
base_durability = 1        
base_potions = 3
base_gold = 0  
base_scrolls = 1
base_whetstones = 1   
base_attack_damage = 10       
potion_heal_percent = 0.5 
base_sp_regen = 14 - sp_regen_bonus
base_sp_regen_delay = 0.45 + sp_regen_delay_bonus
base_hp_level = 1
base_sp_level = 1
base_weapon_level = 1

#weapon
durability_loss = 1
#==================================

#effects
#==================================
#poison
poison_damage_percent = 0.028
poison_interval = 0.5
poison_duration = 14

#paralysis
paralysis_duration = 6

#enchantment
enchantment_duration = 30
enchantment_multiplier = 1.5
#==================================


#objects settings
#==================================
sprites_folder = "Assets/Sprites/"
sprites_scale = 50
icons_folder = "Assets/Sprites/Icons/"
walls_folder = "Assets/Sprites/Levels/Walls/"
#==================================


#HUD settings
#==================================
#stats
hud_x = 305
hud_y = 741
hud_radius = 50
hud_spacing = 489

#effects indicators
indicator_radius = 26
indicator_spacing = 32
indicator_x = 550
indicator_y = 720

#interface
interface_x = 170
interface_y = 636
interface_scale = 0.71

#potion slot
slot_potion_x = 366
slot_potion_y = 648

#left column
slot_scroll_x = 365
slot_whetstone_x = 420
slot_gold_x = 365
slot_weapon_x = 420
slot_left_y = 702

#right column levels
slot_hp_lvl_x = 633
slot_sp_lvl_x = 636
slot_hp_lvl_y = 696
slot_sp_lvl_y = 747

#right column keys
slot_chest_key1_x = 695
slot_chest_key2_x = 696
slot_floor_key_x = 693
slot_keys_y = 652

#key icons
floor_key_icons = [
    icons_folder + "dungeon_key.png",
    icons_folder + "mausoleum_key.png",
    icons_folder + "archive_key.png",
    icons_folder + "hall_key.png"
]

slot_size = 40

#sword
weapon_base_x = 470
weapon_base_y = 44
weapon_scale = 0.95

#sword swing
weapon_walk_freq = 8
weapon_sprint_freq_multiplier = 1.6
weapon_amp_lerp = 7
weapon_max_swing_x = 14
weapon_max_swing_y = 6
weapon_moving_threshold = 0.25
#==================================


#ray casting settings
#==================================
fov = math.pi / 3
halfFov = fov / 2
numRays = width // 4
maxDepth = 800
deltaAngle = fov / numRays
dist = numRays / (2 * math.tan(halfFov))
scale = width / numRays
#==================================


#controls settings
#==================================
mouse_sensitivity = 0.007
interact_key = pygame.K_e
potion_key = pygame.K_f
scroll_key = pygame.K_q
whetstone_key = pygame.K_r
#==================================


#colors
#==================================
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
hp_red = (189, 31, 47)
hp_highlight = (247, 228, 228)
green = (0, 255, 0)
sp_green = (39, 206, 107)
sp_highlight = (228, 247, 237)
blue = (0, 0, 255)
light_gray = (220, 220, 220)
gray = (138, 138, 138)
dark_gray = (50, 50, 50)
light_black = (22, 22, 22)

#indicators colors
poison_off = (8, 46, 17)
poison_on = (44, 226, 49)
paralysis_off = (18, 36, 33)
paralysis_on = (190, 223, 221)
enchant_off = (9, 25, 60)
enchant_on = (19, 165, 236)
#==================================