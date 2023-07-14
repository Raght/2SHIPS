import pygame
from GameObject import *


class ShipPrototype:
    def __init__(self, body_mesh,
                 acceleration, deceleration, max_velocity,
                 max_health, max_ammo, firerate,
                 weapon_prototype):
        self.body_mesh = body_mesh

        self.acceleration = acceleration
        self.deceleration = deceleration
        self.max_velocity = max_velocity

        self.max_health = max_health
        self.max_ammo = max_ammo
        self.firerate = firerate

        self.weapon_prototype = weapon_prototype


class Ship(ShipPrototype):
    def __init__(self, ship_prototype, body_mesh, weapon_prototype,
                 position, direction,
                 acceleration, deceleration, max_velocity,
                 health, max_health, ammo, max_ammo, firerate,
                 faction,
                 botDifficulty=None):
        super().__init__(ship_prototype.body_mesh)
        self.body = GameObject(position, 0, 0, self.body_mesh)
        self.direction = direction

        self.health = health
        self.ammo = ammo

        self.ticksToFire = FPS // firerate
        self.ticks = 0
        self.isDead = False

        self.faction = faction

        self.weapon = Weapon()

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
    def set_x(self, newX): self.set_coord(0, newX)
    def set_y(self, newY): self.set_coord(1, newY)
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

        self.velocity += self.deceleration * (clock.get_time() / 1000) # Hmmm...

        if (self.velocity > 0 and self.deceleration > 0) or (self.velocity < 0 and self.deceleration < 0):
            self.velocity = 0
