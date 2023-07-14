
import pygame
from random import randint
try:
    import configparser as configparser
except ImportError:
    import ConfigParser as configparser


config = configparser.ConfigParser()
config.read("config/gameSettings.ini")
config.read("config/sg_players.ini")
config.read("config/mp_players.ini")


def set_gameSettings_config():
    global resolution, FPS, FPS_GAMEMENU
    resolution = eval(config.get("Game Settings", "resolution"))
    FPS = int(config.get("Game Settings", "FPS"))
    FPS_GAMEMENU = int(config.get("Game Settings", "FPS_GAMEMENU"))

set_gameSettings_config()

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

def set_sg_config():
    global sg_team1_color, sg_team2_color
    global player1_bodyWidth, player1_bodyHeight, player1_headWidth, player1_headHeight, player1_bodyPos, player1_headPos
    global player1_hp, player1_maxHP, player1_speed, player1_ammo, player1_maxAmmo, player1_bulletDamage, player1_bulletSpeed
    global player1_bulletWidth, player1_bulletHeight, player1_bulletPos, player1_bulletColor, player1_bulletMissiles
    global player2_bodyWidth, player2_bodyHeight, player2_headWidth, player2_headHeight, player2_bodyPos, player2_headPos
    global player2_hp, player2_maxHP, player2_speed, player2_ammo, player2_maxAmmo, player2_bulletDamage, player2_bulletSpeed
    global player2_bulletWidth, player2_bulletHeight, player2_bulletPos, player2_bulletColor, player2_bulletMissiles
    global cheat_player1_unlimitedammo, cheat_player1_godmode, cheat_player1_autofire, cheat_player1_autofire_delay, cheat_player1_autofire_maxDelay

    # Team colors
    sg_team1_color = eval(config.get("Player and Bots", "sg_team1_color"))
    sg_team2_color = eval(config.get("Player and Bots", "sg_team2_color"))

    # Player's body
    player1_bodyWidth = int(config.get("Player and Bots", "player1_bodyWidth"))
    player1_bodyHeight = int(config.get("Player and Bots", "player1_bodyHeight"))
    player1_headWidth = int(config.get("Player and Bots", "player1_headWidth"))
    player1_headHeight = int(config.get("Player and Bots", "player1_headHeight"))
    player1_bodyPos = pygame.Rect(randint(7, resolution[0] - player1_bodyWidth - 7),
                                  resolution[1] - 60 - player1_bodyHeight,
                                  player1_bodyWidth, player1_bodyHeight)
    player1_headPos = pygame.Rect(player1_bodyPos[0] + player1_bodyWidth // 2 - player1_headWidth // 2,
                                  player1_bodyPos[1] - player1_headHeight,
                                  player1_headWidth,
                                  player1_bodyHeight)
    # Player's characteristics
    player1_hp = int(config.get("Player and Bots", "player1_hp"))
    player1_maxHP = player1_hp
    player1_speed = int(config.get("Player and Bots", "player1_speed"))
    player1_ammo = int(config.get("Player and Bots", "player1_ammo"))
    player1_maxAmmo = player1_ammo
    player1_bulletDamage = int(config.get("Player and Bots", "player1_bulletDamage"))
    player1_bulletSpeed = int(config.get("Player and Bots", "player1_bulletSpeed"))
    # Player's Bullet
    player1_bulletWidth = int(config.get("Player and Bots", "player1_bulletWidth"))
    player1_bulletHeight = int(config.get("Player and Bots", "player1_bulletHeight"))
    player1_bulletPos = (0, 0, 1, 1)
    player1_bulletColor = eval(config.get("Player and Bots", "player1_bulletColor"))
    player1_bulletMissiles = []

    # Enemy's body
    player2_bodyWidth = int(config.get("Player and Bots", "player2_bodyWidth"))
    player2_bodyHeight = int(config.get("Player and Bots", "player2_bodyHeight"))
    player2_headWidth = int(config.get("Player and Bots", "player2_headWidth"))
    player2_headHeight = int(config.get("Player and Bots", "player2_headHeight"))
    player2_bodyPos = pygame.Rect(randint(7, resolution[0] - player2_bodyWidth - 7), 60,
                                player2_bodyWidth, player2_bodyHeight)
    player2_headPos = pygame.Rect(player2_bodyPos[0] + player2_bodyWidth // 2 - player2_headWidth // 2, 60 + player2_bodyHeight,
                                player2_headWidth, player2_headHeight)
    # Enemy's characteristics
    player2_hp = int(config.get("Player and Bots", "player2_hp"))
    player2_maxHP = player2_hp
    player2_speed = int(config.get("Player and Bots", "player2_speed"))
    player2_ammo = int(config.get("Player and Bots", "player2_ammo"))
    player2_maxAmmo = player2_ammo
    player2_bulletDamage = int(config.get("Player and Bots", "player2_bulletDamage"))
    # Enemy's Bullet
    player2_bulletWidth = int(config.get("Player and Bots", "player2_bulletWidth"))
    player2_bulletHeight = int(config.get("Player and Bots", "player2_bulletHeight"))
    player2_bulletPos = (0, 0, 1, 1)
    player2_bulletColor = eval(config.get("Player and Bots", "player2_bulletColor"))
    player2_bulletSpeed = int(config.get("Player and Bots", "player2_bulletSpeed"))
    player2_bulletMissiles = []

    # Cheats
    cheat_player1_unlimitedammo = int(config.get("Cheats Singleplayer", "cheat_player1_unlimitedammo"))

    cheat_player1_godmode = int(config.get("Cheats Singleplayer", "cheat_player1_godmode"))

    cheat_player1_autofire = int(config.get("Cheats Singleplayer", "cheat_player1_autofire"))
    cheat_player1_autofire_delay = int(config.get("Cheats Singleplayer", "cheat_player1_autofire_delay"))
    cheat_player1_autofire_maxDelay = int(cheat_player1_autofire_delay // (1000 / FPS))
    cheat_player1_autofire_delay = cheat_player1_autofire_maxDelay
