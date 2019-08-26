import pygame
from pygame.locals import *
import random

from res import Unit
from utils import KeyWrapper, Tick, RGBs
from settings import *
from core.effect import Effect, Dodge

class UnitRole(object):
    Player = "player"
    Enemy = "zoobie"
    Bullet = "bullet"

class Stamina(Tick):
    stock = 1

    def __init__(self):
        self.stock = Stamina.stock
        self.left = Stamina.stock
        self.interval = 10
        self.counter= 0

    def stat(self):
        return "[          ]" if self.left < 1 else "[Dodge]"

    def tryIncr(self):
        if self.left < self.stock:
            self.left += 1
            return True
        return False

    def tryCost(self):
        res = self.left > 0
        if res:
            self.left -= 1
        return res

    def tick(self, v):
        if self.left < self.stock:
            self.counter += v
        if self.counter >= self.interval:
            if self.tryIncr():
                self.counter -= self.interval
            else:
                self.counter = self.interval
    
    def dodge(self, u):
        d = None
        if self.tryCost():
            d = Dodge(u)
        return d

class Gun(Tick):
    bulletLife = 36 
    stockInterval = 24
    stock = 5

    def __init__(self):
        self.stock = Gun.stock
        self.left = Gun.stock
        self.interval = Gun.stockInterval
        self.bulletLife = Gun.bulletLife
        self.counter = 0

    def stat(self):
        return "{}{}".format(self.left * "|", (self.stock-self.left)*" ")

    def tryIncr(self):
        if self.left < self.stock:
            self.left += 1
            return True
        return False

    def tryCost(self):
        res = self.left > 0
        if res:
            self.left -= 1
        return res

    def tick(self, v):
        if self.left < self.stock:
            self.counter += v
        if self.counter >= self.interval:
            if self.tryIncr():
                self.counter -= self.interval
            else:
                self.counter = self.interval

    def fire(self, pos, dir, handler):
        b = None
        if self.tryCost():
            b = Bullet.default(pos, dir, self.bulletLife, handler)
        return b

class Player(Unit, KeyWrapper, Tick):
    MOVE = 0
    FIRE = 1
    width = 5
    height = 5
    interval = 4

    clothColor = (31,98,165)
    hairColor = (0,0,0)
    faceColor = (255,255,255)
    gunColor = (0,0,0)

    def __init__(self, pos, handler=None):
        super(Player, self).__init__(pos, Player.width, Player.height, handler)
        self.gun = Gun()
        self.stamina = Stamina()
        self.dir = None
        self.fireDir = K_RIGHT
        self.fill()
        self.left = 1
        self.opts = []
        self.his = {}
        self.interval = Player.interval
        self.counter = 0
        self.safe = False
        self.puncture = False
        self.bullets = []
        self.effects = []
        self.buffs = []
        
        self.clothColor = Player.clothColor

    def type():
        return UnitRole.Player

    def buffStat(self):
        b = None
        if len(self.buffs) > 0:
            b = self.buffs[0]
        return "[{}]".format("  " if b == None else b.time())

    def stat(self):
        return "{} - {} - {}".format(self.gun.stat(), self.stamina.stat(), self.buffStat())

    def setInterval(self, v):
        if self.interval != v:
            f = float(v)/float(self.interval)
            if f > 1.0:
                f = 1.0
            self.surf.set_alpha(int(255.0 * f))
            self.convert()
            self.interval = v

    def setSafe(self, v):
        if self.safe != v:
            self.safe = v

    def fill(self):
        if not self.surf:
            return self

        dm = {
            K_UP: [[(0,0), (5,2), Player.hairColor], [(0,2),(5,3), self.clothColor]],
            K_LEFT: [[(0,0), (5,2), Player.hairColor], [(0,1),(3,1), Player.faceColor], [(0,2),(5,3), self.clothColor], [(0,3),(1,1), Player.gunColor]],
            K_DOWN: [[(0,0), (5,2), Player.hairColor], [(1,1),(3,1), Player.faceColor], [(0,2),(5,3), self.clothColor], [(0,3),(3,1), Player.gunColor]],
            K_RIGHT: [[(0,0), (5,2), Player.hairColor], [(2,1),(3,1), Player.faceColor], [(0,2),(5,3), self.clothColor], [(2,3),(3,1), Player.gunColor]],
        }
        for r in dm.get(self.fireDir, []):
            rect = pygame.Rect(*r[:-1])
            self.surf.fill(r[-1], rect)
        self.convert()
        return self 

    def act(self, stopped):
        action = Player.MOVE
        for e in self.opts:
            key = 0
            if e.type in [KEYDOWN, KEYUP]:
                key = self.getKey(e.key)
            else:
                continue 
            if not self.his.get(key, None):
                self.his[key] = []
            if e.type == KEYDOWN:
                self.his[key] = [KEYDOWN]
                if key in [K_UP, K_DOWN, K_LEFT, K_RIGHT]:
                    self.dir = key 
                    if self.fireDir != key:
                        self.fireDir = key
                        self.fill()
                elif key == K_SPACE:
                    action = Player.FIRE
                elif key == K_LSHIFT:
                    d = self.stamina.dodge(self)
                    if d:
                        self.effects.append(d)
            elif e.type == KEYUP:
                self.his[key].append(KEYUP)
                if self.dir == key and not KEYDOWN in self.his[key]:
                    self.dir = None

        if not stopped:
            for e in self.effects:
                e.act(self)

        if action == Player.MOVE:
            if self.dir and self.tryCost():
                self.move(self.dir)
        else:
            if self.tryCost(-1):
                b = self.gun.fire(self.pos, self.fireDir, self.handler)
                if b:
                    self.bullets.append(b)

        if KEYUP in self.his.get(self.dir, []):
            self.dir = None
        self.opts = []

    def update(self, e):
        self.opts.append(e)

    def draw(self, screen, stopped):
        self.act(stopped)
        super(Player, self).draw(screen)

    def incr(self):
        if self.left < 1:
            self.left += 1
    
    def tryCost(self, min=0):
        res = self.left > min
        if res:
            self.left -= 1
        return res

    def getItem(self, i):
        e = i.effect(self)
        for ee in self.effects:
            if ee.type() == Effect.Skill:
                self.effects.append(ee)
        self.effects.append(e)
        self.buffs = [e]
        self.fill()

    def effectC(self):
        ne = []
        nb = []
        for e in self.effects:
            if e.life > 0:
                ne.append(e)
                if e.type() == Effect.Buff:
                    nb.append(e)
            else:
                e.restore(self)
                self.fill()
        self.effects = ne
        self.buffs = nb
    
    def updateDraw(self, screen):
        v = self.tick()
        if v:
            self.incr() 
            self.gun.tick(self.interval)
            self.stamina.tick(self.interval)
            self.effectC()

        self.draw(screen, False)
        if v:
            self.his = {}

    def bulletsUpdate(self):
        pass

    def bulletsDraw(self, screen):
        for b in self.bullets:
            b.draw(screen)

    def bulletsUpdateDraw(self, screen):
        nb = []
        for b in self.bullets:
            if b.life > 0:
                nb.append(b)
                b.updateDraw(screen)
        self.bullets = nb

    def shotting(self, e):
        nb = []
        shot = False
        for b in self.bullets:
            if b.samePos(e.pos) and not shot:
                shot = True
                if self.puncture:
                    nb.append(b)
            else:
                nb.append(b)
        self.bullets = nb
        return shot

class Enemies(object):
    width = 5
    height = 5
    
    def __init__(self, lf, m, color=(170,170,170), handler=None):
        self.lf = lf
        self.color = color
        self.handler = handler
        self.map = m
        self.units = []
        self.target = None

    def update(self, pc):
        self.target = pc.pos
        for e in self.units:
            e.update(self.target)

    def draw(self, screen):
        for e in self.units:
            e.draw(screen)

    def updateDraw(self, screen):
        if self.lf.tick():
            us = self.lf.units
            if len(self.units) < us:
                e = Enemy(self.map.ramPos(Enemies.width, Enemies.height), Enemies.width, Enemies.height, self.color, self.handler)
                e.update(self.target)
                self.units.append(e)

            nu = []
            for e in self.units:
                e.updateDraw(screen)
                if e.life > -1:
                    nu.append(e)
            self.units = nu
        else:
            self.draw(screen)

    def checksum(self, pc, ):
        nu = []
        for e in self.units:
            if e.reach(pc) and not pc.safe:
                return True, 0
            if not pc.shotting(e):
                nu.append(e)
        score = 100 * (len(self.units)-len(nu))
        self.units = nu
        return False, score

class Enemy(Unit):
    clothColor = (68,68,68)
    hairColor = (0,0,0)
    faceColor = (170,170,170)
    legColor = (255,0,0)

    def __init__(self, pos, width, height, color, handler=None):
        super(Enemy, self).__init__(pos, width, height, handler)
        self.render(color)
        self.dir = K_DOWN 
        self.fill()
        self.target = None
        self.life = enemyLife

    def fill(self):
        if not self.surf:
            return self

        dm = {
            K_UP: [[(0,0), (5,2), self.hairColor], [(0,2),(5,3), self.clothColor]],
            K_LEFT: [[(0,0), (5,2), self.hairColor], [(0,1),(3,1), self.faceColor], [(0,2),(5,3), self.clothColor], [(1,3),(1,2), self.legColor]],
            K_DOWN: [[(0,0), (5,2), self.hairColor], [(1,1),(3,1), self.faceColor], [(0,2),(5,3), self.clothColor], [(1,3),(1,2), self.legColor], [(3,3),(1,2), self.legColor]],
            K_RIGHT: [[(0,0), (5,2), self.hairColor], [(2,1),(3,1), self.faceColor], [(0,2),(5,3), self.clothColor], [(3,3),(1,2), self.legColor]],
        }
        for r in dm.get(self.dir, []):
            rect = pygame.Rect(*r[:-1])
            self.surf.fill(r[-1], rect)
        self.convert()
        return self 

    def type():
        return UnitRole.Enemy

    def update(self, pos):
        self.target = pos
    
    def _draw(self, screen):
        super(Enemy, self).draw(screen)

    def draw(self, screen):
        self._draw(screen)

    def catchTarget(self):
        x = self.pos[0] - self.target[0]
        y = self.pos[1] - self.target[1]
        ds = [K_UP if y > 0 else K_DOWN, K_LEFT if x > 0 else K_RIGHT]
        i = 0
        if y == 0:
            i = 1
        elif x != 0:
            i = random.randint(0, len(ds)-1)
        d = ds[i]
        if self.dir != d:
            self.dir = d
            self.fill()
        self.move(self.dir)
        self.life -= 1

    def updateDraw(self, screen):
        self.catchTarget()
        self._draw(screen)

class Bullet(Unit):
    backgound = mapGroundColor 
    main = (255,255,255)

    def __init__(self, pos, width, height, d, life, handler=None):
        super(Bullet, self).__init__(pos, width, height, handler)
        self.dir = d
        self.life = life
        self.fill()

    def fill(self):
        if not self.surf:
            return self

        bg = pygame.Rect((0,0), (self.width, self.height))
        self.surf.fill(Bullet.backgound, bg)
        # dm = {
        #     K_UP: [[(2,1), (1,2)], [(1,3),(1,1)], [(3,3),(1,1)]],
        #     K_LEFT: [[(1,2), (2,1)], [(3,1),(1,1)], [(3,3),(1,1)]],
        #     K_DOWN: [[(2,2), (1,2)], [(1,1),(1,1)], [(3,1),(1,1)]],
        #     K_RIGHT: [[(2,2), (2,1)], [(1,1),(1,1)], [(1,3),(1,1)]],
        # }
        dm = {
            K_UP: [[(2,1), (1,2)]],
            K_LEFT: [[(1,2), (2,1)]],
            K_DOWN: [[(2,2), (1,2)]],
            K_RIGHT: [[(2,2), (2,1)]],
        }

        for r in dm.get(self.dir, []):
            rect = pygame.Rect(*r)
            self.surf.fill(Bullet.main, rect)
        self.convert()
        return self

    def default(pos, d, life, handler):
        if not d:
            d = K_RIGHT
        w = 5
        h = 5
        if d == K_UP or d == K_DOWN:
            np = (pos[0], pos[1]-h) if d == K_UP else (pos[0], pos[1]+h)
        else:
            np = (pos[0]-w, pos[1]) if d == K_LEFT else (pos[0]+w, pos[1])

        b = Bullet((0,0), w, h, d, life, handler)
        b.pos = handler(b, np)
        return b

    def type():
        return UnitRole.Bullet

    def update(self):
        pass
    
    def updateDraw(self, screen):
        self.move(self.dir)
        self.life -= 1
        self.draw(screen)

    def samePos(self, pos):
        np = self.pos
        fp = self.moveChecked(np, self.dir)
        return self._samePos(np, pos) or self._samePos(fp, pos)