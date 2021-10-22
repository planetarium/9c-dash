from __future__ import annotations
import sqlite3
from const import table_size_limit as TABLE_SIZE_LIMIT
from const import routing_tables_db_path as DB_PATH
from model import RoutingTable

def create_db() -> None:
    con = sqlite3.connect(DB_PATH)
    con.commit()
    con.close()
    return

def create_tables() -> None:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("CREATE TABLE timestamps (timestamp REAL)")
    cur.execute("CREATE TABLE peers (timestamp REAL, address TEXT, tip INTEGER, difficulty INTEGER)")
    con.commit()
    con.close()
    return

def drop_tables() -> None:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("DROP TABLE timestamps")
    cur.execute("DROP TABLE peers")
    con.commit()
    con.close()
    return

def insert_routing_table(routing_table: RoutingTable) -> None:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    routing_table_dict = routing_table.to_dict()
    cur.execute(
        "INSERT INTO timestamps VALUES (?)",
        [routing_table_dict["timestamp"]],
    )
    for peer_dict in routing_table_dict["peers"]:
        cur.execute(
            "INSERT INTO peers VALUES (?, ?, ?, ?)",
            [
                routing_table.timestamp,
                peer_dict["address"],
                peer_dict["tip"],
                peer_dict["difficulty"],
            ]
        )
    con.commit()
    con.close()
    return

def prune_tables() -> None:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    timestamps = [
        row[0] for row
            in cur.execute("SELECT timestamp FROM timestamps").fetchall()
    ]
    con.commit()
    con.close()
    while len(timestamps) > TABLE_SIZE_LIMIT:
        delete_routing_table(timestamps.pop(0))
    return

def load_routing_tables() -> list[RoutingTable]:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    timestamps = [
        row[0] for row
            in cur.execute("SELECT timestamp FROM timestamps").fetchall()
    ]
    con.commit()
    con.close()
    return [load_routing_table(timestamp) for timestamp in timestamps]

def load_routing_table(timestamp: float) -> RoutingTable:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    if cur.execute(
        "SELECT EXISTS(SELECT timestamp FROM timestamps WHERE timestamp=(?))",
        [timestamp]
    ).fetchone()[0]:
        routing_table = RoutingTable.from_dict({
            "timestamp": timestamp,
            "peers": [{
                "address": row[1],
                "tip": row[2],
                "difficulty": row[3],
            } for row in cur.execute(
                "SELECT * FROM peers WHERE timestamp=(?)",
                [timestamp],
            ).fetchall()]
        })
        con.commit()
        con.close()
        return routing_table
    else:
        con.commit()
        con.close()
        raise KeyError(f"Given timestamp {timestamp} not found in database.")

def delete_routing_table(timestamp: float) -> None:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    if cur.execute(
        "SELECT EXISTS(SELECT timestamp FROM timestamps WHERE timestamp=(?))",
        [timestamp]
    ).fetchone()[0]:
        cur.execute(
            "DELETE FROM timestamps WHERE timestamp=(?)",
            [timestamp],
        )
        cur.execute(
            "DELETE FROM peers WHERE timestamp=(?)",
            [timestamp],
        )
        con.commit()
        con.close()
        return
    else:
        con.commit()
        con.close()
        raise KeyError(f"Given timestamp {timestamp} not found in database.")
