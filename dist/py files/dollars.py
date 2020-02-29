import os
import sys
import logging


def _append_run_path():
    if getattr(sys, 'frozen', False):
        pathlist = []
        pathlist.append(sys._MEIPASS)
        _main_app_path = os.path.dirname(sys.executable)
        pathlist.append(_main_app_path)
        os.environ["PATH"] += os.pathsep + os.pathsep.join(pathlist)

    logging.error("current PATH: %s", os.environ['PATH'])


_append_run_path()

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
import time as Time
import admin_enter_ui
import archive_ui
import chat_ui
import enter_ui
import sqlite3
import register_ui


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


class Chat(QMainWindow, chat_ui.Ui_MainWindow):
    def __init__(self, other):
        super().__init__()
        self.setupUi(self)

        self.login = str(other)
        self.con = sqlite3.connect("dollars.db")

        self.setWindowTitle('Dollars')
        self.UserLabel.setText(self.login)
        self.pxm = QPixmap('dollars-mini.png')
        self.dollars_mini.setPixmap(self.pxm)

        self.SendButton.clicked.connect(self.send)
        self.ExitButton.clicked.connect(self.exit)
        self.ArchiveButton.clicked.connect(self.admin_enter)
        self.RebootButton.clicked.connect(self.reboot)

        self.show()

        cur = self.con.cursor()
        self.num = cur.execute("""SELECT MAX(id) FROM messages""").fetchall()
        self.num = self.num[0][0]
        self.lst = []
        if self.num == None:
            self.num = -1
        for i in range(self.num + 1):
            cur = self.con.cursor()
            self.lst.append(cur.execute("""SELECT user, message FROM messages 
            WHERE id == ?""", (str(i))).fetchall())
        lst = [x[0] for x in self.lst[1:]]
        for i in range(len(lst)):
            self.history = self.chat.toPlainText()
            self.chat.setText(
                self.history + lst[i][0] + ': ' + lst[i][1] + '\n')

    def send(self):
        self.text = self.lineEdit.text()
        self.history = self.chat.toPlainText()
        self.chat.setText(self.history + self.UserLabel.text() + ': '
                          + self.text + '\n')
        cur = self.con.cursor()
        self.time = Time.asctime().split()
        self.time = self.time[3].split(':')
        self.time = ':'.join(self.time[:-1])

        cur.execute(
            """INSERT INTO messages(user, message, time) VALUES(?, ?, ?)""",
            (self.UserLabel.text(), self.text, self.time))
        self.lineEdit.setText('')
        self.con.commit()

    def reboot(self):
        cur = self.con.cursor()
        self.num = cur.execute("""SELECT MAX(id) FROM messages""").fetchall()
        self.num = self.num[0][0]
        self.lst = []
        if self.num == None:
            self.num = -1
        for i in range(self.num + 1):
            cur = self.con.cursor()
            self.lst.append(cur.execute("""SELECT user, message FROM messages 
                    WHERE id == ?""", (str(i))).fetchall())
        lst = [x[0] for x in self.lst[1:]]
        self.history = ''
        for i in range(len(lst)):
            self.chat.setText(
                self.history + lst[i][0] + ': ' + lst[i][1] + '\n')
            self.history = self.chat.toPlainText()

    def admin_enter(self):
        self.admin_enter = AdminEnter()
        self.admin_enter.show()

    def exit(self):
        self.enter = Enter()
        self.enter.show()
        self.close()


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


class Archive(QMainWindow, archive_ui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle('DollarsArchive')
        self.pxm = QPixmap('dollars-mini.png')
        self.dollars_mini.setPixmap(self.pxm)

        self.ExitButton.clicked.connect(self.exit)
        self.OKButton.clicked.connect(self.delete)

        self.con = sqlite3.connect("dollars.db")
        cur = self.con.cursor()
        self.num1 = cur.execute("""SELECT MAX(id) FROM users""").fetchall()
        self.num1 = self.num1[0][0]
        self.lst = []
        if self.num1 == None:
            self.num1 = 0

        self.num = cur.execute("""SELECT MAX(id) FROM messages""").fetchall()
        self.num = self.num[0][0]

        self.MessagesTable.setRowCount(self.num)
        self.UsersTable.setRowCount(self.num1)

        self.data_m = cur.execute(
            """SELECT user, message, time FROM messages""").fetchall()
        for i in range(self.num):
            for j in range(3):
                self.MessagesTable.setItem(i, j,
                                           QTableWidgetItem(self.data_m[i][j]))

        self.data_u = cur.execute(
            """SELECT login, date FROM users""").fetchall()
        for i in range(self.num1):
            for j in range(2):
                self.UsersTable.setItem(i, j, QTableWidgetItem(
                    str(self.data_u[i][j])))

        self.MessagesTable.resizeColumnsToContents()
        self.UsersTable.resizeColumnsToContents()

    def delete(self):
        self.user = self.DeleteLineEdit.text()
        if self.user != 'admin' and self.user != '':
            cur = self.con.cursor()

            num = cur.execute(
                """SELECT id FROM users WHERE login = ?""",
                (self.user,)).fetchall()

            if num != []:
                self.for_delete = cur.execute(
                    """DELETE FROM users WHERE login = ?""",
                    (self.user,)).fetchall()

                self.con.commit()

                result = cur.execute("""SELECT id FROM users""").fetchall()
                for x in result:
                    if x[0] > num[0][0]:
                        cur.execute("""UPDATE users SET id = ? WHERE id = ?""",
                                    (x[0] - 1, x[0])).fetchall()

                self.num1 = cur.execute(
                    """SELECT MAX(id) FROM users""").fetchall()
                self.num1 = self.num1[0][0]
                if self.num1 == None:
                    self.num1 = 0
                self.data_u = cur.execute(
                    """SELECT login, date FROM users""").fetchall()
                self.UsersTable.clear()
                for i in range(self.num1):
                    for j in range(2):
                        self.UsersTable.setItem(i, j, QTableWidgetItem(
                            str(self.data_u[i][j])))
                self.UsersTable.setHorizontalHeaderLabels(
                    ["user", "date"])

                self.con.commit()
            else:
                self.DeleteLineEdit.setText("can't delete")
        else:
            self.DeleteLineEdit.setText("can't delete")

    def exit(self):
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Enter()
    ex.show()
    sys.exit(app.exec_())
