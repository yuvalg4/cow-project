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
    texture_size = 10
    v1 = (-1*field_size, 0, -1*field_size)
    v2 = (field_size, 0, -1*field_size)
    v3 = (field_size, 0, field_size)
    v4 = (-1*field_size, 0, field_size)
    draw_quad_texture(v1, v2, v3, v4, grass_texture_id, texture_size)
   
   
    #draw using vertices
   
    # x, y, z = -0.5 * field_size, 0, - 0.5 * field_size
    
    # vertices = [(x, y , z),
    #             (x + field_size, y, z),
    #             (x + field_size, y, z + field_size),
    #             (x, y , z + field_size)]                
    # indices = [(0, 1, 2, 3)]
    # draw_item_texture(vertices, indices, grass_texture_id, texture_size)