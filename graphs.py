from __future__ import annotations
import datetime
import pandas as pd
import plotly.express as px
import blocks_db_util
import routing_tables_db_util
import graph_util

def get_lag_figure(start_timestamp: float, end_timestamp: float):
    routing_tables = routing_tables_db_util.load_routing_tables(start_timestamp)
    timestamps = [
        datetime.datetime.utcfromtimestamp(table.timestamp)
            for table in routing_tables
    ]
    df = pd.DataFrame({
        "timestamp": timestamps,
        "lag": [table.lag for table in routing_tables]
    })
    fig = px.line(
        df,
        x="timestamp",
        y="lag",
        title="Height lag from best known height",
    )
    fig.update_layout(**graph_util.get_timeframe_layout(
        start_timestamp,
        end_timestamp
    ))
    return fig

def get_remotes_count_figure(start_timestamp: float, end_timestamp: float):
    routing_tables = routing_tables_db_util.load_routing_tables(start_timestamp)
    timestamps = [
        datetime.datetime.utcfromtimestamp(table.timestamp)
            for table in routing_tables
    ]
    df = pd.DataFrame({
        "timestamp": timestamps,
        "all_remotes": [len(table.remotes) for table in routing_tables],
        "high_remotes": [
            len([remote for remote in table.remotes
                if remote.tip >= table.local.tip])
                for table in routing_tables
        ],
        "low_remotes": [
            len([remote for remote in table.remotes
                if 0 <= remote.tip and remote.tip < table.local.tip])
                for table in routing_tables
        ],
        "dead_remotes": [
            len([remote for remote in table.remotes if remote.tip < 0])
                for table in routing_tables
        ],
    })
    fig = px.line(
        df,
        x="timestamp",
        y=["all_remotes", "high_remotes", "low_remotes", "dead_remotes"],
        title="Number of remote peers",
    )
    fig.update_layout(**graph_util.get_timeframe_layout(
        start_timestamp,
        end_timestamp
    ))
    return fig

def get_transactions_count_figure(start_timestamp: float, end_timestamp: float):
    blocks = blocks_db_util.load_blocks(start_timestamp)
    timestamps = [
        datetime.datetime.utcfromtimestamp(block.timestamp)
            for block in blocks
    ]
    df = pd.DataFrame({
        "timestamp": timestamps,
        "transactions_count": [len(block.transactions) for block in blocks]
    })
    rolling_interval = 50
    df[f"rolling_{rolling_interval}"] = (
        df["transactions_count"].rolling(rolling_interval).mean()
    )
    fig = px.line(
        df,
        x="timestamp",
        y=["transactions_count", f"rolling_{rolling_interval}"],
        title="Number of transactions",
    )
    fig.update_layout(**graph_util.get_timeframe_layout(
        start_timestamp,
        end_timestamp
    ))
    return fig

def get_difficulty_figure(start_timestamp: float, end_timestamp: float):
    blocks = blocks_db_util.load_blocks(start_timestamp)
    timestamps = [
        datetime.datetime.utcfromtimestamp(block.timestamp)
            for block in blocks
    ]
    df = pd.DataFrame({
        "timestamp": timestamps,
        "difficulty": [block.difficulty for block in blocks]
    })
    rolling_interval = 50
    df[f"rolling_{rolling_interval}"] = (
        df["difficulty"].rolling(rolling_interval).mean()
    )
    fig = px.line(
        df,
        x="timestamp",
        y=["difficulty", f"rolling_{rolling_interval}"],
        title="Difficulty",
    )
    fig.update_layout(**graph_util.get_timeframe_layout(
        start_timestamp,
        end_timestamp
    ))
    return fig

def get_mining_time_figure(start_timestamp: float, end_timestamp: float):
    blocks = blocks_db_util.load_blocks(start_timestamp)
    timestamps = [
        datetime.datetime.utcfromtimestamp(block.timestamp)
            for block in blocks[:-1]
    ]
    mining_time = [
        current.timestamp - prev.timestamp
            for current, prev in zip(blocks[1:], blocks[:-1])
    ]
    df = pd.DataFrame({
        "timestamps": timestamps,
        "mining_time": mining_time,
    })
    rolling_interval = 50
    df[f"rolling_{rolling_interval}"] = (
        df["mining_time"].rolling(rolling_interval).mean()
    )
    fig = px.line(
        df,
        x="timestamps",
        y=["mining_time", f"rolling_{rolling_interval}"],
        title="Estimated mining time",
    )
    fig.update_layout(**graph_util.get_timeframe_layout(
        start_timestamp,
        end_timestamp
    ))
    return fig

def get_mining_time_vs_transactions_count_figure(
    start_timestamp: float,
    end_timestamp: float,
):
    blocks = blocks_db_util.load_blocks(start_timestamp)
    mining_time = [
        current.timestamp - prev.timestamp
            for current, prev in zip(blocks[1:], blocks[:-1])
    ]
    df = pd.DataFrame({
        "mining_time": mining_time,
        "transactions_count": [
            len(block.transactions) for block in blocks[:-1]
        ],
    })
    fig = px.scatter(
        df,
        x="transactions_count",
        y="mining_time",
        trendline="ols",
        trendline_color_override="red",
        title="Estimated mining time vs transactions count",
    )
    return fig

def get_action_type_distribution_figure(
    start_timestamp: float,
    end_timestamp: float,
):
    blocks = blocks_db_util.load_blocks(start_timestamp)
    actions = [
        action
            for block in blocks
            for transaction in block.transactions
            for action in transaction.actions
    ]
    actions = [action if action else "undefined" for action in actions]
    actions = actions + [
        "null"
            for block in blocks
            for transaction in block.transactions
                if not transaction.actions
    ]
    series = pd.Series(actions).value_counts()
    df = pd.DataFrame({
        "action_type": series.index,
        "count": series.values
    })
    fig = px.pie(
        df,
        names="action_type",
        values="count",
        title="Action type distribution",
    )
    return fig
