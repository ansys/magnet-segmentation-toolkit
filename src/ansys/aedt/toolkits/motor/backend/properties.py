"""Data classes used to store data related to Motor-CAD, AEDT and general settings.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import Dict
from typing import List


@dataclass(frozen=True)
class ElectroMagneticSettings:
    """Store electro magnetic settings."""

    nb_cuboids: int
    torque_cycles: int
    toque_points_per_cycle: int


@dataclass(frozen=True)
class LabSettings:
    """Store lab settings."""

    min_speed: int
    max_speed: int
    max_stator_current: int
    speed_step: int
    max_temp_stator_winding: int
    max_temp_magnet: int
    op_speed: int


@dataclass(frozen=True)
class MotorCADProperties:
    """Store Motor-CAD properties."""

    motorcad_file_path: str = ""
    vbs_file_path: str = ""
    emag_settings: ElectroMagneticSettings = ElectroMagneticSettings(6, 1, 30)
    lab_settings: LabSettings = LabSettings(0, 10000, 480, 500, 160, 140, 4500)


@dataclass(frozen=True)
class GeneralProperties:
    """Store general properties."""

    aedt_version: str = "2023.1"
    non_graphical: bool = False
    nb_core: int = 4
    active_project: str = ""
    active_design: Dict[str, str] = field(default_factory=dict)
    projects: List[str] = field(default_factory=list)
    designs_by_project_name: Dict[str, Dict[str, str]] = field(default_factory=dict)
    selected_process: int = 0
    use_grpc: bool = True
    is_toolkit_busy: bool = False
    url: str = "127.0.0.1"
    port: int = 5001
    debug: bool = True
    log_file: str = "backend.log"


@dataclass(frozen=True)
class AEDTProperties:
    """Store AEDT properties."""

    is_skewed: bool = False
    magnets_material: str = ""
    rotor_material: str = ""
    stator_material: str = ""
    rotor_slices: str = ""
    magnets_segments_per_slide: str = ""
    skew_angle: str = ""
    setup_to_analyze: str = "Setup1"


@dataclass(frozen=True)
class Properties:
    """Store all properties."""

    mcad_properties: MotorCADProperties = MotorCADProperties()
    general_properties: GeneralProperties = GeneralProperties()
    aedt_properties: AEDTProperties = AEDTProperties()


properties = Properties()
