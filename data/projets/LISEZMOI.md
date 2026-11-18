# Les données du projet de vendredi

Six cas, un dossier : les huit fichiers sont ici, dans `data/projets/`, donc déjà dans votre copie du dépôt. Rien à télécharger ailleurs. Un lien de fichier ci-dessous le télécharge seul, si besoin.

```python
import pandas as pd
df = pd.read_parquet("data/projets/energie.parquet")
```

Chaque cas a sa page dans [`projet/cas/`](../../projet/cas/README.md) : le contexte, qui utilise l'appli, la décision, chaque colonne expliquée, les pièges et des questions métier possibles. `summary.json` donne, pour chaque fichier, les colonnes, la période et une ligne réelle.

| Cas | Fichier | Lignes | Période | Source | Licence | Page du cas |
|---|---|---|---|---|---|---|
| 1 · Énergie en Centre-Val de Loire | [`energie.parquet`](https://github.com/jlkhermes38/awp-gabarit/raw/main/data/projets/energie.parquet) (0,98 Mo) | 52 603 demi-heures | 01/09/2023 → 31/08/2026 | [RTE, éCO2mix régional](https://opendata.reseaux-energies.fr/explore/dataset/eco2mix-regional-cons-def/) | Licence Ouverte 2.0 | [01-energie.md](../../projet/cas/01-energie.md) |
| 2 · Sécurité routière dans le Loiret | [`securite_routiere.parquet`](https://github.com/jlkhermes38/awp-gabarit/raw/main/data/projets/securite_routiere.parquet) (0,15 Mo) | 3 242 accidents | 2019 → 2025 | [ONISR, accidents corporels (BAAC)](https://www.data.gouv.fr/datasets/bases-de-donnees-annuelles-des-accidents-corporels-de-la-circulation-routiere-annees-de-2005-a-2025/) | Licence Ouverte 2.0 | [02-securite-routiere.md](../../projet/cas/02-securite-routiere.md) |
| 3 · Immobilier autour d'Orléans | [`immobilier.parquet`](https://github.com/jlkhermes38/awp-gabarit/raw/main/data/projets/immobilier.parquet) (1,73 Mo) | 46 022 ventes | 02/01/2021 → 31/12/2025 | [DVF géolocalisées](https://www.data.gouv.fr/datasets/demandes-de-valeurs-foncieres-geolocalisees/) | Licence Ouverte 2.0 | [03-immobilier.md](../../projet/cas/03-immobilier.md) |
| 4 · Location courte durée à Lyon | [`airbnb_lyon.parquet`](https://github.com/jlkhermes38/awp-gabarit/raw/main/data/projets/airbnb_lyon.parquet) (0,61 Mo), [`airbnb_lyon_reviews.parquet`](https://github.com/jlkhermes38/awp-gabarit/raw/main/data/projets/airbnb_lyon_reviews.parquet) (2,48 Mo) | 9 201 annonces, 20 000 avis | relevé du 19/09/2026 | [Inside Airbnb, Lyon](https://insideairbnb.com/get-the-data/) | CC BY 4.0 | [04-location-courte-duree.md](../../projet/cas/04-location-courte-duree.md) |
| 5 · E-commerce au Brésil | [`olist.parquet`](https://github.com/jlkhermes38/awp-gabarit/raw/main/data/projets/olist.parquet) (5,17 Mo), [`olist_commentaires_negatifs.parquet`](https://github.com/jlkhermes38/awp-gabarit/raw/main/data/projets/olist_commentaires_negatifs.parquet) (1,05 Mo) | 110 189 lignes de commande, 10 890 avis | 15/09/2016 → 29/08/2018 | [Olist sur Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) | CC BY-NC-SA 4.0 | [05-e-commerce.md](../../projet/cas/05-e-commerce.md) |
| 6 · Territoire du Loiret | [`territoire_loiret.parquet`](https://github.com/jlkhermes38/awp-gabarit/raw/main/data/projets/territoire_loiret.parquet) (0,03 Mo) | 325 communes | population 2014 → 2023 | [Département du Loiret, 3 jeux](https://www.data.gouv.fr/organizations/departement-du-loiret/) | Licence Ouverte 2.0 | [06-territoire-loiret.md](../../projet/cas/06-territoire-loiret.md) |

Les licences demandent de citer la source : mettez-la dans le pied de page de votre appli (« Source : RTE, éCO2mix », « Inside Airbnb »…). Olist est sous licence non commerciale : suffisant pour un cours, pas pour un produit.

Le cas 6 joint trois jeux du Département du Loiret sur data.gouv.fr : [population municipale](https://www.data.gouv.fr/datasets/population-municipale-des-communes-departements-du-loiret), [structures de santé](https://www.data.gouv.fr/datasets/structures-de-sante-departement-du-loiret) et [lieux de covoiturage](https://www.data.gouv.fr/datasets/lieux-de-covoiturage-organisation-departement-du-loiret). Les centres des communes viennent de [geo.api.gouv.fr](https://geo.api.gouv.fr).
