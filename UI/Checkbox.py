import pygame
import pygame.gfxdraw
from UI import *

resWidth = 1280
resHeight = 780
appName = "Checkbox Test"
fps = 150

pygame.init()
sc = pygame.display.set_mode((resWidth, resHeight))
pygame.display.set_caption(appName)
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

backgroundColor = BLACK
circleColor = GREEN

fontNES = pygame.font.Font("fonts/NES_font.ttf", 32)

check = False
radiusDefault = 50
radiusMax = 260
radiusInc = (140 - 60) // 6

mouseHandler = MouseButtonHandler()

checkboxesSide = 100
checkboxesOutline = 8
checkboxes = []

space = (resWidth - 7 * checkboxesSide) // 8
pos = [space * (len(checkboxes) + 1) + len(checkboxes) * checkboxesSide,
       resHeight // 4 - checkboxesSide // 2]
checkboxes.append(Checkbox(pos, checkboxesSide, checkboxesOutline, check, "check1"))
checkboxes.append(Checkbox(pos, checkboxesSide, checkboxesOutline, check, "check2"))
checkboxes.append(Checkbox(pos, checkboxesSide, checkboxesOutline, check, "check3"))
checkboxes.append(Checkbox(pos, checkboxesSide, checkboxesOutline, check, "cross1"))
checkboxes.append(Checkbox(pos, checkboxesSide, checkboxesOutline, check, "cross2"))
checkboxes.append(Checkbox(pos, checkboxesSide, checkboxesOutline, check, "box"))
checkboxes.append(Checkbox(pos, checkboxesSide, checkboxesOutline, check, None))
for i in range(len(checkboxes)):
    checkboxes[i].pos[0] += i * (space + checkboxesSide)

specialCheckboxes = []
specialCheckboxes.append(Checkbox([50, resHeight - 67 - 50], 67, checkboxesOutline, False, "check1"))
specialCheckboxes.append(Checkbox([resWidth - 177 - 50, resHeight - 177 - 50], 177, checkboxesOutline, False, "cross1"))
specialCheckboxes.append(Checkbox([resWidth // 2, resHeight - 32 - 50], 32, checkboxesOutline, False, "check1"))


while True:
    sc.fill(backgroundColor)
    counter = 0

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            quit()

    mousePos = pygame.mouse.get_pos()
    mouseButtons = mouseHandler.get_pressed()
    index = 0
    for checkbox in checkboxes:
        checkbox.draw(sc, checkbox.color(GREEN, RED), WHITE)
        checkbox.mouse_input(mousePos, mouseButtons[0].pressed)

        check = checkbox.get_state()
        if check:
            counter += 1
        index += 1

    index = 0
    for specialCheckbox in specialCheckboxes:
        specialCheckbox.draw(sc, specialCheckbox.color(GREEN, RED), WHITE)
        if index == 0:
            specialCheckbox.draw_text(sc, WHITE, fontNES, "Shrink", RIGHT)
        elif index == 1:
            specialCheckbox.draw_text(sc, WHITE, fontNES, "Shrink", UP)
        elif index == 2:
            specialCheckbox.draw_text(sc, WHITE, fontNES, "Shrink", LEFT)
        specialCheckbox.mouse_input(mousePos, mouseButtons[0].pressed)
        if specialCheckbox.get_state():
            counter -= 1
        index += 1

    pygame.draw.circle(sc, circleColor, (resWidth // 2, int(resHeight // 1.5)), radiusDefault + counter * radiusInc)

    pygame.display.update()
    clock.tick(fps)
