import pygame
from random import randint, shuffle
from sys import exit as sys_exit
from os.path import abspath
try:
    import configparser as configparser
except ImportError:
    import ConfigParser as configparser
from Engine2D import collide
import UI
path_gameFolder = abspath(__file__).replace("\\", "/")
path_gameFolder = path_gameFolder.replace(path_gameFolder[len(path_gameFolder) - path_gameFolder[::-1].index("/"):len(path_gameFolder)], "")
path_gameResources = path_gameFolder

config = configparser.ConfigParser()
config.read("config/gameSettings.ini")


def full_exit():
    pygame.quit()
    sys_exit()


resWidth = int(config.get("Game Settings", "resWidth"))
resHeight = int(config.get("Game Settings", "resHeight"))
resolution = (resWidth, resHeight)

FPS = int(config.get("Game Settings", "FPS"))
FPS_GAMEMENU = int(config.get("Game Settings", "FPS_MainMenu"))

pygame.init()
windowName = '2SHIPS'
window = pygame.display.set_mode(resolution)
pygame.display.set_caption(windowName)
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

enable_random_menu_color = 1
colors = [RED, GREEN, BLUE, WHITE, YELLOW, ORANGE, GOLD, PINK, DEEPPINK, ORCHID, MAROON, MAGENTA,
          DARKVIOLET, PURPLE, CYAN, TURQUOISE, SKYBLUE, TAN, CHOCOLATE]
colors_shuffled = [RED, GREEN, BLUE, WHITE, YELLOW, ORANGE, GOLD, PINK, DEEPPINK, ORCHID, MAROON, MAGENTA,
          DARKVIOLET, PURPLE, CYAN, TURQUOISE, SKYBLUE, TAN, CHOCOLATE]

if enable_random_menu_color:
    menu_color = colors[randint(0, len(colors) - 1)]
else:
    menu_color = GREEN


sg_rounds = ""
mp_rounds = ""


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


path_font_UI = "fonts/BigNoodleTooOblique.ttf"

font_UI = pygame.font.Font(path_font_UI, 45)
font_60 = pygame.font.Font(path_font_UI, 60)
font_text = pygame.font.Font(path_font_UI, 90)
font_roundOutcome = pygame.font.Font(path_font_UI, 135)
font_gameOutcome = pygame.font.Font(path_font_UI, 135)

UI_player1_hp_pos = (0 + 25, resolution[1] - 45)
UI_player1_ammo_pos = (resolution[0] - 115, resolution[1] - 45)
UI_player2_hp_pos = (0 + 25, 0)
UI_player2_ammo_pos = (resolution[0] - 115, 0)
UI_rounds_score_pos = (resolution[0] // 2 - resolution[0] // 25, 0)


UI_STATE_MAINMENU = 0
UI_STATE_SG_INGAME = 1
UI_STATE_MP_INGAME = 2
UI_STATE_SG_ROUNDSCHOICE = 3
UI_STATE_MP_ROUNDSCHOICE = 4

UI_currentState = UI_STATE_MAINMENU

def change_UI_state(UI_newState):
    global UI_currentState
    UI_currentState = UI_newState


btn_mainMenu_singleplayer = UI.Button([resolution[0] // 2 - 160, resolution[1] // 2 - 75, 320, 60], font_UI, "SINGLEPLAYER")
btn_mainMenu_multiplayer = UI.Button([resolution[0] // 2 - 160, resolution[1] // 2, 320, 60], font_UI, "MULTIPLAYER")
btn_mainMenu_exit = UI.Button([resolution[0] // 2 - 160, resolution[1] // 2 + 150, 320, 60], font_UI, "EXIT GAME")
btn_roundsChoice_backToMainMenu = UI.Button([resolution[0] // 72, resolution[1] // 56, 75, 75], font_UI, "")

btn_roundsChoice_backToMainMenu_trianglePos = ((btn_roundsChoice_backToMainMenu.pos[0] + 24,
                                                btn_roundsChoice_backToMainMenu.pos[1] + btn_roundsChoice_backToMainMenu.pos[3] // 2),
                                               (btn_roundsChoice_backToMainMenu.pos[0] + 49,
                                             btn_roundsChoice_backToMainMenu.pos[1] + btn_roundsChoice_backToMainMenu.pos[3] // 3),
                                               (btn_roundsChoice_backToMainMenu.pos[0] + 49,
                                             btn_roundsChoice_backToMainMenu.pos[1] + btn_roundsChoice_backToMainMenu.pos[3] // 1.5),
                                               (btn_roundsChoice_backToMainMenu.pos[0] + 49,
                                             btn_roundsChoice_backToMainMenu.pos[1] + btn_roundsChoice_backToMainMenu.pos[3] // 1.5))

btn_roundsChoice_play = UI.Button([resolution[0] // 2 - 160, resolution[1] // 2 + 150, 320, 60], font_UI, "PLAY")
btn_endscreen_backToMainMenu = UI.Button([resolution[0] // 2 - 190, resolution[1] - 140, 380, 70], font_UI, "BACK TO MAIN MENU")


def draw_roundsChoiceScreen(rounds, UI_newState):
    global sg_rounds, mp_rounds

    rounds = str(rounds)
    while True:
        window.fill(BLACK)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys_exit()
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_0 or event.key == pygame.K_KP0) and len(rounds):
                    rounds += "0"
                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    rounds += "1"
                if event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    rounds += "2"
                if event.key == pygame.K_3 or event.key == pygame.K_KP3:
                    rounds += "3"
                if event.key == pygame.K_4 or event.key == pygame.K_KP4:
                    rounds += "4"
                if event.key == pygame.K_5 or event.key == pygame.K_KP5:
                    rounds += "5"
                if event.key == pygame.K_6 or event.key == pygame.K_KP6:
                    rounds += "6"
                if event.key == pygame.K_7 or event.key == pygame.K_KP7:
                    rounds += "7"
                if event.key == pygame.K_8 or event.key == pygame.K_KP8:
                    rounds += "8"
                if event.key == pygame.K_9 or event.key == pygame.K_KP9:
                    rounds += "9"
                if event.key == pygame.K_BACKSPACE and len(rounds):
                    rounds = rounds[::-1].replace(rounds[-1], "", 1)[::-1]
                if event.key == pygame.K_ESCAPE:
                    change_UI_state(UI_STATE_MAINMENU)
                    return ""
                if (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and len(rounds):
                    change_UI_state(UI_newState)
                    return int(rounds)

        if UI_currentState == UI_STATE_MAINMENU:
            return ""
        
        m_pos = pygame.mouse.get_pos() + (1, 1)
        m_pressedButtons = pygame.mouse.get_pressed()
        
        if collide(m_pos, btn_roundsChoice_backToMainMenu.pos):
            if m_pressedButtons[0]:
                change_UI_state(UI_STATE_MAINMENU)
                return ""
            btn_roundsChoice_backToMainMenu.draw(window, menu_color, BLACK)
            pygame.draw.polygon(window, BLACK, btn_roundsChoice_backToMainMenu_trianglePos)
            pygame.draw.aaline(window, BLACK, btn_roundsChoice_backToMainMenu_trianglePos[0], btn_roundsChoice_backToMainMenu_trianglePos[1])
            pygame.draw.aaline(window, BLACK, btn_roundsChoice_backToMainMenu_trianglePos[0], btn_roundsChoice_backToMainMenu_trianglePos[2])
        else:
            btn_roundsChoice_backToMainMenu.draw_outline(window, menu_color, menu_color, 4)
            pygame.draw.polygon(window, menu_color, btn_roundsChoice_backToMainMenu_trianglePos)
            pygame.draw.aaline(window, menu_color, btn_roundsChoice_backToMainMenu_trianglePos[0], btn_roundsChoice_backToMainMenu_trianglePos[1])
            pygame.draw.aaline(window, menu_color, btn_roundsChoice_backToMainMenu_trianglePos[0], btn_roundsChoice_backToMainMenu_trianglePos[2])

        if collide(m_pos, btn_roundsChoice_play.pos):
            if m_pressedButtons[0] and len(rounds):
                change_UI_state(UI_newState)
                return int(rounds)
            btn_roundsChoice_play.draw(window, menu_color, BLACK)
        else:
            btn_roundsChoice_play.draw_outline(window, menu_color, menu_color, 4)

        UI_roundschoice_message = font_60.render("HOW MANY ROUNDS DO YOU WANT TO PLAY?", 1, menu_color)
        window.blit(UI_roundschoice_message, (resolution[0] // 2 - font_60.size("HOW MANY ROUNDS DO YOU WANT TO PLAY?")[0] // 2,
                                              resolution[1] // 2 - font_60.size("A")[1]))
        UI_roundschoice_rounds = font_60.render(rounds, 1, menu_color)
        window.blit(UI_roundschoice_rounds, (resolution[0] // 2 - font_60.size(rounds)[0] // 2,
                                             resolution[1] // 2))
        pygame.draw.rect(window, WHITE, (resolution[0] // 2 + font_60.size(rounds)[0] // 2, resolution[1] // 2 + font_60.size("A")[1] - 18,
                                         25, 6))

        pygame.display.update()
        clock.tick(FPS_GAMEMENU)

def singleplayer():
    global player2_shootDelay, player2_switchDirectionDelay, cheat_player1_autofire_delay
    while True:
        window.fill(BLACK)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys_exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not cheat_player1_autofire:
                    if player1.ammo > 0:
                        player1.shoot()
                        if not cheat_player1_unlimitedAmmo:
                            player1.ammo -= 1

        # Moving player by pressing buttons
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and not (player1.bodyPos[0] <= 5):
            player1.bodyPos[0] -= player1.speed
            player1.headPos[0] -= player1.speed
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and not (
            player1.bodyPos[0] >= resolution[0] - player1.bodyWidth - 5):
            player1.bodyPos[0] += player1.speed
            player1.headPos[0] += player1.speed

        if cheat_player1_autofire_delay < cheat_player1_autofire_maxDelay:
            cheat_autofire_delay += 1
        if (cheat_player1_autofire and keys[pygame.K_SPACE]
            and cheat_player1_autofire_delay == cheat_player1_autofire_maxDelay):
            player1.shoot()
            if not (cheat_player1_unlimitedAmmo):
                player1.ammo -= 1
            cheat_autofire_delay = 0

        # Moving enemy
        player2.bodyPos[0] += player2.speed
        player2.headPos[0] += player2.speed

        if (player2.bodyPos[0] <= 5 or
            player2.bodyPos[0] >= resolution[0] - player2.bodyWidth - 5):
            player2.speed = -player2.speed

        # Draw player
        pygame.draw.rect(window, GREEN, player1.bodyPos)
        pygame.draw.rect(window, GREEN, player1.headPos)

        # Draw enemy
        pygame.draw.rect(window, RED, player2.bodyPos)
        pygame.draw.rect(window, RED, player2.headPos)

        if player2_switchDirectionDelay < player2_switchDirectionMaxDelay:
            player2_switchDirectionDelay += 1

        # Collision detection for player's bullets
        for missile in player1.missiles:
            if (collide(missile, player2.headPos) or
                collide(missile, player2.bodyPos)):
                if player2.hp > 0:
                    player2.hp -= player1.bulletDamage
                else:
                    player2.hp = 0

                del player1.missiles[player1.missiles.index(missile)]

            if (missile[0] > player2.bodyPos[0] and
               missile[0] < player2.bodyPos[0] + player2.bodyWidth and
               missile[1] > 60 + player2.bodyHeight + player2.headHeight and
               missile[1] < resolution[1] + player2.headHeight and
               player2_switchDirectionDelay == player2_switchDirectionMaxDelay):
                player2.speed = -player2.speed
                player2_switchDirectionDelay = 0

        player1.move_bullets()

        if player2_shootDelay < player2_shootMaxDelay:
            player2_shootDelay += 1

        if (player2.headPos[0] >= player1.bodyPos[0] and
           player2.headPos[0] < player1.bodyPos[0] + player1.bodyWidth - player2.headWidth // 2 and
           player2_shootDelay == player2_shootMaxDelay):
            player2.shoot()
            player2_shootDelay = 0

        # Collision detection for enemy's bullets
        for missile in player2.missiles:
            if (collide(missile, player1.headPos) or
                collide(missile, player1.bodyPos)):
                if player1.hp > 0:
                    if not (cheat_player1_godmode):
                        player1.hp -= player2.bulletDamage
                else:
                    player1.hp = 0

                del player2.missiles[player2.missiles.index(missile)]

        player2.move_bullets()

        # Draw UI
        # Player's health
        pygame.draw.line(window, sg_team1_color, (0, resolution[1] - 45), (150, resolution[1] - 45), 2)
        pygame.draw.line(window, sg_team1_color, (resolution[0] - 150, resolution[1] - 45),
                         (resolution[0], resolution[1] - 45), 2)
        UI_player1_hp = font_UI.render(str(player1.hp) + " HP", 1, sg_team1_color)
        window.blit(UI_player1_hp, UI_player1_hp_pos)

        # Player's ammo
        pygame.draw.line(window, sg_team1_color, (150, resolution[1] - 45), (150, resolution[1]), 2)
        pygame.draw.line(window, sg_team1_color, (resolution[0] - 150, resolution[1] - 45),
                         (resolution[0] - 150, resolution[1]), 2)
        UI_player1_ammo = font_UI.render(str(player1.ammo) + "/" + str(player1.maxAmmo), 1, sg_team1_color)
        window.blit(UI_player1_ammo, UI_player1_ammo_pos)

        # Enemy's health
        pygame.draw.line(window, sg_team2_color, (0, 45), (150, 45), 2)
        pygame.draw.line(window, sg_team2_color, (150, 45), (150, 0), 2)
        UI_player2_hp = font_UI.render(str(player2.hp) + " HP", 1, sg_team2_color)
        window.blit(UI_player2_hp, UI_player2_hp_pos)

        # Rounds score
        UI_rounds_score = font_UI.render(str(player1_rounds_counter) + " : " + str(player2_rounds_counter), 1, WHITE)
        window.blit(UI_rounds_score, UI_rounds_score_pos)

        if player2.hp <= 0:
            break
        if player1.hp <= 0 or (player1.ammo == 0 and len(player1.missiles) == 0):
            break

        pygame.display.update()
        clock.tick(FPS)

def multiplayer():
    global cheat_player1_autofire_delay, cheat_player2_autofire_delay
    while True:
        window.fill(BLACK)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                full_exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not cheat_player1_autofire:
                    if player1.ammo > 0:
                        player1.shoot()
                        if not(cheat_player1_unlimitedAmmo):
                            player1.ammo -= 1
                if event.key == pygame.K_KP0 and not(cheat_player2_autofire):
                    if player2.ammo > 0:
                        player2.shoot()
                        if not(cheat_player2_unlimitedAmmo):
                            player2.ammo -= 1
    

        # Moving player by pressing buttons
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and not (player1.bodyPos[0] <= 5):
            player1.bodyPos[0] -= player1.speed
            player1.headPos[0] -= player1.speed
        if keys[pygame.K_d] and not (player1.bodyPos[0] >= resolution[0] - player1.bodyWidth - 5):
            player1.bodyPos[0] += player1.speed
            player1.headPos[0] += player1.speed

        if keys[pygame.K_LEFT] and not (player2.bodyPos[0] <= 5):
            player2.bodyPos[0] -= player2.speed
            player2.headPos[0] -= player2.speed
        if keys[pygame.K_RIGHT] and not (player2.bodyPos[0] >= resolution[0] - player2.bodyWidth - 5):
            player2.bodyPos[0] += player2.speed
            player2.headPos[0] += player2.speed


        # Autofire cheat
        if cheat_player1_autofire_delay < cheat_player1_autofire_maxDelay:
            cheat_player1_autofire_delay += 1
        if (player1.ammo > 0 and cheat_player1_autofire and keys[pygame.K_SPACE] and
           cheat_player1_autofire_delay == cheat_player1_autofire_maxDelay):
            player1.shoot()
            if not(cheat_player1_unlimitedAmmo):
                player1.ammo -= 1
            cheat_player1_autofire_delay = 0

        if cheat_player2_autofire_delay < cheat_player2_autofire_maxDelay:
            cheat_player2_autofire_delay += 1
        if (player2.ammo > 0 and cheat_player2_autofire and keys[pygame.K_KP0] and
           cheat_player2_autofire_delay == cheat_player2_autofire_maxDelay):
            player2.shoot()
            if not(cheat_player2_unlimitedAmmo):
                player2.ammo -= 1
            cheat_player2_autofire_delay = 0
        

        # Draw player
        pygame.draw.rect(window, mp_team1_color, player1.bodyPos)
        pygame.draw.rect(window, mp_team1_color, player1.headPos)

        # Draw enemy
        pygame.draw.rect(window, mp_team2_color, player2.bodyPos)
        pygame.draw.rect(window, mp_team2_color, player2.headPos)

        
        # Collision detection for player's bullets
        for missile in player1.missiles:
            if (collide(missile, player2.headPos) or
                collide(missile, player2.bodyPos)):
                if not(cheat_player2_godmode):
                    if player2.hp > 0:
                        player2.hp -= player1.bulletDamage
                    else:
                        player2.hp = 0

                del player1.missiles[player1.missiles.index(missile)]

        player1.move_bullets()
        

        # Collision detection for enemy's bullets
        for missile in player2.missiles:
            if (collide(missile, player1.headPos) or
                collide(missile, player1.bodyPos)):
                if not(cheat_player1_godmode):
                    if player1.hp > 0:
                            player1.hp -= player2.bulletDamage
                    else:
                        player1.hp = 0

                del player2.missiles[player2.missiles.index(missile)]

        player2.move_bullets()
        

        # Draw UI
        # Player's health
        #pygame.draw.line(window, mp_team1_color, (0, resolution[1] - 45), (150, resolution[1] - 45), 2)
        #pygame.draw.line(window, mp_team1_color, (resolution[0] - 150, resolution[1] - 45),
        #                 (resolution[0], resolution[1] - 45), 2)
        UI_player1_hp = font_UI.render(str(player1.hp) + " HP", 1, mp_team1_color)
        window.blit(UI_player1_hp, UI_player1_hp_pos)

        # Player's ammo
        #pygame.draw.line(window, mp_team1_color, (150, resolution[1] - 45), (150, resolution[1]), 2)
        #pygame.draw.line(window, mp_team1_color, (resolution[0] - 150, resolution[1] - 45), (resolution[0] - 150, resolution[1]), 2)
        UI_player1_ammo = font_UI.render(str(player1.ammo) + "/" + str(player1.maxAmmo), 1, mp_team1_color)
        window.blit(UI_player1_ammo, UI_player1_ammo_pos)
        
        # Enemy's health
        #pygame.draw.line(window, mp_team2_color, (0, 45), (150, 45), 2)
        #pygame.draw.line(window, mp_team2_color, (150, 45), (150, 0), 2)
        UI_player2_hp = font_UI.render(str(player2.hp) + " HP", 1, mp_team2_color)
        window.blit(UI_player2_hp, UI_player2_hp_pos)

        # Enemy's ammo
        #pygame.draw.line(window, mp_team2_color, (resolution[0], 45), (resolution[0] - 150, 45), 2)
        #pygame.draw.line(window, mp_team2_color, (resolution[0] - 150, 45), (resolution[0] - 150, 0), 2)
        UI_player2_ammo = font_UI.render(str(player2.ammo) + "/" + str(player2.maxAmmo), 1, mp_team2_color)
        window.blit(UI_player2_ammo, UI_player2_ammo_pos)

        # Rounds score
        UI_rounds_score = font_UI.render(str(player1_rounds_counter) + " : " + str(player2_rounds_counter), 1, WHITE)
        window.blit(UI_rounds_score, UI_rounds_score_pos)


        if player2.hp <= 0 or (player2.ammo == 0 and len(player2.missiles) == 0):
            break
        if player1.hp <= 0 or (player1.ammo == 0 and len(player1.missiles) == 0):
            break


        pygame.display.update()
        clock.tick(FPS)


def draw_endscreen():
    while True:
        window.fill(BLACK)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                full_exit()

        window.blit(UI_message_rounds, (resolution[0] // 2 - UI_message_rounds.get_width() // 2,
                                        resolution[1] // 2 - UI_message_rounds.get_height() - 60))
        window.blit(UI_message_gameOutcome, (resolution[0] // 2 - UI_message_gameOutcome.get_width() // 2,
                                             resolution[1] // 2 - 45))

        m_pos = pygame.mouse.get_pos() + (1, 1)
        m_pressedButtons = pygame.mouse.get_pressed()

        if collide(m_pos, btn_endscreen_backToMainMenu.pos):
            if m_pressedButtons[0]:
                change_UI_state(UI_STATE_MAINMENU)
                break
            btn_endscreen_backToMainMenu.draw(window, menu_color, BLACK)
        else:
            btn_endscreen_backToMainMenu.draw_outline(window, menu_color, menu_color, 4)

        pygame.display.update()
        clock.tick(FPS_GAMEMENU)


while True:
    player1_rounds_counter, player2_rounds_counter = 0, 0

    shuffle(colors_shuffled)
    UI_gameMenu_title_ship1_color, UI_gameMenu_title_ship2_color = WHITE, WHITE
    UI_gameMenu_title_ship1_color = colors_shuffled[randint(0, len(colors) - 1)]
    UI_gameMenu_title_ship2_color = colors_shuffled[randint(0, len(colors) - 1)]

    # Draw Game Menu
    if UI_currentState == UI_STATE_MAINMENU:
        while True:
            window.fill(BLACK)

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    full_exit()

            m_pos = pygame.mouse.get_pos() + (1, 1)
            m_pressedButtons = pygame.mouse.get_pressed()

            pygame.draw.rect(window, UI_gameMenu_title_ship1_color,
                             (resolution[0] // 2 - font_gameOutcome.size("2SHIPS")[0] // 2 - 100,
                              btn_mainMenu_singleplayer.pos[1] - 165,
                              24, 96))
            pygame.draw.rect(window, UI_gameMenu_title_ship1_color,
                             (resolution[0] // 2 - font_gameOutcome.size("2SHIPS")[0] // 2 - 100 + 24,
                              btn_mainMenu_singleplayer.pos[1] - 165 + 32,
                              24, 32))

            UI_gameMenu_title = font_gameOutcome.render("2SHIPS", 1, menu_color)
            window.blit(UI_gameMenu_title, ((resolution[0] - font_gameOutcome.size("2SHIPS")[0]) // 2,
                                            btn_mainMenu_singleplayer.pos[1] - 190))

            pygame.draw.rect(window, UI_gameMenu_title_ship2_color,
                             (resolution[0] // 2 + font_gameOutcome.size("2SHIPS")[0] // 2 + 100 - 24,
                              btn_mainMenu_singleplayer.pos[1] - 165,
                              24, 96))
            pygame.draw.rect(window, UI_gameMenu_title_ship2_color,
                             (resolution[0] // 2 + font_gameOutcome.size("2SHIPS")[0] // 2 + 100 - 48,
                              btn_mainMenu_singleplayer.pos[1] - 165 + 32,
                              24, 32))

            if collide(m_pos, btn_mainMenu_singleplayer.pos):
                if m_pressedButtons[0]:
                    change_UI_state(UI_STATE_SG_ROUNDSCHOICE)
                    break
                btn_mainMenu_singleplayer.draw(window, menu_color, BLACK)
            else:
                btn_mainMenu_singleplayer.draw_outline(window, menu_color, menu_color, 4)

            if collide(m_pos, btn_mainMenu_multiplayer.pos):
                if m_pressedButtons[0]:
                    change_UI_state(UI_STATE_MP_ROUNDSCHOICE)
                    break
                btn_mainMenu_multiplayer.draw(window, menu_color, BLACK)
            else:
                btn_mainMenu_multiplayer.draw_outline(window, menu_color, menu_color, 4)

            if collide(m_pos, btn_mainMenu_exit.pos):
                if m_pressedButtons[0]:
                    full_exit()
                btn_mainMenu_exit.draw(window, menu_color, BLACK)
            else:
                btn_mainMenu_exit.draw_outline(window, menu_color, menu_color, 4)

            pygame.display.update()
            clock.tick(FPS_GAMEMENU)
            
    elif UI_currentState == UI_STATE_SG_ROUNDSCHOICE:
        sg_rounds = draw_roundsChoiceScreen(sg_rounds, UI_STATE_SG_INGAME)

    elif UI_currentState == UI_STATE_MP_ROUNDSCHOICE:
        mp_rounds = draw_roundsChoiceScreen(mp_rounds, UI_STATE_MP_INGAME)

    elif UI_currentState == UI_STATE_SG_INGAME:
        config.read("config/sg_players.ini")

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
        player2_headPos = pygame.Rect(player2_bodyPos[0] + player2_bodyWidth // 2 - player2_headWidth // 2,
                                      60 + player2_bodyHeight,
                                      player2_headWidth, player2_headHeight)
        # Enemy's characteristics
        player2_hp = int(config.get("Player and Bots", "player2_hp"))
        player2_maxHP = player2_hp
        player2_speed = int(config.get("Player and Bots", "player2_speed"))
        player2_bulletDamage = int(config.get("Player and Bots", "player2_bulletDamage"))
        # Enemy's Bullet
        player2_bulletWidth = int(config.get("Player and Bots", "player2_bulletWidth"))
        player2_bulletHeight = int(config.get("Player and Bots", "player2_bulletHeight"))
        player2_bulletPos = (0, 0, 1, 1)
        player2_bulletColor = eval(config.get("Player and Bots", "player2_bulletColor"))
        player2_bulletSpeed = int(config.get("Player and Bots", "player2_bulletSpeed"))
        player2_bulletMissiles = []

        # Cheats
        cheat_player1_unlimitedAmmo = int(config.get("Cheats Singleplayer", "cheat_player1_unlimitedAmmo"))

        cheat_player1_godmode = int(config.get("Cheats Singleplayer", "cheat_player1_godmode"))

        cheat_player1_autofire = int(config.get("Cheats Singleplayer", "cheat_player1_autofire"))
        cheat_player1_autofire_delay = int(config.get("Cheats Singleplayer", "cheat_player1_autofire_delay"))
        cheat_player1_autofire_maxDelay = int(cheat_player1_autofire_delay // (1000 / FPS))
        cheat_player1_autofire_delay = cheat_player1_autofire_maxDelay

        player2_shootDelay = int(config.get("Player and Bots", "player2_shootDelay"))
        player2_shootMaxDelay = int(player2_shootDelay // (1000 / FPS))
        player2_shootDelay = player2_shootMaxDelay

        player2_switchDirectionDelay = int(config.get("Player and Bots", "player2_switchDirectionDelay"))
        player2_switchDirectionMaxDelay = int(player2_switchDirectionDelay // (1000 / FPS))
        player2_switchDirectionDelay = player2_switchDirectionMaxDelay

        player1 = Player(player1_hp, player1_maxHP, player1_speed, player1_ammo, player1_maxAmmo,
                         player1_bodyPos, player1_headPos, player1_bodyWidth, player1_bodyHeight, player1_headWidth,
                         player1_headHeight,
                         player1_bulletDamage, player1_bulletWidth, player1_bulletHeight, player1_bulletPos,
                         player1_bulletSpeed, player1_bulletColor, player1_bulletMissiles)
        player2 = Enemy(player2_hp, player2_maxHP, player2_speed, 999, 999,
                        player2_bodyPos, player2_headPos, player2_bodyWidth, player2_bodyHeight, player2_headWidth,
                        player2_headHeight,
                        player2_bulletDamage, player2_bulletWidth, player2_bulletHeight, player2_bulletPos,
                        player2_bulletSpeed, player2_bulletColor, player2_bulletMissiles)

        for roundsCounter in range(1, sg_rounds + 1):
            player1.hp, player2.hp = player1.maxHP, player2.maxHP
            player1.ammo, player2.ammo = player1.maxAmmo, player2.maxAmmo

            player1.missiles, player2.missiles = [], []

            player1.bodyPos[0] = randint(7, resolution[0] - player1_bodyWidth - 7)
            player1.headPos[0] = player1.bodyPos[0] + player1_bodyWidth // 2 - player1_headWidth // 2

            player2.bodyPos[0] = randint(7, resolution[0] - player2_bodyWidth - 7)
            player2.headPos[0] = player2.bodyPos[0] + player2_bodyWidth // 2 - player2_headWidth // 2

            player2_shootDelay, player2_switchDirectionDelay = 0, 0

            if int(str(roundsCounter)[-1]) == 1 and roundsCounter != 11:
                UI_message_nextRound = font_roundOutcome.render(str(roundsCounter) + "ST " + "ROUND", 1, WHITE)
            elif int(str(roundsCounter)[-1]) == 2 and roundsCounter != 12:
                UI_message_nextRound = font_roundOutcome.render(str(roundsCounter) + "ND " + "ROUND", 1, WHITE)
            elif int(str(roundsCounter)[-1]) == 3 and roundsCounter != 13:
                UI_message_nextRound = font_roundOutcome.render(str(roundsCounter) + "RD " + "ROUND", 1, WHITE)
            else:
                UI_message_nextRound = font_roundOutcome.render(str(roundsCounter) + "TH " + "ROUND", 1, WHITE)

            for frame in range(1, 91):
                window.fill(BLACK)

                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        full_exit()

                window.blit(UI_message_nextRound, (resolution[0] // 2 - UI_message_nextRound.get_width() // 2,
                                                   resolution[1] // 2 - UI_message_nextRound.get_height() // 2))

                pygame.display.update()
                clock.tick(FPS_GAMEMENU)

            singleplayer()

            if player2.hp <= 0 or (player2.ammo == 0 and len(player2.missiles) == 0):
                UI_message_roundOutcome = font_roundOutcome.render("PLAYER WON!", 1, sg_team1_color)
                player1_rounds_counter += 1
            elif player1.hp <= 0 or (player1.ammo == 0 and len(player1.missiles) == 0):
                UI_message_roundOutcome = font_roundOutcome.render("ENEMY WON!", 1, sg_team2_color)
                player2_rounds_counter += 1

            for frame in range(1, 211):
                window.fill(BLACK)

                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        full_exit()

                if frame < 91:
                    window.blit(UI_message_roundOutcome, (resolution[0] // 2 - UI_message_roundOutcome.get_width() // 2,
                                                          resolution[1] // 2 - UI_message_roundOutcome.get_height() // 2))
                elif frame >= 91 and roundsCounter < sg_rounds:
                    UI_rounds_score = font_gameOutcome.render(str(player1_rounds_counter) + " : " + str(player2_rounds_counter), 1, WHITE)
                    window.blit(UI_rounds_score, (resolution[0] // 2 - UI_rounds_score.get_width() // 2,
                                                  resolution[1] // 2 - UI_rounds_score.get_height() // 2))
                else:
                    break

                pygame.display.update()
                clock.tick(FPS_GAMEMENU)

        # Game outcome
        UI_message_rounds = font_gameOutcome.render(str(player1_rounds_counter) + " : " + str(player2_rounds_counter), 1, WHITE)

        if player1_rounds_counter > player2_rounds_counter:
            UI_message_gameOutcome = font_gameOutcome.render("PLAYER WON!", 1, sg_team1_color)
        elif player1_rounds_counter < player2_rounds_counter:
            UI_message_gameOutcome = font_gameOutcome.render("ENEMY WON!", 1, sg_team2_color)
        elif player1_rounds_counter == player2_rounds_counter:
            UI_message_gameOutcome = font_gameOutcome.render("DRAW!", 1, YELLOW)

        draw_endscreen()

    elif UI_currentState == UI_STATE_MP_INGAME:
        config.read("config/mp_players.ini")

        # Team colors
        mp_team1_color = eval(config.get("Players", "mp_team1_color"))
        mp_team2_color = eval(config.get("Players", "mp_team2_color"))

        # Player's body
        player1_bodyWidth = int(config.get("Players", "player1_bodyWidth"))
        player1_bodyHeight = int(config.get("Players", "player1_bodyHeight"))
        player1_headWidth = int(config.get("Players", "player1_headWidth"))
        player1_headHeight = int(config.get("Players", "player1_headHeight"))
        player1_bodyPos = pygame.Rect(randint(7, resolution[0] - player1_bodyWidth - 7),
                                      resolution[1] - 60 - player1_bodyHeight,
                                      player1_bodyWidth,
                                      player1_bodyHeight)
        player1_headPos = pygame.Rect(player1_bodyPos[0] + player1_bodyWidth // 2 - player1_headWidth // 2,
                                      player1_bodyPos[1] - player1_headHeight,
                                      player1_headWidth,
                                      player1_bodyHeight)
        # Player's characteristics
        player1_hp = int(config.get("Players", "player1_hp"))
        player1_maxHP = player1_hp
        player1_speed = int(config.get("Players", "player1_speed"))
        player1_ammo = int(config.get("Players", "player1_ammo"))
        player1_maxAmmo = player1_ammo
        player1_bulletDamage = int(config.get("Players", "player1_bulletDamage"))
        player1_bulletSpeed = int(config.get("Players", "player1_bulletSpeed"))
        # Player's Bullet
        player1_bulletWidth = int(config.get("Players", "player1_bulletWidth"))
        player1_bulletHeight = int(config.get("Players", "player1_bulletHeight"))
        player1_bulletPos = (0, 0, 1, 1)
        player1_bulletColor = eval(config.get("Players", "player1_bulletColor"))
        player1_bulletMissiles = []

        # Enemy's body
        player2_bodyWidth = int(config.get("Players", "player2_bodyWidth"))
        player2_bodyHeight = int(config.get("Players", "player2_bodyHeight"))
        player2_headWidth = int(config.get("Players", "player2_headWidth"))
        player2_headHeight = int(config.get("Players", "player2_headHeight"))
        player2_bodyPos = pygame.Rect(randint(7, resolution[0] - player2_bodyWidth - 7), 60,
                                      player2_bodyWidth, player2_bodyHeight)
        player2_headPos = pygame.Rect(player2_bodyPos[0] + player2_bodyWidth // 2 - player2_headWidth // 2,
                                      60 + player2_bodyHeight,
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
        cheat_player1_unlimitedAmmo = int(config.get("Cheats Multiplayer", "cheat_player1_unlimitedAmmo"))
        cheat_player2_unlimitedAmmo = int(config.get("Cheats Multiplayer", "cheat_player2_unlimitedAmmo"))

        cheat_player1_godmode = int(config.get("Cheats Multiplayer", "cheat_player1_godmode"))
        cheat_player2_godmode = int(config.get("Cheats Multiplayer", "cheat_player2_godmode"))

        cheat_player1_autofire = int(config.get("Cheats Multiplayer", "cheat_player1_autofire"))
        cheat_player1_autofire_delay = int(config.get("Cheats Multiplayer", "cheat_player1_autofire_delay"))
        cheat_player1_autofire_maxDelay = int(cheat_player1_autofire_delay // (1000 / FPS))
        cheat_player1_autofire_delay = cheat_player1_autofire_maxDelay

        cheat_player2_autofire = int(config.get("Cheats Multiplayer", "cheat_player2_autofire"))
        cheat_player2_autofire_delay = int(config.get("Cheats Multiplayer", "cheat_player2_autofire_delay"))
        cheat_player2_autofire_maxDelay = int(cheat_player2_autofire_delay // (1000 / FPS))
        cheat_player2_autofire_delay = cheat_player2_autofire_maxDelay

        player1 = Player(player1_hp, player1_maxHP, player1_speed, player1_ammo, player1_maxAmmo,
                         player1_bodyPos, player1_headPos, player1_bodyWidth, player1_bodyHeight, player1_headWidth,
                         player1_headHeight,
                         player1_bulletDamage, player1_bulletWidth, player1_bulletHeight, player1_bulletPos,
                         player1_bulletSpeed, player1_bulletColor, player1_bulletMissiles)
        player2 = Enemy(player2_hp, player2_maxHP, player2_speed, player2_ammo, player2_maxAmmo,
                        player2_bodyPos, player2_headPos, player2_bodyWidth, player2_bodyHeight, player2_headWidth,
                        player2_headHeight,
                        player2_bulletDamage, player2_bulletWidth, player2_bulletHeight, player2_bulletPos,
                        player2_bulletSpeed, player2_bulletColor, player2_bulletMissiles)

        for roundsCounter in range(1, mp_rounds + 1):
            player1.hp, player2.hp = player1.maxHP, player2.maxHP
            player1.ammo, player2.ammo = player1.maxAmmo, player2.maxAmmo

            player1.missiles, player2.missiles = [], []

            player1.bodyPos[0] = randint(7, resolution[0] - player1_bodyWidth - 7)
            player1.headPos[0] = player1.bodyPos[0] + player1_bodyWidth // 2 - player1_headWidth // 2

            player2.bodyPos[0] = randint(7, resolution[0] - player2_bodyWidth - 7)
            player2.headPos[0] = player2.bodyPos[0] + player2_bodyWidth // 2 - player2_headWidth // 2

            if int(str(roundsCounter)[-1]) == 1 and roundsCounter != 11:
                UI_message_nextRound = font_roundOutcome.render(str(roundsCounter) + "ST " + "ROUND", 1, WHITE)
            elif int(str(roundsCounter)[-1]) == 2 and roundsCounter != 12:
                UI_message_nextRound = font_roundOutcome.render(str(roundsCounter) + "ND " + "ROUND", 1, WHITE)
            elif int(str(roundsCounter)[-1]) == 3 and roundsCounter != 13:
                UI_message_nextRound = font_roundOutcome.render(str(roundsCounter) + "RD " + "ROUND", 1, WHITE)
            else:
                UI_message_nextRound = font_roundOutcome.render(str(roundsCounter) + "TH " + "ROUND", 1, WHITE)

            for frame in range(1, 91):
                window.fill(BLACK)

                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        full_exit()

                window.blit(UI_message_nextRound, (resolution[0] // 2 - UI_message_nextRound.get_width() // 2,
                                                   resolution[1] // 2 - UI_message_nextRound.get_height() // 2))

                pygame.display.update()
                clock.tick(FPS_GAMEMENU)

            multiplayer()

            if player2.hp <= 0 or (player2.ammo == 0 and len(player2.missiles) == 0):
                UI_message_roundOutcome = font_roundOutcome.render("PLAYER1 WON!", 1, mp_team1_color)
                player1_rounds_counter += 1
            elif player1.hp <= 0 or (player1.ammo == 0 and len(player1.missiles) == 0):
                UI_message_roundOutcome = font_roundOutcome.render("PLAYER2 WON!", 1, mp_team2_color)
                player2_rounds_counter += 1

            for frame in range(1, 211):
                window.fill(BLACK)

                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        full_exit()

                if frame < 91:
                    window.blit(UI_message_roundOutcome, (resolution[0] // 2 - UI_message_roundOutcome.get_width() // 2,
                                                          resolution[1] // 2 - UI_message_roundOutcome.get_height() // 2))
                elif frame >= 91 and roundsCounter < mp_rounds:
                    UI_rounds_score = font_gameOutcome.render(str(player1_rounds_counter) + " : " + str(player2_rounds_counter), 1, WHITE)
                    window.blit(UI_rounds_score, (resolution[0] // 2 - UI_rounds_score.get_width() // 2,
                                                  resolution[1] // 2 - UI_rounds_score.get_height() // 2))
                else:
                    break

                pygame.display.update()
                clock.tick(FPS_GAMEMENU)


        # Game outcome
        UI_message_rounds = font_gameOutcome.render(str(player1_rounds_counter) + " : " + str(player2_rounds_counter), 1, WHITE)

        if player1_rounds_counter > player2_rounds_counter:
            UI_message_gameOutcome = font_gameOutcome.render("PLAYER1 WON!", 1, mp_team1_color)
        elif player1_rounds_counter < player2_rounds_counter:
            UI_message_gameOutcome = font_gameOutcome.render("PLAYER2 WON!", 1, mp_team2_color)
        elif player1_rounds_counter == player2_rounds_counter:
            UI_message_gameOutcome = font_gameOutcome.render("DRAW!", 1, YELLOW)

        draw_endscreen()

    else:
        full_exit()
