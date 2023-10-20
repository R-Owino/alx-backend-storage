#!/usr/bin/env python3
"""
Contains a function schools_by_topic
"""


def schools_by_topic(mongo_collection, topic):
    """
    Retrieve a list of schools that have a specific topic

    Args:
        mongo_collection (pymongo.collection.Collection): The PyMongo
        collection object
        topic (str): The topic to search for

    Returns:
        list: A list of school documents that have the specified topic
    """
    filter_criteria = {"topics": topic}
    result = list(mongo_collection.find(filter_criteria))
    return result
