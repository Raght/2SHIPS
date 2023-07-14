from GameObject import *

class WeaponPrototype:
    def __init__(self, missile, firing_positions, mesh):
        self.missile = missile
        self.firing_positions = firing_positions
        self.mesh = mesh


class Weapon(WeaponPrototype):
    def __init__(self, weapon_prototype: WeaponPrototype, game_object: GameObject, ammo: int):
        super().__init__(weapon_prototype.missile, weapon_prototype.firing_positions, weapon_prototype.mesh)
        self.game_object = game_object
        self.ammo = ammo

    def try_shoot(self):
        if self.ammo > 0:
            self._shoot()
            return True
        return False

    def _shoot(self):


