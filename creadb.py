#!/bin/env python3
# -*- coding: Utf-8 -*

import records

class DatabaseCreator:
    """This class has the responsibility of the database construction.
    It constructs a DatabaseCreator object responsible of creating the tables
    needed for the application.

    ======
    Params:
        connection
        instance of a records.Databaseconnection"""

    def __init__(self, connection, dbname):
        self.dbname = connection
        self.dbname.query = ("""CREATE DATABASE offdatabase (id INT PRIMARY_KEY AUTO_INCREMENT) / 
        CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_unicode_ci';""")

    def create_products_table(self):
        """Creates products in the database."""
        self.db.query("""  """)

    def create_categories_table(self):
        """...."""

    def create_store_table():
        """   """
        




if __name__ == "__main__":
    connection = records.offdatabase("mysql + pymysql = //root:rootroot.77@localhost/? charset = utf8mb4")
    creator = DatabaseCreator(connection)
    creator.create_db("projet5")
    creator.create_products_table()
    creator.create_category_table()

