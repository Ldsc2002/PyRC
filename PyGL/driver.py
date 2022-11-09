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

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    GL.player['a'] += pi/10
                if event.key == pygame.K_LEFT:
                    GL.player['a'] -= pi/10
                if event.key == pygame.K_UP:
                    GL.player['y'] += 10
                if event.key == pygame.K_DOWN:
                    GL.player['y'] -= 10
