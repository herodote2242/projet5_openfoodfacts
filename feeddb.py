#/bin/env python3
# -*- coding: Utf-8 -*

import requests
from pprint import pprint

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
