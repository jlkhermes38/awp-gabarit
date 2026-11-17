import plotly.express as px
import streamlit as st

from data import load_data

st.set_page_config(page_title="Carburants Loiret", layout="wide")


@st.cache_data(ttl=600)
def get_data():
    return load_data()


df = get_data()

st.title("Où faire le plein dans le Loiret ?")

with st.sidebar:
    options = sorted(df["carburant"].unique())
    carburant = st.selectbox("Carburant", options, index=options.index("GAZOLE"), key="carburant")
    villes = st.multiselect("Communes", sorted(df["ville"].unique()), key="communes")

vue = df[df["carburant"] == carburant]
if villes:
    vue = vue[vue["ville"].isin(villes)]

c1, c2, c3 = st.columns(3)
c1.metric("Prix médian", f"{vue['prix'].median():.3f} €")
c2.metric("Le moins cher", f"{vue['prix'].min():.3f} €")
c3.metric("Stations", len(vue))

gauche, droite = st.columns([3, 2])
with gauche:
    fig = px.scatter_map(
        vue,
        lat="lat",
        lon="lon",
        color="prix",
        hover_name="ville",
        color_continuous_scale="cividis",
        height=430,
        zoom=7.6,
        center={"lat": 47.92, "lon": 2.25},  # plotly 7 ne centre plus tout seul
    )
    st.plotly_chart(fig)
with droite:
    st.plotly_chart(px.histogram(vue, x="prix", nbins=20, height=430, title="Répartition des prix"))
