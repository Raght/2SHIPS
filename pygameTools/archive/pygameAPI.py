from multipledispatch import dispatch
from pygame.math import Vector2
from sys import exit as sys_exit, exit as sys_quit
from pygame import quit as pygame_exit, quit as pygame_quit
from pygameAPI_constants import *
import pygame
import pygame.gfxdraw


# General

def full_exit():
    sys_exit()
    pygame_exit()

def update_frame(clock, frames_per_second):
    pygame.display.update()
    clock.tick(frames_per_second)


# Collision checking

@dispatch(tuple, tuple)
@dispatch(list, tuple)
@dispatch(Vector2, tuple)
@dispatch(tuple, list)
@dispatch(list, list)
@dispatch(Vector2, list)
def point_vs_rect(point, rectangle):
    return (rectangle[0] <= point[0] <= rectangle[0] + rectangle[2] and
            rectangle[1] <= point[1] <= rectangle[1] + rectangle[3])

@dispatch(Vector2, Vector2, Vector2)
def point_vs_rect(point, rectangle_position_left_upright_corner, rectangle_size):
    rectangle = (rectangle_position_left_upright_corner[0], rectangle_position_left_upright_corner[1],
                 rectangle_size[0], rectangle_size[1])
    return point_vs_rect(point, rectangle)

@dispatch(tuple, tuple)
@dispatch(list, tuple)
@dispatch(Vector2, tuple)
@dispatch(tuple, list)
@dispatch(list, list)
@dispatch(Vector2, list)
def point_vs_rect_round(point, rectangle):
    return (round(rectangle[0]) <= round(point[0]) <= round(rectangle[0] + rectangle[2]) and
            round(rectangle[1]) <= round(point[1]) <= round(rectangle[1] + rectangle[3]))

@dispatch(Vector2, Vector2, Vector2)
def point_vs_rect_round(point, rectangle_position_left_upright_corner, rectangle_size):
    rectangle = (rectangle_position_left_upright_corner[0], rectangle_position_left_upright_corner[1],
                 rectangle_size[0], rectangle_size[1])
    return point_vs_rect_round(point, rectangle)

@dispatch(tuple, tuple)
@dispatch(list, tuple)
@dispatch(tuple, list)
@dispatch(list, list)
def rect_vs_rect(rectangle_first, rectangle_second):
    x, y, w, h = rectangle_first
    
    points = set()
    points.append((x, y))
    points.append((x + w, y))
    points.append((x + w, y + h))
    points.append((x, y + h))

    for point in points:
        if point_vs_rect(point, rectangle_second):
            return True

    return False

@dispatch(Vector2, Vector2, Vector2, Vector2)
def rect_vs_rect(position_first, size_first, position_second, size_second):
    return rect_vs_rect((position_first[0], position_first[1], size_first[0], size_second[1]),
                        (position_second[0], position_second[1], size_second[0], size_second[1]))

@dispatch(tuple, tuple)
@dispatch(list, tuple)
@dispatch(tuple, list)
@dispatch(list, list)
def rect_vs_rect_round(rectangle_first, rectangle_second):
    x, y, w, h = rectangle_first
    
    points = set()
    points.append((x, y))
    points.append((x + w, y))
    points.append((x + w, y + h))
    points.append((x, y + h))

    for point in points:
        if point_vs_rect_round(point, rectangle_second):
            return True

    return False

@dispatch(Vector2, Vector2, Vector2, Vector2)
def rect_vs_rect_round(position_first, size_first, position_second, size_second):
    return rect_vs_rect_round((position_first[0], position_first[1], size_first[0], size_second[1]),
                              (position_second[0], position_second[1], size_second[0], size_second[1]))


# Drawing

def draw_pixel(surface, position, color):
    pygame.draw.line(surface, color, (position[0], position[1]), (position[0], position[1]))

def draw_rect(surface, position, size, color, border_width):
    pygame.draw.rect(surface, color, (position[0], position[1], size[0], size[1]), border_width)

def fill_rect(surface, position, size, color):
    pygame.draw.rect(surface, color, (position[0], position[1], size[0], size[1]), 0)


# Keyboard and mouse input

class Key:
    def __init__(self):
        self.previousState = False
        self.state = False
        self.pressed = False
        self.held = False
        self.released = False

def _update_button_states(b, pressed):
    """ Internal use """
    b.previousState = b.state
    b.state = pressed

    b.isPressed = False
    b.isHeld = False
    b.isReleased = False
    if (not b.previousState) and b.state:
        b.isPressed = True
    elif b.previousState and b.state:
        b.isHeld = True
    elif b.previousState and (not b.state):
        b.isReleased = True

class Mouse:
    def __init__(self):
        self._number_of_buttons = NUMBER_OF_MOUSE_BUTTONS
        self.buttons = (Key() for _ in range(self._number_of_buttons))

    def get_position(self):
        return Vector2(pygame.mouse.get_pos())

    def update_buttons_states(self):
        mouse_pressed = pygame.mouse.get_pressed(num_buttons=self._number_of_buttons)

        for i in range(self._number_of_buttons):
            _update_button_states(self.buttons[i], mouse_pressed[i])

    def get_pressed(self):
        return self.buttons

class Keyboard:
    """ For text input use text_from_events instead """
    def __init__(self):
        self._number_of_buttons = NUMBER_OF_KEYBOARD_BUTTONS
        self.buttons = (Key() for _ in range(self._number_of_buttons))

    def update_buttons_states(self):
        keyboard_pressed = pygame.key.get_pressed()

        for i in range(self._number_of_buttons):
            _update_button_states(self.buttons[i], keyboard_pressed[i])

    def get_pressed(self):
        return self.buttons


def text_from_events(events):
    text = ""
    for event in events:
        if event.type == pygame.TEXTINPUT:
            text += event.dict["text"]

    return text
