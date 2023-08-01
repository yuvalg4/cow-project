
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image
import numpy as np
import math
from fence import draw_fence, NUM_PARTS, CHANGE
from cow import cow
from general_objects import draw_grass, draw_lightpost, draw_sun
from light import setup_lighting, updateLight
from light import spotLoc, spotDir, spotlight_exponent, global_ambient, set_matte_properties, set_shiny_properties

import webbrowser
from rock import draw_rocks_and_sword
from menu import createMainMenu
from globals import *


def InitGlut():
    posX, posY = 100, 100
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
    glutInitWindowSize(winW, winH)
    glutInitWindowPosition(posX, posY)
    glutInit()
    window = glutCreateWindow("Project-Yuval Gabai and Yuval Safran")

def init():
    createMainMenu()
    setup_lighting()

    glClearColor(153/255, 1, 1, 1) # light blue bg
    
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)
    glLoadIdentity()
     
def myDisplay():
    global angle, winH, head_angle_l_r, head_angle_u_d, head_up_vector, left_legs_angle, right_legs_angle
    global tail_angle_l_r, tail_angle_u_d, body_loc, body_move, x_fence, cow_len_z
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # glEnable(GL_COLOR_MATERIAL)
    set_matte_properties()
    if point_of_view == 'camera':
        draw_grass(eyeX, eyeZ)
    else:
        draw_grass(body_loc[0], body_loc[1])

    draw_fence(x_fence, 0, 0) 
    # glDisable(GL_COLOR_MATERIAL)

    draw_rocks_and_sword(x_rock,-2,z_rock)
    set_shiny_properties()
    draw_lightpost()
    set_matte_properties()
    draw_sun(-20, 50, 80)

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
    global winW, winH, aspect
    winW = width
    winH = height
    aspect = float(winW) / winH
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(angle_view_plane, aspect, near_view_plane, far_view_plane)
    if point_of_view == "camera":
        gluLookAt(eyeX, eyeY, eyeZ, 0, 0, 0, 0, 1, 0)
    elif point_of_view == "cow":
        change_cow_eye_parameters()
        gluLookAt(cow_eyeX, cow_eyeY, cow_eyeZ, cow_refX, cow_refY, cow_refZ, 0, 1, 0)

    glMatrixMode(GL_MODELVIEW)

def change_cow_eye_parameters():
    global cow_eyeX, cow_eyeY, cow_eyeZ, cow_refX, cow_refY, cow_refZ

    matrix_neck = translation_matrix(body_move[0],(4/3)*cow_len_z,body_move[1]) @ rotation_matrix_y(
        np.radians(body_angle)) @ translation_matrix(0,-(4/3)*cow_len_z,0)
    
    neck_homogenic =  np.array([0, (14/9)*cow_len_z,-(3/7)*cow_len_z, 1])
    neck_homogenic = matrix_neck @ neck_homogenic
    neck_x = neck_homogenic[0]/neck_homogenic[3]
    neck_y = neck_homogenic[1]/neck_homogenic[3]
    neck_z = neck_homogenic[2]/neck_homogenic[3]

    cow_eye_homogenic = np.array([0, 2*cow_len_z, -(4/3)*cow_len_z, 1])
    cow_eye_homogenic = matrix_neck @ cow_eye_homogenic
    cow_eyeX = cow_eye_homogenic[0]/cow_eye_homogenic[3]
    cow_eyeY = cow_eye_homogenic[1]/cow_eye_homogenic[3]
    cow_eyeZ = cow_eye_homogenic[2]/cow_eye_homogenic[3]

    cow_ref_homogenic = np.array([0, 2*cow_len_z, -10, 1])
    cow_ref_homogenic = matrix_neck @ cow_ref_homogenic
    cow_refX = cow_ref_homogenic[0]/cow_ref_homogenic[3]
    cow_refY = cow_ref_homogenic[1]/cow_ref_homogenic[3]
    cow_refZ = cow_ref_homogenic[2]/cow_ref_homogenic[3]

    matrix = translation_matrix(neck_x,neck_y,neck_z) @ rotation_matrix_y(
        np.radians(head_angle_l_r + body_angle)) @ rotation_matrix_x(np.radians(head_angle_u_d)) @ rotation_matrix_y(
        np.radians(-body_angle)) @ translation_matrix(-neck_x,-neck_y,-neck_z)

    cow_eye_homogenic = np.array([cow_eyeX, cow_eyeY, cow_eyeZ, 1])
    cow_eye_homogenic = matrix @ cow_eye_homogenic
    cow_eyeX = cow_eye_homogenic[0]/cow_eye_homogenic[3]
    cow_eyeY = cow_eye_homogenic[1]/cow_eye_homogenic[3]
    cow_eyeZ = cow_eye_homogenic[2]/cow_eye_homogenic[3]

    cow_ref_homogenic = np.array([cow_refX, cow_refY, cow_refZ, 1])
    cow_ref_homogenic = matrix @ cow_ref_homogenic
    cow_refX = cow_ref_homogenic[0]/cow_ref_homogenic[3]
    cow_refY = cow_ref_homogenic[1]/cow_ref_homogenic[3]
    cow_refZ = cow_ref_homogenic[2]/cow_ref_homogenic[3]

def translation_matrix(tx, ty, tz):
    return np.array([[1, 0, 0, tx],
                     [0, 1, 0, ty],
                     [0, 0, 1, tz],
                     [0, 0, 0, 1]])

def rotation_matrix_x(theta):
    c = np.cos(theta)
    s = np.sin(theta)
    return np.array([[1, 0, 0, 0],
                     [0, c, -s, 0],
                     [0, s, c, 0],
                     [0, 0, 0, 1]])

def rotation_matrix_y(theta):
    c = np.cos(theta)
    s = np.sin(theta)
    return np.array([[c, 0, s, 0],
                     [0, 1, 0, 0],
                     [-s, 0, c, 0],
                     [0, 0, 0, 1]])

def keyboard(key, x, y):
    global head_angle_l_r, head_angle_u_d, head_up_vector, spotLock, spotDir
    global spotlight_exponent, global_ambient, part_of_body
    global cow_eyeX, cow_eyeY, cow_eyeZ, cow_refX, cow_refY, cow_refZ
    global eyeX, eyeY, eyeZ, point_of_view
    
    move(key)

    if (key == b's' or key == b'S'):  
        part_of_body = "spotlight"

    elif (key == b't' or key == b'T' ): 
        part_of_body = "tail"

    elif (key == b'b' or key == b'B' ): 
        part_of_body = "body"
    
    elif (key == b'h' or key == b'H' ): 
        part_of_body = "head"

    elif (key == b'c' or key == b'C'):
        part_of_body = "camera"
        point_of_view = "camera"
        
    elif key == b'p' or key == b'P':
        point_of_view = "cow"
        part_of_body = "body"

    reshape(winW, winH)
    glutPostRedisplay()

def move(key):
    global head_angle_l_r, head_angle_u_d, head_up_vector, part_of_body, body_loc, body_move, last_leg
    global tail_angle_l_r, tail_angle_u_d, body_angle, left_legs_angle, right_legs_angle, x_fence, cow_len_z
    global eyeX, eyeY, eyeZ, radius, camera_movement

    # Explanation of cheking in body movement:
    # fence from (x_fence,0,0) to (x_fence + CHANGE*NUM_PARTS,0,0)
    bounds_z_up = (0 - (2/3)*cow_len_z, 0 + (2/3)*cow_len_z)
    # then from (x_fence + CHANGE*NUM_PARTS,0,0) to (x_fence + CHANGE*NUM_PARTS,0,CHANGE*NUM_PARTS)
    bounds_x = (x_fence + CHANGE*NUM_PARTS - (2/3)*cow_len_z, x_fence + CHANGE*NUM_PARTS + (2/3)*cow_len_z)
    # then from (x_fence + CHANGE*NUM_PARTS,0,CHANGE*NUM_PARTS) to (x_fence,0,CHANGE*NUM_PARTS)
    bounds_z_down = (-1*CHANGE*NUM_PARTS + (2/3)*cow_len_z, -1*CHANGE*NUM_PARTS - (2/3)*cow_len_z)

    if (key == b'j' or key == b'J'):
        if part_of_body == "spotlight" :  # spotlight right    
            spotLoc[0] += 1
            updateLight()

        elif part_of_body == "body":
            body_angle += 5
            if body_angle >= 360:
                body_angle -= 360
        
        elif part_of_body == "head" and head_angle_l_r < 30:
            head_angle_l_r += 5

        elif part_of_body == "tail" and tail_angle_l_r > -25:
            tail_angle_l_r -= 5

        elif part_of_body == "camera":
            if eyeX == radius:
                eyeX -= 5
                camera_movement = "down"

            elif -eyeX == radius:
                eyeX += 5
                camera_movement = "up"

            elif camera_movement == "up":
                eyeX += 5
                if eyeX > radius:
                    eyeX = radius
            
            elif camera_movement == "down":
                eyeX -= 5
                if eyeX < -radius:
                    eyeX = -radius
                
            eyeZ = math.sqrt(math.pow(radius,2)-math.pow(eyeX,2))
            if camera_movement == "up":
                eyeZ = -eyeZ
            
    elif (key == b'l' or key == b'L'):
        if part_of_body == "spotlight":
            spotLoc[0] -= 1
            updateLight()
            #print("F clicked")

        elif part_of_body == "body":
            body_angle -= 5
            if body_angle < 0:
                body_angle += 360
        
        elif part_of_body == "head" and head_angle_l_r > -30:
            head_angle_l_r -= 5

        elif part_of_body == "tail" and tail_angle_l_r < 25:
            tail_angle_l_r += 5

        elif part_of_body == "camera":
            if eyeX == radius:
                eyeX -= 5
                camera_movement = "up"

            elif -eyeX == radius:
                eyeX += 5
                camera_movement = "down"

            elif camera_movement == "up":
                eyeX -= 5
                if eyeX < -radius:
                    eyeX = -radius
            
            elif camera_movement == "down":
                eyeX += 5
                if eyeX > radius:
                    eyeX = radius

            eyeZ = math.sqrt(math.pow(radius,2)-math.pow(eyeX,2))
            if camera_movement == "up":
                eyeZ = -eyeZ

    elif (key == b'i' or key == b'I'):
        if part_of_body == "spotlight":
            spotLoc[2] += 1
            updateLight()
        elif part_of_body == "body":
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

            # fence bounds
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

        elif part_of_body == "camera":
            if eyeY < HIGTH_CAM_MAX:
                eyeY += 5

    elif (key == b'k' or key == b'K'):

        if part_of_body == "spotlight":
            spotLoc[2] -= 1
            updateLight()

        elif part_of_body == "body":
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

        elif part_of_body == "camera":
            if eyeY > HIGTH_CAM_MIN:
                eyeY -= 5

    elif part_of_body == "camera" and (key == b'+' or key == b'-'):
        if key == b'+' and radius > RADIUS_CAM_MIN:
            change = -5

        elif key == b'-' and radius < RADIUS_CAM_MAX:
            change = 5
        else: # got to the bound of radius (mininum or maximum)
            change = 0
        
        eyeX = eyeX*((radius+change)/radius)
        eyeZ = eyeZ*((radius+change)/radius)
        radius += change

    elif (part_of_body == "spotlight"):
        if key == b'.':
            spotLoc[1] += 1
            updateLight()
        elif key == b',' and spotLoc[1] > 5:
            spotLoc[1] -= 1
            updateLight()

        elif (key == b']') and spotlight_exponent[0] < 120: # spotlight stonger
            spotlight_exponent[0] += 5
            updateLight()

        elif (key == b'[') and spotlight_exponent[0] > 0: # spotlight weaker
            spotlight_exponent[0] -= 5
            updateLight() 

        elif(key == b'0') and (global_ambient[0] < 1.0 and global_ambient[1] < 1.0 and global_ambient[2] < 1.0):
            global_ambient[0] += 0.05 
            global_ambient[1] += 0.05
            global_ambient[2] += 0.05
            updateLight()

        elif(key == b'9') and (global_ambient[0] > 0.0 and global_ambient[1] > 0.0 and global_ambient[2] > 0.0):
            global_ambient[0] -= 0.05 
            global_ambient[1] -= 0.05
            global_ambient[2] -= 0.05
            updateLight()

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
    webbrowser.open("Welcome.txt")
    glutMainLoop()

if __name__ == '__main__':
    main()

