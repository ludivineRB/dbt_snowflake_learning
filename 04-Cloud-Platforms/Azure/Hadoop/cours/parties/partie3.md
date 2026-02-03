## 🎯 Objectifs d'Apprentissage

- Comprendre le paradigme de programmation MapReduce
- Maîtriser les phases Map, Shuffle et Reduce
- Écrire un job MapReduce en Java
- Optimiser les performances MapReduce

## 📚 1. Qu'est-ce que MapReduce ?

**MapReduce** est un modèle de programmation pour traiter et générer de grands ensembles
de données de manière parallèle et distribuée sur un cluster.

#### Principe Fondamental

L'idée : **"Diviser pour régner"** (Divide and Conquer)

- Découper un gros problème en petits problèmes indépendants
- Traiter ces petits problèmes en parallèle
- Combiner les résultats pour obtenir le résultat final

### Les Deux Fonctions Principales

#### 🗺️ Map

Traite les données d'entrée et produit des paires clé-valeur intermédiaires

`map: (K1, V1) → list(K2, V2)`

#### 🔽 Reduce

Regroupe les valeurs par clé et produit le résultat final

`reduce: (K2, list(V2)) → list(K3, V3)`

### Exemple Conceptuel : Compter des Mots

```bash
Entrée :
  "Hello World"
  "Hello Hadoop"
  "Hadoop MapReduce"

Phase MAP :
  Hello → 1
  World → 1
  Hello → 1
  Hadoop → 1
  Hadoop → 1
  MapReduce → 1

Phase SHUFFLE & SORT :
  Hadoop → [1, 1]
  Hello → [1, 1]
  MapReduce → [1]
  World → [1]

Phase REDUCE :
  Hadoop → 2
  Hello → 2
  MapReduce → 1
  World → 1
```

## 🔄 2. Architecture et Flux d'Exécution

### Vue d'Ensemble

```bash
┌─────────────────────────────────────────────────────────────────┐
│                      HDFS INPUT DATA                            │
│        Fichiers découpés en blocs (splits)                      │
└────────────┬────────────────────────────────────────────────────┘
             ↓
┌─────────────────────────────────────────────────────────────────┐
│                     MAP PHASE                                   │
│  Mapper 1   Mapper 2   Mapper 3   Mapper N                     │
│  (K1,V1)    (K1,V1)    (K1,V1)    (K1,V1)                      │
│    ↓          ↓          ↓          ↓                           │
│  (K2,V2)    (K2,V2)    (K2,V2)    (K2,V2)                      │
└────────────┬────────────────────────────────────────────────────┘
             ↓
┌─────────────────────────────────────────────────────────────────┐
│              SHUFFLE & SORT PHASE                               │
│    Regroupement et tri des paires par clé                       │
│         (K2, list(V2))                                          │
└────────────┬────────────────────────────────────────────────────┘
             ↓
┌─────────────────────────────────────────────────────────────────┐
│                     REDUCE PHASE                                │
│  Reducer 1  Reducer 2  Reducer 3  Reducer M                    │
│  (K2,[V2])  (K2,[V2])  (K2,[V2])  (K2,[V2])                    │
│    ↓          ↓          ↓          ↓                           │
│  (K3,V3)    (K3,V3)    (K3,V3)    (K3,V3)                      │
└────────────┬────────────────────────────────────────────────────┘
             ↓
┌─────────────────────────────────────────────────────────────────┐
│                    HDFS OUTPUT DATA                             │
│              Résultats finaux stockés                           │
└─────────────────────────────────────────────────────────────────┘
```

### Les Phases en Détail

#### 1️⃣ Input Splits

Les données d'entrée sont divisées en **splits** (morceaux) logiques.

- Par défaut, 1 split = 1 bloc HDFS (128 MB)
- Chaque split est traité par un mapper
- Les mappers s'exécutent là où les données sont stockées (data locality)

#### 2️⃣ Map Phase

Chaque mapper traite un split de données :

- Lit les données ligne par ligne (ou enregistrement par enregistrement)
- Applique la fonction `map()` définie par l'utilisateur
- Émet des paires clé-valeur intermédiaires
- Les résultats sont écrits dans un buffer en mémoire

#### 3️⃣ Shuffle & Sort Phase

Phase critique gérée automatiquement par Hadoop :

- **Partitioning** : Les paires (K2,V2) sont partitionnées par clé vers les reducers
- **Sorting** : Les clés sont triées
- **Grouping** : Les valeurs avec la même clé sont regroupées
- **Transfer** : Les données sont transférées via le réseau vers les reducers

*Cette phase consomme beaucoup de ressources réseau et disque.*

#### 4️⃣ Reduce Phase

Chaque reducer traite un ensemble de clés :

- Reçoit les paires (K2, list(V2)) triées
- Applique la fonction `reduce()` définie par l'utilisateur
- Émet les paires clé-valeur finales (K3, V3)
- Écrit les résultats dans HDFS

## 💻 3. WordCount : L'Exemple Classique avec Python

Le "Hello World" de MapReduce : compter les occurrences de chaque mot dans un corpus de texte.

#### Hadoop Streaming

**Hadoop Streaming** permet d'écrire des jobs MapReduce en Python (ou tout autre langage).
Les scripts lisent depuis stdin et écrivent vers stdout.

### Code Python Complet

#### mapper.py

```bash
#!/usr/bin/env python3
"""
Mapper pour WordCount
Lit les lignes depuis stdin, découpe en mots et émet (mot, 1)
"""
import sys

def main():
# Lire depuis stdin
    for line in sys.stdin:
# Supprimer les espaces en début/fin
        line = line.strip()

# Découper la ligne en mots
        words = line.split()

# Émettre (mot, 1) pour chaque mot
        for word in words:
# Format: clé\tvaleur
            print(f"{word}\t1")

if __name__ == "__main__":
    main()
```

#### reducer.py

```bash
#!/usr/bin/env python3
"""
Reducer pour WordCount
Reçoit les paires (mot, 1) triées par clé et calcule la somme
"""
import sys

def main():
    current_word = None
    current_count = 0

# Lire depuis stdin
    for line in sys.stdin:
# Supprimer les espaces
        line = line.strip()

# Parser la ligne (format: mot\t1)
        try:
            word, count = line.split('\t')
            count = int(count)
        except ValueError:
# Ignorer les lignes mal formées
            continue

# Hadoop trie les clés, donc les mêmes mots sont consécutifs
        if current_word == word:
            current_count += count
        else:
# Nouveau mot rencontré
            if current_word:
# Émettre le résultat pour le mot précédent
                print(f"{current_word}\t{current_count}")

            current_word = word
            current_count = count

# Émettre le dernier mot
    if current_word:
        print(f"{current_word}\t{current_count}")

if __name__ == "__main__":
    main()
```

### Test Local (avant Hadoop)

```bash
# Rendre les scripts exécutables
chmod +x mapper.py reducer.py

# Test du mapper seul
echo "Hello World Hello Hadoop" | ./mapper.py

# Sortie attendue:
# Hello   1
# World   1
# Hello   1
# Hadoop  1

# Test complet avec tri (simule Hadoop)
echo "Hello World Hello Hadoop" | ./mapper.py | sort -k1,1 | ./reducer.py

# Sortie attendue:
# Hadoop  1
# Hello   2
# World   1
```

### Exécution sur Hadoop

#### Préparer les Données

```bash
# Créer un fichier de test
cat > input.txt << EOF
Hello World Hello Hadoop
Hadoop is powerful
Python and Hadoop
EOF

# Créer le répertoire dans HDFS
hdfs dfs -mkdir -p /user/$USER/wordcount/input

# Copier le fichier dans HDFS
hdfs dfs -put input.txt /user/$USER/wordcount/input/

# Vérifier
hdfs dfs -cat /user/$USER/wordcount/input/input.txt
```

#### Lancer le Job MapReduce avec Hadoop Streaming

```bash
# Exécuter le job Hadoop Streaming
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
    -input /user/$USER/wordcount/input \
    -output /user/$USER/wordcount/output \
    -mapper mapper.py \
    -reducer reducer.py \
    -file mapper.py \
    -file reducer.py

# Voir les résultats
hdfs dfs -cat /user/$USER/wordcount/output/part-00000

# Résultat attendu :
# Hadoop  3
# Hello   2
# Python  1
# World   1
# and     1
# is      1
# powerful 1
```

#### Avantages de Python avec Hadoop

- ✅ Code plus simple et lisible que Java
- ✅ Pas de compilation nécessaire
- ✅ Riche écosystème de librairies Python
- ✅ Test facile en local avant Hadoop
- ✅ Idéal pour le prototypage rapide

## ⚡ 4. Optimisations MapReduce

### Combiner

#### Qu'est-ce qu'un Combiner ?

Un **Combiner** est comme un "mini-reducer" qui s'exécute localement sur chaque mapper
pour réduire la quantité de données transférées durant la phase Shuffle.

```bash
// Dans le Driver
job.setCombinerClass(WordCountReducer.class);
```

**Avantage :** Pour WordCount, au lieu de transférer ["Hello"→1, "Hello"→1, "Hello"→1],
on transfère juste ["Hello"→3].

### Partitioner Personnalisé

Le **Partitioner** décide quel reducer recevra quelle clé.
Par défaut : `HashPartitioner` utilise le hashcode de la clé.

```bash
public class CustomPartitioner extends Partitioner<Text, IntWritable> {
    @Override
    public int getPartition(Text key, IntWritable value, int numPartitions) {
        // Exemple : mots commençant par A-M → Reducer 0
        //           mots commençant par N-Z → Reducer 1
        char firstLetter = key.toString().charAt(0);
        if (firstLetter >= 'A' && firstLetter <= 'M') {
            return 0 % numPartitions;
        } else {
            return 1 % numPartitions;
        }
    }
}
```

### Compression

Compresser les données intermédiaires et de sortie réduit l'utilisation disque et réseau.

```bash
// Compression des données intermédiaires (Map output)
conf.setBoolean("mapreduce.map.output.compress", true);
conf.setClass("mapreduce.map.output.compress.codec",
              SnappyCodec.class, CompressionCodec.class);

// Compression de la sortie finale
FileOutputFormat.setCompressOutput(job, true);
FileOutputFormat.setOutputCompressorClass(job, GzipCodec.class);
```

### Autres Optimisations

| Technique | Description | Impact |
| --- | --- | --- |
| **Augmenter le nombre de reducers** | Plus de reducers = plus de parallélisme | ⚡ Performance accrue si le cluster le permet |
| **Réutiliser la JVM** | Éviter le coût de démarrage de JVM pour chaque tâche | ⏱️ Réduction du temps de lancement |
| **Exécution spéculative** | Relancer les tâches lentes sur d'autres nœuds | 🚀 Réduit l'impact des "stragglers" |
| **Buffer d'écriture Map** | Augmenter `mapreduce.task.io.sort.mb` | 💾 Moins de spills sur disque |

## 📊 5. Patterns MapReduce Courants

### 1. Filtering (Filtrage)

Garder seulement les enregistrements qui répondent à un critère.

**Exemple :** Filtrer les logs d'erreur

- Map : Si ligne contient "ERROR" → émettre
- Reduce : Peut être omis (identity reducer)

### 2. Summarization (Agrégation)

Calculer des statistiques agrégées (count, sum, avg, min, max).

**Exemple :** Statistiques par utilisateur

- Map : (user\_id, metric) → émettre
- Reduce : Calculer somme, moyenne, etc.

### 3. Joining (Jointure)

Joindre deux datasets sur une clé commune.

**Reduce-side join :**

- Map : Émettre (clé\_commune, valeur\_avec\_tag)
- Reduce : Regrouper et joindre les valeurs avec la même clé

### 4. Sorting (Tri)

Trier des données à grande échelle.

- Map : Émettre (clé\_de\_tri, enregistrement)
- Reduce : Peut être identity (le tri est fait durant Shuffle)

### 5. Top N

Trouver les N premiers éléments.

- Map : Garder top N localement, émettre
- Reduce : Fusionner et garder top N global

## ⚠️ 6. Limites de MapReduce

#### 🐌 Latence Élevée

Pas adapté au temps réel. Temps de démarrage et I/O disque importants.

#### 💾 I/O Intensif

Écrit et lit beaucoup sur disque (HDFS), pas en mémoire.

#### 🔗 Jobs Chaînés Complexes

Difficile de chaîner plusieurs jobs MapReduce efficacement.

#### 📈 Pas Adapté aux Graphes

Algorithmes itératifs (ML, graphes) sont inefficaces.

#### Alternative : Apache Spark

**Spark** a été créé pour pallier les limites de MapReduce :

- Traitement en mémoire (100x plus rapide)
- API plus simple et expressive
- Support natif du streaming, ML, graphes
- Compatible avec HDFS et YARN

*Cependant, MapReduce reste utilisé pour certains cas d'usage batch intensifs.*

## 📝 Résumé de la Partie 3

### Points Clés à Retenir

- MapReduce suit le paradigme "Diviser pour régner"
- 3 phases principales : Map, Shuffle & Sort, Reduce
- WordCount est l'exemple canonique de MapReduce
- Les Combiners réduisent le trafic réseau
- La compression améliore les performances
- MapReduce est excellent pour le batch mais pas pour le temps réel
- Spark est souvent préféré pour les nouveaux projets

#### ✅ Prêt pour la Suite ?

Vous maîtrisez maintenant MapReduce ! Dans la partie suivante, nous découvrirons **YARN**, le gestionnaire de ressources qui orchestre l'exécution des applications Hadoop.