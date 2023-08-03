from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from texture import load_texture
from light import set_matte_properties, set_shiny_properties, spotLoc
from utils import draw_item_texture, draw_quad_texture, draw_item
from globals import *


#draw grass grid with texture
def draw_grass(centerX,centerZ):
    #load texture
    grass_texture_id = load_texture("grass_texture.png")
    glColor3f(1, 1, 1)
    #set material properties to be matte
    set_matte_properties()
    #make 2 textures per block for higher resolution feel
    texture_size = 2
    field_size = 500
    gridSize = 20
    cellSize = field_size / gridSize
    groundHeight = 0.0

    # seperate the grass section into a grid and render each seperately. 
    # Enables light to show up properly on the ground.
    for x in range(gridSize):
        for z in range(gridSize):
            
            x0 = (centerX-field_size) / 2.0 + x * cellSize
            z0 = (centerZ-field_size) / 2.0 + z * cellSize
            # set normal
            normal = [0, 1, 0]
            p1 = [x0, groundHeight, z0]
            p2 = [x0 + cellSize, groundHeight, z0]
            p3 = [x0 + cellSize, groundHeight, z0 + cellSize]
            p4 = [x0, groundHeight, z0 + cellSize]

            draw_quad_texture(p1, p2, p3, p4, grass_texture_id, texture_size, normal)


def draw_lightpost():
    lightpost_texture_id = load_texture("metal_texture.png")

    #set up coordinates for rendering the light post. The tip is where the spotlight currently is.
    x, y, z = spotLoc[0], 0 , spotLoc[2]
    height_squar = spotLoc[1] - 4
    height_triangle = 2
    width_on_z = 1
    width_on_x = 1.5
    vertices = [(x, y, z),
                (x+width_on_x, y, z),
                (x+width_on_x, y, z+width_on_z),
                (x, y, z+width_on_z),
                (x, y+height_squar, z),
                (x+width_on_x, y+height_squar, z),
                (x+width_on_x, y+height_squar, z+width_on_z),
                (x, y+height_squar, z+width_on_z),
                (x+width_on_x/2, y+height_squar+height_triangle, z+width_on_z/2)]
    indices = [(0, 1, 2, 3),
               (0, 1, 5, 4),
               (1, 2, 6, 5),
               (3, 2, 6, 7),
               (3, 0, 4, 7), 
               (4, 5, 8),
               (5, 6, 8),
               (6, 7, 8),
               (4, 7, 8)]
    
    draw_item_texture(vertices, indices,lightpost_texture_id, 1)
    draw_lamp_head()

    #for debugging spotlight with a line
    lineWidth = 2.0
    glLineWidth(lineWidth)
    glColor3f(1.0, 1.0, 0.0)  # Yellow color

    # Render the line representing the spotlight
    glBegin(GL_LINES)
    glVertex3f(spotLoc[0], spotLoc[1], spotLoc[2])  # Line start point
    glVertex3f(spotLoc[0] + spotDir[0], spotLoc[1]+ spotDir[1], spotLoc[2] + spotDir[2])      # Line end point
    glEnd()
    
   
# renders the head of the lightpost as a cone
def draw_lamp_head():
    x, y, z = spotLoc[0], spotLoc[1] , spotLoc[2]
    glEnable(GL_BLEND)
    #enable blending so the cone lets light through and set up parameters
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glColor4f(1, 0.961, 0.714, 0.8)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, (1.0, 1.0, 1.0, 1.0))
    glMaterialfv(GL_FRONT, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))
    glMaterialfv(GL_FRONT, GL_SHININESS, 100)
    glPushMatrix()
    
    glTranslatef(x+0.75, y-2, z+0.5 )
    # glRotate(145, 0, 1, 0)
    # glRotate(-25, 1, 0, 0)

    quad = gluNewQuadric()
    gluSphere(quad, 3, 50, 50)
    
    glPopMatrix()
    glDisable(GL_BLEND)


# draws the sun in the sky as a sphere at set coordinates.
def draw_sun(center_x, center_y, center_z):
    sun_texture_id = load_texture("sun.png")
    glColor3f(0.714, 0.714, 0.714)

    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, sun_texture_id)

    glPushMatrix()
    glTranslatef(center_x, center_y, center_z)
    quad = gluNewQuadric()
    gluQuadricTexture(quad, GL_TRUE)
    gluSphere(quad, 5, 50, 50)
    glPopMatrix()

    glBindTexture(GL_TEXTURE_2D, 0)
    glDisable(GL_TEXTURE_2D)
    

# A looping function that draws 20 fence pickets.
def draw_fence(x, y, z):
    glColor3f(1, 1, 1)
    for i in range(NUM_PARTS):
        draw_one_part_fence(x, y, z)
        x += CHANGE
    for i in range(NUM_PARTS):
        draw_one_part_fence(x, y, z)
        z -= CHANGE
    for i in range(NUM_PARTS):
        draw_one_part_fence(x, y, z)
        x -= CHANGE

# gets buttom left pos and draws the picket.
def draw_one_part_fence(x, y, z):
    fence_texture_id = load_texture("wood_texture.png")
    
    height_squar = 7
    height_triangle = 2
    width_on_z = 1
    width_on_x = 1.5
    vertices = [(x, y, z),
                (x+width_on_x, y, z),
                (x+width_on_x, y, z+width_on_z),
                (x, y, z+width_on_z),
                (x, y+height_squar, z),
                (x+width_on_x, y+height_squar, z),
                (x+width_on_x, y+height_squar, z+width_on_z),
                (x, y+height_squar, z+width_on_z),
                (x+width_on_x/2, y+height_squar+height_triangle, z+width_on_z/2)]
    indices = [(0, 1, 2, 3),
               (0, 1, 5, 4),
               (1, 2, 6, 5),
               (3, 2, 6, 7),
               (3, 0, 4, 7), 
               (4, 5, 8),
               (5, 6, 8),
               (6, 7, 8),
               (4, 7, 8)]
    
    draw_item_texture(vertices, indices, fence_texture_id, 1)

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