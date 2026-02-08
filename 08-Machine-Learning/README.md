# Machine Learning

## Vue d'ensemble

Ce module couvre le Machine Learning de A à Z : des fondamentaux théoriques jusqu'à la mise en production avec MLOps. Chaque chapitre combine théorie, code pratique et conseils issus de projets réels. L'objectif est de vous rendre autonome pour entraîner, évaluer et déployer des modèles ML en conditions professionnelles.

## Prérequis

- **Python** : POO, NumPy, Pandas (module 01-Fondamentaux)
- **SQL basique** : SELECT, JOIN, GROUP BY (module 05-Databases)
- **Environnement** : `uv` installé, Python 3.10+

## Contenu

| # | Chapitre | Durée | Niveau | Description |
|---|---------|-------|--------|-------------|
| 01 | [Introduction au ML](cours/01-introduction-ml.md) | 2h | Débutant | Définitions, types d'apprentissage, workflow ML, vocabulaire |
| 02 | [Environnement & Setup](cours/02-environnement-setup.md) | 1h | Débutant | Installation uv, scikit-learn, Jupyter, structure de projet |
| 03 | [Preprocessing](cours/03-preprocessing.md) | 2h | Débutant | Nettoyage, valeurs manquantes, normalisation, encodage |
| 04 | [Régression](cours/04-regression.md) | 2h30 | Intermédiaire | Régression linéaire, Ridge, Lasso, métriques de régression |
| 05 | [Classification](cours/05-classification.md) | 2h30 | Intermédiaire | Logistique, arbres de décision, SVM, KNN, métriques |
| 06 | [Méthodes d'Ensemble](cours/06-ensemble-methods.md) | 2h | Intermédiaire | Random Forest, Bagging, Boosting, XGBoost, LightGBM |
| 07 | [Clustering](cours/07-clustering.md) | 2h | Intermédiaire | KMeans, DBSCAN, hiérarchique, évaluation sans labels |
| 08 | [Évaluation & Métriques](cours/08-evaluation-metriques.md) | 2h | Intermédiaire | Cross-validation, overfitting, courbes ROC, matrice de confusion |
| 09 | [Feature Engineering](cours/09-feature-engineering.md) | 2h30 | Avancé | Création de features, sélection, PCA, pipelines sklearn |
| 10 | [MLOps & Production](cours/10-mlops-production.md) | 3h | Avancé | MLflow, FastAPI, Docker, CI/CD, monitoring, data drift |
| - | [Cheatsheet ML](cours/CHEATSHEET-ml.md) | - | Référence | Aide-mémoire : algorithmes, métriques, commandes, erreurs courantes |

**Durée totale cours :** ~22 heures

## Progression recommandée

```
 FONDAMENTAUX               MODÈLES SUPERVISÉS           MODÈLES NON-SUPERVISÉS
┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  Module 01   │─►│  Module 02   │─►│  Module 03   │  │  Module 07   │
│ Introduction │  │    Setup     │  │ Preprocessing│  │  Clustering  │
└──────────────┘  └──────────────┘  └──────┬───────┘  └──────────────┘
                                           │                  ▲
                                           ▼                  │
                                    ┌──────────────┐          │
                                    │  Module 04   │          │
                                    │  Régression  │          │
                                    └──────┬───────┘          │
                                           │                  │
                                           ▼                  │
                                    ┌──────────────┐          │
                                    │  Module 05   │──────────┘
                                    │Classification│
                                    └──────┬───────┘
                                           │
                                           ▼
 AVANCÉ                      ┌──────────────┐
┌──────────────┐             │  Module 06   │
│  Module 09   │◄────────────│  Ensemble    │
│  Features    │             └──────────────┘
└──────┬───────┘
       │         ┌──────────────┐
       │         │  Module 08   │
       ├────────►│  Évaluation  │
       │         └──────────────┘
       ▼
┌──────────────┐  ┌──────────────┐
│  Module 10   │─►│  Cheatsheet  │
│    MLOps     │  │   Référence  │
└──────────────┘  └──────────────┘
```

## Planning suggéré (semaine type)

```
Jour 1 : Fondamentaux (~5h)
├── Module 01 - Introduction au ML (2h)
├── Module 02 - Environnement & Setup (1h)
└── Module 03 - Preprocessing (2h)

Jour 2 : Modèles supervisés (~5h)
├── Module 04 - Régression (2h30)
└── Module 05 - Classification (2h30)

Jour 3 : Méthodes avancées (~4h)
├── Module 06 - Méthodes d'Ensemble (2h)
└── Module 07 - Clustering (2h)

Jour 4 : Évaluation et Features (~4h30)
├── Module 08 - Évaluation & Métriques (2h)
└── Module 09 - Feature Engineering (2h30)

Jour 5 : Production (~3h + pratique)
├── Module 10 - MLOps & Production (3h)
└── Projet pratique / Brief
```

## Ressources complémentaires

- [Cheatsheet ML](cours/CHEATSHEET-ml.md) - Aide-mémoire à garder sous la main
- [Documentation scikit-learn](https://scikit-learn.org/stable/)
- [Documentation MLflow](https://mlflow.org/docs/latest/)
- [Documentation FastAPI](https://fastapi.tiangolo.com/)
