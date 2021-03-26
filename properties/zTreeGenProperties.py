import bpy

from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       )

class zTreeGenProperties(bpy.types.PropertyGroup):
    branch_vert_count: IntProperty(
        name="branch vert count",
        description="the number of vertices for the tree",
        default=10,
        min=4,
        max=100
    )

    branch_falloff: FloatProperty(
        name="branch falloff",
        description="controls the size of the branch as it grows",
        default=0.9,
        min=0.1,
        max=3.0
    )
    
    branch_scale: FloatProperty(
        name="branch scale",
        description="controls the start size of the tree",
        default=3.0,
        min=0.1,
        max=10.0
    )

    branch_split_chance: FloatProperty(
        name="branch split chance",
        description="controls how often a branch will split",
        default=0.15,
        min=0.0,
        max=1.0
    )