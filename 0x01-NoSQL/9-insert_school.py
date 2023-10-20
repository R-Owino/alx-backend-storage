#!/usr/bin/env python3
"""
Contains a function insert_school
"""


def insert_school(mongo_collection, **kwargs):
    """
    Insert a new document into a MongoDB collection based on keyword arguments

    Args:
        mongo_collection (pymongo.collection.Collection): The PyMongo
        collection object
        **kwargs: Keyword arguments representing the fields and values
        for the new document

    Returns:
        ObjectId: The _id of the newly inserted document
    """
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
