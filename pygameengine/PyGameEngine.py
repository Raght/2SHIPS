import pygame
import time


class PygameEngine:
    screen: pygame.Surface
    delta_time: float = 0
    frame_counter: int = 0

    def __init__(self, resolution, flags=0, depth=0, display=0, vsync=0):
        self.resolution_width = resolution[0]
        self.resolution_height = resolution[1]
        self.screen = pygame.display.set_mode(resolution, flags=0, depth=0, display=0, vsync=0)

    def update(self):
        pass

    def start(self):
        while True:
            self._core_update()

    def _core_update(self):
        start = time.time()
        self.update()
        end = time.time()
        self.delta_time = end - start
        self.frame_counter += 1
