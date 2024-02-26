# Copyright (C) 2023 - 2024 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Data classes used to store data related to various settings.

The settings include common AEDT toolkit settings and settings associated
to motor workflows in AEDT.
"""
import json
import os
from typing import Literal

from pydantic import BaseModel

from ansys.aedt.toolkits.magnet_segmentation.backend.common.models import CommonProperties


class AEDTProperties(BaseModel):
    """Store AEDT properties."""

    motor_type: Literal["", "IPM", "SPM"] = ""
    is_skewed: bool = False
    apply_mesh_sheets: bool = False
    magnets_material: str = ""
    rotor_material: str = ""
    stator_material: str = ""
    rotor_slices: int = 0
    magnet_segments_per_slice: int = 0
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
