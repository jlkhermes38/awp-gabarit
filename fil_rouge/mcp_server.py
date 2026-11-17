"""Serveur MCP : deux outils sur mes parties d'échecs. Ils appellent l'API (api.py doit tourner)."""

import os
from typing import Literal

import requests
from mcp.server.fastmcp import FastMCP

API = os.environ.get("AWP_API_URL", "http://127.0.0.1:8000")
Couleur, Cadence = Literal["white", "black"], Literal["bullet", "blitz", "rapid"]
mcp = FastMCP("echecs")


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
    mcp.run()  # stdio : le client LLM lance ce script lui-même
