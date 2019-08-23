import random
import pygame
from pygame.locals import *

from core.scope import Scope
from res import Base, Text
from core.unit import Player, Enemies
from utils import Tick
from settings import *

class State(object):
    Init = 0
    Running = 1
    Stopped = 2

class Game(Scope):
    def __init__(self):
        self.map = Map(width, height-30, pygame.Surface((width, height-30)), (0,15), mapGroundColor)
        self.state = State.Init
        self.stat = Stat(fontColor)
        self.info = Info(fontColor, (1, self.map.bottom+3))
        self.go = GameOver(titleColor)
        self.si = Start(titleColor)
        super(Game, self).__init__([
            self,
            self.info,
        ], 20)

    def running(self):
        return self.state == State.Running

    def emit(self, e):
        if e.type == KEYDOWN:
            if self.state == State.Stopped and e.key == K_r:
                self.init()
                self.state = State.Running
            elif self.state == State.Init:
                self.init()
                self.state = State.Running
        super(Game, self).emit(e)

    def init(self):
        self.pc = Player(self.map.ramPos(Player.width, Player.height), self.map.calPos)
        self.lf = LevelFactor()
        self.enemies = Enemies(self.lf, self.map, handler=self.map.calPos)
        self.stat.clear()

    def checksum(self):
        if self.state == State.Running:
            go, score = self.enemies.checksum(self.pc)
            if go:
                self.state = State.Stopped
            self.stat.score += score
            self.lf.cal(self.stat.score)

    def update(self, e):
        if self.running():
            self.pc.update(e)
            self.enemies.update(self.pc)
            self.pc.bulletsUpdate()

    def drawText(self, screen):
        if self.state == State.Stopped:
            self.go.draw(screen)
        elif self.state == State.Init:
            self.si.draw(screen)
        
        if self.state != State.Init:
            self.stat.draw(screen, [self.pc.stat(), self.lf.stat()])

    def updateDraw(self, screen):
        if self.running():
            self.map.updateDraw(screen)
            self.pc.updateDraw(screen)
            self.enemies.updateDraw(screen)
            self.pc.bulletsUpdateDraw(screen)
            self.drawText(screen)
        else:
            self.draw(screen)

    def draw(self, screen):
        self.map.draw(screen)
        if self.state != State.Init:
            self.pc.draw(screen)
            self.enemies.draw(screen)
            self.pc.bulletsDraw(screen)
        self.drawText(screen)

    def flip(self,screen, ms):
        if self.running():
            self.stat.calTime(ms)
        super(Game, self).flip(screen, ms)

class Info(Text):
    def __init__(self, color, pos):
        super(Info, self).__init__(color, pos)

    def draw(self, screen):
        super(Info, self).draw(screen, "Move - <W, A, S, D> Fire - <SPACE> Dodge - <LEFT SHIFT>")

class GameOver(Text):
    def __init__(self, color):
        super(GameOver, self).__init__(color, None)
        self.text = "You're dead, press <R> to retry..."

    def draw(self, screen):
        fw, fh = self.font.size(self.text)
        w, h = screen.get_size()
        self.pos = ((w-fw)//2, (h-fh)//2)
        super(GameOver, self).draw(screen, self.text)

class Start(GameOver):
    def __init__(self, color):
        super(Start, self).__init__(color)
        self.text = "Press any key to start..."

class Stat(Text):
    def __init__(self, color):
        super(Stat, self).__init__(color, (1,3))
        self.score = 0
        self.max = 7
        self.timems = 0

    def clear(self):
        self.score = 0
        self.timems = 0

    def calTime(self, ms):
        self.timems += ms

    def string(self):
        v = self.score-int(self.timems/timedelta)
        if v < 0:
            v = 0
        s = str(v)
        if len(s) > self.max:
            self.score = 0
            return self.string()
        
        return (self.max - len(s))*"0" + s

    def draw(self, screen, texts):
        sep = " "*3
        text = "{}{}{}".format(self.string(), sep, sep.join(texts))
        super(Stat, self).draw(screen, text)

class Map(Base):
    def __init__(self, width, height, surf, pos, color, detail=None):
        super(Map, self).__init__()
        self.isurf(surf, pos).render(color)
        self.width = width
        self.height = height
        self.top = 0 + pos[1]
        self.bottom = self.height + pos[1]
        self.left = 0 + pos[0]
        self.right = self.width + pos[0]
        self.detail = detail

    def _calPos(self, width, height, pos):
        np = [pos[0], pos[1]]
        if np[0] < self.left:
            np[0] = self.right- width
        elif np[0] > self.right - width:
            np[0] = self.left

        if np[1] < self.top:
            np[1] = self.bottom - height
        elif np[1] > self.bottom - height:
            np[1] = self.top

        return tuple(np)

    def calPos(self, u, pos):
        return self._calPos(u.width, u.height, pos)

    def ramPos(self, width, height):
        wc = self.width/width
        hc = self.height/height
        return self._calPos(width, height, (random.randint(0, wc)*width+self.left, random.randint(0, hc)*height+self.top))

class LevelFactor(Tick):
    def __init__(self, lu=1, mu=30, li=20, mi=3, sf=100):
        self.units = lu 
        self.maxUnit = mu
        self.interval = li 
        self.minInterval = mi
        self.scoreFactor = sf
        self.score = 0
        self.level = 1
        self.counter = 0

    def stat(self):
        return "Level - {}".format(self.level)

    def up(self):
        self.level += 1
        if self.units < self.maxUnit:
            self.units += (self.level-1) 
            if self.units > self.maxUnit:
                self.units = self.maxUnit
        if self.interval > self.minInterval and self.level % 2 == 0:
            self.interval -= self.level-3
            if self.interval < self.minInterval:
                self.interval = self.minInterval

    def cal(self, score):
        if (score-self.score)/self.scoreFactor>= self.level:
            self.score = score
            self.up()