# 02 - Configuration et Workspace

[← 01 - Introduction](01-introduction.md) | [🏠 Accueil](README.md) | [03 - Notebooks et langages →](03-notebooks-langages.md)

---

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
   - **Node type :** Standard\_DS3\_v2
   - **Workers :** Min 2, Max 8 (avec autoscaling)
   - **Auto Termination :** 20 minutes
4. Cliquez sur `Create Cluster`

## 4. Configurations de cluster avancées

### Spark Configuration

```bash
# Configuration Spark personnalisée dans le cluster
spark_conf = {
    "spark.sql.adaptive.enabled": "true",
    "spark.sql.adaptive.coalescePartitions.enabled": "true",
    "spark.databricks.delta.preview.enabled": "true",
    "spark.sql.shuffle.partitions": "auto"
}
```

### Autoscaling
L'autoscaling permet d'ajuster automatiquement le nombre de workers en fonction de la charge.

## 5. Optimisation des coûts

### Stratégies d'optimisation

| Stratégie | Description | Économies potentielles |
| --- | --- | --- |
| **Auto-termination** | Arrêter les clusters inactifs automatiquement | 30-50% sur clusters de dev |
| **Job Clusters** | Utiliser des job clusters au lieu d'all-purpose | 20-40% sur workloads batch |
| **Spot VMs** | Utiliser des VMs Azure Spot pour workers | 60-80% sur coût compute |

---

[← 01 - Introduction](01-introduction.md) | [🏠 Accueil](README.md) | [03 - Notebooks et langages →](03-notebooks-langages.md)
