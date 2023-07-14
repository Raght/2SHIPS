import pygame
import configparser as configparser
from UI import *
from random import randint, shuffle
from sys import exit as sys_exit
from math import ceil


def full_exit():
    pygame.quit()
    sys_exit(0)


cfg = configparser.ConfigParser()
cfgFolder = "config/"


def cfg_read(cfgFile):
    global cfg, cfgFolder
    cfg.read(cfgFolder + cfgFile)


cfg_gameSettings = "gameSettings.ini"
cfg_singleplayer = "sp_players.ini"
cfg_multiplayer = "mp_players.ini"

cfg_read(cfg_gameSettings)
s = "Game Settings"
resWidth = cfg.getint(s, "resWidth")
resHeight = cfg.getint(s, "resHeight")
res = (resWidth, resHeight)
FPS = cfg.getint(s, "FPS")
FPS_MainMenu = cfg.getint(s, "FPS_MainMenu")

pygame.init()

sc = pygame.display.set_mode(res)
pygame.display.set_caption('2SHIPS')
clock = pygame.time.Clock()


def update_frame(FPS):
    pygame.display.update()
    clock.tick(FPS)


def wait(seconds, FPS):
    frames = ceil(seconds * FPS)
    for i in range(frames):
        update_frame(FPS)


def timer(seconds, FPS, func, *args):
    wait(seconds, FPS)
    func(*args)


# Mouse input
mousePos = pygame.mouse.get_pos()
mousePressedButtons = pygame.mouse.get_pressed()
mouseRMB = mousePressedButtons[0]


def draw_and_input(button):
    if collide(mousePos, button.pos):
        button.draw()


# Input constants
RIGHT = 0
LEFT = 1
SHOOT = 10

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

# Fonts
fontPath = "fonts/NES_Font.ttf"


def font(size):
    global fontPath
    return pygame.font.Font(fontPath, size)


font_24 = font(24)
font_32 = font(32)
font_48 = font(48)
font_64 = font(64)

font_round_HUD = font_24
font_game_HUD = font_48

# Round system
roundsMax = 3
rounds = [0, 0]

# Collision
borders = [[-5, -5, 10, resHeight + 10], [resWidth - 5, -5, 10, resHeight + 10]]
obstacles = [[-5, -20, resWidth + 10, 10], [-5, resHeight + 10, resWidth + 10, 10]]


# Ship classes
class Ship:
    def __init__(self, bodyPos, bodySize, headSize, facingDown, shipColor,
                 acceleration, deceleration, maxVelocity,
                 health, maxHealth, ammo, maxAmmo, firerate,
                 bulletSize, bulletColor, bulletDamage, bulletSpeed,
                 botDifficulty=None):
        self.bodyPos = bodyPos
        self.bodySize = bodySize
        self.headPos = [bodyPos[0] + (bodySize[0] - headSize[0]) // 2, self.bodyPos[1]]
        if facingDown:
            self.headPos[1] += headSize[1]
        else:
            self.headPos[1] -= headSize[1]
        self.headSize = headSize
        self.facingDown = facingDown

        self.shipColor = shipColor
        self.health = health
        self.maxHealth = maxHealth
        self.direction = (0, 0)
        self.acceleration = acceleration / FPS
        self.deceleration = deceleration / FPS
        self.maxVelocity = maxVelocity / FPS
        self.velocity = 0
        self.ammo = ammo
        self.maxAmmo = maxAmmo
        self.ticksToFire = FPS // firerate
        self.ticks = 0
        self.isDead = False

        self.bulletSize = bulletSize
        self.bulletColor = bulletColor
        self.bulletDamage = bulletDamage
        if facingDown:
            self.bulletSpeed = bulletSpeed
        else:
            self.bulletSpeed = -bulletSpeed
        self.missiles = []

        self.botDifficulty = botDifficulty

    @property
    def bodyRectPos(self):
        return self.bodyPos + self.bodySize

    @property
    def headRectPos(self):
        return self.headPos + self.headSize

    def set_direction(self, directionRight, directionDown):
        self.direction = (directionRight, directionDown)

    def set_coord(self, i, newCoord):
        dc = newCoord - self.bodyPos[i]
        self.bodyPos[i] += dc
        self.headPos[i] += dc

    def set_x(self, newX):
        self.set_coord(0, newX)

    def set_y(self, newY):
        self.set_coord(1, newY)

    def set_pos(self, newBodyPos):
        self.set_coord(newBodyPos[0])
        self.set_coord(newBodyPos[1])

    def take_damage(self, amount):
        self.health -= amount

        if self.health < 0:
            self.isDead = True

    def draw(self, surface, color):
        pygame.draw.rect(surface, color, self.bodyRectPos)
        pygame.draw.rect(surface, color, self.headRectPos)

    def shoot(self):
        if self.ticks >= self.ticksToFire:
            if self.ammo > 0:
                bulletPos = [self.bodyPos[0] + self.bodySize[0] // 2 - self.bulletSize[0] // 2 + randint(-10, 10),
                             self.bodyPos[1] - self.bulletSize[1] // 2,
                             self.bulletSize[0], self.bulletSize[1]]
                if self.facingDown:
                    bulletPos[1] = self.headPos[1] - self.bulletSize[1] // 2

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

            if collide(pos, enemy.headRectPos) or collide(pos, enemy.bodyRectPos):
                enemy.take_damage(self.bulletDamage)
                del self.missiles[self.missiles.index(pos)]

        if self.ticks < self.ticksToFire:
            self.ticks += 1

    def cap_velocity(self, maxVelocity):
        if self.velocity > maxVelocity:
            self.velocity = maxVelocity
        if self.velocity < -maxVelocity:
            self.velocity = -maxVelocity

    def check_collision(self, obstacles):
        for obstacle in obstacles:
            if collide([self.bodyPos[0] + self.velocity] + self.bodyRectPos[1:4], obstacle):
                return True
        return False

    def move(self, obstacles):
        self.velocity += self.direction[0] * self.acceleration * (clock.get_time() / 1000)
        self.cap_velocity(self.maxVelocity)

        if self.check_collision(obstacles):
            self.velocity = 0
        else:
            self.bodyPos[0] += self.velocity
            self.headPos[0] += self.velocity

    def decelerate(self):
        if self.velocity > 0:
            self.deceleration = -self.acceleration
        elif self.velocity < 0:
            self.deceleration = self.acceleration

        self.velocity += self.deceleration * (clock.get_time() / 1000)  # Hmmm...

        if (self.velocity > 0 and self.deceleration > 0) or (self.velocity < 0 and self.deceleration < 0):
            self.velocity = 0


class Enemy(Ship):
    pass


def control(ship, keys, bindset, obstacles):
    LEFT_down = keys[bindset[LEFT]]
    RIGHT_down = keys[bindset[RIGHT]]
    SHOOT_down = keys[bindset[SHOOT]]
    if LEFT_down == RIGHT_down:
        ship.set_direction(0, 0)
        ship.decelerate()
    elif LEFT_down or RIGHT_down:
        ship.set_direction(RIGHT_down - LEFT_down, 0)

    ship.move(obstacles)

    if SHOOT_down:
        ship.shoot()


def reset_x(ship):
    ship.set_x(randint(0, resWidth - ship.bodySize[0]))


def reset_stats(ship):
    reset_x(ship)
    ship.velocity = 0
    ship.health = ship.maxHealth
    ship.ammo = ship.maxAmmo
    ship.ticks = 0
    ship.isDead = False
    ship.missiles = []


# Ship parameters
def construct_ship_from_cfg(config, playerNumber, bodyPos):
    global cfg, s
    g = lambda varName: cfg.getint(s, varName)
    g_str = lambda varName: cfg.get(s, varName)
    g_list = lambda varName: eval(cfg.get(s, varName))
    g_var = g_list
    playerSection = "Player " + str(playerNumber)

    cfg_read(config)

    # Save mode settings
    s = "Mode Settings"
    useAcceleration = g("useAcceleration")

    # Determine team
    i = 1
    for i in range(1, 3):
        s = f"Team {i}"
        if playerSection in g_list("players"):
            break

    shipColor = g_var("color")
    facingDown = g("facingDown")
    s = playerSection
    bodyWidth = g("bodyWidth")
    bodyHeight = g("bodyHeight")
    bodySize = [bodyWidth, bodyHeight]
    headWidth = g("headWidth")
    headHeight = g("headHeight")
    headSize = [headWidth, headHeight]

    if (useAcceleration):
        acceleration = g("acceleration")
        deceleration = g("deceleration")
        maxVelocity = g("maxVelocity")
    else:
        speed = g("speed")

    health = g("health")  # - g("damageOnStart")
    maxHealth = g("health")
    ammo = g("ammo")
    maxAmmo = ammo
    firerate = g("firerate")

    bulletWidth = g("bulletWidth")
    bulletHeight = g("bulletHeight")
    bulletSize = [bulletWidth, bulletHeight]
    bulletColor = g_var("bulletColor")
    bulletDamage = g("bulletDamage")
    bulletSpeed = g("bulletSpeed")

    return Ship(bodyPos, bodySize, headSize, facingDown, shipColor,
                acceleration, deceleration, maxVelocity,
                health, maxHealth, ammo, maxAmmo, firerate,
                bulletSize, bulletColor, bulletDamage, bulletSpeed)


# Constructing ship objects
"""
ship1 = Ship([100, resHeight - 100], [34, 25], False, GREEN,
             1400, -2100, 600,
             100, 100, 50, 50, 10,
             10, 10, WHITE, 10, 5)
ship2 = Ship([100, 100], [100, 25], [34, 25], True, RED,
             1400, -2100, 600,
             100, 100, 50, 50, 5,
             10, 10, WHITE, 10, 5)
"""
ship1 = construct_ship_from_cfg(cfg_multiplayer, 1, [0, resHeight - 100])
ship1_bindset = {
    RIGHT: pygame.K_d,
    LEFT: pygame.K_a,
    SHOOT: pygame.K_SPACE,
}

ship2 = construct_ship_from_cfg(cfg_multiplayer, 2, [0, 100])
ship2_bindset = {
    RIGHT: pygame.K_KP6,
    LEFT: pygame.K_KP4,
    SHOOT: pygame.K_KP_ENTER,
}

# HUD
HUD_p1_hp_pos = (10, res[1] - 45, 150, 45)
HUD_p1_ammo_pos = (res[0] - 160, res[1] - 45, 150, 45)
HUD_p2_hp_pos = (10, 0, 150, 45)
HUD_p2_ammo_pos = (res[0] - 160, 0, 150, 45)
HUD_round_score_pos = (res[0] // 2 - 75, 0, 150, 45)
HUD_game_score_pos = (res[0] // 2, res[1] // 2, 0, 0)

HUD_p1_hp = TextBox(HUD_p1_hp_pos, 1)
HUD_p1_ammo = TextBox(HUD_p1_ammo_pos, 1)
HUD_p2_hp = TextBox(HUD_p2_hp_pos, 1)
HUD_p2_ammo = TextBox(HUD_p2_ammo_pos, 1)
HUD_round_score = TextBox(HUD_round_score_pos, 1)
HUD_game_score = TextBox(HUD_game_score_pos, 1)


def draw_round_HUD(sc, outC, bgC, textC, ship1, ship2, font=font_round_HUD):
    HUD_p1_hp.draw(sc, outC, bgC, textC, font, f"{ship1.health}HP")
    HUD_p1_ammo.draw(sc, outC, bgC, textC, font, f"{ship1.ammo}")
    HUD_p2_hp.draw(sc, outC, bgC, textC, font, f"{ship2.health}HP")
    HUD_p2_ammo.draw(sc, outC, bgC, textC, font, f"{ship2.ammo}")
    HUD_round_score.draw(sc, outC, bgC, textC, font, f"{rounds[0]}:{rounds[1]}")


def draw_game_HUD(sc, outC, bgC, textC, font=font_game_HUD):
    sc.fill(bgC)
    HUD_game_score.draw(sc, outC, bgC, textC, font, f"{rounds[0]}:{rounds[1]}")
    pygame.display.update()


def round_cycle():
    while True:
        sc.fill(BLACK)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                full_exit()

        keys = pygame.key.get_pressed()
        control(ship1, keys, ship1_bindset, borders)
        control(ship2, keys, ship2_bindset, borders)

        ship1.draw(sc, GREEN)
        ship2.draw(sc, RED)

        ship1.move_bullets(sc, ship2)
        ship2.move_bullets(sc, ship1)

        draw_round_HUD(sc, GREEN, BLACK, GREEN, ship1, ship2)

        ship1.isDead = ship1.health <= 0
        ship2.isDead = ship2.health <= 0
        if ship1.isDead:
            rounds[0] += 1
        if ship2.isDead:
            rounds[0] += 1
        if ship1.isDead or ship2.isDead:
            break

        update_frame(FPS)


if __name__ == "__main__":
    for i in range(roundsMax):
        reset_stats(ship1)
        reset_stats(ship2)

        round_cycle()

        pygame.display.update()
        draw_game_HUD(sc, BLACK, BLACK, GREEN)
        wait(1, FPS_MainMenu)
