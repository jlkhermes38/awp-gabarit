"""Service FastAPI : mes parties, mes ouvertures, une probabilité de victoire."""

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


@app.get("/parties")
def parties(cadence: str = "", couleur: str = "", limit: int = Query(20, ge=1, le=500)):
    vue = df
    if cadence:
        vue = vue[vue["cadence"] == cadence]
    if couleur:
        vue = vue[vue["couleur"] == couleur]
    cols = ["partie_id", "date_jeu", "cadence", "couleur", "resultat", "ouverture_famille"]
    return vue.tail(limit)[cols].fillna("").astype(str).to_dict("records")


@app.get("/ouvertures")
def ouvertures(cadence: str | None = None, min_n: int = 30):
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
