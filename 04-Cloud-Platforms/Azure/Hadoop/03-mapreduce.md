# 03 - MapReduce

[← 02 - HDFS](02-architecture-hdfs.md) | [🏠 Accueil](README.md) | [04 - YARN →](04-yarn.md)

---

## ⚙️ Paradigme MapReduce

L'idée : **"Diviser pour régner"** (Divide and Conquer).

### Les Deux Fonctions Principales
- **🗺️ Map** : Traite les données d'entrée et produit des paires clé-valeur.
- **🔽 Reduce** : Regroupe les valeurs par clé et produit le résultat final.

## 💻 Exemple WordCount (Python)

Utilisation de **Hadoop Streaming** pour exécuter du code Python.

### Mapper
```python
import sys
for line in sys.stdin:
    words = line.strip().split()
    for word in words:
        print(f"{word}	1")
```

### Reducer
Calcul de la somme des occurrences par mot reçu trié par clé.

---

[← 02 - HDFS](02-architecture-hdfs.md) | [🏠 Accueil](README.md) | [04 - YARN →](04-yarn.md)
