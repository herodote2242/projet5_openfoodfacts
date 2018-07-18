#!/usr/bin/env python3
# -*- coding: Utf-8 -*

import records
import config


class DatabaseCreator:
    """This class is responsible of the database construction. It constructs
    a DatabaseCreator object responsible of creating the tables needed
    for the application.

    ======
    Params:
        connection
        instance of a records.Databaseconnection
        """

    def __init__(self, connection):
        self.db = connection

    def clean_table(self):
        """A function used to drop existing tables, in order to create
        new ones in case of a modification.
        """
        self.db.query("""DROP TABLE IF EXISTS product_category;""")
        self.db.query("""DROP TABLE IF EXISTS product_store;""")
        self.db.query("""DROP TABLE IF EXISTS product;""")
        self.db.query("""DROP TABLE IF EXISTS category;""")
        self.db.query("""DROP TABLE IF EXISTS store;""")
        self.db.query("""DROP TABLE IF EXISTS favorite""")

    def create_product_table(self):
        """Creates a table listing the products to be added to the database.
        """
        self.db.query("""CREATE TABLE product (
            code BIGINT(20) UNSIGNED NOT NULL PRIMARY KEY,
            product_name VARCHAR(200) NOT NULL,
            brand VARCHAR(200) NOT NULL,
            url_link VARCHAR(255) NOT NULL,
            nutrition_grade_fr CHAR(1) NOT NULL
            )""")

    def create_category_table(self):
        """Creates a table linking a product with one or several
        category/ies.
        """
        self.db.query("""CREATE TABLE category (
            id MEDIUMINT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(150) NOT NULL UNIQUE
            )""")

    def create_store_table(self):
        """Creates a table linking a product with one or several
        store/s.
        """
        self.db.query("""CREATE TABLE store (
            id MEDIUMINT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(150) NOT NULL UNIQUE
            )""")

    def create_product_category_table(self):
        """Creates a table joining the different products and
        related category/ies.
        """
        self.db.query("""CREATE TABLE product_category (
            id MEDIUMINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
            product_code BIGINT UNSIGNED REFERENCES product(code),
            category_id MEDIUMINT UNSIGNED REFERENCES category(id)
            )""")

    def create_product_store_table(self):
        """Create a table joining the different products
        and related store/s.
        """
        self.db.query("""CREATE TABLE product_store (
            id MEDIUMINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
            product_code BIGINT UNSIGNED REFERENCES product(code),
            store_id MEDIUMINT UNSIGNED REFERENCES store(id)
            )""")

    def create_favorite_table(self):
        """This function creates a table of results saved as 'favorites'
        when the user wants to.
        """
        # -tc- mise à jour de la table favoris pour enregistrer le produit substitué
        self.db.query("""CREATE TABLE favorite (
            id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
            product_id BIGINT UNSIGNED REFERENCES product(code), 
            substitute_id BIGINT UNSIGNED REFERENCES product(code)
            )""")

    def create_tables(self):
        """Launches the cleaner, then the different creators for all
        the tables.
        """
        self.clean_table()
        self.create_product_table()
        self.create_category_table()
        self.create_store_table()
        self.create_product_category_table()
        self.create_product_store_table()
        self.create_favorite_table()


def main():
    """Entry point of the module.
    """
    connection = records.Database(config.DATABASE_URL)
    creator = DatabaseCreator(connection)
    creator.create_tables()


if __name__ == "__main__":
    main()
