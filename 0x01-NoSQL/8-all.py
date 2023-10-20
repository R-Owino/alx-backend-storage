#!/usr/bin/env python3
"""
Contains a function list_all
"""


def list_all(mongo_collection):
    """
    Lists all documents in a collection

    Args:
        mongo_collection (list): list of documents in a collection

    Return:
        List of documents, otherwise empty list if none is found
    """
    all_documents = list(mongo_collection.find({}))
    return all_documents
