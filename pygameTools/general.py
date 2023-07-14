from sys import exit as _sys_exit, exit as _sys_quit
from pygame import quit as _pygame_exit, quit as _pygame_quit
from pygame.display import update as _pygame_display_update


# General

def full_exit():
    _sys_exit()
    _pygame_exit()

def full_quit():
    full_exit()

def update_frame(clock, frames_per_second):
    _pygame_display_update()
    clock.tick(frames_per_second)
