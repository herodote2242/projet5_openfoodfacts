#!/usr/bin/env python3
# -*- coding: Utf-8 -*

import records
import requests
import config as c


class ProductManager:

    def __init__(self, connection):
        self.db = connection

    def find_n_unhealthy_products_by_category(self, category,
            n=c.NUMBER_OF_BAD_FOOD):

        """This function searches in the database'table "product" n
        random products of the category selected with a bad nutriscore."""
        unhealthy_result = self.db.query(f"""SELECT DISTINCT
            product_name FROM product
            JOIN product_category ON product_category.product_code =
            product.code
            JOIN category ON product_category.category_id = category.id
            WHERE nutrition_grade_fr IN ('c', 'd', 'e')
            AND category.name LIKE :catname
            ORDER BY RAND() LIMIT :n;""",
            catname=category, n=n)
        return unhealthy_result.all(as_dict=True)

    def find_n_healthy_products_by_category(self, category,
            n=c.NUMBER_OF_GOOD_FOOD):
        """This function searches in the database'table "product" n
        random products of the category selected with a good nutriscore."""
        healthy_result = self.db.query(f"""SELECT DISTINCT product_name,
            code, url_link, nutrition_grade_fr, brand FROM product
            JOIN product_category ON product_category.product_code =
            product.code
            JOIN category ON product_category.category_id = category.id
            WHERE nutrition_grade_fr IN ('a', 'b')
            AND category.name = :catname
            ORDER BY RAND() LIMIT :n;""",
            catname=category, n=n)
        return healthy_result.all(as_dict=True)

    def find_product_description(self, product_code):
        """This function shows the description of a selected product."""
        description = self.db.query(f"""SELECT * FROM product
            WHERE product.code = :code""",
            code=product_code)
        return description.all(as_dict=True)


class StoreManager:
    """ This class contains the function related to the actions
    the user can ask for related to the table 'store'."""
    def __init__(self, connection):
        self.db = connection

    def find_stores_by_product_code(self, product_code):
        """ The function is called when the user wants to know
        where he can buy a product."""
        stores = self.db.query(f"""SELECT store.name FROM store
            JOIN product_store ON product_store.store_id = store.id
            JOIN product ON product_store.product_code = code
            WHERE product.code = :code""", code=product_code)
        return stores.all(as_dict=True)


class FavoriteManager:
    """This class contains the different SQL queries related
    to the table 'favorites'."""

    def __init__(self, connection):
        self.db = connection

    def find_favorite_list(self):
        """ The function displays all the favorites saved in the table
        and their names."""
        favorites = self.db.query(f"""SELECT code, product_name FROM favorite
            JOIN product ON favorite.product_id = product.code""")
        return favorites.all(as_dict=True)

    def add_favorite_from_product_code(self, product_code):
        """ The function is called when the user wants to add a
        product into the table favorite."""
        self.db.query(f"""INSERT INTO favorite VALUES (:product_code)
            ON DUPLICATE KEY UPDATE product_id = :product_code""",
            product_code=product_code)

    def delete_from_favorite(self, product_code):
        """ The function is called when the user wants to delete one of the
        favorites."""
        self.db.query(f"""DELETE FROM favorite WHERE product_id =
            :product_code""", product_code=product_code)

    def find_favorite_description(self, product_code):
        """This function shows the description of a selected product."""
        description = self.db.query(f"""SELECT * FROM product JOIN favorite
            ON product.code = favorite.product_id""",
            product_code=product_code)
        return description.all(as_dict=True)


# Tests:
if __name__ == "__main__":
    connection = records.Database(c.DATABASE_URL)
