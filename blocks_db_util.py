from __future__ import annotations
import sqlite3
import json
from const import table_size_limit as TABLE_SIZE_LIMIT
from const import blocks_db_path as DB_PATH
from model.block import Block

def create_db() -> None:
    con = sqlite3.connect(DB_PATH)
    con.commit()
    con.close()
    return

def create_tables() -> None:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("CREATE TABLE blocks (timestamp REAL, block TEXT)")
    con.commit()
    con.close()
    return

def drop_tables() -> None:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("DROP TABLE blocks")
    con.commit()
    con.close()
    return

def insert_block(block: Block) -> None:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute(
        "INSERT INTO blocks VALUES (?, ?)",
        [block.timestamp, json.dumps(block.to_dict())],
    )
    con.commit()
    con.close()
    return

def insert_blocks(blocks: list[Block]) -> None:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.executemany(
        "INSERT INTO blocks VALUES (?, ?)",
        [[block.timestamp, json.dumps(block.to_dict())] for block in blocks],
    )
    con.commit()
    con.close()
    return

def prune_tables() -> None:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    timestamps = [
        row[0] for row
            in cur.execute("SELECT timestamp FROM blocks").fetchall()
    ]
    con.commit()
    con.close()
    while len(timestamps) > TABLE_SIZE_LIMIT:
        timestamps.pop(0)
    delete_blocks(timestamps[0])
    return

def load_block(timestamp: float) -> Block:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    if cur.execute(
        "SELECT EXISTS(SELECT timestamp FROM blocks WHERE timestamp = (?))",
        [timestamp],
    ).fetchone()[0]:
        block = Block.from_dict(json.loads(cur.execute(
            "SELECT block FROM blocks WHERE timestamp = (?)",
            [timestamp],
        ).fetchone()[0]))
        con.commit()
        con.close()
        return block
    else:
        con.commit()
        con.close()
        raise KeyError(f"Given timestamp {timestamp} not found in database.")

def load_blocks(timestamp: float=0.0) -> list[Block]:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    rows = cur.execute(
        "SELECT block FROM blocks WHERE timestamp >= (?)",
        [timestamp],
    ).fetchall()
    con.commit()
    con.close()
    return [Block.from_dict(json.loads(row[0])) for row in rows]

def delete_block(timestamp: float) -> None:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    if cur.execute(
        "SELECT EXISTS(SELECT timestamp FROM blocks WHERE timestamp = (?))",
        [timestamp],
    ).fetchone()[0]:
        cur.execute(
            "DELETE FROM blocks WHERE timestamp = (?)",
            [timestamp],
        )
        con.commit()
        con.close()
        return
    else:
        con.commit()
        con.close()
        raise KeyError(f"Given timestamp {timestamp} not found in database.")

def delete_blocks(timestamp: float) -> None:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute(
        "DELETE FROM blocks WHERE timestamp < (?)",
        [timestamp],
    )
    con.commit()
    con.close()
    return
