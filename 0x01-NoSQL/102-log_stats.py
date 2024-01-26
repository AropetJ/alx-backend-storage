#!/usr/bin/env python3
'''102-log_stats.py'''

from pymongo import MongoClient

if __name__ == "__main__":
    """
    This script connects to a MongoDB database and performs various
    log statistics operations. It retrieves the total number of logs,
    counts the occurrence of different HTTP methods, checks the number
    of status checks, and displays the top 10 IP addresses with the
    highest log count.
    The script uses the PyMongo library to interact with the MongoDB
    database.

    Usage:
    - Make sure MongoDB is running on the local machine.
    - Run the script to see the log statistics.
    """
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx

    n_logs = nginx_collection.count_documents({})
    print(f'{n_logs} logs')

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print('Methods:')
    for method in methods:
        count = nginx_collection.count_documents({"method": method})
        print(f'\tmethod {method}: {count}')

    status_check = nginx_collection.count_documents(
        {"method": "GET", "path": "/status"}
    )

    print(f'{status_check} status check')

    top_ips = nginx_collection.aggregate([
        {"$group":
            {
                "_id": "$ip",
                "count": {"$sum": 1}
            }
         },
        {"$sort": {"count": -1}},
        {"$limit": 10},
        {"$project": {
            "_id": 0,
            "ip": "$_id",
            "count": 1
        }}
    ])

    print("IPs:")
    for top_ip in top_ips:
        ip = top_ip.get("ip")
        count = top_ip.get("count")
        print(f'\t{ip}: {count}')
