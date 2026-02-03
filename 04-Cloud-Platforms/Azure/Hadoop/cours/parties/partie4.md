## 🎯 Objectifs d'Apprentissage

- Comprendre l'architecture de YARN
- Distinguer ResourceManager et NodeManager
- Maîtriser les concepts d'ApplicationMaster et Container
- Découvrir les schedulers YARN

## 📚 1. Qu'est-ce que YARN ?

**YARN** (Yet Another Resource Negotiator) est le gestionnaire de ressources de Hadoop 2.x et versions supérieures.
Il sépare la gestion des ressources du traitement des données.

### Pourquoi YARN ?

#### Problème dans Hadoop 1.x

Dans Hadoop 1.x, le **JobTracker** gérait à la fois :

- L'allocation des ressources du cluster
- La planification et le monitoring des jobs MapReduce

**Limites :** Goulot d'étranglement (scalabilité limitée à ~4000 nœuds),
support uniquement de MapReduce, pas d'autres frameworks.

#### Solution : YARN (Hadoop 2.x)

YARN sépare les responsabilités :

- **Gestion des ressources** : ResourceManager + NodeManagers
- **Gestion des applications** : ApplicationMaster par application

**Avantages :** Scalabilité > 10 000 nœuds, support multi-framework
(MapReduce, Spark, Tez, Storm, etc.)

### Hadoop 1.x vs Hadoop 2.x

| Aspect | Hadoop 1.x | Hadoop 2.x (YARN) |
| --- | --- | --- |
| Gestion de ressources | JobTracker | ResourceManager |
| Exécution locale | TaskTracker | NodeManager |
| Frameworks supportés | MapReduce uniquement | MapReduce, Spark, Tez, etc. |
| Scalabilité | ~4 000 nœuds | >10 000 nœuds |
| Utilisation des ressources | Slots fixes (map/reduce) | Conteneurs flexibles |

## 🏗️ 2. Architecture de YARN

### Composants Principaux

```bash
┌─────────────────────────────────────────────────────────────┐
│                        CLIENT                               │
│                   (Soumet l'application)                    │
└─────────────────────┬───────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────────────┐
│                   RESOURCE MANAGER                          │
│                      (Master Global)                        │
│                                                             │
│  ┌──────────────┐              ┌────────────────┐         │
│  │  Scheduler   │              │ ApplicationsManager │     │
│  └──────────────┘              └────────────────┘         │
└────────┬──────────────────────────────────────────┬────────┘
         │                                          │
         ↓                                          ↓
┌────────────────────┐                  ┌──────────────────────┐
│  NODE MANAGER 1    │                  │  NODE MANAGER N      │
│                    │                  │                      │
│  ┌──────────────┐  │                  │  ┌──────────────┐    │
│  │ Container 1  │  │                  │  │ Container 1  │    │
│  │ AppMaster    │  │                  │  │ Task         │    │
│  └──────────────┘  │                  │  └──────────────┘    │
│  ┌──────────────┐  │                  │  ┌──────────────┐    │
│  │ Container 2  │  │                  │  │ Container 2  │    │
│  │ Task         │  │                  │  │ Task         │    │
│  └──────────────┘  │                  │  └──────────────┘    │
└────────────────────┘                  └──────────────────────┘
```

### ResourceManager (RM)

Le **ResourceManager** est le maître global qui gère toutes les ressources du cluster.

#### Responsabilités :

- Allouer les ressources aux applications
- Maintenir un inventaire des ressources disponibles
- Planifier les applications (via le Scheduler)
- Gérer le cycle de vie des applications

#### Sous-composants :

- **Scheduler** : Alloue les ressources (CPU, mémoire) aux applications
- **ApplicationsManager** : Accepte les soumissions de jobs, négocie le premier conteneur pour l'ApplicationMaster

### NodeManager (NM)

Le **NodeManager** est l'agent qui s'exécute sur chaque nœud worker du cluster.

#### Responsabilités :

- Gérer les conteneurs sur son nœud
- Monitorer l'utilisation des ressources (CPU, mémoire, disque, réseau)
- Envoyer des heartbeats au ResourceManager
- Reporter l'état des conteneurs
- Gérer les logs des applications

### ApplicationMaster (AM)

L'**ApplicationMaster** est un processus spécifique à chaque application.

#### Responsabilités :

- Négocier les ressources avec le ResourceManager
- Travailler avec les NodeManagers pour exécuter et monitorer les tâches
- Gérer le cycle de vie de l'application
- Gérer les échecs de tâches et relancer si nécessaire

*Note : Chaque application (job MapReduce, application Spark, etc.) a son propre ApplicationMaster.*

### Container

Un **Container** est une unité d'allocation de ressources.

#### Caractéristiques :

- Encapsule des ressources : CPU (vcores) et mémoire (RAM)
- S'exécute sur un NodeManager
- Peut contenir un ApplicationMaster ou une tâche (Map, Reduce, Spark executor, etc.)

**Exemple :** Container avec 2 GB RAM et 1 vcore

## 🔄 3. Cycle de Vie d'une Application YARN

```bash
1. Client soumet une application au ResourceManager
   ↓
2. ResourceManager alloue un conteneur pour l'ApplicationMaster
   ↓
3. NodeManager lance l'ApplicationMaster dans ce conteneur
   ↓
4. ApplicationMaster s'enregistre auprès du ResourceManager
   ↓
5. ApplicationMaster demande des conteneurs pour les tâches
   ↓
6. ResourceManager (Scheduler) alloue les conteneurs
   ↓
7. ApplicationMaster contacte les NodeManagers pour lancer les conteneurs
   ↓
8. NodeManagers lancent les conteneurs et exécutent les tâches
   ↓
9. Tâches reportent leur statut à l'ApplicationMaster
   ↓
10. ApplicationMaster reporte le progrès au ResourceManager
   ↓
11. Une fois terminé, ApplicationMaster se désenregistre
   ↓
12. NodeManagers nettoient les conteneurs
```

#### Exemple Concret : Job MapReduce

1. Client soumet un job MapReduce
2. RM alloue un conteneur pour le MR ApplicationMaster
3. MR AppMaster démarre et calcule les splits d'entrée
4. MR AppMaster demande des conteneurs pour les mappers et reducers
5. RM alloue les conteneurs demandés
6. NMs lancent les tâches Map et Reduce
7. MR AppMaster monitore le progrès
8. À la fin, MR AppMaster se désenregistre

## 📅 4. Schedulers YARN

Le **Scheduler** détermine quelle application reçoit des ressources et quand.

### Types de Schedulers

#### 1. FIFO Scheduler

**First In, First Out** - Le plus simple.

- Les applications sont servies dans l'ordre de soumission
- Une application monopolise toutes les ressources jusqu'à sa fin

**Avantage :** Simple

**Inconvénient :** Pas de multitâche, petites applications attendent longtemps

*Rarement utilisé en production.*

#### 2. Capacity Scheduler

Divise le cluster en **queues** (files d'attente) avec des capacités garanties.

- Chaque queue a un pourcentage minimum de ressources
- Les ressources inutilisées peuvent être partagées (élasticité)
- Hiérarchie de queues possible
- ACLs (contrôles d'accès) par queue

**Exemple :**

- Queue "production" : 70% des ressources
- Queue "dev" : 20%
- Queue "test" : 10%

*Scheduler par défaut dans la plupart des distributions Hadoop.*

#### 3. Fair Scheduler

Partage équitablement les ressources entre toutes les applications actives.

- Chaque application reçoit environ la même quantité de ressources
- Support des pools (similaire aux queues)
- Possibilité de définir des poids et des priorités
- Préemption : peut tuer des conteneurs pour équilibrer

**Avantage :** Équité entre utilisateurs et applications

*Utilisé par défaut dans Cloudera (CDH).*

### Comparaison des Schedulers

| Caractéristique | FIFO | Capacity | Fair |
| --- | --- | --- | --- |
| Multitâche | ❌ | ✅ | ✅ |
| Partage de ressources | ❌ | Par queue | Équitable |
| Élasticité | ❌ | ✅ | ✅ |
| Préemption | ❌ | Optionnel | ✅ |
| Complexité configuration | Faible | Moyenne | Moyenne |
| Cas d'usage | Test/Dev | Multi-tenant avec SLA | Partage équitable |

## 🖥️ 5. Monitoring YARN

### YARN Web UI

Interface web pour monitorer le cluster YARN.

```bash
# Accéder à l'interface Web du ResourceManager
http://<resourcemanager-host>:8088
```

#### Informations Disponibles :

#### 📊 Cluster Metrics

- Mémoire totale/utilisée/disponible
- VCores totaux/utilisés/disponibles
- Nombre de NodeManagers actifs

#### 📱 Applications

- Applications en cours, terminées, échouées
- Progrès de chaque application
- Logs et diagnostics

#### 📂 Queues

- Utilisation par queue
- Applications en attente par queue
- Capacité utilisée vs disponible

#### 🖥️ Nodes

- État de chaque NodeManager
- Ressources utilisées par nœud
- Conteneurs actifs par nœud

### Commandes CLI

| Commande | Description |
| --- | --- |
| `yarn node -list` | Lister tous les NodeManagers |
| `yarn application -list` | Lister les applications en cours |
| `yarn application -status <app-id>` | Voir le statut d'une application |
| `yarn application -kill <app-id>` | Tuer une application |
| `yarn logs -applicationId <app-id>` | Voir les logs d'une application |
| `yarn queue -status <queue-name>` | Voir le statut d'une queue |

## ⚙️ 6. Configuration YARN

Fichier principal : `yarn-site.xml`

### Paramètres Importants

```bash
<configuration>
    <!-- Adresse du ResourceManager -->
    <property>
        <name>yarn.resourcemanager.hostname</name>
        <value>master.example.com</value>
    </property>

    <!-- Mémoire totale par NodeManager -->
    <property>
        <name>yarn.nodemanager.resource.memory-mb</name>
        <value>8192</value>
    </property>

    <!-- VCores totaux par NodeManager -->
    <property>
        <name>yarn.nodemanager.resource.cpu-vcores</name>
        <value>4</value>
    </property>

    <!-- Scheduler à utiliser -->
    <property>
        <name>yarn.resourcemanager.scheduler.class</name>
        <value>org.apache.hadoop.yarn.server.resourcemanager.scheduler.capacity.CapacityScheduler</value>
    </property>

    <!-- Mémoire minimum par conteneur -->
    <property>
        <name>yarn.scheduler.minimum-allocation-mb</name>
        <value>1024</value>
    </property>

    <!-- Mémoire maximum par conteneur -->
    <property>
        <name>yarn.scheduler.maximum-allocation-mb</name>
        <value>8192</value>
    </property>
</configuration>
```

## 📝 Résumé de la Partie 4

### Points Clés à Retenir

- YARN sépare la gestion des ressources du traitement des données
- Architecture : ResourceManager (maître) + NodeManagers (workers)
- Chaque application a son propre ApplicationMaster
- Les Containers sont les unités d'allocation de ressources
- 3 schedulers : FIFO (simple), Capacity (queues), Fair (équitable)
- YARN permet de faire cohabiter plusieurs frameworks (MapReduce, Spark, etc.)
- Monitoring via Web UI (port 8088) et commandes yarn CLI

#### ✅ Prêt pour la Suite ?

Vous maîtrisez maintenant YARN ! Dans la partie suivante, nous explorerons **l'écosystème Hadoop** avec des outils comme Hive, Pig, HBase et plus encore.