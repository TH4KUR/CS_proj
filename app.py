from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import *
import mysql.connector as ms
import random


class MyGUI(QMainWindow):
    def __init__(self):
        super(MyGUI, self).__init__()
        uic.loadUi("lib.ui", self)
        self.show()
        self.isConnected = False
        self.pushButton.clicked.connect(self.connectDB)
        self.connect_db_button.clicked.connect(self.UseDB)
        self.viewTbBtn.clicked.connect(self.setTable)
        self.update_copies_btn.clicked.connect(self.updateBookCopies)
        self.doActionBtn.clicked.connect(self.uiActions)
        self.addBookConfirm_btn.clicked.connect(self.addBookConfirm)
        self.addBookConfirm_rejectBtn.clicked.connect(self.goToAddBook)
        self.CheckAvailable_btn.clicked.connect(self.checkAvailibilty)
        self.assign_book_btn.clicked.connect(self.assignBook)
        self.btnBox_addBook.accepted.connect(self.addBook)
        self.btnBox_addBook.rejected.connect(self.goToActions)

        self.buttonBox_3.accepted.connect(self.addMember)
        self.buttonBox_3.rejected.connect(self.goToActions)

        ## Disabling all buttons
        self.prohibit()

    def goToActions(self):
        self.stackedWidget.setCurrentWidget(self.actions_page)
        self.setStats()

    def uiActions(self):
        if self.addBook_radio.isChecked():
            self.goToAddBook()

        elif self.addMember_radio.isChecked():
            self.cust_id.setText(str(random.randint(10000000000, 99999999999)))
            self.stackedWidget.setCurrentWidget(self.add_member)

        elif self.checkAvailability_radio.isChecked():
            self.stackedWidget_2.setCurrentWidget(self.checkBookAvaliableScreen)
            self.cur.execute("SELECT * FROM books")
            books = self.cur.fetchall()
            for i in books:
                self.books_drop.addItem(i[1])

        elif self.assignBook_radio.isChecked():
            self.stackedWidget_2.setCurrentWidget(self.assign_book_screen)
            self.groupBox.setEnabled(False)

        elif self.updateCopies_radio.isChecked():
            self.stackedWidget_2.setCurrentWidget(self.update_copies_screen)
            self.groupBox.setEnabled(False)

    def goToAddBook(self):
        self.confirmBookBox.setEnabled(False)
        self.newBookDetails.setEnabled(True)
        self.stackedWidget.setCurrentWidget(self.add_book)

    def addBookConfirm(self):
        try:
            self.cur.execute(
                f"INSERT INTO books values('{self.newBook[0]}','{self.newBook[1]}','{self.newBook[2]}','{self.newBook[3]}','{self.newBook[4]}','{self.newBook[5]}','{self.newBook[6]}')"
            )
            self.con.commit()
            message = QMessageBox()
            message.setText(f"Values added Successfully")
            message.exec_()
            self.setTable("books")
            self.goToActions()

        except Exception as err:
            message = QMessageBox()
            message.setText(f"An error occurred: {err}")
            message.exec_()
            self.goToActions()
            self.setTable("books")

    def addBook(self):
        self.confirmBookBox.setEnabled(True)

        self.newBook = [
            self.book_isbn.text(),
            self.book_name.text(),
            self.book_author.text(),
            self.book_genre.text(),
            self.book_price.text(),
            self.book_copies.text(),
            self.book_copies.text(),
        ]
        print(self.newBook)
        self.tableWidget.setRowCount(len(self.newBook))
        self.tableWidget.setColumnCount(2)
        self.tableWidget_2.setItem(0, 0, QtWidgets.QTableWidgetItem(self.newBook[0]))
        self.tableWidget_2.setItem(1, 0, QtWidgets.QTableWidgetItem(self.newBook[1]))
        self.tableWidget_2.setItem(2, 0, QtWidgets.QTableWidgetItem(self.newBook[2]))
        self.tableWidget_2.setItem(3, 0, QtWidgets.QTableWidgetItem(self.newBook[3]))
        self.tableWidget_2.setItem(4, 0, QtWidgets.QTableWidgetItem(self.newBook[4]))
        self.tableWidget_2.setItem(5, 0, QtWidgets.QTableWidgetItem(self.newBook[5]))
        self.tableWidget_2.setItem(6, 0, QtWidgets.QTableWidgetItem(self.newBook[6]))

        self.newBookDetails.setEnabled(False)

    def setStats(self):
        self.cur.execute(
            "SELECT count(*) as count,(select count(*) from customer) as count2,(select count(*) from issue) as count3 from books"
        )
        stats = self.cur.fetchone()
        print(stats)
        self.stats_totalBooks.setText(
            f"There are currently {stats[0]} books in the library"
        )
        self.stats_totalMembers.setText(
            f"There are currently {stats[1]} members in the library"
        )
        self.stats_totalBorrowers.setText(
            f"There are currently {stats[2]} borrowers in the library"
        )

    def addMember(self):
        try:
            Id = self.cust_id.text()
            name = self.cust_name.text()
            email = self.cust_email.text()
            address = self.cust_address.text()

            self.cur.execute(
                f"INSERT INTO customer VALUES('{Id}','{name}','{email}','{address}')"
            )
            message = QMessageBox()
            message.setText(f"New Member Added successfully")
            message.exec_()
        except Exception as err:
            message = QMessageBox()
            message.setText(f"An error occurred: {err}")
            message.exec_()

    def checkAvailibilty(self):
        book = self.books_drop.currentText()
        self.cur.execute(
            f"SELECT Copies_Available from books WHERE Book_title = '{book}'"
        )
        res = self.cur.fetchone()
        if int(res[0]) == 0:
            self.result.setText(
                f"Sorry All {book} books have been currently lent out :( "
            )
        if int(res[0]) > 0:
            self.result.setText(
                f"There are currently {res[0]} copies of {book} avaliable :)"
            )

    def assignBook(self):
        isbn = self.book_id.text()
        name = self.book_name_2.text()
        cust = self.customer_id.text()
        issueDate = self.issue_date.text()
        returnDate = self.return_date.text()

        self.cur.execute(
            f"INSERT INTO issue VALUES('{random.randint(10000000000,99999999999)}','{name}','{isbn}','{issueDate}','{returnDate}','{cust}')"
        )
        self.con.commit()
        self.cur.execute(
            f"UPDATE books SET Copies_Available=Copies_Available-1 WHERE ISBN='{isbn}'"
        )
        self.con.commit()
        self.setTable("issue")

    def updateCopies(self):
        self.groupBox.setEnabled(False)
        self.stackedWidget_2.setCurrentWidget(self.update_copies_screen)
        print("update book")

    def updateBookCopies(self):
        try:
            book_id = self.new_book_id.text()
            copies = str(self.new_book_copies.value())
            self.cur.execute(
                f"Update books set Copies = '{copies}' where ISBN = '{book_id}'"
            )
            self.con.commit()
            message = QMessageBox()
            message.setText("The book copies where successfully updated!!")
            message.exec_()
            self.stackedWidget_2.setCurrentWidget(self.stats)
            self.groupBox.setEnabled(True)
            self.goToActions()
            self.setTable()
        except Exception as e:
            message = QMessageBox()
            message.setText(f"An error occurred: {e}")
            message.exec_()
            self.goToActions()

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
        self.setStats()

    def connectDB(self):
        try:
            host_ = self.lineEdit.text()
            username_ = self.lineEdit_2.text()
            password_ = self.lineEdit_3.text()

            self.con = ms.connect(host=host_, username=username_, password=password_)
            self.status.setText("Connected!")
            self.isConnected = True
            self.cur = self.con.cursor(buffered=True)

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

    def setTable(self, table="books"):
        try:
            row = 0
            tableX = self.tables_drop.currentText() or table
            if tableX == "other":
                raise Exception("This Table is off limits!")

            self.cur.execute(f"Select col from other where name='{tableX}'")

            headers = self.cur.fetchone()[0].split()

            self.tableWidget.setColumnCount(len(headers))
            self.tableWidget.setHorizontalHeaderLabels((headers))

            self.cur.execute(f"SELECT * from {tableX}")
            data = self.cur.fetchall()
            self.tableWidget.setRowCount(len(data))
            for i in data:
                for j in range(len(headers)):
                    self.tableWidget.setItem(row, j, QtWidgets.QTableWidgetItem(i[j]))
                row += 1
        except Exception as err:
            message = QMessageBox()
            message.setText(f"An error occurred: {err}")
            message.exec_()


app = QApplication([])
window = MyGUI()
app.exec_()
