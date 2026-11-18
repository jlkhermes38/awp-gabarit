# Cas 2 · Collèges du Loiret

[← les cas](README.md) · [toutes les données](../../data/projets/LISEZMOI.md)

## D'où vient ce cas

Les cas 1 à 3 viennent du Département du Loiret. Une directrice du Département, chef de projet « travailler avec l'IA », m'a envoyé le catalogue de données GéoLoiret et trois pistes : croiser les OLD avec le tracé des véloroutes, les collèges, les risques. Le catalogue : [geoloiret.loiret-numerique.fr](https://geoloiret.loiret-numerique.fr/apps/referentiel/catalogue_donnees.htm).

Les collèges sont la première compétence du Département dans l'éducation : c'est lui qui les construit, les agrandit, les équipe et dessine leurs secteurs de recrutement.

## Le contexte

Le code de l'éducation est clair : « Le département a la charge des collèges. Il en assure la construction, la reconstruction, l'extension, les grosses réparations, l'équipement et le fonctionnement » ([article L213-2](https://www.legifrance.gouv.fr/codes/id/LEGISCTA000006166574)). Le conseil départemental arrête aussi « la localisation des établissements, leur capacité d'accueil, leur secteur de recrutement et le mode d'hébergement des élèves », en tenant compte de critères d'équilibre démographique, économique et social (article L213-1). Le Loiret compte 70 collèges, 58 publics et 12 privés. Un collège qui gagne beaucoup d'élèves en quelques années demande des travaux ; deux collèges voisins, l'un plein, l'autre qui se vide, posent la question du secteur.

- **Qui utilise l'appli** : la direction du Département chargée des collèges, et l'élu qui propose la sectorisation au conseil départemental
- **La décision à éclairer** : où programmer des travaux (extension, restructuration, cantine), et quel secteur redessiner, au vu des effectifs et de leur évolution
- **Drill-down attendu** : secteur, collège, rentrée, niveau

## Les données

| | |
|---|---|
| Fichiers | [`colleges.parquet`](../../data/projets/colleges.parquet) ([télécharger](https://github.com/jlkhermes38/awp-gabarit/raw/main/data/projets/colleges.parquet)), [`colleges_secteurs.geojson`](../../data/projets/colleges_secteurs.geojson) ([télécharger](https://github.com/jlkhermes38/awp-gabarit/raw/main/data/projets/colleges_secteurs.geojson)) |
| Lignes | 690 lignes : 70 collèges × 10 rentrées (deux collèges ouverts en 2021 n'en ont que 5) |
| Période | rentrées 2016 à 2025 ; effectifs à partir de 2019, brevet jusqu'à la session 2025 (rentrée 2024) |
| Source | GéoLoiret : [collèges](https://geoloiret.loiret-numerique.fr/ags25/rest/services/III_2_Batiment/ETABLISSEMENTS_SCOLAIRES/FeatureServer/4), [secteurs des collèges](https://geoloiret.loiret-numerique.fr/ags25/rest/services/III_11_Zones_Gestion/SECTORISATION_EDUCATION/FeatureServer/3) ; ministère de l'Éducation nationale, [data.education.gouv.fr](https://data.education.gouv.fr) : effectifs par niveau (`fr-en-college-effectifs-niveau-sexe-lv`), indice de position sociale (`fr-en-ips_colleges`, `…-ap2022`, `…-ap2023`), brevet (`fr-en-dnb-par-etablissement`, `fr-en-indicateurs-valeur-ajoutee-colleges`) |
| Licence | Licence Ouverte 2.0 pour les données du ministère ; GéoLoiret : mention « Source : Département du Loiret » |

```python
import json, pandas as pd, plotly.express as px

df = pd.read_parquet("data/projets/colleges.parquet")
secteurs = json.load(open("data/projets/colleges_secteurs.geojson"))
_2025 = df[(df["rentree"] == 2025) & df["secteur_id"].notna()]
fig = px.choropleth_map(_2025, geojson=secteurs, locations="secteur_id",
                        featureidkey="properties.secteur_id", color="effectif_total", zoom=8,
                        center={"lat": 47.9, "lon": 2.2})
```

| Colonne | Ce qu'elle contient |
|---|---|
| `uai` | code de l'établissement (UAI), la clé de jointure |
| `nom, commune, code_insee` | nom du collège (sans le mot « Collège »), commune et son code INSEE |
| `statut` | `public` ou `privé` |
| `lat, lon` | position du collège |
| `secteur_id` | secteur de recrutement dans `colleges_secteurs.geojson` (= UAI) ; vide pour les 12 privés |
| `rentree, annee_scolaire` | rentrée (2019 = année 2019-2020) et le texte « 2019-2020 » |
| `effectif_total` | élèves de la 6e à la 3e, SEGPA et ULIS compris (à partir de 2019) |
| `effectif_6e, effectif_5e, effectif_4e, effectif_3e` | élèves par niveau (leur somme = le total) |
| `effectif_segpa, effectif_ulis` | élèves en SEGPA et en ULIS, déjà comptés dans le total |
| `rep, rep_plus` | 1 si le collège est en éducation prioritaire REP, ou REP+ |
| `ips, ips_ecart_type` | indice de position sociale des élèves (plus il est haut, plus l'origine sociale est favorisée ; moyenne nationale proche de 100) et sa dispersion |
| `session_dnb, dnb_candidats` | session du brevet qui clôt l'année (= rentrée + 1) et candidats présents |
| `dnb_taux_reussite, dnb_taux_mention` | taux de réussite au brevet et part de mentions, en % |
| `dnb_valeur_ajoutee` | écart au taux de réussite attendu pour des élèves comparables, en points (sessions 2022 à 2025) |
| `source_dnb` | `dnb-par-etablissement` (jusqu'à la rentrée 2020) ou `ivac` (à partir de 2021) |

`colleges_secteurs.geojson` : 59 secteurs (WGS 84), `properties.secteur_id` = UAI. Deux secteurs appartiennent à des collèges du Loir-et-Cher. À Orléans La Source, un seul secteur est partagé par deux collèges.

## À savoir avant de commencer

- le brevet vient de deux sources : jusqu'à la rentrée 2020, toutes séries avec une décimale ; à partir de 2021, série générale arrondie à l'unité. Une marche entre 2020 et 2021 peut venir de la méthode, pas des élèves
- `rentree` 2020, c'est l'année 2020-2021, donc le brevet de 2021 : ne mélangez pas rentrée et session
- public et privé n'accueillent pas les mêmes élèves : un taux de réussite plus haut ne dit pas que le collège « fait » la réussite
- un collège avec 40 candidats au brevet peut gagner 10 points d'une année sur l'autre : ne classez pas sur une seule année
- les effectifs commencent à la rentrée 2019 ; 2016 à 2018 n'ont que l'IPS et le brevet
- la carte des secteurs : `featureidkey="properties.secteur_id"` dans `px.choropleth_map`

## Questions métier possibles

Des pistes, pas une liste à cocher : votre appli en soutient une ou deux, pour la décision ci-dessus.

1. Quels collèges publics gagnent ou perdent le plus d'élèves depuis 2019 ?
2. Où l'effectif de 6e annonce-t-il une hausse dans les années qui viennent ?
3. Faut-il redessiner un secteur pour rééquilibrer deux collèges voisins ?
4. Quels collèges programmer en priorité pour une extension ou une restructuration ?
5. Comment dimensionner les cantines selon l'évolution des effectifs ?
6. Comment présenter à un élu l'écart entre public et privé sans conclure à tort ?

## Questions ouvertes sur les données

Des questions précises, à trancher avec le fichier, chiffres à l'appui. Les réponses ne sont pas données : c'est votre première exploration.

1. Quels collèges publics ont perdu le plus d'élèves entre 2019 et 2025, en nombre et en pourcentage ?
2. Dans quels collèges la 6e de 2025 est-elle plus nombreuse que la 3e ?
3. Quel lien entre l'IPS et le taux de réussite au brevet, en 2024 ?
4. Quels collèges réussissent mieux que leur IPS ne le laisse attendre (`dnb_valeur_ajoutee`) ?
5. Les collèges REP et REP+ ont-ils des effectifs différents des autres ?
6. Quels collèges sont très en dessous de l'effectif médian ?

## Pour aller plus loin

- **ML** : prévoir l'effectif de chaque collège à la prochaine rentrée, à partir des niveaux de l'année
- **LLM** : une fiche collège pour un élu : effectifs, tendance, points d'attention, à partir des chiffres affichés
