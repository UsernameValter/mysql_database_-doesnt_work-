import SUBD_login
import SUBD_table
import mysql.connector
# from PyQt5.QtWidgets import QMessageBox 
import sys
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="9876",
        database="shop"   
    )
    sql = db.cursor()
except: 
    # QMessageBox.question(self, 'Ошибка', "Не возможно подключиться к базе данных",  QMessageBox.Cancel, QMessageBox.Cancel)
    sys.exit(0) 


sql.execute("CREATE TABLE IF NOT EXISTS users (id MEDIUMINT NOT NULL,\
     login varchar(20) NOT NULL UNIQUE, password TEXT, premissions VARCHAR(99) DEFAULT 'None',PRIMARY KEY (id) )")

sql.execute("CREATE TABLE IF NOT EXISTS product (id MEDIUMINT NOT NULL, \
    product_name varchar(33) NOT NULL UNIQUE, model TEXT, description TEXT ,PRIMARY KEY (id) )")

sql.execute("CREATE TABLE IF NOT EXISTS customer (id MEDIUMINT NOT NULL, name TEXT, phone varchar(11), PRIMARY KEY (id) )")

sql.execute("CREATE TABLE IF NOT EXISTS store (id MEDIUMINT NOT NULL, product_name varchar(33)  NOT NULL UNIQUE,count INT, price TEXT , PRIMARY KEY (id) ,\
     FOREIGN KEY(product_name) REFERENCES product (product_name) ON DELETE CASCADE ON UPDATE  CASCADE)")

sql.execute("CREATE TABLE IF NOT EXISTS orders (id MEDIUMINT NOT NULL ,customer_id MEDIUMINT,\
    user_login varchar(20)  NOT NULL ,price INT, date DATETIME DEFAULT NOW(), PRIMARY KEY (id),\
        \
            FOREIGN KEY(customer_id) REFERENCES customer (id) ON DELETE CASCADE ON UPDATE  CASCADE, \
              FOREIGN KEY(user_login) REFERENCES users (login) ON DELETE CASCADE ON UPDATE  CASCADE)")

sql.execute("CREATE TABLE IF NOT EXISTS sold(id MEDIUMINT ,product_name varchar(33) NOT NULL, order_id MEDIUMINT ,PRIMARY KEY (id),\
    FOREIGN KEY(order_id) REFERENCES orders (id) ON DELETE CASCADE ON UPDATE  CASCADE,\
        FOREIGN KEY(product_name) REFERENCES product (product_name) ON DELETE CASCADE ON UPDATE  CASCADE)")

sql.execute("SELECT login FROM users WHERE login = 'admin'")
if not sql.fetchone(): 
    sql.execute(f"INSERT INTO users VALUES (%s ,%s ,%s ,%s)", (0,'admin','pass',"admin")) 
    db.commit()

sql.execute("SELECT id FROM customer WHERE id = '0'")
if not sql.fetchone(): 
    sql.execute(f"INSERT INTO users VALUES (%s ,%s ,%s ,%s)", (0,'None','None')) 
    db.commit()

SUBD_table.main_table(db)
sql.close()