from PyGL.lib.PyGL import *
from random import *

GL = None

def checkInstanceOnCall(function):
    if GL is None: init()
    return function

def init(width: int = 1000, height: int = 500, pixelSize: int = 50) -> None:
    global GL
    GL = PyGL(width, height, pixelSize)

@checkInstanceOnCall
def runGame(file):
    GL.loadMap(file)

    running = True 

    while running:
        GL.render()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            running = False
        elif keys[pygame.K_w] or keys[pygame.K_UP]:
            GL.movePlayer("forward")
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            GL.movePlayer("backward")
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            GL.movePlayer("left")
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            GL.movePlayer("right")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
