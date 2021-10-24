from __future__ import annotations
import datetime

def get_timeframe_layout(start_timestamp: float, end_timestamp: float) -> dict:
    return dict(
        legend_x=0,
        legend_y=1,
        xaxis=dict(
            range=list([
                datetime.datetime.utcfromtimestamp(start_timestamp),
                datetime.datetime.utcfromtimestamp(end_timestamp),
            ]),
            type="date",
        ),
        hovermode="x",
    )
