from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image


# Helper function to load the texture to a parameter according to name.
# return an exception if it goes wrong.
def load_texture(file_name):
    try:
        image = Image.open(file_name)
        image_data = image.convert("RGBA").tobytes()
        width = image.width
        height = image.height

        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_MIRRORED_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

        glTexImage2D(
            GL_TEXTURE_2D,
            0,
            GL_RGBA,
            width,
            height,
            0,
            GL_RGBA,
            GL_UNSIGNED_BYTE,
            image_data,
        )

        glBindTexture(GL_TEXTURE_2D, 0)

        return texture_id

    except Exception as e:
        print(f"Error loading texture: {e}")
        return None
 