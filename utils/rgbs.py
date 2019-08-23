class RGBs(object):
    def __init__(self, rgbcs):
        self.colors = []
        for rgbc in rgbcs:
            rgb = rgbc[:-1]
            for i in range(rgbc[-1]):
                self.colors.append(rgb)
    
    def list(self):
        return self.colors