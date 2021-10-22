#!/usr/bin/python3

from __future__ import annotations
import os
import time
import requests
import const
import routing_tables_db_util
from model import RoutingTable

def get_table() -> RoutingTable:
    response = requests.post(
        url=const.url,
        json={"query": const.routing_table_query},
    )
    response = response.json()
    response = response["data"]["peerChainState"]["state"]
    return RoutingTable.from_dict(RoutingTable.raw_to_dict(response))

if __name__ == "__main__":
    if not os.path.exists(const.routing_tables_db_path):
        routing_tables_db_util.create_db()
        routing_tables_db_util.create_tables()

    while True:
        try:
            table = get_table()

            routing_tables_db_util.insert_routing_table(table)
            routing_tables_db_util.prune_tables()
        except Exception as e:
            print(e)
            pass

        time.sleep(const.sleep_time)
