from __future__ import annotations
import datetime
import flask
import dash
if int(dash.__version__.split(".")[0]) < 2:
    import dash_core_components as dcc
    import dash_html_components as html
else:
    from dash import dcc
    from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import graphs
import option

def serve_layout():
    return html.Div(
        dbc.Col(html.Div([
            html.H1(children='Nine Chronicles Dash'),
            html.Div(
                children=[
                    html.Div(
                        children=[
                            dcc.Graph(
                                id="lag_figure"
                            ),
                            dcc.Dropdown(
                                id="lag_figure_timeframe",
                                options=option.timeframe_options,
                                value="1h",
                                clearable=False,
                            ),
                        ],
                    ),
                    html.Hr(),
                    html.Div(
                        children=[
                            dcc.Graph(
                                id="remotes_count_figure",
                            ),
                            dcc.Dropdown(
                                id="remotes_count_figure_timeframe",
                                options=option.timeframe_options,
                                value="1h",
                                clearable=False,
                            ),
                        ],
                    ),
                    html.Hr(),
                    html.Div(
                        children=[
                            dcc.Graph(
                                id="transactions_count_figure",
                            ),
                            dcc.Dropdown(
                                id="transactions_count_figure_timeframe",
                                options=option.timeframe_options,
                                value="1h",
                                clearable=False,
                            ),
                        ],
                    ),
                    html.Hr(),
                    html.Div(
                        children=[
                            dcc.Graph(
                                id="difficulty_figure",
                            ),
                            dcc.Dropdown(
                                id="difficulty_figure_timeframe",
                                options=option.timeframe_options,
                                value="1h",
                                clearable=False,
                            ),
                        ],
                    ),
                    html.Hr(),
                    html.Div(
                        children=[
                            dcc.Graph(
                                id="mining_time_figure",
                            ),
                            dcc.Dropdown(
                                id="mining_time_figure_timeframe",
                                options=option.timeframe_options,
                                value="1h",
                                clearable=False,
                            ),
                        ],
                    ),
                    html.Hr(),
                    html.Div(
                        children=[
                            dcc.Graph(
                                id="mining_time_vs_transactions_count_figure",
                            ),
                            dcc.Dropdown(
                                id="mining_time_vs_transactions_count_figure_timeframe",
                                options=option.timeframe_options,
                                value="1h",
                                clearable=False,
                            ),
                        ],
                    ),
                    html.Hr(),
                    html.Div(
                        children=[
                            dcc.Graph(
                                id="action_type_distribution_figure",
                            ),
                            dcc.Dropdown(
                                id="action_type_distribution_figure_timeframe",
                                options=option.timeframe_options,
                                value="1h",
                                clearable=False,
                            ),
                        ],
                    ),
                ],
            ),
        ]), width={"size": 8, "offset": 2}),
    )

server = flask.Flask(__name__)
app = dash.Dash(
    __name__,
    server=server,
    url_base_pathname="/app/",
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)
app.layout = serve_layout

@app.callback(
    Output("lag_figure", "figure"),
    Input("lag_figure_timeframe", "value"),
)
def update_lag_figure(timeframe_value: str):
    now = datetime.datetime.now()
    delta = option.timeframe_value_to_timedelta[timeframe_value]
    start_timestamp = (now - delta).timestamp()
    end_timestamp = now.timestamp()
    return graphs.get_lag_figure(start_timestamp, end_timestamp)

@app.callback(
    Output("remotes_count_figure", "figure"),
    Input("remotes_count_figure_timeframe", "value"),
)
def update_remotes_count_figure(timeframe_value: str):
    now = datetime.datetime.now()
    delta = option.timeframe_value_to_timedelta[timeframe_value]
    start_timestamp = (now - delta).timestamp()
    end_timestamp = now.timestamp()
    return graphs.get_remotes_count_figure(start_timestamp, end_timestamp)

@app.callback(
    Output("transactions_count_figure", "figure"),
    Input("transactions_count_figure_timeframe", "value"),
)
def update_transactions_count_figure(timeframe_value: str):
    now = datetime.datetime.now()
    delta = option.timeframe_value_to_timedelta[timeframe_value]
    start_timestamp = (now - delta).timestamp()
    end_timestamp = now.timestamp()
    return graphs.get_transactions_count_figure(start_timestamp, end_timestamp)

@app.callback(
    Output("difficulty_figure", "figure"),
    Input("difficulty_figure_timeframe", "value"),
)
def update_difficulty_figure(timeframe_value: str):
    now = datetime.datetime.now()
    delta = option.timeframe_value_to_timedelta[timeframe_value]
    start_timestamp = (now - delta).timestamp()
    end_timestamp = now.timestamp()
    return graphs.get_difficulty_figure(start_timestamp, end_timestamp)

@app.callback(
    Output("mining_time_figure", "figure"),
    Input("mining_time_figure_timeframe", "value"),
)
def update_mining_time_figure(timeframe_value: str):
    now = datetime.datetime.now()
    delta = option.timeframe_value_to_timedelta[timeframe_value]
    start_timestamp = (now - delta).timestamp()
    end_timestamp = now.timestamp()
    return graphs.get_mining_time_figure(start_timestamp, end_timestamp)

@app.callback(
    Output("mining_time_vs_transactions_count_figure", "figure"),
    Input("mining_time_vs_transactions_count_figure_timeframe", "value"),
)
def update_mining_time_vs_transactions_count_figure(timeframe_value: str):
    now = datetime.datetime.now()
    delta = option.timeframe_value_to_timedelta[timeframe_value]
    start_timestamp = (now - delta).timestamp()
    end_timestamp = now.timestamp()
    return graphs.get_mining_time_vs_transactions_count_figure(
        start_timestamp,
        end_timestamp,
    )

@app.callback(
    Output("action_type_distribution_figure", "figure"),
    Input("action_type_distribution_figure_timeframe", "value"),
)
def update_action_type_distribution_figure(timeframe_value: str):
    now = datetime.datetime.now()
    delta = option.timeframe_value_to_timedelta[timeframe_value]
    start_timestamp = (now - delta).timestamp()
    end_timestamp = now.timestamp()
    return graphs.get_action_type_distribution_figure(
        start_timestamp,
        end_timestamp,
    )

@server.route("/app/")
def index():
    return app.index()

if __name__ == '__main__':
    app.run_server(debug=True)
