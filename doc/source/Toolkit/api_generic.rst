Generic API
===========
The Generic API contains the ``ToolkitGeneric`` class, which provides basic
functions for controlling AEDT that are shared between the backend and frontend.
These functions are the same for all AEDT toolkits.

.. currentmodule:: ansys.aedt.toolkits.motor.backend.common.api_generic

.. autosummary::
   :toctree: _autosummary

   ToolkitGeneric

You can access the ``ToolkitGeneric*`` class directly from the ``toolkit`` class
because it is inherited.

This code shows how to use both the ``Toolkit`` and ``ToolkitGeneric`` classes
to create an object:

.. code:: python

    # Import required modules
    import time

    # Import backend services
    from ansys.aedt.toolkits.motor.backend.api import Toolkit

    # Backend object
    service = Toolkit()

    # Get the default properties loaded from JSON file
    properties = service.get_properties()

    # Set properties
    new_properties = {"aedt_version": "2023.2"}
    service.set_properties(new_properties)
    properties = service.get_properties()

    # Get AEDT sessions
    sessions = service.aedt_sessions()

    # Launch AEDT
    msg = service.launch_aedt()

    # Wait until thread is finished
    response = service.get_thread_status()
    while response[0] == 0:
        time.sleep(1)
        response = service.get_thread_status()

    # Release AEDT
    service.release_aedt()