"""Exo 5 : le service FastAPI. Fin à 16h15.

Question : mes parties derrière une API que n'importe quel client peut appeler (votre appli, puis l'agent de l'exo 6).
À produire : GET /ouvertures et GET /parties, paramètres validés (une cadence inconnue renvoie 422, pas une liste vide).
Ensuite : app_api.py, ou votre appli de l'exo 2 ou de l'exo 4, appelle cette API au lieu de lire les CSV.
Bonus : POST /predict avec le modèle fourni (fil_rouge/model.joblib, déjà entraîné), puis client.py.
Lancer : uv run uvicorn api:app --app-dir fil_rouge --host 127.0.0.1 --port 8000 --reload
Documentation interactive : http://127.0.0.1:8000/docs
"""

from pathlib import Path
from typing import Literal

import joblib
import pandas as pd
from fastapi import FastAPI, Query
from pydantic import BaseModel, Field, StrictInt

from data import familles, load_data

app = FastAPI(title="Mes parties d'échecs", version="1.0")
model = joblib.load(Path(__file__).parent / "model.joblib")
df = load_data()  # modèle et données chargés une fois, au démarrage


Cadence = Literal["bullet", "blitz", "rapid"]  # une autre valeur : 422, pas une liste vide


@app.get("/parties")
def parties(
    cadence: Cadence | None = None,
    couleur: Literal["white", "black"] | None = None,
    limit: int = Query(20, ge=1, le=500),
):
    vue = df
    if cadence:
        vue = vue[vue["cadence"] == cadence]
    if couleur:
        vue = vue[vue["couleur"] == couleur]
    cols = ["partie_id", "date_jeu", "cadence", "couleur", "resultat", "ouverture_famille"]
    return vue.tail(limit)[cols].fillna("").astype(str).to_dict("records")


@app.get("/ouvertures")
def ouvertures(cadence: Cadence | None = None, min_n: int = Query(30, ge=1)):
    vue = df if cadence is None else df[df["cadence"] == cadence]
    return familles(vue, min_n).to_dict("records")


class Partie(BaseModel):
    couleur: Literal["white", "black"]
    cadence: Literal["bullet", "blitz", "rapid"]
    ecart_elo: int = Field(ge=-800, le=800)  # Elo de l'adversaire moins le mien
    heure: StrictInt = Field(ge=0, le=23)  # heure UTC, entier (pas true)


@app.post("/predict")
def predict(partie: Partie) -> dict:
    p = model.predict_proba(pd.DataFrame([partie.model_dump()]))[0, 1]
    return {"proba_victoire": round(float(p), 3)}
