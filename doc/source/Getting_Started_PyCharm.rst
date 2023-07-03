==================================
Getting started using PyCharm
==================================

Important: Internal Only
__________________________

The instructions below explain how to get started in PyCharm. This is one of many third party IDEs (Integrated Development Environment) available
As this is a third party tool it cannot be recommended for external use by Ansys. However, this is one of the main IDEs used within Ansys hence a getting started guide based on PyCharm.

Prerequisites
---------------
To run this toolkit, you must have a licensed copy of Ansys Electronics Desktop (AEDT) and Motor-CAD installed.

To access the toolkit functionalities an IDE (Integrated Development Environment) is needed.

You need to have PyCharm installed and Python 3.x.

You need an active Github account.

Install the toolkit
-------------------

First we need to create a new project. We will clone the repository first from Git. Git is a Version Control System (VCS)
so we will follow these steps:

#. Open PyCharm
#. Close any open projects so you are on the home screen
#. Select *Get from VCS*
#. Use this URL:    https://github.com/ansys/pymotorcad-pyaedt-toolkit.git
#. Directory: populates automatically from the URL
#. Clone

This creates a new project with the cloned repository containing the toolkit from Github. You effectively now have a local copy to run and edit.
Check at the bottom right if you have the correct Python Interpreter running. If you need to change this:

#. Add New Interpreter
#. Add Local
#. Select the interpreter you want to use

Next we need to create a new virtual environment. This is effectively your coding environment.

#. Open a new terminal at the bottom of the screen: click on terminal
#. Change terminal to *Command Prompt* from the pull down menu
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

We need several packages or *dependencies* to be able to use the toolkit. These can all be installed by doing the following

#TODO: pip install . does not work here for some reason

If in future you need additional dependencies these can all be installed from the *pyproject.toml* file. In the file you
find all dependencies available. For example if we want to install additional packages available for documentation:

    .. code:: bash

        # Install additional dependencies from .toml file
        pip install .[doc]

#TODO: doe we need to add to conf.py

#. Install the toolkit from git by running this command:

    .. code:: bash

      pip install git+https://github.com/pyansys/pymotorcad-pyaedt-toolkit.git

#TODO: Install does not run correct version of pip

#TODO: Install gives error using Python 3.9 it's running fine on the project created previously?!?

Version Control in Git
-----------------------
You are now ready to work on your local copy. However, we are still in the main branch so we need to create our own branch to work in.
This enables multiple people to work together and merge their work accordingly into the main branch once ready.

#. In the bottom right of the screen you can see *main*
#. Click here, this opens up all branches
#. Click on main
#. From the menu click on *'New branch from 'main'*
#. Name your new branch. There is a common naming convention to use which can be found in the Developers guide here:
    https://dev.docs.pyansys.com/how-to/contributing.html#branch-naming-conventions

#. Open an instance of Motor-CAD and enable the option to show the GUI when launching Motor-CAD from automation by navigating through: *Default > Automation*.:

    .. image:: ./Resources/Show_GUI_MCAD.png
      :width: 800
      :alt: Motor-CAD GUI

