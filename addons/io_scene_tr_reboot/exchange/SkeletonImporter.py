import bpy
from typing import cast
from mathutils import Vector
from io_scene_tr_reboot.BlenderHelper import BlenderHelper
from io_scene_tr_reboot.BlenderNaming import BlenderNaming
from io_scene_tr_reboot.properties.BoneProperties import BoneProperties
from io_scene_tr_reboot.properties.ObjectProperties import ObjectProperties
from io_scene_tr_reboot.tr.Collection import Collection
from io_scene_tr_reboot.tr.Skeleton import ISkeleton
from io_scene_tr_reboot.util.Enumerable import Enumerable
from io_scene_tr_reboot.util.Serializer import Serializer
from io_scene_tr_reboot.util.SlotsBase import SlotsBase

class SkeletonImporter(SlotsBase):
    scale_factor: float

    def __init__(self, scale_factor: float) -> None:
        self.scale_factor = scale_factor

    def import_from_collection(self, tr_collection: Collection) -> bpy.types.Object | None:
        if bpy.context.object is not None:
            bpy.ops.object.mode_set(mode = "OBJECT")

        tr_skeleton = tr_collection.get_skeleton()
        if tr_skeleton is None or len(tr_skeleton.bones) == 0:
            return None

        armature_name = BlenderNaming.make_local_armature_name(tr_collection.name, tr_skeleton.id)

        bl_armature = bpy.data.armatures.new(armature_name)
        bl_armature.display_type = "STICK"

        bl_armature_obj = BlenderHelper.create_object(bl_armature)
        bl_armature_obj.show_in_front = True

        with BlenderHelper.enter_edit_mode():
            self.create_bones(bl_armature, tr_skeleton)

        self.assign_cloth_bones_to_group(bl_armature_obj, tr_skeleton)
        self.assign_counterparts(bl_armature_obj, tr_skeleton)
        self.assign_constraints(bl_armature_obj, tr_skeleton)
        self.assign_blend_shape_mappings(bl_armature_obj, tr_skeleton)

        return bl_armature_obj

    def create_bones(self, bl_armature: bpy.types.Armature, tr_skeleton: ISkeleton) -> None:
        bone_child_indices: list[list[int]] = []
        bone_heads: list[Vector] = []

        for i, tr_bone in enumerate(tr_skeleton.bones):
            bone_child_indices.append([])
            if tr_bone.parent_id < 0:
                bone_heads.append(tr_bone.relative_location * self.scale_factor)
            else:
                bone_heads.append(bone_heads[tr_bone.parent_id] + tr_bone.relative_location * self.scale_factor)
                bone_child_indices[tr_bone.parent_id].append(i)

        for i, tr_bone in enumerate(tr_skeleton.bones):
            bl_bone = bl_armature.edit_bones.new(BlenderNaming.make_bone_name(None, tr_bone.global_id, i))

            bl_bone.head = bone_heads[i]

            tail_offset: Vector
            if tr_bone.global_id is None:
                tail_offset = Vector((0, 0, 0.01))
            else:
                bone_length: float
                if len(bone_child_indices[i]) > 0:
                    avg_child_head = Enumerable(bone_child_indices[i]).avg(lambda idx: bone_heads[idx])
                    bone_length = (avg_child_head - bone_heads[i]).length
                else:
                    bone_length = tr_bone.distance_from_parent * self.scale_factor

                tail_offset = (tr_bone.absolute_orientation @ Vector((0, 0, 1))) * max(bone_length, 0.001)

            if tr_bone.parent_id < 0:
                bl_bone.tail = bl_bone.head + tail_offset
            else:
                bl_bone.parent = bl_armature.edit_bones[BlenderNaming.make_bone_name(None, tr_skeleton.bones[tr_bone.parent_id].global_id, tr_bone.parent_id)]
                tail1 = bl_bone.head + tail_offset
                tail2 = bl_bone.head - tail_offset
                if (tail1 - bone_heads[tr_bone.parent_id]).length > (tail2 - bone_heads[tr_bone.parent_id]).length:
                    bl_bone.tail = tail1
                else:
                    bl_bone.tail = tail2

    def assign_cloth_bones_to_group(self, bl_armature_obj: bpy.types.Object, tr_skeleton: ISkeleton) -> None:
        bl_armature = cast(bpy.types.Armature, bl_armature_obj.data)
        for i, tr_bone in enumerate(tr_skeleton.bones):
            if tr_bone.global_id is not None:
                continue

            bl_bone = bl_armature.bones[BlenderNaming.make_bone_name(None, None, i)]
            BlenderHelper.move_bone_to_group(bl_armature_obj, bl_bone, BlenderNaming.cloth_bone_group_name, BlenderNaming.cloth_bone_palette_name)

    def assign_counterparts(self, bl_armature_obj: bpy.types.Object, tr_skeleton: ISkeleton) -> None:
        bl_armature = cast(bpy.types.Armature, bl_armature_obj.data)
        for i, tr_bone in enumerate(tr_skeleton.bones):
            if tr_bone.counterpart_local_id is None:
                continue

            bone_name = BlenderNaming.make_bone_name(None, tr_bone.global_id, i)
            counterpart_bone_name = BlenderNaming.make_bone_name(None, tr_skeleton.bones[tr_bone.counterpart_local_id].global_id, tr_bone.counterpart_local_id)
            BoneProperties.get_instance(bl_armature.bones[bone_name]).counterpart_bone_name = counterpart_bone_name

    def assign_constraints(self, bl_armature_obj: bpy.types.Object, tr_skeleton: ISkeleton) -> None:
        bl_armature = cast(bpy.types.Armature, bl_armature_obj.data)
        for i, tr_bone in enumerate(tr_skeleton.bones):
            if len(tr_bone.constraints) == 0:
                continue

            bl_bone = bl_armature.bones[BlenderNaming.make_bone_name(None, tr_bone.global_id, i)]
            prop_constraints = BoneProperties.get_instance(bl_bone).constraints

            for tr_constraint in tr_bone.constraints:
                prop_constraint = prop_constraints.add()
                prop_constraint.data = tr_constraint.serialize()

            BlenderHelper.move_bone_to_group(bl_armature_obj, bl_bone, BlenderNaming.constrained_bone_group_name, BlenderNaming.constrained_bone_palette_name)

    def assign_blend_shape_mappings(self, bl_armature_obj: bpy.types.Object, tr_skeleton: ISkeleton) -> None:
        serialized_mappings = Serializer.serialize_dict(tr_skeleton.global_blend_shape_ids)
        ObjectProperties.get_instance(bl_armature_obj).skeleton.global_blend_shape_ids = serialized_mappings
