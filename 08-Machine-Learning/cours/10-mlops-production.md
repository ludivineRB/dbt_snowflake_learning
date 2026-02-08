# Chapitre 10 : MLOps et Mise en Production

## 🎯 Objectifs

- Comprendre le MLOps et pourquoi il est indispensable pour industrialiser le ML
- Savoir tracker des expériences avec MLflow (logging, comparaison, registry)
- Maîtriser la sauvegarde et le versioning de modèles (joblib, pickle, ONNX)
- Créer une API de prédiction avec FastAPI et la conteneuriser avec Docker
- Mettre en place un pipeline CI/CD pour le ML avec GitHub Actions
- Détecter le data drift et le model drift en production
- Appliquer les bonnes pratiques de mise en production

---

## 1. 🧠 Introduction au MLOps

### 1.1 Qu'est-ce que le MLOps ?

Le **MLOps** (Machine Learning Operations) est l'ensemble des pratiques qui visent à **déployer et maintenir des modèles ML en production de manière fiable et efficace**. C'est la rencontre entre le Machine Learning, le DevOps et le Data Engineering.

> 💡 **Conseil de pro** : "Un modèle qui tourne dans un notebook Jupyter n'a AUCUNE valeur business. La valeur commence quand le modèle est en production, accessible, monitoré et maintenu. Le MLOps, c'est le pont entre l'expérimentation et la valeur business."

### 1.2 Pourquoi c'est important ?

| Problème sans MLOps | Solution avec MLOps |
|---|---|
| "Ça marchait sur mon laptop" | Environnements reproductibles (Docker, uv) |
| Pas de traçabilité des expériences | Experiment tracking (MLflow) |
| Modèle déployé à la main | CI/CD automatisé |
| Aucune idée si le modèle est encore bon | Monitoring et alerting |
| Impossible de revenir en arrière | Versioning des modèles et des données |
| Code spaghetti dans des notebooks | Pipelines structurés et testés |

**Statistiques alarmantes :**

- **87%** des projets ML n'atteignent jamais la production (Gartner)
- **55%** des entreprises n'ont jamais déployé un modèle ML (Algorithmia)
- Le temps moyen de déploiement d'un modèle est de **31 jours** sans MLOps, **7 jours** avec

> ⚠️ **Attention** : "Le MLOps n'est pas un luxe réservé aux grandes entreprises. Même pour un side-project ou une startup, les bonnes pratiques dès le début vous éviteront des mois de dette technique."

### 1.3 Le cycle de vie ML

```
┌─────────────────────────────────────────────────────────────┐
│                     CYCLE DE VIE ML                         │
│                                                             │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌─────────┐ │
│  │ 1. Cadrer│──►│ 2. Données│──►│ 3. Modèle│──►│4. Évaluer│ │
│  │le problème│  │ & Features│   │ Training │   │& Valider│ │
│  └──────────┘   └──────────┘   └──────────┘   └────┬────┘ │
│       ▲                                             │      │
│       │                                             ▼      │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌─────────┐ │
│  │8. Réentr.│◄──│7. Monitor│◄──│6. Opérer │◄──│5. Deploy │ │
│  │& Itérer  │   │& Alerter │   │& Servir  │   │& Livrer │ │
│  └──────────┘   └──────────┘   └──────────┘   └─────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 1.4 Les niveaux de maturité MLOps

| Niveau | Description | Caractéristiques |
|---|---|---|
| **0 - Manuel** | Tout est fait à la main | Notebooks, pas de versioning, pas de monitoring |
| **1 - Pipeline ML** | Pipeline automatisé | Entraînement automatisé, experiment tracking |
| **2 - CI/CD ML** | Automatisation complète | Tests auto, déploiement auto, monitoring |
| **3 - Full MLOps** | Optimisation continue | Réentraînement auto, A/B testing, feature store |

> 💡 **Conseil de pro** : "Visez le niveau 2 comme objectif réaliste. Le niveau 3 n'est pertinent que pour les entreprises qui ont des dizaines de modèles en production avec des données qui changent rapidement."

---

## 2. 📊 Experiment Tracking avec MLflow

### 2.1 Pourquoi tracker ses expériences ?

Sans tracking, vous allez forcément vous retrouver dans cette situation :

```
modele_v1.pkl
modele_v2.pkl
modele_v2_final.pkl
modele_v2_final_FINAL.pkl
modele_v2_final_FINAL_OK.pkl    # ← Lequel est le bon ?
```

MLflow résout ce problème en enregistrant **automatiquement** :
- Les **paramètres** (hyperparamètres, features utilisées)
- Les **métriques** (accuracy, F1, RMSE, etc.)
- Les **artefacts** (modèle sérialisé, graphiques, données)
- L'**environnement** (versions des packages)

### 2.2 Installation et configuration

```bash
# Installation avec uv
uv add mlflow scikit-learn pandas

# Lancer l'interface MLflow
uv run mlflow ui --port 5000
```

> 💡 **Conseil de pro** : "Lancez l'interface MLflow dans un terminal dédié. Ouvrez http://localhost:5000 dans votre navigateur et gardez-le ouvert pendant vos expérimentations. Vous verrez vos runs apparaître en temps réel."

### 2.3 Logging des expériences

```python
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.datasets import load_iris
import pandas as pd

# Charger les données
iris = load_iris()
X = pd.DataFrame(iris.data, columns=iris.feature_names)
y = iris.target

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Configurer l'expérience MLflow
mlflow.set_experiment("classification-iris")

# Définir les hyperparamètres à tester
configs = [
    {"n_estimators": 50,  "max_depth": 3,  "min_samples_split": 2},
    {"n_estimators": 100, "max_depth": 5,  "min_samples_split": 5},
    {"n_estimators": 200, "max_depth": 10, "min_samples_split": 10},
    {"n_estimators": 100, "max_depth": None, "min_samples_split": 2},
]

for params in configs:
    # Chaque run est isolé dans un contexte MLflow
    with mlflow.start_run(run_name=f"rf_depth{params['max_depth']}_est{params['n_estimators']}"):

        # 1. Logger les paramètres
        mlflow.log_params(params)
        mlflow.log_param("random_state", 42)
        mlflow.log_param("test_size", 0.2)

        # 2. Entraîner le modèle
        model = RandomForestClassifier(**params, random_state=42)
        model.fit(X_train, y_train)

        # 3. Prédire et évaluer
        y_pred = model.predict(X_test)

        accuracy = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average="weighted")
        precision = precision_score(y_test, y_pred, average="weighted")
        recall = recall_score(y_test, y_pred, average="weighted")

        # 4. Logger les métriques
        mlflow.log_metrics({
            "accuracy": accuracy,
            "f1_weighted": f1,
            "precision_weighted": precision,
            "recall_weighted": recall,
        })

        # 5. Logger le modèle comme artefact
        mlflow.sklearn.log_model(model, "random_forest_model")

        # 6. Logger des métadonnées supplémentaires
        mlflow.set_tag("auteur", "equipe-ml")
        mlflow.set_tag("type", "classification")
        mlflow.set_tag("dataset", "iris")

        print(f"Params: {params} → Accuracy: {accuracy:.4f}, F1: {f1:.4f}")
```

> ⚠️ **Attention** : "N'oubliez jamais de logger le `random_state` et le `test_size`. Sans ça, vous ne pourrez pas reproduire vos résultats, même avec les mêmes hyperparamètres."

### 2.4 Comparaison de runs

```python
import mlflow

# Récupérer toutes les runs d'une expérience
experiment = mlflow.get_experiment_by_name("classification-iris")
runs = mlflow.search_runs(
    experiment_ids=[experiment.experiment_id],
    order_by=["metrics.f1_weighted DESC"]
)

# Afficher le top 5 des meilleurs runs
print("=== Top 5 des meilleurs modèles ===")
colonnes = ["run_id", "params.n_estimators", "params.max_depth",
            "metrics.accuracy", "metrics.f1_weighted"]
print(runs[colonnes].head(5).to_string(index=False))

# Trouver le meilleur run
best_run = runs.iloc[0]
print(f"\nMeilleur run : {best_run['run_id']}")
print(f"  Accuracy : {best_run['metrics.accuracy']:.4f}")
print(f"  F1 Score : {best_run['metrics.f1_weighted']:.4f}")
```

### 2.5 Model Registry

Le **Model Registry** est un registre centralisé pour gérer le cycle de vie des modèles : staging, production, archivage.

```python
import mlflow
from mlflow.tracking import MlflowClient

client = MlflowClient()

# Enregistrer le meilleur modèle dans le registry
best_run_id = best_run["run_id"]
model_uri = f"runs:/{best_run_id}/random_forest_model"

# Créer ou mettre à jour le modèle dans le registry
result = mlflow.register_model(
    model_uri=model_uri,
    name="iris-classifier"
)
print(f"Modèle enregistré : version {result.version}")

# Passer le modèle en staging (pour validation)
client.transition_model_version_stage(
    name="iris-classifier",
    version=result.version,
    stage="Staging"
)
print(f"Modèle v{result.version} → Staging")

# Après validation, passer en production
client.transition_model_version_stage(
    name="iris-classifier",
    version=result.version,
    stage="Production"
)
print(f"Modèle v{result.version} → Production")

# Charger le modèle de production
model_prod = mlflow.sklearn.load_model("models:/iris-classifier/Production")
print(f"Modèle de production chargé : {type(model_prod).__name__}")
```

> 💡 **Conseil de pro** : "Utilisez systématiquement les stages Staging/Production. Avant de passer un modèle en Production, validez-le sur un jeu de données de staging avec des critères de performance clairs (ex: F1 > 0.95)."

---

## 3. 💾 Sauvegarde et Versioning des Modèles

### 3.1 Sérialisation avec joblib et pickle

```python
import joblib
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

# Créer un pipeline complet
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('model', RandomForestClassifier(n_estimators=100, random_state=42))
])
pipeline.fit(X_train, y_train)

# === Méthode 1 : joblib (RECOMMANDÉ pour sklearn) ===
joblib.dump(pipeline, "model/pipeline_v1.joblib")
pipeline_charge = joblib.load("model/pipeline_v1.joblib")
print(f"joblib - Accuracy : {pipeline_charge.score(X_test, y_test):.4f}")

# === Méthode 2 : pickle (standard Python) ===
with open("model/pipeline_v1.pkl", "wb") as f:
    pickle.dump(pipeline, f)

with open("model/pipeline_v1.pkl", "rb") as f:
    pipeline_pickle = pickle.load(f)
print(f"pickle - Accuracy : {pipeline_pickle.score(X_test, y_test):.4f}")
```

| Format | Avantages | Inconvénients | Cas d'usage |
|---|---|---|---|
| **joblib** | Rapide pour gros arrays numpy | Spécifique Python | Modèles sklearn |
| **pickle** | Standard Python | Lent pour gros objets, vulnérable | Objets Python simples |
| **ONNX** | Multi-plateforme, performant | Complexe à configurer | Production cross-language |
| **MLflow** | Versioning intégré, metadata | Dépendance MLflow | Projets avec tracking |

> ⚠️ **Attention** : "Ne chargez JAMAIS un fichier pickle provenant d'une source non fiable. Pickle peut exécuter du code arbitraire lors du chargement. En production, préférez ONNX ou les formats MLflow."

### 3.2 Export ONNX pour la production

```python
# Installation
# uv add skl2onnx onnxruntime

from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType
import onnxruntime as rt
import numpy as np

# Convertir le pipeline sklearn en ONNX
initial_type = [("float_input", FloatTensorType([None, X_train.shape[1]]))]
onnx_model = convert_sklearn(pipeline, initial_types=initial_type)

# Sauvegarder le modèle ONNX
with open("model/pipeline_v1.onnx", "wb") as f:
    f.write(onnx_model.SerializeToString())

# Charger et inférer avec ONNX Runtime (beaucoup plus rapide)
session = rt.InferenceSession("model/pipeline_v1.onnx")
input_name = session.get_inputs()[0].name

# Prédiction ONNX
onnx_pred = session.run(
    None,
    {input_name: X_test.values.astype(np.float32)}
)
print(f"Prédictions ONNX : {onnx_pred[0][:5]}")
```

> 💡 **Conseil de pro** : "ONNX est le format idéal pour la production. Il est 2 à 10x plus rapide que sklearn pour l'inférence, il est indépendant du langage (Python, C++, Java, JavaScript) et il ne nécessite pas d'installer sklearn en production."

### 3.3 Versioning avec MLflow

```python
import mlflow
import json
from datetime import datetime

# Sauvegarder un modèle avec toutes ses métadonnées
with mlflow.start_run(run_name="production-v1.2"):
    # Logger le modèle
    mlflow.sklearn.log_model(pipeline, "model")

    # Logger les métadonnées de versioning
    mlflow.log_params({
        "model_type": "RandomForest",
        "n_features": X_train.shape[1],
        "n_samples_train": X_train.shape[0],
        "feature_names": json.dumps(list(X_train.columns)),
    })

    mlflow.log_metrics({
        "accuracy": pipeline.score(X_test, y_test),
        "n_classes": len(set(y_test)),
    })

    mlflow.set_tags({
        "version": "1.2",
        "date_training": datetime.now().isoformat(),
        "deploye_par": "equipe-ml",
        "environnement": "production",
    })

    print("Modèle versionné et sauvegardé dans MLflow")
```

---

## 4. 🚀 Serving de Modèles avec FastAPI

### 4.1 Pourquoi FastAPI ?

| Framework | Performance | Documentation auto | Validation | Async |
|---|---|---|---|---|
| Flask | Moyenne | Non | Non | Non |
| **FastAPI** | **Excellente** | **Oui (Swagger)** | **Oui (Pydantic)** | **Oui** |
| Django REST | Bonne | Plugin | Plugin | Plugin |

FastAPI est le choix idéal pour servir des modèles ML grâce à sa **performance**, sa **validation automatique** et sa **documentation Swagger générée automatiquement**.

### 4.2 Installation

```bash
# Installer les dépendances
uv add fastapi uvicorn joblib scikit-learn pydantic
```

### 4.3 API de prédiction complète

```python
# fichier : app/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
import joblib
import numpy as np
import logging
from datetime import datetime

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Charger le modèle au démarrage de l'API
MODEL_PATH = "model/pipeline_v1.joblib"
try:
    model = joblib.load(MODEL_PATH)
    logger.info(f"Modèle chargé depuis {MODEL_PATH}")
except FileNotFoundError:
    logger.error(f"Modèle introuvable : {MODEL_PATH}")
    raise

# Initialiser l'application FastAPI
app = FastAPI(
    title="API de Prédiction ML",
    description="API pour servir un modèle de classification Iris",
    version="1.0.0"
)

# === Schémas Pydantic pour la validation ===

class PredictionInput(BaseModel):
    """Schéma d'entrée pour une prédiction."""
    sepal_length: float = Field(..., ge=0, le=10, description="Longueur du sépale (cm)")
    sepal_width: float = Field(..., ge=0, le=10, description="Largeur du sépale (cm)")
    petal_length: float = Field(..., ge=0, le=10, description="Longueur du pétale (cm)")
    petal_width: float = Field(..., ge=0, le=10, description="Largeur du pétale (cm)")

    class Config:
        json_schema_extra = {
            "example": {
                "sepal_length": 5.1,
                "sepal_width": 3.5,
                "petal_length": 1.4,
                "petal_width": 0.2
            }
        }

class PredictionOutput(BaseModel):
    """Schéma de sortie pour une prédiction."""
    prediction: int
    label: str
    probabilites: List[float]
    timestamp: str

class BatchInput(BaseModel):
    """Schéma d'entrée pour des prédictions en lot."""
    instances: List[PredictionInput]

class HealthResponse(BaseModel):
    """Schéma de réponse pour le health check."""
    status: str
    model_loaded: bool
    timestamp: str

# === Mapping des classes ===
CLASSES = {0: "setosa", 1: "versicolor", 2: "virginica"}

# === Endpoints ===

@app.get("/health", response_model=HealthResponse)
def health_check():
    """Vérifier que l'API et le modèle fonctionnent."""
    return HealthResponse(
        status="healthy",
        model_loaded=model is not None,
        timestamp=datetime.now().isoformat()
    )

@app.post("/predict", response_model=PredictionOutput)
def predict(input_data: PredictionInput):
    """Prédire la classe d'une fleur Iris."""
    try:
        # Convertir l'entrée en array numpy
        features = np.array([[
            input_data.sepal_length,
            input_data.sepal_width,
            input_data.petal_length,
            input_data.petal_width
        ]])

        # Prédiction et probabilités
        prediction = int(model.predict(features)[0])
        probabilites = model.predict_proba(features)[0].tolist()

        # Logger la prédiction (utile pour le monitoring)
        logger.info(
            f"Prédiction: {CLASSES[prediction]} "
            f"(proba: {max(probabilites):.2%}) "
            f"| Input: {input_data.model_dump()}"
        )

        return PredictionOutput(
            prediction=prediction,
            label=CLASSES[prediction],
            probabilites=[round(p, 4) for p in probabilites],
            timestamp=datetime.now().isoformat()
        )

    except Exception as e:
        logger.error(f"Erreur de prédiction : {e}")
        raise HTTPException(status_code=500, detail=f"Erreur de prédiction : {str(e)}")

@app.post("/predict/batch", response_model=List[PredictionOutput])
def predict_batch(batch: BatchInput):
    """Prédire en lot pour plusieurs instances."""
    if len(batch.instances) > 1000:
        raise HTTPException(
            status_code=400,
            detail="Maximum 1000 instances par requête batch"
        )

    resultats = []
    for instance in batch.instances:
        resultat = predict(instance)
        resultats.append(resultat)
    return resultats
```

### 4.4 Lancer l'API

```bash
# Démarrer le serveur de développement
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Accéder à la documentation Swagger automatique
# http://localhost:8000/docs

# Tester avec curl
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}'
```

### 4.5 Tester l'API avec Python

```python
import requests

# Test du health check
response = requests.get("http://localhost:8000/health")
print(f"Statut : {response.json()['status']}")

# Test d'une prédiction unitaire
data = {
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
}
response = requests.post("http://localhost:8000/predict", json=data)
result = response.json()
print(f"Prédiction : {result['label']} (confiance : {max(result['probabilites']):.2%})")

# Test en lot (batch)
batch_data = {
    "instances": [
        {"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2},
        {"sepal_length": 6.7, "sepal_width": 3.0, "petal_length": 5.2, "petal_width": 2.3},
        {"sepal_length": 5.9, "sepal_width": 3.0, "petal_length": 4.2, "petal_width": 1.5},
    ]
}
response = requests.post("http://localhost:8000/predict/batch", json=batch_data)
for r in response.json():
    print(f"  {r['label']} (proba max : {max(r['probabilites']):.2%})")
```

> 💡 **Conseil de pro** : "Testez TOUJOURS votre API avec des données réalistes ET des données aberrantes (valeurs négatives, nulles, très grandes). La validation Pydantic vous protège, mais vérifiez que les messages d'erreur sont clairs pour les consommateurs de l'API."

---

## 5. 🐳 Docker pour le ML

### 5.1 Pourquoi Docker ?

Docker garantit que votre modèle tourne **exactement de la même manière** sur votre laptop, en staging et en production. Plus de "ça marchait chez moi".

### 5.2 Dockerfile pour un modèle ML

```dockerfile
# fichier : Dockerfile

# Image de base Python légère
FROM python:3.11-slim

# Métadonnées
LABEL maintainer="equipe-ml"
LABEL description="API de prédiction ML - Iris Classifier"
LABEL version="1.0.0"

# Variables d'environnement
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_SYSTEM_PYTHON=1

# Installer uv (gestionnaire de paquets rapide)
RUN pip install uv

# Répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances en premier (cache Docker)
COPY pyproject.toml uv.lock* ./

# Installer les dépendances avec uv
RUN uv sync --frozen --no-dev

# Copier le code et le modèle
COPY app/ ./app/
COPY model/ ./model/

# Exposer le port
EXPOSE 8000

# Health check intégré
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Lancer l'API avec uvicorn
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 5.3 Le fichier .dockerignore

```
# fichier : .dockerignore
__pycache__
*.pyc
.git
.gitignore
.env
notebooks/
data/raw/
*.ipynb
.venv/
mlruns/
```

### 5.4 Docker Compose pour l'environnement complet

```yaml
# fichier : docker-compose.yml
version: "3.8"

services:
  # API de prédiction
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - MODEL_PATH=/app/model/pipeline_v1.joblib
      - LOG_LEVEL=INFO
    volumes:
      - ./model:/app/model:ro    # Modèle en lecture seule
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # MLflow pour le tracking (optionnel en prod)
  mlflow:
    image: python:3.11-slim
    command: >
      bash -c "pip install uv && uv pip install mlflow --system &&
      mlflow server --host 0.0.0.0 --port 5000
      --backend-store-uri sqlite:///mlflow.db
      --default-artifact-root ./mlruns"
    ports:
      - "5000:5000"
    volumes:
      - mlflow_data:/app/mlruns
      - mlflow_db:/app
    restart: unless-stopped

volumes:
  mlflow_data:
  mlflow_db:
```

### 5.5 Commandes Docker essentielles

```bash
# Construire l'image
docker build -t ml-api:v1.0 .

# Lancer le conteneur
docker run -d -p 8000:8000 --name ml-api ml-api:v1.0

# Vérifier que ça tourne
docker logs ml-api
curl http://localhost:8000/health

# Lancer l'environnement complet
docker compose up -d

# Vérifier les services
docker compose ps

# Voir les logs en temps réel
docker compose logs -f api

# Arrêter tout
docker compose down
```

> ⚠️ **Attention** : "Ne mettez JAMAIS vos données d'entraînement dans l'image Docker. L'image ne doit contenir que le code, les dépendances et le modèle sérialisé. Les données restent dans des volumes ou des services externes (S3, GCS, BigQuery)."

---

## 6. 🔄 CI/CD pour le ML

### 6.1 Pourquoi CI/CD pour le ML ?

Le CI/CD (Continuous Integration / Continuous Deployment) automatise les tests et le déploiement. Pour le ML, il y a des spécificités :

| CI/CD classique | CI/CD ML |
|---|---|
| Tests unitaires du code | Tests unitaires + tests du modèle |
| Linting du code | Linting + validation des données |
| Build de l'application | Build + entraînement du modèle |
| Déploiement de l'app | Déploiement du modèle + de l'API |

### 6.2 Pipeline GitHub Actions

```yaml
# fichier : .github/workflows/ml-pipeline.yml

name: ML Pipeline CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  # Étape 1 : Tests du code et du modèle
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Installer Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Installer uv
        run: pip install uv

      - name: Installer les dépendances
        run: uv sync

      - name: Linting avec ruff
        run: uv run ruff check .

      - name: Tests unitaires
        run: uv run pytest tests/ -v --tb=short

      - name: Tests du modèle (performance minimale)
        run: uv run pytest tests/test_model.py -v

  # Étape 2 : Build et push de l'image Docker
  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4

      - name: Connexion au registre Docker
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build et push de l'image
        uses: docker/build-push-action@v5
        with:
          push: true
          tags: |
            ghcr.io/${{ github.repository }}/ml-api:latest
            ghcr.io/${{ github.repository }}/ml-api:${{ github.sha }}

  # Étape 3 : Déploiement
  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment: production
    steps:
      - name: Déployer sur le serveur
        run: |
          echo "Déploiement de l'image ghcr.io/${{ github.repository }}/ml-api:${{ github.sha }}"
          # Ici : ssh, kubectl apply, gcloud run deploy, etc.
```

### 6.3 Tests spécifiques au ML

```python
# fichier : tests/test_model.py

import pytest
import joblib
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

# Seuils de performance minimale
ACCURACY_MINIMALE = 0.90
F1_MINIMAL = 0.88

@pytest.fixture
def model():
    """Charger le modèle de production."""
    return joblib.load("model/pipeline_v1.joblib")

@pytest.fixture
def test_data():
    """Préparer les données de test."""
    iris = load_iris()
    _, X_test, _, y_test = train_test_split(
        iris.data, iris.target, test_size=0.2, random_state=42, stratify=iris.target
    )
    return X_test, y_test

class TestModelPerformance:
    """Tests de performance du modèle."""

    def test_accuracy_minimale(self, model, test_data):
        """Le modèle doit avoir une accuracy supérieure au seuil."""
        X_test, y_test = test_data
        accuracy = model.score(X_test, y_test)
        assert accuracy >= ACCURACY_MINIMALE, (
            f"Accuracy {accuracy:.4f} < seuil {ACCURACY_MINIMALE}"
        )

    def test_f1_minimal(self, model, test_data):
        """Le modèle doit avoir un F1 supérieur au seuil."""
        from sklearn.metrics import f1_score
        X_test, y_test = test_data
        y_pred = model.predict(X_test)
        f1 = f1_score(y_test, y_pred, average="weighted")
        assert f1 >= F1_MINIMAL, (
            f"F1 {f1:.4f} < seuil {F1_MINIMAL}"
        )

    def test_prediction_shape(self, model, test_data):
        """Les prédictions doivent avoir la bonne forme."""
        X_test, _ = test_data
        predictions = model.predict(X_test)
        assert predictions.shape == (X_test.shape[0],)

    def test_classes_valides(self, model, test_data):
        """Les prédictions doivent être dans les classes connues."""
        X_test, _ = test_data
        predictions = model.predict(X_test)
        classes_attendues = {0, 1, 2}
        assert set(predictions).issubset(classes_attendues)

    def test_probabilites(self, model, test_data):
        """Les probabilités doivent sommer à 1."""
        X_test, _ = test_data
        probas = model.predict_proba(X_test)
        # Chaque ligne doit sommer à ~1.0
        sommes = probas.sum(axis=1)
        np.testing.assert_allclose(sommes, 1.0, atol=1e-6)

class TestModelRobustesse:
    """Tests de robustesse du modèle."""

    def test_prediction_unitaire(self, model):
        """Le modèle doit gérer une seule instance."""
        instance = np.array([[5.1, 3.5, 1.4, 0.2]])
        prediction = model.predict(instance)
        assert len(prediction) == 1

    def test_valeurs_extremes(self, model):
        """Le modèle ne doit pas planter avec des valeurs extrêmes."""
        extreme = np.array([[0.0, 0.0, 0.0, 0.0]])
        prediction = model.predict(extreme)
        assert prediction is not None

    def test_reproductibilite(self, model, test_data):
        """Deux appels identiques doivent donner le même résultat."""
        X_test, _ = test_data
        pred1 = model.predict(X_test)
        pred2 = model.predict(X_test)
        np.testing.assert_array_equal(pred1, pred2)
```

> 💡 **Conseil de pro** : "Les tests de performance du modèle sont aussi importants que les tests unitaires du code. Si un nouveau commit dégrade l'accuracy en dessous du seuil, le pipeline doit BLOQUER le déploiement."

---

## 7. 📈 Monitoring en Production

### 7.1 Pourquoi monitorer ?

Un modèle ML en production se **dégrade inévitablement** avec le temps. Les données changent, les comportements utilisateurs évoluent, le monde change. C'est ce qu'on appelle le **drift**.

| Type de drift | Description | Exemple |
|---|---|---|
| **Data drift** | La distribution des données d'entrée change | Les clients sont plus jeunes qu'avant |
| **Concept drift** | La relation entre features et target change | Le COVID change les habitudes d'achat |
| **Model drift** | Les performances du modèle se dégradent | L'accuracy passe de 95% à 80% |

### 7.2 Détection du data drift

```python
# uv add scipy numpy pandas

import numpy as np
import pandas as pd
from scipy import stats
from typing import Dict, Tuple

class DataDriftDetector:
    """Détecteur de data drift basé sur des tests statistiques."""

    def __init__(self, reference_data: pd.DataFrame, seuil_pvalue: float = 0.05):
        """
        Initialiser le détecteur avec les données de référence (entraînement).

        Args:
            reference_data: Données utilisées lors de l'entraînement
            seuil_pvalue: Seuil en dessous duquel on considère qu'il y a drift
        """
        self.reference = reference_data
        self.seuil = seuil_pvalue

    def test_drift_numerique(self, production_data: pd.DataFrame) -> Dict[str, dict]:
        """
        Tester le drift sur les colonnes numériques avec le test de Kolmogorov-Smirnov.

        Le test KS compare deux distributions : si la p-value est basse,
        les distributions sont significativement différentes → il y a drift.
        """
        resultats = {}

        colonnes_num = self.reference.select_dtypes(include=[np.number]).columns

        for col in colonnes_num:
            # Test de Kolmogorov-Smirnov : compare deux distributions
            statistic, p_value = stats.ks_2samp(
                self.reference[col].dropna(),
                production_data[col].dropna()
            )

            drift_detecte = p_value < self.seuil

            resultats[col] = {
                "statistic": round(statistic, 4),
                "p_value": round(p_value, 4),
                "drift": drift_detecte,
                "severite": "CRITIQUE" if p_value < 0.001 else "ALERTE" if drift_detecte else "OK",
                "ref_mean": round(self.reference[col].mean(), 4),
                "prod_mean": round(production_data[col].mean(), 4),
            }

        return resultats

    def test_drift_categoriel(self, production_data: pd.DataFrame) -> Dict[str, dict]:
        """
        Tester le drift sur les colonnes catégorielles avec le test du Chi-2.
        """
        resultats = {}

        colonnes_cat = self.reference.select_dtypes(include=["object", "category"]).columns

        for col in colonnes_cat:
            # Distributions des catégories
            ref_counts = self.reference[col].value_counts(normalize=True)
            prod_counts = production_data[col].value_counts(normalize=True)

            # Aligner les catégories
            toutes_categories = set(ref_counts.index) | set(prod_counts.index)
            ref_aligned = [ref_counts.get(c, 0) for c in toutes_categories]
            prod_aligned = [prod_counts.get(c, 0) for c in toutes_categories]

            # Test du Chi-2
            statistic, p_value = stats.chisquare(prod_aligned, ref_aligned)

            resultats[col] = {
                "statistic": round(statistic, 4),
                "p_value": round(p_value, 4),
                "drift": p_value < self.seuil,
            }

        return resultats

    def rapport_complet(self, production_data: pd.DataFrame) -> dict:
        """Générer un rapport complet de drift."""
        drift_num = self.test_drift_numerique(production_data)
        drift_cat = self.test_drift_categoriel(production_data)

        # Compter les colonnes avec drift
        nb_drift_num = sum(1 for v in drift_num.values() if v["drift"])
        nb_drift_cat = sum(1 for v in drift_cat.values() if v["drift"])
        total_colonnes = len(drift_num) + len(drift_cat)
        total_drift = nb_drift_num + nb_drift_cat

        return {
            "resume": {
                "total_colonnes": total_colonnes,
                "colonnes_avec_drift": total_drift,
                "pourcentage_drift": round(total_drift / max(total_colonnes, 1) * 100, 1),
                "action_requise": total_drift > total_colonnes * 0.3,
            },
            "drift_numerique": drift_num,
            "drift_categoriel": drift_cat,
        }


# === Exemple d'utilisation ===

# Données de référence (entraînement)
np.random.seed(42)
ref_data = pd.DataFrame({
    "age": np.random.normal(35, 10, 1000),
    "revenu": np.random.normal(45000, 15000, 1000),
    "nb_achats": np.random.poisson(5, 1000),
})

# Données de production (avec drift sur l'âge)
prod_data = pd.DataFrame({
    "age": np.random.normal(28, 8, 500),       # Drift : clients plus jeunes
    "revenu": np.random.normal(44000, 15000, 500),  # Pas de drift significatif
    "nb_achats": np.random.poisson(5, 500),     # Pas de drift
})

# Détecter le drift
detecteur = DataDriftDetector(ref_data, seuil_pvalue=0.05)
rapport = detecteur.rapport_complet(prod_data)

print("=== RAPPORT DE DATA DRIFT ===")
print(f"Colonnes analysées : {rapport['resume']['total_colonnes']}")
print(f"Drift détecté sur  : {rapport['resume']['colonnes_avec_drift']} colonnes")
print(f"Pourcentage drift  : {rapport['resume']['pourcentage_drift']}%")
print(f"Action requise     : {'OUI' if rapport['resume']['action_requise'] else 'Non'}")
print()

for col, info in rapport["drift_numerique"].items():
    status = f"{'DRIFT' if info['drift'] else 'OK':>8}"
    print(f"  {col:15} : {status} (p={info['p_value']:.4f}, "
          f"ref={info['ref_mean']:.1f}, prod={info['prod_mean']:.1f})")
```

> ⚠️ **Attention** : "Un data drift ne signifie pas toujours que le modèle est mauvais. Parfois les données changent mais le modèle reste performant. C'est pourquoi il faut monitorer AUSSI les métriques de performance du modèle, pas seulement les distributions des données."

### 7.3 Monitoring des métriques en production

```python
import json
import logging
from datetime import datetime
from collections import deque
from typing import Optional

logger = logging.getLogger(__name__)

class ModelMonitor:
    """Moniteur de performance du modèle en production."""

    def __init__(self, nom_modele: str, taille_fenetre: int = 1000):
        """
        Args:
            nom_modele: Nom du modèle monitoré
            taille_fenetre: Nombre de prédictions à garder en mémoire
        """
        self.nom_modele = nom_modele
        self.predictions = deque(maxlen=taille_fenetre)
        self.feedbacks = deque(maxlen=taille_fenetre)
        self.alertes = []

    def enregistrer_prediction(self, input_data: dict, prediction: int,
                                probabilite: float):
        """Enregistrer une prédiction pour le monitoring."""
        self.predictions.append({
            "timestamp": datetime.now().isoformat(),
            "input": input_data,
            "prediction": prediction,
            "probabilite": probabilite,
        })

    def enregistrer_feedback(self, prediction_id: str, vrai_label: int):
        """Enregistrer le vrai label quand il est disponible (feedback loop)."""
        self.feedbacks.append({
            "timestamp": datetime.now().isoformat(),
            "prediction_id": prediction_id,
            "vrai_label": vrai_label,
        })

    def calculer_metriques(self) -> dict:
        """Calculer les métriques sur la fenêtre glissante."""
        if not self.predictions:
            return {"erreur": "Aucune prédiction enregistrée"}

        probas = [p["probabilite"] for p in self.predictions]
        preds = [p["prediction"] for p in self.predictions]

        metriques = {
            "nb_predictions": len(self.predictions),
            "proba_moyenne": round(sum(probas) / len(probas), 4),
            "proba_min": round(min(probas), 4),
            "proba_max": round(max(probas), 4),
            "distribution_classes": {
                cls: preds.count(cls) for cls in set(preds)
            },
        }

        # Alerte si la confiance moyenne baisse
        if metriques["proba_moyenne"] < 0.7:
            alerte = {
                "type": "CONFIANCE_BASSE",
                "message": f"Confiance moyenne à {metriques['proba_moyenne']:.2%}",
                "timestamp": datetime.now().isoformat(),
            }
            self.alertes.append(alerte)
            logger.warning(f"ALERTE : {alerte['message']}")

        return metriques

    def verifier_sante(self) -> dict:
        """Vérification complète de la santé du modèle."""
        metriques = self.calculer_metriques()
        return {
            "modele": self.nom_modele,
            "timestamp": datetime.now().isoformat(),
            "metriques": metriques,
            "alertes_recentes": self.alertes[-5:],
            "sante": "OK" if not self.alertes else "DEGRADEE",
        }
```

### 7.4 Dashboard de monitoring (intégration FastAPI)

```python
# Ajouter ces endpoints à app/main.py

monitor = ModelMonitor("iris-classifier")

@app.get("/monitoring/metriques")
def get_metriques():
    """Récupérer les métriques de monitoring."""
    return monitor.calculer_metriques()

@app.get("/monitoring/sante")
def get_sante():
    """Vérifier la santé du modèle."""
    return monitor.verifier_sante()

@app.get("/monitoring/alertes")
def get_alertes():
    """Récupérer les alertes récentes."""
    return {"alertes": monitor.alertes[-20:]}
```

> 💡 **Conseil de pro** : "En production, connectez ces métriques à un outil de visualisation comme Grafana ou Datadog. Configurez des alertes automatiques (Slack, email) quand la confiance moyenne passe sous un seuil ou quand du drift est détecté."

---

## 8. 📋 Bonnes Pratiques MLOps

### 8.1 Structure de projet recommandée

```
mon-projet-ml/
├── app/                        # Code de l'API
│   ├── __init__.py
│   ├── main.py                 # Endpoints FastAPI
│   └── schemas.py              # Schémas Pydantic
├── src/                        # Code ML
│   ├── __init__.py
│   ├── train.py                # Script d'entraînement
│   ├── predict.py              # Logique de prédiction
│   ├── features.py             # Feature engineering
│   └── evaluate.py             # Évaluation du modèle
├── tests/                      # Tests
│   ├── test_model.py           # Tests du modèle
│   ├── test_api.py             # Tests de l'API
│   └── test_features.py        # Tests du feature engineering
├── model/                      # Modèles sérialisés
│   └── pipeline_v1.joblib
├── data/                       # Données (PAS dans git)
│   ├── raw/
│   ├── processed/
│   └── features/
├── notebooks/                  # Notebooks d'exploration
│   └── exploration.ipynb
├── .github/workflows/          # CI/CD
│   └── ml-pipeline.yml
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml              # Dépendances (uv)
├── uv.lock                     # Lockfile uv
├── .gitignore
├── .env.example                # Variables d'environnement (template)
└── README.md
```

### 8.2 Le .gitignore pour le ML

```
# Données (trop volumineuses pour git)
data/
*.csv
*.parquet
*.h5

# Modèles sérialisés (versionnés avec MLflow ou DVC)
model/*.joblib
model/*.pkl
model/*.onnx

# MLflow
mlruns/

# Environnement
.env
.venv/

# Python
__pycache__/
*.pyc

# Notebooks checkpoints
.ipynb_checkpoints/

# IDE
.vscode/
.idea/
```

### 8.3 Checklist de mise en production

| Etape | Action | Fait ? |
|---|---|---|
| **Code** | Code versionné (git), pas de notebooks en prod | ☐ |
| **Données** | Pipeline de données reproductible | ☐ |
| **Modèle** | Modèle versionné (MLflow/DVC), métriques documentées | ☐ |
| **Tests** | Tests unitaires + tests de performance du modèle | ☐ |
| **API** | Endpoint `/predict` + `/health` + validation Pydantic | ☐ |
| **Docker** | Dockerfile optimisé, `.dockerignore` présent | ☐ |
| **CI/CD** | Pipeline automatisé (build, test, deploy) | ☐ |
| **Monitoring** | Data drift + model drift + alerting | ☐ |
| **Logging** | Toutes les prédictions loggées | ☐ |
| **Sécurité** | Pas de secrets dans le code, HTTPS activé | ☐ |
| **Documentation** | API documentée (Swagger), README à jour | ☐ |
| **Rollback** | Procédure de rollback testée | ☐ |

### 8.4 Les erreurs classiques à éviter

| Erreur | Conséquence | Solution |
|---|---|---|
| Pas de versioning du modèle | Impossible de reproduire ou rollback | MLflow Model Registry |
| Preprocessing séparé du modèle | Bugs subtils en production | Pipeline sklearn complet |
| Pas de monitoring | Le modèle se dégrade en silence | Data drift + métriques |
| Tests manuels seulement | Régressions non détectées | CI/CD avec tests auto |
| Secrets dans le code | Fuite de données | Variables d'env + `.env` |
| Docker image trop grosse | Déploiement lent | Image `slim` + `.dockerignore` |
| Pas de health check | Impossible de détecter les pannes | Endpoint `/health` |
| Données d'entraînement dans Docker | Image de 10 Go | Données dans S3/GCS |

> 💡 **Conseil de pro** : "La règle d'or du MLOps : automatisez tout ce qui peut l'être, documentez le reste. Si une tâche est faite plus de deux fois manuellement, elle doit être automatisée."

---

## 🎯 Points clés à retenir

1. Le **MLOps** est essentiel : 87% des projets ML échouent sans bonnes pratiques de déploiement
2. **MLflow** permet de tracker les expériences, comparer les runs et gérer le cycle de vie des modèles
3. **Sauvegardez le pipeline complet** (preprocessing + modèle), pas juste le modèle seul
4. **ONNX** est le format idéal pour la production (rapide, multi-plateforme)
5. **FastAPI** + Pydantic = API de prédiction robuste avec validation et documentation automatiques
6. **Docker** garantit la reproductibilité : "ça marche sur mon laptop" n'existe plus
7. **CI/CD** avec des tests de performance du modèle empêche les régressions
8. Le **monitoring** est non-négociable : data drift, model drift, métriques de confiance
9. La **structure de projet** doit séparer clairement code ML, API, tests et données
10. **Automatisez tout**, documentez le reste

## ✅ Checklist de validation

- [ ] Je comprends le cycle de vie ML et les niveaux de maturité MLOps
- [ ] Je sais configurer MLflow et logger des expériences (paramètres, métriques, modèles)
- [ ] Je sais comparer des runs et utiliser le Model Registry
- [ ] Je maîtrise la sauvegarde de modèles (joblib, pickle, ONNX)
- [ ] Je sais créer une API FastAPI avec `/predict`, `/health` et validation Pydantic
- [ ] Je sais conteneuriser un modèle ML avec Docker et Docker Compose
- [ ] Je sais écrire des tests de performance du modèle (accuracy minimale, robustesse)
- [ ] Je sais mettre en place un pipeline CI/CD avec GitHub Actions
- [ ] Je sais détecter le data drift avec des tests statistiques (KS, Chi-2)
- [ ] Je connais les bonnes pratiques de mise en production et la checklist de déploiement

---

[⬅️ Chapitre 9 : Feature Engineering](09-feature-engineering.md) | [➡️ Cheatsheet ML](CHEATSHEET-ml.md)
