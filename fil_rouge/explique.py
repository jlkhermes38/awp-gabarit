"""Qu'est-ce qui pèse dans la prédiction ? Valeurs SHAP du modèle (lancer train.py d'abord).

shap et kaleido ne sont pas dans le projet :
uv run --with shap --with kaleido python fil_rouge/explique.py
"""

from pathlib import Path

import joblib
import pandas as pd
import plotly.express as px
import shap
from figures import BLEU, habiller

from data import load_data

ICI, VARIABLES = Path(__file__).parent, ["couleur", "cadence", "ecart_elo", "heure"]
df = load_data()
X = df[df["cadence"].isin(["bullet", "blitz", "rapid"])].dropna(subset=["ecart_elo"])[VARIABLES]

pipe = joblib.load(ICI / "model.joblib")
M = pipe[0].transform(X)
M = M.toarray() if hasattr(M, "toarray") else M
noms = [n.split("__")[1] for n in pipe[0].get_feature_names_out()]
explicateur = shap.LinearExplainer(pipe[-1], shap.maskers.Independent(M, max_samples=len(M)))
valeurs = pd.DataFrame(explicateur.shap_values(M), columns=noms)
# une variable = la somme de ses colonnes (le OneHotEncoder en crée une par modalité)
poids = pd.Series({v: valeurs.filter(regex=f"^{v}").sum(axis=1).abs().mean() for v in VARIABLES})
poids = poids.sort_values()
print(poids.round(3).to_string())
titre = f"{poids.index[-1]} pèse le plus dans le modèle (SHAP moyen {poids.iloc[-1]:.2f}) : vrai effet ou bruit ?"
fig = px.bar(poids, orientation="h", color_discrete_sequence=[BLEU], title=titre)
habiller(fig.update_layout(showlegend=False, xaxis_title=None, yaxis_title=None))
fig.write_image(ICI / "explique.png", width=900, height=450)
