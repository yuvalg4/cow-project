from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from texture import load_texture
from utils import draw_quad, draw_quad_texture, draw_item, draw_item_texture

def cow(center_x, center_z, len_z, head_angle_display_r, head_angle_display_u, 
        tail_angle_display_r, tail_angle_display_u, left_legs_angle, right_legs_angle):
    leg_len = len_z
    len_x = len_y = (2/3)*len_z
    center_y = len_y/2 + leg_len

    # body
    glColor3f(1, 1, 1)
    draw_body(center_x, center_y, center_z, len_x, len_y, len_z)
    # head
    head_x = center_x
    head_y = center_y + (1/3)*len_y
    head_z = center_z - (3/7)*len_z

    neck_x = len_x/3
    neck_y = len_x/2
    neck_z = len_x

    draw_head(head_x, head_y, head_z, neck_x, neck_y, neck_z, head_angle_display_r, head_angle_display_u)
    # legs
    draw_tail(center_x, center_y, center_z + (7/8)*len_z, len_x, 
              tail_angle_display_r, tail_angle_display_u)
    draw_legs(center_x, center_y, center_z, len_x, len_z, left_legs_angle, right_legs_angle)

def draw_legs(center_x, center_y, center_z, len_x, len_z, left_angle, right_angle):
    glColor3f(1,1,1)
    weidth_x = (3/7)*len_x
    weidth_z = (3/2)*weidth_x

    draw_leg(center_x - (1/2)*len_x, center_y, center_z - (3/4)*len_z , weidth_x, weidth_z, left_angle)
    draw_leg(center_x - (1/2)*len_x, center_y, center_z + (3/4)*len_z - weidth_z, 
             weidth_x, weidth_z, left_angle)
    draw_leg(center_x + (1/2)*len_x - weidth_x, center_y, center_z - (3/4)*len_z, 
             weidth_x, weidth_z, right_angle)
    draw_leg(center_x + (1/2)*len_x - weidth_x, center_y, center_z + (3/4)*len_z - weidth_z, 
             weidth_x, weidth_z, right_angle)
    
def draw_leg(x,y,z, weidth_x, weidth_z, angle):
    hoof_heigth = weidth_x
    vertices = [(x, y, z), # first four top ssquare
                (x, y, z + weidth_z),
                (x + weidth_x, y, z + weidth_z),
                (x + weidth_x, y, z),
                (x, hoof_heigth, z), # second four bottom ssquare
                (x, hoof_heigth, z + weidth_z),
                (x + weidth_x, hoof_heigth, z + weidth_z),
                (x + weidth_x, hoof_heigth, z),
                (x, 0, z - (1/3)*weidth_z), # hoof bace
                (x, 0, z + weidth_z),
                (x + weidth_x, 0, z + weidth_z),
                (x + weidth_x, 0, z - (1/3)*weidth_z)] 
    indices = [(0, 1, 2, 3),
               (0, 1, 5, 4),
               (1, 2, 6, 5),
               (2, 3, 7, 6),
               (0, 3, 7, 4),
               (5, 6, 10, 9),
               (6, 7, 11, 10),
               (7, 4, 8, 11),
               (4, 5, 9, 8),
               (8, 9, 10, 11)] 
    leg_texture_id = load_texture("legs_texture.png")

    glPushMatrix()
    glTranslate(x,y,z)
    glRotatef(angle, 1, 0, 0)
    glTranslate(-x,-y,-z)
    draw_item_texture(vertices, indices, leg_texture_id, 1)
    glPopMatrix()

def draw_body(center_x, center_y, center_z, len_x, len_y, len_z):
    textured_body(center_x, center_y, center_z, len_x, len_y, len_z)
    draw_udders(center_x, center_y-(3/4)*len_y, center_z, len_x/2)

def textured_body(center_x, center_y, center_z, len_x, len_y, len_z):
    cow_texture_id = load_texture("cow_texture.png")
    slices = 50
    stacks = 50

    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, cow_texture_id)

    glPushMatrix()
    glTranslatef(center_x, center_y, center_z)
    glScalef(len_x, len_y, len_z)

    quad = gluNewQuadric()
    gluQuadricTexture(quad, GL_TRUE)
    gluSphere(quad, 1, slices, stacks)

    glPopMatrix()

    glBindTexture(GL_TEXTURE_2D, 0)
    glDisable(GL_TEXTURE_2D)

def draw_head(x, y, z, neck_x, neck_y, neck_z, head_angle_display_r, head_angle_display_u): # (x,y,z) point inside body
    vertices = [(x, y, z), #0
                (x-neck_x, y+neck_y, z-neck_z), #1
                (x+neck_x, y+neck_y, z-neck_z), #2
                (x+2*neck_x, y, z-neck_z), #3
                (x, y-neck_y, z-neck_z), #4
                (x-2*neck_x, y, z-neck_z), #5
                (x-2*neck_x, y-neck_y,z-(4/3)*neck_z), #6
                (x+2*neck_x, y-neck_y,z-(4/3)*neck_z), #7
                (x-(1/2)*neck_x, y+(1/2)*neck_y, z-(11/6)*neck_z), #8
                (x+(1/2)*neck_x, y+(1/2)*neck_y, z-(11/6)*neck_z), #9
                (x-(1/2)*neck_x, y+(1/2)*neck_y, z-(13/6)*neck_z), #10
                (x+(1/2)*neck_x, y+(1/2)*neck_y, z-(13/6)*neck_z), #11
                (x+(3/4)*neck_x, y-neck_y,z-(13/6)*neck_z), #12
                (x+(3/4)*neck_x, y-(1/2)*neck_y,z-(13/6)*neck_z), #13
                (x-(3/4)*neck_x, y-neck_y,z-(13/6)*neck_z), #14
                (x-(3/4)*neck_x, y-(1/2)*neck_y,z-(13/6)*neck_z)] #15
    indices = [((0, 1, 2), 1),
               ((0, 2, 3), 0),
               ((0, 3, 4), 0),
               ((0, 4, 5), 0),
               ((0, 5, 1), 0),
               ((2, 3, 7), 0),
               ((1, 5, 6), 0),
               ((3, 4, 7), 0),
               ((4, 5, 6), 0),
               ((4, 6, 7), 0),
               ((6, 7, 12, 14), 0),
               ((1, 2, 9, 8), 1),
               ((2, 7, 12, 9), 0),
               ((1, 6, 14, 8), 0),
               ((8, 9, 11, 10), 1),
               ((9, 11, 13, 12), 2),
               ((8, 10, 15, 14), 2),
               ((12, 14, 15, 13), 2),
               ((10, 11, 13, 15), 2)]
    colors = [(0,0,0), # black
              (1,1,1), # white
              (1, 204/255, 204/255) # pink
              ]
    glPushMatrix()
    glTranslate(x,y,z)
    glRotatef(head_angle_display_r, 0, 1, 0)
    glRotatef(head_angle_display_u, 1, 0, 0)
    glTranslate(-x,-y,-z)
    draw_item(vertices, indices, colors)
    
    left_eye = (x-neck_x, y+(1/3)*neck_y,z-(4/3)*neck_z)
    right_eye = (x+neck_x, y+(1/3)*neck_y,z-(4/3)*neck_z)
    left_ear = vertices[5]
    right_ear = vertices[3]
    left_nose = (x-(1/4)*neck_x, y+(1/4)*neck_y, z-(13/6)*neck_z)
    right_nose = (x+(1/4)*neck_x, y+(1/4)*neck_y, z-(13/6)*neck_z)

    eyes(left_eye,right_eye, (1/2)*neck_x)
    ears(left_ear, right_ear, neck_x, (3/4)*neck_x)
    nose(left_nose,right_nose, (1/4)*neck_x)
    glPopMatrix()

def nose(left,right, size):
    glColor3f(0, 0, 0)
    x, y, z = left
    draw_solid_sphere(x, y, z, size, size, size)
    x, y, z = right
    draw_solid_sphere(x, y, z, size, size, size)

def eyes(left,right, size):
    one_eye(left, "left", size)
    one_eye(right, "right", size)

def one_eye(place,side,size):
    glColor3f(1, 1, 1)
    x, y, z = place
    draw_solid_sphere(x, y, z, size, size, size)
    glColor3f(0, 0, 0)
    if side == "left":
        x -= (2/3)*size
    else:
        x += (2/3)*size
    size = size/2
    z -= size
    draw_solid_sphere(x, y, z, size, size, size)

def ears(left,right, len, weidth):
    one_ear(left, "left", len, weidth)
    one_ear(right, "right", len, weidth)

def one_ear(place, side, len, weidth):
    glColor3f(0, 0, 0)
    x, y, z = place
    if side == "left":
        x -= len/2
    else:
        x += len/2
    draw_solid_sphere(x, y, z, len, weidth, weidth)
    glColor3f(1, 204/255, 204/255)
    len /= 2
    z -= (5/8)*weidth
    weidth /= 2
    draw_solid_sphere(x, y, z, len, weidth, weidth)

def draw_udders(center_x, center_y, center_z, len):
    glColor3f(1, 204/255, 204/255)
    draw_solid_sphere(center_x, center_y, center_z, len, len, len)
    #teats
    teat_weidth = (1/4)*len
    teat_y = center_y - (1/4)*len
    draw_solid_sphere(center_x - len/2, teat_y, center_z - len/2, teat_weidth, len, teat_weidth)
    draw_solid_sphere(center_x - len/2, teat_y, center_z + len/2, teat_weidth, len, teat_weidth)
    draw_solid_sphere(center_x + len/2, teat_y, center_z - len/2, teat_weidth, len, teat_weidth)
    draw_solid_sphere(center_x + len/2, teat_y, center_z + len/2, teat_weidth, len, teat_weidth)

def draw_tail(x, y, z, len, tail_angle_display_r, tail_angle_display_u): 
    # (x,y,z) attachment point to the body  
    tail_weidth = (1/4)*len

    vertices = [(x + (1/2)*tail_weidth, y, z), #0
                (x - (1/2)*tail_weidth, y, z), #1
                (x + (1/2)*tail_weidth, y, z + tail_weidth), #2
                (x - (1/2)*tail_weidth, y, z + tail_weidth), #3
                (x + (1/2)*tail_weidth, y - len, z), #4
                (x - (1/2)*tail_weidth, y - len, z), #5
                (x + (1/2)*tail_weidth, y - len, z + tail_weidth), #6
                (x - (1/2)*tail_weidth, y - len, z + tail_weidth)] #7
    indices = [((0, 1, 3, 2), 0),
               ((4, 5, 7, 6), 0),
               ((0, 1, 5, 4), 0),
               ((0, 2, 6, 4), 0),
               ((2, 3, 7, 6), 0),
               ((3, 1, 5, 7), 0)]
    
    glPushMatrix()
    glTranslate(x,y,z)
    glRotatef(tail_angle_display_r, 0, 0, 1)
    glRotatef(tail_angle_display_u, 1, 0, 0)
    glTranslate(-x,-y,-z)
    draw_item(vertices, indices, [(0,0,0)])
    glColor3f(1, 1, 1)
    draw_solid_sphere(x, y - len - (1/2)*tail_weidth, z + (1/2)*tail_weidth, (2/3)*tail_weidth, 
                      (3/2)*tail_weidth, (2/3)*tail_weidth)
    glPopMatrix()

def draw_solid_sphere(center_x, center_y, center_z, len_x, len_y, len_z):
    slices = 50
    stacks = 50
    glPushMatrix()
    glTranslatef(center_x, center_y, center_z)
    glScalef(len_x, len_y, len_z)
    glutSolidSphere(1, slices, stacks)
    glPopMatrix()