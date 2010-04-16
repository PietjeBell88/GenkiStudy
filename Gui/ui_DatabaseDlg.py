# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\DatabaseDlg.ui'
#
# Created: Mon Mar 29 17:29:12 2010
#      by: PyQt4 UI code generator 4.7
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_DatabaseDlg(object):
    def setupUi(self, DatabaseDlg):
        DatabaseDlg.setObjectName("DatabaseDlg")
        DatabaseDlg.resize(939, 580)
        self.gridLayout = QtGui.QGridLayout(DatabaseDlg)
        self.gridLayout.setObjectName("gridLayout")
        self.listView = QtGui.QListView(DatabaseDlg)
        self.listView.setObjectName("listView")
        self.gridLayout.addWidget(self.listView, 0, 0, 1, 1)
        self.tableView = QtGui.QTableView(DatabaseDlg)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableView.sizePolicy().hasHeightForWidth())
        self.tableView.setSizePolicy(sizePolicy)
        self.tableView.setSortingEnabled(True)
        self.tableView.setObjectName("tableView")
        self.tableView.verticalHeader().setVisible(False)
        self.tableView.verticalHeader().setDefaultSectionSize(20)
        self.tableView.verticalHeader().setMinimumSectionSize(15)
        self.gridLayout.addWidget(self.tableView, 0, 1, 1, 1)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.buttonBox = QtGui.QDialogButtonBox(DatabaseDlg)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.addRowButton = QtGui.QPushButton(DatabaseDlg)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addRowButton.sizePolicy().hasHeightForWidth())
        self.addRowButton.setSizePolicy(sizePolicy)
        self.addRowButton.setObjectName("addRowButton")
        self.verticalLayout.addWidget(self.addRowButton)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem1)
        self.importListButton = QtGui.QPushButton(DatabaseDlg)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.importListButton.sizePolicy().hasHeightForWidth())
        self.importListButton.setSizePolicy(sizePolicy)
        self.importListButton.setObjectName("importListButton")
        self.verticalLayout.addWidget(self.importListButton)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.gridLayout.addLayout(self.verticalLayout, 0, 2, 1, 1)

        self.retranslateUi(DatabaseDlg)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), DatabaseDlg.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), DatabaseDlg.reject)
        QtCore.QObject.connect(self.listView, QtCore.SIGNAL("activated(QModelIndex)"), self.tableView.clearSelection)
        QtCore.QMetaObject.connectSlotsByName(DatabaseDlg)

    def retranslateUi(self, DatabaseDlg):
        DatabaseDlg.setWindowTitle(QtGui.QApplication.translate("DatabaseDlg", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.addRowButton.setText(QtGui.QApplication.translate("DatabaseDlg", "Add Row", None, QtGui.QApplication.UnicodeUTF8))
        self.importListButton.setText(QtGui.QApplication.translate("DatabaseDlg", "Import List", None, QtGui.QApplication.UnicodeUTF8))

