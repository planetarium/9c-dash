from __future__ import annotations
import os
import pathlib
import sqlite3
import json
from const import table_size_limit as TABLE_SIZE_LIMIT
from const import routing_tables_db_path as DB_PATH
from model import RoutingTable

DB_PATH = os.path.join(pathlib.Path(__file__).parent.absolute(), DB_PATH)

def create_db() -> None:
    con = sqlite3.connect(DB_PATH)
    con.commit()
    con.close()
    return

def create_tables() -> None:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("CREATE TABLE routing_tables (timestamp REAL, routing_table TEXT)")
    con.commit()
    con.close()
    return

def drop_tables() -> None:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("DROP TABLE routing_tables")
    con.commit()
    con.close()
    return

def insert_routing_table(routing_table: RoutingTable) -> None:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute(
        "INSERT INTO routing_tables VALUES (?, ?)",
        [routing_table.timestamp, json.dumps(routing_table.to_dict())]
    )
    con.commit()
    con.close()
    return

def insert_routing_tables(routing_tables: list[RoutingTable]) -> None:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.executemany(
        "INSERT INTO routing_tables VALUES (?, ?)",
        [[routing_table.timestamp, json.dumps(routing_table.to_dict())]
            for routing_table in routing_tables]
    )
    con.commit()
    con.close()
    return

def prune_tables() -> None:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    timestamps = [
        row[0] for row
            in cur.execute("SELECT timestamp FROM routing_tables").fetchall()
    ]
    con.commit()
    con.close()
    while len(timestamps) > TABLE_SIZE_LIMIT:
        timestamps.pop(0)
    delete_routing_tables(timestamps[0])
    return

def load_routing_table(timestamp: float) -> RoutingTable:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    if cur.execute(
        "SELECT EXISTS(SELECT timestamp FROM routing_tables WHERE timestamp = (?))",
        [timestamp],
    ).fetchone()[0]:
        routing_table = RoutingTable.from_dict(json.loads(cur.execute(
            "SELECT routing_table FROM routing_tables WHERE timestamp = (?)",
            [timestamp],
        ).fetchone()[0]))
        con.commit()
        con.close()
        return routing_table
    else:
        con.commit()
        con.close()
        raise KeyError(f"Given timestamp {timestamp} not found in database.")

def load_routing_tables(timestamp: float=0.0) -> list[RoutingTable]:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    rows = cur.execute(
        "SELECT routing_table FROM routing_tables WHERE timestamp >= (?)",
        [timestamp],
    ).fetchall()
    con.commit()
    con.close()
    return [
        RoutingTable.from_dict(json.loads(row[0])) for row in rows
    ]

def delete_routing_table(timestamp: float) -> None:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    if cur.execute(
        "SELECT EXISTS(SELECT timestamp FROM routing_tables WHERE timestamp = (?))",
        [timestamp]
    ).fetchone()[0]:
        cur.execute(
            "DELETE FROM routing_tables WHERE timestamp = (?)",
            [timestamp],
        )
        con.commit()
        con.close()
        return
    else:
        con.commit()
        con.close()
        raise KeyError(f"Given timestamp {timestamp} not found in database.")

def delete_routing_tables(timestamp: float) -> None:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute(
        "DELETE FROM routing_tables WHERE timestamp < (?)",
        [timestamp],
    )
    con.commit()
    con.close()
    return
