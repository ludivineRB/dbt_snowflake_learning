# 01 - Introduction à Kubernetes

[🏠 Accueil](README.md) | [02 - Architecture →](02-architecture-k8s.md)

---

## 1. Introduction à Kubernetes

### Qu'est-ce que Kubernetes ?

**Kubernetes** (K8s) est une plateforme open-source d'orchestration de conteneurs développée par Google et maintenue par la CNCF (Cloud Native Computing Foundation). Il automatise le déploiement, la mise à l'échelle et la gestion des applications conteneurisées.

#### Pourquoi K8s ?
Le nom "K8s" vient de "K" + 8 lettres (ubernete) + "s". C'est une abréviation courante dans la communauté.

### Pourquoi utiliser Kubernetes ?

#### 🔄 Auto-scaling
Scale automatiquement vos applications en fonction de la charge (CPU, mémoire, métriques custom).

#### 🏥 Self-healing
Redémarre automatiquement les conteneurs qui échouent, remplace et re-schedule.

#### 🚀 Déploiements automatisés
Rolling updates, rollbacks automatiques, zero-downtime deployments.

#### ⚖️ Load Balancing
Distribution automatique du trafic entre les conteneurs.

#### 🔐 Gestion des secrets
Stockage sécurisé des mots de passe, tokens, clés SSH.

#### ☁️ Multi-cloud
Fonctionne sur AWS, Azure, GCP, on-premise de manière uniforme.

---

### Docker vs Kubernetes

| Aspect | Docker | Kubernetes |
| --- | --- | --- |
| **Rôle** | Conteneurisation | Orchestration de conteneurs |
| **Scope** | Machine unique | Cluster de machines |
| **Scaling** | Manuel | Automatique |
| **High Availability** | Non natif | Oui, natif |
| **Networking** | Simple | Avancé (Services, Ingress) |

#### Complémentaires
Docker et Kubernetes ne sont pas en compétition ! Kubernetes utilise Docker (ou containerd, CRI-O) comme runtime pour exécuter les conteneurs.

---

### Concepts clés

| Concept | Description |
| --- | --- |
| **Cluster** | Ensemble de machines (nodes) qui exécutent des conteneurs |
| **Node** | Machine (VM ou physique) dans le cluster |
| **Pod** | Plus petite unité déployable, contient un ou plusieurs conteneurs |
| **Deployment** | Déclare l'état désiré des Pods (nombre de replicas, image, etc.) |
| **Service** | Point d'accès stable pour communiquer avec des Pods |
| **Namespace** | Isolation virtuelle des ressources dans un cluster |

### 💡 Points clés à retenir
- Kubernetes est une plateforme d'orchestration de conteneurs.
- Il automatise le déploiement, le scaling et la gestion des applications.
- K8s offre auto-scaling, self-healing et rolling updates.
- Docker et Kubernetes sont complémentaires.
- Les concepts de base sont : Cluster, Node, Pod, Deployment, Service.

---

[🏠 Accueil](README.md) | [02 - Architecture →](02-architecture-k8s.md)