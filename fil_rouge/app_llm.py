# Résumé écrit par un petit LLM : uv run streamlit run fil_rouge/app_llm.py --server.address 127.0.0.1
import os
import re

import streamlit as st
from openai import OpenAI

from data import load_data

# Ollama en local par défaut. Groq : LLM_URL=https://api.groq.com/openai/v1
LLM_URL = os.environ.get("LLM_URL", "http://localhost:11434/v1")
LLM_KEY = os.environ.get("LLM_KEY", "ollama")
LLM_MODEL = os.environ.get("LLM_MODEL", "qwen3:0.6b")
CONSIGNE = "Résume ce tableau en 3 phrases, en français, sans inventer de chiffre. /no_think"

client = OpenAI(base_url=LLM_URL, api_key=LLM_KEY)


@st.cache_data(ttl=600)
def donnees():
    return load_data()


@st.cache_data(ttl=3600)  # même filtre, même réponse, pas de nouvel appel
def resumer(agregat: str) -> str:
    messages = [{"role": "system", "content": CONSIGNE}, {"role": "user", "content": agregat}]
    r = client.chat.completions.create(model=LLM_MODEL, temperature=0, messages=messages)
    return re.sub(r"<think>.*?</think>", "", r.choices[0].message.content, flags=re.DOTALL).strip()


df = donnees()
st.title("Est-ce que je progresse aux échecs ?")
options = sorted(df["cadence"].unique())
cadence = st.selectbox("Cadence", options, index=options.index("blitz"), key="cadence")
vue = df[df["cadence"] == cadence]

trimestre = vue["date_jeu"].dt.to_period("Q").astype(str).rename("trimestre")
agregat = (
    vue.groupby(trimestre)
    .agg(
        parties=("score", "size"),
        score=("score", "mean"),
        gaffes_par_partie=("gaffes_joueur", "mean"),
    )
    .round(3)
)

st.info(resumer(agregat.reset_index().to_csv(index=False)))
st.caption(f"Texte généré par {LLM_MODEL} à partir du tableau ci-dessous.")
st.dataframe(agregat)
