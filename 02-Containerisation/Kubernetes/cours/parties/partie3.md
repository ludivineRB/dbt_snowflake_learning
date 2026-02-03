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

### Points clés à retenir

- Minikube est parfait pour développer en local
- kubectl est l'outil CLI pour interagir avec Kubernetes
- kubectl get, describe, logs, apply sont les commandes essentielles
- Un déploiement simple : create deployment → expose → test
- Kubernetes gère automatiquement la création et le placement des Pods

[← Partie 2](partie2.md)
[Partie 4 →](partie4.md)