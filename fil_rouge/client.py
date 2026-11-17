"""Appli Streamlit qui appelle le service FastAPI (lancer api.py d'abord)."""

import os

import requests
import streamlit as st

API = os.environ.get("API_URL", "http://localhost:8000")

st.title("Estimer le prix d'une station")

with st.form("simulation"):
    carburant = st.selectbox("Carburant", ["GAZOLE", "E10", "SP95", "SP98", "E85", "GPLC"])
    axe = st.radio("Axe", ["Route", "Autoroute"], horizontal=True)
    lat = st.number_input("Latitude", 47.5, 48.4, 47.90)
    lon = st.number_input("Longitude", 1.5, 3.1, 1.90)
    envoyer = st.form_submit_button("Estimer")

if envoyer:
    r = requests.post(
        f"{API}/predict",
        json={"carburant": carburant, "axe": axe, "lat": lat, "lon": lon},
        timeout=10,
    )
    r.raise_for_status()
    st.metric("Prix estimé", f"{r.json()['prix_estime']:.3f} €")
    st.caption("Modèle : gradient boosting, erreur moyenne de 0,042 €/L en validation croisée.")
