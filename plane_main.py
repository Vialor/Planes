#!/usr/bin/env python3
VERSION = "1.1"
from plane_sprites import *


class PlaneGame(object):
    def __init__(self):
        pygame.init()

        # music
        pygame.mixer.init()
        load_music("Paper Plane's Adventure.mp3")

        # font
        self.font = pygame.font.SysFont('comicsans', 30, True)  # handle exception?
        self.score = 0

        # objects
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        self.__create_sprites()

        # time
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Paper Plane's Adventure")
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
    def __play_music():
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
        # bullets hit enemy
        bullet_hit_enemy = pygame.sprite.groupcollide(self.enemy_group, self.hero.bullets, False, True)
        for key in bullet_hit_enemy:
            if key.isAlive:
                self.score += 1
                key.isAlive = False
        # TODO bullets hit enemy2
        # TODO bullets hit enemy3
        # TODO bullets hit hero
        hero_hit_enemy = pygame.sprite.spritecollide(self.hero, self.enemy_group, True)
        if hero_hit_enemy:
            self.hero.life -= 1
        if self.hero.life == 0:
            self.hero.isAlive = False

    def __update_sprites(self):
        # objects
        self.back_group.update()
        self.back_group.draw(self.screen)

        self.enemy_group.update()
        self.enemy_group.draw(self.screen)

        self.hero_group.update()
        self.hero_group.draw(self.screen)

        self.hero.bullets.update()
        self.hero.bullets.draw(self.screen)

        # text
        score_text = self.font.render("score: " + str(self.score), 1, (0, 0, 0))
        life_text = self.font.render("X " + str(self.hero.life), 1, (0, 0, 0))
        self.screen.blit(score_text, (10, 10))
        life_img = load_img("life.png")[0]
        self.screen.blit(life_img, (10, 600))
        self.screen.blit(life_text, (60, 625))

    def start_game(self):
        while True:
            self.clock.tick(FRAME_PER_SEC)
            self.__play_music()
            self.__event_handler()
            self.__check_collide()
            self.__update_sprites()
            pygame.display.update()


if __name__ == '__main__':
    game = PlaneGame()
    game.start_game()
