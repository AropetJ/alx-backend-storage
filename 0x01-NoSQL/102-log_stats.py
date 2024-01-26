#!/usr/bin/env python3
'''Log stats'''
from pymongo import MongoClient


def print_nginx_request_logs(nginx_collection):
    """Prints stats about Nginx request logs.
    Args:
        nginx_collection (collection): The collection of Nginx
        request logs.
    Returns:
        None
    """
    print(f"{nginx_collection.count_documents({})} logs")
    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    for method in methods:
        req_count = nginx_collection.count_documents({'method': method})
        print(f"method {method}: {req_count}")
    status_checks_count = nginx_collection.count_documents({'method':
                                                            'GET', 'path':
                                                            '/status'})
    print(f"{status_checks_count} status check")


def print_top_ips(server_collection):
    """Prints statistics about the top 10 HTTP IPs in a collection.
    Args:
        server_collection (collection): The collection containing the
        server logs.
    Returns:
        None
    """
    print("IPs:")
    request_logs = server_collection.aggregate([
        {'$group': {'_id': "$ip", 'totalRequests': {'$sum': 1}}},
        {'$sort': {'totalRequests': -1}},
        {'$limit': 10}
    ])
    for request_log in request_logs:
        ip = request_log['_id']
        ip_requests_count = request_log['totalRequests']
        print(f"{ip}: {ip_requests_count}")


if __name__ == '__main__':
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx
    print_nginx_request_logs(nginx_collection)
    print_top_ips(nginx_collection)
