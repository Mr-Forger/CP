import bpy
import time
import math
import random
from random import randint
from bpy.props import (IntProperty, FloatProperty, BoolProperty, EnumProperty, PointerProperty)
from bpy.types import (Panel, Operator, PropertyGroup)

bl_info = {
    "name": "MeshMetry",
    "author": "SeungHan Moon",
    "version": (0, 1, 1),
    "blender": (4, 00, 0),
    "location": "View3D > Tool Shelf > MeshMetry Tab",
    "description": "Add randomized geometry to a mesh",
    "warning": "This addon can be slow and use a lot of RAM, keep an eye on your system resources with high numbers of iterations",
    "category": "3D View",
}




class MeshMetryProp(PropertyGroup):
    keep: BoolProperty(
        name="Keep Original Mesh",
        description="Keep a copy of the source mesh",
        default=True,
        subtype='ANGLE'
    )

    mode: EnumProperty(
        name="Mode",
        description="Mesh Mode",
        items=[
            ('VERT', "Vertices", "Operate on vertices"),
            ('EDGE', "Edges", "Operate on edges"),
            ('FACE', "Faces", "Operate on faces")
        ],
        default='EDGE'
    )

    iterations: IntProperty(
        name="Iterations",
        description="MeshMetry Iterations",
        default=5,
        min=0,
        max=20,
        soft_max=10
    )

    subSmooth: FloatProperty(
        name="Subdivision Smooth:",
        description="Subdivision Smoothing",
        default=0,
        soft_min=0,
        max=1.0,
        precision=1
    )

    extrude: BoolProperty(
        name="Extrude Random",
        description="Enable Random Extrusion",
        default=True
    )

    extrudeMin: FloatProperty(
        name="Min:",
        description="Minimum Extrusion",
        default=-0.001,
        soft_min=-1.0,
        max=0.0,
        precision=3
    )

    extrudeMax: FloatProperty(
        name="Max:",
        description="Minimum Extrusion",
        default=0.001,
        soft_min=1.0,
        max=1.0,
        precision=3
    )

    poke: BoolProperty(
        name="Poke",
        description="Enable Random Poking",
        default=True
    )

    tri: BoolProperty(
        name="Triangulation",
        description="Enable Random Triangulation",
        default=True
    )

    decimate: BoolProperty(
        name="Decimation",
        description="Enable Random Decimation",
        default=True
    )

    smooth: BoolProperty(
        name="Smoothing",
        description="Enable Random Smoothing",
        default=True
    )

    wireframe: BoolProperty(
        name="Wireframe",
        description="Enable Wireframe",
        default=False
    )


#UI
class MeshMetryUiPanel(bpy.types.Panel):
    bl_label = "MeshMetry"
    bl_idname = "OBJECT_PT_meshmetry"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    # bl_context = "object"
    bl_category = "MeshMetry"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        col = layout.column(align=False)
        row = col.row(align=True)

        col.prop(scene.rmprop, "keep")

        col.separator()
        col.label(text="ITERATION OPTIONS")
        col.prop(scene.rmprop, "mode")
        col.prop(scene.rmprop, "iterations")
        col.prop(scene.rmprop, "subSmooth")
        col.separator()

        # extrude
        col.prop(scene.rmprop, "extrude")
        col = layout.column(align=True)
        if scene.rmprop.extrude == False:
            col.enabled = False
        col.prop(scene.rmprop, "extrudeMin")
        col.prop(scene.rmprop, "extrudeMax")

        # switch
        col = layout.column(align=False)
        col.prop(scene.rmprop, "poke")
        col.prop(scene.rmprop, "tri")
        col.separator()
        col.label(text="POST FX")
        col.prop(scene.rmprop, "decimate")
        col.prop(scene.rmprop, "smooth")
        col.prop(scene.rmprop, "wireframe")

        col.separator()
        sub = col.row()
        sub.scale_y = 2.0
        sub.operator("wm.meshmetry")

# 오퍼레이터
class MeshMetryOperator(bpy.types.Operator):