# 02 - Architecture HDFS

[← 01 - Introduction](01-introduction.md) | [🏠 Accueil](README.md) | [03 - MapReduce →](03-mapreduce.md)

---

## 🏗️ Architecture de HDFS

HDFS suit une architecture **Master/Slave** :

- **🎯 NameNode (Master)** : Gère les métadonnées (arborescence, mapping des blocs).
- **💾 DataNodes (Slaves)** : Stockent physiquement les données sous forme de blocs.

### Concept de Blocs et Réplication
- Les fichiers sont découpés en blocs (128 MB par défaut).
- Chaque bloc est répliqué (facteur 3 par défaut) pour la tolérance aux pannes.

## 💻 Commandes HDFS Essentielles

| Commande | Exemple |
| --- | --- |
| ls | `hdfs dfs -ls /user/data` |
| put | `hdfs dfs -put local.txt /hdfs/` |
| get | `hdfs dfs -get /hdfs/file.txt .` |
| rm | `hdfs dfs -rm /hdfs/file.txt` |

---

[← 01 - Introduction](01-introduction.md) | [🏠 Accueil](README.md) | [03 - MapReduce →](03-mapreduce.md)
