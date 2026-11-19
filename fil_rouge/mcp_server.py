"""Exo 6 : votre propre serveur MCP. Environ 20 min.

Question : un LLM doit pouvoir interroger mes parties.
À produire : un serveur FastMCP de deux ou trois outils au-dessus de votre API (api.py doit
tourner). Le LLM choisit un outil d'après son nom, sa docstring et ses arguments : soignez-les.
Lancer : uv run python fil_rouge/mcp_server.py   (stdio : c'est le client LLM qui le lance,
voir contexte/README.md pour le brancher). Lancé à la main, il n'affiche rien et attend un
client : c'est normal. Pour tester : npx @modelcontextprotocol/inspector uv run python fil_rouge/mcp_server.py
"""

import os
from typing import Literal

import requests
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings

API = os.environ.get("AWP_API_URL", "http://127.0.0.1:8000")
Couleur, Cadence = Literal["white", "black"], Literal["bullet", "blitz", "rapid"]
# Deux transports. stdio (par défaut) : le client LLM lance ce script lui-même, sur la même machine.
# MCP_TRANSPORT=http : un serveur HTTP sur /mcp, pour un client qui ne lance pas le script (un client
# dans le cloud, via un hébergeur ou un tunnel). En local : 127.0.0.1:8001 (l'API est sur 8000), pas
# ouvert à la salle. Sur un hébergeur qui fixe $PORT (Render, Cloud Run) : 0.0.0.0:$PORT.
HTTP = os.environ.get("MCP_TRANSPORT") == "http"
HOTE = "0.0.0.0" if "PORT" in os.environ else "127.0.0.1"
# En local, FastMCP refuse un nom d'hôte autre que 127.0.0.1 ou localhost (protection contre le DNS
# rebinding). Derrière un tunnel (MCP_TUNNEL=1), l'hôte est celui du tunnel : on lève la protection,
# le serveur est de toute façon public tant que le tunnel tourne.
TUNNEL = os.environ.get("MCP_TUNNEL") == "1"
SECU = TransportSecuritySettings(enable_dns_rebinding_protection=False) if TUNNEL else None
mcp = FastMCP(
    "echecs", host=HOTE, port=int(os.environ.get("PORT", "8001")), transport_security=SECU
)


def appeler_api(path, params=None, json=None):  # POST si on envoie un corps, GET sinon
    r = requests.request(
        "POST" if json else "GET", API + path, params=params, json=json, timeout=10
    )
    r.raise_for_status()
    return r.json()


@mcp.tool()
def pire_ouvertures(cadence: Cadence = "blitz", n: int = 5) -> list[dict]:
    """Classe mes familles d'ouvertures de la pire à la meilleure pour une cadence.

    n : nombre de familles renvoyées (les n pires). Seules comptent les familles d'au moins 30
    parties (seuil fixe). Chaque famille donne n (ses parties jouées), score (1 = tout gagné,
    0,5 = autant de victoires que de défaites, 0 = tout perdu) et gaffes (par partie).
    """
    return appeler_api("/ouvertures", {"cadence": cadence, "min_n": 30})[:n]


@mcp.tool()
def proba_victoire(couleur: Couleur, cadence: Cadence, ecart_elo: int, heure: int) -> dict:
    """Estime mes chances de gagner une partie avec un modèle appris sur mes parties.

    couleur : la mienne. ecart_elo : Elo de l'adversaire moins le mien (positif = plus fort).
    heure : heure UTC de la partie, de 0 à 23. Renvoie proba_victoire, entre 0 et 1.
    """
    corps = {"couleur": couleur, "cadence": cadence, "ecart_elo": ecart_elo, "heure": heure}
    return appeler_api("/predict", json=corps)


if __name__ == "__main__":
    # Derrière un tunnel : MCP_TUNNEL=1 MCP_TRANSPORT=http uv run python …, puis npx localtunnel --port 8001
    mcp.run(transport="streamable-http" if HTTP else "stdio")
