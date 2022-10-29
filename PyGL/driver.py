from PyGL.lib.PyGL import *
from random import *

GL = None

def checkInstanceOnCall(function):
    if GL is None: init()
    return function

def init(width: int = 1000, height: int = 1000) -> None:
    global GL
    GL = PyGL(width, height)

@checkInstanceOnCall
def conwaysGameOfLife(initialData = None):
    data = [[False for y in range(GL.height)] for x in range(GL.width)]

    if initialData:
        for x, y in initialData:
            data[x - 1][y - 1] = True
    else:
        for x in range(GL.width):
            for y in range(GL.height):
                if random() < 0.1:
                    data[x][y] = True

    GL.enableScissor(True)

    running = True
    while running:
        for x in range(GL.width):
            for y in range(GL.height):
                if data[x][y]:
                    GL.pixel(x, y, (1.0, 1.0, 1.0, 1.0))
                else:
                    GL.pixel(x, y, (0.0, 0.0, 0.0, 1.0))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                GL.enableScissor(False)

        for x in range(GL.width):
            for y in range(GL.height):
                neighbors = checkNeighbours(x, y, data)
                
                if data[x][y]:
                    if neighbors < 2:
                        data[x][y] = False

                    if neighbors > 3:
                        data[x][y] = False

                    if neighbors == 2 or neighbors == 3:
                        data[x][y] = True
                        
                elif neighbors == 3:
                    data[x][y] = True
            
def checkNeighbours(x, y, data):
    neighbours = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0: continue
            xOffset, yOffset = x + i, y + j

            if xOffset >= GL.width:
                xOffset = 0

            if yOffset >= GL.height:
                yOffset = 0

            if data[xOffset][yOffset]:
                neighbours += 1
    return neighbours