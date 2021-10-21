from __future__ import annotations
import datetime
import pandas as pd
import plotly.express as px
from model.block import Block
from model.table import Table

layout_template = dict(
    legend_x=0,
    legend_y=1,
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                    label="1h",
                    step="hour",
                    stepmode="backward"),
                dict(count=12,
                    label="12h",
                    step="hour",
                    stepmode="backward"),
                dict(count=1,
                    label="1d",
                    step="day",
                    stepmode="backward"),
                dict(count=7,
                    label="7d",
                    step="day",
                    stepmode="backward"),
                dict(step="all"),
            ])
        ),
        type="date"
    ),
    hovermode="x",
)

def get_node_lag_fig(tables: list[Table]):
    timestamps = [
        datetime.datetime.utcfromtimestamp(table.timestamp)
            for table in tables
    ]
    df = pd.DataFrame({
        "timestamp": timestamps,
        "lag": [table.lag for table in tables]
    })
    fig = px.line(
        df,
        x="timestamp",
        y="lag",
        title="Lag from best known height",
    )
    fig.update_layout(**layout_template)
    return fig

def get_peers_count_fig(tables: list[Table]):
    timestamps = [
        datetime.datetime.utcfromtimestamp(table.timestamp)
            for table in tables
    ]
    df = pd.DataFrame({
        "timestamp": timestamps,
        "all_peers": [len(table.remotes) for table in tables],
        "high_peers": [
            len([remote for remote in table.remotes
                if remote.tip >= table.local.tip])
                for table in tables
        ],
        "low_peers": [
            len([remote for remote in table.remotes
                if 0 <= remote.tip and remote.tip < table.local.tip])
                for table in tables
        ],
        "dead_peers": [
            len([remote for remote in table.remotes if remote.tip < 0])
                for table in tables
        ],
    })
    fig = px.line(
        df,
        x="timestamp",
        y=["all_peers", "high_peers", "low_peers", "dead_peers"],
        title="Number of peers",
    )
    fig.update_layout(**layout_template)
    return fig

def get_transactions_count_fig(blocks: list[Block]):
    timestamps = [
        datetime.datetime.utcfromtimestamp(block.timestamp)
            for block in blocks
    ]
    df = pd.DataFrame({
        "timestamp": timestamps,
        "transactions": [block.transactions for block in blocks]
    })
    df["rolling"] = df.transactions.rolling(100).mean()
    fig = px.line(
        df,
        x="timestamp",
        y=["transactions", "rolling"],
        title="Number of transactions",
    )
    fig.update_layout(**layout_template)
    return fig

def get_difficulty_fig(blocks: list[Block]):
    timestamps = [
        datetime.datetime.utcfromtimestamp(block.timestamp)
            for block in blocks
    ]
    df = pd.DataFrame({
        "timestamp": timestamps,
        "difficulty": [block.difficulty for block in blocks]
    })
    df["rolling"] = df.difficulty.rolling(100).mean()
    fig = px.line(
        df,
        x="timestamp",
        y=["difficulty", "rolling"],
        title="Difficulty",
    )
    fig.update_layout(**layout_template)
    return fig

def get_mining_time(blocks: list[Block]):
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
    df["rolling"] = df.mining_time.rolling(100).mean()
    fig = px.line(
        df,
        x="timestamps",
        y=["mining_time", "rolling"],
        title="Estimated mining time",
    )
    fig.update_layout(**layout_template)
    return fig

def get_mining_time_vs_transactions(blocks: list[Block]):
    mining_time = [
        current.timestamp - prev.timestamp
            for current, prev in zip(blocks[1:], blocks[:-1])
    ]
    transactions = [
        block.transactions for block in blocks[:-1]
    ]
    df = pd.DataFrame({
        "mining_time": mining_time,
        "transactions": transactions,
    })
    fig = px.scatter(
        df,
        x="transactions",
        y="mining_time",
        trendline="ols",
        trendline_color_override="red",
        title="Estimated mining time vs transactions",
    )
    return fig
