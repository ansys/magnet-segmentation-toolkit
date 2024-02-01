============
UI reference
============

This section describes how to use the Magnet Segmentation Toolkit Wizard, which requires an installed
and licensed copy of AEDT. It assumes that you have already launched the wizard from
either the AEDT menu or AEDT console. For toolkit installation and wizard launching information,
see these topics:

- :ref:`install-toolkit-AEDT`
- :ref:`install_toolkit_console_ui`

#. On the **Settings** tab, specify settings for either creating an AEDT session or
   connecting to an existing AEDT session.
   
   .. image:: ../_static/design_connected.png
     :width: 800
     :alt: Settings tab

#. Under **Project Name**, click **Select aedt project** to select an AEDT file for a
   3D motor model.

#. Near the bottom of the tab, click **Launch AEDT**.

#. On the **Segmentation** tab, specify the project, design to work in, and
   segmentation settings.

   .. image:: ../_static/segmentation_settings.png
     :width: 800
     :alt: Settings tab

#. From the AEDT menu, select **File > Save** to save the project.

The wizard has a progress bar and a logger box, where you can see the status of every operation.
A red progress bar means that the toolkit is busy. Every operation must wait for the previous
operation to release the toolkit.
