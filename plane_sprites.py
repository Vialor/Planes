try:
    import sys
    import random
    # import math
    import os
    # import getopt
    import pygame
    # from socket import *
    from pygame.locals import *
    from resource_handler import *
except ImportError as e:
    print("couldn't load module. %s" % e)
    sys.exit(2)

SCREEN_RECT = pygame.Rect(0, 0, 400, 700)
FRAME_PER_SEC = 60
ANIMATION_CYCLE = 20
CREATE_ENEMY_EVENT = pygame.USEREVENT
HERO_FIRE_EVENT = pygame.USEREVENT + 1
CREATE_ENEMY2_EVENT = pygame.USEREVENT + 2
CREATE_ENEMY3_EVENT = pygame.USEREVENT + 3
SUPPLY_EVENT = pygame.USEREVENT + 4


class GameSprite(pygame.sprite.Sprite):
    def __init__(self, image_name, speed=1):
        super().__init__()
        self.image, self.rect = load_img(image_name)
        self.speed = speed

    def update(self):
        self.rect.y += self.speed


class Background(GameSprite):
    def __init__(self, is_alt=False):
        super().__init__("background.png")
        if is_alt:
            self.rect.y = -self.rect.height

    def update(self):
        super().update()
        if self.rect.y > SCREEN_RECT.height:
            self.rect.y = -self.rect.height


class Enemy(GameSprite):
    def __init__(self):
        speed = random.randint(1, 3)
        super().__init__("enemy1.png", speed)
        self.rect.bottom = 0
        max_x = SCREEN_RECT.width - self.rect.width
        self.rect.x = random.randint(0, max_x)

    def update(self):
        super().update()
        if self.rect.y > SCREEN_RECT.height:
            self.kill()

    def destroy(self):
        images = ["enemy1_down1.png", "enemy1_down2.png", "enemy1_down3.png", "enemy1_down4.png"]
        for i in images:
            self.image = load_img(i)[0]
            screen = pygame.display.set_mode(SCREEN_RECT.size)
            screen.blit(self.image, self.rect)
            pygame.display.update()
            pygame.time.delay(150)


# class Enemy2(GameSprite):
#
#
# class Enemy3(GameSprite):


class Hero(GameSprite):
    def __init__(self):
        super().__init__("me1.png", 0)
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom - 60
        self.bullets = pygame.sprite.Group()
        self.time = 0
        self.life = 1

    def update(self):
        images = ["me1.png", "me2.png"]
        self.time += 1
        if self.time % ANIMATION_CYCLE == 0:
            if self.time % (2*ANIMATION_CYCLE) == 0:
                self.image = load_img(images[0])[0]
            else:
                self.image = load_img(images[1])[0]

        self.rect.x += self.speed

        # stay in the screen
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.right > SCREEN_RECT.right:
            self.rect.right = SCREEN_RECT.right

    def fire(self):
        for i in (0, 1):
            bullet = Bullet()
            bullet.rect.bottom = self.rect.y - i * 20
            bullet.rect.centerx = self.rect.centerx

            self.bullets.add(bullet)

    def destroy(self):
        images = ["me_destroy_1.png", "me_destroy_2.png",
                  "me_destroy_3.png", "me_destroy_4.png"]
        for i in images:
            self.image = load_img(i)[0]
            # screen = pygame.display.set_mode(SCREEN_RECT.size)
            # screen.blit(self.image, self.rect)
            pygame.display.update()
            pygame.time.delay(50)


class Bullet(GameSprite):
    def __init__(self):
        super().__init__("bullet1.png", -2)

    def update(self):
        super().update()
        if self.rect.bottom < 0:
            self.kill()


class EnemyBullet(GameSprite):
    def __init__(self):
        super().__init__("bullet2.png", -2)

    def update(self):
        super().update()
        if self.rect.top > SCREEN_RECT.height:
            self.kill()
