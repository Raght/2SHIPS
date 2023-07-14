import pygame
import configparser as configparser
from UI import *
from random import randint, shuffle


config = configparser.ConfigParser()
config.read("config/gameSettings.ini")

resWidth = config.getint("Game Settings", "resWidth")
resHeight = config.getint("Game Settings", "resHeight")
resolution = (resWidth, resHeight)
FPS = config.getint("Game Settings", "FPS")
FPS_MainMenu = config.getint("Game Settings", "FPS_MainMenu")

pygame.init()

sc = pygame.display.set_mode(resolution)
pygame.display.set_caption('2SHIPS')
clock = pygame.time.Clock()


def update_frame(FPS):
    pygame.display.update()
    clock.tick(FPS)


# Colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

WHITE = (255, 255, 255)
GREY = (125, 125, 125)
BLACK = (0, 0, 0)

YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
GOLD = (255, 215, 0)

PINK = (255, 192, 203)
DEEPPINK = (255, 20, 147)
ORCHID = (255, 131, 250)
MAROON = (255, 52, 179)
MAGENTA = (255, 0, 255)
DARKVIOLET = (148, 0, 211)
PURPLE = (160, 32, 240)

CYAN = (0, 255, 255)
TURQUOISE = (0, 245, 255)
SKYBLUE = (135, 206, 255)

TAN = (255, 165, 79)
CHOCOLATE = (255, 127, 36)
BROWN = (150, 75, 0)


colors = [RED, GREEN, BLUE, WHITE, YELLOW, ORANGE, GOLD, PINK, DEEPPINK, ORCHID, MAROON, MAGENTA,
          DARKVIOLET, PURPLE, CYAN, TURQUOISE, SKYBLUE, TAN, CHOCOLATE]
colors_shuffled = [RED, GREEN, BLUE, WHITE, YELLOW, ORANGE, GOLD, PINK, DEEPPINK, ORCHID, MAROON, MAGENTA,
                   DARKVIOLET, PURPLE, CYAN, TURQUOISE, SKYBLUE, TAN, CHOCOLATE]

random_menu_color = 1
if random_menu_color:
    menu_color = colors[randint(0, len(colors) - 1)]
else:
    menu_color = GREEN

sg_rounds = ""
mp_rounds = ""

borders = [[-5, -5, 10, resHeight + 10], [resWidth - 5, -5, 10, resHeight + 10]]
obstacles = [[-5, -20, resWidth + 10, 10], [-5, resHeight + 10, resWidth + 10, 10]]


class Ship:
    def __init__(self, health, maxHealth, maxSpeed, ammo, maxAmmo, ticksToFire,
                 bodyPos, headPos,
                 bulletDamage, bulletWidth, bulletHeight, bulletSpeed, bulletColor,
                 botDifficulty=None):
        self.health = health
        self.maxHealth = maxHealth
        self.direction = (0, 0)
        self.maxSpeed = maxSpeed / FPS
        self.velocity = 0
        self.ammo = ammo
        self.maxAmmo = maxAmmo
        self.ticksToFire = ticksToFire
        self.ticks = 0
        self.isDead = False

        self.bodyPos = bodyPos
        self.headPos = headPos
        self.bodyWidth = bodyPos[2]
        self.bodyHeight = bodyPos[3]
        self.headWidth = headPos[2]
        self.headHeight = headPos[3]

        self.bulletDamage = bulletDamage
        self.bulletWidth = bulletWidth
        self.bulletHeight = bulletHeight
        self.bulletSpeed = bulletSpeed
        self.bulletColor = bulletColor
        self.missiles = []
        self.botDifficulty = botDifficulty

    def reset_stats(self):
        self.health = self.maxHealth
        self.ammo = self.maxAmmo
        self.ticks = 0
        self.isDead = False
        self.missiles = []

    def set_direction(self, directionRight, directionDown):
        self.direction = (directionRight, directionDown)

    def set_pos(self, newBodyPos, newHeadPos):
        self.bodyPos = newBodyPos
        self.headPos = newHeadPos

    def take_damage(self, amount):
        self.health -= amount

        if self.health < 0:
            self.isDead = True

    def draw(self, surface, color):
        pygame.draw.rect(surface, color, self.bodyPos)
        pygame.draw.rect(surface, color, self.headPos)

    def shoot(self):
        if self.ticks >= self.ticksToFire:
            if self.ammo > 0:
                bulletPos = [self.bodyPos[0] + self.bodyWidth // 2 - self.bulletWidth // 2,
                             self.bodyPos[1] - self.bulletHeight // 2,
                             self.bulletWidth, self.bulletHeight]
                self.missiles.append(bulletPos)

                self.ammo -= 1
                self.ticks = 0

    def move_bullets(self, surface, enemy):
        for pos in self.missiles:
            pygame.draw.rect(surface, self.bulletColor, pos)
            self.missiles[self.missiles.index(pos)][1] += self.bulletSpeed

            for obstacle in obstacles:
                if collide(pos, obstacle):
                    del self.missiles[self.missiles.index(pos)]
                    continue

            if collide(pos, enemy.headPos) or collide(pos, enemy.bodyPos):
                enemy.take_damage(self.bulletDamage)
                del self.missiles[self.missiles.index(pos)]

        if self.ticks < self.ticksToFire:
            self.ticks += 1

    def check_collision(self, obstacles):
        for obstacle in obstacles:
            if collide([self.bodyPos[0] + self.velocity] + self.bodyPos[1:4], obstacle):
                return True
        return False

    def move(self, obstacles):
        if self.check_collision(obstacles):
            self.velocity = 0
        else:
            self.bodyPos[0] += self.velocity
            self.headPos[0] += self.velocity

    def control(self, keys, left, right, shoot, obstacles):
        if keys[left]:
            self.set_direction(-1, 0)
        elif keys[right]:
            self.set_direction(1, 0)
        else:
            self.set_direction(0, 0)

        self.velocity = self.maxSpeed * self.direction[0]

        self.move(obstacles)

        if keys[shoot]:
            self.shoot()


class Enemy(Ship):
    pass

mousePos = pygame.mouse.get_pos()
mousePressedButtons = pygame.mouse.get_pressed()
mouseRMB = mousePressedButtons[0]

def draw_and_input(button):
    if collide(mousePos, button.pos):
        button.draw()


ship = Ship(100, 100, 600, 50, 50, FPS // 10, [100, 500, 100, 25], [133, 475, 34, 25], 10, 10, 10, -5, WHITE)
ship1 = Ship(100, 100, 300, 50, 50, FPS // 2, [100, 100, 100, 25], [133, 125, 34, 25], 10, 10, 10, 5, WHITE)


if __name__ == "__main__":
    while True:
        sc.fill(BLACK)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        keys = pygame.key.get_pressed()
        ship.control(keys, pygame.K_a, pygame.K_d, pygame.K_SPACE, borders)
        ship1.control(keys, pygame.K_KP4, pygame.K_KP6, pygame.K_KP_ENTER, borders)

        ship.draw(sc, GREEN)
        ship1.draw(sc, RED)

        ship.move_bullets(sc, ship1)
        ship1.move_bullets(sc, ship)

        update_frame(FPS)
