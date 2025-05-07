from PySide6.QtCore import QThread
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QComboBox
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QPushButton

from ansys.aedt.toolkits.magnet_segmentation.ui.windows.post_processing.post_processing_page import Ui_PostProcessing
from ansys.aedt.toolkits.magnet_segmentation.ui.windows.post_processing.post_processing_column import Ui_LeftColumn

# toolkit PySide6 Widgets
from ansys.aedt.toolkits.common.ui.utils.widgets import PyLabel


class ValidateAnalyzeThread(QThread):
    finished_signal = Signal(bool)

    def __init__(self, app, selected_project, selected_design):
        super().__init__()
        self.post_processing_menu = app
        self.main_window = app.main_window
        self.selected_project = selected_project
        self.selected_design = selected_design
        self.is_finished = False

    def run(self):
        self.is_finished = self.main_window.val_check_and_analysis(
            self.selected_project, self.selected_design
        )
        self.finished_signal.emit(self.is_finished)


class MagnetLossThread(QThread):
    finished_signal = Signal(bool)

    def __init__(self, app, selected_project, selected_design):
        super().__init__()
        self.post_processing_menu = app
        self.main_window = app.main_window
        self.selected_project = selected_project
        self.selected_design = selected_design
        self.is_finished = False

    def run(self):
        self.is_finished = self.main_window.get_report(
            self.selected_project, self.selected_design
        )
        self.finished_signal.emit(self.is_finished)


class PostProcessingMenu(object):
    def __init__(self, main_window):
        # General properties
        self.main_window = main_window
        self.ui = main_window.ui

        # Add page
        postprocessing_menu_index = self.ui.add_page(Ui_PostProcessing)
        self.ui.load_pages.pages.setCurrentIndex(postprocessing_menu_index)
        self.postprocessing_menu_widget = self.ui.load_pages.pages.currentWidget()

        # Add left column
        new_column_widget = QWidget()
        new_ui = Ui_LeftColumn()
        new_ui.setupUi(new_column_widget)
        self.ui.left_column.menus.menus.addWidget(new_column_widget)
        self.postprocessing_column_widget = new_column_widget
        self.postprocessing_column_vertical_layout = new_ui.postprocessing_vertical_layout

        # Specific properties
        # Labels
        self.setup_name_label = self.postprocessing_menu_widget.findChild(QLabel, "setup_name_label")
        # Combobox
        self.setup_name_combo = self.postprocessing_menu_widget.findChild(QComboBox, "setup_name_combo")
        # Buttons
        self.validate_and_analyze_button = self.postprocessing_menu_widget.findChild(QPushButton,
                                                                                     "validate_and_analyze")
        self.get_magnet_loss_button = self.postprocessing_menu_widget.findChild(QPushButton, "get_magnet_loss")
        self.validate_analyze_thread = None
        self.magnet_loss_thread = None

    def setup(self):
        # Modify theme
        app_color = self.main_window.ui.themes["app_color"]
        text_color = app_color["text_active"]
        background = app_color["dark_three"]

        self.validate_and_analyze_button.clicked.connect(self.validate_analyze_button_clicked)
        self.get_magnet_loss_button.clicked.connect(self.magnet_loss_button_clicked)

        # UI from Designer
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
        self.setup_name_label.setStyleSheet(custom_style)

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
        self.validate_and_analyze_button.setStyleSheet(custom_style)
        self.get_magnet_loss_button.setStyleSheet(custom_style)

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
        self.setup_name_combo.setStyleSheet(custom_style)

        # Set Column
        msg = "Post-Processing"
        label_widget = PyLabel(
            text=msg,
            font_size=self.ui.app.properties.font["title_size"],
            color=self.ui.themes["app_color"]["text_description"])
        self.postprocessing_column_vertical_layout.addWidget(label_widget)

    def validate_analyze_button_clicked(self):
        if not self.main_window.check_connection():
            msg = "Backend not running."
            self.ui.update_logger(msg)
            return False

        if (self.validate_analyze_thread and self.validate_analyze_thread.isRunning()
                or self.magnet_loss_thread and self.magnet_loss_thread.isRunning()
                or self.main_window.backend_busy()):
            msg = "Toolkit running"
            self.ui.update_logger(msg)
            self.main_window.logger.debug(msg)
            return False

        be_properties = self.main_window.get_properties()

        be_properties["setup_to_analyze"] = self.setup_name_combo.currentText()

        self.main_window.set_properties(be_properties)

        if be_properties.get("active_project"):
            self.ui.update_progress(0)
            selected_project = self.main_window.home_menu.project_combobox.currentText()
            selected_design = self.main_window.home_menu.design_combobox.currentText()

            # Start a separate thread for the backend call
            self.validate_analyze_thread = ValidateAnalyzeThread(
                app=self,
                selected_project=selected_project,
                selected_design=selected_design,
            )
            self.validate_analyze_thread.finished_signal.connect(self.validate_analyze_process_finished)

            self.validate_analyze_thread.start()
        else:
            self.ui.update_logger("Toolkit not connected to AEDT.")

    def magnet_loss_button_clicked(self):
        if not self.main_window.check_connection():
            msg = "Backend not running."
            self.ui.update_logger(msg)
            return False

        if (self.validate_analyze_thread and self.validate_analyze_thread.isRunning()
                or self.magnet_loss_thread and self.magnet_loss_thread.isRunning()
                or self.main_window.backend_busy()):
            msg = "Toolkit running"
            self.ui.update_logger(msg)
            self.main_window.logger.debug(msg)
            return False

        be_properties = self.main_window.get_properties()

        if be_properties.get("active_project"):
            self.ui.update_progress(0)
            selected_project = self.main_window.home_menu.project_combobox.currentText()
            selected_design = self.main_window.home_menu.design_combobox.currentText()

            # Start a separate thread for the backend call
            self.magnet_loss_thread = MagnetLossThread(
                app=self,
                selected_project=selected_project,
                selected_design=selected_design,
            )
            self.magnet_loss_thread.finished_signal.connect(self.magnet_loss_process_finished)

            self.magnet_loss_thread.start()
        else:
            self.ui.update_logger("Toolkit not connected to AEDT.")

    def validate_analyze_process_finished(self):
        self.ui.update_progress(100)
        properties = self.main_window.get_properties()
        active_design = properties["active_design"]

        self.main_window.home_menu.update_design()
        self.main_window.home_menu.design_combobox.setCurrentText(active_design)

        if self.validate_analyze_thread.is_finished:
            msg = "Validation and analysis successful."
            self.ui.update_logger(msg)
        else:
            msg = f"Failed backend call: {self.main_window.url}"
            self.ui.update_logger(msg)

    def magnet_loss_process_finished(self):
        self.ui.update_progress(100)
        properties = self.main_window.get_properties()
        active_design = properties["active_design"]

        self.main_window.home_menu.update_design()
        self.main_window.home_menu.design_combobox.setCurrentText(active_design)

        if self.magnet_loss_thread.is_finished:
            msg = "Magnet loss computation successful."
            self.ui.update_logger(msg)
        else:
            msg = f"Failed backend call: {self.main_window.url}"
            self.ui.update_logger(msg)

    def get_setups(self):
        backend_properties = self.ui.app.get_properties()
        setups = []
        if backend_properties.get("active_project") and backend_properties.get("active_design"):
            setups = self.main_window.get_design_setups()
        self.setup_name_combo.clear()
        if setups:
            for setup in setups:
                self.setup_name_combo.addItem(setup)
