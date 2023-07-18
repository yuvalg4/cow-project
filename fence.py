from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from utils import draw_item_texture
from texture import load_texture

NUM_PARTS = 20
CHANGE = 2

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

# gets buttom left pos
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