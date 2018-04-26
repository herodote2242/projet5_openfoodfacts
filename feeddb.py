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

    def feed_db(self):
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
        req=requests.get(url, params=criteria)
        pprint(req.json())

    def product_manager(self):
        """The function is responsible of feeding the table "product" with the API's results"""
        self.db.query("""INSERT INTO 'product' (code, product_name, brand, url_links,
            store, nutrition_grade_fr) VALUES (:code, :product_name, :brand, :url_links,
            :store, :nutrition_grade_fr);""")

    def category_manager(self):
        """The function is responsible of feeding the table "category" with the API's results"""
        self.db.query("""INSERT INTO 'category' (id, category_name)
            VALUES (:id, :category_name);""")

    def store_manager(self):
        """The function is responsible of feeding the table "store" with the API's results"""        
        self.db.query("""INSERT INTO 'store' (id, store) VALUES (:id, :store);""")

#Tests:
if __name__=="__main__":
    connection = records.Database("mysql+pymysql://root:root@localhost/?charset=utf8mb4")
    feeder = DatabaseFeeder(connection)
    feeder.feed_db()
    feeder.product_manager()
    feeder.category_manager()
    feeder.store_manager()

