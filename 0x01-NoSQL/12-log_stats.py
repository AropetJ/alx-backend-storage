#!/usr/bin/env python3
'''12-log_stats.py
'''
from pymongo import MongoClient


def print_stats(nginx_logs):
    """
    Print the number of logs, the methods used, and the status checks.
    Args:
        nginx_logs (pymongo.collection.Collection): The collection of
        Nginx logs.
    """
    log_count = nginx_logs.count_documents({})
    print(f"{log_count} logs")
    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        method_logs = nginx_logs.find({"method": method})
        method_count = method_logs.count()
        print(f"\tmethod {method}: {method_count}")
    status_logs = nginx_logs.find({"method": "GET", "path": "/status"})
    status_count = status_logs.count()
    print(f"{status_count} status check")


if __name__ == "__main__":
    client = MongoClient()
    nginx_logs = client.logs.nginx
    print_stats(nginx_logs)
