import bpy

class OBJECT_PT_zTreeGenPanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_zTreeMainPanel"
    bl_label = "zTreePanel"
    bl_space_type = "VIEW_3D"   
    bl_region_type = "UI"
    bl_category = "zTree"  # note: replaced by preferences-setting in register function 
    bl_context = "objectmode" 

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        row = layout.row()
        row.label(text="zTree Settings")
        layout.prop(mytool, 'branch_vert_count')
        layout.prop(mytool, 'branch_scale')
        layout.prop(mytool, 'branch_falloff')
        layout.prop(mytool, 'branch_split_chance')
        layout.prop(mytool, 'number_of_leaves')
        layout.prop(mytool, 'iterations')
        layout.prop(mytool, 'grow_min')
        layout.prop(mytool, 'grow_max')
        layout.separator()
        layout.operator('object.ztreegenop')