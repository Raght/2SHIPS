from pygameAPI import *
from draw import *
import pygame
from constants import *
from UI import *

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

pygame.init()
sc = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

mouse = Mouse()

font = pygame.font.Font("fonts/NES_Font.ttf", 32)

text_container = TextContainer((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
                               GREEN, GREEN, 10, font, "Hello, World!", True)

while True:
    sc.fill(BLACK)

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            full_exit()

    text_container.draw(sc)


    update_frame(clock, FPS)
