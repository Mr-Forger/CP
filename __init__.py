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
    "blender": (2, 80, 0),
    "location": "View3D > Tool Shelf > MeshMetry Tab",
    "description": "Add randomized geometry to a mesh",
    "warning": "This addon can be slow and use a lot of RAM, focus on your system resources with high numbers of iterations",
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


# UI
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
    bl_idname = "wm.meshmetry"
    bl_label = "Destroy Mesh"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):

        rmp = bpy.context.scene.rmprop

        def randomfloat(low, high):
            return random.random() * (high - low) + low

        def rsl(pct):
            if (4, 10, 0) > bpy.app.version:
                bpy.ops.mesh.select_random(percent=pct, seed=randint(1, 9999))
            else:
                bpy.ops.mesh.select_random(ratio=pct / 100, seed=randint(1, 9999))

        def rgs(pct, min, max):
            rsl(pct)
            for j in range(min, max):
                bpy.ops.mesh.select_more()

        def meshmetry(iter):
            opstart = time.time()  # 연산 시작

            boo = bpy.ops.object
            bom = bpy.ops.mesh

            print("Iterations: " + str(iter) + '\n' + "-------")

            if rmp.keep == True:
                boo.duplicate()

            boo.convert(target='MESH')

            # deselect
            boo.editmode_toggle()
            bom.select_mode(use_extend=False, use_expand=False, type=rmp.mode)
            bom.select_all(action='SELECT')



        def errmsg(message="", title="Message Box", icon='INFO'):

            def draw(self, context):
                self.layout.label(text=message)

            bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)

        if bpy.context.object.mode != 'OBJECT':
            errmsg("RandoMesh only works in object mode", "Uh Oh!", 'ERROR')
        else:
            meshmetry(rmp.iterations)

        return {'FINISHED'}


# 등록 및 실행
def register():
    bpy.utils.register_class(MeshMetryUiPanel)
    bpy.utils.register_class(MeshMetryOperator)
    bpy.utils.register_class(MeshMetryOperator)
    bpy.types.Scene.rmprop = PointerProperty(type=MeshMetryProp)


def unregister():
    bpy.utils.unregister_class(MeshMetryUiPanel)
    bpy.utils.unregister_class(MeshMetryOperator)
    bpy.utils.unregister_class(MeshMetryProp)
    del bpy.types.Scene.rmprop


if __name__ == "__main__":
    register()
