import numpy as np

class zBranch:
    current_index = 0
    def __init__(self, pos=[0,0,0], idx = 0, prev = None, falloff = 0.9, scale = 2.0):
        self.pos = pos
        self.index = self.current_index
        zBranch.current_index += 1
        self.prev = prev
        self.falloff = falloff
        self.start_scale = scale

        self.scale = (prev.scale*falloff) if prev else scale

    @classmethod
    def reset(cls):
        cls.current_index = 0

    def add_pos(self, points):
        points.append(self.pos)

    def add_edges(self, edges):
        if not self.prev: return
        edges.append((self.index, self.prev.index))

    def grow(self, branches, cloud):
        from random import random
        res = 0
        if random() < 0.15:
            res = self.grow(branches, cloud)
        r = cloud.pull2(self.pos)
        b = zBranch(pos=np.add(r, self.pos), prev = self, falloff=self.falloff, scale=self.start_scale)
        branches.append(b)
        return 1 + res

    def create(self):
        pass
    