from pygame.draw import (
    line as _pygame_draw_line,
    rect as _pygame_draw_rect,
    circle as _pygame_draw_filled_circle
)
from pygame.gfxdraw import (
    circle as _pygame_gfxdraw_circle
)
from pygame import Color


# Constants

RED = Color(255, 0, 0)
GREEN = Color(0, 255, 0)
BLUE = Color(0, 0, 255)

BLACK = Color(0, 0, 0)
GREY = Color(127, 127, 127)
WHITE = Color(255, 255, 255)

YELLOW = Color(255, 255, 0)
MAGENTA = Color(255, 0, 255)
CYAN = Color(0, 255, 255)

ORANGE = Color(255, 165, 0)
GOLD = Color(255, 215, 0)

PINK = Color(255, 192, 203)
DEEPPINK = Color(255, 20, 147)
ORCHID = Color(255, 131, 250)
MAROON = Color(255, 52, 179)
DARKVIOLET = Color(148, 0, 211)
PURPLE = Color(160, 32, 240)

TURQUOISE = Color(0, 245, 255)
SKYBLUE = Color(135, 206, 255)

TAN = Color(255, 165, 79)
CHOCOLATE = Color(255, 127, 36)

colors = [RED, GREEN, BLUE, WHITE, YELLOW, ORANGE, GOLD, PINK, DEEPPINK, ORCHID, MAROON, MAGENTA,
          DARKVIOLET, PURPLE, CYAN, TURQUOISE, SKYBLUE, TAN, CHOCOLATE]

# Drawing

def draw_pixel(surface, position, color):
    _pygame_draw_line(surface, color, (position[0], position[1]), (position[0], position[1]))

def draw_rectangle(surface, position, size, color, outline_width=0):
    if outline_width == 0:
        _pygame_draw_rect(surface, color, [position[0], position[1], size[0], size[1]])
        return

    # UP
    _pygame_draw_rect(surface, color, [position[0] - outline_width, position[1] - outline_width,
                                       size[0] + outline_width * 2, outline_width])
    # RIGHT
    _pygame_draw_rect(surface, color, [position[0] + size[0], position[1],
                                       outline_width, size[1]])
    # DOWN
    _pygame_draw_rect(surface, color, [position[0] - outline_width, position[1] + size[1],
                                       size[0] + outline_width * 2, outline_width])
    # LEFT
    _pygame_draw_rect(surface, color, [position[0] - outline_width, position[1],
                                       outline_width, size[1]])

def draw_round_rectangle(surface, position, size, color, outline_width=0, ):
    if outline_width == 0:
        _pygame_draw_rect(surface, color, [position[0], position[1], size[0], size[1]])
        return

    # UP
    _pygame_draw_rect(surface, color, [position[0] - outline_width, position[1] - outline_width,
                                       size[0] + outline_width * 2, outline_width])
    # RIGHT
    _pygame_draw_rect(surface, color, [position[0] + size[0], position[1],
                                       outline_width, size[1]])
    # DOWN
    _pygame_draw_rect(surface, color, [position[0] - outline_width, position[1] + size[1],
                                       size[0] + outline_width * 2, outline_width])
    # LEFT
    _pygame_draw_rect(surface, color, [position[0] - outline_width, position[1],
                                       outline_width, size[1]])

def fill_rectangle(surface, position, size, color):
    _pygame_draw_rect(surface, color, (position[0], position[1], size[0], size[1]), 0)

def draw_circle(surface, position, radius, color):
    _pygame_gfxdraw_circle(surface, position[0], position[1], radius, color)

def fill_circle(surface, position, radius, color):
    _pygame_draw_filled_circle(surface, color, (position[0], position[1]), radius)
