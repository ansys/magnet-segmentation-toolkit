"""
Maxwell 3D Segmentation
-----------------------
This example shows how you can use the Magnet Segmentation Toolkit to segment your AEDT motor model.
"""
#################################################################################
# Perform required imports
# ~~~~~~~~~~~~~~~~~~~~~~~~
# Perform required imports.
import os
from pathlib import Path
import shutil

from pyaedt import generate_unique_folder_name

from ansys.aedt.toolkits.magnet_segmentation.backend.api import Toolkit

#################################################################################
# Initialize Temporary Folder and Project settings
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Initialize Temporary Folder to copy the input file into
# and set project settings.

src_folder = os.path.join(Path(__file__).parents[0], "input_files")
temp_folder = shutil.copytree(src_folder, os.path.join(generate_unique_folder_name(), "input_files"))
project_name = "e9_eMobility_IPM_1seg_cs_test_ANSYSEM_3D"
active_project = os.path.join(temp_folder, "{}.aedt".format(project_name))
active_design = "Motor-CAD e9_eMobility_IPM_1seg_cs_test"

#################################################################################
# Initialize Toolkit
# ~~~~~~~~~~~~~~~~~~
# Initialize Toolkit.

toolkit = Toolkit()

#################################################################################
# Initialize Properties dictionary
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Initialize Properties dictionary.

data = {
    "aedt_version": "2023.1",
    "active_project": active_project,
    "active_design": {"Maxwell3d": active_design},
    "design_list": {project_name: [{"Maxwell3d": active_design}]},
    "IsSkewed": False,
    "MagnetsMaterial": "N30UH_65C",
    "MagnetsSegmentsPerSlice": "2",
    "RotorMaterial": "M250-35A_20C",
    "StatorMaterial": "M250-35A_20C",
    "RotorSlices": "2",
    "SkewAngle": "2deg",
}
#################################################################################
# Set properties
# ~~~~~~~~~~~~~~
# Set properties.

toolkit.set_properties(data)

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
# Apply skew angle
# ~~~~~~~~~~~~~~~~
# Apply skew angle to rotor slices.
toolkit.apply_skew()

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
