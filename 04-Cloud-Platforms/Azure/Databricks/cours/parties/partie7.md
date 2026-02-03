## 🎯 Objectifs d'apprentissage

- Comprendre MLflow et son rôle dans le ML lifecycle
- Tracker des expériences ML avec MLflow Tracking
- Gérer des modèles avec MLflow Model Registry
- Déployer et servir des modèles ML
- Utiliser AutoML pour accélérer le développement
- Implémenter MLOps sur Databricks

## 1. Introduction à MLflow

MLflow est une **plateforme open source** pour gérer l'intégralité du cycle de vie du Machine Learning. Databricks intègre nativement MLflow avec des fonctionnalités avancées.

### Composants de MLflow

#### MLflow Tracking

Enregistrement des expériences, paramètres, métriques et artefacts

#### MLflow Projects

Format standardisé pour packager le code ML réutilisable

#### MLflow Models

Format standard pour packager les modèles ML

#### Model Registry

Store centralisé pour gérer les versions et le lifecycle des modèles

```bash
┌─────────────────────────────────────────────────────────────┐
│                    ML LIFECYCLE WITH MLFLOW                  │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌───────────────┐      ┌────────────────┐                  │
│  │ Data Prep     │ ───▶ │ Experimentation│                  │
│  └───────────────┘      └───────┬────────┘                  │
│                                  │                           │
│                                  ▼                           │
│                         ┌────────────────┐                   │
│                         │ MLflow Tracking│                   │
│                         │  • Params      │                   │
│                         │  • Metrics     │                   │
│                         │  • Models      │                   │
│                         └───────┬────────┘                   │
│                                 │                            │
│                                 ▼                            │
│                        ┌────────────────┐                    │
│                        │ Model Registry │                    │
│                        │  • None        │                    │
│                        │  • Staging     │                    │
│                        │  • Production  │                    │
│                        │  • Archived    │                    │
│                        └───────┬────────┘                    │
│                                │                             │
│                     ┌──────────┴──────────┐                 │
│                     ▼                     ▼                 │
│              ┌─────────────┐      ┌─────────────┐          │
│              │ Batch Infer │      │ Real-time   │          │
│              │             │      │ Serving     │          │
│              └─────────────┘      └─────────────┘          │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## 2. MLflow Tracking

### Enregistrer une expérience simple

```bash
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
import pandas as pd

# Charger les données
df = spark.read.table("customer_churn").toPandas()
X = df.drop("churn", axis=1)
y = df["churn"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Démarrer une run MLflow
with mlflow.start_run(run_name="rf_baseline") as run:

# Log des paramètres
    n_estimators = 100
    max_depth = 10

    mlflow.log_param("n_estimators", n_estimators)
    mlflow.log_param("max_depth", max_depth)
    mlflow.log_param("model_type", "RandomForest")

# Entraînement
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=42
    )
    model.fit(X_train, y_train)

# Prédictions
    y_pred = model.predict(X_test)

# Log des métriques
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    mlflow.log_metric("accuracy", accuracy)
    mlflow.log_metric("f1_score", f1)

# Log du modèle
    mlflow.sklearn.log_model(
        model,
        "model",
        registered_model_name="customer_churn_classifier"
    )

# Log d'artefacts (fichiers)
    import matplotlib.pyplot as plt
    from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

    cm = confusion_matrix(y_test, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm)
    disp.plot()
    plt.savefig("confusion_matrix.png")
    mlflow.log_artifact("confusion_matrix.png")

    print(f"Run ID: {run.info.run_id}")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"F1 Score: {f1:.4f}")
```

### Tracking avec plusieurs expériences

```bash
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from xgboost import XGBClassifier

# Créer ou récupérer une expérience
experiment_name = "/Users/me@company.com/churn_prediction"
mlflow.set_experiment(experiment_name)

models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Random Forest": RandomForestClassifier(n_estimators=100),
    "Gradient Boosting": GradientBoostingClassifier(n_estimators=100),
    "XGBoost": XGBClassifier(n_estimators=100, use_label_encoder=False)
}

results = []

for model_name, model in models.items():
    with mlflow.start_run(run_name=model_name):

# Tags pour organisation
        mlflow.set_tag("model_family", model_name.split()[0])
        mlflow.set_tag("developer", "data_team")

# Entraînement
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

# Métriques
        accuracy = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)

        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("f1_score", f1)

# Log modèle
        mlflow.sklearn.log_model(model, "model")

        results.append({
            "model": model_name,
            "accuracy": accuracy,
            "f1_score": f1
        })

        print(f"{model_name}: Accuracy={accuracy:.4f}, F1={f1:.4f}")

# Comparer les résultats
results_df = pd.DataFrame(results).sort_values("f1_score", ascending=False)
display(results_df)
```

### Rechercher et comparer des runs

```bash
# Rechercher des runs par filtre
from mlflow.tracking import MlflowClient

client = MlflowClient()

# Obtenir l'expérience
experiment = client.get_experiment_by_name(experiment_name)

# Rechercher les runs avec un filtre
runs = mlflow.search_runs(
    experiment_ids=[experiment.experiment_id],
    filter_string="metrics.accuracy > 0.85",
    order_by=["metrics.f1_score DESC"],
    max_results=10
)

display(runs[["run_id", "start_time", "params.model_type", "metrics.accuracy", "metrics.f1_score"]])

# Obtenir les détails d'un run spécifique
run_id = "abc123..."
run = client.get_run(run_id)
print(f"Paramètres: {run.data.params}")
print(f"Métriques: {run.data.metrics}")
```

## 3. MLflow Model Registry

Le Model Registry est un store centralisé pour gérer les versions et le lifecycle des modèles ML.

### Enregistrer un modèle

```bash
# Méthode 1 : Lors du log
with mlflow.start_run():
    mlflow.sklearn.log_model(
        model,
        "model",
        registered_model_name="customer_churn_classifier"
    )

# Méthode 2 : Depuis un run existant
run_id = "abc123..."
model_uri = f"runs:/{run_id}/model"

mlflow.register_model(
    model_uri=model_uri,
    name="customer_churn_classifier"
)
```

### Gérer les versions et stages

| Stage | Description | Utilisation |
| --- | --- | --- |
| **None** | Nouvellement enregistré | Modèle en développement |
| **Staging** | En test/validation | Tests UAT, A/B testing |
| **Production** | Déployé en production | Serving en production |
| **Archived** | Archivé/obsolète | Modèles retirés |

```bash
from mlflow.tracking import MlflowClient

client = MlflowClient()
model_name = "customer_churn_classifier"

# Promouvoir une version en Staging
client.transition_model_version_stage(
    name=model_name,
    version=3,
    stage="Staging",
    archive_existing_versions=False
)

# Promouvoir en Production (et archiver les anciennes versions)
client.transition_model_version_stage(
    name=model_name,
    version=3,
    stage="Production",
    archive_existing_versions=True  # Archive les anciennes versions en Production
)

# Ajouter une description
client.update_model_version(
    name=model_name,
    version=3,
    description="Modèle entraîné sur données Q1 2024, accuracy=0.92, déployé le 2024-01-15"
)

# Lister toutes les versions
versions = client.search_model_versions(f"name='{model_name}'")
for v in versions:
    print(f"Version {v.version}: {v.current_stage} - {v.description}")
```

### Charger un modèle depuis le Registry

```bash
# Charger la version Production
model_production = mlflow.pyfunc.load_model(
    model_uri=f"models:/{model_name}/Production"
)

# Charger une version spécifique
model_v3 = mlflow.pyfunc.load_model(
    model_uri=f"models:/{model_name}/3"
)

# Prédiction
predictions = model_production.predict(X_test)
```

## 4. AutoML avec Databricks

Databricks AutoML automatise l'entraînement et le tuning de modèles ML pour accélérer le développement.

### Utiliser AutoML via l'interface

#### Lancer une expérience AutoML

1. Dans la barre latérale, cliquez sur `Machine Learning`
2. Cliquez sur `AutoML`
3. Sélectionnez votre table de données
4. Choisissez le type de problème :
   - Classification
   - Regression
   - Forecasting
5. Sélectionnez la colonne cible (label)
6. Configurez les paramètres avancés (optionnel)
7. Cliquez sur `Start AutoML`

### AutoML avec Python API

```bash
from databricks import automl

# Configuration AutoML pour classification
summary = automl.classify(
    dataset=df,
    target_col="churn",
    primary_metric="f1",
    timeout_minutes=30,
    max_trials=20
)

# Résultats
print(f"Best trial: {summary.best_trial}")
print(f"Best model URI: {summary.best_trial.model_path}")
print(f"Best F1 score: {summary.best_trial.metrics['test_f1_score']}")

# Le meilleur modèle est automatiquement enregistré dans MLflow
# Vous pouvez le charger et l'utiliser
best_model = mlflow.pyfunc.load_model(summary.best_trial.model_path)
```

### Ce que fait AutoML

#### Data Preprocessing

- Feature engineering automatique
- Encodage de variables catégorielles
- Gestion des valeurs manquantes

#### Model Selection

- Teste plusieurs algorithmes
- Hyperparameter tuning
- Cross-validation

#### Explainability

- Feature importance
- SHAP values
- Visualisations

#### Notebooks Generated

- Data exploration
- Best model notebook
- Code réutilisable

## 5. Déploiement et serving

### Batch Inference

```bash
# Charger le modèle Production
model = mlflow.pyfunc.load_model(f"models:/{model_name}/Production")

# Charger de nouvelles données
new_data = spark.read.table("new_customers")
new_data_pandas = new_data.toPandas()

# Prédictions batch
predictions = model.predict(new_data_pandas)

# Ajouter les prédictions au DataFrame
new_data_pandas["churn_prediction"] = predictions
new_data_pandas["prediction_date"] = pd.Timestamp.now()

# Sauvegarder les résultats
spark.createDataFrame(new_data_pandas) \
    .write \
    .format("delta") \
    .mode("append") \
    .saveAsTable("churn_predictions")
```

### Model Serving (Real-time)

```bash
# Via l'interface Databricks
# 1. Aller dans Machine Learning → Models
# 2. Sélectionner votre modèle
# 3. Onglet "Serving"
# 4. Cliquer "Enable Serving"
# 5. Configurer : Workload size, Scale-out

# Une fois déployé, vous obtenez une API REST endpoint

# Appeler le endpoint
import requests
import json

# Token d'authentification Databricks
token = dbutils.notebook.entry_point.getDbutils() \
    .notebook().getContext().apiToken().get()

# Endpoint du modèle
serving_endpoint = "https:///serving-endpoints/customer_churn_classifier/invocations"

# Données d'entrée
input_data = {
    "dataframe_records": [
        {"age": 35, "tenure": 12, "monthly_charges": 65.5, "total_charges": 786.0},
        {"age": 42, "tenure": 24, "monthly_charges": 89.3, "total_charges": 2143.2}
    ]
}

# Requête
response = requests.post(
    serving_endpoint,
    headers={"Authorization": f"Bearer {token}"},
    json=input_data
)

predictions = response.json()
print(predictions)
# Output: {"predictions": [0, 1]}
```

### Utilisation via Spark UDF (Inference distribuée)

```bash
import mlflow.pyfunc

# Créer une UDF depuis le modèle
model_udf = mlflow.pyfunc.spark_udf(
    spark,
    model_uri=f"models:/{model_name}/Production",
    result_type="double"
)

# Appliquer le modèle sur un grand DataFrame Spark
large_df = spark.read.table("all_customers")

predictions_df = large_df.withColumn(
    "churn_prediction",
    model_udf(*[col(c) for c in feature_cols])
)

display(predictions_df)

# Sauvegarder
predictions_df.write.format("delta").mode("overwrite").saveAsTable("customer_predictions")
```

## 6. MLOps et CI/CD

### Workflow MLOps complet

```bash
┌─────────────────────────────────────────────────────────────┐
│                      MLOPS WORKFLOW                          │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  1. [Development]                                            │
│     • Feature Engineering                                    │
│     • Model Training (MLflow Tracking)                       │
│     • Experimentation                                        │
│                   │                                          │
│                   ▼                                          │
│  2. [Version Control]                                        │
│     • Git commit (code + config)                             │
│     • Register Model in MLflow Registry                      │
│                   │                                          │
│                   ▼                                          │
│  3. [CI/CD Pipeline]                                         │
│     • Run unit tests                                         │
│     • Train model on CI                                      │
│     • Model validation tests                                 │
│                   │                                          │
│                   ▼                                          │
│  4. [Staging Deployment]                                     │
│     • Transition to "Staging"                                │
│     • A/B testing                                            │
│     • Performance monitoring                                 │
│                   │                                          │
│                   ▼                                          │
│  5. [Production Deployment]                                  │
│     • Transition to "Production"                             │
│     • Enable Model Serving                                   │
│     • Monitor metrics                                        │
│                   │                                          │
│                   ▼                                          │
│  6. [Monitoring & Retraining]                                │
│     • Data drift detection                                   │
│     • Performance degradation alerts                         │
│     • Trigger retraining pipeline                            │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### Exemple de workflow automatisé

```bash
# Notebook 1: Training Pipeline
import mlflow
from datetime import datetime

# Configuration
model_name = "customer_churn_classifier"
min_accuracy_threshold = 0.85

# Entraînement
with mlflow.start_run(run_name=f"training_{datetime.now().strftime('%Y%m%d')}"):

# ... code d'entraînement ...

# Enregistrer le modèle
    if accuracy > min_accuracy_threshold:
        model_version = mlflow.register_model(
            model_uri=f"runs:/{mlflow.active_run().info.run_id}/model",
            name=model_name
        )

# Transition automatique vers Staging
        client.transition_model_version_stage(
            name=model_name,
            version=model_version.version,
            stage="Staging"
        )

        print(f"Modèle version {model_version.version} déployé en Staging")
    else:
        print(f"Accuracy {accuracy} < seuil {min_accuracy_threshold}. Modèle non déployé.")
```

```bash
# Notebook 2: Validation et promotion
from mlflow.tracking import MlflowClient

client = MlflowClient()

# Récupérer la dernière version Staging
staging_versions = client.get_latest_versions(model_name, stages=["Staging"])
staging_version = staging_versions[0]

# Charger et tester sur validation set
model = mlflow.pyfunc.load_model(f"models:/{model_name}/Staging")
val_predictions = model.predict(X_val)
val_accuracy = accuracy_score(y_val, val_predictions)

# Promotion vers Production si validation OK
if val_accuracy > 0.90:
    client.transition_model_version_stage(
        name=model_name,
        version=staging_version.version,
        stage="Production",
        archive_existing_versions=True
    )

# Notification
    print(f"✅ Modèle version {staging_version.version} déployé en Production!")
# Envoyer email/Slack notification
else:
    print(f"❌ Validation échouée. Accuracy: {val_accuracy}")
```

### Monitoring des modèles

```bash
# Détecter le data drift
from scipy.stats import ks_2samp

# Données d'entraînement
train_data = spark.read.table("training_data").toPandas()

# Données de production récentes
prod_data = spark.read.table("production_inference") \
    .filter("prediction_date >= current_date() - 7") \
    .toPandas()

# Test de Kolmogorov-Smirnov pour chaque feature
drift_detected = False
for col in feature_cols:
    statistic, p_value = ks_2samp(train_data[col], prod_data[col])

    if p_value < 0.05:  # Seuil de significativité
        print(f"⚠️ Data drift détecté sur {col}: p-value={p_value:.4f}")
        drift_detected = True

if drift_detected:
    print("Déclenchement du pipeline de retraining...")
# Trigger retraining job via API
```

### 📌 Points clés à retenir

- MLflow gère l'intégralité du ML lifecycle : tracking, registry, serving
- Tracking enregistre paramètres, métriques, modèles et artefacts
- Model Registry centralise la gestion des versions avec stages (None/Staging/Production/Archived)
- AutoML accélère le développement avec tuning automatique
- Déploiement flexible : batch inference ou real-time serving
- MLOps workflow complet avec CI/CD et monitoring
- Intégration native Databricks pour scalabilité et performance

#### 🎉 Félicitations !

Vous avez complété la formation Azure Databricks ! Vous maîtrisez maintenant :

- ✅ L'architecture et les concepts de Databricks
- ✅ La configuration et gestion des clusters
- ✅ Les notebooks et langages multiples
- ✅ Le traitement de données avec Spark
- ✅ Delta Lake pour des données fiables
- ✅ L'orchestration avec Workflows
- ✅ Le Machine Learning avec MLflow

**Prochaines étapes :** Mettez en pratique ces compétences sur des projets réels et explorez les fonctionnalités avancées comme Delta Live Tables, Unity Catalog, et Lakehouse Monitoring.