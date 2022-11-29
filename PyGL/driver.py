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
def menu():
    GL.playMusic("PyGL/Assets/menu.mp3")

    myimage = pygame_menu.baseimage.BaseImage(
        image_path = "PyGL/Assets/menu.jpg",
        drawing_mode = pygame_menu.baseimage.IMAGE_MODE_FILL,
    )

    menuTheme = pygame_menu.themes.Theme(
        background_color = myimage,
        title_background_color = (0, 50, 0),
        title_font = pygame_menu.font.FONT_NEVIS,
        title_font_size = 67,
        widget_font = pygame_menu.font.FONT_NEVIS,
        widget_font_color=(255, 255, 255),
        widget_background_color=(0, 50, 0),
        widget_padding = (10,20),
        widget_margin = (0,20)
    )
                    
    menu = pygame_menu.Menu("Minecraft", 1000, 500, theme = menuTheme)
    menu.add.button("Nivel 1", runGame, "PyGL/Assets/level1.txt")
    menu.add.button("Nivel 2", runGame, "PyGL/Assets/level2.txt")
    menu.add.button("Cerrar", pygame_menu.events.EXIT)

    menu.mainloop(GL.screen)

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
