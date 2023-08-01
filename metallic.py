from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from texture import load_texture

def draw_metallic_object(center_x, center_y, center_z):
    sun_texture_id = load_texture("sun.png")
    ambientColorArray = [1, 1, 1, 1.0]
    diffuseColorArray = [0.1, 0.1, 0.1, 1.0]
    specularColorArray = [1.0, 1.0, 1.0, 1.0]
    shininessValue = 100.0
    glColor3f(0.714, 0.714, 0.714)

    # glMaterial(GL_FRONT, GL_AMBIENT, ambientColorArray)
    # glMaterial(GL_FRONT, GL_DIFFUSE, diffuseColorArray)
    # glMaterial(GL_FRONT, GL_SPECULAR, specularColorArray)
    # glMaterial(GL_FRONT, GL_SHININESS, shininessValue)
    # glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, sun_texture_id)

    glPushMatrix()
    glTranslatef(center_x, center_y, center_z)
    quad = gluNewQuadric()
    gluQuadricTexture(quad, GL_TRUE)
    gluSphere(quad, 5, 50, 50)
    #glScalef(len_x, len_y, len_z)
    glPopMatrix()
    glBindTexture(GL_TEXTURE_2D, 0)
    glDisable(GL_TEXTURE_2D)