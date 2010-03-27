from PyQt4.QtCore import *
from PyQt4.QtGui import *
import Languages
import ui_UserLanguageDialog
import ui_ProgressDialog
import ui_OptionsDialog


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
        
