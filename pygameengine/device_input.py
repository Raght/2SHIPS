from pygame import mouse as _pygame_mouse, key as _pygame_key
from pygame import Vector2
from pygame.locals import TEXTINPUT as _pygame_TEXTINPUT


# Constants

NUMBER_OF_MOUSE_BUTTONS = 5
NUMBER_OF_KEYBOARD_BUTTONS = 512

MOUSE_PRIMARY = 0
MOUSE_SECONDARY = 1
MOUSE_MIDDLE = 2
MOUSE_BACK = 3
MOUSE_FORWARD = 4


# Keyboard and mouse input

class Key:
    def __init__(self):
        self.previous_state = False
        self.state = False
        self.pressed = False
        self.held = False
        self.released = False

def _update_button_states(b, pressed):
    """ Internal use """
    b.previous_state = b.state
    b.state = pressed

    b.pressed = False
    b.held = False
    b.released = False
    if (not b.previous_state) and b.state:
        b.pressed = True
    elif b.previous_state and b.state:
        b.held = True
    elif b.previous_state and (not b.state):
        b.released = True

class Mouse:
    def __init__(self):
        self._number_of_buttons = NUMBER_OF_MOUSE_BUTTONS
        self.buttons = [Key() for _ in range(self._number_of_buttons)]

    def get_position(self):
        return Vector2(_pygame_mouse.get_pos())

    def update_buttons_states(self):
        """
            pygame.event.get has to be called before calling this function
            Don't call multiple times in one frame
        """
        mouse_pressed = _pygame_mouse.get_pressed(num_buttons=self._number_of_buttons)

        for i in range(self._number_of_buttons):
            _update_button_states(self.buttons[i], mouse_pressed[i])

    def get_pressed(self):
        return self.buttons

class Keyboard:
    """ For text input use text_from_events instead """
    def __init__(self):
        self._number_of_buttons = NUMBER_OF_KEYBOARD_BUTTONS
        self.buttons = [Key() for _ in range(self._number_of_buttons)]

    def update_buttons_states(self):
        """
            pygame.event.get has to be called before calling this function
            Don't call multiple times in one frame
        """
        keyboard_pressed = _pygame_key.get_pressed()

        for i in range(self._number_of_buttons):
            _update_button_states(self.buttons[i], keyboard_pressed[i])

    def get_pressed(self):
        return self.buttons


def text_from_events(events):
    text = ""
    for event in events:
        if event.type == _pygame_TEXTINPUT:
            text += event.dict["text"]

    return text
