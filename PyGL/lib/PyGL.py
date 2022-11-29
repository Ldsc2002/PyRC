import pygame
import pygame_menu
from OpenGL.GL import *
from math import cos, sin, pi, atan2

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

SKY = (40, 100, 200)
GROUND = (100, 50, 0)

walls = {
    "1": pygame.image.load("PyGL/Assets/wall1.png"),
    "2": pygame.image.load("PyGL/Assets/wall2.png"),
    "3": pygame.image.load("PyGL/Assets/wall3.png"),
    "4": pygame.image.load("PyGL/Assets/wall4.png"),
}

class PyGL:
    def __init__(this, width, height, blockSize = 50):
        pygame.init()
        this.screen = pygame.display.set_mode((width, height))
        _, _, this.width, this.height = this.screen.get_rect()
        this.blockSize = blockSize
        this.map = []
        this.player = {
            'x': int(this.blockSize + this.blockSize / 2),
            'y': int(this.blockSize + this.blockSize / 2),
            'fov': int(pi/3),
            'a': int(pi/3),
        }
        this.clock = pygame.time.Clock()
        this.font = pygame.font.SysFont("Arial" , 36 , bold = True)

    def pixel(this, x, y, color = WHITE):
        this.screen.set_at((x, y), color)

    def block(this, x, y, wall):
        wall = pygame.transform.scale(wall, (this.blockSize, this.blockSize))
        this.screen.blit(wall, (x, y))

    def loadMap(this, file):
        with open(file, "r") as f:
            mapFile = f.read().splitlines()
            
            for line in mapFile:
                this.map.append(list(line))

    def drawMap(this):
        for y in range(len(this.map)):
            for x in range(len(this.map[y])):
                if this.map[y][x] != " ":
                    wall = this.map[y][x]
                    this.block(x * this.blockSize, y * this.blockSize, walls[wall])

    def drawPlayer(this):
        this.pixel(this.player['x'],this.player['y'], WHITE)

    def drawStake(this, x, h, c, tx):
        start_y = int(this.height/2 - h/2)
        end_y = int(this.height/2 + h/2)
        height = end_y - start_y
        
        wall = walls[c]
        wall = pygame.transform.scale(wall, (wall.get_width(), height))
        this.screen.blit(wall, (x, start_y), (tx, 0, 1, height))

    def castRay(this, a = None):
        d = 0
        ox = this.player['x']
        oy = this.player['y']
        
        while True:
            x = int(ox + d * cos(a))
            y = int(oy + d * sin(a))

            i = int(x / this.blockSize)
            j = int(y / this.blockSize)

            if this.map[j][i] != ' ':
                hitx = x - i * this.blockSize
                hity = y - j * this.blockSize

                if 1 < hitx < this.blockSize - 1:
                    maxhit = hitx
                else:
                    maxhit = hity

                tx = int(maxhit * 128 / this.blockSize)
                return d, this.map[j][i], tx

            this.pixel(x, y)
            d += 1

    def movePlayer(this, direction, speed = 10):
        if direction == "left":
            this.player['a'] -= pi/speed

        elif direction == "right":
            this.player['a'] += pi/speed

        elif direction == "forward":
            dirX = int(speed * cos(this.player['a']))
            dirY = int(speed * sin(this.player['a']))

            this.player['x'] += dirX
            this.player['y'] += dirY

            i = int(this.player['x'] / this.blockSize + dirX / this.blockSize)
            j = int(this.player['y'] / this.blockSize + dirY / this.blockSize)

            if this.map[j][i] != ' ':
                this.player['x'] -= dirX
                this.player['y'] -= dirY

        elif direction == "backward":
            dirX = int(speed * cos(this.player['a']))
            dirY = int(speed * sin(this.player['a']))

            this.player['x'] -= dirX
            this.player['y'] -= dirY

            i = int(this.player['x'] / this.blockSize - dirX / this.blockSize)
            j = int(this.player['y'] / this.blockSize - dirY / this.blockSize)

            if this.map[j][i] != ' ':
                this.player['x'] += dirX
                this.player['y'] += dirY
            
    def fpsCounter(this):
        fps = str(int(this.clock.get_fps()))
        fpsText = this.font.render(fps , 1, pygame.Color("RED"))
        this.screen.blit(fpsText,(0, 0))

    def playMusic(this, file):
        pygame.mixer.music.load(file)
        pygame.mixer.music.play(-1)

    def render(this):
        this.screen.fill(BLACK, (0, 0, this.width, this.height))
        this.screen.fill(SKY, (this.width / 2, 0, this.width, this.height / 2))
        this.screen.fill(GROUND, (this.width / 2, this.height / 2, this.width, this.height / 2))

        this.drawMap()
        this.drawPlayer()

        for i in range(0, int(this.width/2)):
            a = this.player['a'] - this.player['fov'] / 2 + this.player['fov'] * i / (this.width / 2)
            d,c,tx = this.castRay(a)

            if (d == 0): d = 1
            x = int(this.width/2) + i
            h = this.height / (d * cos(a - this.player['a'])) * this.height / 10

            this.drawStake(x,h,c,tx)

        this.fpsCounter()
        this.clock.tick(60)

        pygame.display.flip()
