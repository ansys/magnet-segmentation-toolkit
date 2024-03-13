# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'segmentation_page.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_Segmentation(object):
    def setupUi(self, Segmentation):
        if not Segmentation.objectName():
            Segmentation.setObjectName(u"Segmentation")
        Segmentation.resize(397, 456)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Segmentation.sizePolicy().hasHeightForWidth())
        Segmentation.setSizePolicy(sizePolicy)
        Segmentation.setProperty("segmentation", QRect(0, 0, 890, 1178))
        self.verticalLayout = QVBoxLayout(Segmentation)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_ = QHBoxLayout()
        self.horizontalLayout_.setObjectName(u"horizontalLayout_")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.projects_aedt_combo_label = QLabel(Segmentation)
        self.projects_aedt_combo_label.setObjectName(u"projects_aedt_combo_label")

        self.horizontalLayout_3.addWidget(self.projects_aedt_combo_label)

        self.projects_aedt_combo = QComboBox(Segmentation)
        self.projects_aedt_combo.addItem("")
        self.projects_aedt_combo.setObjectName(u"projects_aedt_combo")

        self.horizontalLayout_3.addWidget(self.projects_aedt_combo)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.design_aedt_combo_label = QLabel(Segmentation)
        self.design_aedt_combo_label.setObjectName(u"design_aedt_combo_label")

        self.horizontalLayout_6.addWidget(self.design_aedt_combo_label)

        self.design_aedt_combo = QComboBox(Segmentation)
        self.design_aedt_combo.addItem("")
        self.design_aedt_combo.setObjectName(u"design_aedt_combo")

        self.horizontalLayout_6.addWidget(self.design_aedt_combo)


        self.verticalLayout_2.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_66 = QHBoxLayout()
        self.horizontalLayout_66.setObjectName(u"horizontalLayout_66")
        self.motor_type_combo_label = QLabel(Segmentation)
        self.motor_type_combo_label.setObjectName(u"motor_type_combo_label")

        self.horizontalLayout_66.addWidget(self.motor_type_combo_label)

        self.motor_type_combo = QComboBox(Segmentation)
        self.motor_type_combo.addItem("")
        self.motor_type_combo.setObjectName(u"motor_type_combo")

        self.horizontalLayout_66.addWidget(self.motor_type_combo)


        self.verticalLayout_2.addLayout(self.horizontalLayout_66)

        self.horizontalLayout_32 = QHBoxLayout()
        self.horizontalLayout_32.setObjectName(u"horizontalLayout_32")
        self.apply_mesh_sheets_label = QLabel(Segmentation)
        self.apply_mesh_sheets_label.setObjectName(u"apply_mesh_sheets_label")

        self.horizontalLayout_32.addWidget(self.apply_mesh_sheets_label)

        self.apply_mesh_sheets = QComboBox(Segmentation)
        self.apply_mesh_sheets.addItem("")
        self.apply_mesh_sheets.addItem("")
        self.apply_mesh_sheets.setObjectName(u"apply_mesh_sheets")

        self.horizontalLayout_32.addWidget(self.apply_mesh_sheets)


        self.verticalLayout_2.addLayout(self.horizontalLayout_32)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.is_skewed_label = QLabel(Segmentation)
        self.is_skewed_label.setObjectName(u"is_skewed_label")

        self.horizontalLayout_4.addWidget(self.is_skewed_label)

        self.is_skewed = QComboBox(Segmentation)
        self.is_skewed.addItem("")
        self.is_skewed.addItem("")
        self.is_skewed.setObjectName(u"is_skewed")

        self.horizontalLayout_4.addWidget(self.is_skewed)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.magnets_material_label = QLabel(Segmentation)
        self.magnets_material_label.setObjectName(u"magnets_material_label")

        self.horizontalLayout_7.addWidget(self.magnets_material_label)

        self.magnets_material = QComboBox(Segmentation)
        self.magnets_material.addItem("")
        self.magnets_material.setObjectName(u"magnets_material")

        self.horizontalLayout_7.addWidget(self.magnets_material)


        self.verticalLayout_2.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_20 = QHBoxLayout()
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.rotor_material_label = QLabel(Segmentation)
        self.rotor_material_label.setObjectName(u"rotor_material_label")

        self.horizontalLayout_20.addWidget(self.rotor_material_label)

        self.rotor_material = QComboBox(Segmentation)
        self.rotor_material.addItem("")
        self.rotor_material.setObjectName(u"rotor_material")

        self.horizontalLayout_20.addWidget(self.rotor_material)


        self.verticalLayout_2.addLayout(self.horizontalLayout_20)

        self.horizontalLayout_20a = QHBoxLayout()
        self.horizontalLayout_20a.setObjectName(u"horizontalLayout_20a")
        self.stator_material_label = QLabel(Segmentation)
        self.stator_material_label.setObjectName(u"stator_material_label")

        self.horizontalLayout_20a.addWidget(self.stator_material_label)

        self.stator_material = QComboBox(Segmentation)
        self.stator_material.addItem("")
        self.stator_material.setObjectName(u"stator_material")

        self.horizontalLayout_20a.addWidget(self.stator_material)


        self.verticalLayout_2.addLayout(self.horizontalLayout_20a)

        self.horizontalLayout_21 = QHBoxLayout()
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.rotor_slices_label = QLabel(Segmentation)
        self.rotor_slices_label.setObjectName(u"rotor_slices_label")

        self.horizontalLayout_21.addWidget(self.rotor_slices_label)

        self.horizontalSpacer_21 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_21.addItem(self.horizontalSpacer_21)

        self.rotor_slices = QLineEdit(Segmentation)
        self.rotor_slices.setObjectName(u"rotor_slices")

        self.horizontalLayout_21.addWidget(self.rotor_slices)


        self.verticalLayout_2.addLayout(self.horizontalLayout_21)

        self.horizontalLayout_22 = QHBoxLayout()
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.magnet_segments_per_slice_label = QLabel(Segmentation)
        self.magnet_segments_per_slice_label.setObjectName(u"magnet_segments_per_slice_label")

        self.horizontalLayout_22.addWidget(self.magnet_segments_per_slice_label)

        self.horizontalSpacer_22 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_22.addItem(self.horizontalSpacer_22)

        self.magnet_segments_per_slice = QLineEdit(Segmentation)
        self.magnet_segments_per_slice.setObjectName(u"magnet_segments_per_slice")

        self.horizontalLayout_22.addWidget(self.magnet_segments_per_slice)


        self.verticalLayout_2.addLayout(self.horizontalLayout_22)

        self.horizontalLayout_33 = QHBoxLayout()
        self.horizontalLayout_33.setObjectName(u"horizontalLayout_33")
        self.mesh_sheets_number_label = QLabel(Segmentation)
        self.mesh_sheets_number_label.setObjectName(u"mesh_sheets_number_label")

        self.horizontalLayout_33.addWidget(self.mesh_sheets_number_label)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_33.addItem(self.horizontalSpacer_3)

        self.mesh_sheets_number = QLineEdit(Segmentation)
        self.mesh_sheets_number.setObjectName(u"mesh_sheets_number")

        self.horizontalLayout_33.addWidget(self.mesh_sheets_number)


        self.verticalLayout_2.addLayout(self.horizontalLayout_33)

        self.horizontalLayout_23 = QHBoxLayout()
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.skew_angle_label = QLabel(Segmentation)
        self.skew_angle_label.setObjectName(u"skew_angle_label")

        self.horizontalLayout_23.addWidget(self.skew_angle_label)

        self.horizontalSpacer_23 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_23.addItem(self.horizontalSpacer_23)

        self.skew_angle = QLineEdit(Segmentation)
        self.skew_angle.setObjectName(u"skew_angle")

        self.horizontalLayout_23.addWidget(self.skew_angle)


        self.verticalLayout_2.addLayout(self.horizontalLayout_23)

        self.perform_segmentation = QPushButton(Segmentation)
        self.perform_segmentation.setObjectName(u"perform_segmentation")
        self.perform_segmentation.setEnabled(True)
        self.perform_segmentation.setMinimumSize(QSize(0, 40))
        self.perform_segmentation.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout_2.addWidget(self.perform_segmentation)

        self.skew = QPushButton(Segmentation)
        self.skew.setObjectName(u"skew")
        self.skew.setEnabled(True)
        self.skew.setMinimumSize(QSize(0, 40))

        self.verticalLayout_2.addWidget(self.skew)


        self.horizontalLayout_.addLayout(self.verticalLayout_2)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_.addItem(self.horizontalSpacer_4)


        self.verticalLayout.addLayout(self.horizontalLayout_)


        self.retranslateUi(Segmentation)

        self.projects_aedt_combo.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Segmentation)
    # setupUi

    def retranslateUi(self, Segmentation):
        Segmentation.setWindowTitle(QCoreApplication.translate("Segmentation", u"Form", None))
        self.projects_aedt_combo_label.setText(QCoreApplication.translate("Segmentation", u"Projects", None))
        self.projects_aedt_combo.setItemText(0, QCoreApplication.translate("Segmentation", u"--Select Project--", None))

        self.design_aedt_combo_label.setText(QCoreApplication.translate("Segmentation", u"Designs", None))
        self.design_aedt_combo.setItemText(0, QCoreApplication.translate("Segmentation", u"--Select Design--", None))

        self.design_aedt_combo.setCurrentText(QCoreApplication.translate("Segmentation", u"--Select Design--", None))
        self.motor_type_combo_label.setText(QCoreApplication.translate("Segmentation", u"Motor Type", None))
        self.motor_type_combo.setItemText(0, QCoreApplication.translate("Segmentation", u"--Select Motor Type--", None))

        self.motor_type_combo.setCurrentText(QCoreApplication.translate("Segmentation", u"--Select Motor Type--", None))
        self.apply_mesh_sheets_label.setText(QCoreApplication.translate("Segmentation", u"Apply Mesh Sheets", None))
        self.apply_mesh_sheets.setItemText(0, QCoreApplication.translate("Segmentation", u"False", None))
        self.apply_mesh_sheets.setItemText(1, QCoreApplication.translate("Segmentation", u"True", None))

        self.is_skewed_label.setText(QCoreApplication.translate("Segmentation", u"Is Skewed", None))
        self.is_skewed.setItemText(0, QCoreApplication.translate("Segmentation", u"False", None))
        self.is_skewed.setItemText(1, QCoreApplication.translate("Segmentation", u"True", None))

        self.magnets_material_label.setText(QCoreApplication.translate("Segmentation", u"Magnets Material", None))
        self.magnets_material.setItemText(0, QCoreApplication.translate("Segmentation", u"--Select Material--", None))

        self.rotor_material_label.setText(QCoreApplication.translate("Segmentation", u"Rotor Material", None))
        self.rotor_material.setItemText(0, QCoreApplication.translate("Segmentation", u"--Select Material--", None))

        self.stator_material_label.setText(QCoreApplication.translate("Segmentation", u"Stator Material", None))
        self.stator_material.setItemText(0, QCoreApplication.translate("Segmentation", u"--Select Material--", None))

        self.rotor_slices_label.setText(QCoreApplication.translate("Segmentation", u"Rotor Slices", None))
        self.magnet_segments_per_slice_label.setText(QCoreApplication.translate("Segmentation", u"Magnet Segments Per Slice", None))
        self.mesh_sheets_number_label.setText(QCoreApplication.translate("Segmentation", u"Mesh Sheets Number", None))
        self.skew_angle_label.setText(QCoreApplication.translate("Segmentation", u"Skew Angle (deg)", None))
        self.perform_segmentation.setText(QCoreApplication.translate("Segmentation", u"Perform Segmentation", None))
        self.skew.setText(QCoreApplication.translate("Segmentation", u"Apply Skew", None))
    # retranslateUi

