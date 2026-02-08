# 04 - Pods et Deployments

[← 03 - Installation](03-installation-minikube.md) | [🏠 Accueil](README.md) | [05 - Networking →](05-services-networking.md)

---

## 4. Pods et Deployments

### Qu'est-ce qu'un Pod ?

Un **Pod** est la plus petite unité déployable dans Kubernetes. Il contient un ou plusieurs conteneurs qui partagent le même réseau et le même stockage.

#### Pod simple (YAML)

```yaml
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
En production, on n'utilise presque jamais de Pods directement. On utilise des **Deployments** qui gèrent les Pods automatiquement.

### Deployments

Un **Deployment** déclare l'état désiré de vos Pods et gère leur cycle de vie (création, mise à jour, scaling, self-healing).

```yaml
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

Un **ReplicaSet** assure qu'un nombre spécifié de réplicas de Pods est toujours en cours d'exécution. Les Deployments créent et gèrent automatiquement des ReplicaSets.

```bash
# Voir les ReplicaSets
kubectl get replicasets
```

### Stratégies de déploiement

```yaml
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
# ... reste du spec
```

| Stratégie | Description | Cas d'usage |
| --- | --- | --- |
| **RollingUpdate** | Remplace progressivement les anciens Pods par des nouveaux | Par défaut, zero-downtime |
| **Recreate** | Supprime tous les anciens Pods avant de créer les nouveaux | Quand les versions ne peuvent pas coexister |

### 💡 Points clés à retenir
- Les Pods sont la plus petite unité déployable dans Kubernetes.
- En production, utilisez toujours des Deployments, pas des Pods seuls.
- Les Deployments gèrent les réplicas, les mises à jour et le rollback.
- Les ReplicaSets sont créés automatiquement par les Deployments.
- RollingUpdate permet des déploiements sans downtime.

---

[← 03 - Installation](03-installation-minikube.md) | [🏠 Accueil](README.md) | [05 - Networking →](05-services-networking.md)