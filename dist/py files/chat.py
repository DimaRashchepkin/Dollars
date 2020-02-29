import sqlite3
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow
import time as Time
import chat_ui
from admin_enter import AdminEnter
from enter import Enter


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
