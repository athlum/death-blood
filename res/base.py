import pygame
from pygame import sprite
from pygame.locals import *

from settings import *

class Base(sprite.Sprite):
    def __init__(self):
        self.surf = None
        self.blit = None
        self.rect = None
        self.pos = None
        return
    
    def isurf(self, s, pos):
        self.surf = s
        self.pos = pos
        return self

    def render(self, color):
        if not self.surf:
            return self
        self.surf.fill(color)
        self.convert()
        return self

    def set_palette(self, colors):
        if not self.surf:
            return self
        self.surf.set_palette(colors)
        self.convert()
        return self

    def convert(self):
        if not self.surf:
            return
        self.blit = self.surf.convert()
        self.rect = self.surf.get_rect()

    def draw(self, screen):
        if not self.blit:
            return
        screen.blit(self.blit, self.pos)

    def updateDraw(self, screen):
        self.draw(screen)

    def drawSurf(self, screen):
        if not self.surf:
            return
        screen.blit(self.surf, self.pos)