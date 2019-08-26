import random
import pygame
from pygame.locals import *

from res import Unit
from utils import Tick
from settings import *

from core.effect import UnlimitStock, Puncture, LongRange, ShortStock

class BaseItem(Unit, Tick):
    width = 5
    height = 5
    layers = [[(0,0), (5,5)],[(1,1), (3,3)]]

    def __init__(self, pos, handler=None):
        super(BaseItem, self).__init__(pos, BaseItem.width, BaseItem.height, handler)
        self.life = itemLife
        self.interval = itemLife 

    def draw(self, screen):
        self.surf.set_alpha(int(255.0 * 0.5) if self.interval % 2 == 0 else 255)
        self.surf.convert()
        super(BaseItem, self).draw(screen)

    def updateDraw(self, screen):
        self.life -= 1
        self.interval -= 1
        self.draw(screen)

    def fill(self, bc, fc):
        if not self.surf:
            return self
        i = 0
        for l in BaseItem.layers:
            c = bc if i % 2 == 0 else fc
            rect = pygame.Rect(*l)
            self.surf.fill(c, rect)
            i += 1
        self.convert()
        return self
    
    def effect(self, u):
        return None

class UnlimitBullet(BaseItem):
    def __init__(self, pos, handler=None):
        super(UnlimitBullet, self).__init__(pos, handler)
        self.fill((255,255,255),UnlimitStock.color)

    def effect(self, u):
        return UnlimitStock(u)

class PunctureBullet(BaseItem):
    def __init__(self, pos, handler=None):
        super(PunctureBullet, self).__init__(pos, handler)
        self.fill((255,255,255),Puncture.color)

    def effect(self, u):
        return Puncture(u)

class LongRangeBullet(BaseItem):
    def __init__(self, pos, handler=None):
        super(LongRangeBullet, self).__init__(pos, handler)
        self.fill((255,255,255),LongRange.color)

    def effect(self, u):
        return LongRange(u)

class ShortStockBullet(BaseItem):
    def __init__(self, pos, handler=None):
        super(ShortStockBullet, self).__init__(pos, handler)
        self.fill((255,255,255),ShortStock.color)

    def effect(self, u):
        return ShortStock(u)

class Support(Tick):
    sp = 1
    ran = (0, 10)
    sran = (0, 3)
    step = 1

    def __init__(self):
        self.interval = 1
        self.counter = 0
        self.score = 0
        self.items = []
        self.p = Support.sp

    def support(self, m, u, score):
        ni = []
        for i in self.items:
            if i.life > 0:
                if i.reach(u):
                    u.getItem(i)
                else:
                    ni.append(i)
        self.items = ni

        if score - self.score > 200:
            self.score = score
            if self.tick():
                v = random.randint(*Support.ran)
                if v <= self.p:
                    self.p = Support.sp
                    self.items.append(self.newItem(m))
                else:
                    self.p += Support.step

    itemList = [UnlimitBullet, PunctureBullet, LongRangeBullet, ShortStockBullet]
    def newItem(self, m):
        return Support.itemList[random.randint(*Support.sran)](m.ramPos(BaseItem.width, BaseItem.height), m.calPos)

    def draw(self, screen):
        for i in self.items:
            i.draw(screen)

    def updateDraw(self, screen):
        for i in self.items:
            i.updateDraw(screen)

