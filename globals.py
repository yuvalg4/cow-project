import math
RADIUS_CAM_MIN = 30
RADIUS_CAM_MAX = 100
HIGTH_CAM_MIN = 10
HIGTH_CAM_MAX = 60


# window
winW, winH = 500, 500
angle = 0
aspect = float(winW) / winH

# locations, size, angles
cow_len_z = 6
aspect = float(winW) / winH

head_angle_l_r = 0
head_angle_u_d = 0
head_up_vector = (0, 1, 0)

tail_angle_l_r = 0
tail_angle_u_d = 0

body_angle = 0
body_loc = (0,0)
body_move = (0,0)

left_legs_angle_u_d = 0
right_legs_angle_u_d = 0
legs_angle_l_r = 0
last_leg = "left"

part_of_body = "body"

# eye parameters
near_view_plane = 0.1
far_view_plane = 150
angle_view_plane = 60
eyeX, eyeY, eyeZ = 0, 20, -60
radius = abs(eyeZ)
camera_movement = "up"
point_of_view = "camera"

# cow eye parameters
cow_eyeX, cow_eyeY, cow_eyeZ = 0, 2*cow_len_z, -(4/3)*cow_len_z
cow_refX, cow_refY, cow_refZ = 0, 2*cow_len_z, -10

#spotlight params:
spotLoc = [-16, 20, -20, 1]  # Position of the spotlight
spotDir = [-1/math.sqrt(3), -1/math.sqrt(3), 1/math.sqrt(3), 0 ]  # Direction of the spotlight
spotlight_exponent = [20.0]  # Exponent that controls the intensity distribution of the spotlight
global_ambient = [0.3, 0.3, 0.3, 1.0] # global ambient lighting

#Fence parameters
NUM_PARTS = 20
CHANGE = 2
x_fence = 4

# rocks parameters
ROCK_BASE = 7
# center, left, right, behind
rock_bases = [ROCK_BASE, (2/3)*ROCK_BASE, (3/4)*ROCK_BASE, (1/3)*ROCK_BASE]
gaps = [int((1/4)*i+1) for i in rock_bases]
x_rock = -35
z_rock = 0