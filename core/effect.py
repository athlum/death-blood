class Effect(object):
    Skill = 0
    Buff = 1

class Dodge(object):
    sm = [3,1,1,1,3]
    def __init__(self, u):
        self.oriInterval = u.interval
        self.life = 3

    def type(self):
        return Effect.Skill

    def setInterval(self, u, v):
        u.interval = v
        if self.life > 0 and self.life < 4:
            u.safe = True
        else:
            u.safe = False

    def restore(self, u):
        if self.life < 0:
            return
        self.setInterval(u, self.oriInterval)

    def act(self, u):
        if self.life <= 0:
            self.restore(u)
        else:
            self.setInterval(u, Dodge.sm[len(Dodge.sm)-self.life])
        self.life -= 1
