import pygame
from pygame.locals import *

import core

class State(object):
    Init = 0
    Running = 1
    Stopped = 2

class Manager(object):
    def __init__(self):
        self.core = core.Core(self)
        self.state = State.Init

    def run(self):
        while self.state != State.Stopped:
            self.core.frame()
        pygame.quit()

    def exit(self):
        self.state = State.Stopped