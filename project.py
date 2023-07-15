
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image
import numpy as np
import time
import math
from fence import draw_fence
from cow import cow
from grass import draw_grass
from light import setup_lighting, updateLight, draw_lightpost
from light import spotLoc, spotDir, spotlight_exponent, global_ambient
from metallic import draw_metallic_object

# golbals
winW, winH = 500, 500
angle = 0

# eye parameters
near_view_plane = 0.1
far_view_plane = 100
angle_view_plane = 60
eyeX, eyeY, eyeZ = 0, 20, -60
refX, refY, refZ = 0, 0, 0
upX, upY, upZ = 0, 1, 0

head_angle_l_r = 0
head_angle_u_d = 0
head_up_vector = (0, 1, 0)

left_legs_angle = 10
right_legs_angle = -10

def InitGlut():
    posX, posY = 100, 100
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
    glutInitWindowSize(winW, winH)
    glutInitWindowPosition(posX, posY)
    glutInit()
    window = glutCreateWindow("Project-Yuval Gabai and Yuval Safran")

def init():
    global grass_texture_id
    glClearColor(153/255, 1, 1, 1) # light blue bg
    setup_lighting()
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)
    glLoadIdentity()
     
def myDisplay():
    global angle, winH, head_angle_l_r, head_angle_u_d, head_up_vector, left_legs_angle, right_legs_angle
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    left_legs_angle, right_legs_angle = right_legs_angle, left_legs_angle

    draw_grass()
    draw_fence(4, 0, 0)

    draw_lightpost()
    draw_metallic_object(-20, 20, 0, 10, 10, 10)
    updateLight()

    glPushMatrix()
    glRotatef(angle, 0, 1, 0)
    cow(0, 0, 6, head_angle_l_r, head_angle_u_d, left_legs_angle, right_legs_angle)
    glPopMatrix()

    angle += 8
    angle %= 360.0
    time.sleep(0.1)

    glutSwapBuffers()   

def show_text(text, xpos, ypos):
    glRasterPos2f(xpos, ypos)
    for c in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))

def reshape(width, height):
    global winW, winH, projection_type
    winW = width
    winH = height
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    aspect = float(width) / height
    gluPerspective(angle_view_plane, aspect, near_view_plane, far_view_plane)
    gluLookAt(eyeX, eyeY, eyeZ, refX, refY, refZ, upX, upY, upZ)
    
    glMatrixMode(GL_MODELVIEW)
    

def keyboard(key, x, y):
    global head_angle_l_r, head_angle_u_d, head_up_vector, spotLock, spotDir, spotlight_exponent, global_ambient
    
    if (key == b'j' or key == b'J') and head_angle_l_r < 30:
        head_angle_l_r += 5
        
    elif (key == b'l' or key == b'L') and head_angle_l_r > -30:
        head_angle_l_r -= 5

    elif (key == b'i' or key == b'I') and head_angle_u_d > -15:
        head_angle_u_d -= 5

    elif (key == b'k' or key == b'K') and head_angle_u_d < 15:
        head_angle_u_d += 5

    elif (key == b'g' or key == b'G') and spotLoc[0] > -1000:  # spotlight forward
        spotLoc[2] -= 1
        print("T clicked")

    elif (key == b't' or key == b'T' ) and spotLoc[0] < 1000: # spotlight backward
        spotLoc[2] += 1

    elif (key == b'f' or key == b'F') and spotLoc[0] > -1000 and spotLoc[0] > -1000:  # spotlight right    
        spotLoc[0] += 1
        print("H clicked")

    elif (key == b'h' or key == b'H' ):  # spotlight left
        spotLoc[0] -= 1
        print("F clicked")

    elif (key == b'v' or key == b'V') and spotLoc[1] < 120: # spotlight higher
        spotLoc[1] += 1

    elif (key == b'B' or key == b'b') and spotLoc[1] > 0: # spotlight lower
        spotLoc[1] -= 1

    elif (key == b']') and spotlight_exponent[0] < 125: # spotlight stonger
        spotlight_exponent[0] += 5

    elif (key == b'[') and spotlight_exponent[0] > 0: # spotlight weaker
        spotlight_exponent[0] -= 5

    elif(key == b'0') and global_ambient[0] < 1.0:
        global_ambient[0] += 0.05 
        global_ambient[1] += 0.05
        global_ambient[2] += 0.05

    elif(key == b'9') and global_ambient[0] > 0.0:
        global_ambient[0] -= 0.05 
        global_ambient[1] -= 0.05
        global_ambient[2] -= 0.05
        
    else:
        return
    
    reshape(winW, winH)
    glutPostRedisplay()

#### Callbacks ####
def RegisterCallbacks():
    glutDisplayFunc(myDisplay)
    glutIdleFunc(myDisplay)
    glutKeyboardFunc(keyboard)
    glutReshapeFunc(reshape)

def main():
    InitGlut()
    init()
    RegisterCallbacks()
    glutMainLoop()

if __name__ == '__main__':
    main()

