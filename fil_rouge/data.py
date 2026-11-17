"""Exo 1 : lire mes parties d'échecs. Fin à 11h00.

Question : je joue depuis 2023, je stagne, qu'est-ce que je devrais travailler ?
À produire : un DataFrame propre, prêt pour les figures de l'exo 1 et pour l'appli de l'exo 2.
Les colonnes et leurs pièges sont dans data/echecs/LISEZMOI.md : lisez-le d'abord.
Lancer : uv run python fil_rouge/data.py
"""

from pathlib import Path

import pandas as pd

DATA = Path(__file__).resolve().parents[1] / "data" / "echecs"
SCORES = {"win": 1.0, "draw": 0.5, "lose": 0.0}
RESULTATS = {"win": "victoire", "draw": "nulle", "lose": "défaite"}
NUMERIQUES = ["elo_joueur", "elo_adverse", "gaffes_joueur", "nb_coups"]


def valider(df: pd.DataFrame) -> pd.DataFrame:
    """Plan B : on s'arrête avec un message clair si le fichier n'a pas la forme attendue."""
    absentes = [c for c in [*NUMERIQUES, "partie_id", "date_jeu", "resultat"] if c not in df]
    if absentes:
        raise ValueError(f"colonnes absentes : {absentes}")
    vides = [c for c in NUMERIQUES if df[c].isna().all()]
    if vides:
        raise ValueError(f"colonnes entièrement vides : {vides}")
    texte = [c for c in NUMERIQUES if not pd.api.types.is_numeric_dtype(df[c])]
    if texte:
        raise ValueError(f"colonnes lues comme du texte : {texte}")
    if not df["partie_id"].is_unique:
        raise ValueError("partie_id en double")
    inconnus = set(df["resultat"]) - set(SCORES)
    if inconnus:
        raise ValueError(f"résultats inconnus : {inconnus}")
    return df


def load_data() -> pd.DataFrame:
    """Une ligne par partie, avec le résultat de mon point de vue et un score 1 / 0,5 / 0."""
    df = valider(pd.read_csv(DATA / "parties.csv", parse_dates=["date_jeu"]))
    df["score"] = df["resultat"].map(SCORES)
    df["resultat"] = df["resultat"].map(RESULTATS)
    df["cadence"] = df["cadence"].fillna(
        "aucune"
    )  # 48 parties : correspondance, importées, 3 Lichess sans pendule
    df["annee"] = df["date_jeu"].dt.year
    df["heure"] = df["date_jeu"].dt.hour  # UTC
    df["ecart_elo"] = df["elo_adverse"] - df["elo_joueur"]
    return df


def load_coups() -> pd.DataFrame:
    """Un de mes coups jugés mauvais par ligne (jamais mes bons coups)."""
    return pd.read_csv(DATA / "coups_juges.csv")


def familles(df: pd.DataFrame, min_n: int = 30) -> pd.DataFrame:
    """Score par famille d'ouvertures, la pire d'abord. Sous min_n parties, le chiffre ne dit rien."""
    g = df.groupby("ouverture_famille").agg(
        n=("score", "size"), score=("score", "mean"), gaffes=("gaffes_joueur", "mean")
    )
    g = g[g["n"] >= min_n].sort_values("score").round(3)
    return g.reset_index().rename(columns={"ouverture_famille": "famille"})


if __name__ == "__main__":
    d = load_data()
    print(d.shape, d["resultat"].value_counts().to_dict())
    print(familles(d).head(3).to_string(index=False))
