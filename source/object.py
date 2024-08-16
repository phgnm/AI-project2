import pygame

class Pit:
    def __init__(self, x, y):
        self.is_discovered = None
        self.size = 10
        self.noti = [[False for i in range(self.size)] for j in range(self.size)]
        self.pit_pos = [[False for i in range(self.size)] for j in range(self.size)]
        for i in range(len(x)):
            self.pit_pos[x[i]][y[i]] = True

    def pit_discovered(self):
        self.is_discovered = True

    