"""Service FastAPI : les stations et une prédiction de prix."""

from functools import lru_cache
from pathlib import Path
from typing import Literal

import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

from data import load_data

app = FastAPI(title="Carburants Loiret", version="1.0")
model = joblib.load(
    Path(__file__).parent / "model.joblib"
)  # chargé une fois, au démarrage du service


@lru_cache
def data():
    return load_data()


@app.get("/stations")
def stations(carburant: str = "E10", limit: int = 20):
    vue = data()[data()["carburant"] == carburant.upper()].nsmallest(limit, "prix")
    return vue[["ville", "adresse", "prix"]].to_dict("records")


class Station(BaseModel):
    carburant: Literal["GAZOLE", "E10", "SP95", "SP98", "E85", "GPLC"]
    axe: Literal["Route", "Autoroute"]
    lat: float
    lon: float


@app.post("/predict")
def predict(station: Station) -> dict:
    prix = model.predict(pd.DataFrame([station.model_dump()]))[0]
    return {"prix_estime": round(float(prix), 3)}
