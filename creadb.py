#!/bin/env python3
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

    def __init__(self, connection, dbname):
        self.dbname = connection
        self.dbname.query = ("""CREATE DATABASE offdatabase CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_unicode_ci';""")
        self.db.query("""USE offdatabase;""")


    def create_products_table(self):
        """Creates a table listing the products to be added to the database."""
        self.db.query("""CREATE TABLE products_table (
            code MEDIUMINT UNSIGNED NOT NULL PRIMARY KEY,
            product_name VARCHAR(100) NOT NULL,
            brands VARCHAR(50) NOT NULL,
            ingredients_text TEXT,
            lien_url VARCHAR(200),
            store VARCHAR(150),
            categories TEXT,
            nutrition_grade_fr CHAR(1),
            serving_size VARCHAR(50)
            );
            """)

    def create_categories_table(self):
        """Creates a table linking a product with one or several category/ies."""
        self.db.query("""CREATE TABLE categories_table (
            code MEDIUMINT UNSIGNED NOT NULL,
            product_name VARCHAR(100),
            categories TEXT
            );
            """)

    def create_store_table():
        """Creates a table linking a product with one or several store(s)."""
        self.db.query("""CREATE TABLE store_table (
            code MEDIUMINT UNSIGNED NOT NULL,
            product_name VARCHAR(100) NOT NULL,
            store VARCHAR(150)
            );
            """)
        




if __name__ == "__main__":
    connection = records.offdatabase("mysql + pymysql = //root:rootroot.77@localhost/? charset = utf8mb4")
    creator = DatabaseCreator(connection)
    creator.create_db("projet5")
    creator.create_products_table()
    creator.create_category_table()

