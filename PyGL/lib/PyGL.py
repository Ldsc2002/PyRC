import pygame   
from OpenGL.GL import *
from math import cos, sin, pi, atan2

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

SKY = (40, 100, 200)
GROUND = (200, 200, 100)
TRANSPARENT = (152, 0, 136, 255)

walls = {
    "1": pygame.image.load("PyGL/Assets/wall1.png"),
    "2": pygame.image.load("PyGL/Assets/wall2.png"),
    "3": pygame.image.load("PyGL/Assets/wall3.png"),
    "4": pygame.image.load("PyGL/Assets/wall4.png"),
    "5": pygame.image.load("PyGL/Assets/wall5.png"),
}

sprite1= pygame.image.load('PyGL/Assets/sprite1.png')
sprite2= pygame.image.load('PyGL/Assets/sprite2.png')

enemies = [
    {
        'x': 100,
        'y': 150,
        'sprite': sprite1,
    },
    {
        'x': 300,
        'y': 300,
        'sprite': sprite2,
    },
]

class PyGL:
    def __init__(this, width, height, blockSize = 50):
        pygame.init()
        this.screen = pygame.display.set_mode((width, height))
        _, _, this.width, this.height = this.screen.get_rect()
        this.blockSize = blockSize
        this.map = []
        this.zbuffer = []
        this.player = {
            'x': int(this.blockSize + this.blockSize / 2),
            'y': int(this.blockSize + this.blockSize / 2),
            'fov': int(pi/3),
            'a': int(pi/3),
        }

        this.clearBuffer()

    def clearBuffer(this):
        this.zbuffer = [9999 for z in range(0,this.width)]

    def pixel(this, x, y, color = WHITE):
        this.screen.set_at((x, y), color)

    def block(this, x, y, wall):
        for i in range(x, x + this.blockSize):
            for j in range(y, y + this.blockSize):
                tx = int((i - x) * 128 / this.blockSize)
                ty = int((j - y) * 128 / this.blockSize)

                c = wall.get_at((tx,ty))
                this.pixel(i, j, c)

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

    def drawSprite(this, sprite):
        sprite_a = atan2(sprite['y'] - this.player['y'],sprite['x'] - this.player['x'],)
        
        d = ((this.player['x']-sprite['x'])**2 + (this.player['y'] - sprite['y'])**2)**0.5

        sprite_size = int(500/d * (500/10))

        sprite_x = int(
            500 + #offset del mapa
            (sprite_a - this.player['a']) * 500/ this.player['fov'] 
            + sprite_size/2
        )
        sprite_y = int(500/2 - sprite_size/2)
        
        for x in range(sprite_x,sprite_x+sprite_size):
            for y in range(sprite_y,sprite_y+sprite_size):
                tx = int((x - sprite_x) * 128/sprite_size)
                ty = int((y-sprite_y) * 128/sprite_size)
                c = sprite['sprite'].get_at((tx,ty))
                if c != TRANSPARENT:
                    if x > 500:
                        if this.zbuffer[x-500] >= d:
                            this.pixel(x,y,c)
                            this.zbuffer[x - 500] = d

    def drawStake(this, x, h, c, tx):
        start_y = int(this.height/2 - h/2)
        end_y = int(this.height/2 + h/2)
        height = end_y - start_y

        for y in range(start_y, end_y):
            ty = int((y - start_y) * 128 / height)
            color = walls[c].get_at((tx,ty))
            this.pixel(x, y, color)

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
            
    def render(this):
        this.screen.fill(BLACK, (0, 0, this.width, this.height))
        this.screen.fill(SKY, (this.width / 2, 0, this.width, this.height / 2))
        this.screen.fill(GROUND, (this.width / 2, this.height / 2, this.width, this.height / 2))

        this.drawMap()
        this.drawPlayer()
        this.clearBuffer()

        for i in range(0, int(this.width/2)):
            a = this.player['a'] - this.player['fov'] / 2 + this.player['fov'] * i / (this.width / 2)
            d,c,tx = this.castRay(a)

            if (d == 0): d = 1
            x = int(this.width/2) + i
            h = this.height / (d * cos(a - this.player['a'])) * this.height / 10

            if this.zbuffer[i] >= d:
                this.drawStake(x,h,c,tx)
                this.zbuffer[i] = d

        for enemy in enemies:
            this.drawSprite(enemy)

        this.flip()

    def flip(this):
        pygame.display.flip()


