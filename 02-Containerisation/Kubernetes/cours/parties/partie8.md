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

### Points clés à retenir

- Ingress gère l'accès externe HTTP/HTTPS aux Services
- Il faut un Ingress Controller (NGINX, Traefik, etc.)
- Ingress offre du routing basé sur l'hôte et le path
- SSL/TLS termination via des Secrets contenant les certificats
- Utilisez cert-manager pour automatiser les certificats Let's Encrypt

[← Partie 7](partie7.md)
[Partie 9 →](partie9.md)