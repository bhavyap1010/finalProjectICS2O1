import pygame
import random

# constants
FB_Y_CHANGE, FB_GRAV, FB_BANNER_CHANGE, FB_BANNER_GAP = 20, 0.5, 10, 200

birdImg = [pygame.image.load('Images/vehicle-2-1.png'), pygame.image.load('Images/vehicle-2-2.png'), pygame.image.load('Images/vehicle-2-3.png')]

upperObsImg = []
for i in range(4):
    upperObsImg.append(pygame.image.load(f'Images/Banners/banner-big-{i + 1}.png'))

lowerObsImg = []
for i in range(3):
    lowerObsImg.append(pygame.image.load(f'Images/Banners/banner-coke-{i + 1}.png'))

upperObsImg2 = []
for i in range(4):
    upperObsImg2.append(pygame.image.load(f'Images/Banners/banner-scroll-{i + 1}.png'))

lowerObsImg2 = []
for i in range(4):
    lowerObsImg2.append(pygame.image.load(f'Images/Banners/banner-side-{i + 1}.png'))


class FlappyBird:
    # initializes first mini-game's variables and resets everytime its called
    def __init__(self, width_, height_, screen):
        self.width, self.height, self.screen = width_, height_, screen

        self.birdImg = birdImg[0]
        self.birdImg = pygame.transform.scale(self.birdImg, (91, 64))
        self.birdX = 50
        self.birdY = self.height / 2
        self.birdYChange = 0
        self.birdYGrav = FB_GRAV
        self.birdImgIndex = 0
        self.animationLock = False
        self.obstacleGap = FB_BANNER_GAP
        self.obstacleX = self.width
        self.obstacleX2 = self.width + self.width / 2
        self.obstacleW = 70
        self.obstacleH = random.randint(100, self.height - self.obstacleGap - 100)
        self.obstacleH2 = random.randint(100, self.height - self.obstacleGap - 100)
        self.obstacleXChange = -FB_BANNER_CHANGE
        self.bannerIndex1 = self.bannerIndex2 = self.banner2Index1 = self.banner2Index2 = 1

        self.upper_obs_img = self.upper_obs_img2 = self.lower_obs_img = self.lower_obs_img2 = None

    # updates and animates through each sprite (bird, obstacle, and obstacle2)

    def bird_update(self, bird_img_index_):
        if not self.animationLock:
            self.birdImg = birdImg[bird_img_index_]
        else:
            self.birdImg = birdImg[2]
        self.birdImg = pygame.transform.scale(self.birdImg, (91, 64))
        self.screen.blit(self.birdImg, (self.birdX, self.birdY))

    def obstacle_update(self, banner_index1_, banner_index2_):
        upper_obs_rect = (self.obstacleX, 0, self.obstacleW, self.obstacleH)
        self.upper_obs_img = upperObsImg[banner_index1_]
        self.upper_obs_img = pygame.transform.scale(self.upper_obs_img, (upper_obs_rect[2], upper_obs_rect[3]))
        self.screen.blit(self.upper_obs_img, (upper_obs_rect[0], upper_obs_rect[1]))

        bottom_obstacle_h = self.height - self.obstacleH - self.obstacleGap

        lower_obs_rect = (self.obstacleX, self.height - bottom_obstacle_h, self.obstacleW, bottom_obstacle_h)
        self.lower_obs_img = lowerObsImg[banner_index2_]
        self.lower_obs_img = pygame.transform.scale(self.lower_obs_img, (lower_obs_rect[2], lower_obs_rect[3]))
        self.screen.blit(self.lower_obs_img, (lower_obs_rect[0], lower_obs_rect[1]))

    def obstacle_update2(self, banner2_index1_, banner2_index2_):
        upper_obs_rect2 = (self.obstacleX2, 0, self.obstacleW, self.obstacleH2)
        self.upper_obs_img2 = upperObsImg2[banner2_index1_]
        self.upper_obs_img2 = pygame.transform.scale(self.upper_obs_img2, (upper_obs_rect2[2], upper_obs_rect2[3]))
        self.screen.blit(self.upper_obs_img2, (upper_obs_rect2[0], upper_obs_rect2[1]))

        bottom_obstacle_h = self.height - self.obstacleH2 - self.obstacleGap

        lower_obs_rect2 = (self.obstacleX2, self.height - bottom_obstacle_h, self.obstacleW, bottom_obstacle_h)
        self.lower_obs_img2 = lowerObsImg2[banner2_index2_]
        self.lower_obs_img2 = pygame.transform.scale(self.lower_obs_img2, (lower_obs_rect2[2], lower_obs_rect2[3]))
        self.screen.blit(self.lower_obs_img2, (lower_obs_rect2[0], lower_obs_rect2[1]))

    def reset(self):
        self.birdImg = self.upper_obs_img = self.upper_obs_img2 = self.lower_obs_img = self.lower_obs_img2 = None
