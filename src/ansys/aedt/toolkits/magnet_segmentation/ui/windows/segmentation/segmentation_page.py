# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'segmentation_page.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import QCoreApplication
from PySide6.QtCore import QDate
from PySide6.QtCore import QDateTime
from PySide6.QtCore import QLocale
from PySide6.QtCore import QMetaObject
from PySide6.QtCore import QObject
from PySide6.QtCore import QPoint
from PySide6.QtCore import QRect
from PySide6.QtCore import QSize
from PySide6.QtCore import QTime
from PySide6.QtCore import QUrl
from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush
from PySide6.QtGui import QColor
from PySide6.QtGui import QConicalGradient
from PySide6.QtGui import QCursor
from PySide6.QtGui import QFont
from PySide6.QtGui import QFontDatabase
from PySide6.QtGui import QGradient
from PySide6.QtGui import QIcon
from PySide6.QtGui import QImage
from PySide6.QtGui import QKeySequence
from PySide6.QtGui import QLinearGradient
from PySide6.QtGui import QPainter
from PySide6.QtGui import QPalette
from PySide6.QtGui import QPixmap
from PySide6.QtGui import QRadialGradient
from PySide6.QtGui import QTransform
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QComboBox
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtWidgets import QSpacerItem
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget


class Ui_Segmentation(object):
    def setupUi(self, Segmentation):
        if not Segmentation.objectName():
            Segmentation.setObjectName("Segmentation")
        Segmentation.resize(397, 456)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Segmentation.sizePolicy().hasHeightForWidth())
        Segmentation.setSizePolicy(sizePolicy)
        Segmentation.setProperty("segmentation", QRect(0, 0, 890, 1178))
        self.verticalLayout = QVBoxLayout(Segmentation)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_ = QHBoxLayout()
        self.horizontalLayout_.setObjectName("horizontalLayout_")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_66 = QHBoxLayout()
        self.horizontalLayout_66.setObjectName("horizontalLayout_66")
        self.motor_type_combo_label = QLabel(Segmentation)
        self.motor_type_combo_label.setObjectName("motor_type_combo_label")

        self.horizontalLayout_66.addWidget(self.motor_type_combo_label)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_66.addItem(self.horizontalSpacer)

        self.motor_type_combo = QComboBox(Segmentation)
        self.motor_type_combo.addItem("")
        self.motor_type_combo.setObjectName("motor_type_combo")
        sizePolicy.setHeightForWidth(self.motor_type_combo.sizePolicy().hasHeightForWidth())
        self.motor_type_combo.setSizePolicy(sizePolicy)

        self.horizontalLayout_66.addWidget(self.motor_type_combo)

        self.verticalLayout_2.addLayout(self.horizontalLayout_66)

        self.horizontalLayout_32 = QHBoxLayout()
        self.horizontalLayout_32.setObjectName("horizontalLayout_32")
        self.apply_mesh_sheets_label = QLabel(Segmentation)
        self.apply_mesh_sheets_label.setObjectName("apply_mesh_sheets_label")

        self.horizontalLayout_32.addWidget(self.apply_mesh_sheets_label)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_32.addItem(self.horizontalSpacer_2)

        self.apply_mesh_sheets = QComboBox(Segmentation)
        self.apply_mesh_sheets.addItem("")
        self.apply_mesh_sheets.addItem("")
        self.apply_mesh_sheets.setObjectName("apply_mesh_sheets")
        sizePolicy.setHeightForWidth(self.apply_mesh_sheets.sizePolicy().hasHeightForWidth())
        self.apply_mesh_sheets.setSizePolicy(sizePolicy)

        self.horizontalLayout_32.addWidget(self.apply_mesh_sheets)

        self.verticalLayout_2.addLayout(self.horizontalLayout_32)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.is_skewed_label = QLabel(Segmentation)
        self.is_skewed_label.setObjectName("is_skewed_label")

        self.horizontalLayout_4.addWidget(self.is_skewed_label)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_5)

        self.is_skewed = QComboBox(Segmentation)
        self.is_skewed.addItem("")
        self.is_skewed.addItem("")
        self.is_skewed.setObjectName("is_skewed")
        sizePolicy.setHeightForWidth(self.is_skewed.sizePolicy().hasHeightForWidth())
        self.is_skewed.setSizePolicy(sizePolicy)

        self.horizontalLayout_4.addWidget(self.is_skewed)

        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.magnets_material_label = QLabel(Segmentation)
        self.magnets_material_label.setObjectName("magnets_material_label")

        self.horizontalLayout_7.addWidget(self.magnets_material_label)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_6)

        self.magnets_material = QComboBox(Segmentation)
        self.magnets_material.addItem("")
        self.magnets_material.setObjectName("magnets_material")
        sizePolicy.setHeightForWidth(self.magnets_material.sizePolicy().hasHeightForWidth())
        self.magnets_material.setSizePolicy(sizePolicy)

        self.horizontalLayout_7.addWidget(self.magnets_material)

        self.verticalLayout_2.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_20 = QHBoxLayout()
        self.horizontalLayout_20.setObjectName("horizontalLayout_20")
        self.rotor_material_label = QLabel(Segmentation)
        self.rotor_material_label.setObjectName("rotor_material_label")

        self.horizontalLayout_20.addWidget(self.rotor_material_label)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_20.addItem(self.horizontalSpacer_7)

        self.rotor_material = QComboBox(Segmentation)
        self.rotor_material.addItem("")
        self.rotor_material.setObjectName("rotor_material")
        sizePolicy.setHeightForWidth(self.rotor_material.sizePolicy().hasHeightForWidth())
        self.rotor_material.setSizePolicy(sizePolicy)

        self.horizontalLayout_20.addWidget(self.rotor_material)

        self.verticalLayout_2.addLayout(self.horizontalLayout_20)

        self.horizontalLayout_20a = QHBoxLayout()
        self.horizontalLayout_20a.setObjectName("horizontalLayout_20a")
        self.stator_material_label = QLabel(Segmentation)
        self.stator_material_label.setObjectName("stator_material_label")

        self.horizontalLayout_20a.addWidget(self.stator_material_label)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_20a.addItem(self.horizontalSpacer_8)

        self.stator_material = QComboBox(Segmentation)
        self.stator_material.addItem("")
        self.stator_material.setObjectName("stator_material")
        sizePolicy.setHeightForWidth(self.stator_material.sizePolicy().hasHeightForWidth())
        self.stator_material.setSizePolicy(sizePolicy)

        self.horizontalLayout_20a.addWidget(self.stator_material)

        self.verticalLayout_2.addLayout(self.horizontalLayout_20a)

        self.horizontalLayout_21 = QHBoxLayout()
        self.horizontalLayout_21.setObjectName("horizontalLayout_21")
        self.rotor_slices_label = QLabel(Segmentation)
        self.rotor_slices_label.setObjectName("rotor_slices_label")

        self.horizontalLayout_21.addWidget(self.rotor_slices_label)

        self.horizontalSpacer_21 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_21.addItem(self.horizontalSpacer_21)

        self.rotor_slices = QLineEdit(Segmentation)
        self.rotor_slices.setObjectName("rotor_slices")
        sizePolicy.setHeightForWidth(self.rotor_slices.sizePolicy().hasHeightForWidth())
        self.rotor_slices.setSizePolicy(sizePolicy)

        self.horizontalLayout_21.addWidget(self.rotor_slices)

        self.verticalLayout_2.addLayout(self.horizontalLayout_21)

        self.horizontalLayout_22 = QHBoxLayout()
        self.horizontalLayout_22.setObjectName("horizontalLayout_22")
        self.magnet_segments_per_slice_label = QLabel(Segmentation)
        self.magnet_segments_per_slice_label.setObjectName("magnet_segments_per_slice_label")

        self.horizontalLayout_22.addWidget(self.magnet_segments_per_slice_label)

        self.horizontalSpacer_22 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_22.addItem(self.horizontalSpacer_22)

        self.magnet_segments_per_slice = QLineEdit(Segmentation)
        self.magnet_segments_per_slice.setObjectName("magnet_segments_per_slice")
        sizePolicy.setHeightForWidth(self.magnet_segments_per_slice.sizePolicy().hasHeightForWidth())
        self.magnet_segments_per_slice.setSizePolicy(sizePolicy)

        self.horizontalLayout_22.addWidget(self.magnet_segments_per_slice)

        self.verticalLayout_2.addLayout(self.horizontalLayout_22)

        self.horizontalLayout_33 = QHBoxLayout()
        self.horizontalLayout_33.setObjectName("horizontalLayout_33")
        self.mesh_sheets_number_label = QLabel(Segmentation)
        self.mesh_sheets_number_label.setObjectName("mesh_sheets_number_label")

        self.horizontalLayout_33.addWidget(self.mesh_sheets_number_label)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_33.addItem(self.horizontalSpacer_3)

        self.mesh_sheets_number = QLineEdit(Segmentation)
        self.mesh_sheets_number.setObjectName("mesh_sheets_number")
        sizePolicy.setHeightForWidth(self.mesh_sheets_number.sizePolicy().hasHeightForWidth())
        self.mesh_sheets_number.setSizePolicy(sizePolicy)

        self.horizontalLayout_33.addWidget(self.mesh_sheets_number)

        self.verticalLayout_2.addLayout(self.horizontalLayout_33)

        self.horizontalLayout_23 = QHBoxLayout()
        self.horizontalLayout_23.setObjectName("horizontalLayout_23")
        self.skew_angle_label = QLabel(Segmentation)
        self.skew_angle_label.setObjectName("skew_angle_label")

        self.horizontalLayout_23.addWidget(self.skew_angle_label)

        self.horizontalSpacer_23 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_23.addItem(self.horizontalSpacer_23)

        self.skew_angle = QLineEdit(Segmentation)
        self.skew_angle.setObjectName("skew_angle")
        sizePolicy.setHeightForWidth(self.skew_angle.sizePolicy().hasHeightForWidth())
        self.skew_angle.setSizePolicy(sizePolicy)

        self.horizontalLayout_23.addWidget(self.skew_angle)

        self.verticalLayout_2.addLayout(self.horizontalLayout_23)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.perform_segmentation = QPushButton(Segmentation)
        self.perform_segmentation.setObjectName("perform_segmentation")
        self.perform_segmentation.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.perform_segmentation.sizePolicy().hasHeightForWidth())
        self.perform_segmentation.setSizePolicy(sizePolicy1)
        self.perform_segmentation.setMinimumSize(QSize(0, 40))
        self.perform_segmentation.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout_2.addWidget(self.perform_segmentation)

        self.skew = QPushButton(Segmentation)
        self.skew.setObjectName("skew")
        self.skew.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.skew.sizePolicy().hasHeightForWidth())
        self.skew.setSizePolicy(sizePolicy1)
        self.skew.setMinimumSize(QSize(0, 40))

        self.verticalLayout_2.addWidget(self.skew)

        self.horizontalLayout_.addLayout(self.verticalLayout_2)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_.addItem(self.horizontalSpacer_4)

        self.verticalLayout.addLayout(self.horizontalLayout_)

        self.retranslateUi(Segmentation)

        QMetaObject.connectSlotsByName(Segmentation)

    # setupUi

    def retranslateUi(self, Segmentation):
        Segmentation.setWindowTitle(QCoreApplication.translate("Segmentation", "Form", None))
        self.motor_type_combo_label.setText(QCoreApplication.translate("Segmentation", "Motor Type", None))
        self.motor_type_combo.setItemText(0, QCoreApplication.translate("Segmentation", "--Select Motor Type--", None))

        self.motor_type_combo.setCurrentText(QCoreApplication.translate("Segmentation", "--Select Motor Type--", None))
        self.apply_mesh_sheets_label.setText(QCoreApplication.translate("Segmentation", "Apply Mesh Sheets", None))
        self.apply_mesh_sheets.setItemText(0, QCoreApplication.translate("Segmentation", "False", None))
        self.apply_mesh_sheets.setItemText(1, QCoreApplication.translate("Segmentation", "True", None))

        self.is_skewed_label.setText(QCoreApplication.translate("Segmentation", "Is Skewed", None))
        self.is_skewed.setItemText(0, QCoreApplication.translate("Segmentation", "False", None))
        self.is_skewed.setItemText(1, QCoreApplication.translate("Segmentation", "True", None))

        self.magnets_material_label.setText(QCoreApplication.translate("Segmentation", "Magnets Material", None))
        self.magnets_material.setItemText(0, QCoreApplication.translate("Segmentation", "--Select Material--", None))

        self.rotor_material_label.setText(QCoreApplication.translate("Segmentation", "Rotor Material", None))
        self.rotor_material.setItemText(0, QCoreApplication.translate("Segmentation", "--Select Material--", None))

        self.stator_material_label.setText(QCoreApplication.translate("Segmentation", "Stator Material", None))
        self.stator_material.setItemText(0, QCoreApplication.translate("Segmentation", "--Select Material--", None))

        self.rotor_slices_label.setText(QCoreApplication.translate("Segmentation", "Rotor Slices", None))
        self.magnet_segments_per_slice_label.setText(
            QCoreApplication.translate("Segmentation", "Magnet Segments Per Slice", None)
        )
        self.mesh_sheets_number_label.setText(QCoreApplication.translate("Segmentation", "Mesh Sheets Number", None))
        self.skew_angle_label.setText(QCoreApplication.translate("Segmentation", "Skew Angle (deg)", None))
        self.perform_segmentation.setText(QCoreApplication.translate("Segmentation", "Perform Segmentation", None))
        self.skew.setText(QCoreApplication.translate("Segmentation", "Apply Skew", None))

    # retranslateUi
