from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from texture import load_texture
from light import set_matte_properties, spotLoc
from utils import draw_item_texture
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
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, grass_texture_id)
    field_size = 500
    gridSize = 13
    cellSize = field_size / gridSize
    groundHeight = 0.0

    # seperate the grass section into a grid and render each seperately. 
    # Enables light to show up properly on the ground.
    for x in range(gridSize):
        for z in range(gridSize):
            glBegin(GL_QUADS)
            
            x0 = (centerX-field_size) / 2.0 + x * cellSize
            z0 = (centerZ-field_size) / 2.0 + z * cellSize
            glTexCoord2f(0.0, 0.0)  
            glVertex3f(x0, groundHeight, z0)
            glTexCoord2f(texture_size, 0.0)

            glVertex3f(x0 + cellSize, groundHeight, z0)
            glTexCoord2f(texture_size, texture_size)

            glVertex3f(x0 + cellSize, groundHeight, z0 + cellSize)
            glTexCoord2f(0.0, texture_size)

            glVertex3f(x0, groundHeight, z0 + cellSize)

            glEnd()

    glDisable(GL_TEXTURE_2D)


def draw_lightpost():
    lightpost_texture_id = load_texture("metal_texture.png")

    #set up coordinates for rendering the light post. The tip is where the spotlight currently is.
    x, y, z = spotLoc[0], 0 , spotLoc[2]
    height_squar = spotLoc[1] - 2
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
    # lineWidth = 2.0
    # glLineWidth(lineWidth)
    # glColor3f(1.0, 1.0, 0.0)  # Yellow color

    # # Render the line representing the spotlight
    # glBegin(GL_LINES)
    # glVertex3f(spotLoc[0], spotLoc[1], spotLoc[2])  # Line start point
    # glVertex3f(spotLoc[0] + spotDir[0], spotLoc[1]+ spotDir[1], spotLoc[2] + spotDir[2])      # Line end point
    # glEnd()
    
   
# renders the head of the lightpost as a cone
def draw_lamp_head():
    x, y, z = spotLoc[0], 0 , spotLoc[2]
    glEnable(GL_BLEND)
    #enable blending so the cone lets light through and set up parameters
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glColor4f(1, 0.961, 0.714, 0.8)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, (1.0, 1.0, 1.0, 1.0))
    glMaterialfv(GL_FRONT, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))
    glMaterialfv(GL_FRONT, GL_SHININESS, 100)
    glPushMatrix()
    
    glTranslatef(x - 1 , spotLoc[1]-1.5, z + 3.5)
    glRotate(145, 0, 1, 0)
    glRotate(-25, 1, 0, 0)

    gluCylinder(gluNewQuadric(), 3.0, 0.0, 5.0, 10, 10)  # Draw the cone
    
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