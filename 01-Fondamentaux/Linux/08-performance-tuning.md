# 08 - Performance et Tuning (Expert)

[← 07 - Administration](07-administration-logs.md) | [🏠 Accueil](README.md) | [09 - Exercices →](09-exercices.md)

---

## 1. Monitoring Avancé

Quand un cluster Spark est lent, il faut savoir identifier le goulot d'étranglement (Bottleneck).

### L'approche USE (Utilization, Saturation, Errors)
- **iostat** : Performance des disques (I/O Wait).
- **sar** : Historique complet des performances.
- **nload** : Visualisation du trafic réseau.

---

## 2. Kernel Tuning via /proc et sysctl

Le Kernel Linux a des milliers de paramètres ajustables sans redémarrer.

### Exemple : Swappiness
Définit à quel point Linux doit utiliser le Swap. Pour la Data, on veut souvent le baisser (ex: 10).
```bash
sysctl -w vm.swappiness=10
```

### Exemple : File Descriptors
Les serveurs de données ouvrent beaucoup de fichiers/sockets. On augmente souvent la limite :
```bash
ulimit -n 65535
```

---

## 3. Comprendre le "Load Average"

Affiché dans `top` : `0.50, 1.20, 2.50`
- Moyenne sur 1 min, 5 min, 15 min.
- **Si Load > Nombre de CPUs** : Le système est surchargé (processus en attente).

---

## 4. Troubleshooting Expert

- **`strace`** : Trace tous les appels système d'un programme. Utile pour savoir pourquoi un binaire plante sans message d'erreur.
- **`lsof`** : List Open Files. Savoir quel processus bloque un fichier ou un port.
- **`iotop`** : Quel processus utilise tout le disque ?

---

## 5. HugePages et Cgroups

- **HugePages** : Optimise la gestion des grandes quantités de RAM pour les bases de données.
- **Cgroups** : Le mécanisme qui limite les ressources des containers (Docker/Kubernetes).

---

[← 07 - Administration](07-administration-logs.md) | [🏠 Accueil](README.md) | [09 - Exercices →](09-exercices.md)
