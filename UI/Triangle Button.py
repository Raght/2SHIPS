import pygame
from UI import *

resolution = (800, 600)
appName = "Triangle button test"
fps = 150

pygame.init()
sc = pygame.display.set_mode(resolution)
pygame.display.set_caption(appName)
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GREEN_DARKER = (0, 200, 0)
BLUE = (0, 0, 255)

buttons = list()
buttons.append(TriangleButton([200, 100], [100, 100], 1,   1,   RIGHT, True, None, None))
buttons.append(TriangleButton([200, 250], [100, 100], 1.5, 1.5, LEFT,  True, None, None))
buttons.append(TriangleButton([200, 400], [50, 50],   1,   1.5, UP,    True, None, None))
buttons.append(TriangleButton([200, 475], [50, 50],   1.5, 1,   DOWN,  True, None, None))

mBHandler = MouseButtonHandler()


while True:
    sc.fill(BLACK)

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            quit()

    mPos = pygame.mouse.get_pos()
    mPressedButtons = mBHandler.get_pressed()

    for button in buttons:
        if point_vs_rect(mPos, button.pos + button.size):
            button.draw(sc, GREEN, BLACK, BLACK)
        else:
            button.draw(sc, BLACK, GREEN, GREEN, 8)


    pygame.display.update()
    clock.tick(fps)
