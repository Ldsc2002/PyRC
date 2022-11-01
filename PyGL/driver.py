from PyGL.lib.PyGL import *
from random import *
from copy import deepcopy

GL = None

def checkInstanceOnCall(function):
    if GL is None: init()
    return function

def init(width: int = 1000, height: int = 1000) -> None:
    global GL
    GL = PyGL(width, height)

def conwaysGameOfLife(pixelSize = 1, width = 250, height = 250, initialData = None):
    init(width, height)
    data = [[False for y in range(int(height / pixelSize))] for x in range(int(width / pixelSize))]

    if width % pixelSize != 0 or height % pixelSize != 0:
        raise Exception("Pixel size must be a factor of width and height")

    if initialData:
        for x, y in initialData:
            data[x - 1][y - 1] = True
    else:
        for x in range(int(width / pixelSize)):
            for y in range(int(height / pixelSize)):
                if random() < 0.1:
                    data[x][y] = True

    GL.enableScissor(True)

    running = True
    while running:
        for x in range(len(data)):
            for y in range(len(data[0])):
                if data[x][y]:
                    GL.pixel(x * pixelSize, y * pixelSize, (1.0, 1.0, 1.0, 1.0), pixelSize)
                else:
                    GL.pixel(x * pixelSize, y * pixelSize, (0.0, 0.0, 0.0, 1.0), pixelSize)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                GL.enableScissor(False)
        
        newData = deepcopy(data)
        for x in range(len(data)):
            for y in range(len(data[0])):
                neighbors = checkNeighbours(x, y, data)
                
                if data[x][y]:
                    if neighbors < 2:
                        newData[x][y] = False

                    elif neighbors > 3:
                        newData[x][y] = False

                    elif neighbors == 2 or neighbors == 3:
                        newData[x][y] = True
                        
                elif neighbors == 3:
                    newData[x][y] = True
        data = newData
            
def checkNeighbours(x, y, data):
    neighbours = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0: continue
            xOffset, yOffset = x + i, y + j

            if xOffset >= len(data):
                xOffset = 0

            if yOffset >= len(data[0]):
                yOffset = 0

            if data[xOffset][yOffset]:
                neighbours += 1
    return neighbours