import pygame
from pygame import sprite
from pygame.locals import *

from settings import *
from res.base import Base

class Unit(Base):
    am = {
        K_UP: (0,-1),
        K_DOWN: (0,1),
        K_LEFT: (-1,0),
        K_RIGHT: (1,0),
    }

    def __init__(self, pos, width, height, handler=None):
        super(Unit, self).__init__()
        self.width = width 
        self.height = height
        self.surf = pygame.Surface((self.width,self.height))
        self.pos = pos
        self.step = unitStep
        self.handler = handler

    def setMove(self, v):
        self.step= v

    def _move(self, pos, k):
        t = self.am.get(k, (0,0))
        return (pos[0]+t[0]*self.step, pos[1]+t[1]*self.step) if t else pos

    def moveChecked(self, pos, k):
        pos = self._move(pos, k)
        return self.handler(self, pos) if self.handler else pos
    
    def move(self, k):
        self.pos = self.moveChecked(self.pos, k)

    def reach(self, u):
        return self.samePos(u.pos)
    
    def samePos(self, pos):
        return self._samePos(self.pos, pos)

    def _samePos(self, p1, p2):
        return p1[0] == p2[0] and p1[1] == p2[1]

        
