#!/usr/bin/env python3
'''11-schools_by_topic.py
'''


def schools_by_topic(mongo_collection, topic):
    """
    Returns the list of school having a specific topic.
    Args:
        mongo_collection (pymongo.collection.Collection):
        The MongoDB collection object.
        topic (str): The topic searched.
    Returns:
        list: A list of school having the topic.
    """
    documents = mongo_collection.find({"topics": topic})
    return documents
