from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from utils import draw_quad_texture, draw_item_texture
from texture import load_texture

def draw_grass(centerX,centerZ):
    grass_texture_id = load_texture("grass_texture.png")
    #glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glColor3f(1, 1, 1)
    # diffuseColorArray = [1.0, 0.0, 0.0, 1.0]
    # ambientColorArray = [0.7529, 0.7529, 0.7529, 1.0]
    # glMaterial(GL_FRONT, GL_AMBIENT, ambientColorArray)
    # glMaterial(GL_FRONT, GL_DIFFUSE, diffuseColorArray)
   

    ambientColorArray = [0.5, 0.5, 0.5, 1.0]
    diffuseColorArray = [0.8, 0.8, 0.8, 1.0]
    specularColorArray = [0.2, 0.2, 0.2, 1.0]
    shininessValue = 10.0
    

    glMaterial(GL_FRONT, GL_AMBIENT, ambientColorArray)
    glMaterial(GL_FRONT, GL_DIFFUSE, diffuseColorArray)
    glMaterial(GL_FRONT, GL_SPECULAR, specularColorArray)
    glMaterial(GL_FRONT, GL_SHININESS, shininessValue)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)




    texture_size = 2
    # v1 = (-1*field_size, 0, -1*field_size)
    # v2 = (field_size, 0, -1*field_size)
    # v3 = (field_size, 0, field_size)
    # v4 = (-1*field_size, 0, field_size)
    #draw_quad_texture(v1, v2, v3, v4, grass_texture_id, texture_size)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, grass_texture_id)
    field_size = 500
    gridSize = 13
    cellSize = field_size / gridSize
    groundHeight = 0.0

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
