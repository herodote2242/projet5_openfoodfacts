#!/usr/bin/env python3
# -*- coding: Utf-8 -*

import records

class DatabaseCreator:
    """This class is responsible of the database construction, by constructing
    a DatabaseCreator object responsible of creating the tables needed
    for the application.

    ======
    Params:
        connection
        instance of a records.Databaseconnection"""

    def __init__(self, connection):
        self.db = connection
        self.db.query("""CREATE DATABASE IF NOT EXISTS projet5 CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_unicode_ci';""")
        self.db.query("""USE projet5;""")


    def create_product_table(self):
        """Creates a table listing the products to be added to the database."""
        #self.db.query drop table product_category, pour ensuite drop category drop product => faire une méthode clean qui drop les tables dans l'ordre.
        self.db.query("""CREATE TABLE product (
            code INT UNSIGNED NOT NULL PRIMARY KEY,
            product_name VARCHAR(100) NOT NULL,
            brands VARCHAR(50) NOT NULL,
            lien_url VARCHAR(200),
            store VARCHAR(150),
            nutrition_grade_fr CHAR(1)
            );
            """)

    def create_category_table(self):
        """Creates a table linking a product with one or several category/ies."""
        self.db.query("""CREATE TABLE category (
            id MEDIUMINT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
            category_name VARCHAR(100),
            );
            """)

    def create_store_table(self):
        """Creates a table linking a product with one or several store(s)."""
        self.db.query("""CREATE TABLE store (
            id MEDIUMINT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
            store VARCHAR(150)
            );
            """)
        
    def create_product_category_table(self):
        self.db.query("""CREATE TABLE product_category (
            id MEDIUMINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
            product_code INT UNSIGNED REFERENCES product(code),
            category_id MEDIUMINT UNSIGNED REFERENCES category(id)
            );
            """)

if __name__ == "__main__":
    connection = records.Database("mysql+pymysql://root:rootroot@localhost/?charset=utf8mb4")
    creator = DatabaseCreator(connection)
    creator.create_products_table()
    creator.create_category_table()
    creator.create_store_table()

