# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
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

import pytest

from tests.tests_aedt.conftest import DESIGN_NAME
from tests.tests_aedt.conftest import PROJECT_NAME

pytestmark = [pytest.mark.aedt]

APP_NAME = "Maxwell3d"
DESIGN_PROPERTIES = {
    "active_design": DESIGN_NAME,
    "design_list": {PROJECT_NAME: [DESIGN_NAME]},
}


class TestAEDTMotorWorkflow:
    """Class defining a simple AEDT motor related workflow."""

    def test_00_installed_aedt_version(self, aedtapp):
        """Check installed aedt version."""
        assert aedtapp.installed_aedt_version() != []

    def test_01_set_properties(self, aedtapp):
        """Set properties."""
        assert aedtapp.set_properties(DESIGN_PROPERTIES)

    def test_02_get_properties(self, aedtapp):
        """Get properties."""
        properties = aedtapp.get_properties()
        assert DESIGN_PROPERTIES["active_design"] == properties["active_design"]
        assert DESIGN_PROPERTIES["design_list"] == properties["design_list"]

    def test_03_connect_aedt(self, aedtapp):
        """Connect aedt."""
        assert aedtapp.connect_aedt()

    def test_04_aedt_sessions(self, aedtapp):
        """Check aedt sessions."""
        assert aedtapp.aedt_sessions() != []

    def test_05_get_design_names(self, aedtapp):
        """Check design names of the project."""
        res = aedtapp.get_design_names()
        assert len(res) == 1
        assert res[0] == DESIGN_NAME

    def test_06_segmentation(self, aedtapp):
        properties = {
            "is_skewed": False,
            "magnets_material": "N30UH_65C",
            "magnet_segments_per_slice": 2,
            "rotor_material": "M250-35A_20C",
            "stator_material": "M250-35A_20C",
            "rotor_slices": 2,
            "apply_mesh_sheets": False,
            # "mesh_sheets_number": 2,
        }
        assert aedtapp.set_properties(properties)
        assert aedtapp.segmentation()

    def test_07_apply_skew(self, aedtapp_segmented):
        """Apply skew angle to rotor slices."""
        properties = {
            "is_skewed": False,
            "magnets_material": "N30UH_65C",
            "magnet_segments_per_slice": 2,
            "rotor_material": "M250-35A_20C",
            "stator_material": "M250-35A_20C",
            "rotor_slices": 2,
            "apply_mesh_sheets": False,
            "skew_angle": "2deg",
        }
        assert aedtapp_segmented.set_properties(properties)
        assert aedtapp_segmented.apply_skew()

    def test_08_validate_and_analyze(self, aedtapp_skewed):
        assert aedtapp_skewed.validate_and_analyze()

    def test_09_get_magnet_loss(self, aedtapp_analyzed):
        magnet_loss = aedtapp_analyzed.get_magnet_loss()
        assert isinstance(magnet_loss, str)
