import pygame
from math import ceil
from warnings import warn

pygame.init()

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
defaultFont = pygame.font.Font("fonts/NES_Font.ttf", 24)


def point_vs_rect(point, rect):
    return (rect[1] <= point[1] <= rect[1] + rect[3] and
            rect[0] <= point[0] <= rect[0] + rect[2])


def collide(object1, object2):
    obj1 = list(object1)[0:4]
    obj2 = list(object2)[0:4]
    for i in range(4):
        obj1[i] = round(obj1[i])
    for i in range(4):
        obj2[i] = round(obj2[i])

    hitboxes = set()
    hitboxes.add((obj1[0], obj1[1]))
    hitboxes.add((obj1[0] + obj1[2], obj1[1]))
    hitboxes.add((obj1[0] + obj1[2], obj1[1] + obj1[3]))
    hitboxes.add((obj1[0], obj1[1] + obj1[3]))

    for hitbox in hitboxes:
        if point_vs_rect(hitbox, obj2):
            return True

    return False


def collide_float(object1, object2):
    hitboxes = set()
    hitboxes.add((object1[0], object1[1]))
    hitboxes.add((object1[0] + object1[2], object1[1]))
    hitboxes.add((object1[0] + object1[2], object1[1] + object1[3]))
    hitboxes.add((object1[0], object1[1] + object1[3]))

    for hitbox in hitboxes:
        if point_vs_rect(hitbox, object2):
            return True

    return False


def draw_border(surface, rectPos, borderColor, thickness):
    # UP
    pygame.draw.rect(surface, borderColor, [rectPos[0] - thickness, rectPos[1] - thickness,
                                            rectPos[2] + 2 * thickness, thickness])
    # DOWN
    pygame.draw.rect(surface, borderColor, [rectPos[0] - thickness, rectPos[1] + rectPos[3],
                                            rectPos[2] + 2 * thickness, thickness])
    # RIGHT
    pygame.draw.rect(surface, borderColor, [rectPos[0] + rectPos[2], rectPos[1],
                                            thickness, rectPos[3]])
    # LEFT
    pygame.draw.rect(surface, borderColor, [rectPos[0] - thickness, rectPos[1],
                                            thickness, rectPos[3]])


def draw_rounded_border(surface, rectPos, borderColor, thickness, offset=1):
    if thickness == 0:
        return
    # UP
    pygame.draw.rect(surface, borderColor, [rectPos[0] - thickness + offset, rectPos[1] - thickness,
                                            rectPos[2] + 2 * thickness - offset * 2, thickness])
    # DOWN
    pygame.draw.rect(surface, borderColor, [rectPos[0] - thickness + offset, rectPos[1] + rectPos[3],
                                            rectPos[2] + 2 * thickness - offset * 2, thickness])
    # RIGHT
    pygame.draw.rect(surface, borderColor, [rectPos[0] + rectPos[2], rectPos[1] - thickness + offset,
                                            thickness, rectPos[3] + thickness * 2 - offset * 2])
    # LEFT
    pygame.draw.rect(surface, borderColor, [rectPos[0] - thickness, rectPos[1] - thickness + 1,
                                            thickness, rectPos[3] + thickness * 2 - offset * 2])


def draw_rect(surface, rectPos, rectColor, outlineColor=None, outline=0):
    if rectColor is not None:
        pygame.draw.rect(surface, rectColor, rectPos)
    if outlineColor is not None:
        draw_border(surface, rectPos, outlineColor, outline)


def draw_text(surface, pos, text, color, size, font=None, enableAntialiasing=0):
    if font is None:
        font = pygame.font.SysFont(defaultFont, size)
    textRender = font.render(text, enableAntialiasing, color)
    surface.blit(textRender, pos)


class Key:
    def __init__(self):
        self.previousState = False
        self.state = False
        self.pressed = False
        self.held = False
        self.released = False


class MouseButtonHandler:
    def __init__(self):
        self.buttons = []
        for i in range(3):
            self.buttons.append(Key())

    def get_pressed(self):
        mousePressed = pygame.mouse.get_pressed()

        for i in range(3):
            self.buttons[i].previousState = self.buttons[i].state
            self.buttons[i].state = mousePressed[i]

            self.buttons[i].pressed = False
            self.buttons[i].held = False
            self.buttons[i].released = False
            if (not self.buttons[i].previousState) and self.buttons[i].state:
                self.buttons[i].pressed = True
            elif self.buttons[i].previousState and self.buttons[i].state:
                self.buttons[i].held = True
            elif self.buttons[i].previousState and (not self.buttons[i].state):
                self.buttons[i].released = True

        return self.buttons




class TextBox:
    def __init__(self, position, enable_antialiasing: bool):
        self.position = position[0:2]
        self.size = position[2:4]
        self.enable_antialiasing = enable_antialiasing

    def draw(self, surface, outlineColor, rectColor, textColor, font, text, outline=0):
        draw_rect(surface, self.position + self.size, rectColor, outlineColor, outline)

        textRender = font.render(text, self.enable_antialiasing, textColor)
        textPos = [self.position[0] + self.size[0] - font.size(text)[0] - (self.size[0] - font.size(text)[0]) // 2,
                   self.position[1] + self.size[1] - font.size(text)[1] - (self.size[1] - font.size(text)[1]) // 2]
        surface.blit(textRender, textPos)


class Button:
    def __init__(self, position, size, enableAntialiasing, function, *args):
        self.position = position
        self.size = size
        self.enableAntialiasing = enableAntialiasing
        self.function = function
        self.arguments = args

    def draw(self, surface, rectColor, outlineColor, textColor, font, text, outline=0):
        draw_rect(surface, self.position + self.size, rectColor, outlineColor, outline)

        text_render = font.render(text, self.enableAntialiasing, textColor)
        text_position = [self.position[0] + self.size[0] - font.size(text)[0] - (self.size[0] - font.size(text)[0]) // 2,
                         self.position[1] + self.size[1] - font.size(text)[1] - (self.size[1] - font.size(text)[1]) // 2]
        surface.blit(text_render, text_position)

    def on_press(self):
        self.function(*self.arguments)


class TriangleButton(Button):
    def __init__(self, pos, size, scaleX, scaleY, direction, enableAntialiasing, function, *args):
        super().__init__(pos, size, enableAntialiasing, function, *args)
        self.scaleX = scaleX
        self.scaleY = scaleY
        self.direction = direction

    def draw(self, surface, rectColor, triangleColor, outlineColor, outline=0):
        draw_rect(surface, self.pos + self.size, rectColor)
        draw_rounded_border(surface, self.pos + self.size, outlineColor, outline)

        third_x = self.size[0] / 3
        third_y = self.size[1] / 3
        third_x_scaled = (third_x * (self.scaleX - 1)) / 2
        third_y_scaled = (third_y * (self.scaleY - 1)) / 2
        square_unit_x = third_x + third_x_scaled * 2
        square_unit_y = third_y + third_y_scaled * 2

        p1 = [self.pos[0] + third_x - third_x_scaled, self.pos[1] + third_y - third_y_scaled]
        p2 = [p1[0] + square_unit_x, p1[1]]
        p3 = [p2[0], p2[1] + square_unit_y]
        p4 = [p1[0], p1[1] + square_unit_y]

        p1[0] = int(p1[0])
        p1[1] = int(p1[1])
        p2[0] = ceil(p2[0])
        p2[1] = int(p2[1])
        p3[0] = ceil(p3[0])
        p3[1] = ceil(p3[1])
        p4[0] = int(p4[0])
        p4[1] = ceil(p4[1])

        p_middle = [self.pos[0] + self.size[0] // 2, p1[1]]
        points = [p3, p4]
        if self.direction == UP:
            pass
        elif self.direction == DOWN:
            p_middle = [self.pos[0] + self.size[0] // 2, p3[1]]
            points = [p1, p2]
        elif self.direction == RIGHT:
            p_middle = [p3[0], self.pos[1] + self.size[1] // 2]
            points = [p1, p4]
        elif self.direction == LEFT:
            p_middle = [p1[0], self.pos[1] + self.size[1] // 2]
            points = [p2, p3]
        else:
            warn("The direction of arrow has not been specified")

        points.append(p_middle)

        pygame.draw.polygon(surface, triangleColor, points)
        if self.enableAntialiasing:
            pygame.draw.aalines(surface, triangleColor, True, points)


class Slider:
    def __init__(self, pos, sliderSize, defaultValue, minValue, maxValue):
        self.pos = pos
        self.sliderSize = sliderSize
        self.currentValue = defaultValue
        self.minValue = minValue
        self.maxValue = maxValue

        self.valuePerPixel = (self.maxValue - self.minValue) / self.pos[2]
        self.sliderMidPointX = self.pos[0] + self.pos[2] * (
                    (self.currentValue - self.minValue) / (self.maxValue - minValue))
        self.sliderPos = [self.sliderMidPointX - ceil(self.sliderSize[0] / 2),
                          self.pos[1] - ceil((self.sliderSize[1] - self.pos[3]) / 2),
                          self.sliderSize[0], self.sliderSize[1]]

        self.flag = False

    def get_value(self):
        return self.currentValue

    def mouse_input(self, mousePos, mousePressed):
        sliderMidPointX_old = self.sliderMidPointX

        if point_vs_rect(mousePos, self.sliderPos) or self.flag:
            if mousePressed:
                self.flag = True
                if self.pos[0] <= mousePos[0] <= self.pos[0] + self.pos[2]:
                    self.sliderMidPointX = mousePos[0]
                elif self.pos[0] >= mousePos[0]:
                    self.sliderMidPointX = self.pos[0]
                elif mousePos[0] >= self.pos[0] + self.pos[2]:
                    self.sliderMidPointX = self.pos[0] + self.pos[2]
            else:
                self.flag = False
        elif point_vs_rect(mousePos, self.pos):
            if mousePressed:
                self.sliderMidPointX = mousePos[0]

        self.currentValue = round(self.currentValue + (self.sliderMidPointX - sliderMidPointX_old) * self.valuePerPixel,
                                  10)

    def draw(self, surface, sliderColor, lineColor):
        pygame.draw.rect(surface, lineColor, self.pos)

        self.sliderPos[0] = self.sliderMidPointX - ceil(self.sliderSize[0] / 2)
        draw_rect(surface, self.sliderPos, sliderColor, lineColor, 2)
        # draw_rounded_border(surface, self.pos, lineColor, outline)
        # pygame.draw.rect(surface, sliderColor, self.sliderPos)


def _new_point(p, scale, sign1, sign2, boxSide):
    """ Internal use """
    return [p[0] + sign1 * int(scale * boxSide),
            p[1] + sign2 * int(scale * boxSide)]


def _draw_check1(self, surface, pos, checkColor):
    """ Internal use """
    p1 = [pos[0] + self.checkGap, pos[1] + self.boxSide // 2 + (0.17333 * self.boxSide - self.checkGap)]
    p2 = _new_point(p1, 0.11333, 1, -1, self.boxSide)
    p3 = _new_point(p2, 0.14667, 1, 1, self.boxSide)
    p4 = _new_point(p3, 0.36, 1, -1, self.boxSide)
    p5 = _new_point(p4, 0.11333, 1, 1, self.boxSide)
    p6 = _new_point(p5, 0.47333, -1, 1, self.boxSide)
    p6[0] = p3[0]
    pygame.draw.polygon(surface, checkColor, (p1, p2, p3, p4, p5, p6))


def _draw_check2(self, surface, pos, checkColor):
    """ Internal use """
    pygame.draw.polygon(surface, checkColor,
                        [
                            [pos[0] + self.checkGap, pos[1] + self.checkGap],
                            [pos[0] + self.checkThickness + self.checkGap, pos[1] + self.checkGap],
                            [pos[0] + self.boxSide // 2,
                             pos[1] + self.boxSide - 2 * self.checkThickness - self.checkGap],
                            [pos[0] + self.boxSide - self.checkThickness - self.checkGap, pos[1] + self.checkGap],
                            [pos[0] + self.boxSide - self.checkGap, pos[1] + self.checkGap],
                            [pos[0] + self.boxSide // 2, pos[1] + self.boxSide - self.checkGap]
                        ])


def _draw_check3(self, surface, pos, checkColor):
    """ Internal use """
    pygame.draw.polygon(surface, checkColor,
                        [
                            pos,
                            [pos[0] + self.checkThickness, pos[1]],
                            [pos[0] + self.boxSide // 2, pos[1] + self.boxSide - 2 * self.checkThickness],
                            [pos[0] + self.boxSide - self.checkThickness, pos[1]],
                            [pos[0] + self.boxSide, pos[1]],
                            [pos[0] + self.boxSide // 2, pos[1] + self.boxSide]
                        ])


def _draw_cross1(self, surface, pos, checkColor):
    """ Internal use """
    pygame.draw.polygon(surface, checkColor,
                        [
                            [pos[0] + self.checkThickness + self.checkGap, pos[1] + self.checkGap],
                            [pos[0] + self.boxSide - self.checkGap,
                             pos[1] + self.boxSide - self.checkThickness - self.checkGap],
                            [pos[0] + self.boxSide - self.checkThickness - self.checkGap,
                             pos[1] + self.boxSide - self.checkGap],
                            [pos[0] + self.checkGap, pos[1] + self.checkThickness + self.checkGap]
                        ])
    pygame.draw.polygon(surface, checkColor,
                        [
                            [pos[0] + self.boxSide - self.checkGap, pos[1] + self.checkThickness + self.checkGap],
                            [pos[0] + self.checkThickness + self.checkGap, pos[1] + self.boxSide - self.checkGap],
                            [pos[0] + self.checkGap, pos[1] + self.boxSide - self.checkThickness - self.checkGap],
                            [pos[0] + self.boxSide - self.checkThickness - self.checkGap, pos[1] + self.checkGap]
                        ])


def _draw_cross2(self, surface, pos, checkColor):
    """ Internal use """
    pygame.draw.polygon(surface, checkColor,
                        [
                            pos,
                            [pos[0] + self.checkThickness, pos[1]],
                            [pos[0] + self.boxSide, pos[1] + self.boxSide - self.checkThickness],
                            [pos[0] + self.boxSide, pos[1] + self.boxSide],
                            [pos[0] + self.boxSide - self.checkThickness, pos[1] + self.boxSide],
                            [pos[0], pos[1] + self.checkThickness]
                        ])
    pygame.draw.polygon(surface, checkColor,
                        [
                            [pos[0] + self.boxSide, pos[1]],
                            [pos[0] + self.boxSide, pos[1] + self.checkThickness],
                            [pos[0] + self.checkThickness, pos[1] + self.boxSide],
                            [pos[0], pos[1] + self.boxSide],
                            [pos[0], pos[1] + self.boxSide - self.checkThickness],
                            [pos[0] + self.boxSide - self.checkThickness, pos[1]]
                        ])


def _draw_box(self, surface, pos, checkColor):
    """ Internal use """
    pygame.draw.rect(surface, checkColor,
                     [pos[0] + self.checkGap, pos[1] + self.checkGap] +
                     [self.boxSide - 2 * self.checkGap] * 2)


def _draw_none(self, surface, pos, checkColor):
    """ Internal use """
    pass


_checkStyleInfo = {
    "check1": [_draw_check1, 0.11333, 0.13667],
    "check2": [_draw_check2, 0.12, 0.22],
    "check3": [_draw_check3, 0.10, 0],
    "cross1": [_draw_cross1, 0.07, 0.20],
    "cross2": [_draw_cross2, 0.07, 0],
    "box": [_draw_box, 0, 0.22]
}


class Checkbox:
    """
    Checkbox (Tickbox)

    Available check styles:
    "check1",
    "check2",
    "check3",
    "cross1",
    "cross2",
    "box",
    """

    def __init__(self, pos, boxSide, outlineThickness, defaultState, checkStyle):
        self.pos = list(pos)
        self.boxSide = boxSide
        self.outlineThickness = outlineThickness
        self.state = defaultState

        self.checkStyle = checkStyle
        try:
            self.draw_check = _checkStyleInfo[checkStyle][0]
            self.checkThickness = int(boxSide * _checkStyleInfo[checkStyle][1])
            self.checkGap = int(boxSide * _checkStyleInfo[checkStyle][2])
        except KeyError:
            warn("CheckStyle has not been specified")
            self.draw_check = _draw_none
            self.checkThickness = None
            self.checkGap = None

    def get_state(self):
        return self.state

    def mouse_input(self, mousePos, mousePressed):
        if point_vs_rect(mousePos, list(self.pos) + [self.boxSide] * 2) and mousePressed:
            self.state = not self.state

    def draw(self, surface, boxColor, checkColor):
        if self.outlineThickness:
            draw_border(surface, list(self.pos) + [self.boxSide] * 2, boxColor, self.outlineThickness)
        else:
            pygame.draw.rect(surface, boxColor, list(self.pos) + [self.boxSide] * 2, self.outlineThickness)

        if self.state:
            self.draw_check(self, surface, self.pos, checkColor)

    def draw_text(self, surface, textColor, font, text, place, antialiasing=0):
        textSurface = font.render(text, antialiasing, textColor)
        textPos = self.pos[:]
        if place == UP:
            textPos[0] += (self.boxSide // 2 - font.size(text)[0] // 2)
            textPos[1] -= (self.outlineThickness + font.size(text)[1] + font.size(" ")[1])
        elif place == DOWN:
            textPos[0] += (self.boxSide // 2 - font.size(text)[0] // 2)
            textPos[1] += self.boxSide + self.outlineThickness + font.size(" ")[1]
        elif place == RIGHT:
            textPos[0] += self.boxSide + self.outlineThickness + font.size(" ")[0]
            textPos[1] += (self.boxSide // 2 - font.size(text)[1] // 2)
        elif place == LEFT:
            textPos[0] -= (self.outlineThickness + font.size(text)[0] + font.size(" ")[0])
            textPos[1] += (self.boxSide // 2 - font.size(text)[1] // 2)
        surface.blit(textSurface, textPos)

    def color(self, boxColorIfTrue, boxColorIfFalse):
        if self.state:
            return boxColorIfTrue
        return boxColorIfFalse
