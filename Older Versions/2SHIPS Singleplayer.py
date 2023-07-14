import pygame
from random import randint
from sys import exit as sys_exit
from os.path import abspath

pygame.init()

# Recommended resolution: 800 x 640
resolution = (800, 640)
windowName = '2SHIPS'
window = pygame.display.set_mode(resolution)
pygame.display.set_caption(windowName)

FPS = 120
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


# Player's body
player_bodyWidth = 100
player_bodyHeight = 25
player_headWidth = 34
player_headHeight = 25
player_bodyPos = pygame.Rect(resolution[0] // 2 - player_bodyWidth // 2,
                             resolution[1] - 60 - player_bodyHeight,
                             player_bodyWidth,
                             player_bodyHeight)
player_headPos = pygame.Rect(resolution[0] // 2 - player_headWidth // 2,
                             resolution[1] - 60 - player_bodyHeight - player_headHeight,
                             player_headWidth,
                             player_headHeight)
# Player's characteristics
player_hp = 100
player_speed = 3
player_ammo = 40
player_maxAmmo = player_ammo
player_bulletDamage = 10
# Player's Bullet
player_bulletWidth = 10
player_bulletHeight = 20
player_bulletPos = (0, 0, 1, 1)
player_bulletColor = WHITE
player_bulletSpeed = 4
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
enemy_speed = 3
enemy_bulletDamage = 15
# Enemy's Bullet
enemy_bulletWidth = 10
enemy_bulletHeight = 20
enemy_bulletPos = (0, 0, 1, 1)
enemy_bulletColor = WHITE
enemy_bulletSpeed = 9
enemy_bulletMissiles = []

enemy_shootDelay = 250
enemy_shootMaxDelay = int(enemy_shootDelay // (1000 / FPS))
enemy_shootDelay = enemy_shootMaxDelay

enemy_switchDirectionDelay = 1000
enemy_switchDirectionMaxDelay = int(enemy_switchDirectionDelay // (1000 / FPS))
enemy_switchDirectionDelay = enemy_switchDirectionMaxDelay

# Cheats
cheat_unlimitedammo = 0
cheat_godmode = 0
cheat_autofire = 0
cheat_autofire_delay = 125
cheat_autofire_maxDelay = int(cheat_autofire_delay // (1000 / FPS))
cheat_autofire_delay = cheat_autofire_maxDelay


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
    def __init__(self, hp, speed, ammo, maxAmmo, bodyPos, headPos, bodyWidth, bodyHeight, headWidth, headHeight,
                 bulletDamage, bulletWidth, bulletHeight, bulletPos, bulletSpeed, bulletColor, missiles):
        self.hp = hp
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


if randint(0, 1):
    enemy_speed = -enemy_speed


player = Player(player_hp, player_speed, player_ammo, player_maxAmmo,
                player_bodyPos, player_headPos, player_bodyWidth, player_bodyHeight, player_headWidth, player_headHeight,
                player_bulletDamage, player_bulletWidth, player_bulletHeight, player_bulletPos,
                player_bulletSpeed, player_bulletColor, player_bulletMissiles)
enemyStormtrooper = Enemy(enemy_hp, enemy_speed, 999, 999,
                          enemy_bodyPos, enemy_headPos, enemy_bodyWidth, enemy_bodyHeight, enemy_headWidth, enemy_headHeight,
                          enemy_bulletDamage, enemy_bulletWidth, enemy_bulletHeight, enemy_bulletPos,
                          enemy_bulletSpeed, enemy_bulletColor, enemy_bulletMissiles)


path_font_UI = abspath(__file__).replace("\\", "/")
path_font_UI = path_font_UI.replace("2SHIPS Singleplayer.py", "files/fonts/BigNoodleTooOblique.ttf")

font_UI = pygame.font.Font(path_font_UI, 45)
UI_enemy_hp_pos = (0 + 25, 0)
UI_player_hp_pos = (0 + 25, resolution[1] - 45)
UI_player_ammo_pos = (resolution[0] - 115, resolution[1] - 45)


def main():
    global player_bodyPos, player_headPos, enemy_shootDelay, enemy_switchDirectionDelay, cheat_autofire_delay
    while True:
        window.fill(BLACK)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys_exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not(cheat_autofire):
                    if player.ammo > 0:
                        player.shoot()
                        if not(cheat_unlimitedammo):
                            player.ammo -= 1
    

        # Moving player by pressing buttons
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and not (player.bodyPos[0] <= 5):
            player.bodyPos[0] -= player.speed
            player.headPos[0] -= player.speed
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and not (player.bodyPos[0] >= resolution[0] - player.bodyWidth - 5):
            player.bodyPos[0] += player.speed
            player.headPos[0] += player.speed
        
        
        if cheat_autofire_delay < cheat_autofire_maxDelay:
            cheat_autofire_delay += 1
        if cheat_autofire and keys[pygame.K_SPACE] and cheat_autofire_delay == cheat_autofire_maxDelay:
            player.shoot()
            if not(cheat_unlimitedammo):
                player.ammo -= 1
            cheat_autofire_delay = 0


        # Moving enemy
        enemyStormtrooper.bodyPos[0] += enemyStormtrooper.speed
        enemyStormtrooper.headPos[0] += enemyStormtrooper.speed
        
        if (enemyStormtrooper.bodyPos[0] <= 5 or
           enemyStormtrooper.bodyPos[0] >= resolution[0] - enemyStormtrooper.bodyWidth - 5):
            enemyStormtrooper.speed = -enemyStormtrooper.speed
        

        # Draw player
        pygame.draw.rect(window, GREEN, player.bodyPos)
        pygame.draw.rect(window, GREEN, player.headPos)

        # Draw enemy
        pygame.draw.rect(window, RED, enemyStormtrooper.bodyPos)
        pygame.draw.rect(window, RED, enemyStormtrooper.headPos)
        

        if enemy_switchDirectionDelay < enemy_switchDirectionMaxDelay:
            enemy_switchDirectionDelay += 1

        # Collision detection for player's bullets
        for missile in player.missiles:
            if not(missile[1] > 60 + enemyStormtrooper.bodyHeight + enemyStormtrooper.headHeight or
                   missile[1] < 60 - player.bulletHeight):
                if (does_collide(missile, enemyStormtrooper.headPos) or
                   does_collide(missile, enemyStormtrooper.bodyPos)):
                    if enemyStormtrooper.hp > 0:
                        enemyStormtrooper.hp -= player.bulletDamage
                    else:
                        enemyStormtrooper.hp = 0

                    del player.missiles[player.missiles.index(missile)]

            if (missile[0] > enemyStormtrooper.bodyPos[0] and
               missile[0] < enemyStormtrooper.bodyPos[0] + enemyStormtrooper.bodyWidth and
               missile[1] < resolution[1] + enemyStormtrooper.headHeight and
               enemy_switchDirectionDelay == enemy_switchDirectionMaxDelay):
                enemyStormtrooper.speed = -enemyStormtrooper.speed
                enemy_switchDirectionDelay = 0

        player.move_bullets()
        

        if enemy_shootDelay < enemy_shootMaxDelay:
            enemy_shootDelay += 1

        if (enemyStormtrooper.headPos[0] >= player.bodyPos[0] and
           enemyStormtrooper.headPos[0] < player.bodyPos[0] + player.bodyWidth - enemyStormtrooper.headWidth // 2 and
           enemy_shootDelay == enemy_shootMaxDelay):
            enemyStormtrooper.shoot()
            enemy_shootDelay = 0

        # Collision detection for enemy's bullets
        for missile in enemyStormtrooper.missiles:
            if (does_collide(missile, player.headPos) or
               does_collide(missile, player.bodyPos)):
                if player.hp > 0:
                    if not(cheat_godmode):
                        player.hp -= enemyStormtrooper.bulletDamage
                else:
                    player.hp = 0

                del enemyStormtrooper.missiles[enemyStormtrooper.missiles.index(missile)]

        enemyStormtrooper.move_bullets()
        

        # Draw UI
        pygame.draw.line(window, RED, (0, 45), (150, 45), 2)
        pygame.draw.line(window, GREEN, (0, resolution[1] - 45), (150, resolution[1] - 45), 2)
        pygame.draw.line(window, GREEN, (resolution[0] - 150, resolution[1] - 45),
                         (resolution[0], resolution[1] - 45), 2)
        pygame.draw.line(window, RED, (150, 45), (150, 0), 2)
        pygame.draw.line(window, GREEN, (150, resolution[1] - 45), (150, resolution[1]), 2)
        pygame.draw.line(window, GREEN, (resolution[0] - 150, resolution[1] - 45), (resolution[0] - 150, resolution[1]), 2)

        UI_enemy_hp = font_UI.render(str(enemyStormtrooper.hp) + " HP", 1, RED)
        UI_player_hp = font_UI.render(str(player.hp) + " HP", 1, GREEN)
        UI_player_ammo = font_UI.render(str(player.ammo) + "/" + str(player.maxAmmo), 1, GREEN)
        window.blit(UI_enemy_hp, UI_enemy_hp_pos)
        window.blit(UI_player_hp, UI_player_hp_pos)
        window.blit(UI_player_ammo, UI_player_ammo_pos)


        if enemyStormtrooper.hp <= 0 or player.hp <= 0:
            break
        if player.ammo == 0 and len(player.missiles) == 0:
            break


        pygame.display.update()
        clock.tick(FPS)


main()


font_gameOutcome = pygame.font.Font(path_font_UI, 135)
if enemyStormtrooper.hp <= 0:
    UI_message_gameOutcome = font_gameOutcome.render("YOU WON!", 1, GREEN)
elif player.hp <= 0 or (player.ammo == 0 and len(player.missiles) == 0):
    UI_message_gameOutcome = font_gameOutcome.render("YOU LOST", 1, RED)

while True:
    window.fill(BLACK)

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys_exit()

    window.blit(UI_message_gameOutcome, (0, 0))

    pygame.display.update()
    clock.tick(60)
