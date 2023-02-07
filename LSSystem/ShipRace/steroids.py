import pygame
import random
from ShipRace.data import *

class Steroids:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = random.randint(2,5)
        self.radius = 5
        self.dir = random.choice(["right","left"])

    def update(self):
        self.speed = random.randint(2, 5)
        self.x = random.randint(0,WIDTH)
        self.y = random.randint(0, HEIGHT-150)
        self.dir = random.choice(["right","left"])

    def draw(self, win):
        self.move()
        pygame.draw.circle(win, WHITE, (int(self.x), self.y), self.radius)

    def move(self):
        if self.x <= 0:
            self.update()
            self.x = WIDTH
            self.dir = "left"

        elif self.x >= WIDTH:
            self.update()
            self.x -= self.speed
            self.x = 0
            self.dir = "right"

        # movement by location
        if self.dir == "right":
            self.x += self.speed

        elif self.dir == "left":
            self.x -= self.speed


steroids_list = []
for i in range(15):
    steroids_list.append(Steroids(random.randint(0,WIDTH), random.randint(0, HEIGHT-150)))