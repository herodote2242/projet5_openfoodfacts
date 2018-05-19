#!/usr/bin/env python3
# -*- coding: Utf-8 -*

tags = ("purees", "pates a tartiner", "pizza", "poissons", "pain", "pates")

class CategoryCleaner:
    """The class defines the function to clean the categories."""

    def __init__(self, categories):
        self.categories = categories

    def clean_categories(self, categories):
        """The function is used to clean the categories : it makes sure
        all of them are written in lower case, and whitout spaces."""
        categories = categories.lower()
        categories = re.split(r',\s*', categories)
        return categories


class StoreCleaner:
    """The class defines the function to clean the stores."""

    def __init__():
        self.stores = stores

    def clean_stores(self, stores):
        """The function cleans the names of the stores : they are all written in lower case
        without spaces."""
        stores = stores.lower()
        stores = re.split(r',\s*', stores)
        return stores
