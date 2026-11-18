# AWP : applications web de données avec Python

CODA Orléans, M2-D, jeudi 19 et vendredi 20 novembre 2026.

Sur cette page, **Use this template** → **Create a new repository**, en public : c'est sur
votre copie que vous pousserez à l'exo 3. Puis :

```bash
git clone https://github.com/<votre-compte>/<votre-copie>
cd <votre-copie>
uv sync
uv run pytest -q     # 2 passed, 2 skipped : les données se lisent, le reste est à faire
```

## Jeudi, le fil rouge : mes parties d'échecs

Le jeu de données est celui d'un joueur, exporté de ChessXP et anonymisé : `data/echecs/`.
Lisez d'abord `data/echecs/LISEZMOI.md` (une section par fichier, les colonnes et leurs pièges), puis
`data/echecs/conseils.md` (comment ChessXP juge un coup). La question de la journée : « je joue depuis
2023, je stagne, qu'est-ce que je devrais travailler ? » Vous n'avez pas besoin de savoir jouer.

Les fichiers de `fil_rouge/` sont des squelettes : un énoncé en tête, des `TODO`, pas de solution.

| Exo | Fin | Fichier | Lancer |
|---|---|---|---|
| 1 | 11h00 | `fil_rouge/data.py`, `fil_rouge/01_figures.py` | `uv run python fil_rouge/01_figures.py` |
| 2 | 12h30 | `fil_rouge/app_streamlit.py` | `uv run streamlit run fil_rouge/app_streamlit.py --server.address 127.0.0.1` |
| 3 | 14h00 | le même, en ligne | share.streamlit.io, fichier d'entrée `fil_rouge/app_streamlit.py` |
| 4 | 15h00 | `fil_rouge/app_dash.py` | `uv run python fil_rouge/app_dash.py` |
| 5 | 16h15 | `fil_rouge/train.py`, `api.py`, `client.py` | `uv run python fil_rouge/train.py`, puis `uv run uvicorn api:app --app-dir fil_rouge --host 127.0.0.1 --port 8000 --reload`, puis `uv run streamlit run fil_rouge/client.py --server.address 127.0.0.1` |
| 6 | 17h00 | l'appli de l'exo 2, puis `fil_rouge/mcp_server.py` | `uv run streamlit run fil_rouge/app_streamlit.py --server.enableAgentApi=true --server.address 127.0.0.1`, puis `uv run python fil_rouge/mcp_server.py` (en HTTP : `MCP_TRANSPORT=http uv run python fil_rouge/mcp_server.py`, sur `http://127.0.0.1:8001/mcp`) |

`contexte/README.md` : les tips, dans l'ordre de la journée (documentation en Markdown, `llms.txt`,
`streamlit skills`, brancher un serveur MCP). Chaque exo se termine par la lecture du code que
l'assistant a écrit : vous expliquez les lignes.

Bloqué : la branche `solutions` de ce dépôt contient le fil rouge terminé, mise à jour à la
fin de chaque exo. Votre copie ne la suit pas, ajoutez ce dépôt comme second remote :

```bash
git remote add prof https://github.com/jlkhermes38/awp-gabarit   # une seule fois
git fetch prof
git checkout prof/solutions -- fil_rouge/app_streamlit.py      # un seul fichier
```

`AGENTS.md` est la base Dash fournie par Plotly, pour votre assistant de code.

## Vendredi, le projet

- `data/projets/` : un Parquet par cas, six cas en tout. Sources, licences, périodes et une ligne d'exemple dans `summary.json`
- `projet/app.py` : le point de départ, `uv run streamlit run projet/app.py --server.address 127.0.0.1`
- `projet/llm.py` : un client compatible OpenAI (Ollama, Groq, Google AI Studio). Copiez `.streamlit/secrets.toml.example` en `.streamlit/secrets.toml`, jamais versionné
- `tests/test_app.py` : les tests du dépôt, `uv run pytest -q`

| Cas | Fichier | Licence |
|---|---|---|
| Énergie | `energie.parquet` | Licence Ouverte 2.0 |
| Sécurité routière | `securite_routiere.parquet` | Licence Ouverte 2.0 |
| Immobilier | `immobilier.parquet` | Licence Ouverte 2.0 |
| Location courte durée | `airbnb_lyon.parquet`, `airbnb_lyon_reviews.parquet` | CC BY 4.0 (Inside Airbnb) |
| E-commerce | `olist.parquet`, `olist_commentaires_negatifs.parquet` | CC BY-NC-SA 4.0 (Olist) |
| Territoire du Loiret | `territoire_loiret.parquet` | Licence Ouverte 2.0 |

Un cas peut être pris par deux groupes, à condition que leurs décisions diffèrent. Vous pouvez aussi
apporter votre propre jeu de données, validé au cadrage : licence, taille, aucune donnée personnelle.
