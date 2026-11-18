# Cas 3 · Risques naturels et technologiques dans le Loiret

[← les cas](README.md) · [toutes les données](../../data/projets/LISEZMOI.md)

## D'où vient ce cas

Les cas 1 à 3 viennent du Département du Loiret. Une directrice du Département, chef de projet « travailler avec l'IA », m'a envoyé le catalogue de données GéoLoiret et trois pistes : croiser les OLD avec le tracé des véloroutes, les collèges, les risques. Le catalogue : [geoloiret.loiret-numerique.fr](https://geoloiret.loiret-numerique.fr/apps/referentiel/catalogue_donnees.htm).

Le Département n'établit pas les plans de prévention (c'est l'État) ni les documents d'information communaux (c'est le maire). Mais ses routes, ses collèges et le budget des pompiers sont exposés aux mêmes risques.

## Le contexte

Le Département entretient les routes départementales, à sa charge ([code de la voirie routière, L131-1 et suivants](https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006070667/LEGISCTA000006116687/)), il a la charge des 58 collèges publics (code de l'éducation, L213-2), et sa contribution au budget du service départemental d'incendie et de secours (SDIS) est une dépense obligatoire ([CGCT, L1424-35](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044374449)). Dans le Loiret, les risques sont connus : argiles qui gonflent et se rétractent, cavités souterraines, crues de la Loire et de ses affluents, sites industriels, transport de matières dangereuses. Les arrêtés de catastrophe naturelle (CatNat) montrent ceux qui ont déjà coûté.

- **Qui utilise l'appli** : les directions du Département chargées des routes et des collèges, et les élus qui répartissent les crédits de prévention
- **La décision à éclairer** : où concentrer la prévention et les diagnostics : quelles communes, quels collèges, quelles routes départementales, selon l'exposition et les catastrophes déjà reconnues
- **Drill-down attendu** : type de risque, commune, arrêté

## Les données

| | |
|---|---|
| Fichiers | [`risques_communes.parquet`](../../data/projets/risques_communes.parquet) ([télécharger](https://github.com/jlkhermes38/awp-gabarit/raw/main/data/projets/risques_communes.parquet)), [`risques_catnat.parquet`](../../data/projets/risques_catnat.parquet) ([télécharger](https://github.com/jlkhermes38/awp-gabarit/raw/main/data/projets/risques_catnat.parquet)), [`risques_communes.geojson`](../../data/projets/risques_communes.geojson) ([télécharger](https://github.com/jlkhermes38/awp-gabarit/raw/main/data/projets/risques_communes.geojson)) |
| Lignes | 325 communes ; 2 065 décisions CatNat (165 arrêtés) |
| Période | événements reconnus du 01/04/1983 au 24/03/2025 (export GASPAR du 02/11/2026) ; couches GéoLoiret de 2024 à 2026 |
| Source | GéoLoiret, [catalogue des risques](https://geoloiret.loiret-numerique.fr/apps/referentiel/catalogue_donnees.htm) : argiles, cavités et mouvements de terrain (BRGM), périmètres des PPRI (DDT45), repères de crues, installations classées (ICPE), transport de matières dangereuses, centrales nucléaires ; Géorisques, [arrêtés CatNat (GASPAR)](https://files.georisques.fr/GASPAR/gaspar.zip) ; INSEE, population 2023 |
| Licence | Licence Ouverte 2.0. Mentions : « Source : BRGM / DDT45 / Département du Loiret, année », « Géorisques, GASPAR » |

```python
import json, pandas as pd, plotly.express as px

df = pd.read_parquet("data/projets/risques_communes.parquet")
catnat = pd.read_parquet("data/projets/risques_catnat.parquet")
communes = json.load(open("data/projets/risques_communes.geojson"))  # id = code INSEE
fig = px.choropleth_map(df, geojson=communes, locations="code_insee", color="pct_argiles_fort", zoom=8,
                        center={"lat": 47.9, "lon": 2.2})
```

### `risques_communes.parquet`, une ligne par commune

| Colonne | Ce qu'elle contient |
|---|---|
| `code_insee, commune` | code INSEE (texte) et nom |
| `population_2023, superficie_km2` | population municipale 2023 et surface |
| `pct_argiles_fort, pct_argiles_moyen, pct_argiles_faible` | part de la surface en aléa retrait-gonflement des argiles fort, moyen, faible (%) |
| `nb_cavites` | cavités souterraines recensées (BRGM) |
| `nb_mouvements_terrain, nb_effondrements` | mouvements de terrain recensés, dont effondrements |
| `pct_ppri, ppri, nb_ppri` | part de la surface dans un périmètre de plan de prévention du risque inondation (PPRI), leurs noms, leur nombre |
| `nb_reperes_crues` | repères de crues |
| `nb_icpe, nb_icpe_autorisation` | installations classées pour l'environnement, dont celles soumises à autorisation |
| `nb_seveso, nb_seveso_seuil_haut` | sites Seveso, dont seuil haut (un minimum : le champ est souvent vide) |
| `km_tmd_autoroutes, km_tmd_routes_dep, km_tmd_voies_ferrees` | kilomètres d'axes de transport de matières dangereuses dans la commune |
| `distance_centrale_km, centrale_proche` | distance à vol d'oiseau à la centrale nucléaire la plus proche, et son nom |
| `nb_colleges, nb_colleges_dans_ppri` | collèges de la commune, dont ceux dans un périmètre de PPRI |
| `nb_catnat, nb_catnat_secheresse, nb_catnat_inondations, nb_catnat_mouvement_terrain, nb_catnat_autres` | arrêtés de catastrophe naturelle, en tout et par péril |
| `annee_dernier_catnat, annee_dicrim` | année du dernier événement reconnu ; année du document d'information communal sur les risques (DICRIM), vide si aucun |
| `lat, lon` | centre de la commune |

### `risques_catnat.parquet`, une ligne par arrêté × commune × péril

| Colonne | Ce qu'elle contient |
|---|---|
| `code_insee, commune` | la commune |
| `id_arrete` | identifiant de l'arrêté |
| `code_peril, peril` | péril reconnu : sécheresse, inondations et coulées de boue, mouvement de terrain, remontée de nappe, effondrement |
| `date_debut, date_fin` | dates de l'événement |
| `date_arrete, date_jo` | signature de l'arrêté et publication au Journal officiel |

`risques_communes.geojson` : les 325 communes (WGS 84), `id` = code INSEE.

## À savoir avant de commencer

- un aléa n'est pas un risque : une commune rurale peut être à 100 % en aléa argiles moyen avec peu de maisons. Croisez avec la population
- un périmètre de PPRI n'est pas la zone inondable : c'est le territoire que couvre le plan
- la couche des argiles est incomplète : pour 19 communes, moins de la moitié de la surface a une classe. « 0 % fort » peut vouloir dire « non cartographié »
- les cavités sont recensées là où l'on habite (Orléans en compte 699) : rapportez-les à la population ou à la surface, jamais en nombre brut
- un arrêté CatNat suppose que le maire l'ait demandé : les comptes disent la procédure autant que la catastrophe. La tempête de décembre 1999 pèse 651 décisions à elle seule
- les ICPE comptent aussi des élevages, des carrières et des éoliennes : un nombre d'ICPE n'est pas un risque industriel

## Questions métier possibles

Des pistes, pas une liste à cocher : votre appli en soutient une ou deux, pour la décision ci-dessus.

1. Quels collèges et quelles routes départementales examiner en priorité, selon l'exposition de leur commune ?
2. Comment répartir une enveloppe de prévention entre exposition forte et nombre d'habitants concernés ?
3. Quelles communes accompagner pour leur DICRIM ou leur plan communal de sauvegarde, et sur quel risque ?
4. Comment montrer à un élu la différence entre un risque exposé (aléa, périmètre) et un risque vécu (arrêtés CatNat) ?
5. Les reconnaissances pour sécheresse augmentent-elles, et touchent-elles les mêmes communes ?
6. Quel indicateur composite, lisible et justifié, pour classer les communes ?

## Questions ouvertes sur les données

Des questions précises, à trancher avec le fichier, chiffres à l'appui. Les réponses ne sont pas données : c'est votre première exploration.

1. Quelles sont les 10 communes qui cumulent le plus d'arrêtés CatNat, et qu'ont-elles en commun ?
2. Combien d'habitants vivent dans une commune à plus de 50 % en aléa argiles fort ou moyen ?
3. Combien de collèges sont dans un périmètre de PPRI, et dans quelles communes ?
4. Le nombre de reconnaissances pour sécheresse augmente-t-il depuis 2000 ?
5. Les communes couvertes par un PPRI ont-elles plus souvent un DICRIM que les autres ?
6. Quelles communes cumulent le plus de types de risques à la fois ?

## Pour aller plus loin

- **ML** : regrouper les communes par profil de risque (k-means sur les parts d'aléa, les comptes rapportés à la population, les CatNat)
- **LLM** : une fiche risques par commune pour un élu, à partir des indicateurs affichés
