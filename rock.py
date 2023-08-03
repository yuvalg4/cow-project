from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from utils import draw_item_texture, draw_item
from texture import load_texture
from light import set_matte_properties, set_shiny_properties
from globals import ROCK_BASE


# calls seperate functions for setting up the sword in rock scene.
def draw_rocks_and_sword(x,y,z):
    # set rock to be matte
    set_matte_properties()
    draw_rock(x, y, z, ROCK_BASE, "rock_texture.png")
    # set sword to be shiny
    set_shiny_properties()
    draw_sword(x+(1/2)*ROCK_BASE,y+ROCK_BASE,z-(1/2)*ROCK_BASE)
    # set rock to be matte
    set_matte_properties()
    draw_rock(x+ROCK_BASE, y, z, (2/3)*ROCK_BASE, "rock2_texture.png")
    draw_rock(x-(4/5)*ROCK_BASE, y, z-(1/2)*ROCK_BASE, (3/4)*ROCK_BASE, "rock2_texture.png")
    draw_rock(x, y, z+(1/3)*ROCK_BASE, (1/3)*ROCK_BASE, "rock2_texture.png")



# sets up parameters for a rock with give parameters
def draw_rock(x, y, z, rock_base, texture_name):
    rock_gap = int((1/4)*rock_base+1)
    rock_texture_id = load_texture(texture_name)
    vertices = [#base 0-3
                (x, y, z),
                (x, y, z-rock_base),
                (x+rock_base, y, z),
                (x+rock_base, y, z-rock_base),
                #top 4-7
                (x, y+rock_base, z),
                (x, y+rock_base, z-rock_base),
                (x+rock_base, y+rock_base, z),
                (x+rock_base, y+rock_base, z-rock_base),
                #sides
                #move on x 8-11
                (x+rock_gap, y+rock_gap, z+rock_gap),
                (x+rock_base-rock_gap, y+rock_gap, z+rock_gap),
                (x+rock_gap, y+rock_base-rock_gap, z+rock_gap),
                (x+rock_base-rock_gap, y+rock_base-rock_gap, z+rock_gap),
                #move on z 12-15
                (x-rock_gap, y+rock_gap, z-rock_gap),
                (x-rock_gap, y+rock_gap, z-rock_base+rock_gap),
                (x-rock_gap, y+rock_base-rock_gap, z-rock_gap),
                (x-rock_gap, y+rock_base-rock_gap, z-rock_base+rock_gap),
                #move on x other side 16-19
                (x+rock_gap, y+rock_gap, z-rock_base-rock_gap),
                (x+rock_base-rock_gap, y+rock_gap, z-rock_base-rock_gap),
                (x+rock_gap, y+rock_base-rock_gap, z-rock_base-rock_gap),
                (x+2*rock_gap, y+rock_base-rock_gap, z-rock_base-rock_gap),
                #move on z other side 20-23
                (x+rock_base+rock_gap, y+rock_gap, z-rock_gap),
                (x+rock_base+rock_gap, y+rock_gap, z-rock_base+rock_gap),
                (x+rock_base+rock_gap, y+rock_base-rock_gap, z-rock_gap),
                (x+rock_base+rock_gap, y+rock_base-rock_gap, z-rock_base+rock_gap),
                #on top 24-27
                (x+rock_gap, y+rock_base+rock_gap, z-rock_gap),
                (x+rock_base-rock_gap, y+rock_base+rock_gap, z-rock_gap),
                (x+rock_gap, y+rock_base+rock_gap, z-rock_base+rock_gap),
                (x+rock_base-rock_gap, y+rock_base+rock_gap, z-rock_base-rock_gap)]
    indices = [(0,1,13,12),
               (0,4,14,12),
               (4,5,15,14),
               (1,5,15,13),
               (12,13,15,14),

               (1,3,17,16),
               (3,7,19,17),
               (7,5,18,19),
               (5,1,16,18),
               (16,17,19,18),

               (2,3,21,20),
               (3,7,23,21),
               (7,6,22,23),
               (6,2,20,22),
               (20,21,23,22),

               (0,2,9,8),
               (2,6,11,9),
               (6,4,10,11),
               (4,0,8,10),
               (8,9,11,10),

               (4,5,26,24),
               (5,7,27,26),
               (7,6,25,27),
               (6,4,24,25),
               (24,25,27,26)]
    
    draw_item_texture(vertices, indices, rock_texture_id, 1)


# Sets up parameters to draw a metallic sword in rocks.
def draw_sword(x,y,z):
    height_squar = 7
    width_on_z = 0.5
    width_on_x = 1.5
    vertices = [(x, y, z),
                (x+width_on_x, y, z),
                (x+width_on_x, y, z+width_on_z),
                (x, y, z+width_on_z),
                (x, y+height_squar, z),
                (x+width_on_x, y+height_squar, z),
                (x+width_on_x, y+height_squar, z+width_on_z),
                (x, y+height_squar, z+width_on_z),
                (x+width_on_x/2, y+height_squar+width_on_z/2, z+width_on_z/2)]
    indices = [((0, 1, 2, 3),0),
               ((0, 1, 5, 4),0),
               ((1, 2, 6, 5),0),
               ((3, 2, 6, 7),0),
               ((3, 0, 4, 7),0),
               ((4, 5, 6, 7),0)]
    

    # draw the sworf accorsing to the parameters.
    draw_item(vertices, indices, [(192/255,192/255,192/255)])



    # draws the hilt at give coordinates
    x, y, z = vertices[8]
    draw_hilt(x, y, z, 0, 4)
    draw_hilt(x, y+1, z, 90, 1.5)


# draws a wooden hilt at input parameters.
def draw_hilt(x,y,z,angle,len_z):
    wood_texture_id = load_texture("wood_texture.png")
    slices = 50
    stacks = 50
    len_x = 0.5
    len_y = 0.5

    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, wood_texture_id)

    glPushMatrix()
    glTranslatef(x,y,z)
    glRotate(angle,1,0,0)
    glScalef(len_x, len_y, len_z)

    quad = gluNewQuadric()
    gluQuadricTexture(quad, GL_TRUE)
    gluSphere(quad, 1, slices, stacks)

    glPopMatrix()

    glBindTexture(GL_TEXTURE_2D, 0)
    glDisable(GL_TEXTURE_2D)