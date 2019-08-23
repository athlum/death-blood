import pygame
from pygame import sprite
from pygame.locals import *

from settings import *
from res.base import Base

class Text(Base):
    def __init__(self, color, pos, font=None):
        super(Text, self).__init__()
        self.font = font or pygame.font.SysFont("mono", 14)
        self.pos = pos
        self.color = color
        self.display = True

    def setDisplay(val):
        self.display = val

    def draw(self, screen, text, color=None):
        if not self.display:
            return
        if color:
            self.color = color
        self.surf = self.font.render(text, True, self.color)
        super(Text, self).drawSurf(screen)


class Stat(Text):
    def __init__(self, clock, color, pos=None):
        super(Stat, self).__init__(color, pos)
        self.clock = clock

    def draw(self, screen):
        text = "FPS - {:6.3}".format(self.clock.get_fps())
        fw, fh = self.font.size(text)
        w, h = screen.get_size()
        self.pos = (w-fw-1, 3)
        super(Stat, self).draw(screen, text)
