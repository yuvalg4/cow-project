from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from tkinter import Tk, simpledialog
from light import updateLight
import webbrowser
from light import global_ambient

# Initiate main menu structure:
# - Help 
# - Set ambient sub menu
# - Exit
def createMainMenu():
    ambientMenu = glutCreateMenu(ProcessAmbientMenu)
    createAmbientMenu()
    glutCreateMenu(ProcessMenu)
    glutAddMenuEntry("Help", 2)
    glutAddSubMenu("Adjust Ambient Light", ambientMenu)
    glutAddMenuEntry("Exit", 1)
    glutAttachMenu(GLUT_RIGHT_BUTTON)


#Set up submenu for ambient lighting settings.
# - Set Red Ambient Value
# - Set Green Ambient Value
# - Set Blue Ambient Value
# - Reset To Default: resets to 0.3,0.3,0.3
def createAmbientMenu():
    glutAddMenuEntry("Set Red Ambient Value", 1)
    glutAddMenuEntry("Set Green Ambient Value", 2)
    glutAddMenuEntry("Set Blue Ambient Value", 3)
    glutAddMenuEntry("Reset To Default", 4)

# processes menu help and exit buttons
def ProcessMenu(value):
    #exits the window
    if value == 1 :
        glutLeaveMainLoop()

    #calls file and opens it
    if value == 2:
        webbrowser.open("Hello and welcome to Cow World.pdf")
       
    return 1

#Calls a pop up requesting values for the relevant color
def ProcessAmbientMenu(value):
    global global_ambient
    if value == 1 :
        #print("starting ambient R setting")
        user_input = popUpInput("Red Value Setting", "Input Ambient R Value (0-1)")
        if user_input != None:
            #print(f'user input is: ',user_input)
            global_ambient[0] = float(user_input)
            #print("updated ambient R")

    elif value == 2:
        #print("starting ambient G setting")
        user_input = popUpInput("Green Value Setting", "Input Ambient G Value (0-1)")
        if user_input != None:
            #print(f'user input is: ',user_input)
            global_ambient[1] = float(user_input)
            #print("updated ambient G")

    elif value == 3:
        #print("starting ambient B setting")
        user_input = popUpInput("Blue Value Setting", "Input Ambient B Value (0-1)")
        if user_input != None:
            #print(f'user input is: ',user_input)
            global_ambient[2] = float(user_input)
            #print("updated ambient B")
    
    elif value == 4:
        global_ambient[0], global_ambient[1], global_ambient[2] = 0.3, 0.3, 0.3 
       
    updateLight()
    return 1


#Pop up functions that creates the window and shows the prompt
def popUpInput(winTitle, winPrompt):
    root = Tk()
    root.withdraw()
    userInput = -1
    #run while the input is illegal and not cancelled by user.
    while userInput != None:
        userInput = simpledialog.askfloat(title=winTitle, prompt=winPrompt)
        #only accept input between 0-1
        if userInput != None and userInput >= 0 and userInput <= 1:
            root.destroy()
            return userInput
    
    root.destroy()
    return userInput
