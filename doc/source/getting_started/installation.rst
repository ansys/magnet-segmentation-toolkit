.. _installation:

Installation
############

Download links
==============

The following installers are available for different operating systems:

.. list-table:: Available Installers
   :header-rows: 1
   :widths: 60 40

   * - `Installer Link <https://github.com/ansys/magnet-segmentation-toolkit/releases/latest>`_
     - Operating System
   * - `Download <https://github.com/ansys/magnet-segmentation-toolkit/releases/latest/download/Magnet-Segmentation-Toolkit-Installer-windows.exe>`_
     - Windows
   * - `Download <https://github.com/ansys/magnet-segmentation-toolkit/releases/latest/download/Magnet-Segmentation-Toolkit-Installer-ubuntu_22_04.exe>`_
     - Ubuntu 22.04
   * - `Download <https://github.com/ansys/magnet-segmentation-toolkit/releases/latest/download/Magnet-Segmentation-Toolkit-Installer-ubuntu_24_04.exe>`_
     - Ubuntu 24.04

Visit the `Releases
<https://github.com/ansys/magnet-segmentation-toolkit/releases>`__ page and pull
down the latest installer.

Installing the ``Magnet Segmentation Toolkit``
==============================================

.. tab-set::

  .. tab-item:: Windows

    First step is installing the ``Magnet Segmentation Toolkit``. In order to do so, follow the next steps.

    #. Download the necessary installer from the `latest available release <https://github.com/ansys/magnet-segmentation-toolkit/releases/latest>`_.
       The file should be named ``Magnet-Segmentation-Toolkit-Installer.exe``.

    #. Execute the installer.

    #. Search for the ``Magnet Segmentation Toolkit`` and run it.

    The ``Magnet Segmentation Toolkit`` window should appear at this stage.

  .. tab-item:: Linux

    .. tab-set::

      .. tab-item:: Ubuntu

        Prerequisites:

        #. **OS** supported for **Ubuntu(24.04 and 22.04)**.

        #. Update ``apt-get`` repository and install the following packages with **sudo** privileges:
           **wget, gnome, libffi-dev, libssl-dev, libsqlite3-dev, libxcb-xinerama0 and build-essential** packages with **sudo** privileges

           .. code:: shell

             sudo apt-get update -y
             sudo apt-get install wget gnome libffi-dev libssl-dev libsqlite3-dev libxcb-xinerama0 build-essential -y

        #. Install **zlib** package

           .. code:: shell

             wget https://zlib.net/current/zlib.tar.gz
             tar xvzf zlib.tar.gz
             cd zlib-*
             make clean
             ./configure
             make
             sudo make install

        To install the ``Magnet Segmentation Toolkit``, follow below steps.

        #. Download the necessary installer from the `latest available release <https://github.com/ansys/magnet-segmentation-toolkit/releases/latest>`_.
           The file should be named ``Magnet-Segmentation-Toolkit-Installer-ubuntu_*.zip``.

        #. Execute the below command on the terminal

           .. code:: shell

             unzip Magnet-Segmentation-Toolkit-Installer-ubuntu_*.zip
             ./installer.sh

        #. Search for the ``Magnet Segmentation Toolkit`` and run it.

        The ``Magnet Segmentation Toolkit`` window should appear at this stage.

        To uninstall the ``Magnet Segmentation Toolkit``, follow below steps.

        #. Go to File menu. Click Uninstall option.

        #. Click ``Uninstall`` button.

Python Installation
===================

The Magnet Segmentation Toolkit can be installed like any other open source package.
From PyPI, you can either install both the backend and user interface (UI) methods or install only the backend methods.

You can either install both the backend and user interface (UI) methods or install only the backend methods.

To install both the backend and UI methods, run this command:

.. code:: bash

    pip install ansys-magnet-segmentation-toolkit[all]

If you only need the common API, install only the backend methods with this
command:

.. code:: bash

    pip install ansys-magnet-segmentation-toolkit

For developers
==============

You can be up and running with four lines of code:

.. code:: bash

   git clone https://github.com/ansys/magnet-segmentation-toolkit
   cd magnet-segmentation-toolkit
   pip install -e .

Now you can run it with:

.. code:: bash

   run_toolkit

**Details**

Installing Pytools installer in developer mode allows you to modify the source
and enhance it.

Before contributing to the project, please refer to the `PyAnsys Developer's
guide`_. You need to follow these steps:

#. Start by cloning this repository:

   .. code:: bash

      git clone https://github.com/ansys/magnet-segmentation-toolkit

#. Create a fresh-clean Python environment and activate it. Refer to the
   official `venv`_ documentation if you require further information:

   .. code:: bash

      # Create a virtual environment
      python -m venv .venv
      # Activate it in a POSIX system
      source .venv/bin/activate
      # Activate it in Windows CMD environment
      .venv\Scripts\activate.bat
      # Activate it in Windows Powershell
      .venv\Scripts\Activate.ps1

#. Install the project in editable mode:

   .. code:: bash

      python -m pip install -e .[tests,doc]

#. Finally, verify your development installation by running:

   .. code:: bash

      pytest tests -v

Style and testing
-----------------

This project uses `pre-commit <https://pre-commit.com/>`_. Install with:

.. code::

   pip install pre-commit
   run pre-commit install

This now runs ``pre-commit`` for each commit to ensure you follow project
style guidelines. For example:

.. code::

   git commit -am 'fix style'
   isort....................................................................Passed
   black....................................................................Passed
   blacken-docs.............................................................Passed
   flake8...................................................................Passed
   codespell................................................................Passed
   pydocstyle...............................................................Passed
   check for merge conflicts................................................Passed
   debug statements (python)................................................Passed
   check yaml...............................................................Passed
   trim trailing whitespace.................................................Passed
   Validate GitHub Workflows................................................Passed

If you need to run it again on all files and not just staged files, run:

.. code::

   run pre-commit run --all-files

Local build
-----------

This app can be deployed as a 'frozen' app using `pyinstaller
<https://pypi.org/project/pyinstaller/>`_ with:

.. code::

   pip install -e .[freeze]
   run pyinstaller frozen.spec

This generates app files at ``dist/magnet_segmentation_toolkit`` and you
can run it locally by executing ``Magnet Segmentation Toolkit.exe``.
For more information on how to create a standalone executable, refer to this section:
`How to distribute
<https://aedt.common.toolkit.docs.pyansys.com/version/stable/distributing.html>`_.


Documentation
-------------
For building documentation, you can either run the usual rules provided in the
`Sphinx`_ Makefile:

.. code:: bash

    pip install -e .[doc]
    doc/make.bat html
    # subsequently open the documentation with (under Linux):
    <your_browser_name> doc/html/index.html

.. LINKS AND REFERENCES
.. _PyAnsys Developer's guide: https://dev.docs.pyansys.com/
.. _Sphinx: https://www.sphinx-doc.org/en/master/
.. _pip: https://pypi.org/project/pip/
.. _venv: https://docs.python.org/3/library/venv.html