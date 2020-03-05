try:
    import sys
    import os
    import pygame
    from pygame.locals import *
    from pygame.compat import geterror
except ImportError as e:
    print("couldn't load module. %s" % e)
    sys.exit(2)

main_dir = os.path.split(os.path.abspath(__file__))[0]
img_dir = os.path.join(main_dir, "images")
msc_dir = os.path.join(main_dir, "music")


def load_img(name):
    fullname = os.path.join(img_dir, name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error:
        print("Cannot load image:", fullname)
        raise SystemExit(str(geterror()))
    return image, image.get_rect()


def load_music(name):
    class NoneMusic:
        def play(self):
            pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneMusic()
    fullname = os.path.join(msc_dir, name)
    try:
        pygame.mixer.music.load(fullname)
    except pygame.error:
        print("Cannot load sound: %s" % fullname)
        raise SystemExit(str(geterror()))

# TODO pause music

class sound():
    pass
