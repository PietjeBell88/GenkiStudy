from PyQt4.QtCore import *
from PyQt4.QtGui import *
import Languages
import ui_UserLanguageDialog
import ui_ProgressDialog
import ui_OptionsDialog
import ui_DatabaseDlg
from Database.databasemodel import *


class UserLanguageDialog(QDialog, ui_UserLanguageDialog.Ui_UserLanguageDialog):
    def __init__(self, settings, users, parent=None):
        super(UserLanguageDialog, self).__init__(parent)
        self.settings = settings
        self.setupUi(self)
        self.user_list.addItems(users)
        self.language_list.addItems([language.name for language in Languages.languages])
        self.language_list.sortItems()

    def on_user_list_currentTextChanged(self, user):
        self.settings["User"] = user
        self.check_if_okay()

    def on_language_list_currentTextChanged(self, language_name):
        language = [language for language in Languages.languages if language.name == language_name][0]
        self.settings["Language"] = language
        self.check_if_okay()

    def check_if_okay(self):
        if None not in self.settings.values():
            self.buttonBox.setEnabled(True)
            
            
class OptionsDialog(QDialog, ui_OptionsDialog.Ui_OptionsDialog):
    def __init__(self, parent=None):
        super(OptionsDialog, self).__init__(parent)
        self.setupUi(self)
        
        
class ProgressDialog(QDialog, ui_ProgressDialog.Ui_ProgressDialog):
    def __init__(self, parent=None):
        super(ProgressDialog, self).__init__(parent)
        self.setupUi(self)
        self.treemodel = DatabaseTreeModel("test.db", self)
        self.progress_tree.setModel(self.treemodel)
        self.connect(self.progress_tree, SIGNAL("expanded(QModelIndex)"),
                     self.expanded)
        self.expanded()
        
    def expanded(self):
        for column in range(self.treemodel.columnCount(QModelIndex())):
            self.progress_tree.resizeColumnToContents(column)

        
class DatabaseDlg(QDialog, ui_DatabaseDlg.Ui_DatabaseDlg):

    def __init__(self, pathtodb, parent=None):
        super(DatabaseDlg, self).__init__(parent)
        self.setupUi(self)
        
        self.listmodel = DatabaseListModel(self, pathtodb)
        self.listView.setModel(self.listmodel)
        
        self.tablemodel = DatabaseTableModel(self, pathtodb, self.listmodel.data[0])
        self.tableView.setModel(self.tablemodel)

        self.connect(self.listView, SIGNAL("activated(QModelIndex)"), self.updateTable)
    
    def updateTable(self, index):
        print index.row()
        print self.listmodel.data[index.row()]
        self.tablemodel.changeTable(self.listmodel.data[index.row()])
        self.tableView.resizeColumnsToContents()
    
        