from PyQt5 import uic, QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QMovie
import mysql.connector as ms


class MyGUI(QMainWindow):
    def __init__(self):
        super(MyGUI, self).__init__()
        uic.loadUi("lib.ui", self)
        self.show()
        self.isConnected = False
        self.pushButton.clicked.connect(self.connectDB)
        self.connect_db_button.clicked.connect(self.UseDB)
        ## Disabling all buttons
        self.prohibit()

    def prohibit(self):
        self.label_database.setEnabled(False)
        self.heading2.setEnabled(False)
        self.databases_drop.setEnabled(False)
        self.connect_db_button.setEnabled(False)

    def hideLogin(self):
        self.stackedWidget.setCurrentWidget(self.load)

    def UseDB(self):
        db = self.databases_drop.currentText()
        self.cur.execute(f"Use {db}")
        self.hideLogin()

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

    def enableDB(self):
        self.heading2.setEnabled(True)
        self.databases_drop.setEnabled(True)
        self.connect_db_button.setEnabled(True)


app = QApplication([])
window = MyGUI()
app.exec_()
