#!/usr/bin/env python3
"""Contains the function `insert_school`"""


def insert_school(mongo_collection, **kwargs):
    """Inserts a new document into a collection based on `kwargs`"""
    return mongo_collection.insert_one(kwargs).inserted_id
