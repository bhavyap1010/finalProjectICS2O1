import pygame
import random

# constants
PONG_PADDLE_SPEED, PONG_BALL_CHANGE = 10, (6, 8)

paddleImg = pygame.image.load('Images/antenna.png')

ballImg = [pygame.image.load('Images/shot-1.png'), pygame.image.load('Images/shot-2.png'), pygame.image.load('Images/shot-3.png')]


class Pong:
    # initializes second mini-game's variables and resets everytime its called
    def __init__(self, width_, height_, screen):
        self.width, self.height, self.screen = width_, height_, screen

        self.pPaddleX = 20
        self.pPaddleY = self.height / 2
        self.pPaddleYChange = 0
        self.pPaddleW = 20
        self.pPaddleH = 100

        self.oPaddleX = self.width - self.pPaddleW - 10
        self.oPaddleY = self.height / 2
        self.oPaddleYChange = -PONG_PADDLE_SPEED
        self.oPaddleW = self.pPaddleW
        self.oPaddleH = self.pPaddleH

        self.ballX = self.width / 2
        self.ballY = self.height / 2
        self.ballXChange = -(random.randint(PONG_BALL_CHANGE[0], PONG_BALL_CHANGE[1]))
        self.ballYChange = random.randint(PONG_BALL_CHANGE[0], PONG_BALL_CHANGE[1])
        self.ballR = 30
        self.ball_index = 1
        self.isBallDirLeft = True

        self.p_paddle_img = self.o_paddle_img = self.ball_img = None

    # updates and animates each sprite
    def p_paddle_update(self):
        p_paddle_rect = (self.pPaddleX, self.pPaddleY, self.pPaddleW, self.pPaddleH)
        self.p_paddle_img = paddleImg
        self.p_paddle_img = pygame.transform.scale(self.p_paddle_img, (p_paddle_rect[2], p_paddle_rect[3]))
        self.screen.blit(self.p_paddle_img, (p_paddle_rect[0], p_paddle_rect[1]))

    def o_paddle_update(self):
        o_paddle_rect = (self.oPaddleX, self.oPaddleY, self.oPaddleW, self.oPaddleH)
        self.o_paddle_img = paddleImg
        self.o_paddle_img = pygame.transform.scale(self.o_paddle_img, (o_paddle_rect[2], o_paddle_rect[3]))
        self.screen.blit(self.o_paddle_img, (o_paddle_rect[0], o_paddle_rect[1]))

    def ball_update(self, ball_index_):
        ball_img_rect = (self.ballX, self.ballY, self.ballR, self.ballR)
        self.ball_img = ballImg[ball_index_]
        self.ball_img = pygame.transform.scale(self.ball_img, (ball_img_rect[2], ball_img_rect[3]))
        if self.isBallDirLeft:
            self.ball_img = pygame.transform.rotate(self.ball_img, 180)
        else:
            self.ball_img = pygame.transform.rotate(self.ball_img, 0)
        self.screen.blit(self.ball_img, (ball_img_rect[0], ball_img_rect[1]))

    def reset(self):
        self.p_paddle_img = self.o_paddle_img = self.ball_img = None
