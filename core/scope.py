from utils import Tick

class Scope(Tick):
    def __init__(self, res, interval):
        self.res = res
        self.interval = interval
        self.counter = 0.0

    def checksum(self):
        pass

    def emit(self, e):
        for r in self.res:
            r.update(e)

    def flip(self, screen, ms):
        if self.tick(ms):
            for r in self.res:
                r.updateDraw(screen)
        else:
            for r in self.res:
                r.draw(screen)

    