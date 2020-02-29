import sqlite3
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow
import enter_ui
from chat import Chat
from register import Register


class Enter(QMainWindow, enter_ui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle('DollarsEnter')
        self.dollars.setPixmap(QPixmap('dollars.png'))

        self.EnterButton.clicked.connect(self.enter)
        self.RegisterButton.clicked.connect(self.register)

    def enter(self):
        self.login = self.LoginLineEdit.text()
        self.password = self.PasswordLineEdit.text()

        self.con = sqlite3.connect("dollars.db")
        cur = self.con.cursor()
        result = cur.execute("""SELECT login, password FROM users 
                        WHERE login == ? AND password == ?""",
                             (self.login, self.password)).fetchall()
        if len(result) > 0:
            result = result[0]
            if result[0] == self.login and str(result[1]) == self.password:
                self.name = self.login
                self.chat = Chat(self.name)
                self.chat.show()
                self.close()
            else:
                self.error.setText("login or password isn't correct")
                self.LoginLineEdit.setText('')
                self.PasswordLineEdit.setText('')
        else:
            self.error.setText("login or password isn't correct")
            self.LoginLineEdit.setText('')
            self.PasswordLineEdit.setText('')

    def register(self):
        self.register = Register()
        self.register.show()
