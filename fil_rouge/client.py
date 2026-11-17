"""Exo 5 : une appli Streamlit « et si ? » qui appelle votre API. Fin à 16h15.

Question : et si je jouais plus tard, ou avec les noirs ?
À produire : un formulaire (couleur, cadence, écart d'Elo, heure), un requests.post vers /predict,
un st.metric, et un message lisible si l'API refuse la requête (422) ou ne répond pas.
Lancez api.py d'abord.
Lancer : uv run streamlit run fil_rouge/client.py --server.address 127.0.0.1
"""

import json
import os
from pathlib import Path

import requests
import streamlit as st

API = os.environ.get("AWP_API_URL", "http://127.0.0.1:8000")

st.title("Et si je jouais plus tard, ou avec les noirs ?")

with st.form("simulation"):
    couleur = st.radio("Couleur", ["white", "black"], horizontal=True)
    cadence = st.selectbox("Cadence", ["blitz", "bullet", "rapid"])
    ecart = st.number_input("Elo de l'adversaire moins le mien", -400, 400, 0)
    heure = st.slider("Heure de la partie (UTC)", 0, 23, 20)
    envoyer = st.form_submit_button("Estimer")

if envoyer:
    corps = {"couleur": couleur, "cadence": cadence, "ecart_elo": ecart, "heure": heure}
    r = requests.post(f"{API}/predict", json=corps, timeout=10)
    r.raise_for_status()
    st.metric("Chances de victoire", f"{r.json()['proba_victoire']:.0%}")
    mesures = Path(__file__).parent / "metriques.json"  # écrit par train.py
    if mesures.exists():
        m = json.loads(mesures.read_text())
        st.caption(
            f"Régression logistique, validation croisée : AUC {m['modele']['auc']:.2f} "
            f"(référence {m['reference']['auc']:.2f}), exactitude {m['modele']['exactitude']:.0%}."
        )
