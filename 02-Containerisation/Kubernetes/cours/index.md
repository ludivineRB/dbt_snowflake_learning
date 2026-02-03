## Bienvenue dans la Formation Kubernetes

Cette formation complète vous permettra de maîtriser **Kubernetes**, la plateforme
d'orchestration de conteneurs la plus populaire. Apprenez à déployer, scaler et gérer des
applications conteneurisées en production.

### 🎯 Objectifs de la formation

- Comprendre Kubernetes et son architecture
- Maîtriser les concepts de base (Pods, Services, Deployments)
- Déployer et gérer des applications dans Kubernetes
- Gérer la configuration, les secrets et le stockage persistant
- Configurer le networking et l'exposition externe avec Ingress
- Mettre en production sur Azure Kubernetes Service (AKS)

### 📋 Prérequis

- Avoir suivi la formation Docker (ou connaissances équivalentes)
- Comprendre les conteneurs et les images Docker
- Notions de ligne de commande (bash/terminal)
- Concepts de base en réseaux et systèmes distribués

### 🔧 Configuration requise

- Un ordinateur avec au moins 8 Go de RAM
- Docker installé et fonctionnel
- 15 Go d'espace disque libre
- Compte Azure (optionnel, pour la partie AKS)

1
10 min

### 📚 Introduction à Kubernetes

Découvrez Kubernetes, ses avantages et pourquoi il est essentiel pour les applications modernes.

- Qu'est-ce que Kubernetes ?
- Pourquoi utiliser K8s ?
- Docker vs Kubernetes
- Concepts clés

[Commencer →](parties/partie1.md)

2
8 min

### 🏗️ Architecture de Kubernetes

Comprenez l'architecture de Kubernetes avec le Control Plane et les Worker Nodes.

- Architecture globale
- Control Plane (Master)
- Worker Nodes
- Composants essentiels

[Commencer →](parties/partie2.md)

3
10 min

### 🚀 Installation et premiers pas

Installez Kubernetes localement avec Minikube et lancez votre première application.

- Options d'installation
- Installer Minikube et kubectl
- Commandes essentielles
- Premier déploiement

[Commencer →](parties/partie3.md)

4
12 min

### 📦 Pods et Deployments

Maîtrisez les Pods, Deployments et ReplicaSets pour gérer vos applications.

- Qu'est-ce qu'un Pod ?
- Deployments et ReplicaSets
- Scaling et rolling updates
- Stratégies de déploiement

[Commencer →](parties/partie4.md)

5
8 min

### 🌐 Services et networking

Configurez les Services pour exposer vos applications et gérer le networking.

- Types de Services
- ClusterIP, NodePort, LoadBalancer
- DNS dans Kubernetes
- Communication inter-pods

[Commencer →](parties/partie5.md)

6
8 min

### 🔐 ConfigMaps et Secrets

Gérez la configuration et les secrets de vos applications de manière sécurisée.

- ConfigMaps pour la configuration
- Secrets pour les données sensibles
- Injection dans les Pods
- Bonnes pratiques de sécurité

[Commencer →](parties/partie6.md)

7
8 min

### 💾 Volumes et persistence

Gérez la persistance des données avec les Volumes, PV et PVC.

- Types de Volumes
- PersistentVolume (PV)
- PersistentVolumeClaim (PVC)
- StorageClass et provisionnement dynamique

[Commencer →](parties/partie7.md)

8
6 min

### 🌍 Ingress et exposition externe

Exposez vos applications sur Internet avec Ingress et SSL/TLS.

- Qu'est-ce qu'un Ingress ?
- Installer un Ingress Controller
- Routing HTTP/HTTPS
- Configuration SSL/TLS

[Commencer →](parties/partie8.md)

9
10 min

### ☁️ Déploiement sur Azure (AKS)

Mettez en production vos applications sur Azure Kubernetes Service.

- Azure Kubernetes Service (AKS)
- Créer un cluster AKS
- Azure Container Registry (ACR)
- Best practices production

[Commencer →](parties/partie9.md)

## 🗺️ Parcours d'apprentissage

1-2

#### Fondamentaux

Comprendre Kubernetes

→

3

#### Installation

Environnement local

→

4-5

#### Core Concepts

Pods et Services

→

6-7

#### Configuration

Config et stockage

→

8-9

#### Production

Ingress et cloud

## 💡 Conseils pour réussir

#### 🎯 Pratiquez

Kubernetes s'apprend en pratiquant. Lancez un cluster local et testez chaque concept.

#### 📖 Lisez la doc

La documentation officielle Kubernetes est excellente. Consultez-la régulièrement.

#### 🔧 Utilisez kubectl

Maîtrisez kubectl, c'est votre outil principal pour interagir avec Kubernetes.

#### ☁️ Testez en cloud

Essayez un cluster managé (AKS, EKS, GKE) pour comprendre la production.

### 🎓 Prêt à commencer ?

Suivez les modules dans l'ordre pour une progression optimale. Kubernetes est complexe mais
très puissant une fois maîtrisé !

[Commencer la Partie 1 : Introduction →](parties/partie1.md)