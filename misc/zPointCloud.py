from random import *
import numpy as np

def rand_neg():
    return random()*2.0-1.0

class zPointCloud:
    def __init__(self, count=100, height=16.0, radius=5.0):
        self.count = count
        self.height = height
        self.radius = radius
        self.points = []

        for i in range(count):
            p = [rand_neg(), rand_neg(), rand_neg()]
            d = np.linalg.norm(p)
            p = [x * self.radius*random()/d for x in p]
            p[2] += height
            self.points.append(p)

    def pull1(self, pos):
        f = [[-(pos[i] - p[i])*random() for i in range(3)] for p in self.points]
        r = np.add.reduce(f)
        r = [x/np.linalg.norm(r) * 2.0  for x in r]
        return r

    def pull2(self, pos):
        ri = randrange(0,len(self.points))
        f = [-(pos[i] - self.points[ri][i])*random() for i in range(3)]
        #f = [[-(pos[i] - p[i])*random() for i in range(3)] for p in self.points]
        #r = np.add.reduce(f)
        r = [x/np.linalg.norm(f) * 2.0  for x in f]
        return r