#!/usr/bin/env python3
# 9-insert_school.py

def insert_school(mongo_collection, **kwargs):
    """
    Inserts a new document in a collection based on kwargs.
    Args:
        mongo_collection (pymongo.collection.Collection):
        The pymongo collection object.
        **kwargs: Keyword arguments representing the fields
        and values of the document.
    Returns:
        str: The new _id of the inserted document.
    """
    new_document = kwargs
    result = mongo_collection.insert_one(new_document)
    return result.inserted_id
