===============
Getting started
===============

To run the Motor Segmentation Toolkit, you must have a licensed copy of AEDT installed.
You have multiple options for installing and launching this toolkit:

- You can install it in AEDT via an installation script and then launch it as a wizard.
  For more information, see :ref:`install-toolkit-AEDT`.
- You can install it in the AEDT console and then launch it as a wizard. For more
  information, see :ref:`install_toolkit_console_ui`.
- You can install and launch it directly from a Python console using its API. For
  more information, see :ref:`install_toolkit_console_api`.


The toolkit features can be accessed from:

- The user interface (UI), see :doc:`Toolkit/ui`.

- The API, see :doc:`Toolkit/index`.

.. _install-toolkit-AEDT:

How to install directly in AEDT and launch as a wizard
------------------------------------------------------

You install the Motor Segmentation Toolkit directly in AEDT using the base
interpreter from the AEDT installation.

#. From `Install from a Python file <https://aedt.docs.pyansys.com/version/stable//Getting_started/Installation.html#install-from-a-python-file> <https://aedt.docs.pyansys.com/version/stable//Getting_started/Installation.html>`_
   in the PyAEDT documentation, download the PyAEDT Installer Python file and run this script.

#. If this is the first toolkit being installed in AEDT, restart AEDT to update its **Tools** menu.

#. In AEDT, select **Tools > Toolkit > PyAEDT > Console** to load the PyAEDT console:

    .. image:: ./_static/console.png
      :width: 800
      :alt: PyAEDT console in AEDT

#. Run these commands to add the Motor Segmentation Toolkit as a wizard in AEDT:

    .. code:: python

      desktop.add_custom_toolkit("MotorWizard")
      exit()

#. Close the PyAEDT console.

#. In AEDT, select **Tools > Toolkit > Update Menu** to update the **Toolkit** menu.

#. Select **Tools > Toolkit > PersonalLib > TemplateToolkit> Run PyAEDT Toolkit Script** to open the
   Motor Toolkit Wizard in AEDT:

    .. image:: ./_static/design_connected.png
      :width: 800
      :alt: UI opened from AEDT, design tab

For wizard usage information, see :doc:`Toolkit/ui`.

.. _install_toolkit_console_ui:

How to install in the AEDT console and launch as a wizard
---------------------------------------------------------

You can install the Motor Segmentation Toolkit in an specific Python environment.

- If you have an existing virtual environment, skip step 1.
- If you have already installed the toolkit in your existing virtual environment, skip step 2.

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

#. Install the toolkit from GitHub:

    .. code:: bash

      python -m pip install git+https://github.com/ansys/pymotorcad-pyaedt-toolkit.git

#. Launch the Motor Toolkit Wizard:

    .. code:: bash

      python .venv\Lib\site-packages\ansys\aedt\toolkits\motor\run_toolkit.py

    .. image:: ./_static/design_connected_launch_AEDT.png
      :width: 800
      :alt: UI opened from console, settings tab

For wizard usage information, see :doc:`Toolkit/ui`.

.. _install_toolkit_console_api:

How to install in the AEDT console and use the API
--------------------------------------------------

You can install the Motor Segmentation Toolkit in a specific Python environment and use its API.

#. Ensure that you have already performed steps 1 and 2 in :ref:`install_toolkit_console_ui`.

#. Open a Python console in your virtual environment:

    .. code:: bash

      python

#. Use the API at the toolkit level.

   For example, this code shows how to import the toolkit, launch AEDT, open a 3D motor model, and then
   segment and skew this model in Maxwell 3D:

    .. code:: python

      # Import required modules
      import os

      # Import backend services
      from ansys.aedt.toolkits.motor.backend.api import Toolkit

      # Backend object
      toolkit = Toolkit()

      # Get service properties
      properties = toolkit.get_properties()

      # Define properties
      project_name = "my_3d_model"
      active_project = os.path.join(temp_folder, "{}.aedt".format(project_name))
      active_design = "my_design"
      magnets_material = "N30UH_65C"
      rotor_material = "M250-35A_20C"

      properties = {
          "aedt_version": "2023.1",
          "active_project": active_project,
          "active_design": {"Maxwell3d": active_design},
          "design_list": {project_name: [{"Maxwell3d": active_design}]},
          "IsSkewed": False,
          "MagnetsMaterial": magnets_material,
          "MagnetsSegmentsPerSlice": "5",
          "RotorMaterial": rotor_material,
          "RotorSlices": "3",
      }

      # Set service properties
      toolkit.set_properties()

      # Launch AEDT in a thread
      service.launch_aedt()

      # Wait until thread is finished
      response = service.get_thread_status()

      while response[0] == 0:
          time.sleep(1)
          response = service.get_thread_status()

      # Apply segmentation
      toolkit.segmentation()

      # Apply skew
      toolkit.apply_skew()

      # Wait until thread is finished
      response = service.get_thread_status()
      while response[0] == 0:
          time.sleep(1)
          response = service.get_thread_status()

      # Release AEDT
      service.release_aedt()
