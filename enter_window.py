import mysql.connector
from PyQt5.QtWidgets import QApplication, QTableView, QWidget, QGridLayout, QPushButton, \
QTreeView, QListView, QComboBox, QLabel, QLineEdit, QDialog,QMessageBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem , QFont
from PyQt5 import QtCore 
import SUBD_table
from datetime import datetime
import orders

class enter_window(QDialog):
    def __init__(self,parent = None,data=None, db = None, table=None):
        super(enter_window, self).__init__(parent)
        self.db = db
        self.sql = db.cursor()    
        self.table = table
        self.sold_all = []
        newfont = QFont("Times", 12, QFont.Bold)  
        self.parent = parent
        self.sql.execute(f"SELECT MAX(id) FROM {table} ")
        self.last_note = self.sql.fetchone()[0] 
        if self.last_note == None:
            self.last_note = 0
        else:
            self.last_note += 1
        self.model = QStandardItemModel()   
  
        grid = QGridLayout(self)
        grid.setContentsMargins(30,30,30,30)  
        self.empty_label = ( QLabel() )      #  отступ слева
        self.empty_label.setText("")
        grid.addWidget(self.empty_label,1,0,1,1)
        
        self.label = ( QLabel() )    #   заголовок
        self.label.setText(table) 
        self.label.setFont(newfont)        
        grid.addWidget(self.label,0,1,1,1)
        self.labels = []
        self.lineEdits = []
        
        self.sql.execute(f"SHOW COLUMNS FROM {table};")
             
        for i, name in enumerate( self.sql.fetchall() ): 
            if name[0] == "date":
                continue
            if name[0] == "price" and self.table == "orders":
                continue
            self.labels.append( QLabel() )      # названия столбцов таблицы 
            self.labels[i].setText(name[0])    
            grid.addWidget(self.labels[i], i+1,1,1,1 ) 

            self.lineEdits.append(QLineEdit())      #  ввод значений столбцов
            grid.addWidget(self.lineEdits[i], i+1,2,1,2 ) 
        else: 
            self.btnEnter = QPushButton("Ввод")      #  кнопка ввода
            grid.addWidget(self.btnEnter,i+2,2,1,1)
        self.lineEdits[0].setText(str(self.last_note))
        self.lineEdits[0].setReadOnly(True)
        if self.table == "orders":
            self.btnEnter.setText("Добавить товар")   
            self.btnEnter.clicked.connect(self.new_item_order) 

            self.btn_new_order = QPushButton("Ввод")      #  кнопка ввода
            grid.addWidget(self.btn_new_order,8,2,1,1)
            self.btn_new_order.clicked.connect(self.input_orders) 
            self.btn_new_order.setDisabled(True)
        else:
            self.btnEnter.clicked.connect(self.values_to_bd)
 

    def values_to_bd(self):      # добавление строки (значения взятые с lineEdit'ов) в таблицу 
        values = [i.text() for i in self.lineEdits ]    
        a = "%s"    # was "?"
        for i in range(1,len(values)):
            a += ", %s"
        try: 
            self.sql.execute(f"INSERT INTO {self.table} VALUES ({a})", values)
            self.db.commit()
            self.parent.load_data()
            self.last_note +=1
            self.lineEdits[0].setText(str(self.last_note))
        except:
            QMessageBox.question(self, 'Ошибка', "Одно из введеных значений не подходит по типу",  QMessageBox.Cancel, QMessageBox.Cancel)


    def input_orders(self):   
        values = [i.text() for i in self.lineEdits ] 
        price = 0
        for i in self.sold_all:
            self.sql.execute(f"SELECT price FROM store WHERE product_name = '{i[1]}'")
            price +=  int(self.sql.fetchone()[0]) 
        values.append(price)
        values.append(datetime.now())
            
        a = "%s"    # was "?"
        for i in range(1,len(values)):
            a += ", %s"
        try:  
            self.sql.execute(f"INSERT INTO orders VALUES ({a})", values)    # вставка в таблицу order
            for i in self.sold_all: 
                self.sql.execute(f"SELECT count FROM store WHERE product_name = '{i[1]}'")
                count = self.sql.fetchone()[0] 
                if count >0:
                    count-=1
                    self.sql.execute(f"INSERT INTO sold VALUES ({i[0]}, '{i[1]}', {i[2]})") #вставка в таблицу sold 
                    self.sql.execute(f"UPDATE store SET count = '{count}' WHERE product_name = '{i[1]}'") 
                else:
                    print("no more products")
                    self.sql.execute(f"SELECT price FROM store WHERE product_name = '{i[1]}'")
                    a = self.sql.fetchone()[0]  
                    price -= int(a)  
                    print("id = ", values[0])
                    self.sql.execute(f"UPDATE orders SET price = '{price}' WHERE id = '{values[0]}'")

            self.db.commit()
            self.parent.load_data()
            self.last_note +=1
            self.lineEdits[0].setText(str(self.last_note))
        except:
            QMessageBox.question(self, 'Ошибка', "Одно из введеных значений не подходит по типу",  QMessageBox.Cancel, QMessageBox.Cancel)

    def return_value(self, sold):
        self.sold_all.append(sold) 
        self.btn_new_order.setDisabled(False)
    def new_item_order(self):
        self.setDisabled(True)
        num = len(self.sold_all)
        if num == None:
            num = 0
        a = orders.input_sold(self, db=self.db, order=self.last_note, num=num)
        a.show()

