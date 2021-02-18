#import sqlite3
import mysql.connector
from PyQt5.QtWidgets import QApplication, QTableView, QWidget, QGridLayout, QPushButton, \
QTreeView, QListView, QComboBox , QMessageBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from win32api import GetSystemMetrics
from PyQt5 import QtCore
import SUBD_login
import sys 
from enter_window import enter_window

class Table(QWidget):
    def __init__(self,data=None,parent = None, db = None):
        super().__init__() 
        self.db = db
        self.sql = db.cursor()  
        self.table_name = "customer"
        self.tables = {}
        self.get_tables()
        data = self.sql.execute("SELECT * FROM users")
        #MainWindow.showFullScreen()
        #QWidget.showFullScreen()
        self.setWindowTitle("СУБД_Толстиков_9СК-31")
        self.model = QStandardItemModel()
        self.table = QTableView()
        self.table.setModel(self.model) 
        self.table.horizontalHeader().setSectionResizeMode(1)

        #self.table.setVerticalHeader(mass[0])

        self.btnEnter = QPushButton("Enter") 
        self.btnSave = QPushButton("Save")
        self.btnDel = QPushButton('Delete')     
        
        self.table_comboBox = QComboBox( )

        self.table_comboBox.activated[str].connect(self.choise_table) 

        self.btnEnter.clicked.connect(self.enter_window)
        self.btnSave.clicked.connect(self.save)
        self.btnDel.clicked.connect(self.delete)
        grid = QGridLayout(self)
        grid.setContentsMargins(1,1,1,1)
        grid.addWidget(self.table,0,0,4,4)
        grid.addWidget(self.btnEnter,4,0,1,1)
        grid.addWidget(self.btnSave,4,3,1,1)
        grid.addWidget(self.btnDel,4,2,1,1)
        grid.addWidget(self.table_comboBox,4,1,1,1)

        self.LW = SUBD_login.login_window(self, db=db)  
        self.LW.show()

        self.hide()


        self.data = []
        self.sql.fetchall()
        self.sql.execute(f"SELECT * FROM {self.table_name}")
        for i in self.sql.fetchall():
            self.data.append(i)
    
    def delete(self): 
        try: 
            row_number = self.table.selectionModel().selectedIndexes()[0].row()     # удаление записи по id
            item = int(self.model.item(row_number,0).text())
            self.sql.execute(f"DELETE FROM {self.table_name} WHERE id = {item}") 
            self.sql.execute(f"SELECT MAX(id) FROM {self.table_name} ") 
            i = int(self.sql.fetchone()[0])
            for i in range(item, i):    
                self.sql.execute(f"UPDATE {self.table_name} SET id = '{i}' WHERE id = {i+1}") 
                
            self.db.commit()
            self.load_data()
        except:
            pass

    def choise_table(self, table_name):         # shows table with choisen name
        self.table_name = table_name
        self.load_data()
    def set_combo_box_values(self, premissions): 
        try:
            premissions_splited = premissions.split(" ")  
            if premissions_splited[0] == "only":
                self.choise_table(premissions_splited[1])   
                for i in premissions_splited:      #  выбор только из таблиц названия которых после "only"
                    if i in self.tables:
                        self.table_comboBox.addItem(i) 
            else:
                self.sql.execute(f"SHOW tables FROM {self.db.database}")    # получениче всех названий таблиц запросом
                for i  in ( self.sql.fetchall()):
                    self.table_comboBox.addItem(i[0])            # добавление названий таблиц 
                if premissions != "admin":                   # удаление по условию
                    self.table_comboBox.removeItem(len(self.tables) - 1)
        except:
            QMessageBox.question(self, 'Ошибка', "Ошибка в указании прав доступа",  QMessageBox.Cancel, QMessageBox.Cancel)    
            self.destroy()
    def enter_window(self):
        ew = enter_window(self,table=self.table_name, db=self.db)
        ew.show()

    def load_data(self):         # load(update) data to table from database
        self.data = []
        #self.sql.fetchall() 
        self.sql.execute(f"SELECT * FROM {self.table_name}")
        for i in self.sql.fetchall(): 
            self.data.append(i)
        try:
            rows = len(self.data)
            cols = len(self.data[0])
        except:
            rows = 0
            cols = 0
        self.model.setHorizontalHeaderLabels(self.tables[self.table_name])
        self.model.setColumnCount(cols)
        self.model.setRowCount(rows)
        
        for row in range(rows):
            for col in range(cols):
                item = QStandardItem(str(self.data[row][col]))
                if col == 0:
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.model.setItem(row,col,item)
            
    def save(self):  # сохранение значений из таблицы в бд
        self.data = self.get_data_from_table()   
        try:
            for i in range(0, len(self.data)): 
                for j in range(1, len(self.tables[self.table_name])):   
                    self.sql.execute(f"UPDATE {self.table_name} SET {self.tables[self.table_name][j]} = \
                        '{self.data[i][j]}' WHERE id = {i}")
            self.db.commit()
        except:
            QMessageBox.question(self, 'Ошибка', "Проверьте введеные значения",  QMessageBox.Cancel, QMessageBox.Cancel)    

    def get_tables(self):    # получение списка столбцов из бд
        self.sql.execute(f"SHOW tables FROM {self.db.database}") 
        table_list = []
        for i, val  in enumerate( self.sql.fetchall()):
            table_list.append(val[0]) 
        
        for i in table_list: 
            self.sql.execute(f"SHOW COLUMNS FROM {i};")
            self.tables[i] = []
            for j in self.sql.fetchall():
                self.tables[i].append(j[0])  
        print(self.tables)

    def get_data_from_table(self):
        rows = self.model.rowCount()
        cols = self.model.columnCount()
        out = [[self.model.item(i,j).text() for j in range(cols)] for i in range(rows)] 
        return (out)
        
                
def main_table(db):
    app = QApplication([]) 
    w = Table(db=db)
    #w.showFullScreen()
    w.resize( GetSystemMetrics(0),GetSystemMetrics(1)-80) 
    w.load_data()
    sys.exit(app.exec_())