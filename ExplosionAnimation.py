import pygame

# initializes mixer
pygame.mixer.init()

# loads the sounds
fbExplosionSound = pygame.mixer.Sound('Sounds/Explosion_002.wav')
pongHitSound = pygame.mixer.Sound('Sounds/hit.wav')
osuExplosionSound = pygame.mixer.Sound('Sounds/explosion-soft.wav')
dhExplosionSound = pygame.mixer.Sound('Sounds/explosion-16bit.wav')
siPortalSound = pygame.mixer.Sound('Sounds/Jump_004.wav')
siExplosionSound = pygame.mixer.Sound('Sounds/Explosion_003.wav')

# lowers volume
fbExplosionSound.set_volume(0.2)
pongHitSound.set_volume(0.2)
osuExplosionSound.set_volume(0.2)
dhExplosionSound.set_volume(0.2)
siPortalSound.set_volume(0.2)
siExplosionSound.set_volume(0.2)

fbExplosionImg = []
for i in range(12):
    fbExplosionImg.append(pygame.image.load(f'Images/Explosions/fb-explosion-{i + 1}.png'))

pongExplosionImg = []
for i in range(3):
    pongExplosionImg.append(pygame.image.load(f'Images/Explosions/shot-hit-{i + 1}.png'))

osuExplosionImg = []
for i in range(23):
    osuExplosionImg.append(pygame.image.load(f'Images/Explosions/asteroid-explosion-{i + 1}.png'))

dhExplosionImg = []
for i in range(5):
    dhExplosionImg.append(pygame.image.load(f'Images/Explosions/explosion{i + 1}.png'))

siExplosionImg = []
for i in range(6):
    siExplosionImg.append(pygame.image.load(f'Images/Explosions/enemy-explosion-{i + 1}.png'))

siPortalImg = []
for i in range(5):
    siPortalImg.append(pygame.image.load(f'Images/Explosions/mirror-{i + 1}.png'))


# explosion pygame sprite class
class ExplosionAnimation(pygame.sprite.Sprite):
    # init parameters for position and minigame and explosion size
    def __init__(self, x, y, minigame_, explosion_size_):
        pygame.sprite.Sprite.__init__(self)
        self.animationFrames = []

        # sets the number of sprites to animate through depending on minigame
        if minigame_ == 1:
            animation_num = 12

        elif minigame_ == 2:
            animation_num = 3

        elif minigame_ == 3:
            animation_num = 23

        elif minigame_ == 4:
            animation_num = 5

        elif minigame_ == 5:
            animation_num = 6

        else:
            animation_num = 5

        # animates through explosion
        for animation_num_index in range(animation_num):

            if minigame_ == 1:
                img = fbExplosionImg[animation_num_index]
                img = pygame.transform.scale(img, (explosion_size_, explosion_size_))

            elif minigame_ == 2:
                img = pongExplosionImg[animation_num_index]
                img = pygame.transform.scale(img, (explosion_size_, explosion_size_))

            elif minigame_ == 3:
                img = osuExplosionImg[animation_num_index]
                img = pygame.transform.scale(img, (explosion_size_, explosion_size_))

            elif minigame_ == 4:
                img = dhExplosionImg[animation_num_index]
                img = pygame.transform.scale(img, (explosion_size_, explosion_size_))

            elif minigame_ == 5:
                img = siExplosionImg[animation_num_index]
                img = pygame.transform.scale(img, (explosion_size_, explosion_size_))

            else:
                img = siPortalImg[animation_num_index]
                img = pygame.transform.scale(img, (36, 117))

            self.animationFrames.append(img)

        # initializes sprite and animation variables
        self.animationFrameIndex = 0
        self.image = self.animationFrames[self.animationFrameIndex]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.animationSpeedIndex = 0

    def update(self, lives_, mingame_):

        # sets explosion speed
        if mingame_ == 1:
            animation_speed = 3
        elif mingame_ == 2:
            animation_speed = 5
        elif mingame_ == 3:
            animation_speed = 2
        elif mingame_ == 4:
            animation_speed = 3
        elif mingame_ == 5:
            animation_speed = 3
        else:
            animation_speed = 2

        # cycles through animation index
        self.animationSpeedIndex += 1

        # plays sound when explosion called
        if mingame_ == 3:
            if self.animationFrameIndex == 13:
                osuExplosionSound.play()

        if mingame_ == 5:
            siPortalSound.play()

        # animates while there are still sprites to animate through, upon when it runs out it kills the sprite and stops the animation
        if self.animationSpeedIndex >= animation_speed:
            if self.animationFrameIndex < len(self.animationFrames) - 1:
                self.animationSpeedIndex = 0
                self.animationFrameIndex += 1
                self.image = self.animationFrames[self.animationFrameIndex]

            if self.animationFrameIndex >= len(self.animationFrames) - 1:
                self.kill()
