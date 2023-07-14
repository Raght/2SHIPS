import pygame.math
from typing import List

from GameObject import *
from Shape import *
from multipledispatch import dispatch


class Mesh:
    def __init__(self, shapes: List[Shape], scale=1):
        self.shapes = shapes
        self._scale = scale
        self.change_scale(scale)

    def draw(self, position, surface):
        for shape in self.shapes:
            shape.draw(position, surface)

    def change_scale(self, new_scale):
        self._scale = new_scale
        # TODO: Update shapes
        # TODO: How to update scale? Do shapes have to provide a function for updating it?

    def __getitem__(self, index):
        return self.shapes[index]

    def __len__(self):
        return len(self.shapes)


@dispatch(Mesh, pygame.math.Vector2, Mesh, pygame.math.Vector2)
def collides(mesh1: Mesh, position1: pygame.math.Vector2, mesh2: Mesh, position2: pygame.math.Vector2):
    for shape1 in mesh1.shapes:
        for shape2 in mesh2.shapes:
            if collides(shape1, position1, shape2, position2):
                return True
    return False


@dispatch(GameObject, GameObject)
def collides(gameobject1: GameObject, gameobject2: GameObject):
    if gameobject1.mesh is None and gameobject2.mesh is None:
        return gameobject1.position == gameobject2.position
    if gameobject1.mesh is None:
        return collides(gameobject1.position, gameobject2.mesh, gameobject2.position)
    if gameobject2.mesh is None:
        return collides(gameobject2.position, gameobject1.mesh, gameobject1.position)
    return collides(gameobject1.mesh, gameobject1.position, gameobject2.mesh, gameobject2.position)