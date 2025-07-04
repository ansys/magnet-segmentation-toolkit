.. _toolkit_API_ref:

=============
API reference
=============

This section provides descriptions of the available API for the Magnet
Segmentation Toolkit:

- **Toolkit API**: Contains the ``ToolkitBackend`` class, which provides methods for
  controlling the toolkit workflow. In addition to methods for creating an AEDT
  session or connecting to an existing AEDT session, this API provides methods
  for automating the segmentation and skew of a 3D motor.

  .. warning::
      Both segmentation and skew of a 3D motor have requirements on the AEDT
      active project. Ensure that the active design meets these requirements:

      - For segmentation, ``SymmetryFactor`` and ``HalfAxial`` design settings must be defined.
      - For skew, ``Shaft`` must be the name of the shaft.

.. toctree::
   :maxdepth: 2

   api
