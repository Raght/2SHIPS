import pygame

import gjk
from gjk import *
from typing import Union
from Shape import *


class Circle(Shape):
    def __init__(self, position, radius, color):
        self.position = position
        self.radius = radius
        self.color = color

    def draw(self, position, surface):
        pygame.draw.circle(surface, self.color, self.position + position, self.radius)


class Rectangle(Shape):
    def __init__(self, position, width, height, color):
        self.position = position
        self.width = width
        self.height = height
        self.color = color

    def draw(self, position, surface):
        pygame.draw.rect(surface, self.color, (self.position[0] + position[0], self.position[1] + position[1],
                                               self.width, self.height))


class Triangle(Shape):
    def __init__(self, position1, position2, position3, color):
        self.points = [position1, position2, position3]
        self.color = color

    def draw(self, position, surface):
        for i in range(3):
            pygame.draw.line(surface, self.color, self.points[i] + position, self.points[(i + 1) % 3] + position)


@dispatch(pygame.math.Vector2, Shape, pygame.math.Vector2)
def collides(position1: pygame.math.Vector2, shape2: Shape, position2: pygame.math.Vector2):
    ...


@dispatch(Circle, pygame.math.Vector2, Circle, pygame.math.Vector2)
def collides(shape1: Circle, position1: pygame.math.Vector2, shape2: Circle, position2: pygame.math.Vector2):
    center1 = shape1.position + position1
    center2 = shape2.position + position2
    return len(center2 - center1) <= shape1.radius + shape2.radius


@dispatch(Circle, pygame.math.Vector2, Shape, pygame.math.Vector2)
def collides(shape1: Circle, position1: pygame.math.Vector2, shape2: Circle, position2: pygame.math.Vector2):
    center1 = shape1.position + position1
    center2 = shape2.position + position2
    return len(center2 - center1) <= shape1.radius + shape2.radius

@dispatch(Shape, pygame.math.Vector2, Shape, pygame.math.Vector2)
def collides(shape1: Shape, position1: pygame.math.Vector2, shape2: Shape, position2: pygame.math.Vector2):
    if type(shape1) == Circle and type(shape2) == Circle:

    if type(shape2) == Circle:
        shape1, position1, shape2, position2 = shape2, position2, shape1, position1

    if type(shape1) == Circle:
        return gjk.collide_poly_circle()
    if type(Shape) in {Polygon, Rectangle, Triangle}: