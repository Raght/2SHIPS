import pygame
import pygame.gfxdraw
import UI

resolution = (800, 600)
appName = "Slider Test"
fps = 150

pygame.init()
sc = pygame.display.set_mode(resolution)
pygame.display.set_caption(appName)
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GREEN_DARKER = (0, 185, 0)

radius = 75
mult = 0
mySlider = UI.Slider([200, 100, 400, 5], [7, 30], mult, -1, 1)

rectLength = 300

MBH = UI.MouseButtonHandler()


while True:
    sc.fill(BLACK)

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            quit()

    mPos = pygame.mouse.get_pos()
    held = MBH.get_pressed()[0].held

    mySlider.mouse_input(mPos, held)
    mySlider.draw(sc, GREEN, GREEN_DARKER)

    mult = mySlider.get_value()
    UI.draw_text(sc, (0, 0), str(mult), WHITE, 32)

    pygame.draw.circle(sc, GREEN, (400, 400), abs(int(radius * mult)))
    pygame.draw.rect(sc, GREEN, (400, 200, rectLength * mult, 15))

    pygame.display.update()
    clock.tick(fps)
