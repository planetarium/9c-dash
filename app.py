from __future__ import annotations
import flask
import dash
if int(dash.__version__.split(".")[0]) < 2:
    import dash_core_components as dcc
    import dash_html_components as html
else:
    from dash import dcc
    from dash import html
import dash_bootstrap_components as dbc
import sqlite3
import const
import graphs
import blocks_db_util
import routing_tables_db_util
from model import Block, RoutingTable, Peer

server = flask.Flask(__name__)
app = dash.Dash(
    __name__,
    server=server,
    url_base_pathname="/app/",
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)

def serve_layout():
    routing_tables = routing_tables_db_util.load_routing_tables()
    blocks = blocks_db_util.load_blocks()
    return html.Div(
        dbc.Col(html.Div([
            html.H1(children='Nine Chronicles Dash'),
            html.Div(
                children=[
                    dcc.Graph(
                        id="lag",
                        figure=graphs.get_node_lag_fig(routing_tables),
                    ),
                    dcc.Graph(
                        id="count",
                        figure=graphs.get_peers_count_fig(routing_tables),
                    ),
                    dcc.Graph(
                        id="transactions",
                        figure=graphs.get_transactions_count_fig(blocks),
                    ),
                    dcc.Graph(
                        id="difficulty",
                        figure=graphs.get_difficulty_fig(blocks),
                    ),
                    dcc.Graph(
                        id="mining_time",
                        figure=graphs.get_mining_time(blocks),
                    ),
                    dcc.Graph(
                        id="mining_time_vs_transactions",
                        figure=graphs.get_mining_time_vs_transactions(blocks),
                    ),
                ]
            ),
        ]), width={"size": 8, "offset": 2}),
    )

app.layout = serve_layout

@server.route("/app/")
def index():
    return app.index()

if __name__ == '__main__':
    app.run_server(debug=True)
