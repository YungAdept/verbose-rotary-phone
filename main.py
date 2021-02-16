import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QHeaderView, QDialog


class Coffee(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.setFixedSize(1157, 686)
        self.con = sqlite3.connect("coffee.sqlite")
        self.cur = self.con.cursor()
        res = self.cur.execute("SELECT * FROM Coffies").fetchall()
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.setRowHeight(4, 200)
        self.tableWidget.setRowCount(len(res))
        self.tableWidget.setColumnWidth(4, 500)
        self.edit.clicked.connect(self.editing)
        self.add.clicked.connect(self.adding)
        for i in range(len(res)):
            elem = res[i]
            self.tableWidget.setItem(i, 0, QTableWidgetItem(str(elem[0])))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(str(elem[1])))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(str(elem[2])))
            self.tableWidget.setItem(i, 3, QTableWidgetItem(str(elem[3])))
            self.tableWidget.setItem(i, 4, QTableWidgetItem(str(elem[4])))
            self.tableWidget.setItem(i, 5, QTableWidgetItem(str(elem[5])))
            self.tableWidget.setItem(i, 6, QTableWidgetItem(str(elem[6])))
        self.tableWidget.itemClicked.connect(self.changer)
    def changer(self, item):
        self.row = item.row()
        self.id = self.tableWidget.item(self.row, 0).text()
        self.name = self.tableWidget.item(self.row, 1).text()
        self.st = self.tableWidget.item(self.row, 2).text()
        self.morz = self.tableWidget.item(self.row, 3).text()
        self.about = self.tableWidget.item(self.row, 4).text()
        self.price = self.tableWidget.item(self.row, 5).text()
        self.capacity = self.tableWidget.item(self.row, 6).text()
    def updating(self):
        res = self.cur.execute("SELECT * FROM Coffies").fetchall()
        self.tableWidget.setRowCount(len(res))
        for i in range(len(res)):
            elem = res[i]
            self.tableWidget.setItem(i, 0, QTableWidgetItem(str(elem[0])))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(str(elem[1])))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(str(elem[2])))
            self.tableWidget.setItem(i, 3, QTableWidgetItem(str(elem[3])))
            self.tableWidget.setItem(i, 4, QTableWidgetItem(str(elem[4])))
            self.tableWidget.setItem(i, 5, QTableWidgetItem(str(elem[5])))
            self.tableWidget.setItem(i, 6, QTableWidgetItem(str(elem[6])))
    def editing(self):
        try:
            result = self.cur.execute(f"""SELECT * FROM Coffies 
                            WHERE id='{self.id}' and name='{self.name}'""").fetchall()
            data = [self.id,
                    self.name,
                    self.st,
                    self.morz,
                    self.about,
                    self.price,
                    self.capacity]
            ed = AddEditCofeeForm(data)
            ed.show()
            ed.exec_()
            self.data = ed.data
            self.cur.execute(f"""DELETE from Coffies where id='{self.data[0]}' and name='{self.data[1]}' and st='{self.data[2]}'""")
            self.cur.execute(f"""INSERT INTO Coffies(id, name, st, morz, about, price, capacity) VALUES('{self.data[0]}', '{self.data[1]}', '{self.data[2]}', '{self.data[3]}', '{self.data[4]}', '{self.data[5]}', '{self.data[6]}')""")
            self.con.commit()
            self.updating()
        except:
            pass
    def adding(self):
        ed = AddEditCofeeForm()
        ed.show()
        ed.exec_()
        try:
            self.data = ed.data
            self.cur.execute(f"""INSERT INTO Coffies(id, name, st, morz, about, price, capacity) VALUES('{self.data[0]}', '{self.data[1]}', '{self.data[2]}', '{self.data[3]}', '{self.data[4]}', '{self.data[5]}', '{self.data[6]}')""")
            self.con.commit()
            self.updating()
        except:
            pass

class AddEditCofeeForm(QDialog):
    def __init__(self, data=[]):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.data = data
        # оk
        if self.data != []:
            self.id.setText(self.data[0])
            self.name.setText(self.data[1])
            self.st.setText(self.data[2])
            self.morz.setText(self.data[3])
            self.about.setText(self.data[4])
            self.price.setText(self.data[5])
            self.capacity.setText(self.data[6])
        self.ok.pressed.connect(self.return_list)
        # cancel
        self.cancel.pressed.connect(self.canceling)
    def canceling(self):
        self.data = None
        self.close()

    def return_list(self):
        self.data = [self.id.text(),
                self.name.text(),
                self.st.text(),
                self.morz.text(),
                self.about.text(),
                self.price.text(),
                self.capacity.text()]
        self.close()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Coffee()
    ex.show()
    sys.exit(app.exec_())
