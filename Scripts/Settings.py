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
pl_speed = 290
pl_rotation_speed = 5
pl_rect = (half_width, half_height, pl_size, pl_size)
#dash
dash_speed_multiplier = 2.5
dash_duration = 0.08
dash_cooldown = 0.2
#run
sprint_speed_multiplier = 1.8

#ray casting settings
fov = math.pi / 3
halfFov = fov / 2
numRays = width // 4
maxDepth = 800
deltaAngle = fov / numRays
dist = numRays / (2 * math.tan(halfFov))
projCoeff = dist * tile_size * 5
scale = width / numRays

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