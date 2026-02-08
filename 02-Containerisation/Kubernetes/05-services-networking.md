# 05 - Services et networking

[← 04 - Deployments](04-pods-deployments.md) | [🏠 Accueil](README.md) | [06 - Configuration →](06-configmaps-secrets.md)

---

## 5. Services et networking

### Qu'est-ce qu'un Service ?

Un **Service** est une abstraction qui définit un moyen d'accéder à un ensemble de Pods. Les Pods sont éphémères (IPs changeantes), mais les Services fournissent une adresse stable.

### Types de Services

| Type | Description | Cas d'usage |
| --- | --- | --- |
| **ClusterIP** | IP interne au cluster (par défaut) | Communication interne entre services |
| **NodePort** | Expose le service sur un port de chaque Node | Accès externe simple (dev/test) |
| **LoadBalancer** | Crée un load balancer externe (cloud) | Production avec cloud provider |
| **ExternalName** | Alias DNS vers un service externe | Pointer vers des services hors cluster |

#### Service ClusterIP

```yaml
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

```yaml
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

```yaml
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
# Dans le shell du pod :
wget -O- nginx-service

# Avec NodePort (Minikube)
minikube service nginx-nodeport --url
curl $(minikube service nginx-nodeport --url)
```

### DNS dans Kubernetes

Kubernetes fournit un serveur DNS interne. Chaque Service obtient automatiquement un nom DNS :

```bash
# Format DNS
<service-name>.<namespace>.svc.cluster.local

# Exemples
nginx-service.default.svc.cluster.local
database.production.svc.cluster.local

# Dans le même namespace, on peut juste utiliser le nom
curl http://nginx-service
```

### 💡 Points clés à retenir
- Les Services fournissent une adresse stable pour accéder aux Pods.
- ClusterIP pour la communication interne (par défaut).
- NodePort pour l'accès externe simple (dev/test).
- LoadBalancer pour l'accès externe en production (cloud).
- Kubernetes fournit un DNS interne automatique pour tous les Services.

---

[← 04 - Deployments](04-pods-deployments.md) | [🏠 Accueil](README.md) | [06 - Configuration →](06-configmaps-secrets.md)