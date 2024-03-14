AEDT Common ToolkitBackend API
=======================
The AEDT Common ToolkitBackend API contains the ``AEDTCommonToolkit`` class, which provides basic
functions for controlling AEDT that are shared between the backend and frontend.
These functions are the same for all AEDT toolkits.

.. currentmodule:: ansys.aedt.toolkits.magnet_segmentation.backend.common.toolkit

.. autosummary::
   :toctree: _autosummary

   AEDTCommonToolkit

You can access the ``AEDTCommonToolkit`` class directly from the ``ToolkitBackend`` class
because it is inherited.

This code shows how to use both the ``ToolkitBackend`` and ``AEDTCommonToolkit`` classes
to create an object:

.. code:: python

    # Import required modules and backend
    from ansys.aedt.toolkits.magnet_segmentation.backend.api import ToolkitBackend

    # Backend object
    toolkit = ToolkitBackend()

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