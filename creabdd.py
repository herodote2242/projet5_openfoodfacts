#!/bin/env python3
# -*- coding: Utf-8 -*


import sqlite3

conn = sqlite3.connect('C:/Users/Douline/Documents/Doudou/informatique/openclassrooms/travaux_pratiques/P5/dboff')
curs =conn.cursor()
creatable = 'CREATE TABLE donnees_openfoodfacts (code MEDIUMINT(8) UNSIGNED NOT NULL, product_name VARCHAR(100) NOT NULL,\
                brands VARCHAR(50) NOT NULL, ingredients_text TEXT, lien_url VARCHAR(200), store VARCHAR(50), categories VARCHAR(250),\
                nutrition_grade_fr CHAR(1), serving_size VARCHAR(10))'
curs.execute(creatable)
