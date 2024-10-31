import pygame
import math
import random

# constants
DUCK_X_CHANGE, DUCK_AMPLITUDE, DUCK_FREQUENCY = 5, 250, 500

crosshairImg = pygame.image.load('Images/crosshair.png')

dhEnemyImg = []
for i in range(5):
    dhEnemyImg.append(pygame.image.load(f'Images/enemy{i + 1}.png'))


class Duck:
    # initializes enemy objects' variables and resets everytime its called
    def __init__(self, x, y, xchange, movement_type_, width_, height_, screen, going_left_):
        self.width, self.height, self.screen = width_, height_, screen

        self.xPos = x
        self.yPos = y
        self.xChange = xchange
        self.r = 60
        self.duckMovementType = movement_type_
        if self.duckMovementType == 1:
            self.yPos = random.randint(self.height / 2 - 50, self.height / 2 + 50)
        self.sinCos = random.randint(1, 2)
        self.duckAnimationIndex = 1
        self.goingLeft = going_left_
        self.duck_img = None

    # shows and animates this object
    def show(self, duck_index_):
        self.duck_img = dhEnemyImg[duck_index_]
        if self.goingLeft:
            self.duck_img = pygame.transform.flip(self.duck_img, True, False)
        else:
            self.duck_img = pygame.transform.flip(self.duck_img, False, False)
        self.duck_img = pygame.transform.scale(self.duck_img, (self.r, self.r))
        self.screen.blit(self.duck_img, (self.xPos, self.yPos))

    # updates this objects' movement
    def update(self):
        if self.duckMovementType != 1:
            self.xPos += self.xChange
        else:
            self.xPos += self.xChange
            if self.sinCos == 1:
                self.yPos = (math.sin(self.xPos / DUCK_FREQUENCY) * self.height / DUCK_AMPLITUDE) + self.yPos
            elif self.sinCos == 2:
                self.yPos = -(math.cos(self.xPos / DUCK_FREQUENCY) * self.height / DUCK_AMPLITUDE) + self.yPos
            if self.yPos > self.height - self.r:
                self.yPos = self.height - self.r
            elif self.yPos < self.r:
                self.yPos = self.r

    # checks for collisions with this object
    def is_collision(self, x1, y1):
        distance = math.sqrt(math.pow(x1 - self.xPos, 2) + (math.pow(y1 - self.yPos, 2)))
        if distance < self.r:
            return True
        return False

    def reset(self):
        self.duck_img = None


class DuckHunt:
    # initializes fourth mini-game's variables and resets everytime its called
    def __init__(self, width_, height_, screen):
        self.width, self.height, self.screen = width_, height_, screen

        self.duckClicked = False
        self.duckNum = 10
        self.ducks = []
        duck_index = 0

        self.ducksReset = False

        # creates a new object from above class per number of objects (self.duckNum)
        while duck_index < self.duckNum:

            if bool(random.getrandbits(1)):
                going_left = False
                x_change = DUCK_X_CHANGE
                x = -random.randint(0, self.width)

            else:
                going_left = True
                x_change = -DUCK_X_CHANGE
                x = random.randint(self.width, self.width * 2)

            self.ducks.append(Duck(x, random.randint(50, self.height - 50), x_change, random.randint(1, math.ceil(self.duckNum / 5)), self.width, self. height, self.screen, going_left))
            duck_index += 1

        self.crosshair_img = None

    # updates crosshair to mouse pos
    def update(self):
        self.crosshair_img = crosshairImg
        self.screen.blit(self.crosshair_img, (pygame.mouse.get_pos()[0] - 32, pygame.mouse.get_pos()[1] - 32))

    def reset(self):
        self.crosshair_img = None
