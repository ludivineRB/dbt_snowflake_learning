## 🎯 Objectifs d'Apprentissage

- Comprendre l'architecture master/slave de HDFS
- Maîtriser les concepts de NameNode et DataNode
- Appréhender la réplication et la tolérance aux pannes
- Utiliser les commandes HDFS essentielles

## 📚 1. Qu'est-ce que HDFS ?

**HDFS** (Hadoop Distributed File System) est le système de fichiers distribué de Hadoop.
C'est un système conçu pour stocker de très grandes quantités de données sur plusieurs machines tout en
offrant une tolérance aux pannes et un débit élevé.

### Principes de Conception

#### 💪 Tolérance aux Pannes

Les pannes matérielles sont la norme, pas l'exception. HDFS détecte et récupère automatiquement.

#### 📈 Scalabilité

Conçu pour s'adapter à des centaines ou milliers de nœuds dans un cluster.

#### 📊 Gros Fichiers

Optimisé pour stocker des fichiers de plusieurs gigaoctets à téraoctets.

#### 🔄 Accès Streaming

Conçu pour des lectures séquentielles rapides plutôt que des accès aléatoires.

#### 💻 Matériel Standard

Fonctionne sur du matériel commodity (bon marché), pas de serveurs spécialisés requis.

#### ✏️ Write Once, Read Many

Les fichiers sont écrits une fois et lus plusieurs fois. Pas de modifications en place.

#### Analogie

Imaginez une bibliothèque où les livres (données) sont répartis dans plusieurs bâtiments (DataNodes).
Il y a un catalogue central (NameNode) qui sait exactement dans quel bâtiment se trouve chaque livre.
Chaque livre existe en plusieurs exemplaires dans différents bâtiments pour éviter la perte.

## 🏗️ 2. Architecture de HDFS

### Vue d'Ensemble

HDFS suit une architecture **Master/Slave** (ou Master/Worker) :

```bash
┌─────────────────────────────────────────────────────────────────┐
│                           CLIENT                                │
│                    (Application Hadoop)                         │
└────────┬──────────────────────────────────────────┬─────────────┘
         │                                          │
         │ Métadonnées                             │ Données
         ↓                                          ↓
┌────────────────────┐                    ┌──────────────────────┐
│     NAMENODE       │ ← Heartbeat &     │     DATANODES        │
│   (Master/Maître)  │   Block Reports → │   (Slaves/Workers)   │
│                    │                    │                      │
│ - Métadonnées      │                    │  DataNode 1          │
│ - Arborescence     │                    │  DataNode 2          │
│ - Localisation     │                    │  DataNode 3          │
│   des blocs        │                    │  DataNode N          │
└────────────────────┘                    └──────────────────────┘
         ↕
┌────────────────────┐
│ SECONDARY NAMENODE │
│   (Checkpoint)     │
└────────────────────┘
```

### Composants Principaux

#### 🎯 NameNode (Master)

Le NameNode est le **maître** du cluster HDFS. Il gère :

- **Métadonnées** : Structure de l'arborescence des fichiers et répertoires
- **Namespace** : Noms de fichiers, permissions, propriétaires
- **Mapping des blocs** : Quelle partie de fichier est stockée où
- **Heartbeats** : Surveillance de l'état des DataNodes
- **Réplication** : Décisions sur où répliquer les blocs

#### Point de Défaillance Unique (SPOF)

Le NameNode est critique ! Si le NameNode tombe en panne, tout le cluster devient inaccessible.
Solution : **High Availability (HA)** avec un NameNode de secours.

#### 💾 DataNodes (Slaves)

Les DataNodes sont les **esclaves/workers** qui :

- Stockent physiquement les données sous forme de blocs
- Servent les requêtes de lecture et d'écriture des clients
- Envoient des heartbeats au NameNode toutes les 3 secondes
- Envoient des block reports (liste de blocs stockés) régulièrement
- Exécutent les instructions du NameNode (réplication, suppression)

#### 🔄 Secondary NameNode

**Attention :** Ce n'est PAS un NameNode de backup !

Le Secondary NameNode :

- Fusionne périodiquement les fichiers FSImage et EditLog
- Crée des checkpoints pour accélérer le redémarrage du NameNode
- Réduit la charge du NameNode principal

*Note : En production, on utilise plutôt la configuration High Availability avec un Standby NameNode.*

## 🧩 3. Blocs et Réplication

### Concept de Blocs

Dans HDFS, les fichiers sont découpés en **blocs** de taille fixe.

| Version Hadoop | Taille de Bloc par Défaut |
| --- | --- |
| Hadoop 1.x | 64 MB |
| Hadoop 2.x et 3.x | 128 MB |

#### Exemple

Un fichier de 300 MB sera découpé en :

- Bloc 1 : 128 MB
- Bloc 2 : 128 MB
- Bloc 3 : 44 MB (reste du fichier)

### Pourquoi des Blocs Aussi Gros ?

#### 📉 Minimiser les Métadonnées

Moins de blocs = moins de métadonnées à gérer dans le NameNode

#### ⚡ Optimiser le Débit

Transferts séquentiels longs = meilleur débit réseau et disque

#### 🔍 Réduire le Seek Time

Moins de déplacements de la tête de lecture sur le disque

### Réplication des Blocs

Chaque bloc est **répliqué** sur plusieurs DataNodes pour assurer la tolérance aux pannes.
Le facteur de réplication par défaut est **3**.

```bash
Fichier original (300 MB)
         ↓
Découpage en blocs
         ↓
┌────────┬────────┬────────┐
│ Bloc A │ Bloc B │ Bloc C │
│ 128 MB │ 128 MB │ 44 MB  │
└────────┴────────┴────────┘
         ↓
Réplication (facteur 3)

Rack 1              Rack 2              Rack 3
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ DataNode 1  │    │ DataNode 3  │    │ DataNode 5  │
│ A, B        │    │ A, C        │    │ B, C        │
├─────────────┤    ├─────────────┤    ├─────────────┤
│ DataNode 2  │    │ DataNode 4  │    │ DataNode 6  │
│ B, C        │    │ A, B        │    │ A           │
└─────────────┘    └─────────────┘    └─────────────┘
```

### Stratégie de Placement des Répliques

### 🎯 Politique par Défaut (Rack Awareness)

- **Réplique 1** : Sur le nœud local (ou aléatoire si écriture depuis l'extérieur)
- **Réplique 2** : Sur un nœud d'un rack différent
- **Réplique 3** : Sur un autre nœud du même rack que la réplique 2

**Avantages :** Balance entre fiabilité (tolérance aux pannes de rack) et
performance réseau (2 répliques sur le même rack = moins de bande passante inter-rack).

## ⚙️ 4. Lecture et Écriture dans HDFS

### Processus de Lecture

```bash
1. Client demande au NameNode les métadonnées du fichier
   ↓
2. NameNode retourne la liste des blocs et leur localisation
   ↓
3. Client contacte directement les DataNodes pour lire les blocs
   ↓
4. Client reçoit les données et les assemble
```

#### Optimisation

Le client lit toujours depuis le DataNode le plus proche (même rack, puis même datacenter).
Cela minimise la latence et la consommation de bande passante réseau.

### Processus d'Écriture

```bash
1. Client demande au NameNode de créer un nouveau fichier
   ↓
2. NameNode vérifie les permissions et crée l'entrée
   ↓
3. Client découpe le fichier en blocs et demande les DataNodes cibles
   ↓
4. NameNode fournit une liste de DataNodes pour chaque bloc
   ↓
5. Client envoie le premier bloc au premier DataNode
   ↓
6. Le DataNode réplique automatiquement vers les autres DataNodes (pipeline)
   ↓
7. Une fois tous les blocs écrits et répliqués, le fichier est "fermé"
```

#### Pipeline de Réplication

```bash
Client  →  DataNode 1  →  DataNode 2  →  DataNode 3
                ↓              ↓              ↓
              ACK 1  ←  ACK 2  ←  ACK 3
```

Les données sont envoyées en pipeline : pendant que DataNode 1 reçoit le bloc, il commence
déjà à l'envoyer à DataNode 2, qui l'envoie à DataNode 3. C'est très efficace !

## 💻 5. Commandes HDFS Essentielles

HDFS propose des commandes similaires aux commandes Unix pour manipuler les fichiers.

### Format Général

```bash
hdfs dfs -<commande> <arguments>
# ou
hadoop fs -<commande> <arguments>
```

### Commandes de Base

| Commande | Description | Exemple |
| --- | --- | --- |
| ls | Lister les fichiers et répertoires | `hdfs dfs -ls /user/data` |
| mkdir | Créer un répertoire | `hdfs dfs -mkdir /user/mydir` |
| put | Copier un fichier local vers HDFS | `hdfs dfs -put data.txt /user/data/` |
| get | Copier un fichier HDFS vers local | `hdfs dfs -get /user/data/result.txt .` |
| cat | Afficher le contenu d'un fichier | `hdfs dfs -cat /user/data/log.txt` |
| rm | Supprimer un fichier | `hdfs dfs -rm /user/data/old.txt` |
| rm -r | Supprimer un répertoire | `hdfs dfs -rm -r /user/data/olddir` |
| cp | Copier dans HDFS | `hdfs dfs -cp /src/file.txt /dest/` |
| mv | Déplacer/renommer dans HDFS | `hdfs dfs -mv /old/path /new/path` |
| du | Taille des fichiers/répertoires | `hdfs dfs -du -h /user/data` |
| df | Espace disque disponible | `hdfs dfs -df -h` |

### Commandes Avancées

| Commande | Description | Exemple |
| --- | --- | --- |
| copyFromLocal | Copier local → HDFS (idem put) | `hdfs dfs -copyFromLocal data.txt /user/` |
| copyToLocal | Copier HDFS → local (idem get) | `hdfs dfs -copyToLocal /user/data.txt .` |
| getmerge | Fusionner plusieurs fichiers HDFS en un seul local | `hdfs dfs -getmerge /user/logs/* output.log` |
| tail | Afficher la fin d'un fichier | `hdfs dfs -tail /user/logs/app.log` |
| chmod | Changer les permissions | `hdfs dfs -chmod 755 /user/data` |
| chown | Changer le propriétaire | `hdfs dfs -chown user:group /user/data` |
| setrep | Modifier le facteur de réplication | `hdfs dfs -setrep -w 5 /user/important.txt` |
| stat | Afficher les statistiques d'un fichier | `hdfs dfs -stat %r /user/data.txt` |

#### Exercice Pratique : Commandes HDFS

À faire dans votre environnement Hadoop (vous le configurerez dans la Partie 6) :

1. Créer un répertoire `/user/votrenom/tp1`
2. Créer un fichier local contenant "Hello Hadoop" et le copier dans HDFS
3. Lister le contenu du répertoire dans HDFS
4. Afficher le contenu du fichier depuis HDFS
5. Vérifier le facteur de réplication du fichier
6. Modifier le facteur de réplication à 5
7. Supprimer le fichier

## 🛡️ 6. Tolérance aux Pannes

### Mécanismes de Protection

#### 💓 Heartbeats

Les DataNodes envoient des heartbeats au NameNode toutes les 3 secondes. Si pas de heartbeat pendant 10 minutes → DataNode considéré comme mort.

#### 🔄 Ré-réplication Automatique

Si un DataNode tombe, le NameNode lance automatiquement la réplication des blocs manquants vers d'autres DataNodes.

#### ✅ Checksums

Chaque bloc est accompagné d'un checksum CRC-32. À chaque lecture, le checksum est vérifié pour détecter la corruption.

#### 📸 Snapshots

Possibilité de créer des snapshots en lecture seule de l'arborescence HDFS pour la protection des données.

### Scénarios de Panne

| Type de Panne | Impact | Récupération |
| --- | --- | --- |
| Panne d'un DataNode | Faible - Données toujours accessibles via répliques | Automatique - Ré-réplication des blocs |
| Panne d'un Rack | Faible - Répliques sur autres racks | Automatique - Ré-réplication |
| Corruption de Bloc | Faible - Lecture depuis réplique saine | Automatique - Bloc corrompu supprimé et ré-répliqué |
| Panne du NameNode | **Critique** - Cluster inaccessible | Manuelle (sans HA) ou Automatique (avec HA) |

## 📝 Résumé de la Partie 2

### Points Clés à Retenir

- HDFS utilise une architecture Master (NameNode) / Slaves (DataNodes)
- Les fichiers sont découpés en blocs de 128 MB (par défaut)
- Chaque bloc est répliqué 3 fois par défaut pour la tolérance aux pannes
- Le NameNode gère les métadonnées, les DataNodes stockent les données
- Les commandes HDFS sont similaires aux commandes Unix
- HDFS est optimisé pour les gros fichiers et les accès séquentiels
- La réplication et les checksums assurent la fiabilité des données

#### ✅ Prêt pour la Suite ?

Vous maîtrisez maintenant HDFS, le système de stockage de Hadoop. Dans la partie suivante, nous découvrirons **MapReduce**, le paradigme de traitement parallèle des données.