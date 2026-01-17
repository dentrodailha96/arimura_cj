-- Create tables

CREATE TABLE IF NOT EXISTS products(
    id_product SERIAL NOT NULL 
  , name VARCHAR(500) NOT NULL
  , price_product DECIMAL(10,2) NOT NULL
  , sales_unit VARCHAR(5000)
  , last_modified TIMESTAMP NULL);

CREATE TABLE IF NOT EXISTS client(
    id_client SERIAL
  , name VARCHAR(500) NOT NULL
  , telephone varchar(15) NOT NULL
  , address varchar(500) NULL
  , email varchar(500) NULL);

CREATE TABLE IF NOT EXISTS orders(
    id_order SERIAL NOT NULL
  , id_client INT NOT NULL
  , status VARCHAR(100) NULL
  , delivery_date DATE NOT NULL
  , delivery_time TIME NOT NULL
  , created_at TIMESTAMP NULL);

CREATE TABLE IF NOT EXISTS order_product(
    id SERIAL NOT NULL
  ,  id_order INT 
  , id_product INT 
  , quantity INT NOT NULL
  , unit_price DECIMAL(10,2) NULL
  , observation VARCHAR (4000));

