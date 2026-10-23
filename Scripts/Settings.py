import math

#screen settings
width = 1200
height = 800
half_width = width // 2
half_height = height // 2
FPS = 60
tile_size = 50

#player settings
pl_pos = (half_width, half_height)
pl_angle = 0
pl_size = 20
pl_speed = 100
pl_rotation_speed = 5
pl_rect = (half_width, half_height, pl_size, pl_size)
#dash
dash_speed_multiplier = 3.5
dash_duration = 0.09
dash_cooldown = 1
#run
sprint_speed_multiplier = 1.8
#attack
animation_duration = 0.1
reload_time = 0.35
block_duration = 0.3

#status settings
#max status
max_durability = 100
max_scrolls = 2
max_weapon_level = 3
max_hp_level = 4
max_sp_level = 3
#base stats
base_hp = 100          
base_sp = 100
base_durability = 80          
base_potions = 1
base_gold = 0  
base_scrolls = 2   
base_attack_damage = 10       
potion_heal_percent = 0.5 
#effects
#poison
poison_damage_percent = 0.01
poison_interval = 0.5
poison_duration = 12
#paralysis
paralysis_duration = 5
#enchantment
enchantment_duration = 10
enchantment_multiplier = 1.5
#weapon
durability_loss = 1

#ray casting settings
fov = math.pi / 3
halfFov = fov / 2
numRays = width // 4
maxDepth = 800
deltaAngle = fov / numRays
dist = numRays / (2 * math.tan(halfFov))
projCoeff = dist * tile_size * 5
scale = width / numRays

#objects settings
sprites_folder = "Assets/Sprites/"
sprites_scale = 1

#controls settings
mouse_sensitivity = 0.007

#colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
light_gray = (220, 220, 220)
gray = (138, 138, 138)
dark_gray = (50, 50, 50)
light_black = (22, 22, 22)