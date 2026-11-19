"""Exo 5, suite : l'appli ne lit plus les CSV, elle demande à l'API. Fin à 16h05.

Lancez api.py d'abord : uv run uvicorn api:app --app-dir fil_rouge --host 127.0.0.1 --port 8000
Lancer : uv run streamlit run fil_rouge/app_api.py --server.address 127.0.0.1
"""

import os

import pandas as pd
import plotly.express as px
import requests
import streamlit as st

API = os.environ.get("AWP_API_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="Mes parties d'échecs", layout="wide")
st.title("Quelles ouvertures me coûtent des points\u00a0?")


def appeler(chemin: str, **params) -> pd.DataFrame:
    r = requests.get(f"{API}{chemin}", params=params, timeout=10)
    r.raise_for_status()  # une 422 ou une 500 devient une exception
    return pd.DataFrame(r.json())


with st.sidebar:
    cadence = st.selectbox("Cadence", ["blitz", "rapid", "bullet"], key="cadence")
    n_min = st.slider("Parties minimum par ouverture", 10, 60, 30, key="n_min")

try:
    ouvertures = appeler("/ouvertures", cadence=cadence, min_n=n_min)
    parties = appeler("/parties", cadence=cadence, limit=10)
except requests.RequestException as e:
    st.error(f"L'API ne répond pas sur {API}. Lancez uvicorn, puis rechargez la page.")
    st.caption(str(e))
    st.stop()

if ouvertures.empty:
    st.warning("Aucune famille n'a autant de parties.")
    st.stop()
fig = px.bar(ouvertures, x="score", y="famille", orientation="h", hover_data=["n"])
fig.update_yaxes(autorange="reversed")  # la pire en haut
st.plotly_chart(fig, key="familles")
st.subheader("Mes dix dernières parties")
st.dataframe(parties, hide_index=True)
