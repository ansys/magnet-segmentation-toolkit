# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'segmentation_page.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
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
        Segmentation.resize(627, 456)
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
        self.horizontalLayout_32 = QHBoxLayout()
        self.horizontalLayout_32.setObjectName(u"horizontalLayout_32")
        self.apply_mesh_sheets_label = QLabel(Segmentation)
        self.apply_mesh_sheets_label.setObjectName(u"apply_mesh_sheets_label")

        self.horizontalLayout_32.addWidget(self.apply_mesh_sheets_label)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_32.addItem(self.horizontalSpacer_2)

        self.apply_mesh_sheets = QComboBox(Segmentation)
        self.apply_mesh_sheets.addItem("")
        self.apply_mesh_sheets.addItem("")
        self.apply_mesh_sheets.setObjectName(u"apply_mesh_sheets")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.apply_mesh_sheets.sizePolicy().hasHeightForWidth())
        self.apply_mesh_sheets.setSizePolicy(sizePolicy1)
        self.apply_mesh_sheets.setMinimumSize(QSize(300, 0))

        self.horizontalLayout_32.addWidget(self.apply_mesh_sheets)


        self.verticalLayout_2.addLayout(self.horizontalLayout_32)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.is_skewed_label = QLabel(Segmentation)
        self.is_skewed_label.setObjectName(u"is_skewed_label")

        self.horizontalLayout_4.addWidget(self.is_skewed_label)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_5)

        self.is_skewed = QComboBox(Segmentation)
        self.is_skewed.addItem("")
        self.is_skewed.addItem("")
        self.is_skewed.setObjectName(u"is_skewed")
        sizePolicy1.setHeightForWidth(self.is_skewed.sizePolicy().hasHeightForWidth())
        self.is_skewed.setSizePolicy(sizePolicy1)
        self.is_skewed.setMinimumSize(QSize(300, 0))

        self.horizontalLayout_4.addWidget(self.is_skewed)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.magnets_material_label = QLabel(Segmentation)
        self.magnets_material_label.setObjectName(u"magnets_material_label")

        self.horizontalLayout_7.addWidget(self.magnets_material_label)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_6)

        self.magnets_material = QComboBox(Segmentation)
        self.magnets_material.addItem("")
        self.magnets_material.setObjectName(u"magnets_material")
        sizePolicy1.setHeightForWidth(self.magnets_material.sizePolicy().hasHeightForWidth())
        self.magnets_material.setSizePolicy(sizePolicy1)
        self.magnets_material.setMinimumSize(QSize(300, 0))

        self.horizontalLayout_7.addWidget(self.magnets_material)


        self.verticalLayout_2.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_20 = QHBoxLayout()
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.rotor_material_label = QLabel(Segmentation)
        self.rotor_material_label.setObjectName(u"rotor_material_label")

        self.horizontalLayout_20.addWidget(self.rotor_material_label)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_20.addItem(self.horizontalSpacer_7)

        self.rotor_material = QComboBox(Segmentation)
        self.rotor_material.addItem("")
        self.rotor_material.setObjectName(u"rotor_material")
        sizePolicy1.setHeightForWidth(self.rotor_material.sizePolicy().hasHeightForWidth())
        self.rotor_material.setSizePolicy(sizePolicy1)
        self.rotor_material.setMinimumSize(QSize(300, 0))

        self.horizontalLayout_20.addWidget(self.rotor_material)


        self.verticalLayout_2.addLayout(self.horizontalLayout_20)

        self.horizontalLayout_20a = QHBoxLayout()
        self.horizontalLayout_20a.setObjectName(u"horizontalLayout_20a")
        self.stator_material_label = QLabel(Segmentation)
        self.stator_material_label.setObjectName(u"stator_material_label")

        self.horizontalLayout_20a.addWidget(self.stator_material_label)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_20a.addItem(self.horizontalSpacer_8)

        self.stator_material = QComboBox(Segmentation)
        self.stator_material.addItem("")
        self.stator_material.setObjectName(u"stator_material")
        sizePolicy1.setHeightForWidth(self.stator_material.sizePolicy().hasHeightForWidth())
        self.stator_material.setSizePolicy(sizePolicy1)
        self.stator_material.setMinimumSize(QSize(300, 0))

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
        sizePolicy1.setHeightForWidth(self.rotor_slices.sizePolicy().hasHeightForWidth())
        self.rotor_slices.setSizePolicy(sizePolicy1)
        self.rotor_slices.setMinimumSize(QSize(300, 0))

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
        sizePolicy1.setHeightForWidth(self.magnet_segments_per_slice.sizePolicy().hasHeightForWidth())
        self.magnet_segments_per_slice.setSizePolicy(sizePolicy1)
        self.magnet_segments_per_slice.setMinimumSize(QSize(300, 0))

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
        sizePolicy1.setHeightForWidth(self.mesh_sheets_number.sizePolicy().hasHeightForWidth())
        self.mesh_sheets_number.setSizePolicy(sizePolicy1)
        self.mesh_sheets_number.setMinimumSize(QSize(300, 0))

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
        sizePolicy1.setHeightForWidth(self.skew_angle.sizePolicy().hasHeightForWidth())
        self.skew_angle.setSizePolicy(sizePolicy1)
        self.skew_angle.setMinimumSize(QSize(300, 0))

        self.horizontalLayout_23.addWidget(self.skew_angle)


        self.verticalLayout_2.addLayout(self.horizontalLayout_23)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.perform_segmentation = QPushButton(Segmentation)
        self.perform_segmentation.setObjectName(u"perform_segmentation")
        self.perform_segmentation.setEnabled(True)
        sizePolicy.setHeightForWidth(self.perform_segmentation.sizePolicy().hasHeightForWidth())
        self.perform_segmentation.setSizePolicy(sizePolicy)
        self.perform_segmentation.setMinimumSize(QSize(0, 40))
        self.perform_segmentation.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout_2.addWidget(self.perform_segmentation)

        self.skew = QPushButton(Segmentation)
        self.skew.setObjectName(u"skew")
        self.skew.setEnabled(True)
        sizePolicy.setHeightForWidth(self.skew.sizePolicy().hasHeightForWidth())
        self.skew.setSizePolicy(sizePolicy)
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
        Segmentation.setWindowTitle(QCoreApplication.translate("Segmentation", u"Form", None))
        self.apply_mesh_sheets_label.setText(QCoreApplication.translate("Segmentation", u"Apply Mesh Sheets", None))
        self.apply_mesh_sheets.setItemText(0, QCoreApplication.translate("Segmentation", u"False", None))
        self.apply_mesh_sheets.setItemText(1, QCoreApplication.translate("Segmentation", u"True", None))

        self.is_skewed_label.setText(QCoreApplication.translate("Segmentation", u"Is Skewed", None))
        self.is_skewed.setItemText(0, QCoreApplication.translate("Segmentation", u"False", None))
        self.is_skewed.setItemText(1, QCoreApplication.translate("Segmentation", u"True", None))

        self.magnets_material_label.setText(QCoreApplication.translate("Segmentation", u"Magnet Material", None))
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

