#!/usr/bin/python3

from __future__ import annotations
import os
import time
import requests
import sqlite3
import const
from model.block import Block

def create_db() -> None:
    con = sqlite3.connect(const.chain_db_path)
    con.commit()
    con.close()
    return

def create_table() -> None:
    con = sqlite3.connect(const.chain_db_path)
    cur = con.cursor()
    cur.execute("CREATE TABLE chain (timestamp REAL, index_ INTEGER, hash_ TEXT, prev TEXT, difficulty INTEGER, transactions INTEGER, miner TEXT)")
    con.commit()
    con.close()
    return

def drop_table() -> None:
    con = sqlite3.connect(const.chain_db_path)
    cur = con.cursor()
    cur.execute("DROP TABLE chain")
    con.commit()
    con.close()
    return

def insert_block(block: Block) -> None:
    con = sqlite3.connect(const.chain_db_path)
    cur = con.cursor()
    cur.execute("INSERT INTO chain VALUES (?, ?, ?, ?, ?, ?, ?)", block.to_row())
    con.commit()
    con.close()
    return

def delete_block(block: Block) -> None:
    con = sqlite3.connect(const.chain_db_path)
    cur = con.cursor()
    cur.execute("DELETE FROM chain WHERE hash_=(?)", block.hash_)
    con.commit()
    con.close()
    return

def prune_blocks() -> None:
    con = sqlite3.connect(const.chain_db_path)
    cur = con.cursor()
    overflow = True
    while overflow:
        row_ids = cur.execute("SELECT rowid FROM chain").fetchall()
        if len(row_ids) > const.table_size_limit:
            cur.execute("DELETE FROM chain WHERE rowid=(?)", row_ids[0])
        else:
            overflow = False
    con.commit()
    con.close()
    return

def load_blocks() -> list[Block]:
    con = sqlite3.connect(const.chain_db_path)
    cur = con.cursor()
    rows = cur.execute("SELECT * FROM chain").fetchall()
    con.commit()
    con.close()
    return [Block.from_row(row) for row in rows]

def get_blocks(limit: int) -> list[Block]:
    response = requests.post(
        url=const.url,
        json={"query": const.chain_query.replace("<limit>", f"{limit}")}
    )
    response = response.json()
    response = response["data"]["chainQuery"]["blockQuery"]["blocks"]
    return [Block.from_dict(Block.raw_to_dict(raw)) for raw in response][::-1]

def find_branching_block(
    old_blocks: list[Block],
    new_blocks: list[Block],
) -> Block:
    new_hashes = [block.hash_ for block in new_blocks]
    for old_block in reversed(old_blocks):
        if old_block.hash_ in new_hashes:
            return old_block
    return None

if __name__ == "__main__":
    if not os.path.exists(const.chain_db_path):
        create_db()
        create_table()

    limits = [16, 64, 256, 1024]
    while True:
        try:
            old_blocks = load_blocks()

            if not old_blocks:
                new_blocks = get_blocks(limits[-1])
                for block in new_blocks:
                    insert_block(block)
            else:
                for limit in limits:
                    new_blocks = get_blocks(limit)
                    branching_block = find_branching_block(old_blocks, new_blocks)
                    if branching_block:
                        break
                if branching_block:
                    blocks_to_delete = [
                        block for block in old_blocks
                            if block.index_ > branching_block.index_
                    ]
                    blocks_to_insert = [
                        block for block in new_blocks
                            if block.index_ > branching_block.index_
                    ]
                    for block in blocks_to_delete:
                        delete_block(block)
                    for block in blocks_to_insert:
                        insert_block(block)
                # something went horribly wrong
                # start from scratch
                else:
                    drop_table()
                    create_table()

            prune_blocks()
        except Exception:
            pass

        time.sleep(const.sleep_time)
