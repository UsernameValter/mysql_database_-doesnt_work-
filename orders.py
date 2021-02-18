import mysql.connector
from PyQt5.QtWidgets import QApplication, QTableView, QWidget, QGridLayout, QPushButton, \
QTreeView, QListView, QComboBox, QLabel, QLineEdit, QDialog,QMessageBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem , QFont
from PyQt5 import QtCore 
import SUBD_table
from datetime import datetime 

class input_sold(QDialog):
    def __init__(self, parent = None, db = None, order=0,num=0):
        super(input_sold, self).__init__(parent)
        self.db = db
        self.order =order
        self.sql = db.cursor()    
        self.table = "sold"
        newfont = QFont("Times", 12, QFont.Bold)  
        self.parent = parent
        self.sql.execute(f"SELECT MAX(id) FROM {self.table} ")
        self.last_note = self.sql.fetchone()[0] 
        if self.last_note == None:
            self.last_note = 0
        else:
            self.last_note += 1
            self.last_note += num
        self.model = QStandardItemModel()   
  
        grid = QGridLayout(self)
        grid.setContentsMargins(30,30,30,30)  
        self.empty_label = ( QLabel() )      #  отступ слева
        self.empty_label.setText("")
        grid.addWidget(self.empty_label,1,0,1,1)
        
        self.label_title = ( QLabel() )    #   заголовок
        self.label_title.setText(f"Order №{self.order}") 
        self.label_title.setFont(newfont)        
        grid.addWidget(self.label_title,0,1,1,1)
 
 
        self.label_name =  QLabel()       # product_name
        self.label_name.setText(" Название товара") 
        self.label_name.setFont(newfont)        
        grid.addWidget(self.label_name,0,2,1,1)
 

        self.lineEdit = QLineEdit()      #  ввод значений столбцов
        grid.addWidget(self.lineEdit , 1,2,1,2 )  

        self.btnEnter = QPushButton("Ввод")      #  кнопка ввода
        grid.addWidget(self.btnEnter,2,2,1,1)

 
        self.btnEnter.clicked.connect(self.end) 

        
        #self.setFixedSize(444,300)

    def end(self, parameter_list): 
            #self.sql.execute(f"INSERT INTO sold VALUES ({self.last_note},{self.lineEdit.text()},{self.order} )")
        
        self.sql.execute(f"SELECT product_name FROM product WHERE product_name = '{self.lineEdit.text()}'") 
        if not self.sql.fetchone(): 
            QMessageBox.question(self, 'Ошибка', "Товар отсудствует на складе",  QMessageBox.Cancel, QMessageBox.Cancel)

        else: 
            self.hide()
            self.parent.return_value([self.last_note,self.lineEdit.text(),self.order])
            self.parent.setDisabled(False)   