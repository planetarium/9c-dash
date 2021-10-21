#!/usr/bin/python3

from __future__ import annotations
import os
import time
import requests
import sqlite3
import const
from model.table import Table

def create_db() -> None:
    con = sqlite3.connect(const.peers_db_path)
    con.commit()
    con.close()
    return

def create_table() -> None:
    con = sqlite3.connect(const.peers_db_path)
    cur = con.cursor()
    cur.execute("CREATE TABLE peers (data text)")
    con.commit()
    con.close()
    return

def drop_table() -> None:
    con = sqlite3.connect(const.peers_db_path)
    cur = con.cursor()
    cur.execute("DROP TABLE peers")
    con.commit()
    con.close()
    return

def insert_table(table: Table) -> None:
    con = sqlite3.connect(const.peers_db_path)
    cur = con.cursor()
    cur.execute("INSERT INTO peers VALUES (?)", table.to_row())
    con.commit()
    con.close()
    return

def prune_table() -> None:
    con = sqlite3.connect(const.peers_db_path)
    cur = con.cursor()
    flag = True
    while flag:
        row_ids = cur.execute("SELECT rowid FROM peers").fetchall()
        if len(row_ids) > const.table_size_limit:
            cur.execute("DELETE FROM peers WHERE rowid=(?)", row_ids[0])
        else:
            flag = False
    con.commit()
    con.close()

def load_tables() -> list[Table]:
    con = sqlite3.connect(const.peers_db_path)
    cur = con.cursor()
    rows = cur.execute("SELECT * FROM peers").fetchall()
    con.commit()
    con.close()
    return [Table.from_row(row) for row in rows]

def get_table() -> Table:
    response = requests.post(
        url=const.url,
        json={"query": const.peers_query},
    )
    response = response.json()
    response = response["data"]["peerChainState"]["state"]
    return Table.from_dict(Table.raw_to_dict(response))

if __name__ == "__main__":
    if not os.path.exists(const.peers_db_path):
        create_db()
        create_table()

    while True:
        try:
            table = get_table()

            insert_table(table)
            prune_table()
        except Exception:
            pass

        time.sleep(const.sleep_time)
