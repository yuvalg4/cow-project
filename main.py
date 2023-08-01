from project import InitGlut, init, RegisterCallbacks
from OpenGL.GLUT import *
import webbrowser


def main():
    InitGlut()
    init()
    RegisterCallbacks()
    webbrowser.open("Welcome.txt")
    glutMainLoop()

if __name__ == '__main__':
    main()