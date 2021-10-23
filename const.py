url = "https://9c-main-full-state.planetarium.dev/graphql"

routing_tables_db_path = "routing_tables.db"
routing_table_query = """
query {
    peerChainState {
        state
    }
}
"""

blocks_db_path = "blocks.db"
blocks_query = """
query {
    chainQuery {
        blockQuery {
            blocks (
                desc: true,
                limit: <limit>,
                excludeEmptyTxs: false
            ) {
                timestamp
                index
                difficulty
                hash
                previousBlock {
                    hash
                }
                transactions {
                    id
                    actions {
                        inspection
                    }
                }
                miner
            }
        }
    }
}
"""

sleep_time = 4
table_size_limit = 65_536
