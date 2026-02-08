# 04 - YARN (Resource Negotiator)

[← 03 - MapReduce](03-mapreduce.md) | [🏠 Accueil](README.md) | [05 - Écosystème →](05-ecosysteme.md)

---

## 🏗️ Architecture de YARN

YARN sépare la gestion des ressources du traitement des données.

- **RESOURCE MANAGER** : Master Global qui alloue les ressources.
- **NODE MANAGER** : Agent sur chaque nœud worker.
- **ApplicationMaster** : Spécifique à chaque application (job).
- **Container** : Unité d'allocation (CPU + RAM).

### Schedulers YARN
- **FIFO** : Simple file.
- **Capacity** : Queues avec garanties.
- **Fair** : Partage équitable.

---

[← 03 - MapReduce](03-mapreduce.md) | [🏠 Accueil](README.md) | [05 - Écosystème →](05-ecosysteme.md)
