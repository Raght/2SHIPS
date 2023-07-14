from multipledispatch import dispatch
from pygame.math import Vector2
from pygameAPI import *
import pygame.draw
import pygame.mouse


class TextContainer:
    def __init__(self, position, size, text_color, container_color, outline_width, font, text, enable_antialiasing=False):
        self.position = position
        self.size = size
        self.text_color = text_color
        self.container_color = container_color
        self.outline_width = outline_width
        self.font = font
        self.text = text
        self.enableAntialiasing = enable_antialiasing

    @property
    def up_left_corner(self):
        return [self.position[0] - self.size[0] / 2, self.position[1] - self.size[1] / 2]

    @property
    def up_left_corner_with_outline(self):
        return [self.position[0] - self.size[0] / 2 - self.outline_width,
                self.position[1] - self.size[1] / 2 - self.outline_width]

    def draw(self, surface):
        draw_rectangle(surface, self.up_left_corner, self.size, self.container_color, self.outline_width)

        text_render = self.font.render(self.text, self.enableAntialiasing, self.text_color)
        text_position = [self.position[0] - self.font.size(self.text)[0] / 2,
                         self.position[1] - self.font.size(self.text)[1] / 2]
        surface.blit(text_render, text_position)


class ButtonState:
    def __init__(self, pointed, pressed):
        self.pointed = pointed
        self.pressed = pressed

class Button:
    def __init__(self, position, size, enableAntialiasing, function, *args):
        self.position = position
        self.size = size
        self.text_color = text_color
        self.container_color = container_color
        self.outline_width = outline_width
        self.font = font
        self.text = text
        self.enableAntialiasing = enable_antialiasing

        self.size = size
        self.enableAntialiasing = enableAntialiasing
        self.function = function
        self.arguments = args

        self.pos = [0, 0]

    def draw(self, surface, pos, outlineColor, textColor, font, text, outline=0):
        self.pos = pos
        if outline:
            draw_rectangle(surface, pos, outlineColor, outline)
        else:
            pygame.draw.rect(surface, outlineColor, pos)
        
        textRender = font.render(text, self.enableAntialiasing, textColor)
        textPos = [pos[0] + self.size[0] - font.size(text)[0] - (self.size[0] - font.size(text)[0]) // 2,
                   pos[1] + self.size[1] - font.size(text)[1] - (self.size[1] - font.size(text)[1]) // 2]
        surface.blit(textRender, textPos)

    def on_press(self):
        self.function(*self.arguments)


class SwitchButton:
    def __init__(self, pos, size, outline, defaultState):
        self.pos = pos
        self.size = size
        self.outline = outline
        self.outlineCached = outline

        self.state = defaultState

        self.colorIfTrue = (0, 255, 0)
        self.colorIfFalse = (255, 0, 0)
        self.color = []

        self.isMouseColliding = False

    def draw(self, surface):
        if self.state:
            self.color = self.colorIfTrue
        else:
            self.color = self.colorIfFalse

        pygame.draw.rect(surface, self.color, tuple(self.pos) + tuple(self.size))
        draw_rectangle(surface, tuple(self.pos) + tuple(self.size), self.color, self.outline)

    def mouse_input(self, mousePos, mousePressed):
        if self.isMouseColliding:
            self.outline = self.outlineCached
        else:
            self.outline = 0

        if point_vs_rect(mousePos, [self.pos[0] - self.outline, self.pos[1] - self.outline,
                                    self.size[0] + 2 * self.outline, self.size[1] + 2 * self.outline]):
            self.isMouseColliding = True
            if mousePressed:
                self.state = not self.state
        else:
            self.isMouseColliding = False
