import numpy as np

class zBranch:
    current_index = 0
    def __init__(self, pos=[0,0,0], idx = 0, prev = None, dir = [0,0,1], falloff = 0.9, scale = 2.0, split_chance = 0.15):
        self.pos = pos
        self.index = self.current_index
        zBranch.current_index += 1
        self.prev = prev
        self.dir = dir
        self.falloff = falloff
        self.start_scale = scale
        self.split_chance = split_chance
        self.count = 0

        self.scale = (prev.scale*falloff) if prev else scale

    @classmethod
    def reset(cls):
        cls.current_index = 0

    def add_pos(self, points):
        points.append(self.pos)

    def add_edges(self, edges):
        if not self.prev: return
        edges.append((self.index, self.prev.index))

    def grow2(self):
        p = np.add(self.pos, self.dir)
        return zBranch(pos=p, prev=self, dir=self.dir, falloff=self.falloff, scale=self.start_scale, split_chance=self.split_chance)

    def grow(self, branches, cloud):
        from random import random
        res = 0
        if random() < 0.15:
            res = self.grow(branches, cloud)
        r = cloud.pull2(np.add(self.pos, self.dir))
        b = zBranch(pos = np.add(self.pos, self.dir), 
            dir=np.add(r, self.dir), 
            prev = self, 
            falloff=self.falloff, 
            scale=self.start_scale, 
            split_chance=self.split_chance)
        branches.append(b)
        return 1 + res

    def create(self):
        pass
    