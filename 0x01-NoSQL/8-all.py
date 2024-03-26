#!/usr/bin/env python3
"""This script contains the `list_all` function"""


def list_all(mongo_collection):
    """Lists all documents in a collection"""
    return mongo_collection.find()
