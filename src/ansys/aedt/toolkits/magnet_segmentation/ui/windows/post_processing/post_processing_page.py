# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'post_processing_page.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
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
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_PostProcessing(object):
    def setupUi(self, PostProcessing):
        if not PostProcessing.objectName():
            PostProcessing.setObjectName(u"PostProcessing")
        PostProcessing.resize(890, 1178)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(PostProcessing.sizePolicy().hasHeightForWidth())
        PostProcessing.setSizePolicy(sizePolicy)
        PostProcessing.setProperty("post-processing", QRect(9, 9, 701, 441))
        self.verticalLayout = QVBoxLayout(PostProcessing)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.setup_name_label = QLabel(PostProcessing)
        self.setup_name_label.setObjectName(u"setup_name_label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.setup_name_label.sizePolicy().hasHeightForWidth())
        self.setup_name_label.setSizePolicy(sizePolicy1)
        self.setup_name_label.setMinimumSize(QSize(0, 0))

        self.horizontalLayout_2.addWidget(self.setup_name_label)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_6)

        self.setup_name_combo = QComboBox(PostProcessing)
        self.setup_name_combo.addItem("")
        self.setup_name_combo.setObjectName(u"setup_name_combo")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.setup_name_combo.sizePolicy().hasHeightForWidth())
        self.setup_name_combo.setSizePolicy(sizePolicy2)
        self.setup_name_combo.setMinimumSize(QSize(300, 0))

        self.horizontalLayout_2.addWidget(self.setup_name_combo)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Maximum)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.validate_and_analyze = QPushButton(PostProcessing)
        self.validate_and_analyze.setObjectName(u"validate_and_analyze")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.validate_and_analyze.sizePolicy().hasHeightForWidth())
        self.validate_and_analyze.setSizePolicy(sizePolicy3)
        self.validate_and_analyze.setMinimumSize(QSize(0, 40))
        self.validate_and_analyze.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout_3.addWidget(self.validate_and_analyze)

        self.get_magnet_loss = QPushButton(PostProcessing)
        self.get_magnet_loss.setObjectName(u"get_magnet_loss")
        sizePolicy3.setHeightForWidth(self.get_magnet_loss.sizePolicy().hasHeightForWidth())
        self.get_magnet_loss.setSizePolicy(sizePolicy3)
        self.get_magnet_loss.setMinimumSize(QSize(0, 40))
        self.get_magnet_loss.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout_3.addWidget(self.get_magnet_loss)


        self.horizontalLayout.addLayout(self.verticalLayout_3)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(PostProcessing)

        QMetaObject.connectSlotsByName(PostProcessing)
    # setupUi

    def retranslateUi(self, PostProcessing):
        PostProcessing.setWindowTitle(QCoreApplication.translate("PostProcessing", u"Form", None))
        self.setup_name_label.setText(QCoreApplication.translate("PostProcessing", u"Setup to analyze", None))
        self.setup_name_combo.setItemText(0, QCoreApplication.translate("PostProcessing", u"--No Setups--", None))

        self.validate_and_analyze.setText(QCoreApplication.translate("PostProcessing", u"Validate and Analyze", None))
        self.get_magnet_loss.setText(QCoreApplication.translate("PostProcessing", u"Get Magnet Loss", None))
    # retranslateUi

