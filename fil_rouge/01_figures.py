"""Exo 1 : trois figures sur les prix des carburants."""

import plotly.express as px

from data import load_data

df = load_data()

med = df.groupby(["carburant", "axe"], as_index=False)["prix"].median()
px.bar(med, x="carburant", y="prix", color="axe", barmode="group",
       title="Prix médian par carburant, route et autoroute").show()  # fmt: skip

gazole = df[df["carburant"] == "GAZOLE"]
px.scatter_map(
    gazole, lat="lat", lon="lon", color="prix", hover_name="ville",
    color_continuous_scale="cividis", zoom=7.6,
    center={"lat": 47.92, "lon": 2.25},  # plotly 7 ne centre plus tout seul
).show()  # fmt: skip

px.histogram(gazole, x="prix", nbins=25, title="Répartition des prix du gazole").show()
