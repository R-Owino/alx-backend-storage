#!/usr/bin/env python3
"""
Contains a function top_students
"""


def top_students(mongo_collection):
    """
    Retrieve all students from a MongoDB collection sorted by average score

    Args:
        mongo_collection (pymongo.collection.Collection): The PyMongo
        collection object

    Returns:
        list: A list of student documents sorted by average score
    """
    # Aggregate the scores for each student
    pipeline = [
        {
            "$unwind": "$scores"
        },
        {
            "$group": {
                "_id": "$_id",
                "name": {"$first": "$name"},
                "scores": {"$push": "$scores.score"}
            }
        }
    ]

    top_students = list(mongo_collection.aggregate(pipeline))
    return top_students
