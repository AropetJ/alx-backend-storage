#!/usr/bin/env python3
"""101-students.py"""


def top_students(mongo_collection):
    """
    Returns a cursor to the top students in the MongoDB
    collection.
    Args:
        mongo_collection (pymongo.collection.Collection):
        The MongoDB collection.
    Returns:
        pymongo.command_cursor.CommandCursor: A cursor to
        the top students, sorted by average score in descending order.
    """
    return mongo_collection.aggregate([
        {"$project": {"name": "$name", "averageScore":
                      {"$avg": "$topics.score"}}},
        {"$sort": {"averageScore": -1}}
    ])
