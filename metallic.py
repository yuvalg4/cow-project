from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from texture import load_texture

def draw_metallic_object(center_x, center_y, center_z, len_x, len_y, len_z):
    ambientColorArray = [0.7529, 0.7529, 0.7529, 1.0]
    diffuseColorArray = [0.1, 0.1, 0.1, 1.0]
    specularColorArray = [1.0, 1.0, 1.0, 1.0]
    shininessValue = 100.0

    glMaterial(GL_FRONT, GL_AMBIENT, ambientColorArray)
    glMaterial(GL_FRONT, GL_DIFFUSE, diffuseColorArray)
    glMaterial(GL_FRONT, GL_SPECULAR, specularColorArray)
    glMaterial(GL_FRONT, GL_SHININESS, shininessValue)
    glMaterial(GL_FRONT, GL_DIFFUSE, diffuseColorArray)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glPushMatrix()
    glTranslatef(center_x, center_y, center_z)
    quad = gluNewQuadric()
    gluSphere(quad, 5, 50, 50)
    #glScalef(len_x, len_y, len_z)
    glPopMatrix()