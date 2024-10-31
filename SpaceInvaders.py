import pygame
import math
import random

# constants
ENEMY_X_CHANGE, ENEMY_Y_CHANGE, SHIP_X_CHANGE, PROJECTILE_Y_CHANGE = 10, 20, 15, 15

shipImg = [pygame.image.load('Images/player1.png'), pygame.image.load('Images/player2.png'), pygame.image.load('Images/player3.png')]

projectileImg = [pygame.image.load('Images/shoot1.png'), pygame.image.load('Images/shoot2.png')]

siFlashImg = pygame.image.load('Images/flash.png')

droneImg = []
for i in range(5):
    droneImg.append(pygame.image.load(f'Images/drone-{i + 1}.png'))


class SpaceInvaders:
    # initializes fifth mini-game's variables and resets everytime its called
    def __init__(self, width_, height_, screen):
        self.width, self.height, self.screen = width_, height_, screen

        self.delLife = False
        self.isProjectileActive = False

        self.shipImg = shipImg[0]
        self.shipX = self.width / 2 - 32
        self.shipY = self.height - 100
        self.shipXChange = 0

        self.enemyImg = []
        self.enemyX = []
        self.enemyY = []
        self.enemyXChange = []
        self.enemyTurnIndex = []
        self.isTurningOnLeftSide = []
        self.enemyNum = 7

        # initializes each enemy's properties
        for enemy_index in range(self.enemyNum):
            self.enemyImg.append(droneImg[4])
            self.enemyX.append(random.randint(0, self.width - 64))
            self.enemyY.append(random.randint(50, 150))
            self.enemyXChange.append(ENEMY_X_CHANGE)
            self.enemyTurnIndex.append(0)
            self.isTurningOnLeftSide.append(False)

        self.projectileImg = None
        self.projectileIndex = 1
        self.projectileX = self.shipX + 5
        self.projectileY = self.height
        self.projectileXChange = 0
        self.projectileYChange = PROJECTILE_Y_CHANGE

    # shows ship and enemies

    def ship_show(self):
        self.shipImg = pygame.transform.scale(self.shipImg, (42, 52))
        self.screen.blit(self.shipImg, (self.shipX, self.shipY))

    def enemies_show(self, x_, y_, enemy_index_):
        self.screen.blit(self.enemyImg[enemy_index_], (x_, y_))

    # updates and animates projectile
    def projectile_update(self, projectile_index_):
        self.projectileImg = projectileImg[(int(projectile_index_) % 2)]
        self.projectileImg = pygame.transform.scale(self.projectileImg, (10, 32))
        self.screen.blit(self.projectileImg, (self.projectileX + 16, self.projectileY + 24))

    # checks for collisions with projectile
    def is_collision(self, x1, y1):
        distance = math.sqrt(math.pow(x1 - self.projectileX, 2) + (math.pow(y1 - self.projectileY, 2)))
        if distance < 32:
            return True
        return False

    def reset(self):
        self.shipImg = self.projectileImg = None
        for enemy_index in range(self.enemyNum):
            self.enemyImg[enemy_index] = None
