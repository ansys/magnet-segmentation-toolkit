# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 - 2025 ANSYS, Inc. and/or its affiliates.
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

# # Maxwell 3D segmentation
#
# This example shows how to use the Magnet Segmentation Toolkit to segment
# your AEDT motor model.

# ## Perform required imports
#
# Perform required imports.

# +
import os
import shutil
import tempfile

from ansys.aedt.toolkits.common.utils import download_file

from ansys.aedt.toolkits.magnet_segmentation.backend.api import ToolkitBackend

# -

# ## Initialize temporary folder and project settings
#
# Initialize a temporary folder to copy the input file into
# and specify project settings.

# +
URL_BASE = "https://raw.githubusercontent.com/ansys/example-data/master/toolkits/magnet_segmentation/"
AEDT_PROJECT = "e9_eMobility_IPM_3D"
URL = os.path.join(URL_BASE, AEDT_PROJECT + ".aedt")

temp_dir = tempfile.TemporaryDirectory(suffix=".ansys")
active_project = os.path.join(temp_dir.name, AEDT_PROJECT + ".aedt")
download_file(URL, active_project)
active_design = "e9_eMobility_IPM_3D_test"
# -

# ## Initialize toolkit
#
# Initialize the toolkit.

toolkit = ToolkitBackend()

# ## Get toolkit properties
#
# Get the toolkit properties.

properties = toolkit.get_properties()

# ## Initialize properties
#
# Initialize a dictionary of properties.

properties["aedt_version"] = "2025.1"
properties["active_project"] = AEDT_PROJECT
properties["active_design"] = active_design
properties["design_list"] = {AEDT_PROJECT: [active_design]}
properties["is_skewed"] = False
properties["rotor_material"] = "M250-35A_20C"
properties["stator_material"] = "M250-35A_20C"
properties["magnets_material"] = "N30UH_65C"
properties["magnet_segments_per_slice"] = 2
properties["rotor_slices"] = 2
properties["apply_mesh_sheets"] = False
# properties["mesh_sheets_number"] = 3
properties["skew_angle"] = "2deg"

# ## Set non-graphical mode
#
# Set non-graphical mode. The default value is ``False``.

properties["non_graphical"] = False

# ## Set properties
#
# Set properties.

toolkit.set_properties(properties)

# ## Initialize AEDT
#
# Launch a new AEDT session.

toolkit.launch_aedt()

# ## Open project
#
# Open the project.

toolkit.open_project(active_project)

# ## Connect design
#
# Connect or create a new design.

toolkit.connect_design()

# ## Apply segmentation
#
# Apply segmentation and assign the relative coordinate system.

toolkit.segmentation()

# ## Apply skew angle
#
# Apply the skew angle to rotor slices.

toolkit.apply_skew()

# ## Validate and analyze design
#
# Uncomment the line to validate and analyze the design.

# toolkit.validate_and_analyze()

# ## Create magnet loss report
#
# Uncomment the lines to create magnet loss report and compute average value.

# magnet_loss = toolkit.get_magnet_loss()
# print(f"Average magnet loss: {magnet_loss} W")

# ## Save and release AEDT
#
# Save and release AEDT.

# toolkit.save_project()

toolkit.release_aedt(True, True)

# ## Remove temporary folder
#
# Remove the temporary folder.

shutil.rmtree(temp_dir.name, ignore_errors=True)
