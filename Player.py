class PlayerInput:
    def __init__(self, controlled_ship, control_scheme):
        self.controlled_ship = controlled_ship
        self.control_scheme = control_scheme

        self.buttons_to_check = [key for key in self.control_scheme.keys()]


