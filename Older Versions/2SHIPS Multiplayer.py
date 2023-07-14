import pygame
from random import randint
from sys import exit as sys_exit
from os.path import abspath

#rounds = int(input("Number of rounds: "))
rounds = 3


pygame.init()

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

team1_color = GREEN
team2_color = RED


# Player's body
player_bodyWidth = 100
player_bodyHeight = 25
player_headWidth = 34
player_headHeight = 25
player_bodyPos = pygame.Rect(randint(7, resolution[0] - player_bodyWidth - 7), resolution[1] - 60 - player_bodyHeight,
                             player_bodyWidth, player_bodyHeight)
player_headPos = pygame.Rect(player_bodyPos[0] + player_bodyWidth // 2 - player_headWidth // 2,
                             player_bodyPos[1] - player_headHeight,
                             player_headWidth,
                             player_bodyHeight)
# Player's characteristics
player_hp = 100
player_maxHP = player_hp
player_speed = 4
player_ammo = 50
player_maxAmmo = player_ammo
player_bulletDamage = 15
player_bulletSpeed = 10
# Player's Bullet
player_bulletWidth = 10
player_bulletHeight = 20
player_bulletPos = (0, 0, 1, 1)
player_bulletColor = WHITE
player_bulletMissiles = []


# Enemy's body
enemy_bodyWidth = 100
enemy_bodyHeight = 25
enemy_headWidth = 34
enemy_headHeight = 25
enemy_bodyPos = pygame.Rect(randint(7, resolution[0] - enemy_bodyWidth - 7), 60,
                            enemy_bodyWidth, enemy_bodyHeight)
enemy_headPos = pygame.Rect(enemy_bodyPos[0] + enemy_bodyWidth // 2 - enemy_headWidth // 2, 60 + enemy_bodyHeight,
                            enemy_headWidth, enemy_headHeight)
# Enemy's characteristics
enemy_hp = 100
enemy_maxHP = enemy_hp
enemy_speed = 4
enemy_ammo = 50
enemy_maxAmmo = enemy_ammo
enemy_bulletDamage = 15
# Enemy's Bullet
enemy_bulletWidth = 10
enemy_bulletHeight = 20
enemy_bulletPos = (0, 0, 1, 1)
enemy_bulletColor = WHITE
enemy_bulletSpeed = 10
enemy_bulletMissiles = []

enemy_shootDelay = 250
enemy_shootMaxDelay = int(enemy_shootDelay // (1000 / FPS))
enemy_shootDelay = enemy_shootMaxDelay


# Cheats
cheat_player_unlimitedammo = 0
cheat_enemy_unlimitedammo = 0

cheat_player_godmode = 0
cheat_enemy_godmode = 0

cheat_player_autofire = 0
cheat_player_autofire_delay = 200
cheat_player_autofire_maxDelay = int(cheat_player_autofire_delay // (1000 / FPS))
cheat_player_autofire_delay = cheat_player_autofire_maxDelay

cheat_enemy_autofire = 0
cheat_enemy_autofire_delay = 200
cheat_enemy_autofire_maxDelay = int(cheat_enemy_autofire_delay // (1000 / FPS))
cheat_enemy_autofire_delay = cheat_enemy_autofire_maxDelay


def does_collide(missile, object2):
    hitboxes1 = set()
    hitboxes1.add((missile[0], missile[1]))
    hitboxes1.add((missile[0], missile[1] + missile[3]))
    hitboxes1.add((missile[0] + missile[2], missile[1]))
    hitboxes1.add((missile[0] + missile[2], missile[1] + missile[3]))

    hitboxes2 = set()
    for x in range(0, object2[2]):
        for y in range(0, object2[3]):
            hitboxes2.add((object2[0] + x, object2[1] + y))
                
    for hit in hitboxes1:
        if hit in hitboxes2:
            return True
    return False


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
enemyStormtrooper = Enemy(enemy_hp, enemy_maxHP, enemy_speed, enemy_ammo, enemy_maxAmmo,
                          enemy_bodyPos, enemy_headPos, enemy_bodyWidth, enemy_bodyHeight, enemy_headWidth, enemy_headHeight,
                          enemy_bulletDamage, enemy_bulletWidth, enemy_bulletHeight, enemy_bulletPos,
                          enemy_bulletSpeed, enemy_bulletColor, enemy_bulletMissiles)


path_gameFolder = abspath(__file__).replace("\\", "/")
path_font_UI = path_gameFolder.replace("2SHIPS Multiplayer.py", "files/fonts/BigNoodleTooOblique.ttf")

font_UI = pygame.font.Font(path_font_UI, 45)
UI_enemy_hp_pos = (0 + 25, 0)
UI_enemy_ammo_pos = (resolution[0] - 115, 0)
UI_player_hp_pos = (0 + 25, resolution[1] - 45)
UI_player_ammo_pos = (resolution[0] - 115, resolution[1] - 45)
UI_rounds_score_pos = (resolution[0] // 2 - resolution[0] // 25, 0)

player_rounds_counter, enemy_rounds_counter = 0, 0


def main():
    global cheat_player_autofire_delay, cheat_enemy_autofire_delay
    while True:
        window.fill(BLACK)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys_exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not(cheat_player_autofire):
                    if player.ammo > 0:
                        player.shoot()
                        if not(cheat_player_unlimitedammo):
                            player.ammo -= 1
                if event.key == pygame.K_KP0 and not(cheat_enemy_autofire):
                    if enemyStormtrooper.ammo > 0:
                        enemyStormtrooper.shoot()
                        if not(cheat_enemy_unlimitedammo):
                            enemyStormtrooper.ammo -= 1
    

        # Moving player by pressing buttons
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and not (player.bodyPos[0] <= 5):
            player.bodyPos[0] -= player.speed
            player.headPos[0] -= player.speed
        if keys[pygame.K_d] and not (player.bodyPos[0] >= resolution[0] - player.bodyWidth - 5):
            player.bodyPos[0] += player.speed
            player.headPos[0] += player.speed

        if keys[pygame.K_LEFT] and not (enemyStormtrooper.bodyPos[0] <= 5):
            enemyStormtrooper.bodyPos[0] -= enemyStormtrooper.speed
            enemyStormtrooper.headPos[0] -= enemyStormtrooper.speed
        if keys[pygame.K_RIGHT] and not (enemyStormtrooper.bodyPos[0] >= resolution[0] - enemyStormtrooper.bodyWidth - 5):
            enemyStormtrooper.bodyPos[0] += enemyStormtrooper.speed
            enemyStormtrooper.headPos[0] += enemyStormtrooper.speed
        
        
        if cheat_player_autofire_delay < cheat_player_autofire_maxDelay:
            cheat_player_autofire_delay += 1
        if (player.ammo > 0 and cheat_player_autofire and keys[pygame.K_SPACE] and
           cheat_player_autofire_delay == cheat_player_autofire_maxDelay):
            player.shoot()
            if not(cheat_player_unlimitedammo):
                player.ammo -= 1
            cheat_player_autofire_delay = 0

        if cheat_enemy_autofire_delay < cheat_enemy_autofire_maxDelay:
            cheat_enemy_autofire_delay += 1
        if (enemyStormtrooper.ammo > 0 and cheat_enemy_autofire and keys[pygame.K_KP0] and
           cheat_enemy_autofire_delay == cheat_enemy_autofire_maxDelay):
            enemyStormtrooper.shoot()
            if not(cheat_enemy_unlimitedammo):
                enemyStormtrooper.ammo -= 1
            cheat_enemy_autofire_delay = 0
        

        # Draw player
        pygame.draw.rect(window, team1_color, player.bodyPos)
        pygame.draw.rect(window, team1_color, player.headPos)

        # Draw enemy
        pygame.draw.rect(window, team2_color, enemyStormtrooper.bodyPos)
        pygame.draw.rect(window, team2_color, enemyStormtrooper.headPos)

        
        # Collision detection for player's bullets
        for missile in player.missiles:
            if not(missile[1] > 60 + enemyStormtrooper.bodyHeight + enemyStormtrooper.headHeight or
                   missile[1] < 60 - player.bulletHeight):
                if (does_collide(missile, enemyStormtrooper.headPos) or
                   does_collide(missile, enemyStormtrooper.bodyPos)):
                    if not(cheat_enemy_godmode):
                        if enemyStormtrooper.hp > 0:
                            enemyStormtrooper.hp -= player.bulletDamage
                        else:
                            enemyStormtrooper.hp = 0

                    del player.missiles[player.missiles.index(missile)]

        player.move_bullets()
        

        # Collision detection for enemy's bullets
        for missile in enemyStormtrooper.missiles:
            if not(missile[1] > 60 + enemyStormtrooper.bodyHeight + enemyStormtrooper.headHeight and
                   missile[1] < resolution[1] - 60 - player.bodyHeight - player.headHeight):
                if (does_collide(missile, player.headPos) or
                   does_collide(missile, player.bodyPos)):
                    if not(cheat_player_godmode):
                        if player.hp > 0:
                                player.hp -= enemyStormtrooper.bulletDamage
                        else:
                            player.hp = 0

                    del enemyStormtrooper.missiles[enemyStormtrooper.missiles.index(missile)]

        enemyStormtrooper.move_bullets()
        

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
        UI_enemy_hp = font_UI.render(str(enemyStormtrooper.hp) + " HP", 1, team2_color)
        window.blit(UI_enemy_hp, UI_enemy_hp_pos)

        # Enemy's ammo
        pygame.draw.line(window, team2_color, (resolution[0], 45), (resolution[0] - 150, 45), 2)
        pygame.draw.line(window, team2_color, (resolution[0] - 150, 45), (resolution[0] - 150, 0), 2)
        UI_enemy_ammo = font_UI.render(str(enemyStormtrooper.ammo) + "/" + str(enemyStormtrooper.maxAmmo), 1, team2_color)
        window.blit(UI_enemy_ammo, UI_enemy_ammo_pos)

        # Rounds score
        UI_rounds_score = font_UI.render(str(player_rounds_counter) + " : " + str(enemy_rounds_counter), 1, WHITE)
        window.blit(UI_rounds_score, UI_rounds_score_pos)



        if enemyStormtrooper.hp <= 0 or (enemyStormtrooper.ammo == 0 and len(enemyStormtrooper.missiles) == 0):
            break
        if player.hp <= 0 or (player.ammo == 0 and len(player.missiles) == 0):
            break


        pygame.display.update()
        clock.tick(FPS)

for i in range(rounds):
    player.hp = player.maxHP
    enemyStormtrooper.hp = enemyStormtrooper.maxHP
    
    player.ammo = player.maxAmmo
    enemyStormtrooper.ammo = enemyStormtrooper.maxAmmo
    
    player.missiles, enemyStormtrooper.missiles = [], []
    
    player.bodyPos[0] = randint(7, resolution[0] - player_bodyWidth - 7)
    player.headPos[0] = player.bodyPos[0] + player_bodyWidth // 2 - player_headWidth // 2
    
    enemyStormtrooper.bodyPos[0] = randint(7, resolution[0] - enemy_bodyWidth - 7)
    enemyStormtrooper.headPos[0] = enemyStormtrooper.bodyPos[0] + enemy_bodyWidth // 2 - enemy_headWidth // 2
    
    main()

    font_roundOutcome = pygame.font.Font(path_font_UI, 135)
    if enemyStormtrooper.hp <= 0 or (enemyStormtrooper.ammo == 0 and len(enemyStormtrooper.missiles) == 0):
        UI_message_roundOutcome = font_roundOutcome.render("PLAYER1 WON!", 1, team1_color)
        player_rounds_counter += 1
    elif player.hp <= 0 or (player.ammo == 0 and len(player.missiles) == 0):
        UI_message_roundOutcome = font_roundOutcome.render("PLAYER2 WON!", 1, team2_color)
        enemy_rounds_counter += 1
        
    for i in range(120):
        window.fill(BLACK)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys_exit()

        
        window.blit(UI_message_roundOutcome, (0, 0))

        pygame.display.update()
        
        clock.tick(FPS_GAMEMENU)


font_gameOutcome = pygame.font.Font(path_font_UI, 135)
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
            pygame.quit()
            sys_exit()

    window.blit(UI_message_rounds, (0, 0))
    window.blit(UI_message_gameOutcome, (0, 140))

    pygame.display.update()
    clock.tick(FPS_GAMEMENU)
