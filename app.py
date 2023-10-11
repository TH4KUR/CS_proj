from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt
import mysql.connector as ms


class MyGUI(QMainWindow):
    def __init__(self):
        super(MyGUI, self).__init__()
        uic.loadUi("lib.ui", self)
        self.show()
        self.isConnected = False
        self.pushButton.clicked.connect(self.connectDB)
        self.connect_db_button.clicked.connect(self.UseDB)
        self.viewTbBtn.clicked.connect(self.setTable)
        ## Disabling all buttons
        self.prohibit()

    def prohibit(self):
        self.label_database.setEnabled(False)
        self.heading2.setEnabled(False)
        self.databases_drop.setEnabled(False)
        self.connect_db_button.setEnabled(False)

    def hideLogin(self):
        self.stackedWidget.setCurrentWidget(self.actions_page)

    def UseDB(self):
        db = self.databases_drop.currentText()
        self.cur.execute(f"Use {db}")
        self.hideLogin()
        self.setTable("books")
        self.setTbDrop()
        self.cur.execute(
            "SELECT name FROM sys.columns WHERE object_id = OBJECT_ID('books')"
        )
        x = self.cur.fetchall()
        print(x)

    def connectDB(self):
        try:
            host_ = self.lineEdit.text()
            username_ = self.lineEdit_2.text()
            password_ = self.lineEdit_3.text()

            self.con = ms.connect(host=host_, username=username_, password=password_)
            self.status.setText("Connected!")
            self.isConnected = True
            self.cur = self.con.cursor()

            self.enableDB()
            self.setDbDrop()

        except Exception as err:
            print(err)
            self.prohibit()
            self.status.setText("Error! Couldn't connect to DB")

    def setDbDrop(self):
        self.cur.execute("SHOW DATABASES")
        dbs = self.cur.fetchall()
        for i in dbs:
            self.databases_drop.addItem(i[0])

    def setTbDrop(self):
        self.cur.execute("SHOW Tables")
        tbs = self.cur.fetchall()
        for i in tbs:
            self.tables_drop.addItem(i[0])

    def enableDB(self):
        self.heading2.setEnabled(True)
        self.databases_drop.setEnabled(True)
        self.connect_db_button.setEnabled(True)

    def setTable(self, table):
        row = 0
        tableX = table
        if not table:
            tableX = self.tables_drop.currentText()

        self.cur.execute(f"SELECT * from {tableX}")
        data = self.cur.fetchall()
        self.tableWidget.setRowCount(len(data))
        for i in data:
            row += 1
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(i[0]))
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(i[1]))
            self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(i[2]))
            self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(i[3]))


app = QApplication([])
window = MyGUI()
app.exec_()
