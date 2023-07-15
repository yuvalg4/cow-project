from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from utils import draw_quad_texture
from texture import load_texture

def draw_grass():
    grass_texture_id = load_texture("grass_texture.png")
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    field_size = 100
    texture_size = 10
    v1 = (-1*field_size, 0, -1*field_size)
    v2 = (field_size, 0, -1*field_size)
    v3 = (field_size, 0, field_size)
    v4 = (-1*field_size, 0, field_size)
    draw_quad_texture(v1, v2, v3, v4, grass_texture_id, texture_size)