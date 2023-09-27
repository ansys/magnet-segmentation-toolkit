# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'toolkit.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
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
    QLabel, QLayout, QLineEdit, QMainWindow,
    QMenu, QMenuBar, QPlainTextEdit, QProgressBar,
    QPushButton, QSizePolicy, QSpacerItem, QStatusBar,
    QTabWidget, QVBoxLayout, QWidget)

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
        self.MotorCADsettings = QWidget()
        self.MotorCADsettings.setObjectName(u"MotorCADsettings")
        self.horizontalLayout_26 = QHBoxLayout(self.MotorCADsettings)
        self.horizontalLayout_26.setObjectName(u"horizontalLayout_26")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setSizeConstraint(QLayout.SetNoConstraint)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.MotorCADsettings)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_7)

        self.MCAD_file_path = QLineEdit(self.MotorCADsettings)
        self.MCAD_file_path.setObjectName(u"MCAD_file_path")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.MCAD_file_path.sizePolicy().hasHeightForWidth())
        self.MCAD_file_path.setSizePolicy(sizePolicy2)

        self.horizontalLayout.addWidget(self.MCAD_file_path)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_8)

        self.load_MCAD_file = QPushButton(self.MotorCADsettings)
        self.load_MCAD_file.setObjectName(u"load_MCAD_file")

        self.horizontalLayout_2.addWidget(self.load_MCAD_file)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.EmagSettings = QLabel(self.MotorCADsettings)
        self.EmagSettings.setObjectName(u"EmagSettings")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.EmagSettings.sizePolicy().hasHeightForWidth())
        self.EmagSettings.setSizePolicy(sizePolicy3)
        self.EmagSettings.setAlignment(Qt.AlignHCenter|Qt.AlignTop)

        self.horizontalLayout_8.addWidget(self.EmagSettings)


        self.verticalLayout_3.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_2 = QLabel(self.MotorCADsettings)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_9.addWidget(self.label_2)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_9)

        self.nrCuboids = QLineEdit(self.MotorCADsettings)
        self.nrCuboids.setObjectName(u"nrCuboids")
        sizePolicy2.setHeightForWidth(self.nrCuboids.sizePolicy().hasHeightForWidth())
        self.nrCuboids.setSizePolicy(sizePolicy2)

        self.horizontalLayout_9.addWidget(self.nrCuboids)


        self.verticalLayout_3.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_3 = QLabel(self.MotorCADsettings)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_10.addWidget(self.label_3)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_10)

        self.TorquePointsPerCycle = QLineEdit(self.MotorCADsettings)
        self.TorquePointsPerCycle.setObjectName(u"TorquePointsPerCycle")

        self.horizontalLayout_10.addWidget(self.TorquePointsPerCycle)


        self.verticalLayout_3.addLayout(self.horizontalLayout_10)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_4 = QLabel(self.MotorCADsettings)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_11.addWidget(self.label_4)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_11)

        self.TorqueNrCycles = QLineEdit(self.MotorCADsettings)
        self.TorqueNrCycles.setObjectName(u"TorqueNrCycles")

        self.horizontalLayout_11.addWidget(self.TorqueNrCycles)


        self.verticalLayout_3.addLayout(self.horizontalLayout_11)

        self.horizontalLayout_27 = QHBoxLayout()
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.set_emag = QPushButton(self.MotorCADsettings)
        self.set_emag.setObjectName(u"set_emag")
        self.set_emag.setEnabled(False)
        sizePolicy3.setHeightForWidth(self.set_emag.sizePolicy().hasHeightForWidth())
        self.set_emag.setSizePolicy(sizePolicy3)
        self.set_emag.setMinimumSize(QSize(0, 35))

        self.horizontalLayout_27.addWidget(self.set_emag)


        self.verticalLayout_3.addLayout(self.horizontalLayout_27)

        self.horizontalLayout_28 = QHBoxLayout()
        self.horizontalLayout_28.setObjectName(u"horizontalLayout_28")
        self.run_emag = QPushButton(self.MotorCADsettings)
        self.run_emag.setObjectName(u"run_emag")
        self.run_emag.setEnabled(False)
        sizePolicy3.setHeightForWidth(self.run_emag.sizePolicy().hasHeightForWidth())
        self.run_emag.setSizePolicy(sizePolicy3)
        self.run_emag.setMinimumSize(QSize(0, 35))

        self.horizontalLayout_28.addWidget(self.run_emag)


        self.verticalLayout_3.addLayout(self.horizontalLayout_28)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.LABSettings = QLabel(self.MotorCADsettings)
        self.LABSettings.setObjectName(u"LABSettings")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.LABSettings.sizePolicy().hasHeightForWidth())
        self.LABSettings.setSizePolicy(sizePolicy4)
        self.LABSettings.setAlignment(Qt.AlignHCenter|Qt.AlignTop)

        self.horizontalLayout_12.addWidget(self.LABSettings)


        self.verticalLayout_3.addLayout(self.horizontalLayout_12)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.label_5 = QLabel(self.MotorCADsettings)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_13.addWidget(self.label_5)

        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_12)

        self.MaxStatorCurrent = QLineEdit(self.MotorCADsettings)
        self.MaxStatorCurrent.setObjectName(u"MaxStatorCurrent")
        self.MaxStatorCurrent.setEnabled(True)
        sizePolicy5 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.MaxStatorCurrent.sizePolicy().hasHeightForWidth())
        self.MaxStatorCurrent.setSizePolicy(sizePolicy5)
        self.MaxStatorCurrent.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_13.addWidget(self.MaxStatorCurrent)


        self.verticalLayout_3.addLayout(self.horizontalLayout_13)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.label_6 = QLabel(self.MotorCADsettings)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_14.addWidget(self.label_6)

        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_13)

        self.SpeedMax = QLineEdit(self.MotorCADsettings)
        self.SpeedMax.setObjectName(u"SpeedMax")
        sizePolicy2.setHeightForWidth(self.SpeedMax.sizePolicy().hasHeightForWidth())
        self.SpeedMax.setSizePolicy(sizePolicy2)

        self.horizontalLayout_14.addWidget(self.SpeedMax)


        self.verticalLayout_3.addLayout(self.horizontalLayout_14)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.label_7 = QLabel(self.MotorCADsettings)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_15.addWidget(self.label_7)

        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_15.addItem(self.horizontalSpacer_14)

        self.SpeedStep = QLineEdit(self.MotorCADsettings)
        self.SpeedStep.setObjectName(u"SpeedStep")
        sizePolicy2.setHeightForWidth(self.SpeedStep.sizePolicy().hasHeightForWidth())
        self.SpeedStep.setSizePolicy(sizePolicy2)

        self.horizontalLayout_15.addWidget(self.SpeedStep)


        self.verticalLayout_3.addLayout(self.horizontalLayout_15)

        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.label_8 = QLabel(self.MotorCADsettings)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_16.addWidget(self.label_8)

        self.horizontalSpacer_15 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_16.addItem(self.horizontalSpacer_15)

        self.SpeedMin = QLineEdit(self.MotorCADsettings)
        self.SpeedMin.setObjectName(u"SpeedMin")
        sizePolicy2.setHeightForWidth(self.SpeedMin.sizePolicy().hasHeightForWidth())
        self.SpeedMin.setSizePolicy(sizePolicy2)

        self.horizontalLayout_16.addWidget(self.SpeedMin)


        self.verticalLayout_3.addLayout(self.horizontalLayout_16)

        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.label_9 = QLabel(self.MotorCADsettings)
        self.label_9.setObjectName(u"label_9")

        self.horizontalLayout_17.addWidget(self.label_9)

        self.horizontalSpacer_16 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_17.addItem(self.horizontalSpacer_16)

        self.MaxTempStatorWdg = QLineEdit(self.MotorCADsettings)
        self.MaxTempStatorWdg.setObjectName(u"MaxTempStatorWdg")
        sizePolicy2.setHeightForWidth(self.MaxTempStatorWdg.sizePolicy().hasHeightForWidth())
        self.MaxTempStatorWdg.setSizePolicy(sizePolicy2)
        self.MaxTempStatorWdg.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_17.addWidget(self.MaxTempStatorWdg)


        self.verticalLayout_3.addLayout(self.horizontalLayout_17)

        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.label_10 = QLabel(self.MotorCADsettings)
        self.label_10.setObjectName(u"label_10")

        self.horizontalLayout_18.addWidget(self.label_10)

        self.horizontalSpacer_17 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_18.addItem(self.horizontalSpacer_17)

        self.MaxTempMagnet = QLineEdit(self.MotorCADsettings)
        self.MaxTempMagnet.setObjectName(u"MaxTempMagnet")

        self.horizontalLayout_18.addWidget(self.MaxTempMagnet)


        self.verticalLayout_3.addLayout(self.horizontalLayout_18)

        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.label_11 = QLabel(self.MotorCADsettings)
        self.label_11.setObjectName(u"label_11")

        self.horizontalLayout_19.addWidget(self.label_11)

        self.horizontalSpacer_18 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_19.addItem(self.horizontalSpacer_18)

        self.OPSpeed = QLineEdit(self.MotorCADsettings)
        self.OPSpeed.setObjectName(u"OPSpeed")
        sizePolicy2.setHeightForWidth(self.OPSpeed.sizePolicy().hasHeightForWidth())
        self.OPSpeed.setSizePolicy(sizePolicy2)

        self.horizontalLayout_19.addWidget(self.OPSpeed)


        self.verticalLayout_3.addLayout(self.horizontalLayout_19)

        self.horizontalLayout_29 = QHBoxLayout()
        self.horizontalLayout_29.setObjectName(u"horizontalLayout_29")
        self.build_lab_model = QPushButton(self.MotorCADsettings)
        self.build_lab_model.setObjectName(u"build_lab_model")
        self.build_lab_model.setEnabled(False)
        sizePolicy3.setHeightForWidth(self.build_lab_model.sizePolicy().hasHeightForWidth())
        self.build_lab_model.setSizePolicy(sizePolicy3)
        self.build_lab_model.setMinimumSize(QSize(0, 35))

        self.horizontalLayout_29.addWidget(self.build_lab_model)


        self.verticalLayout_3.addLayout(self.horizontalLayout_29)

        self.horizontalLayout_30 = QHBoxLayout()
        self.horizontalLayout_30.setObjectName(u"horizontalLayout_30")
        self.run_lab_performance_calc = QPushButton(self.MotorCADsettings)
        self.run_lab_performance_calc.setObjectName(u"run_lab_performance_calc")
        self.run_lab_performance_calc.setEnabled(False)
        sizePolicy3.setHeightForWidth(self.run_lab_performance_calc.sizePolicy().hasHeightForWidth())
        self.run_lab_performance_calc.setSizePolicy(sizePolicy3)
        self.run_lab_performance_calc.setMinimumSize(QSize(0, 35))

        self.horizontalLayout_30.addWidget(self.run_lab_performance_calc)


        self.verticalLayout_3.addLayout(self.horizontalLayout_30)

        self.horizontalLayout_31 = QHBoxLayout()
        self.horizontalLayout_31.setObjectName(u"horizontalLayout_31")
        self.lab_op_point = QPushButton(self.MotorCADsettings)
        self.lab_op_point.setObjectName(u"lab_op_point")
        self.lab_op_point.setEnabled(False)
        sizePolicy3.setHeightForWidth(self.lab_op_point.sizePolicy().hasHeightForWidth())
        self.lab_op_point.setSizePolicy(sizePolicy3)
        self.lab_op_point.setMinimumSize(QSize(0, 35))

        self.horizontalLayout_31.addWidget(self.lab_op_point)


        self.verticalLayout_3.addLayout(self.horizontalLayout_31)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Preferred)

        self.verticalLayout_3.addItem(self.verticalSpacer_2)

        self.export_MCAD = QPushButton(self.MotorCADsettings)
        self.export_MCAD.setObjectName(u"export_MCAD")
        self.export_MCAD.setEnabled(False)
        sizePolicy3.setHeightForWidth(self.export_MCAD.sizePolicy().hasHeightForWidth())
        self.export_MCAD.setSizePolicy(sizePolicy3)
        self.export_MCAD.setMinimumSize(QSize(0, 35))

        self.verticalLayout_3.addWidget(self.export_MCAD)


        self.horizontalLayout_26.addLayout(self.verticalLayout_3)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_26.addItem(self.horizontalSpacer_6)

        self.toolkit_tab.addTab(self.MotorCADsettings, "")
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
        self.magnets_material.setObjectName(u"magnets_material")

        self.horizontalLayout_7.addWidget(self.magnets_material)


        self.verticalLayout_2.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_20 = QHBoxLayout()
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.label_14 = QLabel(self.Segmentation)
        self.label_14.setObjectName(u"label_14")

        self.horizontalLayout_20.addWidget(self.label_14)

        self.rotor_material = QComboBox(self.Segmentation)
        self.rotor_material.setObjectName(u"rotor_material")

        self.horizontalLayout_20.addWidget(self.rotor_material)


        self.verticalLayout_2.addLayout(self.horizontalLayout_20)

        self.horizontalLayout_20a = QHBoxLayout()
        self.horizontalLayout_20a.setObjectName(u"horizontalLayout_20a")
        self.label_14a = QLabel(self.Segmentation)
        self.label_14a.setObjectName(u"label_14a")

        self.horizontalLayout_20a.addWidget(self.label_14a)

        self.stator_material = QComboBox(self.Segmentation)
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

        self.horizontalLayout_24 = QHBoxLayout()
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.label_18 = QLabel(self.Segmentation)
        self.label_18.setObjectName(u"label_18")

        self.horizontalLayout_24.addWidget(self.label_18)

        self.horizontalSpacer_24 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_24.addItem(self.horizontalSpacer_24)

        self.setup_to_analyze = QLineEdit(self.Segmentation)
        self.setup_to_analyze.setObjectName(u"setup_to_analyze")

        self.horizontalLayout_24.addWidget(self.setup_to_analyze)


        self.verticalLayout_2.addLayout(self.horizontalLayout_24)

        self.perform_segmentation = QPushButton(self.Segmentation)
        self.perform_segmentation.setObjectName(u"perform_segmentation")
        self.perform_segmentation.setEnabled(False)
        self.perform_segmentation.setMinimumSize(QSize(0, 40))

        self.verticalLayout_2.addWidget(self.perform_segmentation)

        self.skew = QPushButton(self.Segmentation)
        self.skew.setObjectName(u"skew")
        self.skew.setEnabled(False)
        self.skew.setMinimumSize(QSize(0, 40))

        self.verticalLayout_2.addWidget(self.skew)


        self.horizontalLayout_.addLayout(self.verticalLayout_2)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_.addItem(self.horizontalSpacer_4)

        self.toolkit_tab.addTab(self.Segmentation, "")

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

        self.toolkit_tab.setCurrentIndex(1)
        self.projects_aedt_combo.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.action_save_project.setText(QCoreApplication.translate("MainWindow", u"Save project", None))
        self.release_button.setText(QCoreApplication.translate("MainWindow", u" Close Toolkit ", None))
        self.release_and_exit_button.setText(QCoreApplication.translate("MainWindow", u" Close Desktop and Toolkit ", None))
        self.cores_label.setText(QCoreApplication.translate("MainWindow", u"Number of Cores", None))
        self.numcores.setText(QCoreApplication.translate("MainWindow", u"4", None))
        self.graphical_label.setText(QCoreApplication.translate("MainWindow", u"Non Graphical", None))
        self.non_graphical_combo.setItemText(0, QCoreApplication.translate("MainWindow", u"False", None))
        self.non_graphical_combo.setItemText(1, QCoreApplication.translate("MainWindow", u"True", None))

        self.version_label.setText(QCoreApplication.translate("MainWindow", u"AEDT Version", None))
        self.aedt_sessions_label.setText(QCoreApplication.translate("MainWindow", u"Available AEDT Sessions", None))
        self.process_id_combo.setItemText(0, QCoreApplication.translate("MainWindow", u"Create New Session", None))

        self.project_path_label.setText(QCoreApplication.translate("MainWindow", u"Project Name", None))
        self.browse_project.setText(QCoreApplication.translate("MainWindow", u"Select aedt project", None))
        self.connect_aedtapp.setText(QCoreApplication.translate("MainWindow", u"Launch AEDT", None))
        self.toolkit_tab.setTabText(self.toolkit_tab.indexOf(self.AEDTsettings), QCoreApplication.translate("MainWindow", u" AEDT Settings ", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Motor-CAD file path:", None))
        self.load_MCAD_file.setText(QCoreApplication.translate("MainWindow", u"Load", None))
        self.EmagSettings.setText(QCoreApplication.translate("MainWindow", u"E-mag Settings", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Number Of Cuboids", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Torque Points Per Cycle", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Torque Number Of Cycles", None))
        self.set_emag.setText(QCoreApplication.translate("MainWindow", u"Set E-Mag Model", None))
        self.run_emag.setText(QCoreApplication.translate("MainWindow", u"Run E-Mag Calculation", None))
        self.LABSettings.setText(QCoreApplication.translate("MainWindow", u"LAB Settings", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Max Stator Current", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Speed Max (rpm)", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Speed Step (rpm)", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Speed Min (rpm)", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Max Temp. Stator Winding (\u00b0C)", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Max Temp. Magnet (\u00b0C)", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"OP Speed (rpm)", None))
        self.build_lab_model.setText(QCoreApplication.translate("MainWindow", u"Build LAB Model", None))
        self.run_lab_performance_calc.setText(QCoreApplication.translate("MainWindow", u"Run LAB Performance Calculation", None))
        self.lab_op_point.setText(QCoreApplication.translate("MainWindow", u"LAB Op. Point", None))
        self.export_MCAD.setText(QCoreApplication.translate("MainWindow", u"Export Motor-CAD file", None))
        self.toolkit_tab.setTabText(self.toolkit_tab.indexOf(self.MotorCADsettings), QCoreApplication.translate("MainWindow", u"Motor-CAD Settings", None))
        self.projects_label_2.setText(QCoreApplication.translate("MainWindow", u"Projects", None))
        self.projects_aedt_combo.setItemText(0, QCoreApplication.translate("MainWindow", u"No project", None))

        self.designs_label.setText(QCoreApplication.translate("MainWindow", u"Designs", None))
        self.design_aedt_combo.setItemText(0, QCoreApplication.translate("MainWindow", u"No design", None))

        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Is Skewed", None))
        self.is_skewed.setItemText(0, QCoreApplication.translate("MainWindow", u"False", None))
        self.is_skewed.setItemText(1, QCoreApplication.translate("MainWindow", u"True", None))

        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Magnets Material", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Rotor Material", None))
        self.label_14a.setText(QCoreApplication.translate("MainWindow", u"Stator Material", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Rotor Slices", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Magnet Segments Per Slice", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"Skew Angle (deg)", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"Setup To Analyze", None))
        self.perform_segmentation.setText(QCoreApplication.translate("MainWindow", u"Perform Segmentation", None))
        self.skew.setText(QCoreApplication.translate("MainWindow", u"Apply Skew", None))
        self.toolkit_tab.setTabText(self.toolkit_tab.indexOf(self.Segmentation), QCoreApplication.translate("MainWindow", u"Segmentation", None))
        self.top_menu.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
    # retranslateUi

