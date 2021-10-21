url = "https://9c-main-full-state.planetarium.dev/graphql"

peers_db_path = "peers.db"
peers_query = """
query {
    peerChainState {
        state
    }
}
"""

chain_db_path = "chain.db"
chain_query = """
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
                }
                miner
            }
        }
    }
}
"""

sleep_time = 4
table_size_limit = 65_536
