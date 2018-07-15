#!/usr/bin/env python3
# -*- coding: Utf-8 -*

import requests
import records
import creadb
import re
import config


class DatabaseFeeder:
    """ This class will integrate the results of the fetch_data
    function into the different tables created in the database :
    product, category, store, product_store, product_category.
    """

    def __init__(self, connection):
        self.db = connection
        self.products = []

    def fetch_data(self):
        """This functions collects data from the Open Food Facts API
        according to the criteria."""
        for category in config.CATEGORIES_TO_RECOVER:
            for grade in config.GRADES_TO_RECOVER:
                url = "https://fr.openfoodfacts.org/cgi/search.pl"
                criteria = {
                    "action": "process",
                    "tagtype_0": "categories",
                    "tag_contains_0": "contains",
                    "tag_0": category,
                    "tagtype_1": "nutrition_grade_fr",
                    "tag_contains_1": "contains",
                    "tag_1": grade,
                    "sort_by": "product_name",
                    "page_size": config.NUMBER_OF_PRODUCTS,
                    "json": 1
                }
                req = requests.get(url, params=criteria)
                data = req.json()
                self.products.extend(data["products"])

    def clean_tables(self):
        """A function to erase the tables'data, just in case
        they are already filled.
        """
        self.db.query("""DELETE FROM product_category;""")
        self.db.query("""DELETE FROM product_store;""")
        self.db.query("""DELETE FROM product;""")
        self.db.query("""DELETE FROM category;""")
        self.db.query("""DELETE FROM store;""")
        self.db.query("""DELETE FROM favorite;""")

    def product_invalid(self, product):
        """This function checks if a product has all the informations
        required. If no, it is invalid. If yes, it is valid and can
        be saved in the database.
        """
        keys = ("code", "product_name", "brands", "stores",
                "categories", "url", "nutrition_grade_fr")
        for key in keys:
            if key not in product or not product[key]:
                return True
        return False

    def feed_products(self):
        """The function is responsible of feeding the
        table "product" with the API's results.
        """
        for product in self.products:
            if not self.product_invalid(product):
                self.db.query("""INSERT INTO product (code,
                    product_name, brand, url_link, nutrition_grade_fr)
                    VALUES (:code, :product_name, :brand, :url_link,
                    :nutrition_grade_fr) ON DUPLICATE KEY UPDATE
                    code = :code;""", code=int(product["code"]),
                    product_name=product["product_name"],
                    brand=product["brands"], url_link=product["url"],
                    nutrition_grade_fr=product["nutrition_grade_fr"])
                self.feed_categories(product)
                self.feed_stores(product)

    def clean_categories(self, categories):
        """The function is used to clean the categories : it makes sure
        all of them are written in lower case, and whitout spaces.
        """
        categories = categories.lower()
        categories = re.split(r',\s*', categories)
        return categories

    def feed_categories(self, product):
        """The function is responsible of feeding the
        table "category" with the API's results.
        """
        categories = self.clean_categories(product["categories"])
        for category in categories:
            self.db.query("""INSERT INTO category (name)
                VALUES (:name) ON DUPLICATE KEY UPDATE name = :name;""",
                name=category)
            self.feed_product_category(product, category)

    def clean_stores(self, stores):
        """The function cleans the names of the stores :
        they are all written in lower case without spaces.
        """
        stores = stores.lower()
        stores = re.split(r',\s*', stores)
        return stores

    def feed_stores(self, product):
        """The function feeds the table "stores" with the API's results.
        """
        stores = self.clean_stores(product["stores"])
        for store in stores:
            self.db.query("""INSERT INTO store (name) VALUES (:name)
                ON DUPLICATE KEY UPDATE name = :name;""",
                name=store)
            self.feed_product_store(product, store)

    def feed_product_store(self, product, store):
        """Feeds the table product_store according
        to the data in product and store tables.
        """
        self.db.query("""INSERT INTO product_store (product_code, store_id)
            VALUES (:code, (SELECT id FROM store WHERE name = :store));""",
            code=product['code'], store=store)

    def feed_product_category(self, product, category):
        """Feeds the table product_category according
        to the data in product and category tables.
        """
        self.db.query("""INSERT INTO product_category
            (product_code, category_id) VALUES (:code, (SELECT id
            FROM category WHERE name = :category));""",
            code=product['code'], category=category)


# Tests:
if __name__ == "__main__":
    print("Database feeding started, please wait...")

    connection = records.Database(config.DATABASE_URL)
    feeder = DatabaseFeeder(connection)
    feeder.fetch_data()
    feeder.clean_tables()
    feeder.feed_products()
    print("Feeding complete.")
