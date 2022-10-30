import pygame   
from OpenGL.GL import *

class PyGL:
    def __init__(this, width, height):
        pygame.init()
        this.width = width
        this.height = height
        this.screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)

    def enableScissor(this, enable):
        if enable:
            glEnable(GL_SCISSOR_TEST)
        else:
            glDisable(GL_SCISSOR_TEST)

    def pixel(this, x, y, color, size = 1):
        glScissor(x, y, size, size)
        glClearColor(color[0], color[1], color[2], 1.0)
        glClear(GL_COLOR_BUFFER_BIT)
