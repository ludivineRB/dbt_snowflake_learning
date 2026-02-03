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

### Points clés à retenir

- Le Control Plane gère le cluster (API Server, Scheduler, etcd, Controller Manager)
- Les Worker Nodes exécutent les applications (kubelet, kube-proxy, Container Runtime)
- etcd stocke l'état complet du cluster
- Le Scheduler décide où placer les Pods
- Les services managés (AKS/EKS/GKE) gèrent le Control Plane pour vous

[← Partie 1](partie1.md)
[Partie 3 →](partie3.md)