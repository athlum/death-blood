class Effect(object):
    Skill = 0
    Buff = 1

class Dodge(object):
    sm = [3,1,1,1,3]
    def __init__(self, u):
        self.oriInterval = u.interval
        self.life = 3
        self.dead = False

    def type(self):
        return Effect.Skill

    def setInterval(self, u, v):
        u.setInterval(v)
        if self.life > 0 and self.life < 4:
            u.setSafe(True)
        else:
            u.setSafe(False)

    def restore(self, u):
        if not self.dead:
            self.setInterval(u, self.oriInterval)
            self.dead = True

    def act(self, u):
        if self.life <= 0:
            self.restore(u)
        else:
            self.setInterval(u, Dodge.sm[len(Dodge.sm)-self.life])
        self.life -= 1


class UnlimitStock(object):
    color = (255,0,0)

    def __init__(self, u):
        self.life = 12.5 * 60
        self.dead = False
        self.oriCloth = u.clothColor

    def type(self):
        return Effect.Buff

    def restore(self, u):
        u.clothColor = self.oriCloth

    def act(self, u):
        if self.life > 0:
            u.gun.left = u.gun.stock
            u.clothColor = UnlimitStock.color
        self.life -= 1

    def time(self):
        return int(self.life/12.5)

class Puncture(object):
    color = (139,0,255)

    def __init__(self, u):
        self.life = 12.5 * 60
        self.dead = False
        self.oriCloth = u.clothColor

    def type(self):
        return Effect.Buff

    def restore(self, u):
        u.puncture = False
        u.clothColor = self.oriCloth

    def act(self, u):
        if self.life > 0:
            u.puncture = True
            u.clothColor = Puncture.color
        else:
            self.restore(u)
        self.life -= 1

    def time(self):
        return int(self.life/12.5)

class LongRange(object):
    color = (160,82,45)

    def __init__(self, u):
        self.life = 12.5 * 60
        self.dead = False
        self.oriCloth = u.clothColor
        self.oriLife = u.gun.bulletLife

    def type(self):
        return Effect.Buff

    def restore(self, u):
        u.gun.bulletLife = self.oriLife
        u.clothColor = self.oriCloth

    def act(self, u):
        if self.life > 0:
            u.gun.bulletLife = self.oriLife * 2
            u.clothColor = LongRange.color
        else:
            self.restore(u)
        self.life -= 1

    def time(self):
        return int(self.life/12.5)

class ShortStock(object):
    color = (255,255,0)

    def __init__(self, u):
        self.life = 12.5 * 60
        self.dead = False
        self.oriCloth = u.clothColor
        self.oriInterval = u.gun.interval

    def type(self):
        return Effect.Buff

    def restore(self, u):
        u.gun.interval = self.oriInterval
        u.clothColor = self.oriCloth

    def act(self, u):
        if self.life > 0:
            u.gun.interval = self.oriInterval/2
            u.clothColor = ShortStock.color
        else:
            self.restore(u)
        self.life -= 1

    def time(self):
        return int(self.life/12.5)