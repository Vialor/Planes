#!/usr/bin/env python3
VERSION = "1.1"
from plane_sprites import *


class PlaneGame(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        self.clock = pygame.time.Clock()
        self.__create_sprites()
        pygame.display.set_caption("The Adventure of a Plane")
        pygame.time.set_timer(CREATE_ENEMY_EVENT, 1000)
        pygame.time.set_timer(HERO_FIRE_EVENT, 500)

    def __create_sprites(self):
        bg1 = Background()
        bg2 = Background(True)
        self.back_group = pygame.sprite.Group(bg1, bg2)

        self.enemy_group = pygame.sprite.Group()

        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)

    @staticmethod
    def __play_music(self):
        self.music = BGM();
        if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play()

    @staticmethod
    def __game_over():
        print('game over')
        pygame.quit()
        exit()

    def __event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or\
                    (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.__game_over()
            elif event.type == CREATE_ENEMY_EVENT:
                enemy = Enemy()
                self.enemy_group.add(enemy)
            elif event.type == HERO_FIRE_EVENT:
                self.hero.fire()

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_RIGHT]:
            self.hero.speed = 2
        elif keys_pressed[pygame.K_LEFT]:
            self.hero.speed = -2
        else:
            self.hero.speed = 0

    def __check_collide(self):
        # bullets hit enemies
        pygame.sprite.groupcollide(self.hero.bullets, self.enemy_group, True, True)
        # hero crashes into enemies
        enemies = pygame.sprite.spritecollide(self.hero, self.enemy_group, True)
        if enemies:
            self.hero.destroy()
            self.hero.kill()
            self.__game_over()

    def __update_sprites(self):
        self.back_group.update()
        self.back_group.draw(self.screen)

        self.enemy_group.update()
        self.enemy_group.draw(self.screen)

        self.hero_group.update()
        self.hero_group.draw(self.screen)

        self.hero.bullets.update()
        self.hero.bullets.draw(self.screen)

    def start_game(self):
        print('start game')
        while True:
            self.clock.tick(FRAME_PER_SEC)
            # self.__play_music()
            self.__event_handler()
            self.__check_collide()
            self.__update_sprites()
            pygame.display.update()


if __name__ == '__main__':
    game = PlaneGame()
    game.start_game()
