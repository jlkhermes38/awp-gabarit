"""Exo 1 : trois figures. Fin à 11h00.

Question : où ce joueur perd-il des points ?
Les figures sont construites dans figures.py (le titre est calculé, il dit ce que montrent
les données) : l'appli de l'exo 2 et l'appli Dash les réutilisent.
Lancer : uv run python fil_rouge/01_figures.py
"""

from figures import fig_familles, fig_heures, fig_phases

from data import load_coups, load_data

df, coups = load_data(), load_coups()
print(df.shape, coups.shape)

# 1. Le score par famille d'ouvertures, la pire en haut
fig_familles(df).show()

# 2. La phase de la partie où tombent ses gaffes : ouverture, milieu, finale
fig_phases(coups).show()

# 3. Le score selon l'heure de la partie (heures UTC, au moins 30 parties par heure)
fig_heures(df).show()
