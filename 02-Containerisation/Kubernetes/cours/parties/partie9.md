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
curl http://<EXTERNAL-IP>
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

## Ressources et liens utiles

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

### Points clés à retenir

- AKS est le service Kubernetes managé d'Azure
- Le Control Plane est géré par Microsoft, vous payez uniquement les Nodes
- Azure Container Registry (ACR) pour stocker vos images Docker
- Utilisez des Managed Identities pour la sécurité
- Activez le monitoring avec Azure Monitor
- Configurez l'autoscaling pour la production

#### Félicitations ! Formation terminée

Vous avez maintenant une compréhension complète de Kubernetes, de l'installation locale
au déploiement en production sur Azure. Continuez à pratiquer et explorez les outils
avancés pour devenir un expert Kubernetes !

[Retour à l'accueil](../index.md)

[← Partie 8](partie8.md)
[🏠 Accueil](../index.md)