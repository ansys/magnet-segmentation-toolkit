# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'post_processing_page.ui'
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
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtWidgets import QSpacerItem
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget


class Ui_PostProcessing(object):
    def setupUi(self, PostProcessing):
        if not PostProcessing.objectName():
            PostProcessing.setObjectName("PostProcessing")
        PostProcessing.resize(890, 1178)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(PostProcessing.sizePolicy().hasHeightForWidth())
        PostProcessing.setSizePolicy(sizePolicy)
        PostProcessing.setProperty("post-processing", QRect(9, 9, 701, 441))
        self.verticalLayout = QVBoxLayout(PostProcessing)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.setup_name_label = QLabel(PostProcessing)
        self.setup_name_label.setObjectName("setup_name_label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.setup_name_label.sizePolicy().hasHeightForWidth())
        self.setup_name_label.setSizePolicy(sizePolicy1)
        self.setup_name_label.setMinimumSize(QSize(0, 0))

        self.horizontalLayout_2.addWidget(self.setup_name_label)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_6)

        self.setup_name_combo = QComboBox(PostProcessing)
        self.setup_name_combo.addItem("")
        self.setup_name_combo.setObjectName("setup_name_combo")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.setup_name_combo.sizePolicy().hasHeightForWidth())
        self.setup_name_combo.setSizePolicy(sizePolicy2)

        self.horizontalLayout_2.addWidget(self.setup_name_combo)

        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.validate_and_analyze = QPushButton(PostProcessing)
        self.validate_and_analyze.setObjectName("validate_and_analyze")
        sizePolicy2.setHeightForWidth(self.validate_and_analyze.sizePolicy().hasHeightForWidth())
        self.validate_and_analyze.setSizePolicy(sizePolicy2)
        self.validate_and_analyze.setMinimumSize(QSize(0, 40))
        self.validate_and_analyze.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout_3.addWidget(self.validate_and_analyze)

        self.get_magnet_loss = QPushButton(PostProcessing)
        self.get_magnet_loss.setObjectName("get_magnet_loss")
        sizePolicy2.setHeightForWidth(self.get_magnet_loss.sizePolicy().hasHeightForWidth())
        self.get_magnet_loss.setSizePolicy(sizePolicy2)
        self.get_magnet_loss.setMinimumSize(QSize(0, 40))
        self.get_magnet_loss.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout_3.addWidget(self.get_magnet_loss)

        self.horizontalLayout.addLayout(self.verticalLayout_3)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(PostProcessing)

        QMetaObject.connectSlotsByName(PostProcessing)

    # setupUi

    def retranslateUi(self, PostProcessing):
        PostProcessing.setWindowTitle(QCoreApplication.translate("PostProcessing", "Form", None))
        self.setup_name_label.setText(QCoreApplication.translate("PostProcessing", "Setup to analyze", None))
        self.setup_name_combo.setItemText(0, QCoreApplication.translate("PostProcessing", "--No Setups--", None))

        self.validate_and_analyze.setText(QCoreApplication.translate("PostProcessing", "Validate and Analyze", None))
        self.get_magnet_loss.setText(QCoreApplication.translate("PostProcessing", "Get Magnet Loss", None))

    # retranslateUi
