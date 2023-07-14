import pygame.math
from multipledispatch import dispatch
from abc import ABC, abstractmethod


class Shape(ABC):
    @abstractmethod
    def draw(self, position, surface):
        pass
