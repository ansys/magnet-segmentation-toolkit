"""
Maxwell 3D Segmentation
-----------------------
This example shows how you can use PyMotorCAD-PyAEDT toolkit to segment
your AEDT motor model.
"""
#################################################################################
# Perform required imports
# ~~~~~~~~~~~~~~~~~~~~~~~~
# Perform required imports.
import os
from pathlib import Path
import shutil

from pyaedt import generate_unique_folder_name

from ansys.aedt.toolkits.motor.backend.api import Toolkit

#################################################################################
# Initialize Temporary Folder and Project settings
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Initialize Temporary Folder to copy the input file into
# and set project settings.

src_folder = os.path.join(Path(__file__).parents[0], "input_files")
temp_folder = shutil.copytree(src_folder, os.path.join(generate_unique_folder_name(), "input_files"))
project_name = "e9_eMobility_IPM_3D"
active_project = os.path.join(temp_folder, "{}.aedt".format(project_name))
active_design = "e9_eMobility_IPM_3D_test"

#################################################################################
# Initialize Toolkit
# ~~~~~~~~~~~~~~~~~~
# Initialize Toolkit.

toolkit = Toolkit()

#################################################################################
# Get Toolkit properties
# ~~~~~~~~~~~~~~~~~~~~~~
# Get Toolkit properties.

properties = toolkit.get_properties()

#################################################################################
# Initialize Properties dictionary
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Initialize Properties dictionary.

properties["active_project"] = active_project
properties["active_design"] = {"Maxwell3d": active_design}
properties["designs_by_project_name"] = {active_project: [{"Maxwell3d": active_design}]}
properties["is_skewed"] = False
properties["motor_type"] = "IPM"
properties["rotor_material"] = "M250-35A_20C"
properties["stator_material"] = "M250-35A_20C"
properties["magnets_material"] = "N30UH_65C"
properties["magnet_segments_per_slice"] = 2
properties["rotor_slices"] = 2
properties["apply_mesh_sheets"] = True
properties["mesh_sheets_number"] = 3

#################################################################################
# Set properties
# ~~~~~~~~~~~~~~
# Set properties.

toolkit.set_properties(properties)

#################################################################################
# Initialize AEDT
# ~~~~~~~~~~~~~~~
# Initialize AEDT.

toolkit.launch_aedt()

#################################################################################
# Apply segmentation
# ~~~~~~~~~~~~~~~~~~
# Apply segmentation and assign relative coordinate system.

toolkit.segmentation()

#################################################################################
# Save and Release desktop
# ~~~~~~~~~~~~~~~~~~~~~~~~
# Save and Release desktop.

# toolkit.save_project()

toolkit.release_aedt(True, True)

#################################################################################
# Remove temporary folder
# ~~~~~~~~~~~~~~~~~~~~~~~
# Remove temporary folder.

shutil.rmtree(temp_folder, ignore_errors=True)
