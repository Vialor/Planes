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