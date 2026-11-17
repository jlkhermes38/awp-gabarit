"""Exo 2 : l'appli Streamlit du fil rouge. Fin à 12h30.

Question : l'appli que ce joueur ouvrirait chaque semaine pour savoir quoi travailler.
À produire : une barre latérale (cadence, période, couleur), trois st.metric, deux figures
en colonnes. Le titre de la page dit la question, pas « Dashboard ».
Lancer : uv run streamlit run fil_rouge/app_streamlit.py --server.address 127.0.0.1
"""

import streamlit as st

from data import load_coups, load_data
from figures import fig_familles, fig_phases, pct

st.set_page_config(page_title="Mes parties d'échecs", layout="wide")
COULEURS = {"toutes": None, "blancs": "white", "noirs": "black"}


@st.cache_data
def donnees():
    return load_data(), load_coups()


df, coups = donnees()
st.title("Je stagne aux échecs : qu'est-ce que je dois travailler ?")

with st.sidebar:
    cadences = st.multiselect("Cadence", sorted(df["cadence"].unique()), ["blitz"], key="cadence")
    d0, d1 = df["date_jeu"].min().date(), df["date_jeu"].max().date()
    periode = st.date_input("Période", (d0, d1), min_value=d0, max_value=d1, key="periode")
    couleur = st.radio("Couleur", list(COULEURS), horizontal=True, key="couleur")
    n_min = st.slider("Parties minimum par ouverture", 30, 60, 30, key="n_min")

if len(periode) != 2:  # l'utilisateur n'a choisi que la première date
    st.stop()
vue = df[df["cadence"].isin(cadences) & df["date_jeu"].dt.date.between(*periode)]
if COULEURS[couleur]:
    vue = vue[vue["couleur"] == COULEURS[couleur]]
if vue.empty:
    st.warning("Aucune partie avec ces filtres.")
    st.stop()

c1, c2, c3 = st.columns(3)
c1.metric("Parties", len(vue))
c2.metric("Score", pct(vue["score"].mean()))
c3.metric("Gaffes par partie", f"{vue['gaffes_joueur'].mean():.2f}")

gauche, droite = st.columns(2)
gauche.plotly_chart(fig_familles(vue, n_min), key="familles")
droite.plotly_chart(fig_phases(coups[coups["partie_id"].isin(vue["partie_id"])]), key="phases")
