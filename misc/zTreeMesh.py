import bpy
import numpy as np

from .zBranch import zBranch
from .zPointCloud import zPointCloud

normalize = lambda v: v / np.sqrt(np.sum(np.array(v)**2))

class zTreeMesh:
    def __init__(self, num_vert = 10, leaves = 50, grow_min = 0.6, grow_max=5.0):
        self.points = []
        self.edges = []
        self.faces = []
        self.num_vert = num_vert
        self.branches = []
        self.cloud = zPointCloud(count=leaves)
        zBranch.reset()

        self.max_dist = grow_max
        self.min_dist = grow_min

    def finalize(self, context, name = 'zTree', col_name='Collection'):
        for b in self.branches:
            b.add_pos(self.points)
            b.add_edges(self.edges)

        mesh = bpy.data.meshes.new(name)
        obj = bpy.data.objects.new(mesh.name, mesh)
        col = bpy.data.collections.get(col_name)
        col.objects.link(obj)
        context.view_layer.objects.active = obj
        mesh.from_pydata(self.points, self.edges, self.faces)
    
        bpy.ops.object.modifier_add(type='SKIN')
        bpy.ops.object.modifier_add(type='SUBSURF')

        bpy.ops.object.mode_set(mode = 'EDIT') 
        bpy.ops.mesh.select_mode(type="VERT")
        bpy.ops.mesh.select_all(action = 'DESELECT')
        bpy.ops.object.mode_set(mode = 'OBJECT')

        for i in range(len(obj.data.vertices)):
            v = obj.data.vertices[i]
            v.select = True
            bpy.ops.object.mode_set(mode = 'EDIT') 
            for b in self.branches:
                if b.index == i:
                    self.scale_vert(b.scale)
            bpy.ops.mesh.select_all(action = 'DESELECT')
            bpy.ops.object.mode_set(mode = 'OBJECT')

        bpy.ops.object.mode_set(mode = 'EDIT') 
        bpy.ops.object.mode_set(mode = 'OBJECT')

        

    def scale_vert(self, scale):
        bpy.ops.transform.skin_resize(value=(scale, scale, scale), 
        orient_type='GLOBAL', 
        orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), 
        orient_matrix_type='GLOBAL', 
        mirror=False, 
        use_proportional_edit=False, 
        proportional_edit_falloff='SMOOTH', 
        proportional_size=1, 
        use_proportional_connected=False, 
        use_proportional_projected=False)


    def trunk(self, branch_scale = 3.0, branch_falloff = 0.9, split_chance = 0.15):
        self.branches.append(zBranch(scale = branch_scale, falloff=branch_falloff, split_chance=split_chance))

        current = self.branches[0]
        found = False
        while not found:
            for p in self.cloud.points:
                d = np.linalg.norm(np.subtract(current.pos, p))
                if d < self.max_dist:
                    found = True
            if not found:
                b = current.grow2()
                self.branches.append(b)
                current = b

    def grow2(self):
        for branch in self.branches:
            average_dir = [0, 0, 0]
            count = 0
            for leaf in self.cloud.points:
                direction = np.subtract(leaf, branch.pos)
                dist = np.linalg.norm(direction)
                if dist < self.min_dist:
                    pass
                elif dist > self.max_dist:
                    pass
                else:
                    average_dir = np.add(average_dir, dir)
            average_dir = [x/(count if count else 1) for x in average_dir]


    def grow(self):

        for leaf in self.cloud.points:
            closest_branch = None
            closest_dist = 10000000000.0
            closest_dir = None
            found = False
            for b in self.branches:
                dist = np.linalg.norm(np.subtract(leaf, b.pos))
                if dist < self.min_dist:
                    del leaf
                    closest_branch = None
                    found = True
                    break
                elif dist > self.max_dist:
                    pass
                elif not closest_branch or dist < closest_dist:
                    closest_branch = b
                    closest_dist = dist
                    closest_dir = np.subtract(leaf, closest_branch.pos)
                    closest_dir = normalize(closest_dir)
            
            if found: 
                continue

            if closest_branch:
                closest_branch.dir = normalize(np.add(closest_branch.dir, closest_dir))
                closest_branch.count += 1
            
        for b in self.branches:
            if b.count > 0:
                #b.dir = [x/b.count for x in b.dir]
                new_branch = b.grow2()
                self.branches.append(new_branch)
            b.count = 0

    def create(self, branch_scale = 3.0, branch_falloff = 0.9, split_chance = 0.15):
        last_b = None
        

        if 1:
            self.branches.append(zBranch(scale = branch_scale, falloff=branch_falloff, split_chance=split_chance))
            c = self.num_vert
            while c > 0:
                c -= self.branches[-1].grow(self.branches, self.cloud)

            return

        for i in range(self.num_vert):
            p = np.add(last_b.pos, [0,0,i*0.5]) if last_b else [0,0,0]
            p = np.add(p, self.cloud.pull(p))
            b = zBranch(pos=p, idx=i, prev=last_b, scale = branch_scale, falloff=branch_falloff)

            self.branches.append(b)
            last_b = b
