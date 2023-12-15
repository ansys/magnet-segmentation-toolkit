"""Data classes used to store data related to Motor-CAD, AEDT and general settings.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import Dict
from typing import List


@dataclass()
class GeneralProperties:
    """Store general properties."""

    aedt_version: str = "2023.2"
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
    log_file: str = "motor_backend.log"


@dataclass()
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


@dataclass()
class Properties:
    """Store all properties."""

    general_properties: GeneralProperties = GeneralProperties()
    aedt_properties: AEDTProperties = AEDTProperties()

    def update(self, key, value):
        for properties in [self.general_properties, self.aedt_properties]:
            try:
                setattr(properties, key, value)
                break
            except AttributeError:
                continue


properties = Properties()
