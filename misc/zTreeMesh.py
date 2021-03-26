import bpy
import numpy as np

from .zBranch import zBranch
from .zPointCloud import zPointCloud

class zTreeMesh:
    def __init__(self, num_vert = 10):
        self.points = []
        self.edges = []
        self.faces = []
        self.num_vert = num_vert
        self.branches = []
        self.cloud = zPointCloud()
        zBranch.reset()

    def finalize(self, context, name = 'zTree', col_name='Collection'):
        print(self.edges)
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


    def create(self, branch_scale = 3.0, branch_falloff = 0.9):
        last_b = None
        

        if 1:
            self.branches.append(zBranch(scale = branch_scale, falloff=branch_falloff))
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
