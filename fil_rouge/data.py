"""Chargement des prix des carburants du Loiret (API data.economie.gouv.fr), avec repli sur un CSV."""

from pathlib import Path

import pandas as pd
import requests

API = (
    "https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/"
    "prix-des-carburants-en-france-flux-instantane-v2/records"
)
DATA = Path(__file__).resolve().parents[1] / "data"
SNAPSHOT = DATA / "carburants_45.csv"  # versionné dans git, jamais réécrit
CACHE = DATA / "cache" / "carburants_45.csv"  # copie du dernier appel réussi, hors git
CARBURANTS = ["gazole", "e10", "sp95", "sp98", "e85", "gplc"]


def fetch(departement: str = "45") -> pd.DataFrame:
    """Toutes les stations d'un département, une ligne par station."""
    rows, offset = [], 0
    while True:
        r = requests.get(
            API,
            params={"where": f'code_departement="{departement}"', "limit": 100, "offset": offset},
            timeout=20,
        )
        r.raise_for_status()
        page = r.json()["results"]
        rows += page
        offset += 100
        if len(page) < 100:
            break
    df = pd.json_normalize(rows)
    return df.rename(columns={"geom.lat": "lat", "geom.lon": "lon"})


def tidy(df: pd.DataFrame) -> pd.DataFrame:
    """Format long : une ligne par station et par carburant."""
    keep = ["id", "ville", "adresse", "pop", "lat", "lon"]
    prix = [f"{c}_prix" for c in CARBURANTS]
    long = (
        df[keep + prix]
        .melt(
            id_vars=keep,
            value_vars=prix,
            var_name="carburant",
            value_name="prix",
        )
        .dropna(subset=["prix"])
    )
    long["carburant"] = long["carburant"].str.removesuffix("_prix").str.upper()
    long["axe"] = long["pop"].map({"R": "Route", "A": "Autoroute"})
    return long


def load_data() -> pd.DataFrame:
    """L'API si elle répond, sinon la dernière copie, sinon l'instantané du dépôt."""
    try:
        df = tidy(fetch())
        CACHE.parent.mkdir(exist_ok=True)
        df.to_csv(CACHE, index=False)
        return df
    except requests.RequestException:
        return pd.read_csv(CACHE if CACHE.exists() else SNAPSHOT)


if __name__ == "__main__":
    d = load_data()
    print(f"{len(d)} lignes, {d['id'].nunique()} stations, {d['carburant'].nunique()} carburants")
