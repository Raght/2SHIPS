class GameObject:
    def __init__(self, position, initial_velocity, initial_acceleration, mesh=None):
        self.position = position
        self._velocity = initial_velocity
        self._acceleration = initial_acceleration
        self.mesh = mesh

    @property
    def velocity(self):
        return self._velocity

    @property
    def acceleration(self):
        return self._acceleration

    def apply_acceleration(self, acceleration):
        self._acceleration += acceleration

    def update_physics(self, delta_time):
        self._velocity += self.acceleration * delta_time
        self.position += self.velocity * delta_time

    def stop_movement(self):
        self._acceleration = 0
        self._velocity = 0

    def set_position(self, new_position):
        self.position = new_position

    def set_position_and_stop(self, new_position):
        self.set_position(new_position)
        self.stop_movement()

    def draw(self, surface):
        for part in self.mesh:
            part.draw(surface)
