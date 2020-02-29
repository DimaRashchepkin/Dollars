from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
import archive_ui
import sqlite3


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
