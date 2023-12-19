# """Data classes used to store data related to various settings.

# The settings include common AEDT toolkit settings and settings associated
# to motor workflows in AEDT.
# """
# import json
# import os

# # from dataclasses import dataclass
# from typing import Literal

# # from pydantic.dataclasses import dataclass
# from pydantic import BaseModel, ValidationError

# # from abc import ABC
# from ansys.aedt.toolkits.motor.backend.common.models import CommonProperties

# # from pydantic import Field


# # @dataclass()
# class AEDTProperties(BaseModel):
#     """Store AEDT properties."""

#     # motor_type: str = ""
#     motor_type: Literal["", "IPM", "SPM"] = ""
#     is_skewed: bool = False
#     magnets_material: str = ""
#     rotor_material: str = ""
#     stator_material: str = ""
#     # FIXME: use int instead of str for rotor_slices
#     rotor_slices: str = ""
#     # FIXME: use int instead of str for magnets_segments_per_slide
#     magnets_segments_per_slide: str = ""
#     skew_angle: str = ""
#     setup_to_analyze: str = "Setup1"
import os

from marshmallow import Schema
from marshmallow import fields
from marshmallow import validate

from ansys.aedt.toolkits.motor.backend.common.models import CommonProperties


class AEDTProperties(Schema):
    """Store common AEDT properties."""

    motor_type = fields.Str(validate=validate.OneOf(["", "IPM", "SPM"]), missing="")
    is_skewed = fields.Bool(missing=False)
    magnets_material = fields.Str(missing="")
    rotor_material = fields.Str(missing="")
    stator_material = fields.Str(missing="")
    # FIXME: use int instead of str for rotor_slices
    rotor_slices = fields.Str(missing="")
    # FIXME: use int instead of str for magnets_segments_per_slide
    magnets_segments_per_slide = fields.Str(missing="")
    skew_angle = fields.Str(missing="")
    setup_to_analyze = fields.Str(missing="Setup1")


class Properties(Schema):
    """Store all properties."""

    common = fields.Nested(CommonProperties, required=True)
    aedt = fields.Nested(AEDTProperties, required=True)
    # common_properties: CommonProperties
    # aedt_properties: AEDTProperties

    # def update(self, key, value) -> None:
    #     for properties in [self.common_properties, self.aedt_properties]:
    #         try:
    #             setattr(properties, key, value)
    #             break
    #         except AttributeError:
    #             continue


aedt_kwargs = {}
if os.path.expanduser(os.path.join(os.path.dirname(__file__), "aedt_properties.json")):
    with open(os.path.join(os.path.dirname(__file__), "aedt_properties.json")) as file_handler:
        aedt_properties = json.load(file_handler)
# aedt_properties = AEDTProperties(**aedt_kwargs)

common_kwargs = {}
if os.path.expanduser(os.path.join(os.path.dirname(__file__), "common_properties.json")):
    with open(os.path.join(os.path.dirname(__file__), "common_properties.json")) as file_handler:
        common_kwargs = json.load(file_handler)
# common_properties = CommonProperties(**common_kwargs)

properties = Properties(**common_kwargs, **aedt_kwargs)
