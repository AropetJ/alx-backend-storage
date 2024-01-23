#!/usr/bin/env python3
# 8-all.py

def list_all(mongo_collection):
    """
    Lists all documents in a MongoDB collection.
    Args:
        mongo_collection (pymongo.collection.Collection):
        The MongoDB collection object.
    Returns:
        list: A list of all documents in the collection.
    """
    documents = list(doc for doc in mongo_collection.find())
    return documents
