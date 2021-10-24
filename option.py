import datetime

timeframe_options = [
    {"label": "1 hour", "value": "1h"},
    {"label": "6 hours", "value": "6h"},
    {"label": "1 day", "value": "1d"},
    {"label": "1 week", "value": "1w"},
]
timeframe_value_to_timedelta = {
    "1h": datetime.timedelta(hours=1),
    "6h": datetime.timedelta(hours=6),
    "1d": datetime.timedelta(days=1),
    "1w": datetime.timedelta(days=7),
}
