from abc import abstractmethod
from typing import ClassVar, NamedTuple, Protocol
from mathutils import Vector
from io_scene_tr_reboot.tr.Collision import Collision
from io_scene_tr_reboot.tr.ResourceBuilder import ResourceBuilder
from io_scene_tr_reboot.tr.ResourceReader import ResourceReader
from io_scene_tr_reboot.tr.ResourceReference import ResourceReference
from io_scene_tr_reboot.util.SlotsBase import SlotsBase

class ClothMassAnchorBone(NamedTuple):
    local_bone_id: int
    offset: Vector

class ClothMassSpringVector(NamedTuple):
    spring_idx: int
    vector: Vector

class ClothMass(SlotsBase):
    local_bone_id: int
    position: Vector
    mass: float
    anchor_local_bones: list[ClothMassAnchorBone]
    spring_vectors: list[ClothMassSpringVector]
    bounceback_factor: float

    def __init__(self, local_bone_id: int, position: Vector) -> None:
        self.local_bone_id = local_bone_id
        self.position = position
        self.mass = 1.0
        self.anchor_local_bones = []
        self.spring_vectors = []
        self.bounceback_factor = 0

class ClothSpring(SlotsBase):
    mass_1_idx: int
    mass_2_idx: int
    stretchiness: float

    def __init__(self, mass_1_idx: int, mass_2_idx: int, stretchiness: float) -> None:
        self.mass_1_idx = mass_1_idx
        self.mass_2_idx = mass_2_idx
        self.stretchiness = stretchiness

class ClothStrip(SlotsBase):
    id: int
    parent_bone_local_id: int
    masses: list[ClothMass]
    springs: list[ClothSpring]
    collisions: list[Collision]

    gravity_factor: float
    wind_factor: float
    pose_follow_factor: float
    rigidity: float
    mass_bounceback_factor: float
    drag: float

    def __init__(self, id: int, parent_bone_local_id: int) -> None:
        self.id = id
        self.parent_bone_local_id = parent_bone_local_id
        self.masses = []
        self.springs = []
        self.collisions = []

        self.gravity_factor = 1
        self.wind_factor = 1
        self.pose_follow_factor = 0
        self.rigidity = 0
        self.mass_bounceback_factor = 0
        self.drag = 0

class ClothFeatureSupport(NamedTuple):
    strip_pose_follow_factor: bool
    mass_specific_bounceback_factor: bool
    spring_specific_stretchiness: bool

class Cloth(SlotsBase):
    supports: ClassVar[ClothFeatureSupport]

    definition_id: int
    tune_id: int
    strips: list[ClothStrip]

    def __init__(self, definition_id: int, tune_id: int) -> None:
        self.definition_id = definition_id
        self.tune_id = tune_id
        self.strips = []

    @abstractmethod
    def read(self, definition_reader: ResourceReader, tune_reader: ResourceReader, global_bone_ids: list[int | None], external_collisions: list[Collision]) -> None: ...

    @abstractmethod
    def write(self, definition_writer: ResourceBuilder, tune_writer: ResourceBuilder, global_bone_ids: list[int | None]) -> None: ...





class IClothDef(Protocol):
    strips_ref: ResourceReference | None
    num_strips: int

class IClothDefStrip(Protocol):
    id: int
    masses_ref: ResourceReference | None
    springs_ref: ResourceReference | None
    parent_bone_local_id: int
    num_masses: int
    num_springs: int
    max_rank: int

class IClothDefMass(Protocol):
    position: Vector
    anchor_bones_ref: ResourceReference | None
    num_anchor_bones: int
    spring_vector_array_ref: ResourceReference | None
    local_bone_id: int
    mass: int
    bounce_back_factor: int
    rank: int

class IClothDefAnchorBone(Protocol):
    offset: Vector
    weight: float
    local_bone_id: int

class IClothDefSpring(Protocol):
    rest_length: float
    mass_1_idx: int
    mass_2_idx: int
    stretchiness_interpolation_value: float

class IClothTune(Protocol):
    enabled: int
    inner_distance: float
    outer_distance: float
    configs_ref: ResourceReference | None
    num_configs: int
    strip_groups_ref: ResourceReference | None
    num_strip_groups: int
    collision_groups_ref: ResourceReference | None
    num_collision_groups: int
    flammable: int
    num_flammable_configs: int
    flammable_configs_ref: ResourceReference | None

class IClothTuneConfig(Protocol):
    num_strip_group_indices: int
    strip_group_indices_ref: ResourceReference | None

class IClothTuneStripGroup(Protocol):
    gravity_factor: float
    buoyancy: float
    drag: float
    max_velocity_update_iterations: int
    max_position_update_iterations: int
    relaxation_iterations: int
    sub_step_count: int
    wind_factor: float
    wind_on_constraints: int
    max_mass_bounceback_factor: float
    pose_follow_factor: float
    transform_type: int
    spring_stretchiness_default_percentage: int
    spring_stretchiness_lower_percentage: int
    spring_stretchiness_upper_percentage: int
    rigidity_percentage: int
    acceleration_divider: float
    time_delta_multiplier: float
    reference_time_delta_multiplier: float
    num_strip_ids: int
    strip_ids_ref: ResourceReference | None
    num_collision_group_indices: int
    collision_group_indices_ref: ResourceReference | None

class IClothTuneCollisionGroup(Protocol):
    count: int
    items_ref: ResourceReference | None

class IClothTuneCollisionKey(Protocol):
    type: int
    hash_data_1: int
    hash_data_2: int
    remaining_hash_data_ref: ResourceReference | None
