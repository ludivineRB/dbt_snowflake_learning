## 🎯 Objectifs d'apprentissage

- Comprendre Databricks Workflows (anciennement Jobs)
- Créer des Jobs avec plusieurs tâches
- Gérer les dépendances entre tâches
- Planifier l'exécution automatique
- Monitorer et gérer les alertes
- Intégrer avec Azure Data Factory

## 1. Introduction aux Databricks Workflows

Databricks Workflows est la plateforme d'orchestration native pour automatiser et orchestrer vos pipelines de données et ML.

### Composants principaux

#### Jobs

Un job est un workflow automatisé composé d'une ou plusieurs tâches

#### Tasks

Une tâche est une unité d'exécution (notebook, script, JAR, etc.)

#### Triggers

Déclenchement par planification (cron) ou événements

#### Runs

Une exécution d'un job avec son historique et statut

```bash
┌─────────────────────────────────────────────────────────────┐
│                    DATABRICKS WORKFLOW                       │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌────────────┐         Trigger (Schedule/Manual)           │
│  │    Job     │                    │                         │
│  └─────┬──────┘                    ▼                         │
│        │              ┌──────────────────────┐               │
│        │              │   Task 1: Ingestion  │               │
│        │              └──────────┬───────────┘               │
│        │                         │                           │
│        │          ┌──────────────┴────────────┐              │
│        │          ▼                           ▼              │
│        │   ┌─────────────┐           ┌─────────────┐        │
│        │   │Task 2: ETL  │           │Task 3: Check│        │
│        │   └──────┬──────┘           └──────┬──────┘        │
│        │          │                          │               │
│        │          └──────────┬───────────────┘               │
│        │                     ▼                               │
│        │            ┌─────────────────┐                      │
│        │            │Task 4: Analytics│                      │
│        │            └─────────────────┘                      │
│        │                                                     │
│        │  Results → Notifications (Email, Slack, etc.)      │
│        │                                                     │
└─────────────────────────────────────────────────────────────┘
```

## 2. Créer un Job via l'interface

#### Créer votre premier Job

1. Dans la barre latérale, cliquez sur `Workflows`
2. Cliquez sur `Create Job`
3. Nommez le job : "ETL Pipeline Daily"
4. Créez la première tâche :
   - **Task name :** "ingest\_raw\_data"
   - **Type :** Notebook
   - **Source :** Sélectionnez votre notebook d'ingestion
   - **Cluster :** Sélectionnez un job cluster
   - **Parameters :** Ajoutez des paramètres si nécessaire
5. Ajoutez d'autres tâches avec `+ Add task`
6. Définissez les dépendances en liant les tâches
7. Configurez le déclenchement (schedule)
8. Cliquez sur `Create`

### Types de tâches

| Type | Description | Cas d'usage |
| --- | --- | --- |
| **Notebook** | Exécute un notebook Databricks | ETL, analyse, ML training |
| **Python script** | Exécute un fichier .py | Scripts standalone |
| **JAR** | Application Scala/Java | Jobs Spark Scala |
| **Python wheel** | Package Python (.whl) | Applications Python packagees |
| **SQL** | Exécute des requêtes SQL | Data transformations SQL |
| **dbt** | Exécute des projets dbt | Transformations avec dbt |
| **Delta Live Tables** | Pipeline DLT | Pipelines déclaratifs |

## 3. Créer un Job via l'API

```bash
import requests
import json

DATABRICKS_HOST = "https://<workspace-url>"
DATABRICKS_TOKEN = "<your-token>"

# Configuration du job
job_config = {
    "name": "ETL Pipeline Daily",
    "email_notifications": {
        "on_failure": ["data-team@company.com"],
        "on_success": ["data-team@company.com"]
    },
    "timeout_seconds": 7200,  # 2 heures
    "max_concurrent_runs": 1,
    "tasks": [
        {
            "task_key": "ingest_raw_data",
            "description": "Ingestion des données brutes",
            "notebook_task": {
                "notebook_path": "/Workspace/ETL/01_Ingestion",
                "base_parameters": {
                    "date": "{{job.start_date}}",
                    "environment": "production"
                }
            },
            "new_cluster": {
                "spark_version": "13.3.x-scala2.12",
                "node_type_id": "Standard_DS3_v2",
                "num_workers": 2,
                "autoscale": {
                    "min_workers": 2,
                    "max_workers": 8
                }
            },
            "timeout_seconds": 3600,
            "max_retries": 2,
            "retry_on_timeout": True
        },
        {
            "task_key": "transform_data",
            "description": "Transformation des données",
            "depends_on": [
                {"task_key": "ingest_raw_data"}
            ],
            "notebook_task": {
                "notebook_path": "/Workspace/ETL/02_Transform",
                "base_parameters": {
                    "date": "{{job.start_date}}"
                }
            },
            "new_cluster": {
                "spark_version": "13.3.x-scala2.12",
                "node_type_id": "Standard_DS3_v2",
                "num_workers": 4
            }
        },
        {
            "task_key": "data_quality_checks",
            "description": "Vérifications qualité",
            "depends_on": [
                {"task_key": "transform_data"}
            ],
            "python_wheel_task": {
                "package_name": "data_quality",
                "entry_point": "run_checks",
                "parameters": ["--date", "{{job.start_date}}"]
            },
            "libraries": [
                {"pypi": {"package": "great-expectations==0.18.0"}}
            ],
            "existing_cluster_id": "<cluster-id>"
        },
        {
            "task_key": "publish_analytics",
            "description": "Publication analytics",
            "depends_on": [
                {"task_key": "data_quality_checks"}
            ],
            "sql_task": {
                "query": {
                    "query_id": "<query-id>"
                },
                "warehouse_id": "<warehouse-id>"
            }
        }
    ],
    "schedule": {
        "quartz_cron_expression": "0 0 2 * * ?",  # 2h du matin
        "timezone_id": "Europe/Paris",
        "pause_status": "UNPAUSED"
    },
    "tags": {
        "environment": "production",
        "team": "data-engineering"
    }
}

# Créer le job
headers = {
    "Authorization": f"Bearer {DATABRICKS_TOKEN}",
    "Content-Type": "application/json"
}

response = requests.post(
    f"{DATABRICKS_HOST}/api/2.1/jobs/create",
    headers=headers,
    json=job_config
)

job_id = response.json()["job_id"]
print(f"Job créé avec l'ID : {job_id}")

# Déclencher une exécution immédiate
run_response = requests.post(
    f"{DATABRICKS_HOST}/api/2.1/jobs/run-now",
    headers=headers,
    json={"job_id": job_id}
)

run_id = run_response.json()["run_id"]
print(f"Run démarré avec l'ID : {run_id}")
```

## 4. Gestion des dépendances

### Types de dépendances

#### Sequential (Séquentielle)

Tâche B attend que A se termine

```bash
A → B
```

#### Parallel (Parallèle)

B et C s'exécutent en parallèle après A

```bash
   ┌→ B
A ─┤
   └→ C
```

#### Fan-in (Convergence)

D attend B ET C

```bash
B ─┐
   ├→ D
C ─┘
```

#### Conditional

Exécution conditionnelle basée sur le résultat

```bash
A → IF success → B
  → IF failure → C
```

### Exemple de workflow complexe

```bash
# Pipeline ETL complet avec branches conditionnelles
workflow_config = {
    "name": "Complex ETL Pipeline",
    "tasks": [
# Tâche initiale
        {
            "task_key": "validate_source",
            "description": "Valider la source de données",
            "notebook_task": {
                "notebook_path": "/ETL/00_Validate"
            }
        },
# Branches parallèles pour différentes sources
        {
            "task_key": "ingest_crm",
            "depends_on": [{"task_key": "validate_source"}],
            "notebook_task": {
                "notebook_path": "/ETL/Ingest_CRM"
            }
        },
        {
            "task_key": "ingest_erp",
            "depends_on": [{"task_key": "validate_source"}],
            "notebook_task": {
                "notebook_path": "/ETL/Ingest_ERP"
            }
        },
        {
            "task_key": "ingest_web",
            "depends_on": [{"task_key": "validate_source"}],
            "notebook_task": {
                "notebook_path": "/ETL/Ingest_Web"
            }
        },
# Convergence : transformation après toutes les ingestions
        {
            "task_key": "transform_join",
            "depends_on": [
                {"task_key": "ingest_crm"},
                {"task_key": "ingest_erp"},
                {"task_key": "ingest_web"}
            ],
            "notebook_task": {
                "notebook_path": "/ETL/Transform_Join"
            }
        },
# Branches parallèles analytics
        {
            "task_key": "analytics_sales",
            "depends_on": [{"task_key": "transform_join"}],
            "notebook_task": {
                "notebook_path": "/Analytics/Sales"
            }
        },
        {
            "task_key": "analytics_customer",
            "depends_on": [{"task_key": "transform_join"}],
            "notebook_task": {
                "notebook_path": "/Analytics/Customer"
            }
        },
# Notification finale
        {
            "task_key": "send_report",
            "depends_on": [
                {"task_key": "analytics_sales"},
                {"task_key": "analytics_customer"}
            ],
            "python_wheel_task": {
                "package_name": "reporting",
                "entry_point": "send_daily_report"
            }
        }
    ]
}
```

## 5. Planification et déclenchement

### Expressions Cron

| Expression | Description | Cas d'usage |
| --- | --- | --- |
| `0 0 2 * * ?` | Tous les jours à 2h du matin | ETL quotidien |
| `0 */4 * * * ?` | Toutes les 4 heures | Synchronisation régulière |
| `0 0 0 * * MON` | Tous les lundis à minuit | Rapport hebdomadaire |
| `0 0 9 1 * ?` | Le 1er de chaque mois à 9h | Rapport mensuel |
| `0 30 8-17 * * MON-FRI` | Toutes les heures de 8h30 à 17h30 en semaine | Monitoring business hours |

### Déclenchement par événement

```bash
# Déclencher un job lorsqu'un fichier arrive
# Via Azure Event Grid + Logic App + Databricks API

# 1. Event Grid détecte nouveau fichier dans Blob Storage
# 2. Logic App reçoit l'événement
# 3. Logic App appelle l'API Databricks

# Exemple de déclenchement programmatique
import requests

def trigger_job_on_file_arrival(file_path):
    job_id = "12345"

    response = requests.post(
        f"{DATABRICKS_HOST}/api/2.1/jobs/run-now",
        headers=headers,
        json={
            "job_id": job_id,
            "notebook_params": {
                "file_path": file_path,
                "triggered_by": "event"
            }
        }
    )

    return response.json()["run_id"]
```

## 6. Monitoring et alertes

### Types de notifications

```bash
# Configuration des notifications
notification_config = {
    "email_notifications": {
        "on_start": ["team@company.com"],
        "on_success": ["team@company.com"],
        "on_failure": ["team@company.com", "oncall@company.com"],
        "on_duration_warning_threshold_exceeded": ["team@company.com"]
    },
    "webhook_notifications": {
        "on_failure": [{
            "id": "slack-webhook-id"
        }]
    }
}
```

### Monitoring des runs

```bash
# Obtenir le statut d'un run
run_status = requests.get(
    f"{DATABRICKS_HOST}/api/2.1/jobs/runs/get",
    headers=headers,
    params={"run_id": run_id}
).json()

print(f"State: {run_status['state']['life_cycle_state']}")
print(f"Result: {run_status['state'].get('result_state', 'N/A')}")

# Lister tous les runs d'un job
runs_list = requests.get(
    f"{DATABRICKS_HOST}/api/2.1/jobs/runs/list",
    headers=headers,
    params={"job_id": job_id, "limit": 25}
).json()

for run in runs_list.get("runs", []):
    print(f"Run {run['run_id']}: {run['state']['result_state']}")

# Annuler un run en cours
requests.post(
    f"{DATABRICKS_HOST}/api/2.1/jobs/runs/cancel",
    headers=headers,
    json={"run_id": run_id}
)
```

### Métriques et dashboards

#### Métriques clés à surveiller

- **Success Rate :** Taux de réussite des runs
- **Duration :** Temps d'exécution (détection de dégradation)
- **Cost :** Coût DBU par job
- **Failures :** Nombre et type d'échecs
- **SLA Compliance :** Respect des SLA de temps

## 7. Intégration Azure Data Factory

Vous pouvez orchestrer Databricks depuis Azure Data Factory pour une intégration complète avec l'écosystème Azure.

```bash
{
  "name": "DatabricksPipeline",
  "properties": {
    "activities": [
      {
        "name": "RunDatabricksNotebook",
        "type": "DatabricksNotebook",
        "linkedServiceName": {
          "referenceName": "DatabricksLinkedService",
          "type": "LinkedServiceReference"
        },
        "typeProperties": {
          "notebookPath": "/Workspace/ETL/Transform",
          "baseParameters": {
            "date": "@formatDateTime(pipeline().TriggerTime, 'yyyy-MM-dd')",
            "environment": "production"
          }
        }
      },
      {
        "name": "RunSparkJob",
        "type": "DatabricksSparkJar",
        "dependsOn": [
          {
            "activity": "RunDatabricksNotebook",
            "dependencyConditions": ["Succeeded"]
          }
        ],
        "typeProperties": {
          "mainClassName": "com.company.etl.MainApp",
          "parameters": ["--date", "@formatDateTime(pipeline().TriggerTime, 'yyyy-MM-dd')"]
        }
      }
    ]
  }
}
```

### Avantages ADF vs Databricks Workflows

| Critère | Databricks Workflows | Azure Data Factory |
| --- | --- | --- |
| **Simplicité** | ✅ Natif, intégré | Interface visuelle ADF |
| **Intégration Azure** | Via API/connectors | ✅ Natif (Blob, SQL, etc.) |
| **Coût** | Inclus dans Databricks | Facturation ADF séparée |
| **Monitoring** | Databricks UI | ✅ Azure Monitor intégré |
| **Orchestration hybride** | Databricks uniquement | ✅ Multi-services Azure |

### 📌 Points clés à retenir

- Workflows orchestre vos pipelines avec tâches et dépendances
- Supporté plusieurs types de tâches : notebooks, scripts, SQL, dbt, DLT
- Planification flexible avec expressions Cron
- Gestion avancée des dépendances (séquentiel, parallèle, conditionnel)
- Monitoring complet avec notifications multi-canaux
- Intégration Azure Data Factory pour orchestration hybride
- API complète pour automatisation et CI/CD

#### Prochaine étape

Vos workflows sont automatisés ! Dans la **Partie 7**, découvrez le Machine Learning avec MLflow.