# Copyright (C) 2023 - 2024 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'toolkit.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QMainWindow, QMenu,
    QMenuBar, QPlainTextEdit, QProgressBar, QPushButton,
    QSizePolicy, QSpacerItem, QStatusBar, QTabWidget,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(890, 1178)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.action_save_project = QAction(MainWindow)
        self.action_save_project.setObjectName(u"action_save_project")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.main_menu = QWidget(self.centralwidget)
        self.main_menu.setObjectName(u"main_menu")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.main_menu.sizePolicy().hasHeightForWidth())
        self.main_menu.setSizePolicy(sizePolicy1)
        self.gridLayout = QGridLayout(self.main_menu)
        self.gridLayout.setObjectName(u"gridLayout")
        self.release_button = QPushButton(self.main_menu)
        self.release_button.setObjectName(u"release_button")
        self.release_button.setMinimumSize(QSize(0, 40))

        self.gridLayout.addWidget(self.release_button, 3, 2, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 3, 1, 1, 1)

        self.release_and_exit_button = QPushButton(self.main_menu)
        self.release_and_exit_button.setObjectName(u"release_and_exit_button")
        self.release_and_exit_button.setMinimumSize(QSize(0, 40))

        self.gridLayout.addWidget(self.release_and_exit_button, 3, 3, 1, 1)

        self.toolkit_tab = QTabWidget(self.main_menu)
        self.toolkit_tab.setObjectName(u"toolkit_tab")
        sizePolicy1.setHeightForWidth(self.toolkit_tab.sizePolicy().hasHeightForWidth())
        self.toolkit_tab.setSizePolicy(sizePolicy1)
        self.toolkit_tab.setTabShape(QTabWidget.Triangular)
        self.AEDTsettings = QWidget()
        self.AEDTsettings.setObjectName(u"AEDTsettings")
        self.horizontalLayout_25 = QHBoxLayout(self.AEDTsettings)
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.settings_layout = QVBoxLayout()
        self.settings_layout.setObjectName(u"settings_layout")
        self.cores_layout = QHBoxLayout()
        self.cores_layout.setObjectName(u"cores_layout")
        self.cores_label = QLabel(self.AEDTsettings)
        self.cores_label.setObjectName(u"cores_label")

        self.cores_layout.addWidget(self.cores_label)

        self.horizontalSpacer_30 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.cores_layout.addItem(self.horizontalSpacer_30)

        self.numcores = QLineEdit(self.AEDTsettings)
        self.numcores.setObjectName(u"numcores")

        self.cores_layout.addWidget(self.numcores)


        self.settings_layout.addLayout(self.cores_layout)

        self.graphical_layout = QHBoxLayout()
        self.graphical_layout.setObjectName(u"graphical_layout")
        self.graphical_label = QLabel(self.AEDTsettings)
        self.graphical_label.setObjectName(u"graphical_label")

        self.graphical_layout.addWidget(self.graphical_label)

        self.non_graphical_combo = QComboBox(self.AEDTsettings)
        self.non_graphical_combo.addItem("")
        self.non_graphical_combo.addItem("")
        self.non_graphical_combo.setObjectName(u"non_graphical_combo")

        self.graphical_layout.addWidget(self.non_graphical_combo)


        self.settings_layout.addLayout(self.graphical_layout)

        self.aedt_version_layout = QHBoxLayout()
        self.aedt_version_layout.setObjectName(u"aedt_version_layout")
        self.version_label = QLabel(self.AEDTsettings)
        self.version_label.setObjectName(u"version_label")

        self.aedt_version_layout.addWidget(self.version_label)

        self.aedt_version_combo = QComboBox(self.AEDTsettings)
        self.aedt_version_combo.setObjectName(u"aedt_version_combo")

        self.aedt_version_layout.addWidget(self.aedt_version_combo)


        self.settings_layout.addLayout(self.aedt_version_layout)

        self.aedt_sessions_layout = QHBoxLayout()
        self.aedt_sessions_layout.setObjectName(u"aedt_sessions_layout")
        self.aedt_sessions_label = QLabel(self.AEDTsettings)
        self.aedt_sessions_label.setObjectName(u"aedt_sessions_label")

        self.aedt_sessions_layout.addWidget(self.aedt_sessions_label)

        self.process_id_combo = QComboBox(self.AEDTsettings)
        self.process_id_combo.addItem("")
        self.process_id_combo.setObjectName(u"process_id_combo")

        self.aedt_sessions_layout.addWidget(self.process_id_combo)


        self.settings_layout.addLayout(self.aedt_sessions_layout)

        self.project_path_layout = QHBoxLayout()
        self.project_path_layout.setObjectName(u"project_path_layout")
        self.project_path_label = QLabel(self.AEDTsettings)
        self.project_path_label.setObjectName(u"project_path_label")

        self.project_path_layout.addWidget(self.project_path_label)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.project_path_layout.addItem(self.horizontalSpacer_2)

        self.project_name = QLineEdit(self.AEDTsettings)
        self.project_name.setObjectName(u"project_name")

        self.project_path_layout.addWidget(self.project_name)


        self.settings_layout.addLayout(self.project_path_layout)

        self.select_aedt_proj_layout = QHBoxLayout()
        self.select_aedt_proj_layout.setObjectName(u"select_aedt_proj_layout")
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.select_aedt_proj_layout.addItem(self.horizontalSpacer_5)

        self.browse_project = QPushButton(self.AEDTsettings)
        self.browse_project.setObjectName(u"browse_project")

        self.select_aedt_proj_layout.addWidget(self.browse_project)


        self.settings_layout.addLayout(self.select_aedt_proj_layout)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")

        self.settings_layout.addLayout(self.horizontalLayout_5)

        self.verticalSpacer_8 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.settings_layout.addItem(self.verticalSpacer_8)

        self.connect_aedtapp = QPushButton(self.AEDTsettings)
        self.connect_aedtapp.setObjectName(u"connect_aedtapp")
        self.connect_aedtapp.setEnabled(True)
        self.connect_aedtapp.setMinimumSize(QSize(0, 40))

        self.settings_layout.addWidget(self.connect_aedtapp)


        self.horizontalLayout_25.addLayout(self.settings_layout)

        self.horizontalSpacer_29 = QSpacerItem(40, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_25.addItem(self.horizontalSpacer_29)

        self.toolkit_tab.addTab(self.AEDTsettings, "")
        self.Segmentation = QWidget()
        self.Segmentation.setObjectName(u"Segmentation")
        self.horizontalLayout_ = QHBoxLayout(self.Segmentation)
        self.horizontalLayout_.setObjectName(u"horizontalLayout_")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.projects_label_2 = QLabel(self.Segmentation)
        self.projects_label_2.setObjectName(u"projects_label_2")

        self.horizontalLayout_3.addWidget(self.projects_label_2)

        self.projects_aedt_combo = QComboBox(self.Segmentation)
        self.projects_aedt_combo.addItem("")
        self.projects_aedt_combo.setObjectName(u"projects_aedt_combo")

        self.horizontalLayout_3.addWidget(self.projects_aedt_combo)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.designs_label = QLabel(self.Segmentation)
        self.designs_label.setObjectName(u"designs_label")

        self.horizontalLayout_6.addWidget(self.designs_label)

        self.design_aedt_combo = QComboBox(self.Segmentation)
        self.design_aedt_combo.addItem("")
        self.design_aedt_combo.setObjectName(u"design_aedt_combo")

        self.horizontalLayout_6.addWidget(self.design_aedt_combo)


        self.verticalLayout_2.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_66 = QHBoxLayout()
        self.horizontalLayout_66.setObjectName(u"horizontalLayout_66")
        self.motor_type = QLabel(self.Segmentation)
        self.motor_type.setObjectName(u"motor_type")

        self.horizontalLayout_66.addWidget(self.motor_type)

        self.motor_type_combo = QComboBox(self.Segmentation)
        self.motor_type_combo.addItem("")
        self.motor_type_combo.setObjectName(u"motor_type_combo")

        self.horizontalLayout_66.addWidget(self.motor_type_combo)


        self.verticalLayout_2.addLayout(self.horizontalLayout_66)

        self.horizontalLayout_32 = QHBoxLayout()
        self.horizontalLayout_32.setObjectName(u"horizontalLayout_32")
        self.label_19 = QLabel(self.Segmentation)
        self.label_19.setObjectName(u"label_19")

        self.horizontalLayout_32.addWidget(self.label_19)

        self.apply_mesh_sheets = QComboBox(self.Segmentation)
        self.apply_mesh_sheets.addItem("")
        self.apply_mesh_sheets.addItem("")
        self.apply_mesh_sheets.setObjectName(u"apply_mesh_sheets")

        self.horizontalLayout_32.addWidget(self.apply_mesh_sheets)


        self.verticalLayout_2.addLayout(self.horizontalLayout_32)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_12 = QLabel(self.Segmentation)
        self.label_12.setObjectName(u"label_12")

        self.horizontalLayout_4.addWidget(self.label_12)

        self.is_skewed = QComboBox(self.Segmentation)
        self.is_skewed.addItem("")
        self.is_skewed.addItem("")
        self.is_skewed.setObjectName(u"is_skewed")

        self.horizontalLayout_4.addWidget(self.is_skewed)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_13 = QLabel(self.Segmentation)
        self.label_13.setObjectName(u"label_13")

        self.horizontalLayout_7.addWidget(self.label_13)

        self.magnets_material = QComboBox(self.Segmentation)
        self.magnets_material.addItem("")
        self.magnets_material.setObjectName(u"magnets_material")

        self.horizontalLayout_7.addWidget(self.magnets_material)


        self.verticalLayout_2.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_20 = QHBoxLayout()
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.label_14 = QLabel(self.Segmentation)
        self.label_14.setObjectName(u"label_14")

        self.horizontalLayout_20.addWidget(self.label_14)

        self.rotor_material = QComboBox(self.Segmentation)
        self.rotor_material.addItem("")
        self.rotor_material.setObjectName(u"rotor_material")

        self.horizontalLayout_20.addWidget(self.rotor_material)


        self.verticalLayout_2.addLayout(self.horizontalLayout_20)

        self.horizontalLayout_20a = QHBoxLayout()
        self.horizontalLayout_20a.setObjectName(u"horizontalLayout_20a")
        self.label_14a = QLabel(self.Segmentation)
        self.label_14a.setObjectName(u"label_14a")

        self.horizontalLayout_20a.addWidget(self.label_14a)

        self.stator_material = QComboBox(self.Segmentation)
        self.stator_material.addItem("")
        self.stator_material.setObjectName(u"stator_material")

        self.horizontalLayout_20a.addWidget(self.stator_material)


        self.verticalLayout_2.addLayout(self.horizontalLayout_20a)

        self.horizontalLayout_21 = QHBoxLayout()
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.label_15 = QLabel(self.Segmentation)
        self.label_15.setObjectName(u"label_15")

        self.horizontalLayout_21.addWidget(self.label_15)

        self.horizontalSpacer_21 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_21.addItem(self.horizontalSpacer_21)

        self.rotor_slices = QLineEdit(self.Segmentation)
        self.rotor_slices.setObjectName(u"rotor_slices")

        self.horizontalLayout_21.addWidget(self.rotor_slices)


        self.verticalLayout_2.addLayout(self.horizontalLayout_21)

        self.horizontalLayout_22 = QHBoxLayout()
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.label_16 = QLabel(self.Segmentation)
        self.label_16.setObjectName(u"label_16")

        self.horizontalLayout_22.addWidget(self.label_16)

        self.horizontalSpacer_22 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_22.addItem(self.horizontalSpacer_22)

        self.magnet_segments_per_slice = QLineEdit(self.Segmentation)
        self.magnet_segments_per_slice.setObjectName(u"magnet_segments_per_slice")

        self.horizontalLayout_22.addWidget(self.magnet_segments_per_slice)


        self.verticalLayout_2.addLayout(self.horizontalLayout_22)

        self.horizontalLayout_33 = QHBoxLayout()
        self.horizontalLayout_33.setObjectName(u"horizontalLayout_33")
        self.label_20 = QLabel(self.Segmentation)
        self.label_20.setObjectName(u"label_20")

        self.horizontalLayout_33.addWidget(self.label_20)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_33.addItem(self.horizontalSpacer_3)

        self.mesh_sheets_number = QLineEdit(self.Segmentation)
        self.mesh_sheets_number.setObjectName(u"mesh_sheets_number")

        self.horizontalLayout_33.addWidget(self.mesh_sheets_number)


        self.verticalLayout_2.addLayout(self.horizontalLayout_33)

        self.horizontalLayout_23 = QHBoxLayout()
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.label_17 = QLabel(self.Segmentation)
        self.label_17.setObjectName(u"label_17")

        self.horizontalLayout_23.addWidget(self.label_17)

        self.horizontalSpacer_23 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_23.addItem(self.horizontalSpacer_23)

        self.skew_angle = QLineEdit(self.Segmentation)
        self.skew_angle.setObjectName(u"skew_angle")

        self.horizontalLayout_23.addWidget(self.skew_angle)


        self.verticalLayout_2.addLayout(self.horizontalLayout_23)

        self.perform_segmentation = QPushButton(self.Segmentation)
        self.perform_segmentation.setObjectName(u"perform_segmentation")
        self.perform_segmentation.setEnabled(True)
        self.perform_segmentation.setMinimumSize(QSize(0, 40))
        self.perform_segmentation.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout_2.addWidget(self.perform_segmentation)

        self.skew = QPushButton(self.Segmentation)
        self.skew.setObjectName(u"skew")
        self.skew.setEnabled(True)
        self.skew.setMinimumSize(QSize(0, 40))

        self.verticalLayout_2.addWidget(self.skew)


        self.horizontalLayout_.addLayout(self.verticalLayout_2)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_.addItem(self.horizontalSpacer_4)

        self.toolkit_tab.addTab(self.Segmentation, "")
        self.Post_Processing = QWidget()
        self.Post_Processing.setObjectName(u"Post_Processing")
        self.verticalLayoutWidget = QWidget(self.Post_Processing)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(9, 9, 701, 441))
        self.verticalLayout_3 = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.verticalLayoutWidget)
        self.label.setObjectName(u"label")
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)
        self.label.setMinimumSize(QSize(0, 0))

        self.horizontalLayout.addWidget(self.label)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_6)

        self.setup_name = QLineEdit(self.verticalLayoutWidget)
        self.setup_name.setObjectName(u"setup_name")

        self.horizontalLayout.addWidget(self.setup_name)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.validate_and_analyze = QPushButton(self.verticalLayoutWidget)
        self.validate_and_analyze.setObjectName(u"validate_and_analyze")
        self.validate_and_analyze.setMinimumSize(QSize(0, 40))
        self.validate_and_analyze.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout_3.addWidget(self.validate_and_analyze)

        self.get_magnet_loss = QPushButton(self.verticalLayoutWidget)
        self.get_magnet_loss.setObjectName(u"get_magnet_loss")
        self.get_magnet_loss.setMinimumSize(QSize(0, 40))
        self.get_magnet_loss.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout_3.addWidget(self.get_magnet_loss)

        self.toolkit_tab.addTab(self.Post_Processing, "")

        self.gridLayout.addWidget(self.toolkit_tab, 0, 0, 1, 5)


        self.verticalLayout.addWidget(self.main_menu)

        self.log_text = QPlainTextEdit(self.centralwidget)
        self.log_text.setObjectName(u"log_text")
        sizePolicy.setHeightForWidth(self.log_text.sizePolicy().hasHeightForWidth())
        self.log_text.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.log_text)

        self.progress_bar = QProgressBar(self.centralwidget)
        self.progress_bar.setObjectName(u"progress_bar")
        self.progress_bar.setFocusPolicy(Qt.NoFocus)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setOrientation(Qt.Horizontal)
        self.progress_bar.setTextDirection(QProgressBar.TopToBottom)

        self.verticalLayout.addWidget(self.progress_bar)

        MainWindow.setCentralWidget(self.centralwidget)
        self.top_menu_bar = QMenuBar(MainWindow)
        self.top_menu_bar.setObjectName(u"top_menu_bar")
        self.top_menu_bar.setGeometry(QRect(0, 0, 890, 28))
        font = QFont()
        font.setPointSize(12)
        self.top_menu_bar.setFont(font)
        self.top_menu = QMenu(self.top_menu_bar)
        self.top_menu.setObjectName(u"top_menu")
        self.top_menu.setFont(font)
        MainWindow.setMenuBar(self.top_menu_bar)
        self.status_bar = QStatusBar(MainWindow)
        self.status_bar.setObjectName(u"status_bar")
        MainWindow.setStatusBar(self.status_bar)

        self.top_menu_bar.addAction(self.top_menu.menuAction())
        self.top_menu.addAction(self.action_save_project)

        self.retranslateUi(MainWindow)

        self.toolkit_tab.setCurrentIndex(0)
        self.projects_aedt_combo.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.action_save_project.setText(QCoreApplication.translate("MainWindow", u"Save project", None))
        self.release_button.setText(QCoreApplication.translate("MainWindow", u" Close Toolkit ", None))
        self.release_and_exit_button.setText(QCoreApplication.translate("MainWindow", u" Close AEDT and Toolkit ", None))
        self.cores_label.setText(QCoreApplication.translate("MainWindow", u"Number of Cores", None))
        self.numcores.setText(QCoreApplication.translate("MainWindow", u"4", None))
        self.graphical_label.setText(QCoreApplication.translate("MainWindow", u"Non Graphical", None))
        self.non_graphical_combo.setItemText(0, QCoreApplication.translate("MainWindow", u"False", None))
        self.non_graphical_combo.setItemText(1, QCoreApplication.translate("MainWindow", u"True", None))

        self.version_label.setText(QCoreApplication.translate("MainWindow", u"AEDT Version", None))
        self.aedt_sessions_label.setText(QCoreApplication.translate("MainWindow", u"Available AEDT Sessions", None))
        self.process_id_combo.setItemText(0, QCoreApplication.translate("MainWindow", u"Create New Session", None))

        self.project_path_label.setText(QCoreApplication.translate("MainWindow", u"Project Name", None))
        self.browse_project.setText(QCoreApplication.translate("MainWindow", u"Select AEDT project", None))
        self.connect_aedtapp.setText(QCoreApplication.translate("MainWindow", u"Launch AEDT", None))
        self.toolkit_tab.setTabText(self.toolkit_tab.indexOf(self.AEDTsettings), QCoreApplication.translate("MainWindow", u" AEDT Settings ", None))
        self.projects_label_2.setText(QCoreApplication.translate("MainWindow", u"Projects", None))
        self.projects_aedt_combo.setItemText(0, QCoreApplication.translate("MainWindow", u"--Select Project--", None))

        self.designs_label.setText(QCoreApplication.translate("MainWindow", u"Designs", None))
        self.design_aedt_combo.setItemText(0, QCoreApplication.translate("MainWindow", u"--Select Design--", None))

        self.design_aedt_combo.setCurrentText(QCoreApplication.translate("MainWindow", u"--Select Design--", None))
        self.motor_type.setText(QCoreApplication.translate("MainWindow", u"Motor Type", None))
        self.motor_type_combo.setItemText(0, QCoreApplication.translate("MainWindow", u"--Select Motor Type--", None))

        self.motor_type_combo.setCurrentText(QCoreApplication.translate("MainWindow", u"--Select Motor Type--", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"Apply Mesh Sheets", None))
        self.apply_mesh_sheets.setItemText(0, QCoreApplication.translate("MainWindow", u"False", None))
        self.apply_mesh_sheets.setItemText(1, QCoreApplication.translate("MainWindow", u"True", None))

        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Is Skewed", None))
        self.is_skewed.setItemText(0, QCoreApplication.translate("MainWindow", u"False", None))
        self.is_skewed.setItemText(1, QCoreApplication.translate("MainWindow", u"True", None))

        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Magnets Material", None))
        self.magnets_material.setItemText(0, QCoreApplication.translate("MainWindow", u"--Select Material--", None))

        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Rotor Material", None))
        self.rotor_material.setItemText(0, QCoreApplication.translate("MainWindow", u"--Select Material--", None))

        self.label_14a.setText(QCoreApplication.translate("MainWindow", u"Stator Material", None))
        self.stator_material.setItemText(0, QCoreApplication.translate("MainWindow", u"--Select Material--", None))

        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Rotor Slices", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Magnet Segments Per Slice", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"Mesh Sheets Number", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"Skew Angle (deg)", None))
        self.perform_segmentation.setText(QCoreApplication.translate("MainWindow", u"Perform Segmentation", None))
        self.skew.setText(QCoreApplication.translate("MainWindow", u"Apply Skew", None))
        self.toolkit_tab.setTabText(self.toolkit_tab.indexOf(self.Segmentation), QCoreApplication.translate("MainWindow", u"Segmentation", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Setup to analyze", None))
        self.validate_and_analyze.setText(QCoreApplication.translate("MainWindow", u"Validate and Analyze", None))
        self.get_magnet_loss.setText(QCoreApplication.translate("MainWindow", u"Get Magnet Loss", None))
        self.toolkit_tab.setTabText(self.toolkit_tab.indexOf(self.Post_Processing), QCoreApplication.translate("MainWindow", u" Post-Processing ", None))
        self.top_menu.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
    # retranslateUi

