#!/usr/bin/env python3
# -*- coding: Utf-8 -*

import feeddb
import creadb
#import app
import records

class Favorite():
    def __init__(self, connection):
        self.db = connection


    def create_favorite():
        """This function creates a table of results saved as 'favorites' 
        when the user wants to."""
        self.db.query("""CREATE TABLE favorite (
            search_number INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
            product_name VARCHAR(100) NOT NULL,
            brand VARCHAR(50) NOT NULL,
            url_link VARCHAR(200),
            nutrition_grade_fr CHAR(1)
            )
            ENGINE=INNODB""")

    def list_favorite():
        """This function stores into the table 'favorites' if the user decides
        to save the last search done in the application."""
        self.db.query("""INSERT INTO favorite VALUES (seach_number, product_name, brand,
            url_link, nutrition_grade_fr)
            ;""")

#Tests.
if __name__ == '__main__':
    favorite = Favorite(connection)
    favorite.create_favorite()
    favorite.list_favorite()