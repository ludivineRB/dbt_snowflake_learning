# 🤖 Machine Learning — Du Vrai Zéro à l'Expertise Industrielle

## Vue d'ensemble

Ce module vous emmène du **vrai zéro** jusqu'à la **mise en production** d'un modèle ML. Chaque concept est introduit par le problème qu'il résout, jamais par la formule. La progression suit trois principes :

1. **Le problème avant la solution** : on ne parle jamais d'un outil mathématique avant d'avoir vu le problème qu'il résout
2. **Triple explication** : intuition métier → visualisation → formalisation + code
3. **Ancrage progressif** : chaque concept est réutilisé plusieurs fois avant d'introduire le suivant

## Prérequis

- **Python** : bases, boucles, fonctions, listes/dictionnaires (module 01-Fondamentaux)
- **Pandas basique** : DataFrame, read_csv (module 01-Fondamentaux/Python)
- **Environnement** : Python 3.10+, `uv` installé
- **Aucun prérequis en maths avancées** — tout est construit progressivement

## 📚 Contenu du parcours (12-16 semaines)

### Phase 0 : Comprendre avant de calculer (Semaines 1-2)

| # | Chapitre | Durée | Niveau |
|---|---------|-------|--------|
| 01 | [Qu'est-ce que le ML, vraiment ?](cours/01-quest-ce-que-le-ml.md) | 3h | Débutant |
| 02 | [Anatomie d'un problème ML](cours/02-anatomie-probleme-ml.md) | 3h | Débutant |

### Phase 1 : Les maths comme outils, pas comme punition (Semaines 3-5)

| # | Chapitre | Durée | Niveau |
|---|---------|-------|--------|
| 03 | [Vecteurs, Matrices et KNN](cours/03-vecteurs-matrices-knn.md) | 3h | Débutant |
| 04 | [Fonctions, Erreurs et Gradient Descent](cours/04-fonctions-erreurs-gradient.md) | 4h | Intermédiaire |
| 05 | [Probabilités et Incertitude](cours/05-probabilites-incertitude.md) | 3h | Intermédiaire |

### Phase 2 : La vraie vie des données (Semaines 6-8)

| # | Chapitre | Durée | Niveau |
|---|---------|-------|--------|
| 06 | [Comprendre ses Données](cours/06-comprendre-donnees.md) | 3h | Intermédiaire |
| 07 | [Feature Engineering](cours/07-feature-engineering.md) | 4h | Intermédiaire |
| 08 | [Data Leakage — Le Crime Parfait](cours/08-data-leakage.md) | 3h | Intermédiaire |

### Phase 3 : Les algorithmes, enfin ! (Semaines 9-11)

| # | Chapitre | Durée | Niveau |
|---|---------|-------|--------|
| 09 | [Modèles Linéaires et Logiques](cours/09-modeles-lineaires.md) | 4h | Intermédiaire |
| 10 | [Arbres de Décision et Forêts](cours/10-arbres-forets.md) | 4h | Intermédiaire |
| 11 | [Boosting — Les Champions de Kaggle](cours/11-boosting.md) | 3h | Avancé |

### Phase 4 : Évaluer sérieusement (Semaines 12-13)

| # | Chapitre | Durée | Niveau |
|---|---------|-------|--------|
| 12 | [Métriques — Au-delà de l'Accuracy](cours/12-metriques-classification.md) | 3h | Intermédiaire |
| 13 | [Validation et Généralisation](cours/13-validation-generalisation.md) | 3h | Intermédiaire |

### Phase 5 : Interprétabilité et Éthique (Semaine 14)

| # | Chapitre | Durée | Niveau |
|---|---------|-------|--------|
| 14 | [Interpréter ses Modèles et Éthique](cours/14-interpretabilite-ethique.md) | 4h | Avancé |

### Phase 6 : Production et MLOps (Semaines 15-16)

| # | Chapitre | Durée | Niveau |
|---|---------|-------|--------|
| 15 | [Du Notebook à l'API](cours/15-notebook-api.md) | 4h | Avancé |
| 16 | [Docker, Monitoring et MLOps](cours/16-docker-monitoring.md) | 4h | Avancé |

| - | [Cheatsheet ML](cours/CHEATSHEET-ml.md) | - | Référence |

**Durée totale estimée : ~50 heures** (cours + exercices + projet)

## 🗺️ Progression recommandée

```
 PHASE 0 : COMPRENDRE              PHASE 1 : LES MATHS UTILES
┌──────────────┐                   ┌──────────────┐
│  Chapitre 01 │                   │  Chapitre 03 │
│  Qu'est-ce   │──────────────────▶│  Vecteurs &  │
│  que le ML ? │                   │  KNN         │
└──────┬───────┘                   └──────┬───────┘
       │                                  │
       ▼                                  ▼
┌──────────────┐                   ┌──────────────┐
│  Chapitre 02 │                   │  Chapitre 04 │
│  Anatomie    │──────────────────▶│  Erreurs &   │
│  problème ML │                   │  Gradient    │
└──────────────┘                   └──────┬───────┘
                                          │
                                          ▼
                                   ┌──────────────┐
                                   │  Chapitre 05 │
                                   │  Probabilités│
                                   └──────┬───────┘
                                          │
       ┌──────────────────────────────────┘
       ▼
 PHASE 2 : LES DONNÉES             PHASE 3 : LES ALGORITHMES
┌──────────────┐                   ┌──────────────┐
│  Chapitre 06 │                   │  Chapitre 09 │
│  Comprendre  │──────────────────▶│  Modèles     │
│  les données │                   │  linéaires   │
└──────┬───────┘                   └──────┬───────┘
       │                                  │
       ▼                                  ▼
┌──────────────┐                   ┌──────────────┐
│  Chapitre 07 │                   │  Chapitre 10 │
│  Feature     │                   │  Arbres &    │
│  Engineering │                   │  Forêts      │
└──────┬───────┘                   └──────┬───────┘
       │                                  │
       ▼                                  ▼
┌──────────────┐                   ┌──────────────┐
│  Chapitre 08 │                   │  Chapitre 11 │
│  Data        │──────────────────▶│  Boosting    │
│  Leakage     │                   │              │
└──────────────┘                   └──────┬───────┘
                                          │
       ┌──────────────────────────────────┘
       ▼
 PHASE 4 : ÉVALUER                 PHASE 5-6 : PRODUCTION
┌──────────────┐                   ┌──────────────┐
│  Chapitre 12 │                   │  Chapitre 14 │
│  Métriques   │──────────────────▶│Interprétabi- │
│              │                   │  lité        │
└──────┬───────┘                   └──────┬───────┘
       │                                  │
       ▼                                  ▼
┌──────────────┐                   ┌──────────────┐
│  Chapitre 13 │                   │  Chapitre 15 │
│  Validation  │                   │  API         │
│              │──────────────────▶│  Production  │
└──────────────┘                   └──────┬───────┘
                                          │
                                          ▼
                                   ┌──────────────┐
                                   │  Chapitre 16 │
                                   │  Docker &    │
                                   │  Monitoring  │
                                   └──────────────┘
```

## 📅 Planning suggéré

```
Semaine 1-2 : Phase 0 — Comprendre (~6h)
├── Chapitre 01 - Qu'est-ce que le ML ? (3h)
└── Chapitre 02 - Anatomie d'un problème ML (3h)

Semaine 3-5 : Phase 1 — Maths utiles (~10h)
├── Chapitre 03 - Vecteurs, Matrices, KNN (3h)
├── Chapitre 04 - Fonctions, Erreurs, Gradient (4h)
└── Chapitre 05 - Probabilités (3h)

Semaine 6-8 : Phase 2 — Les données (~10h)
├── Chapitre 06 - Comprendre les données (3h)
├── Chapitre 07 - Feature Engineering (4h)
└── Chapitre 08 - Data Leakage (3h)

Semaine 9-11 : Phase 3 — Les algorithmes (~11h)
├── Chapitre 09 - Modèles linéaires (4h)
├── Chapitre 10 - Arbres et Forêts (4h)
└── Chapitre 11 - Boosting (3h)

Semaine 12-13 : Phase 4 — Évaluation (~6h)
├── Chapitre 12 - Métriques (3h)
└── Chapitre 13 - Validation (3h)

Semaine 14 : Phase 5 — Interprétabilité (~4h)
└── Chapitre 14 - Interpréter et éthique (4h)

Semaine 15-16 : Phase 6 — Production (~8h)
├── Chapitre 15 - Du notebook à l'API (4h)
└── Chapitre 16 - Docker et monitoring (4h)
```

## 🎯 Projet fil rouge : Scoring de Churn Client

Utilisé tout au long du parcours sur le dataset [Telco Churn](data/clients_churn.csv) :

| Phase | Utilisation du projet |
|-------|----------------------|
| Phase 0 | Exploration et compréhension des données |
| Phase 1 | Calcul de distances, régression simple |
| Phase 2 | Nettoyage, feature engineering, pipeline |
| Phase 3 | Modélisation et comparaison d'algorithmes |
| Phase 4 | Évaluation rigoureuse et validation |
| Phase 5 | Explication des prédictions (SHAP) |
| Phase 6 | API de scoring en production |

## 📂 Structure du module

```
08-Machine-Learning/
├── README.md                          ← Vous êtes ici
├── cours/                             ← 16 chapitres + cheatsheet
│   ├── 01-quest-ce-que-le-ml.md
│   ├── 02-anatomie-probleme-ml.md
│   ├── ...
│   ├── 16-docker-monitoring.md
│   └── CHEATSHEET-ml.md
├── notebooks/                         ← Notebooks interactifs
│   ├── 01-regression-prix-immobilier.ipynb
│   ├── 02-classification-churn-client.ipynb
│   └── 03-clustering-produits.ipynb
├── exercices/                         ← Exercices pratiques
│   ├── exercice-01-exploration-donnees.md
│   ├── exercice-02-maths-knn.md
│   ├── exercice-03-preprocessing-pipeline.md
│   ├── exercice-04-comparaison-modeles.md
│   └── exercice-05-evaluation-complete.md
├── briefs/                            ← Projet fil rouge
│   └── brief-churn-scoring.md
├── data/                              ← Datasets
│   ├── clients_churn.csv
│   ├── house_prices.csv
│   └── produits_clustering.csv
└── images/                            ← Diagrammes et visuels
```

## 🔗 Ressources complémentaires

- [Cheatsheet ML](cours/CHEATSHEET-ml.md) — Aide-mémoire à garder sous la main
- [Documentation scikit-learn](https://scikit-learn.org/stable/)
- [Documentation XGBoost](https://xgboost.readthedocs.io/)
- [Documentation SHAP](https://shap.readthedocs.io/)
- [Documentation FastAPI](https://fastapi.tiangolo.com/)
- [Documentation MLflow](https://mlflow.org/docs/latest/)

## ✨ Ce qui différencie ce cours

- **Zéro jargon non expliqué** — chaque terme est défini par l'usage avant la théorie
- **Maths introduites au moment du besoin** — pas de chapitre "prérequis maths" isolé
- **Triple progression** : intuition → visualisation → code
- **Ancré dans la production** — pas que de la théorie, un vrai déploiement
- **Projet fil rouge réaliste** du début à la fin sur le même dataset
