# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\UserLanguageDialog.ui'
#
# Created: Thu Mar 25 17:44:22 2010
#      by: PyQt4 UI code generator 4.7
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_UserLanguageDialog(object):
    def setupUi(self, UserLanguageDialog):
        UserLanguageDialog.setObjectName("UserLanguageDialog")
        UserLanguageDialog.resize(525, 218)
        self.gridLayout = QtGui.QGridLayout(UserLanguageDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.user_label = QtGui.QLabel(UserLanguageDialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.user_label.setFont(font)
        self.user_label.setObjectName("user_label")
        self.gridLayout.addWidget(self.user_label, 0, 0, 1, 1)
        self.language_label = QtGui.QLabel(UserLanguageDialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.language_label.setFont(font)
        self.language_label.setObjectName("language_label")
        self.gridLayout.addWidget(self.language_label, 0, 1, 1, 1)
        self.user_list = QtGui.QListWidget(UserLanguageDialog)
        self.user_list.setObjectName("user_list")
        self.gridLayout.addWidget(self.user_list, 1, 0, 1, 1)
        self.language_list = QtGui.QListWidget(UserLanguageDialog)
        self.language_list.setObjectName("language_list")
        self.gridLayout.addWidget(self.language_list, 1, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(UserLanguageDialog)
        self.buttonBox.setEnabled(False)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 2)

        self.retranslateUi(UserLanguageDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), UserLanguageDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), UserLanguageDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(UserLanguageDialog)

    def retranslateUi(self, UserLanguageDialog):
        UserLanguageDialog.setWindowTitle(QtGui.QApplication.translate("UserLanguageDialog", "Select User and Language", None, QtGui.QApplication.UnicodeUTF8))
        self.user_label.setText(QtGui.QApplication.translate("UserLanguageDialog", "User", None, QtGui.QApplication.UnicodeUTF8))
        self.language_label.setText(QtGui.QApplication.translate("UserLanguageDialog", "Language", None, QtGui.QApplication.UnicodeUTF8))

