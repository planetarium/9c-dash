#!/usr/bin/python3

from __future__ import annotations
import os
import pathlib
import time
import requests
import const
import blocks_db_util
from model import Block

DB_PATH = os.path.join(
    pathlib.Path(__file__).parent.absolute(),
    const.blocks_db_path,
)

def get_blocks(limit: int) -> list[Block]:
    response = requests.post(
        url=const.url,
        json={"query": const.blocks_query.replace("<limit>", f"{limit}")}
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
    if not os.path.exists(DB_PATH):
        blocks_db_util.create_db()
        blocks_db_util.create_tables()

    limits = [16, 64, 256, 1024]
    while True:
        try:
            old_blocks = blocks_db_util.load_blocks()
            if not old_blocks:
                new_blocks = get_blocks(limits[-1])
                blocks_db_util.insert_blocks(new_blocks)
            else:
                for limit in limits:
                    new_blocks = get_blocks(limit)
                    branching_block = find_branching_block(
                        old_blocks,
                        new_blocks,
                    )
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
                        blocks_db_util.delete_block(block.timestamp)
                    blocks_db_util.insert_blocks(blocks_to_insert)
                # something went horribly wrong
                # start from scratch
                else:
                    blocks_db_util.drop_tables()
                    blocks_db_util.create_tables()
            blocks_db_util.prune_tables()
        except Exception as e:
            print(e)
            pass

        time.sleep(const.sleep_time)
