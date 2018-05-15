#!/usr/bin/env python3
# -*- coding: Utf-8 -*

import requests
import records
from pprint import pprint
import creadb

class DatabaseFeeder:
    """ This class will integrate the results of the feed_db function into the
    different tables created in the database : product, category, store."""

    def __init__(self, connection):
        self.db = connection
        self.data = None

    def fetch_data(self):
        """This functions collects data from the Open Food Facts API
        according to the criteria"""
        url="https://fr.openfoodfacts.org/cgi/search.pl"
        criteria={
            "action":"process",
            "tagtype_0":"categories",
            "tag_contains_0":"contains",
            "tag_0":"produits laitiers",
            "tagtype_1":"nutrition_grades",
            "tag_contains_1":"contains",
            "tag_1":"a",
            "sort_by":"product_name",
            "page_size":3,
            "json":1
        }
        req=requests.get(url, params = criteria)
        #pprint(req.json())
        #print(req.url)
        self.data = req.json()

    def use_database(self):
        """The function only exists to point to the right database"""
        self.db.query("""USE projet5;""")

    def clean_tables(self):
        self.db.query("""DELETE FROM product;""")
        self.db.query("""DELETE FROM category;""")
        self.db.query("""DELETE FROM store;""")
        self.db.query("""DELETE FROM product_category;""")
        self.db.query("""DELETE FROM product_store;""")

    def product_manager(self):
        """The function is responsible of feeding the table "product" with the API's results"""
        products = self.data["products"]
        for product in products:
            self.db.query("""INSERT INTO product (code, product_name, brand, url_link,
                nutrition_grade_fr) VALUES (:code, :product_name, :brand, :url_link,
                :nutrition_grade_fr);""", code = int(product["code"]), product_name = product["product_name"], 
                brand = product["brands"], url_link = product["url"],
                nutrition_grade_fr = product["nutrition_grade_fr"])

    def category_manager(self):
        """The function is responsible of feeding the table "category" with the API's results"""
        products = self.data["products"]
        categories = []
        for product in products:
            cat_list = product["categories"].split(",")
            categories.extend(cat_list)
            self.db.query("""INSERT INTO category (category_name)
                VALUES (:category_name) ON DUPLICATE KEY UPDATE category_name=:category_name;""",
                category_name = product["categories"])
        # To erase doubles
        categories = set(categories)

    def store_manager(self):
        """The function is responsible of feeding the table "store" with the API's results"""        
        products = self.data["products"]
        stores = []
        for product in products:
            sto_list = product["stores"].split(",")
            stores.extend(sto_list)
            self.db.query("""INSERT INTO store (store)
                VALUES (:store_name);""", store_name = product["stores"])
        # To erase doubles
        stores = set(stores)

    
    def product_store_manager(self):
        for store in sto_list:
            self.db.query("""INSERT INTO product_store (product_code, store_id) VALUES ((SELECT id
                FROM product WHERE name = :product_name), (SELECT id from store WHERE name = :product_store));""", 
                product_name = product_name,
                product_store = store
            )

    def product_category_manager(self):
        for category in cat_list:
            self.db.query("""INSERT INTO product_category (product_id, category_id) VALUES ((SELECT id
                FROM category WHERE name = :product_name), (SELECT id from category WHERE name = :product_category));""",
                product_name = product_name,
                product_category = product_category
            )


class CategoryCleaner:
    """This is a class used to make sure only one example of each kind of
    categories is added to the table."""

    def clean(self, categories):
        """The function is used to clean the categories : it makes sure
        all of them are in lower cas, and calls two other functions to structure them"""
        categories = categories.lower()
        categories = self._tolist(categories)
        categories = self._remove_tagged(categories)
        return categories

    def _tolist(self, categories):
        """This function is responsible of eliminating the "s" at the end of a category
        if it's a plural form"""
        categories = re.split(r', \s*', categories)
        return categories

    def _remove_tagged(self, categories):
        """A function eliminating every result if containing a colon"""
        return [cat in categories if ':' not in cat]


#Tests:
if __name__=="__main__":
    connection = records.Database("mysql+pymysql://root:root@localhost/?charset=utf8mb4")
    feeder = DatabaseFeeder(connection)
    feeder.fetch_data()
    feeder.use_database()
    feeder.clean_tables()
    feeder.product_manager()
    feeder.category_manager()
    feeder.store_manager()
    feeder.product_store_manager()
    feeder.product_store_manager()
