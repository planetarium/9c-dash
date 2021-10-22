from __future__ import annotations
import sqlite3
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
    cur.execute("CREATE TABLE hashes (hash_ TEXT)")
    cur.execute("CREATE TABLE blocks (hash_ TEXT, timestamp REAL, index_ INTEGER, prev TEXT, difficulty INTEGER, miner TEXT)")
    cur.execute("CREATE TABLE transactions (hash_ TEXT, id_ TEXT)")
    cur.execute("CREATE TABLE actions (id_ TEXT, action TEXT)")
    con.commit()
    con.close()
    return

def drop_tables() -> None:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("DROP TABLE hashes")
    cur.execute("DROP TABLE blocks")
    cur.execute("DROP TABLE transactions")
    cur.execute("DROP TABLE actions")
    con.commit()
    con.close()
    return

def insert_block(block: Block) -> None:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("INSERT INTO hashes VALUES (?)", [block.hash_])
    cur.execute(
        "INSERT INTO blocks VALUES (?, ?, ?, ?, ?, ?)",
        [block.hash_, block.timestamp, block.index_, block.prev, block.difficulty, block.miner],
    )
    for transaction in block.transactions:
        cur.execute(
            "INSERT INTO transactions VALUES (?, ?)",
            [block.hash_, transaction.id_]
        )
        for action in transaction.actions:
            cur.execute(
                "INSERT INTO actions VALUES (?, ?)",
                [transaction.id_, action]
            )
    con.commit()
    con.close()
    return

def prune_blocks() -> None:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    hashes = [
        row[0] for row
            in cur.execute("SELECT hash_ FROM hashes").fetchall()
    ]
    con.commit()
    con.close()
    while len(hashes) > TABLE_SIZE_LIMIT:
        delete_block(hashes.pop(0))
    return

def load_block(hash_: str) -> Block:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    if cur.execute(
        "SELECT EXISTS(SELECT hash_ FROM hashes WHERE hash_=(?))",
        [hash_]
    ).fetchone()[0]:
        row = cur.execute(
            "SELECT * FROM blocks WHERE hash_=(?)",
            [hash_],
        ).fetchone()
        block = Block.from_dict({
            "hash_": row[0],
            "timestamp": row[1],
            "index_": row[2],
            "prev": row[3],
            "difficulty": row[4],
            "miner": row[5],
            "transactions": [{
                "id_": transaction_row[1],
                "actions": [
                    action_row[1] for action_row
                        in cur.execute(
                            "SELECT * FROM actions WHERE id_=(?)",
                            [transaction_row[1]],
                        ).fetchall()
                ]
            } for transaction_row in cur.execute(
                "SELECT * FROM transactions WHERE hash_=(?)",
                [hash_],
            ).fetchall()]
        })
        con.commit()
        con.close()
        return block
    else:
        con.commit()
        con.close()
        raise KeyError(f"Given hash {hash_} not found in database.")

def load_blocks() -> list[Block]:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    hashes = [row[0] for row in cur.execute("SELECT hash_ FROM hashes").fetchall()]
    con.commit()
    con.close()
    return [load_block(hash_) for hash_ in hashes]

def delete_block(hash_: str) -> None:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    if cur.execute(
        "SELECT EXISTS(SELECT hash_ FROM hashes WHERE hash_=(?))",
        [hash_]
    ).fetchone()[0]:
        cur.execute("DELETE FROM hashes WHERE hash_=(?)", [hash_])
        cur.execute("DELETE FROM blocks WHERE hash_=(?)", [hash_])
        ids = [
            row[0] for row
                in cur.execute(
                    "SELECT id_ FROM transactions WHERE hash_=(?)",
                    [hash_],
                ).fetchall()
        ]
        cur.execute("DELETE FROM transactions WHERE hash_=(?)", [hash_])
        for id_ in ids:
            cur.execute("DELETE FROM actions WHERE action=(?)", id_)
        con.commit()
        con.close()
        return
    else:
        con.commit()
        con.close()
        raise KeyError(f"Given hash {hash_} not found in database.")
