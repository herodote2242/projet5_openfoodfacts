#!/usr/bin/env python3
# -*- coding: Utf-8 -*

import requests
import records
from pprint import pprint


def feed_db(self):
    """This functions collects data from the Open Food Facts API
    according to the criteria and stores them into the database"""
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
        "page_size":100,
        "json":1
    }
    req=requests.get(url, params=criteria)
    pprint(req.json())

class DatabaseFeeder:
    """ This class will integrate the results of the feed_db function into the
    different tables created in the database : product, category, store."""

    def __init__(self, connection, req):
        self.db = connection
        self.req = req

    def product_manager(self):
        self.db.query("""INSERT INTO 'product' (code, product_name, brand, url_links
            store, nutrition_grade_fr) VALUES (self.req)""")

    def category_manager(self):
        self.db.query("""INSERT INTO 'category' (id, category_name) VALUES (self.req)""")

    def store_manager(self):
        self.db.query("""INSERT INTO 'store' (id, store) VALUES (self.req)""")

#Tests:
if __name__=="__main__":
    feeder = DatabaseFeeder(connection, req)
    feeder.product_manager()
    feeder.category_manager()
    feeder.store_manager()

