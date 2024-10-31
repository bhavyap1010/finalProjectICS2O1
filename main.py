# Bhavya Patel

# importing time and freetype module for fonts and pausing time between games
import time
import pygame.freetype

# importing game classes, explosion class, background vehicles, and loads sound, font, and image files
# this also imports the pygame, random, and math modules
from ExplosionAnimation import *
from FlappyBird import *
from Pong import *
from Osu import *
from DuckHunt import *
from SpaceInvaders import *
from BackgroundVehicles import *
from LoadFiles import *

# sets window caption and icon
pygame.display.set_caption("Switch!")
icon = pygame.image.load('Images/SwitchIcon.png')
pygame.display.set_icon(icon)

# sets window size
SIZE = WIDTH, HEIGHT = 1080, 640 - 64
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = WIDTH, HEIGHT + 64

# creates window
SCREEN = pygame.display.set_mode(WINDOW_SIZE, 0, 0)
# creates display surface which is drawn onto the window
DISPLAY = pygame.Surface(WINDOW_SIZE).convert_alpha()

# initializing screen shake variable and clock
screen_shake_index = 0
clock = pygame.time.Clock()

# loading and scaling background images, as well as their x position
farBackgroundImg = pygame.image.load('Images/back.png')
farBackgroundImg = pygame.transform.scale(farBackgroundImg, (WIDTH, WINDOW_HEIGHT))

backgroundImg = pygame.image.load('Images/middle.png')
backgroundImg = pygame.transform.scale(backgroundImg, (WIDTH, WINDOW_HEIGHT))
backgroundX = -(WIDTH / 2)

foregroundImg = pygame.image.load('Images/front.png')
foregroundImg = pygame.transform.scale(foregroundImg, (WIDTH, WINDOW_HEIGHT))
foregroundX = -(WIDTH / 2)

# loading and transforming glass crack images and initializing their position
glassCrack1 = GLASS_CRACK
glassCrack1 = pygame.transform.rotate(glassCrack1, random.randint(0, 360))
glassCrack1Pos = (random.randint(0, WIDTH / 2), random.randint(0, WINDOW_HEIGHT / 2))

glassCrack2 = GLASS_CRACK
glassCrack2 = pygame.transform.rotate(glassCrack2, random.randint(0, 360))
glassCrack2Pos = (random.randint(WIDTH / 2, WIDTH - 128), random.randint(WINDOW_HEIGHT / 2, WINDOW_HEIGHT - 128))

# loading and scaling sound icon, and initializing boolean isMuted variable
muteImg = pygame.image.load('Images/mute.png')
muteImg = pygame.transform.scale(muteImg, (32, 32))

volumeImg = pygame.image.load('Images/volume.png')
volumeImg = pygame.transform.scale(volumeImg, (32, 32))
isMuted = False


# dictionary for colors
colors = {
    "White": (255, 255, 255),
    "Black": (0, 0, 0),
    "Red": (255, 0, 0),
    "Green": (0, 255, 0),
    "Blue": (0, 0, 255),
    "Yellow": (255, 255, 0),
    "Dark Blue": (0, 0, 200),
    "Transparent Cobalt": (33, 0, 75, 240)
}

# creating objects from imported classes, and passing in surface and screen dimension values

explosion_sprites = pygame.sprite.Group()

fb = FlappyBird(WIDTH, HEIGHT, DISPLAY)

pong = Pong(WIDTH, HEIGHT, DISPLAY)

osu = Osu(WIDTH, HEIGHT, DISPLAY)

dh = DuckHunt(WIDTH, HEIGHT, DISPLAY)
dhShotClicked = False

si = SpaceInvaders(WIDTH, HEIGHT, DISPLAY)

bv = BackgroundVehicles(0, WIDTH, HEIGHT, DISPLAY)


# function to animate and display menu selector turret
def menu_selector(menu_index_, selector_index_):
    selector_img = selectorImg[int(selector_index_) % 8]
    selector_img = pygame.transform.scale(selector_img, (40, 34))

    # handles position of selector depending on whether controls and rules are selected
    if areInstructionsVisible:
        selector_pos = (WIDTH / 8 * 7 - 165, (WINDOW_HEIGHT / 8) * 7 - 57)
    else:
        selector_pos = (WIDTH / 2 - 75, 250 + menu_index_ * 75)
    DISPLAY.blit(selector_img, selector_pos)


# initializing keyIndex that represent which menu option is selected
# and the selector animation index to cycle through animations
keyIndex = selectorAnimationIndex = 0


# function for both start and replay menus
def wait_to_start(selector_index_):
    # incrementing selector animation index to have it animate
    global selectorAnimationIndex
    selectorAnimationIndex = selector_index_
    selectorAnimationIndex += 0.4

    # displaying menu options using pygame freetype
    title_text_pos = (WIDTH / 2 - 145, 75)
    titleFont.render_to(DISPLAY, title_text_pos, "Sw!tch", colors["White"])

    menu_x_pos = WIDTH / 2

    ctrls_text_pos = (menu_x_pos, 325)
    menuFont.render_to(DISPLAY, ctrls_text_pos, "Ctrls", colors["White"])

    options_text_pos = (menu_x_pos, 400)
    menuFont.render_to(DISPLAY, options_text_pos, "Rules", colors["White"])

    exit_text_pos = (menu_x_pos, 475)
    menuFont.render_to(DISPLAY, exit_text_pos, "Ex!t", colors["White"])

    # handling whether the menu should be in replay or in start form
    if not replay:
        start_text_pos = (menu_x_pos, 250)
        menuFont.render_to(DISPLAY, start_text_pos, "Start", colors["White"])

    else:
        start_text_pos = (menu_x_pos, 250)
        menuFont.render_to(DISPLAY, start_text_pos, "Replay", colors["White"])

        global farBackgroundImg
        farBackgroundImg = BACK
        global backgroundImg
        backgroundImg = MIDDLE
        global foregroundImg
        foregroundImg = FRONT

        farBackgroundImg = pygame.transform.scale(farBackgroundImg, (WIDTH, WINDOW_HEIGHT))
        backgroundImg = pygame.transform.scale(backgroundImg, (WIDTH, WINDOW_HEIGHT))
        foregroundImg = pygame.transform.scale(foregroundImg, (WIDTH, WINDOW_HEIGHT))

        global glassCrack1
        glassCrack1 = GLASS_CRACK
        glassCrack1 = pygame.transform.rotate(glassCrack1, random.randint(0, 360))
        global glassCrack1Pos
        glassCrack1Pos = (random.randint(0, WIDTH / 2), random.randint(0, WINDOW_HEIGHT / 2))

        global glassCrack2
        glassCrack2 = GLASS_CRACK
        glassCrack2 = pygame.transform.rotate(glassCrack2, random.randint(0, 360))
        global glassCrack2Pos
        glassCrack2Pos = (random.randint(WIDTH / 2, WIDTH - 128), random.randint(WINDOW_HEIGHT / 2, WINDOW_HEIGHT - 128))


# function that displays controls and rules
def show_instructions(menu_index_):
    # loads pop up window
    info_back = pygame.Surface(((WIDTH / 8) * 6, (WINDOW_HEIGHT / 8) * 6), pygame.SRCALPHA)
    info_back.fill(colors["Transparent Cobalt"])
    DISPLAY.blit(info_back, (WIDTH / 8, WINDOW_HEIGHT / 8))

    pygame.draw.rect(DISPLAY, colors["Dark Blue"], (WIDTH / 8, WINDOW_HEIGHT / 8, (WIDTH / 8) * 6, (WINDOW_HEIGHT / 8) * 6), 10, 15)

    # shows the controls or rules depending on which menu option is selected
    if menu_index_ == 1:
        ctrls_img = CONTROLS_IMAGE
        DISPLAY.blit(ctrls_img, (WIDTH / 8, WINDOW_HEIGHT / 8))
    elif menu_index_ == 2:
        rules_img = RULES_IMAGE
        DISPLAY.blit(rules_img, (WIDTH / 8, WINDOW_HEIGHT / 8))

    # overlays back button
    how_to_play_text_pos = (WIDTH / 8 * 7 - 110, (WINDOW_HEIGHT / 8) * 7 - 60)
    howToPlayReturnFont.render_to(DISPLAY, how_to_play_text_pos, "back", colors["White"])


# initializing boolean variable that checks if instructions are visible
areInstructionsVisible = False


# function that loads each minigame
def load_minigame(prev_game_state_):
    # adds a small pause between each change of game state
    time.sleep(0.1)

    # randomly selects minigame
    global game_state
    game_state = random.randint(1, 5)

    # loads parallax background depending on the minigame
    global farBackgroundImg
    global backgroundImg
    global foregroundImg

    if game_state == OSU or game_state == SPACE_INVADERS:
        farBackgroundImg = BG_BACK
        backgroundImg = BG_PLANET
        foregroundImg = BG_STARS

    elif game_state == PONG or game_state == DUCKHUNT:
        farBackgroundImg = SKYLINE
        backgroundImg = BUILDINGS
        foregroundImg = NEAR_BUILDINGS

    else:
        farBackgroundImg = FAR_BUILDINGS
        backgroundImg = BACK_BUILDINGS
        foregroundImg = FOREGROUND

    # scales the backgrounds
    farBackgroundImg = pygame.transform.scale(farBackgroundImg, (WIDTH, WINDOW_HEIGHT))
    backgroundImg = pygame.transform.scale(backgroundImg, (WIDTH, WINDOW_HEIGHT))
    foregroundImg = pygame.transform.scale(foregroundImg, (WIDTH, WINDOW_HEIGHT))

    # initializes background vehicles
    bv.__init__(game_state, WIDTH, HEIGHT, DISPLAY)

    # resets previously loaded files
    if prev_game_state_ == FLAPPY_BIRD:
        fb.reset()
    elif prev_game_state_ == PONG:
        pong.reset()
    elif prev_game_state_ == OSU:
        osu.reset()
    elif prev_game_state_ == DUCKHUNT:
        dh.reset()

        for j in range(len(dh.ducks)):
            dh.ducks[j].reset()

    elif prev_game_state_ == SPACE_INVADERS:
        si.reset()

    # depending on game state, initializes each game
    if game_state == FLAPPY_BIRD:
        fb.__init__(WIDTH, HEIGHT, DISPLAY)

    elif game_state == PONG:
        pong.__init__(WIDTH, HEIGHT, DISPLAY)

    elif game_state == OSU:
        osu.__init__(WIDTH, HEIGHT, DISPLAY)

    elif game_state == DUCKHUNT:
        dh.__init__(WIDTH, HEIGHT, DISPLAY)

    elif game_state == SPACE_INVADERS:
        si.__init__(WIDTH, HEIGHT, DISPLAY)

        # creates portal animation for when enemies spawn in
        for enemy_index in range(si.enemyNum):
            enemy_portal_init = ExplosionAnimation(si.enemyX[enemy_index] + 32, si.enemyY[enemy_index] + 32, 5.1, None)
            explosion_sprites.add(enemy_portal_init)

    # resets minigame static time and randomly selects how long the current minigame will last from 10-15 seconds
    global minigameStatTime
    minigameStatTime = pygame.time.get_ticks()
    global minigameSeconds
    minigameSeconds = random.randint(10, 15)


# Assigns the values to each game state
MENU, FLAPPY_BIRD, PONG, OSU, DUCKHUNT, SPACE_INVADERS = 0, 1, 2, 3, 4, 5

# initializes minigame static time and randomly selects how long the current minigame will last from 10-15 seconds
minigameStatTime = pygame.time.get_ticks()
minigameSeconds = random.randint(10, 15)


# function that displays high score, score, lives, and next minigame
def show_data(lives_, score_, high_score_, time_difference_, wait_time, foreground_bar_animation_index_):
    # loops through each iteration of and calls the moving front bars respectively
    for objectLoopIndex in range(6):
        show_front_bar(objectLoopIndex, foreground_bar_animation_index_)

    # shows the data
    data_text_y = WINDOW_HEIGHT - 45

    lives_text_pos = (15, data_text_y)
    dataFont.render_to(DISPLAY, lives_text_pos, "L!ves: " + str(lives_), colors["White"])

    score_text_pos = (150, data_text_y)
    dataFont.render_to(DISPLAY, score_text_pos, "Score: " + str(score_), colors["White"])

    high_score_text_pos = (300, data_text_y)
    dataFont.render_to(DISPLAY, high_score_text_pos, "H!gh Score: " + str(high_score_), colors["White"])

    countdown = wait_time - (math.floor(time_difference_ / 1000))

    game_time_text_pos = (WIDTH - 220, data_text_y)
    dataFont.render_to(DISPLAY, game_time_text_pos, "Next Game !n: " + str(countdown), colors["White"])


# draws the core of the front bar's pattern which is duplicated
def show_front_bar(object_loop_index_, foreground_bar_animation_index_):
    bar_img_rect1 = ((object_loop_index_ * (60 + 51 + 128)) + foreground_bar_animation_index_, HEIGHT, 60, 64)
    bar_img1 = BAR1
    bar_img1 = pygame.transform.scale(bar_img1, (bar_img_rect1[2], bar_img_rect1[3]))
    DISPLAY.blit(bar_img1, (bar_img_rect1[0], bar_img_rect1[1]))

    bar_img_rect2 = (bar_img_rect1[0] + bar_img_rect1[2], HEIGHT - (81 - 64), 51, 81)
    bar_img2 = BAR2
    bar_img2 = pygame.transform.scale(bar_img2, (bar_img_rect2[2], bar_img_rect2[3]))
    DISPLAY.blit(bar_img2, (bar_img_rect2[0], bar_img_rect2[1]))

    bar_img_rect3 = (bar_img_rect1[0] + bar_img_rect1[2] + bar_img_rect2[2], HEIGHT, 128, 64)
    bar_img3 = BAR3
    bar_img3 = pygame.transform.scale(bar_img3, (bar_img_rect3[2], bar_img_rect3[3]))
    DISPLAY.blit(bar_img3, (bar_img_rect3[0], bar_img_rect3[1]))


# initializes the index upon which the front bar is positioned in relation to
foreground_bar_animation_index = -((60 + 51 + 128) / 2)

# initializes game state, lives, high score, and score
lives = 3
highScore = score = 0
game_state = MENU

# initializes replay being false
replay = False

# forever loop
running = True
while running:

    # updates current time
    currentTime = pygame.time.get_ticks()

    # sets frame rate
    clock.tick(30)

    # fills background to black
    DISPLAY.fill(colors["Black"])

    # overlays background images relative to their x position (backgroundX)
    DISPLAY.blit(farBackgroundImg, (0, 0))
    DISPLAY.blit(backgroundImg, (backgroundX - (WIDTH / 2), 0))
    DISPLAY.blit(backgroundImg, (backgroundX + WIDTH / 2, 0))
    DISPLAY.blit(foregroundImg, (foregroundX - (WIDTH / 2), 0))
    DISPLAY.blit(foregroundImg, (foregroundX + WIDTH / 2, 0))

    # draws and updates background vehicles when not in menu state
    if game_state != MENU:
        for k in range(len(bv.vehicles)):
            bv.vehicles[k].show()
            bv.vehicles[k].update()

    # darkens everything behind the game to make sprites pop out
    backPane = pygame.Surface((WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    backPane.fill((0, 0, 0, 128))
    DISPLAY.blit(backPane, (0, 0))

    # checks for user interaction events
    for event in pygame.event.get():
        # quits pygame when user closes the tab
        if event.type == pygame.QUIT:
            running = False
        # toggles mute
        if WIDTH - 48 < pygame.mouse.get_pos()[0] < WIDTH - 16:
            if 16 < pygame.mouse.get_pos()[1] < 48:
                if event.type == pygame.MOUSEBUTTONUP:
                    isMuted = not isMuted

        # cycles through index using up or down key events
        # when space is pressed, (depending on selected option)
            # starts game
            # toggles show instructions
            # exits pygame
        if game_state == MENU:
            if event.type == pygame.KEYUP:
                if not areInstructionsVisible:
                    if event.key == pygame.K_UP:
                        keyIndex -= 1
                        selectSound.play()
                        if keyIndex < 0:
                            keyIndex = 0
                    elif event.key == pygame.K_DOWN:
                        keyIndex += 1
                        selectSound.play()
                        if keyIndex > 3:
                            keyIndex = 3
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    enterSound.play()
                    if keyIndex == 0:
                        lives = 3
                        load_minigame(game_state)
                    elif keyIndex == 1 or keyIndex == 2:
                        areInstructionsVisible = not areInstructionsVisible
                    elif keyIndex == 3:
                        pygame.quit()

        # allows vehicle to fly when space pressed
        if game_state == FLAPPY_BIRD:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    fbFlySound.play()
                    fb.animationLock = True
                    fb.birdYChange = -FB_Y_CHANGE

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    fb.animationLock = False
                    fb.birdYChange = 0

        # moves paddle up or do depending on up arrow or down arrow key event being pressed
        # NOTE: upon life loss, a new minigame is loaded by calling load_minigame()
        if game_state == PONG:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    pong.pPaddleYChange = PONG_PADDLE_SPEED
                if event.key == pygame.K_UP:
                    pong.pPaddleYChange = -PONG_PADDLE_SPEED

            if event.type == pygame.KEYUP:
                pong.pPaddleYChange = 0

        # handles events for each type of asteroid in third minigame type
       if game_state == OSU:

            # spawns new asteroid when "C" pressed while mouse is within asteroid position
            # if "C" is pressed elsewhere, you lose a life
            if osu.circleType == 1:
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_c:
                        if osu.is_collision(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):

                            osuHitSound.play()

                            score += 1

                            osuExplosion = ExplosionAnimation(osu.circlePos[0], osu.circlePos[1], game_state, 2 * osu.circleR)
                            explosion_sprites.add(osuExplosion)

                            osu.__init__(WIDTH, HEIGHT, DISPLAY)
                        else:
                            lives -= 1
                            screen_shake_index = 20
                            if lives != 0:
                                load_minigame(game_state)

            # damages asteroid when "V" pressed while mouse is within asteroid position
            # new asteroid spawns when asteroid health runs out
            # if "V" is pressed elsewhere, you lose a life
            elif osu.circleType == 2:

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_v:

                        if osu.clicks + 1 < osu.circleCounter:
                            if osu.is_collision(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                                osuHitSound.play()
                                osu.clicks += 1

                            else:
                                lives -= 1
                                screen_shake_index = 20
                                if lives != 0:
                                    load_minigame(game_state)
                        else:
                            score += 1

                            osuHitSound.play()

                            osuExplosion = ExplosionAnimation(osu.circlePos[0], osu.circlePos[1], game_state, 2 * osu.circleR)
                            explosion_sprites.add(osuExplosion)
                            explosion_sprites.add(osuExplosion)

                            osu.__init__(WIDTH, HEIGHT, DISPLAY)

            # increments selector bar when "B" pressed and held while mouse is within asteroid position
            # new asteroid spawns when "B" is released and both bars are lined up, while mouse is within asteroid position
            # if "B" is pressed/released elsewhere, you lose a life
            elif osu.circleType == 3:

                spacePressed = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b:
                        if osu.is_collision(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):

                            osu.type3BarShow = True
                            osu.type3StaticTime = pygame.time.get_ticks()

                            if osu.type3SoundCheck:
                                osu.type3StaticTimeSoundDifference = math.floor((currentTime - osu.type3StaticTime) / 1000)
                                osu.type3SoundCheck = not osu.type3SoundCheck

                            spacePressed = True

                        else:
                            lives -= 1
                            screen_shake_index = 20
                            if lives != 0:
                                load_minigame(game_state)

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_b:
                        if osu.is_collision(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):

                            if spacePressed:

                                osu.type3BarShow = False
                                spacePressed = False

                                if osu.holdTime * 1000 < currentTime - osu.type3StaticTime < (osu.holdTime + 1) * 1000:
                                    score += 1

                                    osuEnterSound.play()

                                    osuExplosion = ExplosionAnimation(osu.circlePos[0], osu.circlePos[1], game_state, 2 * osu.circleR)
                                    explosion_sprites.add(osuExplosion)

                                    osu.__init__(WIDTH, HEIGHT, DISPLAY)

                        # each asteroid stays for 5 seconds, if time is up, you lose a life
                        else:
                            lives -= 1
                            screen_shake_index = 20
                            if lives != 0:
                                load_minigame(game_state)

        # explodes enemy spaceships when clicked on
        if game_state == DUCKHUNT:
            for j in range(len(dh.ducks)):
                if event.type == pygame.MOUSEBUTTONUP:
                    dhShotClicked = True
                    if dh.ducks[j].is_collision(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                        dhExplosionSound.play()
                        dh.duckClicked = True

        # moves spaceship left or right with corresponding arrow keys
        # fires projectile when space is pressed (and projectile is not already fired)
        if game_state == SPACE_INVADERS:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    si.shipXChange = -SHIP_X_CHANGE
                    si.shipImg = shipImg[1]

                elif event.key == pygame.K_RIGHT:
                    si.shipXChange = SHIP_X_CHANGE
                    si.shipImg = shipImg[2]

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    si.shipImg = shipImg[0]
                    si.shipXChange = 0
                if event.key == pygame.K_SPACE:
                    if not si.isProjectileActive:
                        siShot1Sound.play()
                        siShot2Sound.play()

                        flashImg = siFlashImg
                        flashImg = pygame.transform.scale(flashImg, (28, 17))
                        DISPLAY.blit(flashImg, (si.shipX + 6, si.shipY - 10))

                        si.projectileX = si.shipX
                        # sets projectile fired to true
                        si.isProjectileActive = True

    # updates the game depending on game state

    # updates vehicle and banners for first minigame
    if game_state == FLAPPY_BIRD:

        # creates explosion animation class for this minigame and passes in coordinates, game state, and explosion size
        fbExplosion = ExplosionAnimation(fb.bidX + 176 / 2, fb.birdY + 125 / 2, game_state, 91)

        # updates y pos of vehicle while accounting for grav
        fb.birdYChange += fb.birdYGrav
        fb.birdY += fb.birdYChange

        # constrains vehicle Y on screen
        if fb.birdY <= 0:
            fb.birdY = 0
        if fb.birdY >= HEIGHT - 64:
            fb.birdY = HEIGHT - 64

        # updates banners
        fb.obstacleX += fb.obstacleXChange
        fb.obstacleX2 += fb.obstacleXChange

        # loads hit boxes
        birdHitBox = pygame.Rect(fb.birdX, fb.birdY, 91, 64)
        upperObstacleHitBox = pygame.Rect(fb.obstacleX, 0, fb.obstacleW, fb.obstacleH)
        lowerObstacleHitBox = pygame.Rect(fb.obstacleX, fb.obstacleH + fb.obstacleGap, fb.obstacleW, HEIGHT - fb.obstacleH - fb.obstacleGap)
        upperObstacleHitBox2 = pygame.Rect(fb.obstacleX2, 0, fb.obstacleW, fb.obstacleH2)
        lowerObstacleHitBox2 = pygame.Rect(fb.obstacleX2, fb.obstacleH2 + fb.obstacleGap, fb.obstacleW, HEIGHT - fb.obstacleH2 - fb.obstacleGap)

        condition_1 = birdHitBox.colliderect(upperObstacleHitBox) or birdHitBox.colliderect(lowerObstacleHitBox)
        condition_2 = birdHitBox.colliderect(upperObstacleHitBox2) or birdHitBox.colliderect(lowerObstacleHitBox2)

        # checks for collision between vehicle and banner
        if condition_1 or condition_2:
            fbExplosionSound.play()
            explosion_sprites.add(fbExplosion)
            fbExplosionLock = True
            lives -= 1
            screen_shake_index = 20
            if lives != 0:
                load_minigame(game_state)

        # moves banners from right to left and cycles through with different height each time
        if fb.obstacleX <= -fb.obstacleW:
            score += 1
            fb.obstacleX = WIDTH
            fb.obstacleH = random.randint(100, HEIGHT - fb.obstacleGap - 100)

        if fb.obstacleX2 <= -fb.obstacleW:
            score += 1
            fb.obstacleX2 = WIDTH
            fb.obstacleH2 = random.randint(100, HEIGHT - fb.obstacleGap - 100)

        # increments animation indices for each sprite
        fb.birdImgIndex += 0.5
        fb.bannerIndex1 += 0.4
        fb.bannerIndex2 += 0.01
        fb.banner2Index1 += 0.2
        fb.banner2Index2 += 0.4

        # tells the objects to update from class
        fb.bird_update(int(fb.birdImgIndex) % 2)
        fb.obstacle_update(int(fb.bannerIndex1) % 4, int(fb.bannerIndex2) % 3)
        fb.obstacle_update2(int(fb.banner2Index1) % 4, int(fb.banner2Index2) % 4)

    # updates sprites in second minigame
    if game_state == PONG:

        # updates player paddle
        pong.pPaddleY += pong.pPaddleYChange

        # constrains player paddle
        if pong.pPaddleY <= 0:
            pong.pPaddleY = 0

        if pong.pPaddleY >= HEIGHT - pong.pPaddleH:
            pong.pPaddleY = HEIGHT - pong.pPaddleH

        # updates opponents paddle
        pong.oPaddleY += pong.oPaddleYChange

        # constrains opponents paddle
        if pong.oPaddleY <= 0:
            pong.oPaddleYChange *= -1

        if pong.oPaddleY >= HEIGHT - pong.pPaddleH:
            pong.oPaddleYChange *= -1

        # updates ball
        pong.ballX += pong.ballXChange
        pong.ballY += pong.ballYChange

        # bounces off of the top and bottom of the screen
        if pong.ballY - pong.ballR <= 0:
            pongHitSound.play()

            pongExplosion = ExplosionAnimation(pong.ballX + pong.ballR / 2, pong.ballY + pong.ballR / 2, game_state, pong.ballR)
            explosion_sprites.add(pongExplosion)

            pong.ballYChange *= -1

        if pong.ballY + pong.ballR >= HEIGHT:
            pongHitSound.play()
            pongExplosion = ExplosionAnimation(pong.ballX, pong.ballY, game_state, pong.ballR)
            explosion_sprites.add(pongExplosion)

            pong.ballYChange *= -1

        # checks if ball reaches pass player, upon which loses life and loads minigame
        if pong.ballX - pong.ballR <= 0:
            lives -= 1
            screen_shake_index = 20
            if lives != 0:
                load_minigame(game_state)

        # loads hit boxes
        ballHitBox = pygame.Rect(pong.ballX, pong.ballY, pong.ballR, pong.ballR)
        pPaddleHitBox = pygame.Rect(pong.pPaddleX, pong.pPaddleY, pong.pPaddleW, pong.pPaddleH)
        oPaddleHitBox = pygame.Rect(pong.oPaddleX, pong.oPaddleY, pong.oPaddleW, pong.oPaddleH)

        # bounces upon collision
        if ballHitBox.colliderect(pPaddleHitBox) or ballHitBox.colliderect(oPaddleHitBox):
            pongHitSound.play()
            pongExplosion = ExplosionAnimation(pong.ballX, pong.ballY, game_state, pong.ballR)
            explosion_sprites.add(pongExplosion)

            pong.isBallDirLeft = not pong.isBallDirLeft
            pong.ballXChange *= -1

        # increments score when ball goes past opponent paddle and restarts pong
        if pong.ballX + pong.ballR >= WIDTH:
            score += 1
            pong.__init__(WIDTH, HEIGHT, DISPLAY)

        # animates ball
        pong.ball_index += 0.2

        # tells the objects to update from class
        pong.p_paddle_update()
        pong.o_paddle_update()
        pong.ball_update(int(pong.ball_index) % 3)

    # updates sprites in third minigame
    if game_state == OSU:
        # sets rotation to clockwise or counter-clockwise depending on the class value which is randomized upon initialization
        if osu.rotationClockwise:
            osu.rotationIndex -= 1
        else:
            osu.rotationIndex += 1

        # updates asteroids as long as 5 seconds haven't passed
        if currentTime - osu.waitStaticTime < osu.waitTime * 1000:
            # updates asteroid and passes in rotation index
            osu.update(int(osu.rotationIndex) % 360)

            # shows and updates health bar for green asteroid
            if osu.circleType == 2:
                pygame.draw.rect(DISPLAY, colors["Red"], (osu.circlePos[0] - osu.circleR / 4, osu.circlePos[1] + osu.circleR - 20, osu.circleR, 10))

                type2Width = osu.circleR - osu.clicks * osu.circleR / osu.circleCounter
                pygame.draw.rect(DISPLAY, colors["Green"], (osu.circlePos[0] - osu.circleR / 4, osu.circlePos[1] + osu.circleR - 20, type2Width, 10))

            # shows and updates two bars
            if osu.circleType == 3:

                pygame.draw.rect(DISPLAY, colors["Blue"], (osu.circlePos[0] - osu.circleR / 4, osu.circlePos[1] + osu.circleR - 35, osu.circleR, 10))

                type3X1 = (osu.circlePos[0] - osu.circleR / 4) + osu.holdTime * (osu.circleR / 5)
                type3Y1 = osu.circlePos[1] + osu.circleR
                pygame.draw.rect(DISPLAY, colors["Yellow"], (type3X1, type3Y1 - 35, 10, 10))

                pygame.draw.rect(DISPLAY, colors["Blue"], (osu.circlePos[0] - osu.circleR / 4, osu.circlePos[1] + osu.circleR - 15, osu.circleR, 10))

                if osu.type3BarShow:
                    if osu.type3StaticTimeSoundDifference != math.floor((currentTime - osu.type3StaticTime) / 1000):
                        osuSelectSound.play()
                        osu.type3StaticTimeSoundDifference = math.floor((currentTime - osu.type3StaticTime) / 1000)
                        osu.type3SoundCheck = not osu.type3SoundCheck

                    type3X2 = (osu.circlePos[0] - osu.circleR / 4) + math.floor((currentTime - osu.type3StaticTime) / 1000) * (osu.circleR / 5)
                    type3Y2 = osu.circlePos[1] + osu.circleR

                    if type3X2 >= osu.circlePos[0] - osu.circleR / 4:
                        pygame.draw.rect(DISPLAY, colors["Yellow"], (type3X2, type3Y2 - 15, 10, 10))

        # if time is up, removes a life and spawns new asteroid
        else:
            lives -= 1
            screen_shake_index = 20

            osu.__init__(WIDTH, HEIGHT, DISPLAY)

    # updates sprites in fourth minigame
    if game_state == DUCKHUNT:

        # cycles through each enemy
        for j in range(len(dh.ducks)):
            # updates, shows, and animates enemies
            dh.ducks[j].duckAnimationIndex += random.randint(2, 4) / 10
            dh.ducks[j].show(int(dh.ducks[j].duckAnimationIndex) % 5)
            dh.ducks[j].update()

            # explodes duck and sends it back off-screen when clicked on
            if dh.ducks[j].is_collision(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) and dh.duckClicked:

                duckExplosion = ExplosionAnimation(dh.ducks[j].xPos + dh.ducks[j].r / 2, dh.ducks[j].yPos + dh.ducks[j].r / 2, game_state, dh.ducks[j].r)
                explosion_sprites.add(duckExplosion)

                score += 1

                dh.duckClicked = False

                # handles whether to send back to left or to right side
                if not dh.ducks[j].goingLeft:
                    dh.ducks[j].xPos = -dh.ducks[j].r
                else:
                    dh.ducks[j].xPos = WIDTH + dh.ducks[j].r

                # randomizes whether ducks should move in a linear or a sinusoidal pattern
                dh.ducks[j].duckMovementType = random.randint(1, math.ceil(dh.duckNum / 2))

                if dh.ducks[j].duckMovementType != 1:
                    dh.ducks[j].yPos = random.randint(50, HEIGHT - 50)

                else:
                    dh.ducks[j].yPos = random.randint(HEIGHT / 2 - 50, HEIGHT / 2 + 50)

            # removes life and loads minigame if enemies reach other side of scree
            if not dh.ducks[j].goingLeft:
                if dh.ducks[j].xPos >= WIDTH:
                    lives -= 1
                    screen_shake_index = 20
                    if lives != 0:
                        load_minigame(game_state)
            else:
                if dh.ducks[j].xPos <= -dh.ducks[j].r:
                    lives -= 1
                    screen_shake_index = 20
                    if lives != 0:
                        load_minigame(game_state)

        # plays shot sound separately from explosion sound to avoid one sound drowning out the other
        if dhShotClicked:
            dhShotSound.set_volume(0.5)
            dhShotSound.play()
            dhShotClicked = False

        # updates fourth minigame
        dh.update()

    # updates sprites in fifth minigame
    if game_state == SPACE_INVADERS:
        # removes life if class detects enemy reaching player
        # done through class so that it can only be set true once, and not multiple times by all enemies and as a result doesn't glitch
        if si.delLife:
            lives -= 1
            screen_shake_index = 20
            si.delLife = False
            if lives != 0:
                load_minigame(game_state)

        # updates ship x pos
        si.shipX += si.shipXChange

        # constrains ship x pos to screen
        if si.shipX <= 0:
            si.shipX = 0
        elif si.shipX >= WIDTH - 64:
            si.shipX = WIDTH - 64

        # cycles through each enemy
        for i in range(si.enemyNum):
            # sets si.delLife to true when enemy reaches ship so that other enemies cannot load a minigame if they reach the ship around the same time
            if si.enemyY[i] > si.shipY - 32:
                si.delLife = True

            # updates enemy x
            si.enemyX[i] += si.enemyXChange[i]

            # turns and animates enemy when reaches left side, and increments y value
            if si.enemyX[i] <= 0:

                si.enemyTurnIndex[i] += 0.5
                si.enemyImg[i] = droneImg[(int(si.enemyTurnIndex[i]) % 4) + 1]

                if (int(si.enemyTurnIndex[i]) % 4) + 2 < 5:
                    si.isTurningOnLeftSide[i] = True
                else:
                    si.isTurningOnLeftSide[i] = False

                if not si.isTurningOnLeftSide[i]:
                    si.enemyTurnIndex[i] = 0
                    si.enemyXChange[i] = 10
                else:
                    si.enemyXChange[i] = 0
                    si.enemyY[i] += ENEMY_Y_CHANGE

            # turns and animates enemy when reaches right side, and increments y value
            elif si.enemyX[i] >= WIDTH - 64:

                si.enemyTurnIndex[i] += 0.5
                si.enemyImg[i] = droneImg[5 - ((int(si.enemyTurnIndex[i]) % 4) + 2)]

                if 6 - ((int(si.enemyTurnIndex[i]) % 4) + 2) > 1:
                    si.isTurningOnLeftSide[i] = True
                else:
                    si.isTurningOnLeftSide[i] = False

                if not si.isTurningOnLeftSide[i]:
                    si.enemyTurnIndex[i] = 0
                    si.enemyXChange[i] = -10
                else:
                    si.enemyXChange[i] = 0
                    si.enemyY[i] += ENEMY_Y_CHANGE

            # checks for collision between projectile and enemy for each enemy
            if si.is_collision(si.enemyX[i], si.enemyY[i]):
                score += 1

                # resets projectile
                si.projectileY = si.shipY + 10
                si.isProjectileActive = False

                siExplosionSound.play()

                enemyExplosion = ExplosionAnimation(si.enemyX[i] + 32, si.enemyY[i] + 32, game_state, 64)
                explosion_sprites.add(enemyExplosion)

                # spawns new enemy upon collision at the top of the screen
                si.enemyImg[i] = droneImg[4]
                si.enemyX[i] = random.randint(0, WIDTH - 50)
                si.enemyY[i] = random.randint(50, 150)
                enemyPortal = ExplosionAnimation(si.enemyX[i] + 32, si.enemyY[i] + 32, 5.1, None)
                explosion_sprites.add(enemyPortal)
                si.enemyXChange[i] = 10
                si.enemyTurnIndex[i] = 0
                si.isTurningOnLeftSide[i] = False

            # shows enemies
            si.enemies_show(si.enemyX[i], si.enemyY[i], i)

        # resets projectile when reaches the top of the screen
        if si.projectileY <= 0:
            si.projectileY = si.shipY + 10
            si.isProjectileActive = False

        # increments projectile animation index
        si.projectileIndex += 0.2

        # updates and animates projectile only when launched
        if si.isProjectileActive:
            if si.projectileY < si.shipY:
                si.projectile_update(si.projectileIndex)

            si.projectileY -= si.projectileYChange

        # shows ship
        si.ship_show()

    # updates and draws all explosion sprites constantly
    # so that when an explosion is called, the explosion sprite can create an object with the passed in parameters where it is called
    explosion_sprites.update(lives, game_state)
    explosion_sprites.draw(DISPLAY)

    # updates menu by calling functions
    if game_state == MENU:
        wait_to_start(selectorAnimationIndex)
        if areInstructionsVisible:
            show_instructions(keyIndex)
        menu_selector(keyIndex, selectorAnimationIndex)
        minigameTimeDifference = None
        minigameSeconds = None

    # when game state is not the menu state
    else:
        # checks if minigame count down reaches 0 to load minigame
        if currentTime - minigameStatTime > minigameSeconds * 1000:
            if lives != 0:
                load_minigame(game_state)

        # updates and counts down the seconds left of the current minigame
        minigameTimeDifference = currentTime - minigameStatTime

    # updates high score if greater than score
    if score > highScore:
        highScore = score

    # sets replay to true so menu is in replay mode when lives reach 0
    if lives <= 0:
        replay = True

        score = minigameSeconds = minigameTimeDifference = 0
        game_state = MENU

        if areInstructionsVisible:
            show_instructions(keyIndex)
        menu_selector(keyIndex, selectorAnimationIndex)

    # increments front bar animation index
    foreground_bar_animation_index -= 1

    # cycles and loops through the front bar, so it is constantly moving
    if foreground_bar_animation_index < -(60 + 51 + 128):
        foreground_bar_animation_index = 0

    # shows data only after game is started for the FIRST time
    if replay or game_state != MENU:
        show_data(lives, score, highScore, minigameTimeDifference, minigameSeconds, foreground_bar_animation_index)

    # updates parallax backgrounds
    # cycles and loops through each background, so they are constantly moving
    backgroundX -= 0.25

    if backgroundX < -WIDTH / 2:
        backgroundX = WIDTH / 2

    foregroundX -= 0.5

    if foregroundX < -WIDTH / 2:
        foregroundX = WIDTH / 2

    # shows a crack or two on the screen depending on lives
    if game_state != 0 and lives != 0 and lives != 3:
        if lives == 1:
            DISPLAY.blit(glassCrack1, glassCrack1Pos)
            DISPLAY.blit(glassCrack2, glassCrack2Pos)

        if lives == 2:
            DISPLAY.blit(glassCrack1, glassCrack1Pos)

    # toggles music being played
    if isMuted:
        pygame.mixer.music.pause()
        DISPLAY.blit(muteImg, (WIDTH - 48, 16))
    else:
        pygame.mixer.music.unpause()
        DISPLAY.blit(volumeImg, (WIDTH - 48, 16))

    # updates screen shake index and decreases it every time it is greater than 0
    if screen_shake_index > 0:
        screen_shake_index -= 1

    render_offset = [0, 0]
    if screen_shake_index:
        render_offset[0] = random.randint(0, 8) - 4
        render_offset[1] = random.randint(0, 8) - 4

    # draws everything drawn on the display, onto the screen window
    SCREEN.blit(DISPLAY, render_offset)

    # performance stuff
    pygame.display.flip()
    # updates display
    pygame.display.update()
# quits pygame when forever loop is broken
pygame.quit()
