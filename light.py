from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from utils import draw_item_texture
from texture import load_texture

#spotlight params:
spotLoc = [16, 20, 0, 0]  # Position of the spotlight
spotDir = [-5, -5 , 5]  # Direction of the spotlight
spotlight_exponent = [20.0]  # Exponent that controls the intensity distribution of the spotlight
global_ambient = [0.4, 0.4, 0.4, 1.0] # global ambient lighting


def setup_lighting():

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0) 
    glEnable(GL_NORMALIZE)
    glEnable(GL_LIGHT1)

    # Set light parameters for sunlight
    #sunlight_position = [-30, 10, -20, 1.0]  # Position of the sunlight
    sunlight_color = [1.0, 1.0, 1.0, 1.0]  # Color of the sunlight
    ambient_light = [0.1, 0.1, 0.1, 1.0]  
    diffuse = [0.5, 0.5, 0.5, 1.0]  # K diffuse reflection
    specular = [0.5, 0.5, 0.5, 1.0]  # K Specular reflection
    
   
    shininess = 0



    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, global_ambient)

    #glLightfv(GL_LIGHT0, GL_POSITION, sunlight_position)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambient_light)
    glLightfv(GL_LIGHT0, GL_SPECULAR, specular)
    

    
    # Set light parameters for spotlight
    angle_cutoff = 180
    exp = 0
    aim = [1, 1 , 0]


    #spotLoc = [spotX, spotY, spotZ, 1.0]  # Position of the spotlight
    #spotDir = [dirX, dirY, dirZ]  # Direction of the spotlight
    spotlight_color = [1.0, 1.0, 1.0, 1.0]  # Color of the spotlight
    spotlight_cutoff = 40.0  # Angle (in degrees) within which the spotlight illuminates

    glLightfv(GL_LIGHT1, GL_DIFFUSE, spotlight_color)
    glLightfv(GL_LIGHT1, GL_SPECULAR, spotlight_color)
    glLightfv(GL_LIGHT1, GL_POSITION, spotLoc)
    glLightfv(GL_LIGHT1, GL_SPOT_DIRECTION, spotDir)
    glLightf(GL_LIGHT1, GL_SPOT_CUTOFF, spotlight_cutoff)
    glLightf(GL_LIGHT1, GL_SPOT_EXPONENT, spotlight_exponent[0])

    
    

    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    return

def updateLight():
    global spotDir, spotLoc, spotlight_exponent
    #spotlight_position = [spotX, spotY, spotZ, 1.0]  # Position of the spotlight
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, global_ambient)
    glLightfv(GL_LIGHT1, GL_POSITION, spotLoc)
    glLightf(GL_LIGHT1, GL_SPOT_EXPONENT, spotlight_exponent[0])
    #print("x is " + str(spotLoc))
    #print("exponent is" + str(spotlight_exponent[0]))
    
    lineWidth = 2.0
    glLineWidth(lineWidth)
    glColor3f(1.0, 1.0, 0.0)  # Yellow color

    # Render the line representing the spotlight
    glBegin(GL_LINES)
    glVertex3f(spotLoc[0], spotLoc[1], spotLoc[2])  # Line start point
    glVertex3f(spotLoc[0] + spotDir[0], spotLoc[1]+ spotDir[1], spotLoc[2] + spotDir[2])      # Line end point
    glEnd()
    # glPushMatrix()
    # glTranslatef(spotLoc[0], spotLoc[1], spotLoc[2])
    # quad = gluNewQuadric()
    # gluSphere(quad, 1, 50, 50)
    # #glScalef(len_x, len_y, len_z)
    # glPopMatrix()
    # glColor3f(1.0, 0.0, 0.0)  # Yellow color
    # glPushMatrix()
    # glTranslatef(spotLoc[0] + spotDir[0], spotLoc[1]+ spotDir[1], spotLoc[2] + spotDir[2])
    # quad = gluNewQuadric()
    # gluSphere(quad, 1, 50, 50)
    # #glScalef(len_x, len_y, len_z)
    # glPopMatrix()



def draw_lightpost():
    fence_texture_id = load_texture("metal_texture.png")

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
    
    draw_item_texture(vertices, indices, fence_texture_id, 1)
    