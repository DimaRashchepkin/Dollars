import sqlite3
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow
import time as Time
import register_ui


class Register(QMainWindow, register_ui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.con = sqlite3.connect("dollars.db")
        self.setupUi(self)

        self.time = Time.asctime().split()
        self.time = self.time[1:3]
        self.time = ' '.join(self.time)

        self.setWindowTitle('DollarsRegistration')
        self.pxm = QPixmap('dollars.png')
        self.dollars.setPixmap(self.pxm)

        self.RegisterButton.clicked.connect(self.register)
        self.FinishButton.clicked.connect(self.finish)

    def register(self):
        self.login = self.LoginLineEdit.text()
        self.password = self.PasswordLineEdit.text()

        cur = self.con.cursor()
        if self.login != '' and self.password != '':
            try:
                num = cur.execute(
                    """SELECT MAX(id) FROM users""").fetchall()

                cur.execute(
                    """INSERT INTO users(id, login, password, date) 
                    VALUES(?, ?, ?, ?)""",
                    (num[0][0] + 1, self.login, self.password, self.time))

                self.con.commit()
                self.error.setText("")
                self.successful.setText("register's successfully")

            except sqlite3.IntegrityError:
                self.error.setText("login's already used")
                self.successful.setText("")
                self.LoginLineEdit.setText('')
                self.PasswordLineEdit.setText('')
        else:
            self.error.setText("place's empty")
            self.successful.setText("")
            self.LoginLineEdit.setText('')
            self.PasswordLineEdit.setText('')

    def finish(self):
        self.close()
