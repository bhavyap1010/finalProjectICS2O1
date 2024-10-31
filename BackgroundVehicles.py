import pygame
import random

# SAME AS DUCKHUNT FILE BUT WITHOUT SINUSOIDAL MOVEMENT AND VARYING IMAGE FILES

vehicleImg = {
    "Police": pygame.image.load(f'Images/v-police.png'),
    "Red": pygame.image.load(f'Images/v-red.png'),
    "Truck": pygame.image.load(f'Images/v-truck.png'),
    "Yellow": pygame.image.load(f'Images/v-yellow.png')
}


class Vehicle:
    def __init__(self, x, y, xchange, vehicle, minigame_, width_, height_, screen):
        self.width, self.height, self.screen = width_, height_, screen

        self.xPos = x
        self.yPos = y
        self.xChange = xchange
        if vehicle == 1:
            self.w = 163
            self.h = 60
        elif vehicle == 2:
            self.w = 96
            self.h = 61
        elif vehicle == 3:
            self.w = 257
            self.h = 104
        elif vehicle == 4:
            self.w = 93
            self.h = 60
        else:
            self.w = None
            self.h = None

        if minigame_ != 1:
            self.w = self.w / 2
            self.h = self.h / 2

        self.vehicleType = vehicle

    def show(self):
        if self.vehicleType == 1:
            vehicle_img = vehicleImg["Police"]
        elif self.vehicleType == 2:
            vehicle_img = vehicleImg["Red"]
        elif self.vehicleType == 3:
            vehicle_img = vehicleImg["Truck"]
        elif self.vehicleType == 4:
            vehicle_img = vehicleImg["Yellow"]
        else:
            vehicle_img = vehicleImg["Police"]

        vehicle_img = pygame.transform.scale(vehicle_img, (self.w, self.h))
        if self.xChange > 0:
            vehicle_img = pygame.transform.flip(vehicle_img, True, False)
        else:
            vehicle_img = pygame.transform.flip(vehicle_img, False, False)
        self.screen.blit(vehicle_img, (self.xPos, self.yPos))

    def update(self):
        self.xPos += self.xChange
        if self.xChange > 0:
            if self.xPos > self.width:
                self.xPos = -self.w
        else:
            if self.xPos < -self.w:
                self.xPos = self.width


class BackgroundVehicles:
    def __init__(self, minigame_, width_, height_, screen):
        self.width, self.height, self.screen = width_, height_, screen

        global vehicleNum
        if minigame_ != 1:
            self.vehicleNum = 15
        else:
            self.vehicleNum = 5
        self.vehicles = []
        vehicle_index = 0

        while vehicle_index < self.vehicleNum:
            rand_vehicle = random.randint(1, 4)

            if bool(random.getrandbits(1)):
                x_change = 5
                x = random.randint(-self.width / 2, self.width / 2)

            else:
                x_change = -5
                x = random.randint(self.width / 2, self.width + self.width / 2)

            if rand_vehicle == 1:
                y = random.randint(0, self.height - 60)
            elif rand_vehicle == 2:
                y = random.randint(0, self.height - 61)
            elif rand_vehicle == 3:
                y = random.randint(0, self.height - 104)
            else:
                y = random.randint(0, self.height - 60)

            self.vehicles.append(Vehicle(x, y, x_change, rand_vehicle, minigame_, self.width, self.height, self.screen))
            vehicle_index += 1
