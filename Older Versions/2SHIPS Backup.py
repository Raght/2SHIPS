import pygame
from random import randint
from sys import exit as sys_exit
from os.path import abspath
from Engine2D import does_collide
import UI
try:
    import configparser as configparser
except ImportError:
    import ConfigParser as configparser

#rounds = int(input("Number of rounds: "))
rounds = 3


def full_exit():
    pygame.quit()
    sys_exit()
    

pygame.init()
config = configparser.ConfigParser()

path_gameFolder = abspath(__file__).replace("\\", "/")
path_gameFolder = path_gameFolder.replace(path_gameFolder[len(path_gameFolder) - path_gameFolder[::-1].index("/"):len(path_gameFolder)], "")
path_gameResources = path_gameFolder
config.read(path_gameResources + "config/players.ini")

# Recommended resolution: 800 x 640
resolution = (800, 640)
windowName = '2SHIPS Multiplayer'
window = pygame.display.set_mode(resolution)
pygame.display.set_caption(windowName)

FPS = 120
FPS_GAMEMENU = 60
clock = pygame.time.Clock()


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

team1_color = eval(config.get("Players", "team1_color"))
team2_color = eval(config.get("Players", "team2_color"))


# Player's body
player_bodyWidth = int(config.get("Players", "player_bodyWidth"))
player_bodyHeight = int(config.get("Players", "player_bodyHeight"))
player_headWidth = int(config.get("Players", "player_headWidth"))
player_headHeight = int(config.get("Players", "player_headHeight"))
player_bodyPos = pygame.Rect(randint(7, resolution[0] - player_bodyWidth - 7), resolution[1] - 60 - player_bodyHeight,
                             player_bodyWidth, player_bodyHeight)
player_headPos = pygame.Rect(player_bodyPos[0] + player_bodyWidth // 2 - player_headWidth // 2,
                             player_bodyPos[1] - player_headHeight,
                             player_headWidth,
                             player_bodyHeight)
# Player's characteristics
player_hp = int(config.get("Players", "player_hp"))
player_maxHP = player_hp
player_speed = int(config.get("Players", "player_speed"))
player_ammo = int(config.get("Players", "player_ammo"))
player_maxAmmo = player_ammo
player_bulletDamage = int(config.get("Players", "player_bulletDamage"))
player_bulletSpeed = int(config.get("Players", "player_bulletSpeed"))
# Player's Bullet
player_bulletWidth = int(config.get("Players", "player_bulletWidth"))
player_bulletHeight = int(config.get("Players", "player_bulletHeight"))
player_bulletPos = (0, 0, 1, 1)
player_bulletColor = eval(config.get("Players", "player_bulletColor"))
player_bulletMissiles = []

# Enemy's body
player2_bodyWidth = int(config.get("Players", "player2_bodyWidth"))
player2_bodyHeight = int(config.get("Players", "player2_bodyHeight"))
player2_headWidth = int(config.get("Players", "player2_headWidth"))
player2_headHeight = int(config.get("Players", "player2_headHeight"))
player2_bodyPos = pygame.Rect(randint(7, resolution[0] - player2_bodyWidth - 7), 60,
                              player2_bodyWidth, player2_bodyHeight)
player2_headPos = pygame.Rect(player2_bodyPos[0] + player2_bodyWidth // 2 - player2_headWidth // 2, 60 + player2_bodyHeight,
                              player2_headWidth, player2_headHeight)
# Enemy's characteristics
player2_hp = int(config.get("Players", "player2_hp"))
player2_maxHP = player2_hp
player2_speed = int(config.get("Players", "player2_speed"))
player2_ammo = int(config.get("Players", "player2_ammo"))
player2_maxAmmo = player2_ammo
player2_bulletDamage = int(config.get("Players", "player2_bulletDamage"))
# Enemy's Bullet
player2_bulletWidth = int(config.get("Players", "player2_bulletWidth"))
player2_bulletHeight = int(config.get("Players", "player2_bulletHeight"))
player2_bulletPos = (0, 0, 1, 1)
player2_bulletColor = eval(config.get("Players", "player2_bulletColor"))
player2_bulletSpeed = int(config.get("Players", "player2_bulletSpeed"))
player2_bulletMissiles = []

# Cheats
cheat_player_unlimitedammo = int(config.get("Cheats", "cheat_player_unlimitedammo"))
cheat_player2_unlimitedammo = int(config.get("Cheats", "cheat_player2_unlimitedammo"))

cheat_player_godmode = int(config.get("Cheats", "cheat_player_godmode"))
cheat_player2_godmode = int(config.get("Cheats", "cheat_player2_godmode"))

cheat_player_autofire = int(config.get("Cheats", "cheat_player_autofire"))
cheat_player_autofire_delay = int(config.get("Cheats", "cheat_player_autofire_delay"))
cheat_player_autofire_maxDelay = int(cheat_player_autofire_delay // (1000 / FPS))
cheat_player_autofire_delay = cheat_player_autofire_maxDelay

cheat_player2_autofire = int(config.get("Cheats", "cheat_player2_autofire"))
cheat_player2_autofire_delay = int(config.get("Cheats", "cheat_player2_autofire_delay"))
cheat_player2_autofire_maxDelay = int(cheat_player2_autofire_delay // (1000 / FPS))
cheat_player2_autofire_delay = cheat_player2_autofire_maxDelay


class Ship:
    def __init__(self, hp, maxHP, speed, ammo, maxAmmo, bodyPos, headPos, bodyWidth, bodyHeight, headWidth, headHeight,
                 bulletDamage, bulletWidth, bulletHeight, bulletPos, bulletSpeed, bulletColor, missiles):
        self.hp = hp
        self.maxHP = maxHP
        self.speed = speed
        self.bodyPos = bodyPos
        self.headPos = headPos
        self.bodyWidth = bodyWidth
        self.bodyHeight = bodyHeight
        self.headWidth = headWidth
        self.headHeight = headHeight
        self.ammo = ammo
        self.maxAmmo = maxAmmo
        self.bulletDamage = bulletDamage
        self.bulletWidth = bulletWidth
        self.bulletHeight = bulletHeight
        self.bulletPos = bulletPos
        self.bulletSpeed = bulletSpeed
        self.bulletColor = bulletColor
        self.missiles = missiles

    def shoot(self):
        self.bulletPos = [self.bodyPos[0] + self.bodyWidth // 2 - self.bulletWidth // 2,
                          self.bodyPos[1] - self.bulletHeight // 2,
                          self.bulletWidth,
                          self.bulletHeight]
        self.missiles.append(self.bulletPos)

    def move_bullets(self):
        for pos in self.missiles:
            pygame.draw.rect(window, self.bulletColor, pos)
            self.missiles[self.missiles.index(pos)][1] += self.bulletSpeed

            if pos[1] > resolution[1] + 10:
                del self.missiles[self.missiles.index(pos)]


class Player(Ship):
    def move_bullets(self):
        for pos in self.missiles:
            pygame.draw.rect(window, self.bulletColor, pos)
            self.missiles[self.missiles.index(pos)][1] -= self.bulletSpeed

            if pos[1] < -10:
                del self.missiles[self.missiles.index(pos)]


class Enemy(Ship):
    pass


player = Player(player_hp, player_maxHP, player_speed, player_ammo, player_maxAmmo,
                player_bodyPos, player_headPos, player_bodyWidth, player_bodyHeight, player_headWidth, player_headHeight,
                player_bulletDamage, player_bulletWidth, player_bulletHeight, player_bulletPos,
                player_bulletSpeed, player_bulletColor, player_bulletMissiles)
player2 = Enemy(player2_hp, player2_maxHP, player2_speed, player2_ammo, player2_maxAmmo,
                player2_bodyPos, player2_headPos, player2_bodyWidth, player2_bodyHeight, player2_headWidth, player2_headHeight,
                player2_bulletDamage, player2_bulletWidth, player2_bulletHeight, player2_bulletPos,
                player2_bulletSpeed, player2_bulletColor, player2_bulletMissiles)


path_font_UI = "fonts/BigNoodleTooOblique.ttf"

font_UI = pygame.font.Font(path_font_UI, 45)
font_gameOutcome = pygame.font.Font(path_font_UI, 135)

UI_player_hp_pos = (0 + 25, resolution[1] - 45)
UI_player_ammo_pos = (resolution[0] - 115, resolution[1] - 45)
UI_player2_hp_pos = (0 + 25, 0)
UI_player2_ammo_pos = (resolution[0] - 115, 0)
UI_rounds_score_pos = (resolution[0] // 2 - resolution[0] // 25, 0)

player_rounds_counter, enemy_rounds_counter = 0, 0

test = UI.Button([resolution[0] // 2 - 60, resolution[1] - 100, 120, 100], font_UI, "EXIT")

def main():
    global cheat_player_autofire_delay, cheat_player2_autofire_delay
    while True:
        window.fill(BLACK)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                full_exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not(cheat_player_autofire):
                    if player.ammo > 0:
                        player.shoot()
                        if not(cheat_player_unlimitedammo):
                            player.ammo -= 1
                if event.key == pygame.K_KP0 and not(cheat_player2_autofire):
                    if player2.ammo > 0:
                        player2.shoot()
                        if not(cheat_player2_unlimitedammo):
                            player2.ammo -= 1
    

        # Moving player by pressing buttons
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and not (player.bodyPos[0] <= 5):
            player.bodyPos[0] -= player.speed
            player.headPos[0] -= player.speed
        if keys[pygame.K_d] and not (player.bodyPos[0] >= resolution[0] - player.bodyWidth - 5):
            player.bodyPos[0] += player.speed
            player.headPos[0] += player.speed

        if keys[pygame.K_LEFT] and not (player2.bodyPos[0] <= 5):
            player2.bodyPos[0] -= player2.speed
            player2.headPos[0] -= player2.speed
        if keys[pygame.K_RIGHT] and not (player2.bodyPos[0] >= resolution[0] - player2.bodyWidth - 5):
            player2.bodyPos[0] += player2.speed
            player2.headPos[0] += player2.speed

        m_pressedButtons = pygame.mouse.get_pressed()
        m_pos = pygame.mouse.get_pos() + (1, 1)
        
        if does_collide(m_pos, test.pos):
            if m_pressedButtons[0]:
                full_exit()
            test.draw_outline(window, GREEN, BLACK)
        else:
            test.draw(window, 4, GREEN, GREEN)
        
        if cheat_player_autofire_delay < cheat_player_autofire_maxDelay:
            cheat_player_autofire_delay += 1
        if (player.ammo > 0 and cheat_player_autofire and keys[pygame.K_SPACE] and
           cheat_player_autofire_delay == cheat_player_autofire_maxDelay):
            player.shoot()
            if not(cheat_player_unlimitedammo):
                player.ammo -= 1
            cheat_player_autofire_delay = 0

        if cheat_player2_autofire_delay < cheat_player2_autofire_maxDelay:
            cheat_player2_autofire_delay += 1
        if (player2.ammo > 0 and cheat_player2_autofire and keys[pygame.K_KP0] and
           cheat_player2_autofire_delay == cheat_player2_autofire_maxDelay):
            player2.shoot()
            if not(cheat_player2_unlimitedammo):
                player2.ammo -= 1
            cheat_player2_autofire_delay = 0
        

        # Draw player
        pygame.draw.rect(window, team1_color, player.bodyPos)
        pygame.draw.rect(window, team1_color, player.headPos)

        # Draw enemy
        pygame.draw.rect(window, team2_color, player2.bodyPos)
        pygame.draw.rect(window, team2_color, player2.headPos)

        
        # Collision detection for player's bullets
        for missile in player.missiles:
            if not(missile[1] > 60 + player2.bodyHeight + player2.headHeight or
                   missile[1] < 60 - player.bulletHeight):
                if (does_collide(missile, player2.headPos) or
                   does_collide(missile, player2.bodyPos)):
                    if not(cheat_player2_godmode):
                        if player2.hp > 0:
                            player2.hp -= player.bulletDamage
                        else:
                            player2.hp = 0

                    del player.missiles[player.missiles.index(missile)]

        player.move_bullets()
        

        # Collision detection for enemy's bullets
        for missile in player2.missiles:
            if not(missile[1] > 60 + player2.bodyHeight + player2.headHeight and
                   missile[1] < resolution[1] - 60 - player.bodyHeight - player.headHeight):
                if (does_collide(missile, player.headPos) or
                   does_collide(missile, player.bodyPos)):
                    if not(cheat_player_godmode):
                        if player.hp > 0:
                                player.hp -= player2.bulletDamage
                        else:
                            player.hp = 0

                    del player2.missiles[player2.missiles.index(missile)]

        player2.move_bullets()
        

        # Draw UI
        # Player's health
        pygame.draw.line(window, team1_color, (0, resolution[1] - 45), (150, resolution[1] - 45), 2)
        pygame.draw.line(window, team1_color, (resolution[0] - 150, resolution[1] - 45),
                         (resolution[0], resolution[1] - 45), 2)
        UI_player_hp = font_UI.render(str(player.hp) + " HP", 1, team1_color)
        window.blit(UI_player_hp, UI_player_hp_pos)

        # Player's ammo
        pygame.draw.line(window, team1_color, (150, resolution[1] - 45), (150, resolution[1]), 2)
        pygame.draw.line(window, team1_color, (resolution[0] - 150, resolution[1] - 45), (resolution[0] - 150, resolution[1]), 2)
        UI_player_ammo = font_UI.render(str(player.ammo) + "/" + str(player.maxAmmo), 1, team1_color)
        window.blit(UI_player_ammo, UI_player_ammo_pos)
        
        # Enemy's health
        pygame.draw.line(window, team2_color, (0, 45), (150, 45), 2)
        pygame.draw.line(window, team2_color, (150, 45), (150, 0), 2)
        UI_player2_hp = font_UI.render(str(player2.hp) + " HP", 1, team2_color)
        window.blit(UI_player2_hp, UI_player2_hp_pos)

        # Enemy's ammo
        pygame.draw.line(window, team2_color, (resolution[0], 45), (resolution[0] - 150, 45), 2)
        pygame.draw.line(window, team2_color, (resolution[0] - 150, 45), (resolution[0] - 150, 0), 2)
        UI_player2_ammo = font_UI.render(str(player2.ammo) + "/" + str(player2.maxAmmo), 1, team2_color)
        window.blit(UI_player2_ammo, UI_player2_ammo_pos)

        # Rounds score
        UI_rounds_score = font_UI.render(str(player_rounds_counter) + " : " + str(enemy_rounds_counter), 1, WHITE)
        window.blit(UI_rounds_score, UI_rounds_score_pos)


        if player2.hp <= 0 or (player2.ammo == 0 and len(player2.missiles) == 0):
            break
        if player.hp <= 0 or (player.ammo == 0 and len(player.missiles) == 0):
            break


        pygame.display.update()
        clock.tick(FPS)


for roundsCounter in range(rounds):
    player.hp = player.maxHP
    player2.hp = player2.maxHP
    
    player.ammo = player.maxAmmo
    player2.ammo = player2.maxAmmo

    player.missiles, player2.missiles = [], []
    
    player.bodyPos[0] = randint(7, resolution[0] - player_bodyWidth - 7)
    player.headPos[0] = player.bodyPos[0] + player_bodyWidth // 2 - player_headWidth // 2
    
    player2.bodyPos[0] = randint(7, resolution[0] - player2_bodyWidth - 7)
    player2.headPos[0] = player2.bodyPos[0] + player2_bodyWidth // 2 - player2_headWidth // 2
    
    main()

    font_roundOutcome = pygame.font.Font(path_font_UI, 135)
    if player2.hp <= 0 or (player2.ammo == 0 and len(player2.missiles) == 0):
        UI_message_roundOutcome = font_roundOutcome.render("PLAYER1 WON!", 1, team1_color)
        player_rounds_counter += 1
    elif player.hp <= 0 or (player.ammo == 0 and len(player.missiles) == 0):
        UI_message_roundOutcome = font_roundOutcome.render("PLAYER2 WON!", 1, team2_color)
        enemy_rounds_counter += 1


    for frame in range(1, 181):
        window.fill(BLACK)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                full_exit()

        if frame < 91:
            window.blit(UI_message_roundOutcome, (0, 0))
        elif frame >= 91 and roundsCounter < rounds - 1:
            UI_rounds_score = font_gameOutcome.render(str(player_rounds_counter) + " : " + str(enemy_rounds_counter), 1, WHITE)
            window.blit(UI_rounds_score, (0, 0))
        else:
            break

        pygame.display.update()
        clock.tick(FPS_GAMEMENU)


UI_message_rounds = font_gameOutcome.render(str(player_rounds_counter) + " : " + str(enemy_rounds_counter), 1, WHITE)

if player_rounds_counter > enemy_rounds_counter:
    UI_message_gameOutcome = font_gameOutcome.render("PLAYER1 WON!", 1, team1_color)
elif player_rounds_counter < enemy_rounds_counter:
    UI_message_gameOutcome = font_gameOutcome.render("PLAYER2 WON!", 1, team2_color)
elif player_rounds_counter == enemy_rounds_counter:
    UI_message_gameOutcome = font_gameOutcome.render("DRAW!", 1, YELLOW)
    
while True:
    window.fill(BLACK)

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            full_exit()

    window.blit(UI_message_rounds, (0, 0))
    window.blit(UI_message_gameOutcome, (0, 140))

    pygame.display.update()
    clock.tick(FPS_GAMEMENU)
