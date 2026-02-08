# 06 - ConfigMaps et Secrets

[← 05 - Services](05-services-networking.md) | [🏠 Accueil](README.md) | [07 - Persistance →](07-volumes-persistence.md)

---

## 6. ConfigMaps et Secrets

### ConfigMaps

Les **ConfigMaps** permettent de stocker des données de configuration non confidentielles (fichiers de config, variables d'environnement).

```yaml
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

```yaml
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
```

### Secrets

Les **Secrets** stockent des données sensibles (mots de passe, tokens, clés SSH). Les données sont encodées en base64 (pas chiffrées par défaut !).

```yaml
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

```yaml
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

Par défaut, les Secrets sont encodés en base64, pas chiffrés ! En production, utilisez :
- Encryption at rest (chiffrement dans etcd).
- Azure Key Vault, AWS Secrets Manager, ou HashiCorp Vault.
- Sealed Secrets pour versionner les secrets de manière sécurisée.

### 💡 Points clés à retenir
- ConfigMaps stockent les configurations non sensibles.
- Secrets stockent les données sensibles (encodées en base64).
- On peut injecter les configs via variables d'env ou volumes.
- Les Secrets ne sont PAS chiffrés par défaut dans etcd.
- En production, utilisez des solutions externes (Key Vault, Vault).

---

[← 05 - Services](05-services-networking.md) | [🏠 Accueil](README.md) | [07 - Persistance →](07-volumes-persistence.md)