===============
Getting started
===============

To run this toolkit, you must have a licensed copy of Ansys Electronics Desktop (AEDT) and Motor-CAD installed.

To access the toolkit functionalities an IDE (Integrated Development Environment) is needed.

Install the toolkit
-------------------

If you have an existing virtual environment, you can skip step 1:

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

#. Install the toolkit from git by running this command:

    .. code:: bash

      pip install git+https://github.com/pyansys/pymotorcad-pyaedt-toolkit.git

#. Open an instance of Motor-CAD and enable the option to show the GUI when launching Motor-CAD from automation by navigating through: *Default > Automation*.:

    .. image:: ./Resources/Show_GUI_MCAD.png
      :width: 800
      :alt: Motor-CAD GUI
