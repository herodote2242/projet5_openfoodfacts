#!/usr/bin/env python3
# -*- coding: Utf-8 -*

CATEGORIES_TO_RECOVER = {"Purées" : "%purees%", "Pâtes à tartiner" : "%tartiner%",
    "Pizzas" : "%pizza%", "Poissons" : "%poisson%", "Pains" : "%pain%", "Chocolat" : "%chocolat%"}
GRADES_TO_RECOVER = ["a", "b", "c", "d", "e"]
NUMBER_OF_PRODUCTS = 500
NUMBER_OF_BAD_FOOD = 10
NUMBER_OF_GOOD_FOOD = 3
DATABASE_URL = "mysql+mysqlconnector://root:root@localhost/projet5?charset=utf8mb4"
DATABASE_NAME = "projet5"
