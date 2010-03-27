# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ProgressDialog.ui'
#
# Created: Sat Mar 27 16:57:43 2010
#      by: PyQt4 UI code generator 4.7
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ProgressDialog(object):
    def setupUi(self, ProgressDialog):
        ProgressDialog.setObjectName("ProgressDialog")
        ProgressDialog.resize(716, 666)
        self.gridLayout = QtGui.QGridLayout(ProgressDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.language_label = QtGui.QLabel(ProgressDialog)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.language_label.setFont(font)
        self.language_label.setObjectName("language_label")
        self.gridLayout.addWidget(self.language_label, 0, 0, 1, 1)
        self.progress_label = QtGui.QLabel(ProgressDialog)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.progress_label.setFont(font)
        self.progress_label.setObjectName("progress_label")
        self.gridLayout.addWidget(self.progress_label, 0, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ProgressDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 1, 1, 1)
        self.progress_tree = QtGui.QTreeView(ProgressDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progress_tree.sizePolicy().hasHeightForWidth())
        self.progress_tree.setSizePolicy(sizePolicy)
        self.progress_tree.setSizeIncrement(QtCore.QSize(0, 0))
        self.progress_tree.setObjectName("progress_tree")
        self.gridLayout.addWidget(self.progress_tree, 1, 1, 1, 1)
        self.language_list = QtGui.QListWidget(ProgressDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.language_list.sizePolicy().hasHeightForWidth())
        self.language_list.setSizePolicy(sizePolicy)
        self.language_list.setObjectName("language_list")
        self.gridLayout.addWidget(self.language_list, 1, 0, 1, 1)

        self.retranslateUi(ProgressDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), ProgressDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), ProgressDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ProgressDialog)

    def retranslateUi(self, ProgressDialog):
        ProgressDialog.setWindowTitle(QtGui.QApplication.translate("ProgressDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.language_label.setText(QtGui.QApplication.translate("ProgressDialog", "Language", None, QtGui.QApplication.UnicodeUTF8))
        self.progress_label.setText(QtGui.QApplication.translate("ProgressDialog", "Progress", None, QtGui.QApplication.UnicodeUTF8))

