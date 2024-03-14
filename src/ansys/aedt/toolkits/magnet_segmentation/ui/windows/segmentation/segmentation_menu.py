from PySide6.QtCore import QThread
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QComboBox
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QPushButton

from pyaedt.generic.general_methods import _to_boolean

from windows.segmentation.segmentation_page import Ui_Segmentation
from windows.segmentation.segmentation_column import Ui_LeftColumn

# toolkit PySide6 Widgets
from ansys.aedt.toolkits.common.ui.utils.widgets import PyLabel


class SegmentationThread(QThread):
    finished_signal = Signal(bool)

    def __init__(self, app, selected_project, selected_design):
        super().__init__()
        self.segmentation_menu = app
        self.main_window = app.main_window
        self.selected_project = selected_project
        self.selected_design = selected_design

    def run(self):
        success = self.main_window.apply_segmentation(
            self.selected_project, self.selected_design
        )
        self.finished_signal.emit(success)

class SkewThread(QThread):
    finished_signal = Signal(bool)

    def __init__(self, app, selected_project, selected_design):
        super().__init__()
        self.segmentation_menu = app
        self.main_window = app.main_window
        self.selected_project = selected_project
        self.selected_design = selected_design

    def run(self):
        success = self.main_window.apply_skew(
            self.selected_project, self.selected_design
        )
        self.finished_signal.emit(success)


class SegmentationMenu(object):
    def __init__(self, main_window):
        # General properties
        self.main_window = main_window
        self.ui = main_window.ui

        # Add page
        segmentation_menu_index = self.ui.add_page(Ui_Segmentation)
        self.ui.load_pages.pages.setCurrentIndex(segmentation_menu_index)
        self.segmentation_menu_widget = self.ui.load_pages.pages.currentWidget()

        # Add left column
        new_column_widget = QWidget()
        new_ui = Ui_LeftColumn()
        new_ui.setupUi(new_column_widget)
        self.ui.left_column.menus.menus.addWidget(new_column_widget)
        self.segmentation_column_widget = new_column_widget
        self.segmentation_column_vertical_layout = new_ui.segmentation_vertical_layout

        # Specific properties
        # Combo boxes
        self.projects_aedt_combo = self.segmentation_menu_widget.findChild(QComboBox, "projects_aedt_combo")
        self.design_aedt_combo = self.segmentation_menu_widget.findChild(QComboBox, "design_aedt_combo")
        self.motor_type_combo = self.segmentation_menu_widget.findChild(QComboBox, "motor_type_combo")
        self.apply_mesh_sheets = self.segmentation_menu_widget.findChild(QComboBox, "apply_mesh_sheets")
        self.is_skewed = self.segmentation_menu_widget.findChild(QComboBox, "is_skewed")
        self.magnets_material = self.segmentation_menu_widget.findChild(QComboBox, "magnets_material")
        self.rotor_material = self.segmentation_menu_widget.findChild(QComboBox, "rotor_material")
        self.stator_material = self.segmentation_menu_widget.findChild(QComboBox, "stator_material")
        # LineEdits
        self.rotor_slices = self.segmentation_menu_widget.findChild(QLineEdit, "rotor_slices")
        self.magnet_segments_per_slice = self.segmentation_menu_widget.findChild(QLineEdit, "magnet_segments_per_slice")
        self.mesh_sheets_number = self.segmentation_menu_widget.findChild(QLineEdit, "mesh_sheets_number")
        self.skew_angle = self.segmentation_menu_widget.findChild(QLineEdit, "skew_angle")
        # Labels
        self.projects_aedt_combo_label = self.segmentation_menu_widget.findChild(QLabel, "projects_aedt_combo_label")
        self.design_aedt_combo_label = self.segmentation_menu_widget.findChild(QLabel, "design_aedt_combo_label")
        self.motor_type_combo_label = self.segmentation_menu_widget.findChild(QLabel, "motor_type_combo_label")
        self.apply_mesh_sheets_label = self.segmentation_menu_widget.findChild(QLabel, "apply_mesh_sheets_label")
        self.is_skewed_label = self.segmentation_menu_widget.findChild(QLabel, "is_skewed_label")
        self.magnets_material_label = self.segmentation_menu_widget.findChild(QLabel, "magnets_material_label")
        self.rotor_material_label = self.segmentation_menu_widget.findChild(QLabel, "rotor_material_label")
        self.stator_material_label = self.segmentation_menu_widget.findChild(QLabel, "stator_material_label")
        self.rotor_slices_label = self.segmentation_menu_widget.findChild(QLabel, "rotor_slices_label")
        self.magnet_segments_per_slice_label = self.segmentation_menu_widget.findChild(QLabel, "magnet_segments_per_slice_label")
        self.mesh_sheets_number_label = self.segmentation_menu_widget.findChild(QLabel, "mesh_sheets_number_label")
        self.skew_angle_label = self.segmentation_menu_widget.findChild(QLabel, "skew_angle_label")
        # Buttons
        self.perform_segmentation_button = self.segmentation_menu_widget.findChild(QPushButton, "perform_segmentation")
        self.apply_skew_button = self.segmentation_menu_widget.findChild(QPushButton, "skew")
        self.segmentation_thread = None
        self.skew_thread = None

    def setup(self):
        # Modify theme
        app_color = self.main_window.ui.themes["app_color"]
        text_color = app_color["text_active"]
        background = app_color["dark_three"]

        self.perform_segmentation_button.clicked.connect(self.segmentation_button_clicked)
        self.apply_skew_button.clicked.connect(self.skew_button_clicked)

        # Motor Type
        # Add in UI
        self.motor_type_combo.addItems(["IPM", "SPM"])

        # UI from Designer
        # Combo boxes
        combo_box_style = """
            QComboBox {{
                border: none;
                padding: 10px;
                color: {_color};
                background-color: {_bg_color};
                selection-background-color: red;
                font-size: {_font_size}pt;
            }}
            QComboBox QAbstractItemView {{
                border: none;
                background-color: {_bg_color};
                color: {_color};
            }}
        """
        custom_style = combo_box_style.format(
            _color=text_color, _bg_color=background, _font_size=self.main_window.properties.font["title_size"]
        )
        self.projects_aedt_combo.setStyleSheet(custom_style)
        self.design_aedt_combo.setStyleSheet(custom_style)
        self.motor_type_combo.setStyleSheet(custom_style)
        self.apply_mesh_sheets.setStyleSheet(custom_style)
        self.is_skewed.setStyleSheet(custom_style)
        self.magnets_material.setStyleSheet(custom_style)
        self.rotor_material.setStyleSheet(custom_style)
        self.stator_material.setStyleSheet(custom_style)

        # Multiplier line
        line_style = """
            QLineEdit {{
            border: none;
            padding: 10px;
            color: {_color};
            background-color: {_bg_color};
            selection-background-color: red;
            font-size: {_font_size}pt;
            }}
        """
        custom_style = line_style.format(
            _color=text_color, _bg_color=background, _font_size=self.main_window.properties.font["title_size"]
        )
        self.rotor_slices.setStyleSheet(custom_style)
        self.magnet_segments_per_slice.setStyleSheet(custom_style)
        self.mesh_sheets_number.setStyleSheet(custom_style)
        self.skew_angle.setStyleSheet(custom_style)

        # Multiplier label button
        multiplier_label_style = """
                    QLabel {{
                    color: {_color};
                    font-size: {_font_size}pt;
                    font-weight: bold;
                    }}
                    """
        custom_style = multiplier_label_style.format(
            _color=text_color, _bg_color=background, _font_size=self.main_window.properties.font["title_size"]
        )
        self.projects_aedt_combo_label.setStyleSheet(custom_style)
        self.design_aedt_combo_label.setStyleSheet(custom_style)
        self.motor_type_combo_label.setStyleSheet(custom_style)
        self.apply_mesh_sheets_label.setStyleSheet(custom_style)
        self.is_skewed_label.setStyleSheet(custom_style)
        self.magnets_material_label.setStyleSheet(custom_style)
        self.rotor_material_label.setStyleSheet(custom_style)
        self.stator_material_label.setStyleSheet(custom_style)
        self.rotor_slices_label.setStyleSheet(custom_style)
        self.magnet_segments_per_slice_label.setStyleSheet(custom_style)
        self.mesh_sheets_number_label.setStyleSheet(custom_style)
        self.skew_angle_label.setStyleSheet(custom_style)

        # Geometry label button
        select_geometry_label_style = """
                            QLabel {{
                            color: {_color};
                            font-size: {_font_size}pt;
                            font-weight: bold;
                            }}
                            """
        custom_style = select_geometry_label_style.format(
            _color=text_color, _bg_color=background, _font_size=self.main_window.properties.font["title_size"]
        )
        self.perform_segmentation_button.setStyleSheet(custom_style)
        self.apply_skew_button.setStyleSheet(custom_style)

        # Set Column
        msg = "Segmentation"
        label_widget = PyLabel(
            text=msg,
            font_size=self.ui.app.properties.font["title_size"],
            color=self.ui.themes["app_color"]["text_description"])
        self.segmentation_column_vertical_layout.addWidget(label_widget)

    def segmentation_button_clicked(self):
        if not self.main_window.check_connection():
            msg = "Backend not running."
            self.ui.update_logger(msg)
            return False

        if (self.segmentation_thread or self.skew_thread
                and self.segmentation_thread.isRunning() or self.skew_thread.isRunning()
                or self.main_window.backend_busy()):
            msg = "Toolkit running"
            self.ui.update_logger(msg)
            self.main_window.logger.debug(msg)
            return False

        be_properties = self.main_window.get_properties()

        be_properties["motor_type"] = self.motor_type_combo.currentText()
        be_properties["is_skewed"] = _to_boolean(self.is_skewed.currentText())
        if not be_properties["is_skewed"]:
            be_properties["rotor_material"] = self.rotor_material.currentText()
            be_properties["stator_material"] = self.stator_material.currentText()
            be_properties["rotor_slices"] = int(self.rotor_slices.text())
            be_properties["skew_angle"] = self.skew_angle.text()
        be_properties["apply_mesh_sheets"] = _to_boolean(self.apply_mesh_sheets.currentText())
        if be_properties["apply_mesh_sheets"]:
            be_properties["mesh_sheets_number"] = int(self.mesh_sheets_number.text())
        be_properties["magnets_material"] = self.magnets_material.currentText()
        be_properties["magnet_segments_per_slice"] = int(self.magnet_segments_per_slice.text())
        # be_properties.setup_to_analyze = self.setup_to_analyze.text()
        be_properties["active_project"] = self.projects_aedt_combo.currentText()
        be_properties["active_design"] = self.design_aedt_combo.currentText()

        self.main_window.set_properties(be_properties)

        if be_properties.get("active_project"):
            self.ui.update_progress(0)
            selected_project = self.main_window.home_menu.project_combobox.currentText()
            selected_design = self.main_window.home_menu.design_combobox.currentText()

            # Start a separate thread for the backend call
            self.segmentation_thread = SegmentationThread(
                app=self,
                selected_project=selected_project,
                selected_design=selected_design,
            )
            self.segmentation_thread.finished_signal.connect(self.process_finished)

            msg = "Segmentation successfull."
            self.ui.update_logger(msg)

            self.segmentation_thread.start()
        else:
            self.ui.update_logger("Toolkit not connect to AEDT.")

    def skew_button_clicked(self):
        if not self.main_window.check_connection():
            msg = "Backend not running."
            self.ui.update_logger(msg)
            return False

        if (self.segmentation_thread or self.skew_thread
                and self.segmentation_thread.isRunning() or self.skew_thread.isRunning()
                or self.main_window.backend_busy()):
            msg = "Toolkit running"
            self.ui.update_logger(msg)
            self.main_window.logger.debug(msg)
            return False

        be_properties = self.main_window.get_properties()

        self.main_window.set_properties(be_properties)

        if be_properties.get("active_project"):
            self.ui.update_progress(0)
            selected_project = self.main_window.home_menu.project_combobox.currentText()
            selected_design = self.main_window.home_menu.design_combobox.currentText()

            # Start a separate thread for the backend call
            self.skew_thread = SkewThread(
                app=self,
                selected_project=selected_project,
                selected_design=selected_design,
            )
            self.skew_thread.finished_signal.connect(self.process_finished)

            msg = "Segmentation successfull."
            self.ui.update_logger(msg)

            self.skew_thread.start()
        else:
            self.ui.update_logger("Toolkit not connect to AEDT.")

    def process_finished(self, success):
        self.ui.update_progress(100)
        selected_project = self.main_window.home_menu.project_combobox.currentText()
        selected_design = self.main_window.home_menu.design_combobox.currentText()

        # Populate combo boxes
        # Materials
        materials = self.main_window.get_materials()
        for mat in materials:
            self.magnets_material.addItem(mat)
            self.rotor_material.addItem(mat)
            self.stator_material.addItem(mat)

        properties = self.main_window.get_properties()
        active_project = self.main_window.get_project_name(properties["active_project"])
        active_design = properties["active_design"]
        if active_project != selected_project or active_design != selected_design:
            self.main_window.home_menu.update_project()
            self.main_window.home_menu.update_design()

        if success:
            msg = "Process successfully finished."
            self.ui.update_logger(msg)
        else:
            msg = f"Failed backend call: {self.main_window.url}"
            self.ui.update_logger(msg)
