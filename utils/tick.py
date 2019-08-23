class Tick(object):
    interval = 1.0
    counter = 0.0

    def tick(self, v=1):
        self.counter += v
        res = self.counter >= self.interval
        if res:
            self.counter -= self.interval
        return res
