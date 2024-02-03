AEDT Common Toolkit API
=======================
The AEDT Common Toolkit API contains the ``AEDTCommonToolkit`` class, which provides basic
functions for controlling AEDT that are shared between the backend and frontend.
These functions are the same for all AEDT toolkits.

.. currentmodule:: ansys.aedt.toolkits.magnet_segmentation.backend.common.toolkit

.. autosummary::
   :toctree: _autosummary

   AEDTCommonToolkit

You can access the ``AEDTCommonToolkit`` class directly from the ``Toolkit`` class
because it is inherited.

This code shows how to use both the ``Toolkit`` and ``AEDTCommonToolkit`` classes
to create an object:

.. code:: python

    # Import required modules and backend
    from ansys.aedt.toolkits.magnet_segmentation.backend.api import Toolkit

    # Backend object
    toolkit = Toolkit()

    # Get the default properties loaded from JSON file
    properties = toolkit.get_properties()

    # Set properties
    new_properties = {"aedt_version": "2023.2"}
    toolkit.set_properties(new_properties)
    properties = toolkit.get_properties()

    # Launch AEDT
    msg = toolkit.launch_aedt()

    # Wait for the toolkit thread to be idle
    toolkit.wait_to_be_idle()

    # Release AEDT
    toolkit.release_aedt()