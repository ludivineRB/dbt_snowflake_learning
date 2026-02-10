# Brief Projet Fil Rouge : API de Scoring Churn Client

## 📋 Contexte du projet

**Entreprise** : TelcoPlus, opérateur télécom avec 7 000 clients
**Problème métier** : Le taux de churn (désabonnement) est de ~26%. Chaque client perdu coûte en moyenne 500€ en acquisition d'un nouveau client. L'entreprise souhaite **prédire le churn** pour cibler les actions de rétention.

**Votre mission** : Construire un système ML complet, de l'exploration des données au déploiement d'une API de scoring, en passant par la modélisation et l'interprétation des résultats.

---

## 🎯 Objectifs pédagogiques

Ce projet couvre **toutes les phases** du parcours ML :

| Phase | Compétence évaluée | Livrable |
|-------|--------------------|----------|
| 0 | Exploration et compréhension des données | Rapport d'audit |
| 1 | Bases mathématiques appliquées | Notebook explicatif |
| 2 | Preprocessing et feature engineering | Pipeline robuste |
| 3 | Modélisation et comparaison | Tableau comparatif |
| 4 | Évaluation rigoureuse | Rapport d'évaluation |
| 5 | Interprétabilité | Explications SHAP |
| 6 | Mise en production | API Dockerisée |

---

## 📊 Dataset

**Fichier** : `data/clients_churn.csv`

Le dataset contient des informations sur les clients d'un opérateur télécom :
- Informations démographiques (genre, senior, partenaire, personnes à charge)
- Informations sur le compte (ancienneté, contrat, facturation, paiement)
- Services souscrits (téléphone, internet, sécurité, streaming...)
- Variable cible : `Churn` (Yes/No)

---

## 📝 Livrables attendus

### Partie 0 : Exploration (Semaines 1-2)

**Livrable** : `notebooks/00-exploration.ipynb`

- [ ] Chargement et description du dataset (shape, dtypes, describe)
- [ ] Analyse des valeurs manquantes (quantification + stratégie)
- [ ] Distribution de la variable cible (déséquilibre ?)
- [ ] Visualisations : histogrammes, countplots, heatmap corrélation
- [ ] Identification des variables les plus corrélées au churn
- [ ] Rapport d'audit en markdown (10-15 lignes)

### Partie 1 : Préparation des données (Semaines 6-8)

**Livrable** : `src/preprocessing.py` + `notebooks/01-preprocessing.ipynb`

- [ ] Traitement des valeurs manquantes (imputation justifiée)
- [ ] Encodage des variables catégorielles (One-Hot / Ordinal selon le cas)
- [ ] Scaling des variables numériques (StandardScaler)
- [ ] Création d'au moins 3 nouvelles features pertinentes
- [ ] Pipeline scikit-learn avec ColumnTransformer
- [ ] **Aucun data leakage** (vérifiable : fit uniquement sur train)
- [ ] Train/test split stratifié (80/20)

### Partie 2 : Modélisation (Semaines 9-11)

**Livrable** : `notebooks/02-modelisation.ipynb`

- [ ] Baseline : Régression Logistique
- [ ] Au moins 4 autres modèles testés (RF, XGBoost, LightGBM, etc.)
- [ ] Tableau comparatif avec au moins 4 métriques
- [ ] Tuning des hyperparamètres sur les 2 meilleurs modèles (GridSearchCV)
- [ ] Justification de la métrique principale choisie
- [ ] Sélection du modèle final argumentée

### Partie 3 : Évaluation (Semaines 12-13)

**Livrable** : `notebooks/03-evaluation.ipynb`

- [ ] Cross-validation (5-fold stratifié) avec scores et écarts-types
- [ ] Matrice de confusion du modèle final
- [ ] Courbe ROC + AUC
- [ ] Courbe Precision-Recall
- [ ] Courbes d'apprentissage (diagnostic overfitting)
- [ ] Analyse du seuil de décision optimal
- [ ] Rapport d'évaluation formaté

### Partie 4 : Interprétabilité (Semaine 14)

**Livrable** : `notebooks/04-interpretabilite.ipynb`

- [ ] Feature importance globale (permutation ou MDI)
- [ ] Analyse SHAP :
  - Summary plot (global)
  - Waterfall plot (3 exemples individuels)
  - Dependence plot (2 features clés)
- [ ] Explication "business-friendly" : pourquoi ce client va-t-il churner ?
- [ ] Identification de 3 leviers d'action pour la rétention

### Partie 5 : Mise en production (Semaines 15-16)

**Livrable** : `src/` + `Dockerfile` + `docker-compose.yml`

- [ ] Sérialisation du modèle (joblib)
- [ ] API FastAPI avec endpoint `POST /predict`
- [ ] Validation des entrées avec Pydantic
- [ ] Endpoint `GET /health`
- [ ] Dockerfile fonctionnel
- [ ] docker-compose.yml
- [ ] Tests de l'API (au moins 3 tests)
- [ ] README avec instructions de lancement

---

## 📐 Structure attendue du projet

```
projet-churn/
├── data/
│   ├── raw/
│   │   └── clients_churn.csv
│   └── processed/
│       └── (généré par le pipeline)
├── notebooks/
│   ├── 00-exploration.ipynb
│   ├── 01-preprocessing.ipynb
│   ├── 02-modelisation.ipynb
│   ├── 03-evaluation.ipynb
│   └── 04-interpretabilite.ipynb
├── src/
│   ├── __init__.py
│   ├── preprocessing.py
│   ├── model.py
│   ├── predict.py
│   └── api.py
├── models/
│   ├── pipeline.joblib
│   └── model_metadata.json
├── tests/
│   ├── test_preprocessing.py
│   ├── test_model.py
│   └── test_api.py
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── README.md
```

---

## 🏆 Critères d'évaluation

| Critère | Points | Détails |
|---------|--------|---------|
| Exploration des données | /10 | Qualité de l'audit, visualisations pertinentes |
| Preprocessing | /15 | Pipeline robuste, pas de leakage, features créées |
| Modélisation | /15 | Comparaison rigoureuse, tuning, choix argumenté |
| Évaluation | /15 | Métriques complètes, cross-validation, diagnostic |
| Interprétabilité | /15 | SHAP, feature importance, explications métier |
| Production | /15 | API fonctionnelle, Docker, tests |
| Qualité du code | /10 | Lisibilité, structure, documentation |
| Présentation orale | /5 | Pitch de 15 min clair et structuré |
| **Total** | **/100** | |

---

## 📅 Planning suggéré

| Semaine | Livrable | Points |
|---------|----------|--------|
| 1-2 | Exploration | 10 |
| 6-8 | Preprocessing | 15 |
| 9-11 | Modélisation | 15 |
| 12-13 | Évaluation | 15 |
| 14 | Interprétabilité | 15 |
| 15-16 | Production + Tests + Présentation | 30 |

---

## 💡 Conseils

- **Commencez simple** : une régression logistique avec 3 features vaut mieux qu'un XGBoost sur un pipeline buggé
- **Versionnez votre travail** : un commit par étape majeure
- **Documentez vos choix** : "J'ai choisi X parce que Y" vaut plus que "J'ai utilisé X"
- **Testez votre API** : un `curl` qui fonctionne vaut mieux qu'un Swagger qui plante
- **Préparez votre pitch** : 15 min, orienté métier, pas technique
