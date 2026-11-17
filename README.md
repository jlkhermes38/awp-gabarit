# AWP : applications web de données avec Python

CODA Orléans, M2-D, jeudi 19 et vendredi 20 novembre 2026.

Sur cette page, **Use this template** → **Create a new repository**, en public : c'est sur
votre copie que vous pousserez à l'exo 3. Puis :

```bash
git clone https://github.com/<votre-compte>/<votre-copie>
cd <votre-copie>
uv sync
uv run python fil_rouge/data.py     # 379 lignes, 107 stations, six carburants
```

Pas de réseau, ou l'API ne répond pas : `data.py` lit `data/carburants_45.csv`, le même jeu.

## Jeudi, le fil rouge : les prix des carburants du Loiret

| Exo | Fichier | Lancer |
|---|---|---|
| 1 | `fil_rouge/01_figures.py` | `uv run python fil_rouge/01_figures.py` |
| 2 | `fil_rouge/app_streamlit.py` | `uv run streamlit run fil_rouge/app_streamlit.py` |
| 3 | le même, en ligne | share.streamlit.io, fichier d'entrée `fil_rouge/app_streamlit.py` |
| 4 | `fil_rouge/app_dash.py` | `uv run python fil_rouge/app_dash.py` |
| 5 | `fil_rouge/train.py`, `api.py`, `client.py` | `uv run python fil_rouge/train.py`, puis `uv run uvicorn api:app --app-dir fil_rouge --reload`, puis `uv run streamlit run fil_rouge/client.py` |
| 6 | l'appli de l'exo 2 | `uv run streamlit run fil_rouge/app_streamlit.py --server.enableAgentApi=true --server.address 127.0.0.1` |

Bloqué : la branche `solutions` de ce dépôt contient le fil rouge terminé, mise à jour à la
fin de chaque exo. Votre copie ne la suit pas, ajoutez ce dépôt comme second remote :

```bash
git remote add prof https://github.com/jlkhermes38/awp-gabarit   # une seule fois
git fetch prof
git checkout prof/solutions -- fil_rouge/app_streamlit.py      # un seul fichier
```

`AGENTS.md` est la base Dash fournie par Plotly, pour votre assistant de code.

## Vendredi, le projet

- `data/projets/` : un Parquet par cas. Sources, licences, périodes et une ligne d'exemple dans `summary.json`
- `projet/app.py` : le point de départ, `uv run streamlit run projet/app.py`
- `projet/llm.py` : un client compatible OpenAI (Ollama, Groq, Google AI Studio). Copiez `.streamlit/secrets.toml.example` en `.streamlit/secrets.toml`, jamais versionné
- `tests/test_app.py` : un test qui lance l'appli, `uv run pytest -q`

| Cas | Fichier | Licence |
|---|---|---|
| Énergie | `energie.parquet` | Licence Ouverte 2.0 |
| Sécurité routière | `securite_routiere.parquet` | Licence Ouverte 2.0 |
| Immobilier | `immobilier.parquet` | Licence Ouverte 2.0 |
| Location courte durée | `airbnb_lyon.parquet`, `airbnb_lyon_reviews.parquet` | CC BY 4.0 (Inside Airbnb) |
| E-commerce | `olist.parquet`, `olist_commentaires_negatifs.parquet` | CC BY-NC-SA 4.0 (Olist) |
| Territoire du Loiret | `territoire_loiret.parquet` | Licence Ouverte 2.0 |
| Échecs | à venir | données d'un joueur, partagées par lui |
