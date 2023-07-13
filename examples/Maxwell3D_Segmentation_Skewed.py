"""
Maxwell 3D Segmentation
-----------------------
This example shows how you can use PyMotorCAD-PyAEDT toolkit to segment
a skewed IPM in AEDT.
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
project_name = "M3D_3Slices_Skewed"
active_project = os.path.join(temp_folder, "{}.aedt".format(project_name))
active_design = "0_Segmentation_automation"

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
    "selected_process": 19676,
    "aedt_version": "2023.1",
    "use_grpc": False,
    "active_project": active_project,
    "active_design": {"Maxwell3d": active_design},
    "design_list": {project_name: [{"Maxwell3d": active_design}]},
    "IsSkewed": True,
    "MagnetsMaterial": "N42EH_80C",
    "MagnetsSegmentsPerSlice": "5",
    "RotorMaterial": "NO18-1160_140C",
    "RotorSlices": "3",
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
toolkit.init_aedt()

#################################################################################
# Set AEDT project settings
# ~~~~~~~~~~~~~~~~~~~~~~~~~
# Set AEDT project settings.
toolkit.set_model()

#################################################################################
# Apply segmentation
# ~~~~~~~~~~~~~~~~~~
# Apply segmentation.
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
