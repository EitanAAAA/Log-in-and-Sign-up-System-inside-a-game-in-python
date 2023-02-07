import pygame

class SpaceShip:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = pygame.image.load("pic/spaceship.png")
        self.speed = 3
        self.moving = False
        self._timer = 0
        self.score = "" # the final score, when the player reaching the finish line


    def draw(self, win, steroids, sound):
        self.move()
        self.collisonWithSteroids(steroids, sound)
        win.blit(self.img, (self.x, self.y))

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.y -= self.speed
            self.moving = True

        elif keys[pygame.K_s]:
            self.y += self.speed

        # check if the player reaching the finish line
        if self.y <= 0:
            self.moving = False
            self.score = str(self._timer)[0:5]


        if self.moving:
            self._timer += 0.017



    def collisonWithSteroids(self, steroids, sound):
        for s in steroids:
            if self.x + self.img.get_width() > s.x > self.x and self.y + self.img.get_height() > s.y > self.y:
                self.y = 500
                sound.play()

