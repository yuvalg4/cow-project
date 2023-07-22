from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image

def draw_item_texture(vertices, indices, texture_id, texture_size):
    for ind in indices:
        if len(ind) == 4: # quad
            draw_quad_texture(vertices[ind[0]], vertices[ind[1]], vertices[ind[2]], vertices[ind[3]], texture_id, texture_size)
        elif len(ind) == 3: # triengle
            draw_triengle_texture(vertices[ind[0]], vertices[ind[1]], vertices[ind[2]], texture_id, texture_size)

def draw_quad_texture(v1, v2, v3, v4, texture_id, texture_size):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    
    glColor3f(1,1,1)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(v1[0], v1[1], v1[2])
    glTexCoord2f(texture_size, 0.0)
    glVertex3f(v2[0], v2[1], v2[2])
    glTexCoord2f(texture_size, texture_size)
    glVertex3f(v3[0], v3[1], v3[2])
    glTexCoord2f(0.0, texture_size)
    glVertex3f(v4[0], v4[1], v4[2])
    glEnd()

    
    

    glDisable(GL_TEXTURE_2D)

def draw_triengle_texture(v1, v2, v3, texture_id, texture_size):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    glBegin(GL_TRIANGLES)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(v1[0], v1[1], v1[2])
    glTexCoord2f(texture_size, 0.0)
    glVertex3f(v2[0], v2[1], v2[2])
    glTexCoord2f(texture_size/2, texture_size)
    glVertex3f(v3[0], v3[1], v3[2])
    glEnd()

    glDisable(GL_TEXTURE_2D)

def draw_item(vertices, indices, colors):
    for ind in indices:
        ver = ind[0]
        r, g, b = colors[ind[1]]
        glColor3f(r, g, b)
        if len(ver) == 4: # quad
            draw_quad(vertices[ver[0]], vertices[ver[1]], vertices[ver[2]], vertices[ver[3]])
        elif len(ver) == 3: # triengle
            draw_triengle(vertices[ver[0]], vertices[ver[1]], vertices[ver[2]])

def draw_quad(v1, v2, v3, v4):
    glBegin(GL_QUADS)
    glVertex3f(v1[0], v1[1], v1[2])
    glVertex3f(v2[0], v2[1], v2[2])
    glVertex3f(v3[0], v3[1], v3[2])
    glVertex3f(v4[0], v4[1], v4[2])
    glEnd()

def draw_triengle(v1, v2, v3):
    glBegin(GL_TRIANGLES)
    glVertex3f(v1[0], v1[1], v1[2])
    glVertex3f(v2[0], v2[1], v2[2])
    glVertex3f(v3[0], v3[1], v3[2])
    glEnd()