## 🎯 Objectifs d'apprentissage

- Créer un workspace Azure Databricks
- Comprendre les différentes options de configuration
- Configurer la sécurité réseau et les accès
- Créer et gérer des clusters Spark
- Optimiser les coûts avec autoscaling et terminaison automatique

## 1. Création d'un workspace Databricks

### Prérequis

- Un abonnement Azure actif
- Les permissions pour créer des ressources (Contributor ou Owner)
- Un groupe de ressources Azure

### Étapes de création via le portail Azure

#### Création d'un workspace

1. **Accédez au portail Azure** (portal.azure.com)
2. Cliquez sur `+ Créer une ressource`
3. Recherchez "Azure Databricks"
4. Cliquez sur `Créer`
5. Remplissez les informations de base :
   - **Abonnement :** Sélectionnez votre abonnement
   - **Groupe de ressources :** Créez ou sélectionnez un groupe existant
   - **Nom du workspace :** Par exemple "databricks-prod-workspace"
   - **Région :** Choisissez une région proche de vos données (ex: West Europe)
   - **Niveau tarifaire :** Standard, Premium ou Trial

### Niveaux tarifaires

| Niveau | Fonctionnalités | Cas d'usage |
| --- | --- | --- |
| **Trial** | • 14 jours gratuits  • Fonctionnalités Premium  • Limité en ressources | Tests et POC |
| **Standard** | • Clusters Spark  • Notebooks  • Jobs scheduling  • RBAC basique | Data Engineering de base |
| **Premium** | • Tout du Standard +  • RBAC avancé  • Azure AD intégration  • Audit logs  • Secrets management | Production enterprise |

#### Recommandation

Pour un usage en production, choisissez toujours le niveau **Premium** qui offre des fonctionnalités de sécurité et gouvernance essentielles.

## 2. Configuration réseau et sécurité

### Options de déploiement réseau

#### Déploiement standard

**VNet managé par Databricks**

- Configuration automatique
- Rapide à déployer
- Moins de contrôle

#### VNet Injection

**Votre propre VNet Azure**

- Contrôle total du réseau
- Intégration avec infrastructure existante
- Configuration NSG personnalisée

### Configuration VNet Injection

#### Prérequis pour VNet Injection

1. **Créer un VNet avec au moins 2 subnets via le portail Azure :**
   - **Subnet privé pour les workers :** minimum /26 (ex: 10.0.1.0/26)
   - **Subnet public pour le control plane :** minimum /26 (ex: 10.0.2.0/26)
2. **Déléguer les subnets à Databricks :**
   - Dans chaque subnet, aller dans "Délégations de service"
   - Sélectionner "Microsoft.Databricks/workspaces"
3. **Lors de la création du workspace Databricks :**
   - Cocher "Déployer Azure Databricks dans votre réseau virtuel"
   - Sélectionner le VNet et les subnets créés

#### Important : Taille des subnets

Chaque subnet doit avoir au moins un préfixe /26 (64 adresses) pour permettre la création de clusters. Pour les environnements de production, utilisez au minimum /24.

### Sécurité avec Azure AD

#### Configuration de l'authentification

En niveau Premium, l'authentification Azure AD est activée automatiquement. Les utilisateurs se connectent avec leurs identifiants Azure AD existants.

L'attribution des rôles et permissions se fait via le portail Azure dans la section "Contrôle d'accès (IAM)" de votre workspace Databricks.

## 3. Gestion des clusters

### Types de clusters

| Type | Description | Cas d'usage |
| --- | --- | --- |
| **All-Purpose Cluster** | • Cluster interactif  • Partagé entre utilisateurs  • Persiste entre exécutions | • Développement  • Exploration de données  • Notebooks interactifs |
| **Job Cluster** | • Créé automatiquement  • Terminé après le job  • Optimisé pour une tâche | • Jobs automatisés  • Pipelines de production  • Optimisation des coûts |

### Création d'un cluster via l'interface

#### Créer un cluster All-Purpose

1. Dans votre workspace, cliquez sur `Compute` dans la barre latérale
2. Cliquez sur `Create Cluster`
3. Configurez :
   - **Cluster name :** "dev-cluster"
   - **Cluster mode :** Standard
   - **Databricks Runtime Version :** 13.3 LTS (ou plus récent)
   - **Node type :** Standard\_DS3\_v2 (ou selon vos besoins)
   - **Workers :** Min 2, Max 8 (avec autoscaling)
   - **Auto Termination :** 20 minutes
4. Cliquez sur `Create Cluster`

### Configuration via l'API Databricks

```bash
# Création de cluster via l'API Databricks
import requests
import json

DATABRICKS_HOST = "https://<workspace-url>"
DATABRICKS_TOKEN = "<your-token>"

cluster_config = {
    "cluster_name": "production-cluster",
    "spark_version": "13.3.x-scala2.12",
    "node_type_id": "Standard_DS3_v2",
    "num_workers": 2,
    "autoscale": {
        "min_workers": 2,
        "max_workers": 8
    },
    "auto_termination_minutes": 30,
    "enable_elastic_disk": True,
    "cluster_source": "API"
}

headers = {
    "Authorization": f"Bearer {DATABRICKS_TOKEN}",
    "Content-Type": "application/json"
}

response = requests.post(
    f"{DATABRICKS_HOST}/api/2.0/clusters/create",
    headers=headers,
    json=cluster_config
)

cluster_id = response.json()["cluster_id"]
print(f"Cluster créé avec l'ID : {cluster_id}")
```

## 4. Configurations de cluster avancées

### Types de VMs recommandés

| Workload | VM Type | Caractéristiques |
| --- | --- | --- |
| Data Engineering général | Standard\_DS3\_v2 | 4 vCPU, 14 GB RAM - Équilibré |
| Calcul intensif | Standard\_F8s\_v2 | 8 vCPU, 16 GB RAM - Optimisé CPU |
| Machine Learning | Standard\_NC6s\_v3 | 6 vCPU, GPU V100 - Accélération GPU |
| Mémoire intensive | Standard\_E8s\_v3 | 8 vCPU, 64 GB RAM - Haute mémoire |

### Spark Configuration

```bash
# Configuration Spark personnalisée dans le cluster
spark_conf = {
    "spark.sql.adaptive.enabled": "true",
    "spark.sql.adaptive.coalescePartitions.enabled": "true",
    "spark.databricks.delta.preview.enabled": "true",
    "spark.sql.shuffle.partitions": "auto"
}

# Variables d'environnement
env_vars = {
    "PYSPARK_PYTHON": "/databricks/python3/bin/python3",
    "ENV": "production"
}

# Init Scripts pour installer des dépendances
init_scripts = [{
    "dbfs": {
        "destination": "dbfs:/databricks/init-scripts/install-libs.sh"
    }
}]
```

### Autoscaling

L'autoscaling permet d'ajuster automatiquement le nombre de workers en fonction de la charge :

#### Avantages

- Optimisation automatique des coûts
- Performance adaptée à la charge
- Pas de sur-provisionnement

#### Configuration recommandée

- Min workers : 2 (haute disponibilité)
- Max workers : 8-16 (selon budget)
- Scale down : 10 minutes d'inactivité

```bash
{
  "autoscale": {
    "min_workers": 2,
    "max_workers": 10
  },
  "auto_termination_minutes": 30
}
```

## 5. Optimisation des coûts

### Stratégies d'optimisation

| Stratégie | Description | Économies potentielles |
| --- | --- | --- |
| **Auto-termination** | Arrêter les clusters inactifs automatiquement | 30-50% sur clusters de dev |
| **Job Clusters** | Utiliser des job clusters au lieu d'all-purpose | 20-40% sur workloads batch |
| **Instance Pools** | Réutiliser des VMs pré-provisionnées | Démarrage 4x plus rapide |
| **Spot VMs** | Utiliser des VMs Azure Spot pour workers | 60-80% sur coût compute |
| **Photon Engine** | Moteur vectorisé C++ (Premium tier) | Performances 2-4x meilleures |

#### Bonnes pratiques de coûts

- Toujours activer l'auto-termination (recommandé : 20-30 minutes)
- Utiliser des job clusters pour les pipelines de production
- Dimensionner les clusters en fonction de la charge réelle
- Monitorer l'utilisation avec Azure Cost Management
- Utiliser des tags pour tracker les coûts par projet/équipe

### Configuration Spot VMs

```bash
# Configuration de cluster avec Spot VMs pour les workers
cluster_config_spot = {
    "cluster_name": "spot-cluster",
    "spark_version": "13.3.x-scala2.12",
    "node_type_id": "Standard_DS3_v2",
    "driver_node_type_id": "Standard_DS3_v2",  # Driver on-demand
    "num_workers": 4,
    "autoscale": {
        "min_workers": 2,
        "max_workers": 10
    },
    "azure_attributes": {
        "availability": "SPOT_WITH_FALLBACK_AZURE",  # Spot avec fallback on-demand
        "first_on_demand": 1,  # Driver toujours on-demand
        "spot_bid_max_price": -1  # Prix max = prix on-demand
    }
}
```

### 📌 Points clés à retenir

- Choisissez Premium tier pour la production (sécurité et gouvernance)
- VNet Injection offre un contrôle réseau complet
- All-Purpose clusters pour le dev, Job clusters pour la production
- Activez toujours l'autoscaling et auto-termination
- Utilisez Spot VMs pour réduire les coûts de 60-80%
- Dimensionnez vos clusters selon la charge réelle

#### Prochaine étape

Votre workspace est configuré ! Dans la **Partie 3**, vous allez créer votre premier notebook et découvrir les différents langages supportés.