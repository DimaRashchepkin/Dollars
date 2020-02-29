from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow
import admin_enter_ui
from archive import Archive


class AdminEnter(QMainWindow, admin_enter_ui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle('DollarsAdminEnter')
        self.pxm = QPixmap('dollars-mini.png')
        self.dollars_mini.setPixmap(self.pxm)

        self.EnterButton.clicked.connect(self.enter)

    def enter(self):
        self.password = self.PasswordLineEdit.text()

        if self.password == 'durara':
            self.archive = Archive()
            self.archive.show()
            self.close()
        else:
            self.error.setText("password isn't correct")
            self.PasswordLineEdit.setText('')
