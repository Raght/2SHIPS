import pygame
from Engine2D import collide
from math import ceil

class Button:
    def __init__(self, pos, font, text):
        self.pos = pos
        self.font = font
        self.text = text
        self.textPos = [0, 0]
        self.textPos[0] = self.pos[0] + self.pos[2] - self.font.size(text)[0] - (self.pos[2] - self.font.size(text)[0]) // 2
        self.textPos[1] = self.pos[1] + self.pos[3] - self.font.size(text)[1] - (self.pos[3] - self.font.size(text)[1]) // 2
    
    def draw(self, surface, rectColor, textColor):
        pygame.draw.rect(surface, rectColor, self.pos)
        
        textRender = self.font.render(self.text, 1, textColor)
        surface.blit(textRender, self.textPos)

    def draw_outline(self, surface, outlineColor, textColor, outline):
        pygame.draw.rect(surface, outlineColor, self.pos, outline)
        
        textRender = self.font.render(self.text, 1, textColor)
        surface.blit(textRender, self.textPos)

class Slider:
    """
    Only positive values
    """
    def __init__(self, pos, sliderSize, currentValue, minValue, maxValue):
        self.pos = pos
        self.sliderSize = sliderSize
        self.currentValue = currentValue
        self.minValue = minValue
        self.maxValue = maxValue

        self.sliderMidPointX = self.pos[0] + self.pos[2] * (self.currentValue / (self.maxValue - self.minValue))
        self.sliderPos = [self.sliderMidPointX - ceil(self.sliderSize[0] / 2),
                          self.pos[1] - ceil((self.sliderSize[1] - self.pos[3]) / 2),
                          self.sliderSize[0], self.sliderSize[1]]

        self.flag = False

    def get_value(self):
        return self.currentValue

    def mouse_input(self, mousePos, mousePressedButtons):
        if collide(mousePos, self.sliderPos) or self.flag:
            if mousePressedButtons[0]:
                self.flag = True
                if self.pos[0] <= mousePos[0] <= self.pos[0] + self.pos[2]:
                    self.sliderMidPointX = mousePos[0]
                elif self.pos[0] >= mousePos[0]:
                    self.sliderMidPointX = self.pos[0]
                elif mousePos[0] >= self.pos[0] + self.pos[2]:
                    self.sliderMidPointX = self.pos[0] + self.pos[2]
            else:
                self.flag = False


    def draw(self, surface, lineColor, sliderColor):
        pygame.draw.rect(surface, lineColor, self.pos)
        
        self.sliderPos[0] = self.sliderMidPointX - ceil(self.sliderSize[0] / 2)
        pygame.draw.rect(surface, sliderColor, self.sliderPos)

        self.currentValue = ((self.sliderMidPointX - self.pos[0]) / self.pos[2]) * (self.maxValue - self.minValue)
