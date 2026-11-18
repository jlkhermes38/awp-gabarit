# Cas 2 · Sécurité routière dans le Loiret

[← les six cas](README.md) · [toutes les données](../../data/projets/LISEZMOI.md)

## Le contexte

Chaque accident corporel (au moins une victime) fait l'objet d'une fiche remplie par les forces de l'ordre : le fichier BAAC, publié chaque année par l'ONISR. Ici, les accidents du Loiret de 2019 à 2025, une ligne par accident, avec le lieu, l'heure, la météo, le type de route et le nombre de victimes. Les moyens de contrôle et de prévention sont limités : il faut choisir où et quand les placer.

- **Qui utilise l'appli** : le service sécurité routière de la préfecture
- **La décision à éclairer** : où et quand cibler les contrôles et la prévention
- **Drill-down attendu** : département, commune, accident

## Les données

| | |
|---|---|
| Fichier | [`securite_routiere.parquet`](../../data/projets/securite_routiere.parquet) ([télécharger](https://github.com/jlkhermes38/awp-gabarit/raw/main/data/projets/securite_routiere.parquet)) |
| Lignes | 3 242 accidents, un par ligne |
| Période | 01/01/2019 → 31/12/2025 (616 en 2019, 413 en 2025) |
| Source | [ONISR, bases annuelles des accidents corporels (BAAC)](https://www.data.gouv.fr/datasets/bases-de-donnees-annuelles-des-accidents-corporels-de-la-circulation-routiere-annees-de-2005-a-2025/) : la page donne aussi la description de chaque code |
| Licence | Licence Ouverte 2.0 (Etalab) : citer « ONISR, fichier BAAC » |

```python
import pandas as pd
df = pd.read_parquet("data/projets/securite_routiere.parquet")
```

| Colonne | Ce qu'elle contient |
|---|---|
| `id_accident` | identifiant de l'accident |
| `date, an, mois, jour, heure` | quand (heure : 0 à 23) |
| `dep, com, commune` | département, code INSEE et nom de la commune |
| `lat, long` | position de l'accident |
| `grave` | `True` si au moins un tué ou un blessé hospitalisé |
| `nb_usagers, nb_tues, nb_hospitalises` | nombre de personnes impliquées, tuées, hospitalisées |
| `lum, lum_libelle` | lumière (plein jour, nuit avec ou sans éclairage…), code et texte |
| `atm, atm_libelle` | conditions atmosphériques (normale, pluie, brouillard…), code et texte |
| `catr, catr_libelle` | type de route (autoroute, départementale, voie communale…), code et texte |
| `agg` | 1 = hors agglomération, 2 = en agglomération |
| `int, col, surf, circ, nbv` | intersection, type de collision, état de la chaussée, régime de circulation, nombre de voies (codes BAAC, -1 = non renseigné) |
| `vma` | vitesse maximale autorisée, en km/h |


## À savoir avant de commencer

- les colonnes `int`, `col`, `surf` et `circ` sont des codes : traduisez ceux que vous affichez, avec la description de l'ONISR
- le taux dit où c'est grave, le nombre dit où agir : 69 % de graves sur autoroute, mais 116 accidents graves contre 674 sur les départementales
- 2020 est une année de confinement : comparer 2019 et 2020 ne dit rien de la prévention
- un modèle qui prédit la gravité ne dit pas où placer un contrôle : gardez la décision en tête
- le fichier ne contient aucune donnée sur les personnes : seulement des nombres de victimes

## Questions métier possibles

Des pistes, pas une liste à cocher : votre appli en soutient une ou deux, pour la décision ci-dessus.

1. Quelles communes et quels types de route comptent le plus d'accidents graves ?
2. À quelle heure et quel jour de la semaine les accidents graves sont-ils les plus nombreux ?
3. La nuit sans éclairage est-elle plus grave que le plein jour ?
4. La pluie ou le brouillard changent-ils la part d'accidents graves ?
5. Hors agglomération contre en agglomération : combien d'accidents, quelle part de graves ?
6. À quelle vitesse autorisée se produisent la plupart des accidents graves ?
7. Si la préfecture place trois contrôles par semaine, quels créneaux et quelles communes couvrent le plus d'accidents graves ?

## Pour aller plus loin

- **ML** : la probabilité qu'un accident soit grave selon le lieu, l'heure et la météo, et ce que ce modèle ne dit pas
- **LLM** : une note de synthèse pour le préfet sur la commune choisie

## Le constat déjà pris

« Sur autoroute, 69 % des accidents sont graves. Les routes départementales en comptent bien plus : 674 contre 116 (n = 3 242 accidents, 2019-2025) »

C'est la figure de départ du cas. Trouvez-en deux autres.
