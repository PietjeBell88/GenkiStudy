# -*- coding: utf-8 -*-
import sys
import re
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import platform
import Languages
import Gui.ui_MainWindow as ui_MainWindow
from Gui.UserInterface import *

__version__ = 0.01

class MainWindow(QMainWindow, ui_MainWindow.Ui_MainWindow):
    def __init__(self, users, settings, parent=None):
        super(MainWindow, self).__init__(parent)
        self.settings = settings
        self.users = users
        self.setupUi(self)
        
        self.on_actionSwitchUserLanguage_triggered()


    def initializeLanguage(self):
        rehearse_type = self.language.rehearse_types[0]
        self.question_type_label.setText(self.language.name + ": " + rehearse_type.name)
        self.answer_type_label.setText(rehearse_type.answer)
        self.menuRehearse.clear()
        rehearse_group = QActionGroup(self)
        #rehearse_group.setExclusive(False)
        for rehearse_type in self.language.rehearse_types:
            action = self.createAction(rehearse_type.name, slot=self.change_rehearse, checkable=True)
            rehearse_group.addAction(action)
            self.menuRehearse.addAction(action)


    def createAction(self, text, slot=None, shortcut=None, icon=None,
                     tip=None, checkable=False, signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action


    def addActions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)

    @pyqtSignature("")
    def on_actionAbout_triggered(self):
        QMessageBox.about(self, "About GenkiStudy",
                """<b>GenkiStudy</b> v%s
                <p>Copyright &copy; 2010 Pietje Bell. 
                All rights reserved.
                <p>This application helps you slack.
                <p>Python %s - Qt %s - PyQt %s on %s""" % (
                __version__, platform.python_version(),
                QT_VERSION_STR, PYQT_VERSION_STR, platform.system()))

    @pyqtSignature("")
    def on_actionOptions_triggered(self):
        dlg = OptionsDialog(self)
        dlg.exec_()
        
    @pyqtSignature("")
    def on_actionProgress_triggered(self):
        dlg = ProgressDialog(self)
        dlg.exec_()

    @pyqtSignature("")
    def on_actionDatabase_triggered(self):
        dlg = DatabaseDlg(self.language.database, self)
        dlg.exec_()
        
    @pyqtSignature("")    
    def on_actionSwitchUserLanguage_triggered(self):
        userlanguagedialog = UserLanguageDialog(self.settings, self.users, self)
        if not userlanguagedialog.exec_():
            self.centralwidget.setEnabled(False)
        else:
            self.language = self.settings["Language"]
            self.initializeLanguage()
            self.centralwidget.setEnabled(True)

    def change_rehearse(self):
        pass


def main():
    users = ["Pietje"]
    settings = {"User": None, "Language": None}
    app = QApplication(sys.argv)
    app.setOrganizationName("Pietje Bell")
    app.setOrganizationDomain("imnotsosure.com")
    app.setApplicationName("GenkiStudy")
    app.setWindowIcon(QIcon("images/icon2.png"))
    mainwindow = MainWindow(users,settings)
    mainwindow.show()
    app.exec_()
    
main()
