from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from utils import draw_item_texture
from texture import load_texture
from globals import *
from utils import translation_matrix, rotation_matrix_y
import numpy as np
import math


def setup_lighting():

    # Enable lighting options for scene.
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0) 
    glEnable(GL_LIGHT1)
    glEnable(GL_NORMALIZE)
    glShadeModel(GL_SMOOTH)
    
    # Set light parameters for sunlight
    sunlight_position = [-20, 20, -20, 0.0] 
    ambient_light = [0.1, 0.1, 0.1, 1.0]  
    diffuse = [0.3, 0.3, 0.3, 1.0] 
    specular = [0.5, 0.5, 0.5, 1.0] 
    
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, global_ambient)

    glLightfv(GL_LIGHT0, GL_POSITION, sunlight_position)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambient_light)
    glLightfv(GL_LIGHT0, GL_SPECULAR, specular)

    # Set light parameters for spotlight
    spotlight_color = [1.0, 1.0, 1.0, 1.0]  
    spotlight_cutoff = 40.0  
    light_diffuse = [1, 1, 1, 1.0]  
    light_specular = [1, 1, 1, 1.0]  
    

    glLightfv(GL_LIGHT1, GL_DIFFUSE, spotlight_color)
    glLightfv(GL_LIGHT1, GL_SPECULAR, spotlight_color)
    glLightfv(GL_LIGHT1, GL_POSITION, spotLoc)
    glLightfv(GL_LIGHT1, GL_SPOT_DIRECTION, spotDir)
    glLightf(GL_LIGHT1, GL_SPOT_CUTOFF, spotlight_cutoff)
    glLightf(GL_LIGHT1, GL_SPOT_EXPONENT, spotlight_exponent[0])
    glLightfv(GL_LIGHT1, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT1, GL_SPECULAR, light_specular)
    
    #enable GL Color rendering for front and back.
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    

    return

# updates light location for scene recalculation
# global coordiantes are updated before calling
def updateLight():
    global spotDir, spotLoc, spotlight_exponent
    glEnable(GL_NORMALIZE)
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, global_ambient)
    glLightfv(GL_LIGHT1, GL_POSITION, spotLoc)
    glLightf(GL_LIGHT1, GL_SPOT_EXPONENT, spotlight_exponent[0])
    glLightfv(GL_LIGHT1, GL_SPOT_DIRECTION, spotDir)
    

def spot_rotate(theta):
    global spotDir
    #matrix = translation_matrix(spotLoc[0], spotLoc[1], spotLoc[2]) @ rotation_matrix_y(math.radians(theta)) @ translation_matrix(-spotLoc[0], -spotLoc[1], -spotLoc[2])
    spotDir_homogen = np.array([spotDir[0], spotDir[1], spotDir[2], 0])
    spotDir_homogen = rotation_matrix_y(math.radians(theta)) @ spotDir_homogen
    spotDir[0] = spotDir_homogen[0] #/ spotDir_homogen[3] 
    spotDir[1] = spotDir_homogen[1] #/ spotDir_homogen[3]
    spotDir[2] = spotDir_homogen[2] #/ spotDir_homogen[3]
    print("Direction: ", spotDir)
    
    # print("Homogen: ",spotDir_homogen)
    # print("spot loc: ", spotLoc)
    updateLight()


# Settings for all objects to be rendered. 
def set_matte_properties():
    mat_ambient = [0.2, 0.2, 0.2, 1.0]  
    mat_diffuse = [0.8, 0.8, 0.8, 1.0]   
    mat_specular = [0.0, 0.0, 0.0, 1.0]  
    mat_shininess = 0.0                  
  
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, mat_shininess) 



# Settings for all shiny/metallic to be rendered. 
def set_shiny_properties():
    mat_ambient = [0.1, 0.1, 0.1, 1.0]   
    mat_diffuse = [0.5, 0.5, 0.5, 1.0]   
    mat_specular = [0.9, 0.9, 0.9, 1.0] 
    mat_shininess = 100.0               

    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, mat_shininess) 
    