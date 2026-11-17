"""Quatre figures Plotly. Le titre énonce ce que montrent les données : il est calculé, pas écrit.

Pour enregistrer les figures en HTML : uv run python fil_rouge/figures.py <dossier>
"""

import sys
from pathlib import Path

import joblib
import pandas as pd
import plotly.express as px

from data import familles, load_coups, load_data

BLEU, ORANGE, ROUGE = "#0072B2", "#E69F00", "#D55E00"  # Okabe-Ito
PHASES = {"opening": "en ouverture", "middlegame": "en milieu de partie", "endgame": "en finale"}
NBSP = "\u00a0"  # espace insécable : le « : » et le « % » ne passent pas seuls à la ligne


def pct(x: float) -> str:
    return f"{100 * x:.1f}{NBSP}%".replace(".", ",")


def habiller(fig):
    fig.update_xaxes(automargin=True)  # les titres d'axe ne sont plus coupés
    return fig.update_layout(
        template="plotly_white",
        font={"family": "Inter, Helvetica, sans-serif", "size": 15},
        margin={"l": 40, "r": 20, "t": 60, "b": 70},
    )


def vide():
    return habiller(px.bar(title="Rien à montrer avec ces filtres"))


def fig_familles(df, min_n=30):
    f = familles(df, min_n)
    if f.empty:
        return vide()
    pire = f.iloc[0]
    titre = f"{pire['famille']}{NBSP}: {pct(pire['score'])} de score en {pire['n']} parties"
    fig = px.bar(f, x="score", y="famille", color_discrete_sequence=[BLEU], title=titre)
    fig.update_yaxes(autorange="reversed", title=None, dtick=1)  # une étiquette par famille
    return habiller(fig).update_layout(height=max(400, 30 * len(f) + 120))


def fig_phases(coups):
    gaffes = coups[coups["jugement"] == "blunder"]["phase"].value_counts(normalize=True)
    if gaffes.empty:
        return vide()
    gaffes = gaffes.rename(index=PHASES).rename("part").reset_index()
    titre = f"{pct(gaffes['part'].max())} de mes gaffes arrivent {gaffes['phase'][0]}"
    return habiller(
        px.bar(gaffes, x="phase", y="part", color_discrete_sequence=[ORANGE], title=titre)
    )


def fig_heures(df, min_n=30):
    h = df.groupby("heure").agg(n=("score", "size"), score=("score", "mean")).reset_index()
    h = h[h["n"] >= min_n]
    haut, bas = h.loc[h["score"].idxmax()], h.loc[h["score"].idxmin()]
    titre = (
        f"Score de {pct(bas['score'])} à {int(bas['heure'])} h, "
        f"de {pct(haut['score'])} à {int(haut['heure'])} h (UTC)"
    )
    return habiller(px.bar(h, x="heure", y="score", color_discrete_sequence=[BLEU], title=titre))


def fig_elo(df, min_n=10):
    b = df[(df["plateforme"] == "lichess") & (df["cadence"] == "blitz")]
    m = b.groupby(b["date_jeu"].dt.to_period("M").dt.to_timestamp()).agg(
        n=("elo_joueur", "size"), elo=("elo_joueur", "median")
    )
    m = m[m["n"] >= min_n].reset_index()
    debut, fin = m.iloc[0], m.iloc[-1]
    titre = (
        f"Elo blitz sur Lichess{NBSP}: {debut['elo']:.0f} en {debut['date_jeu']:%m/%Y}, "
        f"{fin['elo']:.0f} en {fin['date_jeu']:%m/%Y}"
    )
    fig = px.line(m, x="date_jeu", y="elo", markers=True, title=titre)
    return habiller(fig.update_traces(line_color=BLEU, marker_color=BLEU))


def fig_modele(df, model, pas=25, min_n=15, borne=150):
    """Ce que le modèle a appris : chances de victoire prédites selon l'écart d'Elo, et observées."""
    cols = ["couleur", "cadence", "ecart_elo", "heure"]
    noms, heure = {"white": "blancs", "black": "noirs"}, int(df["heure"].median())
    ordre = {"cadence": ["bullet", "blitz", "rapid"], "couleur": ["blancs", "noirs"]}
    teintes = {"blancs": BLEU, "noirs": ROUGE}
    grille = pd.MultiIndex.from_product(
        [noms, ordre["cadence"], range(-borne, borne + 1, 5), [heure]], names=cols
    ).to_frame(index=False)
    grille["proba"] = model.predict_proba(grille)[:, 1]
    grille["couleur"] = grille["couleur"].map(noms)
    obs = df.assign(ecart=(df["ecart_elo"] // pas) * pas + pas / 2, couleur=df["couleur"].map(noms))
    obs = (
        obs[obs["ecart"].abs() <= borne]
        .groupby(["couleur", "cadence", "ecart"])
        .agg(n=("score", "size"), victoires=("resultat", lambda r: (r == "victoire").mean()))
    )
    obs = obs[obs["n"] >= min_n].reset_index()
    kw = {"color": "couleur", "facet_col": "cadence", "color_discrete_map": teintes}
    fig = px.line(grille, x="ecart_elo", y="proba", category_orders=ordre, **kw)
    pts = px.scatter(obs, x="ecart", y="victoires", size="n", category_orders=ordre, **kw)
    fig.add_traces([t.update(showlegend=False, opacity=0.5) for t in pts.data])

    def p(e):
        return model.predict_proba(pd.DataFrame([["white", "blitz", e, heure]], columns=cols))[0, 1]

    titre = (
        f"+100 points d'Elo chez l'adversaire : {100 * (p(100) - p(0)):.0f}{NBSP}points de chances "
        f"de victoire (blitz, blancs, {pct(p(0))} à Elo égal)"
    )
    fig.update_yaxes(tickformat=".0%", title=None).update_xaxes(title=None)
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))
    note = (
        "Elo de l'adversaire moins le mien, avant la partie. Lignes : modèle. "
        "Points : parties observées par tranche de 25, taille = nombre de parties (au moins 15)."
    )
    fig.add_annotation(text=note, x=0.5, y=-0.18, xref="paper", yref="paper", showarrow=False)
    fig.update_layout(title=titre, legend_title_text="ma couleur")
    return habiller(fig).update_layout(margin={"b": 90})


if __name__ == "__main__":
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    df, coups = load_data(), load_coups()
    figs = {
        "familles": fig_familles(df),
        "phases": fig_phases(coups),
        "heures": fig_heures(df),
        "elo": fig_elo(df),
    }
    if (modele := Path(__file__).parent / "model.joblib").exists():
        figs["modele"] = fig_modele(df, joblib.load(modele))
    for nom, fig in figs.items():
        # le titre de fig_modele est long : il lui faut plus de largeur
        fig.update_layout(
            width=1400 if nom == "modele" else 900, height=560 if nom == "modele" else 520
        )
        fig.write_html(
            out / f"{nom}.html", include_plotlyjs="cdn", config={"displayModeBar": False}
        )
    print("ok", list(figs))
