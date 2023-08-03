from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np


# input: a list of vertices, indices, texture, and texture size to be used.
# output: an item rendered of the input lists
# done by calling sub-functions for rendering each piece.
def draw_item_texture(vertices, indices, texture_id, texture_size):
    for ind in indices:
        if len(ind) == 4: # quad
            draw_quad_texture(vertices[ind[0]], vertices[ind[1]], vertices[ind[2]], vertices[ind[3]], texture_id, texture_size)
        elif len(ind) == 3: # triengle
            draw_triengle_texture(vertices[ind[0]], vertices[ind[1]], vertices[ind[2]], texture_id, texture_size)


# input: 4 3d vectors, a texture and a size
# output: render a quad with texture
def draw_quad_texture(v1, v2, v3, v4, texture_id, texture_size, normal = [0,0,0]):
    
    
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    # Map the texture to the quad while rendering.
    glColor3f(1,1,1)
    glBegin(GL_QUADS)
    
    glTexCoord2f(0.0, 0.0)
    if(normal[0] != 0 or normal[1] != 0 or normal[2] !=0): # when drawing grass - force normal to be (0,1,0) for proper lighting.
        glNormal3fv(normal) 
    glVertex3f(v1[0], v1[1], v1[2])
    glTexCoord2f(texture_size, 0.0)
    if(normal[0] != 0 or normal[1] != 0 or normal[2] !=0): # when drawing grass - force normal to be (0,1,0) for proper lighting.
        glNormal3fv(normal) 
    glVertex3f(v2[0], v2[1], v2[2])
    glTexCoord2f(texture_size, texture_size)
    if(normal[0] != 0 or normal[1] != 0 or normal[2] !=0): # when drawing grass - force normal to be (0,1,0) for proper lighting.
        glNormal3fv(normal) 
    glVertex3f(v3[0], v3[1], v3[2])
    glTexCoord2f(0.0, texture_size)
    if(normal[0] != 0 or normal[1] != 0 or normal[2] !=0): # when drawing grass - force normal to be (0,1,0) for proper lighting.
        glNormal3fv(normal) 
    glVertex3f(v4[0], v4[1], v4[2])
    glEnd()

    glDisable(GL_TEXTURE_2D)

# input: Three 3d vectors, a texture and a size
# output: render a triangle with texture
def draw_triengle_texture(v1, v2, v3, texture_id, texture_size):

    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    # Map the texture to the quad while rendering.
    glBegin(GL_TRIANGLES)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(v1[0], v1[1], v1[2])
    glTexCoord2f(texture_size, 0.0)
    glVertex3f(v2[0], v2[1], v2[2])
    glTexCoord2f(texture_size/2, texture_size)
    glVertex3f(v3[0], v3[1], v3[2])
    glEnd()

    glDisable(GL_TEXTURE_2D)

# input: a list of vertices, indices, and colors to be used.
# output: an item rendered of the input lists
# done by calling sub-functions for rendering each piece.
def draw_item(vertices, indices, colors):
    #traverse the indices
    for ind in indices:
        ver = ind[0]
        r, g, b = colors[ind[1]]
        glColor3f(r, g, b)
        if len(ver) == 4: # quad
            draw_quad(vertices[ver[0]], vertices[ver[1]], vertices[ver[2]], vertices[ver[3]])
        elif len(ver) == 3: # triengle
            draw_triangle(vertices[ver[0]], vertices[ver[1]], vertices[ver[2]])


# draw a quad out of 4 3d vectors.
def draw_quad(v1, v2, v3, v4):
    glBegin(GL_QUADS)
    glVertex3f(v1[0], v1[1], v1[2])
    glVertex3f(v2[0], v2[1], v2[2])
    glVertex3f(v3[0], v3[1], v3[2])
    glVertex3f(v4[0], v4[1], v4[2])
    glEnd()


# draw a triangle out of three 3d vectors
def draw_triangle(v1, v2, v3):
    glBegin(GL_TRIANGLES)
    glVertex3f(v1[0], v1[1], v1[2])
    glVertex3f(v2[0], v2[1], v2[2])
    glVertex3f(v3[0], v3[1], v3[2])
    glEnd()

def textured_sphere(center_x, center_y, center_z, len_x, len_y, len_z, texture_id):
    slices = 50
    stacks = 50

    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    glPushMatrix()
    glTranslatef(center_x, center_y, center_z)
    glScalef(len_x, len_y, len_z)

    quad = gluNewQuadric()
    gluQuadricTexture(quad, GL_TRUE)
    gluSphere(quad, 1, slices, stacks)

    glPopMatrix()

    glBindTexture(GL_TEXTURE_2D, 0)
    glDisable(GL_TEXTURE_2D)

def draw_solid_sphere(center_x, center_y, center_z, len_x, len_y, len_z):
    slices = 50
    stacks = 50
    glPushMatrix()
    glTranslatef(center_x, center_y, center_z)
    glScalef(len_x, len_y, len_z)
    glutSolidSphere(1, slices, stacks)
    glPopMatrix()

# Sets a translation matrix according to parameters for calculations
def translation_matrix(tx, ty, tz):
    return np.array([[1, 0, 0, tx],
                     [0, 1, 0, ty],
                     [0, 0, 1, tz],
                     [0, 0, 0, 1]])


# sets a rotation matrix according to parameters for calculations
def rotation_matrix_x(theta):
    c = np.cos(theta)
    s = np.sin(theta)
    return np.array([[1, 0, 0, 0],
                     [0, c, -s, 0],
                     [0, s, c, 0],
                     [0, 0, 0, 1]])

# Sets a rotation matrix according to parameters on second axis for calculations
def rotation_matrix_y(theta):
    c = np.cos(theta)
    s = np.sin(theta)
    return np.array([[c, 0, s, 0],
                     [0, 1, 0, 0],
                     [-s, 0, c, 0],
                     [0, 0, 0, 1]])