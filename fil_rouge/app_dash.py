import dash_ag_grid as dag
import plotly.express as px
from dash import Dash, Input, Output, callback, dcc, html

from data import load_data

df = load_data()

app = Dash(__name__, title="Carburants Loiret")
server = app.server  # Dash tourne sur Flask

app.layout = html.Div(
    [
        html.H2("Prix par commune : cliquez une barre"),
        dcc.Dropdown(sorted(df["carburant"].unique()), "E10", id="carburant", clearable=False),
        dcc.Graph(id="communes"),
        html.H4(id="titre-detail"),
        dag.AgGrid(
            id="stations",
            columnSize="sizeToFit",
            columnDefs=[{"field": c} for c in ["ville", "adresse", "axe", "prix"]],
        ),
    ],
    style={"maxWidth": 1000, "margin": "auto", "fontFamily": "Inter, sans-serif"},
)


@callback(Output("communes", "figure"), Input("carburant", "value"))
def communes(carburant):
    vue = df[df["carburant"] == carburant]
    top = vue.groupby("ville", as_index=False)["prix"].median().nsmallest(15, "prix")
    fig = px.bar(top, x="ville", y="prix", color_discrete_sequence=["#0072B2"])
    return fig.update_yaxes(range=[top["prix"].min() - 0.05, top["prix"].max() + 0.02])


@callback(
    Output("stations", "rowData"),
    Output("titre-detail", "children"),
    Input("communes", "clickData"),
    Input("carburant", "value"),
)
def detail(click, carburant):
    if not click:
        return [], "Aucune commune sélectionnée"
    ville = click["points"][0]["x"]
    vue = df[(df["carburant"] == carburant) & (df["ville"] == ville)]
    return vue.to_dict("records"), f"Stations à {ville}"


if __name__ == "__main__":
    app.run(debug=False, port=8050)
