#!/usr/bin/env python3
# -*- coding: Utf-8 -*

import feeddb

data = "".split()

def list_category():
"""This function stores the different categories and adds one if not already added"""
    already_added = set()
    for category in data:   
        if category not in already_added:
            already_added.add(category)