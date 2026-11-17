"""Exo 5 : la probabilité de gagner une partie. Fin à 16h15.

Question : avec quelle couleur, à quelle cadence, à quelle heure ce joueur gagne-t-il le plus ?
À produire : un modèle de classification scikit-learn, son erreur mesurée par validation croisée,
une référence à battre (toujours prédire la fréquence de victoire), et model.joblib enregistré
à côté de ce fichier (jamais versionné).
Lancer : uv run python fil_rouge/train.py
"""

import json
from pathlib import Path

import joblib
from sklearn.compose import make_column_transformer
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from data import load_data
from figures import fig_modele

ICI = Path(__file__).parent
df = load_data()
df = df[df["cadence"].isin(["bullet", "blitz", "rapid"])].dropna(subset=["ecart_elo"])
X, y = df[["couleur", "cadence", "ecart_elo", "heure"]], df["resultat"] == "victoire"

model = make_pipeline(
    make_column_transformer(
        (OneHotEncoder(handle_unknown="ignore"), ["couleur", "cadence", "heure"]),
        (StandardScaler(), ["ecart_elo"]),
    ),
    LogisticRegression(),
)
cv = StratifiedKFold(5, shuffle=True, random_state=0)
scoring = ["neg_log_loss", "roc_auc", "accuracy"]


def moyennes(m):
    r = cross_validate(m, X, y, cv=cv, scoring=scoring)
    return {
        "log_loss": -r["test_neg_log_loss"].mean(),
        "auc": r["test_roc_auc"].mean(),
        "exactitude": r["test_accuracy"].mean(),
    }


# La référence à battre : toujours prédire la fréquence de victoire de l'ensemble
mesures = {}
for nom, m in [("modele", model), ("reference", DummyClassifier(strategy="prior"))]:
    mesures[nom] = moyennes(m)
    s = mesures[nom]
    print(
        f"{nom} : log loss {s['log_loss']:.3f}, AUC {s['auc']:.3f}, exactitude {s['exactitude']:.1%}"
    )
mesures["n_parties"] = len(df)
(ICI / "metriques.json").write_text(json.dumps(mesures, indent=2))  # lu par client.py
joblib.dump(model.fit(X, y), ICI / "model.joblib")
fig_modele(df, model).write_html(ICI / "courbe_modele.html", include_plotlyjs="cdn")
print("figure : courbe_modele.html")
