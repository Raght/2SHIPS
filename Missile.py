from GameObject import *


class Missile(GameObject):
    def __init__(self, position, velocity, acceleration, mesh, damage, sender):
        super().__init__(position, velocity, acceleration, mesh)
        self.damage = damage
        self.sender = sender
