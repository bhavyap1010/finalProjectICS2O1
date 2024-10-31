import pygame
import math
import random

# constants
OSU_WAIT_TIME, OSU_TYPE2_COUNTER_RANGE = 5, (1, 5)

asteroidImg = [pygame.image.load('Images/asteroid-1.png'), pygame.image.load('Images/asteroid-2.png'), pygame.image.load('Images/asteroid-3.png'), ]


class Osu:
    # initializes third mini-game's variables and resets everytime its called
    def __init__(self, width_, height_, screen):
        self.width, self.height, self.screen = width_, height_, screen

        self.circleR = 50
        self.circlePos = (random.randint(self.circleR, self.width - self.circleR), random.randint(self.circleR, self.height - self.circleR))
        self.circleType = random.randint(1, 3)
        self.circleCounter = random.randint(OSU_TYPE2_COUNTER_RANGE[0], OSU_TYPE2_COUNTER_RANGE[1])
        self.holdTime = random.randint(1, 3)
        self.rotationIndex = 0
        self.rotationClockwise = bool(random.getrandbits(1))

        self.clicks = 0
        self.type3StaticTime = 0
        self.waitTime = OSU_WAIT_TIME
        self.waitStaticTime = pygame.time.get_ticks()

        self.type3BarShow = False
        self.type3SoundDifference = 0
        self.type3SoundCheck = True

        self.asteroid_img = None

    # checks for collision
    def is_collision(self, x1, y1):
        distance = math.sqrt(math.pow(x1 - self.circlePos[0], 2) + (math.pow(y1 - self.circlePos[1], 2)))
        if distance < self.circleR:
            return True
        return False

    # updates asteroids and animates them
    def update(self, rotation_):
        self.asteroid_img = asteroidImg[self.circleType - 1]
        self.asteroid_img = pygame.transform.scale(self.asteroid_img, (2 * self.circleR, 2 * self.circleR))
        self.asteroid_img = pygame.transform.rotate(self.asteroid_img, rotation_)
        self.screen.blit(self.asteroid_img, (self.circlePos[0] - self.circleR, self.circlePos[1] - self.circleR))

    def reset(self):
        self.asteroid_img = None
