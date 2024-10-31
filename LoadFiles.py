import pygame

# initializes pygame
pygame.init()
pygame.freetype.init()

# loads fonts
titleFont = pygame.freetype.Font('Fonts/FFF-Forward.TTF', 75)
dataFont = pygame.freetype.Font('Fonts/FFF-Forward.TTF', 20)
menuFont = pygame.freetype.Font('Fonts/FFF-Forward.TTF', 25)
howToPlayReturnFont = pygame.freetype.Font('Fonts/FFF-Forward.TTF', 30)

# plays music
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.load('Sounds/Synthetic Life.wav')
pygame.mixer.music.play(-1)

# loads sound files
selectSound = pygame.mixer.Sound('Sounds/Select_005.wav')
enterSound = pygame.mixer.Sound('Sounds/Pickup_005.wav')
fbFlySound = pygame.mixer.Sound('Sounds/Randomize9.wav')
fbExplosionSound = pygame.mixer.Sound('Sounds/Explosion_002.wav')
pongHitSound = pygame.mixer.Sound('Sounds/hit.wav')
osuHitSound = pygame.mixer.Sound('Sounds/Shoot_005.wav')
osuSelectSound = pygame.mixer.Sound('Sounds/Select_003.wav')
osuEnterSound = pygame.mixer.Sound('Sounds/Pickup_007.wav')
dhShotSound = pygame.mixer.Sound('Sounds/beam.wav')
dhExplosionSound = pygame.mixer.Sound('Sounds/explosion-16bit.wav')
siShot1Sound = pygame.mixer.Sound('Sounds/shot 1.wav')
siShot2Sound = pygame.mixer.Sound('Sounds/shot 2.wav')
siExplosionSound = pygame.mixer.Sound('Sounds/Explosion_003.wav')

# lowers volume
selectSound.set_volume(0.5)
enterSound.set_volume(0.5)
fbFlySound.set_volume(0.2)
fbExplosionSound.set_volume(0.5)
pongHitSound.set_volume(0.5)
osuHitSound.set_volume(0.5)
osuSelectSound.set_volume(0.5)
osuEnterSound.set_volume(0.5)
dhShotSound.set_volume(0.5)
dhExplosionSound.set_volume(0.5)
siShot1Sound.set_volume(0.5)
siShot2Sound.set_volume(0.5)
siExplosionSound.set_volume(0.5)

# constants that load images required within the loop
CONTROLS_IMAGE, RULES_IMAGE, GLASS_CRACK = pygame.image.load('Images/Ctrls.png'), pygame.image.load('Images/Rules.png'), pygame.image.load('Images/glassCrack.png')
BACK, MIDDLE, FRONT = pygame.image.load('Images/back.png'), pygame.image.load('Images/middle.png'), pygame.image.load('Images/front.png')
BG_BACK, BG_PLANET, BG_STARS = pygame.image.load('Images/bg-back.png'), pygame.image.load('Images/bg-planet.png'), pygame.image.load('Images/bg-stars.png')
SKYLINE, BUILDINGS, NEAR_BUILDINGS = pygame.image.load('Images/skyline.png'), pygame.image.load('Images/buildings-bg.png'), pygame.image.load('Images/near-buildings-bg.png')
FAR_BUILDINGS, BACK_BUILDINGS, FOREGROUND = pygame.image.load('Images/far-buildings.png'), pygame.image.load('Images/back-buildings.png'), pygame.image.load('Images/foreground.png')
BAR1, BAR2, BAR3 = pygame.image.load('Images/control-box-1.png'), pygame.image.load('Images/control-box-2.png'), pygame.image.load('Images/control-box-3.png')

selectorImg = []
for i in range(8):
    selectorImg.append(pygame.image.load(f'Images/turret-{i + 1}.png'))
