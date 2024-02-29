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

from pyaedt import generate_unique_folder_name

from ansys.aedt.toolkits.magnet_segmentation.backend.api import Toolkit
from ansys.aedt.toolkits.magnet_segmentation.utils import download_file

# -

# ## Initialize temporary folder and project settings
#
# Initialize a temporary folder to copy the input file into
# and specify project settings.

# +
URL_BASE = "https://raw.githubusercontent.com/ansys/example-data/master/toolkits/magnet_segmentation/"
AEDT_PROJECT = "e9_eMobility_IPM_3D.aedt"
URL = os.path.join(URL_BASE, AEDT_PROJECT)

temp_folder = os.path.join(generate_unique_folder_name())
active_project = os.path.join(temp_folder, AEDT_PROJECT)
download_file(URL, active_project)
active_design = "e9_eMobility_IPM_3D_test"
# -

# ## Initialize toolkit
#
# Initialize the toolkit.

toolkit = Toolkit()

# ## Get toolkit properties
#
# Get the toolkit properties.

properties = toolkit.get_properties()

# ## Initialize properties
#
# Initialize a dictionary of properties.

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
# Initialize AEDT.

toolkit.launch_aedt()

# ## Wait for the toolkit thread to be idle
#
# Wait for the toolkit thread to be idle and ready to accept a new task.

toolkit.wait_to_be_idle()

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

#toolkit.validate_and_analyze()

# ## Create magnet loss report
#
# Uncomment the lines to create magnet loss report and compute average value.

#magnet_loss = toolkit.get_magnet_loss()
#print(f"Average magnet loss: {magnet_loss['SolidLoss']['Value']}{magnet_loss['SolidLoss']['Unit']}")

# ## Save and release AEDT
#
# Save and release AEDT.

# toolkit.save_project()

toolkit.release_aedt(True, True)

# ## Remove temporary folder
#
# Remove the temporary folder.

shutil.rmtree(temp_folder, ignore_errors=True)
