#!/usr/bin/env python3
"""102-log_stats.py"""
from pymongo import MongoClient


def print_stats(nginx_logs):
    """
    Print the number of logs, the methods used, and the status checks.
    Args:
    - nginx_logs: The collection of Nginx logs
    Returns:
    - None
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


def print_ips(nginx_logs):
    """
    Print the IP addresses and the number of requests for each.

    Args:
    - nginx_logs: The collection of Nginx logs

    Returns:
    - None
    """
    print("IPs:")
    ip_logs = nginx_logs.aggregate(
        [
            {"$group": {"_id": "$ip", "totalRequests": {"$sum": 1}}},
            {"$sort": {"totalRequests": -1}},
            {"$limit": 10},
        ]
    )
    for ip_log in ip_logs:
        ip = ip_log["_id"]
        ip_requests_count = ip_log["totalRequests"]
        print(f"\t{ip}: {ip_requests_count}")


if __name__ == "__main__":
    client = MongoClient()
    nginx_logs = client.logs.nginx
    print_stats(nginx_logs)
    print_ips(nginx_logs)
