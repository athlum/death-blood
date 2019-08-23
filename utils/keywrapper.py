import pygame
from pygame.locals import *

class KeyWrapper(object):
    wrapMap = {
        K_w: K_UP,
        K_s: K_DOWN,
        K_a: K_LEFT,
        K_d: K_RIGHT, 
    }

    def getKey(self, key):
        return self.wrapMap.get(key, key)