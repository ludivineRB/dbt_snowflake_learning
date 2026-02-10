# Chapitre 15 : Du Notebook à l'API — Mettre en Production

## 🎯 Objectifs

- Comprendre le **gap** entre un notebook Jupyter et un code de production
- Maîtriser la **sérialisation** des modèles (pickle, joblib, ONNX)
- Savoir structurer un **projet ML** professionnel
- Construire une **API de prédiction** avec FastAPI
- Écrire des **tests unitaires** pour le preprocessing et l'API
- Réaliser un TP complet : API de scoring churn en local

> **Phase 6 - Semaine 15**

---

## 1. 🧠 Le gap Notebook vers Production

### 1.1 Pourquoi un notebook ne suffit pas

Un notebook Jupyter est parfait pour l'**exploration** et le **prototypage**. Mais il est **inadapté** à la production.

```
NOTEBOOK (Exploration)              PRODUCTION (Déploiement)
┌─────────────────────┐            ┌─────────────────────┐
│ Code spaghetti      │            │ Code modulaire      │
│ Variables globales  │            │ Fonctions/Classes   │
│ Pas de tests        │     →      │ Tests unitaires     │
│ Pas de versioning   │            │ Git + CI/CD         │
│ Dépendances floues  │            │ requirements.txt    │
│ Exécution manuelle  │            │ API automatisée     │
│ "Ça marche chez moi"│            │ Docker = partout    │
└─────────────────────┘            └─────────────────────┘
```

### 1.2 Les problèmes classiques du notebook

| Problème | Exemple | Solution |
|----------|---------|----------|
| **Ordre d'exécution** | Cellule 15 dépend de cellule 3 qu'on a modifiée | Modules Python |
| **Variables globales** | `df` modifié à 10 endroits différents | Fonctions pures |
| **Pas de tests** | On ne sait pas si le code marche encore | pytest |
| **Pas de gestion d'erreurs** | Le notebook crash sur une donnée inattendue | try/except, validation |
| **Non reproductible** | "Kernel > Restart and Run All" échoue | Pipeline reproductible |
| **Non déployable** | On ne peut pas exposer un notebook en API | FastAPI, Flask |

> 💡 **Conseil** : "Le notebook est votre **brouillon**. Le code de production est votre **copie propre**. Ne déployez jamais un brouillon."

---

## 2. 💾 Sérialisation du modèle

### 2.1 Pickle : simple mais dangereux

```python
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# --- Entraîner ---
cancer = load_breast_cancer()
X_train, X_test, y_train, y_test = train_test_split(
    cancer.data, cancer.target, test_size=0.2, random_state=42
)

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('model', RandomForestClassifier(n_estimators=100, random_state=42))
])
pipeline.fit(X_train, y_train)

# --- Sauvegarder avec pickle ---
with open('model_v1.pkl', 'wb') as f:
    pickle.dump(pipeline, f)

# --- Charger ---
with open('model_v1.pkl', 'rb') as f:
    pipeline_loaded = pickle.load(f)

y_pred = pipeline_loaded.predict(X_test)
print(f"Score après chargement : {pipeline_loaded.score(X_test, y_test):.4f}")
```

> ⚠️ **Attention** : "Pickle est **dangereux** d'un point de vue sécurité. Ne chargez **JAMAIS** un fichier pickle provenant d'une source non fiable : il peut exécuter du code arbitraire à l'ouverture. Utilisez-le uniquement pour vos propres modèles."

### 2.2 Joblib : optimisé pour numpy/sklearn

Joblib est plus **efficace** que pickle pour les objets contenant de grands tableaux numpy (comme les modèles sklearn).

```python
import joblib

# --- Sauvegarder avec joblib ---
joblib.dump(pipeline, 'model_v1.joblib')

# --- Charger ---
pipeline_loaded = joblib.load('model_v1.joblib')

y_pred = pipeline_loaded.predict(X_test)
print(f"Score après chargement : {pipeline_loaded.score(X_test, y_test):.4f}")
```

| Critère | pickle | joblib |
|---------|--------|--------|
| **Vitesse (gros modèles)** | Lent | Rapide |
| **Taille fichier** | Plus gros | Plus compact |
| **Compression** | Non | Oui (optionnel) |
| **Sécurité** | Dangereux | Dangereux aussi |
| **Recommandé pour sklearn** | Non | **Oui** |

```python
# Joblib avec compression
joblib.dump(pipeline, 'model_v1_compressed.joblib', compress=3)
```

### 2.3 ONNX : interopérabilité

ONNX (Open Neural Network Exchange) est un format **universel** qui permet de charger un modèle dans n'importe quel langage (Python, Java, C++, JavaScript...).

```python
# Installation
# pip install skl2onnx onnxruntime

from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType
import onnxruntime as rt
import numpy as np

# --- Convertir en ONNX ---
initial_type = [('float_input', FloatTensorType([None, X_train.shape[1]]))]
onnx_model = convert_sklearn(pipeline, initial_types=initial_type)

# --- Sauvegarder ---
with open('model_v1.onnx', 'wb') as f:
    f.write(onnx_model.SerializeToString())

# --- Charger et prédire avec ONNX Runtime ---
session = rt.InferenceSession('model_v1.onnx')
input_name = session.get_inputs()[0].name

# Prédire
y_pred_onnx = session.run(
    None,
    {input_name: X_test.astype(np.float32)}
)[0]
print(f"Prédictions identiques : {(y_pred_onnx == pipeline.predict(X_test)).all()}")
```

### 2.4 Versioning du modèle + pipeline

```python
import joblib
from datetime import datetime

# --- Bonne pratique : sauvegarder le pipeline COMPLET ---
# (preprocessing + modèle ensemble)
metadata = {
    'model': pipeline,
    'version': '1.0.0',
    'date': datetime.now().isoformat(),
    'features': list(cancer.feature_names),
    'metrics': {
        'f1_test': 0.97,
        'accuracy_test': 0.96
    },
    'training_params': {
        'n_samples': X_train.shape[0],
        'random_state': 42
    }
}

joblib.dump(metadata, f"model_v{metadata['version']}_{datetime.now():%Y%m%d}.joblib")
```

> 💡 **Conseil** : "Sauvegardez **toujours** le pipeline complet (scaler + modèle) et non le modèle seul. Sinon, vous devrez recréer le scaler à chaque chargement, et les résultats seront différents si le scaler n'est pas exactement le même."

---

## 3. 📁 Structure d'un projet ML

### 3.1 Structure recommandée

```
projet-ml-churn/
├── data/
│   ├── raw/                    # Données brutes (jamais modifiées)
│   │   └── clients.csv
│   └── processed/              # Données transformées
│       └── clients_clean.csv
├── notebooks/
│   ├── 01_exploration.ipynb    # EDA
│   ├── 02_modelisation.ipynb   # Expérimentations
│   └── 03_evaluation.ipynb     # Évaluation finale
├── src/
│   ├── __init__.py
│   ├── preprocessing.py        # Fonctions de nettoyage/transformation
│   ├── model.py                # Entraînement et évaluation
│   ├── predict.py              # Prédiction sur nouvelles données
│   └── api.py                  # API FastAPI
├── tests/
│   ├── test_preprocessing.py   # Tests du preprocessing
│   └── test_model.py           # Tests du modèle
├── models/                     # Modèles sérialisés
│   └── model_v1.0.0.joblib
├── Dockerfile
├── pyproject.toml              # Dépendances et config
└── README.md
```

### 3.2 Pourquoi cette structure ?

| Dossier | Rôle | Règle |
|---------|------|-------|
| `data/raw/` | Données originales | **Jamais** modifiées |
| `data/processed/` | Données transformées | Reproductibles via le code |
| `notebooks/` | Exploration | Ne pas déployer |
| `src/` | Code de production | Modulaire, testé |
| `tests/` | Tests unitaires | Exécutés à chaque commit |
| `models/` | Modèles sérialisés | Versionnés |

---

## 4. 🔧 Refactoring du notebook en modules Python

### 4.1 Extraire le preprocessing

```python
# src/preprocessing.py

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from typing import Tuple


def charger_donnees(chemin: str) -> pd.DataFrame:
    """Charge les données brutes depuis un fichier CSV."""
    df = pd.read_csv(chemin)
    print(f"Données chargées : {df.shape[0]} lignes, {df.shape[1]} colonnes")
    return df


def nettoyer_donnees(df: pd.DataFrame) -> pd.DataFrame:
    """Nettoie les données : valeurs manquantes, doublons, types."""
    df = df.copy()

    # Supprimer les doublons
    n_doublons = df.duplicated().sum()
    if n_doublons > 0:
        df = df.drop_duplicates()
        print(f"  {n_doublons} doublons supprimés")

    # Remplir les valeurs manquantes
    for col in df.select_dtypes(include=[np.number]).columns:
        if df[col].isnull().sum() > 0:
            mediane = df[col].median()
            df[col] = df[col].fillna(mediane)
            print(f"  {col} : NaN remplis par la médiane ({mediane:.2f})")

    return df


def preparer_features(
    df: pd.DataFrame,
    target_col: str,
    scaler: StandardScaler = None
) -> Tuple[np.ndarray, np.ndarray, StandardScaler, list]:
    """Prépare les features et la target pour l'entraînement."""
    # Séparer features et target
    feature_cols = [c for c in df.select_dtypes(include=[np.number]).columns if c != target_col]
    X = df[feature_cols].values
    y = df[target_col].values

    # Scaler
    if scaler is None:
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
    else:
        X_scaled = scaler.transform(X)

    return X_scaled, y, scaler, feature_cols
```

### 4.2 Extraire le modèle

```python
# src/model.py

import joblib
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import cross_val_score
from sklearn.metrics import f1_score, classification_report
from datetime import datetime


def entrainer_modele(
    X_train: np.ndarray,
    y_train: np.ndarray,
    **params
) -> GradientBoostingClassifier:
    """Entraîne un Gradient Boosting Classifier."""
    default_params = {
        'n_estimators': 100,
        'max_depth': 3,
        'learning_rate': 0.1,
        'random_state': 42
    }
    default_params.update(params)

    model = GradientBoostingClassifier(**default_params)
    model.fit(X_train, y_train)
    return model


def evaluer_modele(model, X_test, y_test) -> dict:
    """Évalue le modèle et retourne un dictionnaire de métriques."""
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    metrics = {
        'f1': f1_score(y_test, y_pred),
        'accuracy': (y_pred == y_test).mean(),
    }

    print("=== Évaluation ===")
    print(classification_report(y_test, y_pred))
    return metrics


def sauvegarder_modele(model, scaler, feature_cols, metrics, version, path):
    """Sauvegarde le modèle avec ses métadonnées."""
    artefact = {
        'model': model,
        'scaler': scaler,
        'feature_cols': feature_cols,
        'version': version,
        'date': datetime.now().isoformat(),
        'metrics': metrics
    }
    joblib.dump(artefact, path)
    print(f"Modèle sauvegardé : {path}")


def charger_modele(path):
    """Charge un modèle et ses métadonnées."""
    artefact = joblib.load(path)
    print(f"Modèle v{artefact['version']} chargé (date : {artefact['date']})")
    return artefact
```

### 4.3 Écrire des tests unitaires simples

```python
# tests/test_preprocessing.py

import pytest
import pandas as pd
import numpy as np
from src.preprocessing import nettoyer_donnees, preparer_features


def test_nettoyer_donnees_supprime_doublons():
    """Vérifie que les doublons sont supprimés."""
    df = pd.DataFrame({
        'a': [1, 2, 2, 3],
        'b': [4, 5, 5, 6]
    })
    result = nettoyer_donnees(df)
    assert result.shape[0] == 3  # 1 doublon supprimé


def test_nettoyer_donnees_remplit_nan():
    """Vérifie que les NaN sont remplis par la médiane."""
    df = pd.DataFrame({
        'a': [1.0, 2.0, np.nan, 4.0],
        'b': [10, 20, 30, 40]
    })
    result = nettoyer_donnees(df)
    assert result['a'].isnull().sum() == 0
    assert result['a'].iloc[2] == 2.0  # Médiane de [1, 2, 4]


def test_preparer_features_shape():
    """Vérifie les dimensions de sortie."""
    df = pd.DataFrame({
        'feat1': [1.0, 2.0, 3.0],
        'feat2': [4.0, 5.0, 6.0],
        'target': [0, 1, 0]
    })
    X, y, scaler, cols = preparer_features(df, target_col='target')
    assert X.shape == (3, 2)
    assert y.shape == (3,)
    assert len(cols) == 2


def test_preparer_features_standardise():
    """Vérifie que les features sont standardisées."""
    df = pd.DataFrame({
        'feat1': [10.0, 20.0, 30.0, 40.0, 50.0],
        'target': [0, 1, 0, 1, 0]
    })
    X, y, scaler, cols = preparer_features(df, target_col='target')
    assert abs(X.mean()) < 1e-10  # Moyenne ~ 0
    assert abs(X.std(ddof=0) - 1.0) < 1e-10  # Écart-type ~ 1
```

```python
# tests/test_model.py

import pytest
import numpy as np
from src.model import entrainer_modele, evaluer_modele


def test_entrainer_modele():
    """Vérifie que le modèle s'entraîne sans erreur."""
    X = np.random.rand(100, 5)
    y = (X[:, 0] > 0.5).astype(int)
    model = entrainer_modele(X, y, n_estimators=10)
    assert hasattr(model, 'predict')


def test_prediction_shape():
    """Vérifie que les prédictions ont la bonne forme."""
    X_train = np.random.rand(100, 5)
    y_train = (X_train[:, 0] > 0.5).astype(int)
    X_test = np.random.rand(20, 5)

    model = entrainer_modele(X_train, y_train, n_estimators=10)
    y_pred = model.predict(X_test)
    assert y_pred.shape == (20,)
    assert set(y_pred).issubset({0, 1})
```

Exécuter les tests :

```bash
# Depuis la racine du projet
pytest tests/ -v
```

---

## 5. 🚀 API avec FastAPI

### 5.1 Pourquoi FastAPI

| Critère | FastAPI | Flask | Django |
|---------|---------|-------|--------|
| **Performance** | Très rapide (async) | Correcte | Lourde |
| **Validation** | Automatique (Pydantic) | Manuelle | Manuelle |
| **Documentation** | Auto (Swagger + ReDoc) | Manuelle | Manuelle |
| **Type hints** | Natif | Non | Partiel |
| **Idéal pour** | API ML | API simple | App web complète |

### 5.2 Code complet de l'API

```python
# src/api.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
import joblib
import numpy as np

# --- Initialiser l'application ---
app = FastAPI(
    title="API de Prédiction Churn",
    description="Prédit si un client va quitter le service (churn)",
    version="1.0.0"
)

# --- Charger le modèle au démarrage ---
MODEL_PATH = "models/model_v1.0.0.joblib"

try:
    artefact = joblib.load(MODEL_PATH)
    model = artefact['model']
    scaler = artefact['scaler']
    feature_cols = artefact['feature_cols']
    print(f"Modèle v{artefact['version']} chargé avec succès")
except FileNotFoundError:
    print(f"ERREUR : Modèle non trouvé à {MODEL_PATH}")
    model = None


# --- Schémas de données (Pydantic) ---
class ClientInput(BaseModel):
    """Données d'un client pour prédire le churn."""
    anciennete_mois: float = Field(..., ge=0, description="Ancienneté en mois")
    montant_mensuel: float = Field(..., ge=0, description="Montant mensuel en euros")
    nb_reclamations: int = Field(..., ge=0, description="Nombre de réclamations")
    nb_produits: int = Field(..., ge=1, le=10, description="Nombre de produits souscrits")
    satisfaction: float = Field(..., ge=1, le=5, description="Score de satisfaction (1-5)")

    class Config:
        json_schema_extra = {
            "example": {
                "anciennete_mois": 24.0,
                "montant_mensuel": 59.99,
                "nb_reclamations": 2,
                "nb_produits": 3,
                "satisfaction": 3.5
            }
        }


class PredictionOutput(BaseModel):
    """Résultat de la prédiction."""
    churn: bool
    probabilite_churn: float
    confidence: str


class BatchInput(BaseModel):
    """Lot de clients pour prédiction en masse."""
    clients: List[ClientInput]


class BatchOutput(BaseModel):
    """Résultats pour un lot de clients."""
    predictions: List[PredictionOutput]
    nb_clients: int


# --- Endpoints ---
@app.get("/")
def root():
    """Page d'accueil de l'API."""
    return {
        "message": "API de prédiction Churn",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    """Vérifie que l'API et le modèle fonctionnent."""
    if model is None:
        raise HTTPException(status_code=503, detail="Modèle non chargé")
    return {"status": "healthy", "model_version": artefact.get('version', 'unknown')}


@app.post("/predict", response_model=PredictionOutput)
def predict(client: ClientInput):
    """Prédit le churn pour un client."""
    if model is None:
        raise HTTPException(status_code=503, detail="Modèle non disponible")

    # Transformer en array numpy
    features = np.array([[
        client.anciennete_mois,
        client.montant_mensuel,
        client.nb_reclamations,
        client.nb_produits,
        client.satisfaction
    ]])

    # Scaler + prédire
    features_scaled = scaler.transform(features)
    proba = model.predict_proba(features_scaled)[0]
    churn = bool(proba[1] > 0.5)

    # Niveau de confiance
    confidence_score = max(proba)
    if confidence_score > 0.8:
        confidence = "haute"
    elif confidence_score > 0.6:
        confidence = "moyenne"
    else:
        confidence = "faible"

    return PredictionOutput(
        churn=churn,
        probabilite_churn=round(float(proba[1]), 4),
        confidence=confidence
    )


@app.post("/predict/batch", response_model=BatchOutput)
def predict_batch(batch: BatchInput):
    """Prédit le churn pour un lot de clients."""
    if model is None:
        raise HTTPException(status_code=503, detail="Modèle non disponible")

    predictions = []
    for client in batch.clients:
        prediction = predict(client)
        predictions.append(prediction)

    return BatchOutput(
        predictions=predictions,
        nb_clients=len(predictions)
    )
```

### 5.3 Lancer l'API

```bash
# Installation
pip install fastapi uvicorn

# Lancer le serveur
uvicorn src.api:app --reload --host 0.0.0.0 --port 8000
```

### 5.4 Tester avec curl et Swagger

```bash
# --- Test du health check ---
curl http://localhost:8000/health

# --- Test de prédiction ---
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "anciennete_mois": 6.0,
    "montant_mensuel": 89.99,
    "nb_reclamations": 5,
    "nb_produits": 1,
    "satisfaction": 1.5
  }'

# Réponse :
# {
#   "churn": true,
#   "probabilite_churn": 0.8234,
#   "confidence": "haute"
# }
```

La documentation **Swagger** est automatiquement disponible à `http://localhost:8000/docs`. Elle permet de tester l'API directement depuis le navigateur.

```
Documentation automatique :

┌─────────────────────────────────────────────┐
│  API de Prédiction Churn                    │
│  Version 1.0.0                              │
├─────────────────────────────────────────────┤
│                                             │
│  GET  /          Page d'accueil             │
│  GET  /health    Health check               │
│  POST /predict   Prédiction unitaire        │
│  POST /predict/batch  Prédiction en masse   │
│                                             │
│  Chaque endpoint est documenté avec :       │
│  - Schéma d'entrée (avec exemples)          │
│  - Schéma de sortie                         │
│  - Bouton "Try it out" pour tester          │
│                                             │
└─────────────────────────────────────────────┘
```

> 💡 **Conseil** : "Ajoutez toujours un endpoint `/health` à votre API. C'est indispensable pour que les orchestrateurs (Kubernetes, Docker) vérifient que votre service est opérationnel."

---

## 6. 🧪 Tests de l'API

### 6.1 Tests avec pytest + httpx

```python
# tests/test_api.py

import pytest
from fastapi.testclient import TestClient
from src.api import app

client = TestClient(app)


def test_root():
    """Teste la page d'accueil."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health():
    """Teste le health check."""
    response = client.get("/health")
    # 200 si le modèle est chargé, 503 sinon
    assert response.status_code in [200, 503]


def test_predict_valid():
    """Teste une prédiction avec des données valides."""
    payload = {
        "anciennete_mois": 24.0,
        "montant_mensuel": 59.99,
        "nb_reclamations": 2,
        "nb_produits": 3,
        "satisfaction": 3.5
    }
    response = client.post("/predict", json=payload)

    # Si le modèle est chargé
    if response.status_code == 200:
        data = response.json()
        assert "churn" in data
        assert "probabilite_churn" in data
        assert "confidence" in data
        assert isinstance(data["churn"], bool)
        assert 0 <= data["probabilite_churn"] <= 1


def test_predict_invalid_data():
    """Teste une prédiction avec des données invalides."""
    payload = {
        "anciennete_mois": -5,  # Négatif → invalide
        "montant_mensuel": 59.99,
        "nb_reclamations": 2,
        "nb_produits": 3,
        "satisfaction": 3.5
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422  # Validation error


def test_predict_missing_field():
    """Teste une prédiction avec un champ manquant."""
    payload = {
        "anciennete_mois": 24.0,
        # montant_mensuel manquant !
        "nb_reclamations": 2,
        "nb_produits": 3,
        "satisfaction": 3.5
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422


def test_predict_batch():
    """Teste la prédiction en lot."""
    payload = {
        "clients": [
            {
                "anciennete_mois": 24.0,
                "montant_mensuel": 59.99,
                "nb_reclamations": 2,
                "nb_produits": 3,
                "satisfaction": 3.5
            },
            {
                "anciennete_mois": 3.0,
                "montant_mensuel": 99.99,
                "nb_reclamations": 8,
                "nb_produits": 1,
                "satisfaction": 1.0
            }
        ]
    }
    response = client.post("/predict/batch", json=payload)
    if response.status_code == 200:
        data = response.json()
        assert data["nb_clients"] == 2
        assert len(data["predictions"]) == 2
```

```bash
# Exécuter les tests
pytest tests/test_api.py -v
```

---

## 7. 🧪 TP : API de scoring churn en local

### 7.1 Le livrable

Créez un projet complet avec la structure vue en section 3. Le projet doit :

1. Charger et préparer un dataset de churn (vous pouvez le simuler)
2. Entraîner un modèle dans un notebook
3. Refactorer le code en modules (`src/`)
4. Sérialiser le modèle avec joblib
5. Exposer une API FastAPI avec les endpoints `/health`, `/predict` et `/predict/batch`
6. Écrire au moins 5 tests unitaires

### 7.2 Script d'entraînement complet

```python
# scripts/train.py

"""Script d'entraînement du modèle de churn."""

import sys
sys.path.insert(0, '.')

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from src.preprocessing import nettoyer_donnees, preparer_features
from src.model import entrainer_modele, evaluer_modele, sauvegarder_modele


def generer_donnees_churn(n=2000):
    """Génère un dataset synthétique de churn."""
    np.random.seed(42)

    df = pd.DataFrame({
        'anciennete_mois': np.random.exponential(24, n).clip(1, 120).astype(int),
        'montant_mensuel': np.random.normal(60, 25, n).clip(10, 200),
        'nb_reclamations': np.random.poisson(2, n),
        'nb_produits': np.random.choice([1, 2, 3, 4, 5], n, p=[0.3, 0.3, 0.2, 0.15, 0.05]),
        'satisfaction': np.random.uniform(1, 5, n).round(1),
    })

    # Simuler le churn
    score = (
        -0.02 * df['anciennete_mois'] +
        0.01 * df['montant_mensuel'] +
        0.15 * df['nb_reclamations'] +
        -0.1 * df['nb_produits'] +
        -0.3 * df['satisfaction'] +
        np.random.normal(0, 0.5, n)
    )
    df['churn'] = (score > np.percentile(score, 70)).astype(int)

    return df


def main():
    # 1. Générer les données
    print("=== Génération des données ===")
    df = generer_donnees_churn()
    print(f"Shape : {df.shape}")
    print(f"Taux de churn : {df['churn'].mean():.2%}")

    # 2. Nettoyer
    print("\n=== Nettoyage ===")
    df = nettoyer_donnees(df)

    # 3. Préparer
    print("\n=== Préparation ===")
    X, y, scaler, feature_cols = preparer_features(df, target_col='churn')
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # 4. Entraîner
    print("\n=== Entraînement ===")
    model = entrainer_modele(X_train, y_train, n_estimators=200, max_depth=4)

    # 5. Évaluer
    print("\n=== Évaluation ===")
    metrics = evaluer_modele(model, X_test, y_test)

    # 6. Sauvegarder
    print("\n=== Sauvegarde ===")
    sauvegarder_modele(
        model=model,
        scaler=scaler,
        feature_cols=feature_cols,
        metrics=metrics,
        version='1.0.0',
        path='models/model_v1.0.0.joblib'
    )

    print("\nTerminé !")


if __name__ == '__main__':
    main()
```

```bash
# Entraîner
python scripts/train.py

# Lancer l'API
uvicorn src.api:app --reload --port 8000

# Tester
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"anciennete_mois": 6, "montant_mensuel": 89.99, "nb_reclamations": 5, "nb_produits": 1, "satisfaction": 1.5}'
```

---

## 🎯 Points clés à retenir

1. Un **notebook** est pour l'exploration ; le code de production doit être **modulaire et testé**
2. **Joblib** est la méthode recommandée pour sérialiser les modèles sklearn
3. Sérialisez toujours le **pipeline complet** (preprocessing + modèle)
4. Structurez votre projet avec `src/`, `tests/`, `models/`, `data/`
5. **FastAPI** est idéal pour les API ML : rapide, validation auto, documentation auto
6. Utilisez **Pydantic** pour valider les données d'entrée (typage, bornes, exemples)
7. L'endpoint `/health` est indispensable pour le monitoring
8. Les **tests unitaires** (pytest) garantissent que le code ne casse pas lors des modifications
9. **ONNX** permet l'interopérabilité entre langages et frameworks
10. Ne chargez **jamais** un fichier pickle d'une source non fiable (risque de sécurité)

---

## ✅ Checklist de validation

- [ ] Je comprends pourquoi un notebook ne suffit pas en production
- [ ] Je sais sérialiser un modèle avec joblib (et je connais les risques de pickle)
- [ ] Je sais structurer un projet ML avec `src/`, `tests/`, `models/`
- [ ] Je sais refactorer un notebook en modules Python réutilisables
- [ ] Je sais construire une API avec FastAPI (endpoint POST /predict)
- [ ] Je sais utiliser Pydantic pour valider les données d'entrée
- [ ] Je sais écrire des tests unitaires avec pytest pour le preprocessing et l'API
- [ ] Je sais lancer l'API avec uvicorn et la tester avec curl
- [ ] Je sais accéder à la documentation Swagger auto-générée (/docs)
- [ ] J'ai réalisé le TP complet : API de scoring churn en local

---

**Précédent** : [Chapitre 14 : Interpréter ses Modèles et Éthique du ML](14-interpretabilite-ethique.md)

**Suivant** : [Chapitre 16 : Docker, Monitoring et la Vie en Production](16-docker-monitoring.md)
