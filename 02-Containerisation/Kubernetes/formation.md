## Objectifs de la formation

- Comprendre Kubernetes et son architecture
- Maîtriser les concepts de base (Pods, Services, Deployments)
- Déployer des applications dans Kubernetes
- Gérer la configuration et les secrets
- Configurer le networking et l'ingress
- Mettre en production sur Azure (AKS)

## 1. Introduction à Kubernetes

### Qu'est-ce que Kubernetes ?

**Kubernetes** (K8s) est une plateforme open-source d'orchestration de conteneurs
développée par Google et maintenue par la CNCF (Cloud Native Computing Foundation). Il automatise
le déploiement, la mise à l'échelle et la gestion des applications conteneurisées.

#### Pourquoi K8s ?

Le nom "K8s" vient de "K" + 8 lettres (ubernete) + "s".
C'est une abréviation courante dans la communauté.

### Pourquoi utiliser Kubernetes ?

#### 🔄 Auto-scaling

Scale automatiquement vos applications en fonction de la charge (CPU, mémoire, métriques custom)

#### 🏥 Self-healing

Redémarre automatiquement les conteneurs qui échouent, remplace et re-schedule

#### 🚀 Déploiements automatisés

Rolling updates, rollbacks automatiques, zero-downtime deployments

#### ⚖️ Load Balancing

Distribution automatique du trafic entre les conteneurs

#### 🔐 Gestion des secrets

Stockage sécurisé des mots de passe, tokens, clés SSH

#### ☁️ Multi-cloud

Fonctionne sur AWS, Azure, GCP, on-premise de manière uniforme

### Docker vs Kubernetes

| Aspect | Docker | Kubernetes |
| --- | --- | --- |
| **Rôle** | Conteneurisation | Orchestration de conteneurs |
| **Scope** | Machine unique | Cluster de machines |
| **Scaling** | Manuel | Automatique |
| **High Availability** | Non natif | Oui, natif |
| **Networking** | Simple | Avancé (Services, Ingress) |

#### Complémentaires

Docker et Kubernetes ne sont pas en compétition ! Kubernetes utilise Docker
(ou containerd, CRI-O) comme runtime pour exécuter les conteneurs.

### Concepts clés

| Concept | Description |
| --- | --- |
| **Cluster** | Ensemble de machines (nodes) qui exécutent des conteneurs |
| **Node** | Machine (VM ou physique) dans le cluster |
| **Pod** | Plus petite unité déployable, contient un ou plusieurs conteneurs |
| **Deployment** | Déclare l'état désiré des Pods (nombre de replicas, image, etc.) |
| **Service** | Point d'accès stable pour communiquer avec des Pods |
| **Namespace** | Isolation virtuelle des ressources dans un cluster |

## 2. Architecture de Kubernetes

### Architecture globale

```bash
┌────────────────────────────────────────────────────────────────┐
│                       KUBERNETES CLUSTER                        │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │              CONTROL PLANE (Master Node)                 │  │
│  │                                                           │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │  │
│  │  │  API Server  │  │  Scheduler   │  │  Controller  │  │  │
│  │  │              │  │              │  │   Manager    │  │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘  │  │
│  │                                                           │  │
│  │  ┌──────────────────────────────────────────────────┐   │  │
│  │  │              etcd (State Store)                    │   │  │
│  │  └──────────────────────────────────────────────────┘   │  │
│  └─────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │                    WORKER NODES                          │  │
│  │                                                           │  │
│  │  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   │  │
│  │  │   Node 1    │   │   Node 2    │   │   Node 3    │   │  │
│  │  │             │   │             │   │             │   │  │
│  │  │  ┌───────┐  │   │  ┌───────┐  │   │  ┌───────┐  │   │  │
│  │  │  │ Pod 1 │  │   │  │ Pod 3 │  │   │  │ Pod 5 │  │   │  │
│  │  │  └───────┘  │   │  └───────┘  │   │  └───────┘  │   │  │
│  │  │  ┌───────┐  │   │  ┌───────┐  │   │  ┌───────┐  │   │  │
│  │  │  │ Pod 2 │  │   │  │ Pod 4 │  │   │  │ Pod 6 │  │   │  │
│  │  │  └───────┘  │   │  └───────┘  │   │  └───────┘  │   │  │
│  │  │             │   │             │   │             │   │  │
│  │  │  kubelet    │   │  kubelet    │   │  kubelet    │   │  │
│  │  │  kube-proxy │   │  kube-proxy │   │  kube-proxy │   │  │
│  │  └─────────────┘   └─────────────┘   └─────────────┘   │  │
│  └─────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────┘
```

### Control Plane (Master Node)

Le **Control Plane** gère le cluster et prend toutes les décisions :

| Composant | Rôle |
| --- | --- |
| **API Server** | Point d'entrée pour toutes les commandes (kubectl, dashboards). Interface REST |
| **etcd** | Base de données clé-valeur qui stocke l'état du cluster |
| **Scheduler** | Décide sur quel Node placer les nouveaux Pods |
| **Controller Manager** | Exécute les controllers (Node, Replication, Endpoints, etc.) |
| **Cloud Controller Manager** | Interactions avec les APIs cloud (AWS, Azure, GCP) |

### Worker Nodes

Les **Worker Nodes** exécutent les applications :

| Composant | Rôle |
| --- | --- |
| **kubelet** | Agent qui s'assure que les conteneurs tournent dans les Pods |
| **kube-proxy** | Gère le networking et le load balancing des Services |
| **Container Runtime** | Moteur de conteneurs (Docker, containerd, CRI-O) |

#### Managed Kubernetes

Avec les services managés (AKS, EKS, GKE), le Control Plane est géré par le provider.
Vous ne gérez que les Worker Nodes (et parfois même pas avec les node pools auto-managés).

## 3. Installation et premiers pas

### Options d'installation

#### 💻 Minikube

Cluster local sur votre machine, parfait pour le développement

#### 🐳 Docker Desktop

Kubernetes intégré à Docker Desktop (Mac/Windows)

#### 🎯 Kind

Kubernetes in Docker, léger et rapide pour les tests

#### ☁️ Cloud managé

AKS (Azure), EKS (AWS), GKE (Google)

### Installation Minikube

```bash
# macOS
brew install minikube kubectl

# Linux
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Windows (avec Chocolatey)
choco install minikube kubernetes-cli

# Démarrer Minikube
minikube start

# Vérifier l'installation
kubectl version --client
kubectl cluster-info
kubectl get nodes
```

### Installation kubectl

**kubectl** est l'outil en ligne de commande pour interagir avec Kubernetes :

```bash
# macOS
brew install kubectl

# Linux
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Windows (avec Chocolatey)
choco install kubernetes-cli

# Vérifier
kubectl version --client

# Configuration (pointe vers votre cluster)
kubectl config view
kubectl config get-contexts
kubectl config use-context minikube
```

### Commandes kubectl essentielles

| Commande | Description |
| --- | --- |
| `kubectl get pods` | Lister tous les Pods |
| `kubectl get services` | Lister tous les Services |
| `kubectl get deployments` | Lister tous les Deployments |
| `kubectl describe pod <name>` | Détails d'un Pod |
| `kubectl logs <pod>` | Voir les logs d'un Pod |
| `kubectl exec -it <pod> -- bash` | Se connecter à un Pod |
| `kubectl apply -f <file.yaml>` | Appliquer une configuration |
| `kubectl delete -f <file.yaml>` | Supprimer des ressources |

### Premier déploiement

```bash
# Déployer nginx
kubectl create deployment nginx --image=nginx:latest

# Vérifier le déploiement
kubectl get deployments
kubectl get pods

# Exposer via un Service
kubectl expose deployment nginx --port=80 --type=NodePort

# Obtenir l'URL du service (avec Minikube)
minikube service nginx --url

# Tester
curl $(minikube service nginx --url)

# Nettoyer
kubectl delete service nginx
kubectl delete deployment nginx
```

#### Félicitations !

Vous venez de déployer votre première application sur Kubernetes !
Kubernetes a automatiquement créé un Pod, l'a assigné à un Node, et l'a exposé via un Service.

## 4. Pods et Deployments

### Qu'est-ce qu'un Pod ?

Un **Pod** est la plus petite unité déployable dans Kubernetes.
Il contient un ou plusieurs conteneurs qui partagent le même réseau et le même stockage.

#### Pod simple (YAML)

```bash
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
  labels:
    app: nginx
spec:
  containers:
  - name: nginx
    image: nginx:1.25
    ports:
    - containerPort: 80
```

```bash
# Créer le Pod
kubectl apply -f nginx-pod.yaml

# Vérifier
kubectl get pods
kubectl describe pod nginx-pod

# Voir les logs
kubectl logs nginx-pod

# Se connecter au Pod
kubectl exec -it nginx-pod -- bash

# Supprimer
kubectl delete pod nginx-pod
```

#### Ne pas utiliser les Pods seuls

En production, on n'utilise presque jamais de Pods directement.
On utilise des **Deployments** qui gèrent les Pods automatiquement.

### Deployments

Un **Deployment** déclare l'état désiré de vos Pods et gère leur cycle de vie
(création, mise à jour, scaling, self-healing).

```bash
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: 3  # Nombre de Pods
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.25
        ports:
        - containerPort: 80
        resources:
          requests:
            memory: "64Mi"
            cpu: "250m"
          limits:
            memory: "128Mi"
            cpu: "500m"
```

```bash
# Créer le Deployment
kubectl apply -f nginx-deployment.yaml

# Vérifier
kubectl get deployments
kubectl get pods  # 3 Pods créés

# Voir le rollout status
kubectl rollout status deployment/nginx-deployment

# Scaler manuellement
kubectl scale deployment nginx-deployment --replicas=5

# Mettre à jour l'image
kubectl set image deployment/nginx-deployment nginx=nginx:1.26

# Voir l'historique des déploiements
kubectl rollout history deployment/nginx-deployment

# Rollback vers la version précédente
kubectl rollout undo deployment/nginx-deployment

# Supprimer
kubectl delete deployment nginx-deployment
```

### ReplicaSet

Un **ReplicaSet** assure qu'un nombre spécifié de réplicas de Pods est toujours en cours d'exécution.
Les Deployments créent et gèrent automatiquement des ReplicaSets.

```bash
# Voir les ReplicaSets
kubectl get replicasets

# Un ReplicaSet a été créé automatiquement par le Deployment
# nginx-deployment-xxxxxxxxxx   3         3         3       5m
```

### Stratégies de déploiement

```bash
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 3
  strategy:
    type: RollingUpdate  # ou Recreate
    rollingUpdate:
      maxSurge: 1        # Nombre max de Pods en plus pendant le rollout
      maxUnavailable: 1  # Nombre max de Pods indisponibles pendant le rollout
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.25
        ports:
        - containerPort: 80
```

| Stratégie | Description | Cas d'usage |
| --- | --- | --- |
| **RollingUpdate** | Remplace progressivement les anciens Pods par des nouveaux | Par défaut, zero-downtime |
| **Recreate** | Supprime tous les anciens Pods avant de créer les nouveaux | Quand les versions ne peuvent pas coexister |

## 5. Services et networking

### Qu'est-ce qu'un Service ?

Un **Service** est une abstraction qui définit un moyen d'accéder à un ensemble de Pods.
Les Pods sont éphémères (IPs changeantes), mais les Services fournissent une adresse stable.

### Types de Services

| Type | Description | Cas d'usage |
| --- | --- | --- |
| **ClusterIP** | IP interne au cluster (par défaut) | Communication interne entre services |
| **NodePort** | Expose le service sur un port de chaque Node | Accès externe simple (dev/test) |
| **LoadBalancer** | Crée un load balancer externe (cloud) | Production avec cloud provider |
| **ExternalName** | Alias DNS vers un service externe | Pointer vers des services hors cluster |

#### Service ClusterIP

```bash
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  type: ClusterIP  # Par défaut
  selector:
    app: nginx  # Sélectionne les Pods avec ce label
  ports:
  - protocol: TCP
    port: 80        # Port du Service
    targetPort: 80  # Port du conteneur
```

#### Service NodePort

```bash
apiVersion: v1
kind: Service
metadata:
  name: nginx-nodeport
spec:
  type: NodePort
  selector:
    app: nginx
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
    nodePort: 30080  # Port sur les Nodes (30000-32767)
```

#### Service LoadBalancer

```bash
apiVersion: v1
kind: Service
metadata:
  name: nginx-loadbalancer
spec:
  type: LoadBalancer
  selector:
    app: nginx
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
```

```bash
# Créer les Services
kubectl apply -f nginx-service.yaml

# Lister les Services
kubectl get services

# Détails d'un Service
kubectl describe service nginx-service

# Tester depuis un Pod dans le cluster
kubectl run -it --rm debug --image=busybox --restart=Never -- sh
wget -O- nginx-service

# Avec NodePort (Minikube)
minikube service nginx-nodeport --url
curl $(minikube service nginx-nodeport --url)
```

### DNS dans Kubernetes

Kubernetes fournit un serveur DNS interne. Chaque Service obtient automatiquement un nom DNS :

```bash
# Format DNS
..svc.cluster.local

# Exemples
nginx-service.default.svc.cluster.local
database.production.svc.cluster.local

# Dans le même namespace, on peut juste utiliser le nom
curl http://nginx-service
```

## 6. ConfigMaps et Secrets

### ConfigMaps

Les **ConfigMaps** permettent de stocker des données de configuration non confidentielles
(fichiers de config, variables d'environnement).

```bash
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
# Variables simples
  DATABASE_HOST: "postgres.default.svc.cluster.local"
  DATABASE_PORT: "5432"
  APP_ENV: "production"

# Fichier de configuration
  app.conf: |
    server {
      listen 80;
      server_name example.com;
    }
```

#### Utiliser un ConfigMap dans un Pod

```bash
apiVersion: v1
kind: Pod
metadata:
  name: myapp
spec:
  containers:
  - name: app
    image: myapp:1.0
# Méthode 1: Variables d'environnement
    env:
    - name: DATABASE_HOST
      valueFrom:
        configMapKeyRef:
          name: app-config
          key: DATABASE_HOST

# Méthode 2: Toutes les clés en variables d'env
    envFrom:
    - configMapRef:
        name: app-config

# Méthode 3: Monter comme fichiers
    volumeMounts:
    - name: config-volume
      mountPath: /etc/config

  volumes:
  - name: config-volume
    configMap:
      name: app-config
```

```bash
# Créer un ConfigMap depuis kubectl
kubectl create configmap app-config \
  --from-literal=DATABASE_HOST=postgres \
  --from-literal=DATABASE_PORT=5432

# Depuis un fichier
kubectl create configmap nginx-config --from-file=nginx.conf

# Voir les ConfigMaps
kubectl get configmaps
kubectl describe configmap app-config

# Supprimer
kubectl delete configmap app-config
```

### Secrets

Les **Secrets** stockent des données sensibles (mots de passe, tokens, clés SSH).
Les données sont encodées en base64 (pas chiffrées par défaut !).

```bash
apiVersion: v1
kind: Secret
metadata:
  name: db-credentials
type: Opaque
data:
# Valeurs en base64
  username: YWRtaW4=       # admin
  password: cGFzc3dvcmQ=   # password
```

```bash
# Créer un Secret depuis kubectl
kubectl create secret generic db-credentials \
  --from-literal=username=admin \
  --from-literal=password=secret123

# Encoder/décoder base64
echo -n "admin" | base64      # YWRtaW4=
echo "YWRtaW4=" | base64 -d   # admin

# Voir les Secrets (valeurs cachées)
kubectl get secrets
kubectl describe secret db-credentials

# Voir les valeurs (nécessite les permissions)
kubectl get secret db-credentials -o yaml
```

#### Utiliser un Secret dans un Pod

```bash
apiVersion: v1
kind: Pod
metadata:
  name: myapp
spec:
  containers:
  - name: app
    image: myapp:1.0
    env:
    - name: DB_USERNAME
      valueFrom:
        secretKeyRef:
          name: db-credentials
          key: username
    - name: DB_PASSWORD
      valueFrom:
        secretKeyRef:
          name: db-credentials
          key: password

# Ou monter comme fichiers
    volumeMounts:
    - name: secret-volume
      mountPath: /etc/secrets
      readOnly: true

  volumes:
  - name: secret-volume
    secret:
      secretName: db-credentials
```

#### Sécurité des Secrets

Par défaut, les Secrets sont encodés en base64, pas chiffrés !
En production, utilisez :

- Encryption at rest (chiffrement dans etcd)
- Azure Key Vault, AWS Secrets Manager, ou HashiCorp Vault
- Sealed Secrets pour versionner les secrets de manière sécurisée

## 7. Volumes et persistence des données

### Types de Volumes

| Type | Description | Cas d'usage |
| --- | --- | --- |
| **emptyDir** | Volume temporaire, supprimé avec le Pod | Cache, données temporaires |
| **hostPath** | Monte un répertoire du Node | Dev, logs système |
| **PersistentVolume** | Stockage persistant (NFS, cloud storage) | Bases de données, fichiers persistants |
| **ConfigMap/Secret** | Monte des configs ou secrets | Configuration, credentials |

### emptyDir

```bash
apiVersion: v1
kind: Pod
metadata:
  name: shared-volume-pod
spec:
  containers:
  - name: writer
    image: busybox
    command: ["sh", "-c", "while true; do date >> /data/log.txt; sleep 5; done"]
    volumeMounts:
    - name: shared-data
      mountPath: /data

  - name: reader
    image: busybox
    command: ["sh", "-c", "while true; do cat /data/log.txt; sleep 10; done"]
    volumeMounts:
    - name: shared-data
      mountPath: /data

  volumes:
  - name: shared-data
    emptyDir: {}
```

### PersistentVolume (PV) et PersistentVolumeClaim (PVC)

**PersistentVolume (PV)** : Stockage provisionné par l'admin
**PersistentVolumeClaim (PVC)** : Demande de stockage par un utilisateur

#### PersistentVolume

```bash
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-storage
spec:
  capacity:
    storage: 10Gi
  accessModes:
  - ReadWriteOnce  # RWO = un seul Node, RWX = plusieurs Nodes
  persistentVolumeReclaimPolicy: Retain  # ou Delete
  storageClassName: manual
  hostPath:
    path: "/mnt/data"  # Pour dev (hostPath), en prod utiliser NFS ou cloud storage
```

#### PersistentVolumeClaim

```bash
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-storage
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
  storageClassName: manual
```

#### Utiliser un PVC dans un Pod

```bash
apiVersion: v1
kind: Pod
metadata:
  name: postgres-pod
spec:
  containers:
  - name: postgres
    image: postgres:15
    env:
    - name: POSTGRES_PASSWORD
      value: mysecretpassword
    volumeMounts:
    - name: postgres-storage
      mountPath: /var/lib/postgresql/data

  volumes:
  - name: postgres-storage
    persistentVolumeClaim:
      claimName: pvc-storage
```

```bash
# Créer les ressources
kubectl apply -f pv.yaml
kubectl apply -f pvc.yaml
kubectl apply -f pod-with-pvc.yaml

# Vérifier
kubectl get pv
kubectl get pvc
kubectl describe pvc pvc-storage

# Le PVC est automatiquement lié au PV disponible
```

### StorageClass (provisionnement dynamique)

Les **StorageClass** permettent le provisionnement dynamique de volumes sans créer de PV manuellement.

```bash
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: azure-disk
provisioner: kubernetes.io/azure-disk
parameters:
  storageaccounttype: Standard_LRS
  kind: Managed
```

```bash
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: dynamic-pvc
spec:
  accessModes:
  - ReadWriteOnce
  storageClassName: azure-disk  # Utilise la StorageClass
  resources:
    requests:
      storage: 10Gi
```

#### Provisionnement automatique

Avec une StorageClass, Kubernetes crée automatiquement le PV et le disque dans le cloud
quand vous créez un PVC. Très pratique en production !

## 8. Ingress et exposition externe

### Qu'est-ce qu'un Ingress ?

Un **Ingress** est un objet qui gère l'accès externe aux Services, typiquement HTTP/HTTPS.
Il fournit du load balancing, SSL termination, et du routing basé sur le nom d'hôte ou le path.

```bash
Internet
   │
   ↓
┌──────────────────┐
│  Load Balancer   │  (Cloud provider ou Nginx)
└──────────────────┘
   │
   ↓
┌──────────────────┐
│  Ingress         │  Routing rules
└──────────────────┘
   │
   ├─────────────────┬─────────────────┐
   ↓                 ↓                 ↓
Service A        Service B        Service C
(frontend)       (api)            (admin)
```

### Installer un Ingress Controller

```bash
# Avec Minikube
minikube addons enable ingress

# Avec Helm (NGINX Ingress Controller)
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update
helm install ingress-nginx ingress-nginx/ingress-nginx

# Vérifier
kubectl get pods -n ingress-nginx
```

### Exemple d'Ingress

```bash
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: frontend-service
            port:
              number: 80

      - path: /api
        pathType: Prefix
        backend:
          service:
            name: backend-service
            port:
              number: 8080
```

#### Ingress avec SSL/TLS

```bash
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: tls-ingress
spec:
  tls:
  - hosts:
    - myapp.example.com
    secretName: tls-secret  # Secret contenant le certificat SSL
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: myapp-service
            port:
              number: 80
```

```bash
# Créer un Secret TLS depuis des certificats
kubectl create secret tls tls-secret \
  --cert=path/to/tls.crt \
  --key=path/to/tls.key

# Appliquer l'Ingress
kubectl apply -f ingress.yaml

# Vérifier
kubectl get ingress
kubectl describe ingress myapp-ingress
```

### Best Practices Ingress

- Utilisez toujours HTTPS en production avec Let's Encrypt (cert-manager)
- Configurez des rate limits pour protéger vos APIs
- Utilisez des annotations pour personnaliser le comportement
- Mettez en place du monitoring sur votre Ingress Controller
- Utilisez plusieurs Ingress pour séparer les domaines

## 9. Déploiement sur Azure (AKS)

### Azure Kubernetes Service (AKS)

**AKS** est le service Kubernetes managé d'Azure. Le Control Plane est entièrement géré par Microsoft,
vous ne payez que pour les Worker Nodes.

### Créer un cluster AKS

```bash
# Installer Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Se connecter
az login

# Créer un resource group
az group create --name myResourceGroup --location francecentral

# Créer un cluster AKS
az aks create \
  --resource-group myResourceGroup \
  --name myAKSCluster \
  --node-count 3 \
  --node-vm-size Standard_D2s_v3 \
  --enable-managed-identity \
  --generate-ssh-keys

# Récupérer les credentials
az aks get-credentials --resource-group myResourceGroup --name myAKSCluster

# Vérifier la connexion
kubectl get nodes
kubectl cluster-info
```

### Déployer une application sur AKS

```bash
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: myregistry.azurecr.io/myapp:v1
        ports:
        - containerPort: 80
        resources:
          requests:
            cpu: 250m
            memory: 128Mi
          limits:
            cpu: 500m
            memory: 256Mi
---
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  type: LoadBalancer
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 80
```

```bash
# Déployer
kubectl apply -f deployment.yaml

# Attendre le Load Balancer
kubectl get service myapp-service --watch

# Une fois l'EXTERNAL-IP disponible
curl http://
```

### Azure Container Registry (ACR)

```bash
# Créer un Azure Container Registry
az acr create \
  --resource-group myResourceGroup \
  --name myRegistry \
  --sku Basic

# Lier AKS à ACR
az aks update \
  --resource-group myResourceGroup \
  --name myAKSCluster \
  --attach-acr myRegistry

# Build et push une image
az acr build \
  --registry myRegistry \
  --image myapp:v1 \
  .

# Vérifier
az acr repository list --name myRegistry --output table
```

### Best Practices AKS

- Utilisez des Managed Identities plutôt que des Service Principals
- Activez Azure Monitor pour les logs et métriques
- Configurez autoscaling des Pods (HPA) et des Nodes (Cluster Autoscaler)
- Utilisez Azure Key Vault pour les secrets sensibles
- Mettez en place des Network Policies pour la sécurité
- Configurez des resource quotas par namespace
- Utilisez GitOps (Flux, ArgoCD) pour les déploiements

## 📚 Ressources et liens utiles

[**Documentation officielle Kubernetes**

Documentation complète, concepts et références](https://kubernetes.io/docs/)
[**Kubernetes Tutorials**

Tutorials interactifs pour apprendre K8s](https://kubernetes.io/docs/tutorials/)
[**Azure AKS Documentation**

Guide complet pour AKS](https://learn.microsoft.com/azure/aks/)
[**Helm**

Package manager pour Kubernetes](https://helm.sh/)
[**Kubernetes The Hard Way**

Comprendre K8s en profondeur](https://github.com/kelseyhightower/kubernetes-the-hard-way)
[**CNCF**

Cloud Native Computing Foundation](https://www.cncf.io/)

#### Prochaines étapes

Maintenant que vous maîtrisez Kubernetes, explorez :

- **Helm** : Package manager pour simplifier les déploiements
- **Kustomize** : Gestion des configurations Kubernetes
- **ArgoCD/Flux** : GitOps pour déploiements automatiques
- **Prometheus + Grafana** : Monitoring et alerting
- **Istio/Linkerd** : Service Mesh pour microservices
- **Cert-Manager** : Gestion automatique des certificats SSL