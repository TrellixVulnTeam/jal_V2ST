# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'quotes_update.ui'
##
## Created by: Qt User Interface Compiler version 5.14.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide2.QtWidgets import *


class Ui_UpdateQuotesDlg(object):
    def setupUi(self, UpdateQuotesDlg):
        if UpdateQuotesDlg.objectName():
            UpdateQuotesDlg.setObjectName(u"UpdateQuotesDlg")
        UpdateQuotesDlg.resize(250, 140)
        self.gridLayout = QGridLayout(UpdateQuotesDlg)
        self.gridLayout.setObjectName(u"gridLayout")
        self.EndDateEdit = QDateEdit(UpdateQuotesDlg)
        self.EndDateEdit.setObjectName(u"EndDateEdit")
        self.EndDateEdit.setCalendarPopup(True)

        self.gridLayout.addWidget(self.EndDateEdit, 1, 1, 1, 1)

        self.buttonBox = QDialogButtonBox(UpdateQuotesDlg)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 3, 1, 1, 1)

        self.EndDateLbl = QLabel(UpdateQuotesDlg)
        self.EndDateLbl.setObjectName(u"EndDateLbl")

        self.gridLayout.addWidget(self.EndDateLbl, 1, 0, 1, 1)

        self.StartDateEdit = QDateEdit(UpdateQuotesDlg)
        self.StartDateEdit.setObjectName(u"StartDateEdit")
        self.StartDateEdit.setCalendarPopup(True)

        self.gridLayout.addWidget(self.StartDateEdit, 0, 1, 1, 1)

        self.StartDateLbl = QLabel(UpdateQuotesDlg)
        self.StartDateLbl.setObjectName(u"StartDateLbl")

        self.gridLayout.addWidget(self.StartDateLbl, 0, 0, 1, 1)

        self.UseProxyCheck = QCheckBox(UpdateQuotesDlg)
        self.UseProxyCheck.setObjectName(u"UseProxyCheck")

        self.gridLayout.addWidget(self.UseProxyCheck, 2, 1, 1, 1)


        self.retranslateUi(UpdateQuotesDlg)
        self.buttonBox.accepted.connect(UpdateQuotesDlg.accept)
        self.buttonBox.rejected.connect(UpdateQuotesDlg.reject)

        QMetaObject.connectSlotsByName(UpdateQuotesDlg)
    # setupUi

    def retranslateUi(self, UpdateQuotesDlg):
        UpdateQuotesDlg.setWindowTitle(QCoreApplication.translate("UpdateQuotesDlg", u"Update asset's quotes", None))
        self.EndDateEdit.setDisplayFormat(QCoreApplication.translate("UpdateQuotesDlg", u"dd/MM/yyyy", None))
        self.EndDateLbl.setText(QCoreApplication.translate("UpdateQuotesDlg", u"End date", None))
        self.StartDateEdit.setDisplayFormat(QCoreApplication.translate("UpdateQuotesDlg", u"dd/MM/yyyy", None))
        self.StartDateLbl.setText(QCoreApplication.translate("UpdateQuotesDlg", u"Start date", None))
        self.UseProxyCheck.setText(QCoreApplication.translate("UpdateQuotesDlg", u"Use &Proxy", None))
    # retranslateUi
