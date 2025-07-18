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
   connecting to an existing AEDT session and click **Connect to AEDT**.

   .. image:: ../_static/settings_tab.png
     :width: 800
     :alt: Settings tab

#. Choose project and design from the drop-down list in the **Home menu**.

   .. image:: ../_static/home_menu.png
     :width: 800
     :alt: Project tab

#. Click on the **Segmentation menu** to specify segmentation settings.

   .. image:: ../_static/segmentation_menu.png
     :width: 800
     :alt: Segmentation tab

#. At the bottom of the tab, click **Perform Segmentation** and then **Apply Skew**.

#. Click on the **Post-processing menu** to select the desired setup to validate and analyze.

   .. image:: ../_static/post_processing_menu.png
     :width: 800
     :alt: Post-processing tab

#. Click on **Get Magnet Loss** to automatically compute Magnet Loss in AEDT.
   The report is automatically generated in AEDT.

#. Click on the **Design menu** to visualize within the toolkit the segmented magnets.

    .. image:: ../_static/view_model.png
       :width: 800
       :alt: Design menu tab

#. The wizard has a progress circle and a logger box where you can see the status of
   every operation. Every operation must wait for the previous operation to release the toolkit.

    .. image:: ../_static/logger.png
       :width: 800
       :alt: Logger tab
