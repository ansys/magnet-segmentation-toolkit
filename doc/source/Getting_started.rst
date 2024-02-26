===============
Getting started
===============

To run the Magnet Segmentation Toolkit, you must have a licensed copy of AEDT installed.
You have multiple options for installing and launching this toolkit:

- You can install the toolkit directly in AEDT via an installation script and then launch it
  as a wizard. For more information, see :ref:`install-toolkit-AEDT`.
- You can install the toolkit from the AEDT console and then launch it as a wizard. For more
  information, see :ref:`install_toolkit_console_ui`.
- You can install and launch the toolkit directly from a Python console and then use the toolkit's APIs.
  For more information, see :ref:`install_toolkit_console_api`.

.. _install-toolkit-AEDT:

How to install directly in AEDT and launch as a wizard
------------------------------------------------------

You can install the Magnet Segmentation Toolkit directly in AEDT using the base
interpreter from the AEDT installation.

#. From `Install from a Python file <https://aedt.docs.pyansys.com/version/stable//Getting_started/Installation.html#install-from-a-python-file>`_
   in the PyAEDT documentation, download the ``PyAEDTInstallerFromDesktop.py`` file and then run this Python script.

#. If this is the first toolkit being installed in AEDT, restart AEDT to update its **Tools** menu.

#. In AEDT, select **Tools > Toolkit > PyAEDT > Console** to load the PyAEDT console:

   .. image:: ./_static/console.png
     :width: 800
     :alt: PyAEDT console in AEDT

#. In the PyAEDT console, run these commands to add the Magnet Segmentation Toolkit as a wizard (toolkit UI)
   in AEDT:

   .. code:: python

     desktop.add_custom_toolkit("MagnetSegmentationWizard")
     exit()

#. Close the PyAEDT console.

#. In AEDT, select **Tools > Toolkit > Update Menu** to update the **Toolkit** menu.

#. Select **Tools > Toolkit > PersonalLib > TemplateToolkit > Run PyAEDT Toolkit Script** to open the
   Magnet Segmentation Toolkit Wizard in AEDT:

   .. image:: ./_static/design_connected.png
     :width: 800
     :alt: UI opened from AEDT, design tab

The wizard is connected directly to the AEDT session. For wizard usage information, see :doc:`Toolkit/ui`.

.. _install_toolkit_console_ui:

How to install from the AEDT console and launch as a wizard
-----------------------------------------------------------

You can install the Magnet Segmentation Toolkit in a specific Python environment from the
AEDT console.

- If you have an existing virtual environment, skip step 1.
- If you have already installed the toolkit in your virtual environment, skip step 2.

#. Create a fresh-clean Python environment and activate it:

   .. code:: bash

      # Create a virtual environment
      python -m venv .venv

      # Activate it in a POSIX system
      source .venv/bin/activate

      # Activate it in a Windows CMD environment
      .venv\Scripts\activate.bat

      # Activate it in Windows PowerShell
      .venv\Scripts\Activate.ps1

#. Install the toolkit from the GitHub repository:

   .. code:: bash

     python -m pip install git+https://github.com/ansys/magnet-segmentation-toolkit.git

#. Launch the Magnet Segmentation Toolkit Wizard:

   .. code:: bash

     python .venv\Lib\site-packages\ansys\aedt\toolkits\magnet_segmentation\run_toolkit.py

For wizard usage information, see :doc:`Toolkit/ui`.

.. _install_toolkit_console_api:

How to install from a Python console and use the toolkit's APIs
---------------------------------------------------------------

You can install the Magnet Segmentation Toolkit in a specific Python environment from a Python
console and then use this toolkit's APIs.

.. note::
  The following procedure assumes that you have already performed steps 1 and 2 in
  :ref:`install_toolkit_console_ui`. These steps create and activate a virtual environment
  and install the toolkit from the GitHub repository.

#. Open a Python console in your virtual environment:

   .. code:: bash

     python

#. Use the toolkit's APIs at the toolkit level.

   For example, this code shows how to use the toolkit's APIs to import the toolkit, launch AEDT,
   open a 3D motor model, and then segment and skew this model in Maxwell 3D:

   .. code:: python

     # Import required modules
     import os

     # Import backend services
     from ansys.aedt.toolkits.magnet_segmentation.backend.api import Toolkit

     # Backend object
     toolkit = Toolkit()

     # Get service properties
     properties = toolkit.get_properties()

     # Define properties

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

     # Set service properties
     toolkit.set_properties(properties)

     # Launch AEDT
     toolkit.launch_aedt()

     # Wait for the toolkit thread to be idle and ready to accept a new task
     toolkit.wait_to_be_idle()

     # Apply segmentation
     toolkit.segmentation()

     # Apply skew
     toolkit.apply_skew()

     # Release AEDT
     service.release_aedt()

For descriptions of the APIs available for the Magnet Segmentation Toolkit, see :doc:`Toolkit/index`.
