CREATE DATABASE test_database;
create database shop;
USE test_database; 
USE shop;
SELECT * FROM orders;
SHOW COLUMNS FROM users; 

SHOW tables FROM shop;
CREATE TABLE IF NOT EXISTS store (id TINYINT NOT NULL, product_id TINYINT, PRIMARY KEY (id) , FOREIGN KEY(product_id) REFERENCES product (id) ON DELETE CASCADE ON UPDATE  CASCADE) ;

show columns from orders;
drop table orders, users, store, customer, product; 
drop table customer;
drop table store;
drop table sold;

Insert into orders values (1,1,0,"admin",222,now()) ;
SELECT price FROM product WHERE product_name = 1;

CREATE TABLE IF NOT EXISTS sold(id MEDIUMINT ,product_name varchar(33), order_id MEDIUMINT ,PRIMARY KEY (name), 
 FOREIGN KEY(order_id) REFERENCES orders (id) ON DELETE CASCADE ON UPDATE  CASCADE, FOREIGN KEY(product_name) 
 REFERENCES product (product_name) ON DELETE CASCADE ON UPDATE  CASCADE); 
 SELECT count FROM store WHERE product_name =phone;