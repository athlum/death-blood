import pygame
from pygame.locals import *

from settings import *
from res import Base, Text, Stat
from core.game import Game

class Core(object):
    def __init__(self, m):
        self.screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF)
        self.manager = m
        self.bg = Base().isurf(pygame.Surface(self.screen.get_size()),(0,0)).render((0,0,0))
        self.ms = [
            Game(),
        ]
        self.fps = fps
        self.clock = pygame.time.Clock()
        self.stat = Stat(self.clock, (0,255,0))

    def frame(self):
        self.emit(pygame.event.get())

    def emit(self, es):
        for s in self.ms:
            s.checksum()

        for e in es:
            if e.type == QUIT:
                self.manager.exit()

            for s in self.ms:
                s.emit(e)

        self.flip(self.clock.tick(self.fps))

    def flip(self, ms):
        self.stat.draw(self.screen)
        for s in self.ms:
            s.flip(self.screen, ms)
        pygame.display.flip()
        self.bg.draw(self.screen)
