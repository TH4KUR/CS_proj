from PyQt5 import uic
from PyQt5.QtWidgets import *
import mysql.connector as ms


class MyGUI(QMainWindow):
    def __init__(self):
        super(MyGUI, self).__init__()
        uic.loadUi("lib.ui", self)
        self.show()
        self.isConnected = True
        self.pushButton.clicked.connect(self.connectDB)
        self.pushButton.clicked.connect(self.UseDB)

        ## Disabling all buttons

        self.tables_drop.setEnabled(False)
        self.label_tables.setEnabled(False)
        self.label_database.setEnabled(False)
        self.heading2.setEnabled(False)
        self.databases_drop.setEnabled(False)
        self.connect_db_button.setEnabled(False)
        self.add_table_button.setEnabled(False)

    def UseDB(self):
        return;

    def connectDB(self):
        try:
            host_ = self.lineEdit.text()
            username_ = self.lineEdit_2.text()
            password_ = self.lineEdit_3.text()

            con = ms.connect(host=host_, user=username_, password=password_)
            self.status.setText("Connected!")
            self.isConnected = True
            self.cur = con.cursor()

            self.enableDB()
            self.setDbDrop()
            self.setTablesDrop()
        except Exception as err:
            print(err)
            self.status.setText("Error! Couldn't connect to DB")

    # Sets the dropdown to show all the active dbs present

    def setDbDrop(self):
        self.cur.execute("SHOW DATABASES")
        dbs = self.cur.fetchall()
        for i in dbs:
            self.databases_drop.addItem(i[0])
    def setTablesDrop(self):
        self.cur.execute("SHOW TABLES")
        tbls = self.cur.fetchall()
        for i in tbls:
            self.tables_drop.addItem(i[0])
    def enableDB(self):
        self.tables_drop.setEnabled(True)
        self.label_tables.setEnabled(True)
        self.label_database.setEnabled(True)
        self.heading2.setEnabled(True)
        self.databases_drop.setEnabled(True)
        self.connect_db_button.setEnabled(True)
        self.add_table_button.setEnabled(True)


app = QApplication([])
window = MyGUI()
app.exec_()