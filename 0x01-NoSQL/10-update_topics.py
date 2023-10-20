#!/usr/bin/env python3
"""
Contains a function update_topics
"""


def update_topics(mongo_collection, name, topics):
    """
    Update the topics of a school document based on the school's name

    Args:
        mongo_collection (pymongo.collection.Collection): The PyMongo
        collection object
        name (str): The school name to update
        topics (list): The list of topics to be set for the school

    Returns:
        int: The number of documents updated (0 or 1)
    """
    filter_criteria = {"name": name}
    update_data = {"$set": {"topics": topics}}
    result = mongo_collection.update_many(filter_criteria, update_data)
    return result
