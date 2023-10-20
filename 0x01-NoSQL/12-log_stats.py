#!/usr/bin/env python3
"""
Contains a function nginx_logs_stats
"""

from pymongo import MongoClient


def nginx_logs_stats():
    """
    Provides some stats about Nginx logs stored in MongoDB
    """
    # Connect to the MongoDB
    client = MongoClient('mongodb://localhost:27017')
    db = client['logs']
    collection = db['nginx']

    # Count the total number of logs
    total_logs = collection.count_documents({})

    # Count the number of logs for each HTTP method
    http_methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_counts = {}
    for method in http_methods:
        method_counts[method] = collection.count_documents({"method": method})

    # Count the number of logs with a specific method and path
    status_check_count = collection.count_documents({"method": "GET",
                                                     "path": "/status"})

    # Display the results in the specified format
    print(f"{total_logs} logs")
    print("Methods:")
    for method, count in method_counts.items():
        print(f"\tmethod {method}: {count}")
    print(f"{status_check_count} status check")


if __name__ == "__main__":
    nginx_logs_stats()
