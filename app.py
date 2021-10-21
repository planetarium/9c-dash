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
from model.table import Table
from model.block import Block

server = flask.Flask(__name__)
app = dash.Dash(
    __name__,
    server=server,
    url_base_pathname="/app/",
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)

def load_tables() -> list[Table]:
    con = sqlite3.connect(const.peers_db_path)
    cur = con.cursor()
    rows = cur.execute("SELECT * FROM peers").fetchall()
    con.commit()
    con.close()
    return [Table.from_row(row) for row in rows]

def load_blocks() -> list[Block]:
    con = sqlite3.connect(const.chain_db_path)
    cur = con.cursor()
    rows = cur.execute("SELECT * FROM chain").fetchall()
    con.commit()
    con.close()
    return [Block.from_row(row) for row in rows]

def serve_layout():
    tables = load_tables()
    blocks = load_blocks()
    return html.Div(children=[
        html.H1(children='Nine Chronicles Dash'),

        html.Div(children=[
            dcc.Graph(
                id="lag",
                figure=graphs.get_node_lag_fig(tables),
            ),
            dcc.Graph(
                id="count",
                figure=graphs.get_peers_count_fig(tables),
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
        ]),
    ])

app.layout = serve_layout

@server.route("/app/")
def index():
    return app.index()

if __name__ == '__main__':
    app.run_server(debug=True)

