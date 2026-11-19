"""Exo 4 : la même appli en Dash, avec un drill-down. Environ 25 min.

Question : quelles ouvertures coûtent des points, et dans quelles parties ?
À produire : un curseur (parties minimum) et le graphique des familles ; un clic sur une barre
liste les parties, un clic sur une partie liste les coups jugés mauvais, dans deux AG Grid.
Lancer : uv run python fil_rouge/app_dash.py   (http://127.0.0.1:8050)
"""

import os

import dash_ag_grid as dag
from dash import Dash, Input, Output, callback, dcc, html

from data import load_coups, load_data
from figures import fig_familles

df, coups = load_data(), load_coups()
TIP, ESPACE = {"always_visible": True}, {"marginBottom": 45}  # place du tooltip sous le titre
PARTIES = "partie_id date_jeu ouverture_nom couleur resultat elo_joueur elo_adverse"


def grille(id, champs):
    colonnes = [{"field": c} for c in champs.split()]
    options = {
        "rowSelection": {"mode": "singleRow", "enableClickSelection": True}
    }  # clic sur la ligne
    return dag.AgGrid(id=id, columnSize="sizeToFit", columnDefs=colonnes, dashGridOptions=options)


# AWP_MCP=1 expose les callbacks à un LLM sur /_mcp
app = Dash(__name__, title="Mes parties d'échecs", enable_mcp=os.environ.get("AWP_MCP") == "1")
server = app.server  # Dash tourne sur Flask

app.layout = html.Div(
    [
        html.H2("Quelles ouvertures me coûtent des points ? Cliquez une barre", style=ESPACE),
        dcc.Slider(30, 60, 10, value=30, id="n-min", marks=None, tooltip=TIP),
        dcc.Graph(id="familles"),
        grille("parties", PARTIES),
        html.H4("Mes coups jugés mauvais dans la partie choisie"),
        grille("coups", "numero_coup coup meilleur_coup jugement phase"),
    ],
    style={"maxWidth": 1100, "margin": "auto", "fontFamily": "Inter, sans-serif"},
)


@callback(Output("familles", "figure"), Input("n-min", "value"))
def familles(n_min):
    return fig_familles(df, n_min)


@callback(Output("parties", "rowData"), Input("familles", "clickData"))
def parties(click):
    if not click:
        return []
    vue = df[df["ouverture_famille"] == click["points"][0]["y"]]
    vue = vue.assign(date_jeu=vue["date_jeu"].dt.strftime("%Y-%m-%d %H:%M"))
    return vue[PARTIES.split()].to_dict("records")


@callback(Output("coups", "rowData"), Input("parties", "selectedRows"))
def detail(rows):
    if not rows:
        return []
    # astype(object) : fillna("") sur une colonne float lève un Pandas4Warning
    vue = coups[coups["partie_id"] == rows[0]["partie_id"]].astype(object)
    return vue.fillna("").to_dict("records")


if __name__ == "__main__":
    app.run(debug=False, port=8050)
