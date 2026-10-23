import math
import pygame

#screen settings
#==================================
width = 1200
height = 800
half_width = width // 2
half_height = height // 2
FPS = 60
tile_size = 50
#==================================


#player settings
#==================================
#movement
pl_pos = (half_width, half_height)
pl_angle = 0
pl_size = 20
pl_speed = 90
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
max_scrolls = 2
max_weapon_level = 3
max_hp_level = 4
max_sp_level = 3

#sp
sp_cost_dash = 25          
sp_cost_sprint_per_sec = 11
sp_cost_attack = 12       
sp_cost_block = 30
sp_bonus = 16
sp_regen_bonus = 6
sp_regen_delay_bonus = 0.11

#base stats
base_hp = 100         
base_sp = 100 - sp_bonus
base_durability = 80          
base_potions = 1
base_gold = 0  
base_scrolls = 2   
base_attack_damage = 10       
potion_heal_percent = 0.5 
base_sp_regen = 14 - sp_regen_bonus
base_sp_regen_delay = 0.45 + sp_regen_delay_bonus

#weapon
durability_loss = 1
#==================================

#effects
#==================================
#poison
poison_damage_percent = 0.01
poison_interval = 0.5
poison_duration = 12

#paralysis
paralysis_duration = 5

#enchantment
enchantment_duration = 10
enchantment_multiplier = 1.5
#==================================


#HUD settings
#==================================
#stats
hud_x = 375
hud_y = 710
hud_radius = 80
hud_spacing = 450

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
projCoeff = dist * tile_size * 5
scale = width / numRays
#==================================


#objects settings
#==================================
sprites_folder = "Assets/Sprites/"
sprites_scale = 1
#==================================


#controls settings
#==================================
mouse_sensitivity = 0.007
interact_key = pygame.K_e
potion_key = pygame.K_f
scroll_key = pygame.K_r
damage_key = pygame.K_q
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
#==================================