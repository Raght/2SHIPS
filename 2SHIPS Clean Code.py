import pygame
import configparser as configparser
from UI import *
from random import randint, shuffle
from sys import exit as sys_exit
from math import ceil
from game_settings import *
from config_constants import *
from Ship import *
from Player import *
from GameObject import *
from pygameTools.pygameAPI import *


def full_exit():
    pygame.quit()
    sys_exit(0)


cfg = configparser.ConfigParser()


def config_read(config_file):
    global cfg, config_folder
    cfg.read(config_folder + config_file)


config_read(config_game_settings)
s = "Game Settings"
resolution_width = cfg.getint(s, RESOLUTION_WIDTH)
resolution_height = cfg.getint(s, RESOLUTION_HEIGHT)
resolution = (resolution_width, resolution_height)
FPS = cfg.getint(s, FRAMES_PER_SECOND)
FPS_MainMenu = cfg.getint(s, FRAMES_PER_SECOND_MAIN_MENU)

pygame.init()

sc = pygame.display.set_mode(resolution)
pygame.display.set_caption(main_title)
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
mouseLMB = mousePressedButtons[0]


def draw_and_input(button):
    if collide(mousePos, button.pos):
        button.draw()


# Input constants
RIGHT = 0
LEFT = 1
ROTATE_RIGHT = 10
ROTATE_LEFT = 11
SHOOT = 20

menu_color = colors[randint(0, len(colors) - 1)] if enable_random_menu_color else default_menu_color

font_path = fonts_folder + font_name

font_NES_24 = pygame.font.Font(font_path, 24)
font_NES_32 = pygame.font.Font(font_path, 32)
font_NES_48 = pygame.font.Font(font_path, 48)
font_NES_64 = pygame.font.Font(font_path, 64)

font_round_HUD = font_NES_24
font_game_HUD = font_NES_48

# Round system
roundsMax = 3
rounds = [0, 0]

# Collision
borders = [[-5, -5, 10, resHeight + 10], [resWidth - 5, -5, 10, resHeight + 10]]
obstacles = [[-5, -20, resWidth + 10, 10], [-5, resHeight + 10, resWidth + 10, 10]]


# Ship classes
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

    if useAcceleration:
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
control_schemes = []
control_schemes.append({
    RIGHT: pygame.K_d,
    LEFT: pygame.K_a,
    SHOOT: pygame.K_SPACE,
})
control_schemes.append({
    RIGHT: pygame.K_KP6,
    LEFT: pygame.K_KP4,
    SHOOT: pygame.K_KP_ENTER,
})

players = []
ships = []
ships.append(construct_ship_from_cfg(cfg_multiplayer, 1, [0, resHeight - 100]))
ships.append(construct_ship_from_cfg(cfg_multiplayer, 2, [0, 100]))
players.append(PlayerInput(ships[0], control_schemes[0]))
players.append(PlayerInput(ships[1], control_schemes[1]))

missiles = []

borders = []
death_triggers = []

game_objects = []

# HUD
HUD_p1_hp_pos = (10, resolution[1] - 45, 150, 45)
HUD_p1_ammo_pos = (resolution[0] - 160, resolution[1] - 45, 150, 45)
HUD_p2_hp_pos = (10, 0, 150, 45)
HUD_p2_ammo_pos = (resolution[0] - 160, 0, 150, 45)
HUD_round_score_pos = (resolution[0] // 2 - 75, 0, 150, 45)
HUD_game_score_pos = (resolution[0] // 2, resolution[1] // 2, 0, 0)

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


ui_elements = []
hud_elements = []

time_previous_frame = 0
delta_time = 0


def round_cycle():
    global time_previous_frame, delta_time
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

        for game_object in game_objects:
            game_object.update_position(delta_time)

        for player in players:
            player.control(keys)

        for ship in ships:
            if ship.ai_controlled:
                ship.ai.control(missiles)
                continue

        for missile in missiles:
            for ship in ships:
                if collides(missile, ship.body) and missile.sender.faction != ship.faction:
                    ship.take_damage(missile.damage)

        for game_object in game_objects:
            game_object.draw(sc)

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
        delta_time = clock.get_time() / 1000 - time_previous_frame
        time_previous_frame = clock.get_time() / 1000


if __name__ == "__main__":
    for i in range(roundsMax):
        for ship in ships:
            reset_stats(ship)

        round_cycle()

        pygame.display.update()
        draw_game_HUD(sc, BLACK, BLACK, GREEN)
        wait(1, FPS_MainMenu)
