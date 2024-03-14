ToolkitBackend API
===========
The ToolkitBackend API contains the ``ToolkitBackend`` class, which provides methods for
controlling the toolkit workflow. In addition to methods for creating an AEDT
session or connecting to an existing AEDT session, this API provides methods for
automating the segmentation and skew of a 3D motor.

.. warning::
    Both segmentation and skew of a 3D motor have requirements on the AEDT
    active project. Ensure that the active design meets these requirements:
    
    - For segmentation, ``SymmetryFactor`` and ``HalfAxial`` design settings must be defined.
    - For skew, ``Shaft`` must be the name of the shaft.

.. currentmodule:: ansys.aedt.toolkits.magnet_segmentation.backend.api

.. autosummary::
   :toctree: _autosummary

   ToolkitBackend

This code shows how to use the ``ToolkitBackend`` class:

.. code:: python

    # Import required modules and backend
    from ansys.aedt.toolkits.magnet_segmentation.backend.api import ToolkitBackend

    # Initialize generic service
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

    # Segment and skew motor
    toolkit.segmentation()
    toolkit.apply_skew()

    # Release AEDT
    toolkit.release_aedt()
