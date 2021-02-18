import mysql.connector
from PyQt5 import QtCore, QtGui, QtWidgets 
import SUBD_table



class login_window(QtWidgets.QDialog):
    def __init__(self, parent=None,db=None ):
        super(login_window, self).__init__(parent) 
        self.parent = parent
        self.db = db
        self.setupUi(self)
        self.pushButton.clicked.connect(self.login_def) 

    def login_def(self):     # сравнение логина со списком юзеров в бд
        log = self.lineEdit.text() 
        sql = self.db.cursor() 
        password = self.lineEdit_2.text() 

        sql.execute(f"SELECT login FROM users WHERE login = '{log}' and password = '{password}' ")
        if sql.fetchone() is None:
            self.label_3.setText("Пароль или логин введен не правильно")   
        else:  
            self.hide()
            self.parent.show()
            sql.execute(f"SELECT premissions FROM users WHERE login = '{log}'")
            prem = sql.fetchone()[0]
            self.parent.set_combo_box_values(prem)          

    def setupUi(self, Form):    
            Form.setObjectName("Form")
            #Form.resize(211, 211)
            Form.setFixedSize(211, 211)
            self.verticalLayout = QtWidgets.QVBoxLayout(Form)
            self.verticalLayout.setObjectName("verticalLayout")
            spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
            self.verticalLayout.addItem(spacerItem)
            spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
            self.verticalLayout.addItem(spacerItem1)
            spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
            self.verticalLayout.addItem(spacerItem2)
            self.formLayout = QtWidgets.QFormLayout()
            self.formLayout.setObjectName("formLayout")
            self.label = QtWidgets.QLabel(Form)
            self.label.setObjectName("label")
            self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label)
            self.lineEdit = QtWidgets.QLineEdit(Form)
            self.lineEdit.setObjectName("lineEdit")
            self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit)
            self.label_2 = QtWidgets.QLabel(Form)
            self.label_2.setObjectName("label_2")
            self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_2)
            self.lineEdit_2 = QtWidgets.QLineEdit(Form) 
            self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password) 
            self.lineEdit_2.setObjectName("lineEdit_2")
            self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEdit_2)
            spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
            self.formLayout.setItem(3, QtWidgets.QFormLayout.LabelRole, spacerItem3)
            self.pushButton = QtWidgets.QPushButton(Form)
            self.pushButton.setObjectName("pushButton")
            self.formLayout.setWidget(4, QtWidgets.QFormLayout.SpanningRole, self.pushButton)
            spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
            self.formLayout.setItem(5, QtWidgets.QFormLayout.LabelRole, spacerItem4)
            spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
            self.formLayout.setItem(0, QtWidgets.QFormLayout.FieldRole, spacerItem5)
            self.label_3 = QtWidgets.QLabel(Form)
            self.label_3.setText("")
            self.label_3.setWordWrap(True)
            self.label_3.setAlignment(QtCore.Qt.AlignCenter)
            self.label_3.setObjectName("label_3")
            self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.label_3)
            self.verticalLayout.addLayout(self.formLayout)

            self.retranslateUi(Form)
            QtCore.QMetaObject.connectSlotsByName(Form)    
    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Вход"))
        self.label.setText(_translate("Form", "Логин"))
        self.label_2.setText(_translate("Form", "Пароль"))
        self.pushButton.setText(_translate("Form", "Вход"))
