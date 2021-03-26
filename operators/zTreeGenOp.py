import bpy

from zTreeGen.misc.zTreeMesh import zTreeMesh
from zTreeGen.misc.zBranch import zBranch

class ZTreeGenOpOperator(bpy.types.Operator):
    bl_idname = "object.ztreegenop"
    bl_label = "zTreeGenOp"

    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool

        tree = zTreeMesh(num_vert=mytool.branch_vert_count)

        tree.create(branch_falloff=mytool.branch_falloff, branch_scale=mytool.branch_scale)

        tree.finalize(context)

        return {'FINISHED'}
