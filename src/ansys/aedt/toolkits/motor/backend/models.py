"""Data classes used to store data related to various settings.

The settings include common AEDT toolkit settings and settings associated
to motor workflows in AEDT.
"""
import json
import os
from typing import Literal

from pydantic import BaseModel

from ansys.aedt.toolkits.motor.backend.common.models import CommonProperties


class AEDTProperties(BaseModel):
    """Store AEDT properties."""

    motor_type: Literal["", "IPM", "SPM"] = ""
    is_skewed: bool = False
    apply_mesh_sheets: bool = False
    magnets_material: str = ""
    rotor_material: str = ""
    stator_material: str = ""
    rotor_slices: int = 0
    magnets_segments_per_slide: int = 0
    mesh_sheets_number: int = 0
    skew_angle: str = ""
    setup_to_analyze: str = "Setup1"


class Properties(CommonProperties, AEDTProperties, validate_assignment=True):
    """Store all properties."""

    pass


aedt_kwargs = {}
if os.path.expanduser(os.path.join(os.path.dirname(__file__), "aedt_properties.json")):
    with open(os.path.join(os.path.dirname(__file__), "aedt_properties.json")) as file_handler:
        aedt_properties = json.load(file_handler)

common_kwargs = {}
if os.path.expanduser(os.path.join(os.path.dirname(__file__), "common_properties.json")):
    with open(os.path.join(os.path.dirname(__file__), "common_properties.json")) as file_handler:
        common_kwargs = json.load(file_handler)

properties = Properties(**common_kwargs, **aedt_kwargs)
