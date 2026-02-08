# 07 - Volumes et persistence des données

[← 06 - Configuration](06-configmaps-secrets.md) | [🏠 Accueil](README.md) | [08 - Ingress →](08-ingress-exposition.md)

---

## 7. Volumes et persistence des données

### Types de Volumes

| Type | Description | Cas d'usage |
| --- | --- | --- |
| **emptyDir** | Volume temporaire, supprimé avec le Pod | Cache, données temporaires |
| **hostPath** | Monte un répertoire du Node | Dev, logs système |
| **PersistentVolume** | Stockage persistant (NFS, cloud storage) | Bases de données, fichiers persistants |
| **ConfigMap/Secret** | Monte des configs ou secrets | Configuration, credentials |

### emptyDir

```yaml
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

**PersistentVolume (PV)** : Stockage provisionné par l'admin.
**PersistentVolumeClaim (PVC)** : Demande de stockage par un utilisateur.

#### PersistentVolume

```yaml
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

```yaml
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

```yaml
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

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: azure-disk
provisioner: kubernetes.io/azure-disk
parameters:
  storageaccounttype: Standard_LRS
  kind: Managed
```

```yaml
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
Avec une StorageClass, Kubernetes crée automatiquement le PV et le disque dans le cloud quand vous créez un PVC. Très pratique en production !

### 💡 Points clés à retenir
- `emptyDir` pour le stockage temporaire (supprimé avec le Pod).
- PersistentVolume (PV) pour le stockage persistant provisionné par l'admin.
- PersistentVolumeClaim (PVC) pour demander du stockage.
- StorageClass permet le provisionnement dynamique automatique.
- En production cloud, utilisez toujours StorageClass.

---

[← 06 - Configuration](06-configmaps-secrets.md) | [🏠 Accueil](README.md) | [08 - Ingress →](08-ingress-exposition.md)