
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image
import numpy as np
import math
from fence import draw_fence, NUM_PARTS, CHANGE
from cow import cow
from grass import draw_grass
from light import setup_lighting, updateLight, draw_lightpost
from light import spotLoc, spotDir, spotlight_exponent, global_ambient
from metallic import draw_metallic_object
import webbrowser

input_text = ""
cursor_position = 0
max_input_length = 20
input = False


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

tail_angle_l_r = 0
tail_angle_u_d = 0

body_angle = 0
body_loc = (0,0)
body_move = (0,0)

left_legs_angle = 0
right_legs_angle = 0
last_leg = "left"

part_of_body = "body"

x_fence = 4
cow_len_z = 6

def InitGlut():
    posX, posY = 100, 100
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
    glutInitWindowSize(winW, winH)
    glutInitWindowPosition(posX, posY)
    glutInit()
    window = glutCreateWindow("Project-Yuval Gabai and Yuval Safran")

def init():
    createMenu()
    setup_lighting()

    glClearColor(153/255, 1, 1, 1) # light blue bg
    
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)
    glLoadIdentity()
     


def myDisplay():
    global angle, winH, head_angle_l_r, head_angle_u_d, head_up_vector, left_legs_angle, right_legs_angle
    global tail_angle_l_r, tail_angle_u_d, body_loc, body_move, x_fence, cow_len_z
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


    draw_grass()
    draw_fence(x_fence, 0, 0) 

    draw_lightpost()

    draw_metallic_object(-20, 20, 0, 10, 10, 10)

    x, z = body_loc
    y = (4/3)*cow_len_z

    glPushMatrix()
    glTranslate(body_move[0],y,body_move[1])
    glRotatef(body_angle, 0, 1, 0)  
    glTranslate(-x,-y,-z)  
    cow(x, z, cow_len_z, head_angle_l_r, head_angle_u_d, tail_angle_l_r, tail_angle_u_d, left_legs_angle, right_legs_angle)
    glPopMatrix()

    body_loc = body_move

    # update legs when not moving
    left_legs_angle = 0
    right_legs_angle = 0

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
    global head_angle_l_r, head_angle_u_d, head_up_vector, spotLock, spotDir
    global spotlight_exponent, global_ambient, part_of_body
    global input_text, cursor_position, input
    
    if input == True:
        if key == b'\r' or key == b'\x03':  # Enter or Ctrl+C to finish input
            print("Entered data:", input_text)
            draw_text(5, 5, input_text)
            input_text = ""
            cursor_position = 0
            input = False
        elif key == b'\x08':  # Backspace to delete characters
            if cursor_position > 0:
                input_text = input_text[:cursor_position - 1] + input_text[cursor_position:]
                cursor_position -= 1
        elif key.isalnum() and len(input_text) < max_input_length:  # Allow alphanumeric characters
            input_text = input_text[:cursor_position] + key.decode('utf-8') + input_text[cursor_position:]
            cursor_position += 1
    
    else:
            
        move(key)

        if (key == b'g' or key == b'G') and spotLoc[0] > -1000:  # spotlight forward
            spotLoc[2] -= 1
            updateLight()
            #print("T clicked")

        elif (key == b't' or key == b'T' ) and spotLoc[0] < 1000: # spotlight backward
            part_of_body = "tail"
            spotLoc[2] += 1
            updateLight()

        elif (key == b'f' or key == b'F') and spotLoc[0] > -1000 and spotLoc[0] > -1000:  # spotlight right    
            spotLoc[0] += 1
            updateLight()
            #print("H clicked")

        elif (key == b'h' or key == b'H' ):  # spotlight left
            part_of_body = "head"
            spotLoc[0] -= 1
            updateLight()
            #print("F clicked")

        elif (key == b'v' or key == b'V') and spotLoc[1] < 120: # spotlight higher
            spotLoc[1] += 1
            updateLight()


        elif (key == b'B' or key == b'b') and spotLoc[1] > 0: # spotlight lower
            part_of_body = "body"

            spotLoc[1] -= 1
            updateLight()

        elif (key == b']') and spotlight_exponent[0] < 125: # spotlight stonger
            spotlight_exponent[0] += 5
            updateLight()

        elif (key == b'[') and spotlight_exponent[0] > 0: # spotlight weaker
            spotlight_exponent[0] -= 5
            updateLight()

        elif(key == b'0') and global_ambient[0] < 1.0:
            global_ambient[0] += 0.05 
            global_ambient[1] += 0.05
            global_ambient[2] += 0.05
            updateLight()

        elif(key == b'9') and global_ambient[0] > 0.0:
            global_ambient[0] -= 0.05 
            global_ambient[1] -= 0.05
            global_ambient[2] -= 0.05
            updateLight()

            
        else:
            return
    
    reshape(winW, winH)
    glutPostRedisplay()

def move(key):
    global head_angle_l_r, head_angle_u_d, head_up_vector, part_of_body, body_loc, body_move, last_leg
    global tail_angle_l_r, tail_angle_u_d, body_angle, left_legs_angle, right_legs_angle, x_fence, cow_len_z

    # Explanation of cheking in body movement:
    # fence from (x_fence,0,0) to (x_fence + CHANGE*NUM_PARTS,0,0)
    bounds_z_up = (0 - (2/3)*cow_len_z, 0 + (2/3)*cow_len_z)
    # then from (x_fence + CHANGE*NUM_PARTS,0,0) to (x_fence + CHANGE*NUM_PARTS,0,CHANGE*NUM_PARTS)
    bounds_x = (x_fence + CHANGE*NUM_PARTS - (2/3)*cow_len_z, x_fence + CHANGE*NUM_PARTS + (2/3)*cow_len_z)
    # then from (x_fence + CHANGE*NUM_PARTS,0,CHANGE*NUM_PARTS) to (x_fence,0,CHANGE*NUM_PARTS)
    bounds_z_down = (-1*CHANGE*NUM_PARTS + (2/3)*cow_len_z, -1*CHANGE*NUM_PARTS - (2/3)*cow_len_z)

    if (key == b'j' or key == b'J'):
        if part_of_body == "body":
            body_angle += 5
            if body_angle >= 360:
                body_angle -= 360
        
        elif part_of_body == "head" and head_angle_l_r < 30:
            head_angle_l_r += 5

        elif part_of_body == "tail" and tail_angle_l_r > -25:
            tail_angle_l_r -= 5
        
    elif (key == b'l' or key == b'L'):
        if part_of_body == "body":
            body_angle -= 5
            if body_angle < 0:
                body_angle += 360
        
        elif part_of_body == "head" and head_angle_l_r > -30:
            head_angle_l_r -= 5

        elif part_of_body == "tail" and tail_angle_l_r < 25:
            tail_angle_l_r += 5

    elif (key == b'i' or key == b'I'):
        if part_of_body == "body":
            x, z = body_loc

            if 0 <= body_angle < 90:
                alpha = math.radians(body_angle)
                body_move = (x - 5*math.sin(alpha),z - 5*math.cos(alpha))

            elif 90 <= body_angle < 180:
                alpha = math.radians(body_angle - 90)
                body_move = (x - 5*math.cos(alpha),z + 5*math.sin(alpha))

            elif 180 <= body_angle < 270:
                alpha = math.radians(body_angle - 180)
                body_move = (x + 5*math.sin(alpha),z + 5*math.cos(alpha))

            elif 270 <= body_angle < 360:
                alpha = math.radians(body_angle - 270)
                body_move = (x + 5*math.cos(alpha),z - 5*math.sin(alpha))

            if ((z < bounds_z_up[0] <= body_move[1] or body_move[1] < bounds_z_up[1] <= z) and 
                x_fence + CHANGE*NUM_PARTS > x > x_fence) or (
                (x < bounds_x[0] <= body_move[0] or body_move[0] < bounds_x[1] <= x) and
                0 > z > -1*CHANGE*NUM_PARTS) or (
                (z > bounds_z_down[0] >= body_move[1] or body_move[1] > bounds_z_down[1] >= z) and
                x_fence + CHANGE*NUM_PARTS > x > x_fence):
                body_move = body_loc
             
            if last_leg == "left":
                left_legs_angle = -10
                right_legs_angle = 10
                last_leg = "right"

            elif last_leg == "right":
                left_legs_angle = 10
                right_legs_angle = -10
                last_leg = "left"
        
        elif part_of_body == "head" and head_angle_u_d < 15:
            head_angle_u_d += 5

        elif part_of_body == "tail" and tail_angle_u_d > -50:
            tail_angle_u_d -= 5

    elif (key == b'k' or key == b'K'):
        if part_of_body == "body":
            x, z = body_loc

            if 0 <= body_angle < 90:
                alpha = math.radians(body_angle)
                body_move = (x + 5*math.sin(alpha),z + 5*math.cos(alpha))

            elif 90 <= body_angle < 180:
                alpha = math.radians(body_angle - 90)
                body_move = (x + 5*math.cos(alpha),z - 5*math.sin(alpha))

            elif 180 <= body_angle < 270:
                alpha = math.radians(body_angle - 180)
                body_move = (x - 5*math.sin(alpha),z - 5*math.cos(alpha))

            elif 270 <= body_angle < 360:
                alpha = math.radians(body_angle - 270)
                body_move = (x - 5*math.cos(alpha),z + 5*math.sin(alpha))

            if ((z > bounds_z_up[1] >= body_move[1] or body_move[1] > bounds_z_up[0] >= z) and 
                x_fence + CHANGE*NUM_PARTS > x > x_fence) or (
                (x > bounds_x[1] >= body_move[0] or body_move[0] > bounds_x[0] >= x) and
                0 > z > -1*CHANGE*NUM_PARTS) or (
                (z < bounds_z_down[1] <= body_move[1] or body_move[1] < bounds_z_down[0] <= z) and
                x_fence + CHANGE*NUM_PARTS > x > x_fence):
                body_move = body_loc

            if last_leg == "left":
                left_legs_angle = -10
                right_legs_angle = 10
                last_leg = "right"

            elif last_leg == "right":
                left_legs_angle = 10
                right_legs_angle = -10
                last_leg = "left"
        
        elif part_of_body == "head" and head_angle_u_d > -30:
            head_angle_u_d -= 5

        elif part_of_body == "tail" and tail_angle_u_d < 0:
            tail_angle_u_d += 5

#### Callbacks ####
def RegisterCallbacks():
    glutDisplayFunc(myDisplay)
    glutIdleFunc(myDisplay)
    glutKeyboardFunc(keyboard)
    glutReshapeFunc(reshape)

def ProcessMenu(value):
    global input
    if value == 1 :
        glutLeaveMainLoop()

    if value == 2:
        webbrowser.open("help.txt")

    if value == 3:
       draw_ambient_input()
       input = True 
       
    return 1


def createMenu():
    
    glutAddMenuEntry("Exit", 1)
    glutAddMenuEntry("Help", 2)
    glutAddMenuEntry("Set Ambient Light", 3)
    glutAttachMenu(GLUT_RIGHT_BUTTON)

def draw_text(x, y, text):
    glWindowPos2f(x, y)
    for character in text:
        glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(character))

def draw_ambient_input():
    glClear(GL_COLOR_BUFFER_BIT)
    # Implement your rendering here

    # Draw the data entry area
    glColor3f(0.8, 0.8, 0.8)
    glBegin(GL_QUADS)
    glVertex2f(100, 100)
    glVertex2f(300, 100)
    glVertex2f(300, 140)
    glVertex2f(100, 140)
    glEnd()

    # Draw the entered text
    glColor3f(0, 0, 0)
    draw_text(105, 110, input_text)

    glFlush()


def main():
    InitGlut()
    glutCreateMenu(ProcessMenu)
    init()
    RegisterCallbacks()
    glutMainLoop()

if __name__ == '__main__':
    main()

