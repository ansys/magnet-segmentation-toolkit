"""Data classes used to store data related to various settings.

The settings include common AEDT toolkit settings and settings associated
to motor workflows in AEDT.
"""
from dataclasses import dataclass
import json
import os

from ansys.aedt.toolkits.motor.backend.common.properties import CommonProperties


@dataclass()
class AEDTProperties:
    """Store AEDT properties."""

    motor_type: str = ""
    is_skewed: bool = False
    magnets_material: str = ""
    rotor_material: str = ""
    stator_material: str = ""
    rotor_slices: str = ""
    magnets_segments_per_slide: str = ""
    skew_angle: str = ""
    setup_to_analyze: str = "Setup1"


# FIXME: singleton
@dataclass()
class Properties:
    """Store all properties."""

    common_properties: CommonProperties
    aedt_properties: AEDTProperties

    def update(self, key, value) -> None:
        for properties in [self.common_properties, self.aedt_properties]:
            try:
                setattr(properties, key, value)
                break
            except AttributeError:
                continue


aedt_kwargs = {}
if os.path.expanduser(os.path.join(os.path.dirname(__file__), "aedt_properties.json")):
    with open(os.path.join(os.path.dirname(__file__), "aedt_properties.json")) as file_handler:
        aedt_properties = json.load(file_handler)
aedt_properties = AEDTProperties(**aedt_kwargs)

common_kwargs = {}
if os.path.expanduser(os.path.join(os.path.dirname(__file__), "common_properties.json")):
    with open(os.path.join(os.path.dirname(__file__), "common_properties.json")) as file_handler:
        common_kwargs = json.load(file_handler)

common_properties = CommonProperties(**common_kwargs)

properties = Properties(common_properties, aedt_properties)
