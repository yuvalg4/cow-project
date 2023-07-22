from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from utils import draw_quad_texture, draw_item_texture
from texture import load_texture

def draw_grass():
    grass_texture_id = load_texture("grass_texture.png")
    #glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glColor3f(1, 1, 1)
    #glColor3f(1,1,1)
    diffuseColorArray = [0.7, 0.7, 0.7, 1.0]
    ambientColorArray = [0.7529, 0.7529, 0.7529, 1.0]
    glMaterial(GL_FRONT, GL_AMBIENT, ambientColorArray)
    glMaterial(GL_FRONT, GL_DIFFUSE, diffuseColorArray)
    field_size = 100
    texture_size = 1
    v1 = (-1*field_size, 0, -1*field_size)
    v2 = (field_size, 0, -1*field_size)
    v3 = (field_size, 0, field_size)
    v4 = (-1*field_size, 0, field_size)
    #draw_quad_texture(v1, v2, v3, v4, grass_texture_id, texture_size)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, grass_texture_id)
    gridSize = 5
    floorSize = field_size
    cellSize = floorSize / gridSize
    floorHeight = -1.0

    for x in range(gridSize):
        for z in range(gridSize):
            glBegin(GL_QUADS)
            

            x0 = -floorSize / 2.0 + x * cellSize
            z0 = -floorSize / 2.0 + z * cellSize
            glTexCoord2f(0.0, 0.0)  
            glVertex3f(x0, floorHeight, z0)
            glTexCoord2f(texture_size, 0.0)

            glVertex3f(x0 + cellSize, floorHeight, z0)
            glTexCoord2f(texture_size, texture_size)

            glVertex3f(x0 + cellSize, floorHeight, z0 + cellSize)
            glTexCoord2f(0.0, texture_size)

            glVertex3f(x0, floorHeight, z0 + cellSize)

            glEnd()
    glDisable(GL_TEXTURE_2D)
