## 🎯 Objectifs d'Apprentissage

- Comprendre les enjeux du Big Data
- Découvrir l'historique et l'origine de Hadoop
- Identifier les composants de l'écosystème Hadoop
- Connaître les cas d'usage réels de Hadoop

## 📊 1. Qu'est-ce que le Big Data ?

### Définition

Le **Big Data** désigne des ensembles de données si volumineux et complexes qu'ils dépassent
les capacités des outils traditionnels de gestion de bases de données pour les capturer, stocker, gérer et analyser.

### Les 6 V du Big Data

#### 📈 Volume

Quantité massive de données générées chaque seconde (pétaoctets, exaoctets)

- Logs de serveurs
- Données IoT
- Transactions financières

#### ⚡ Vélocité

Vitesse à laquelle les données sont générées et doivent être traitées

- Streaming en temps réel
- Flux de capteurs
- Réseaux sociaux

#### 🎨 Variété

Diversité des types et formats de données

- Structurées (SQL)
- Semi-structurées (JSON, XML)
- Non structurées (texte, images, vidéos)

#### ✅ Véracité

Qualité et fiabilité des données

- Données bruitées
- Incohérences
- Validation nécessaire

#### 💰 Valeur

Capacité à extraire des insights utiles

- Analytics
- Machine Learning
- Décisions business

#### 🔄 Variabilité

Évolution de la signification des données

- Contexte changeant
- Saisonnalité
- Tendances

#### Exemple Concret

**Facebook** génère plus de 4 pétaoctets de données par jour, incluant :
photos, vidéos, messages, likes, commentaires, données de localisation, etc.
Ces données sont de types variés et arrivent en continu.

## 🕰️ 2. Historique et Origine de Hadoop

### La Genèse

```bash
2003 : Google publie le papier sur GFS (Google File System)
  ↓
2004 : Google publie le papier sur MapReduce
  ↓
2005 : Doug Cutting et Mike Cafarella créent Hadoop
  ↓
2006 : Yahoo! engage Doug Cutting - Hadoop devient un projet Apache
  ↓
2008 : Hadoop devient un projet Apache de top niveau
  ↓
2011+ : Explosion de l'écosystème Hadoop (Hive, Pig, HBase, etc.)
  ↓
Aujourd'hui : Hadoop 3.x avec de nombreuses améliorations
```

#### Le saviez-vous ?

Le nom "Hadoop" vient du jouet en peluche en forme d'éléphant jaune du fils de Doug Cutting.
C'est pourquoi le logo d'Hadoop est un éléphant jaune ! 🐘

### Influence de Google

| Technologie Google | Équivalent Hadoop | Fonction |
| --- | --- | --- |
| GFS (Google File System) | HDFS (Hadoop Distributed File System) | Stockage distribué |
| MapReduce (Google) | MapReduce (Hadoop) | Traitement parallèle |
| BigTable | HBase | Base de données NoSQL |

## 🏗️ 3. Architecture Générale de Hadoop

### Les Composants Principaux

Hadoop est composé de 4 modules fondamentaux :

#### 📁 Hadoop Common

Bibliothèques et utilitaires communs nécessaires aux autres modules Hadoop

#### 💾 HDFS

Système de fichiers distribué qui stocke les données sur plusieurs machines

#### ⚙️ MapReduce

Framework de traitement parallèle pour traiter de grandes quantités de données

#### 🎯 YARN

Gestionnaire de ressources pour la planification et l'exécution des tâches

### Architecture Simplifiée

```bash
┌─────────────────────────────────────────────────────────┐
│                    Écosystème Hadoop                    │
├─────────────────────────────────────────────────────────┤
│  Hive  │  Pig  │  HBase  │  Sqoop  │  Flume  │  Spark  │
├─────────────────────────────────────────────────────────┤
│                         YARN                            │
│              (Gestion des Ressources)                   │
├──────────────────────┬──────────────────────────────────┤
│      MapReduce       │      Autres Applications         │
│  (Traitement)        │      (Spark, Tez, etc.)         │
├──────────────────────┴──────────────────────────────────┤
│                         HDFS                            │
│              (Stockage Distribué)                       │
└─────────────────────────────────────────────────────────┘
```

### 🔑 Principes Fondamentaux

- **Scalabilité horizontale** : Ajout de machines pour augmenter la capacité
- **Tolérance aux pannes** : Réplication des données et relance automatique des tâches
- **Traitement local** : Le code est envoyé vers les données, pas l'inverse
- **Matériel standard** : Fonctionne sur du matériel commodity (bon marché)
- **Open Source** : Gratuit et communauté active

## 🌐 4. L'Écosystème Hadoop

Hadoop n'est pas qu'un seul logiciel, c'est tout un écosystème de projets complémentaires :

| Outil | Catégorie | Description |
| --- | --- | --- |
| **Hive** | Requêtage SQL | Interface SQL pour interroger des données dans HDFS |
| **Pig** | Scripting | Langage de haut niveau pour traiter des données |
| **HBase** | Base NoSQL | Base de données orientée colonnes sur HDFS |
| **Sqoop** | Import/Export | Transfert de données entre Hadoop et bases relationnelles |
| **Flume** | Ingestion | Collecte et agrégation de logs en temps réel |
| **Spark** | Traitement | Moteur de traitement rapide en mémoire |
| **Oozie** | Orchestration | Planificateur de workflows pour jobs Hadoop |
| **ZooKeeper** | Coordination | Service de coordination pour applications distribuées |

## 💼 5. Cas d'Usage et Entreprises Utilisatrices

### Secteurs d'Application

#### 🏦 Finance

Détection de fraude, analyse de risques, trading algorithmique

#### 🛒 E-commerce

Recommandations produits, analyse du comportement client, optimisation des prix

#### 🏥 Santé

Analyse génomique, dossiers médicaux électroniques, recherche médicale

#### 📱 Télécoms

Analyse des CDR (Call Detail Records), optimisation réseau, prévention du churn

#### 🎬 Médias

Recommandations de contenu, analyse d'audience, personnalisation

#### 🚗 Transport

Optimisation de routes, véhicules connectés, maintenance prédictive

### Entreprises Utilisatrices

#### Quelques exemples célèbres

- **Yahoo!** - Pionnier de l'utilisation de Hadoop (cluster de 42 000 machines)
- **Facebook** - Stockage et analyse de données utilisateurs
- **LinkedIn** - Recommandations et analytics
- **Twitter** - Analyse de tweets et trending topics
- **eBay** - Analyse des transactions et recommandations
- **Spotify** - Recommandations musicales
- **Netflix** - Recommandations de films et séries
- **Airbnb** - Optimisation des prix et recherche

### Cas d'Usage Concret : Netflix

#### 🎬 Système de Recommandation Netflix

Netflix utilise Hadoop pour analyser des milliards d'événements quotidiens :

- Quels films/séries sont regardés ?
- À quel moment l'utilisateur met en pause ou arrête ?
- Quel contenu est ajouté à la liste ?
- Quelles recherches sont effectuées ?
- Sur quels appareils le contenu est visionné ?

Ces données alimentent des algorithmes de Machine Learning qui génèrent
**80% du contenu regardé via les recommandations**.

## ⚖️ 6. Hadoop vs Solutions Traditionnelles

| Critère | SGBD Traditionnel | Hadoop |
| --- | --- | --- |
| **Type de données** | Structurées | Tous types (structurées, semi-structurées, non structurées) |
| **Schéma** | Schema-on-write | Schema-on-read |
| **Scalabilité** | Verticale (scale-up) | Horizontale (scale-out) |
| **Coût** | Élevé (matériel spécialisé) | Faible (commodity hardware) |
| **Traitement** | OLTP (transactionnel) | OLAP (analytique batch) |
| **Latence** | Faible (millisecondes) | Élevée (minutes/heures) |

#### Attention

Hadoop n'est **pas** un remplacement des bases de données traditionnelles !
C'est un outil complémentaire pour des cas d'usage spécifiques nécessitant :

- Traitement de très gros volumes de données
- Analyse de données non structurées
- Traitement batch (non temps-réel)
- Coût de stockage réduit

## 📝 Résumé de la Partie 1

### Points Clés à Retenir

- Le Big Data se caractérise par les 6 V : Volume, Vélocité, Variété, Véracité, Valeur, Variabilité
- Hadoop a été créé par Doug Cutting en s'inspirant des papiers de Google (GFS et MapReduce)
- Hadoop est composé de 4 modules : Common, HDFS, MapReduce, YARN
- L'écosystème Hadoop comprend de nombreux outils (Hive, Pig, HBase, Spark, etc.)
- Hadoop est utilisé par les plus grandes entreprises tech pour l'analyse Big Data
- Hadoop complète les bases de données traditionnelles, ne les remplace pas

#### ✅ Prêt pour la Suite ?

Vous avez maintenant une vue d'ensemble de Hadoop et du Big Data. Dans la partie suivante, nous plongerons dans **HDFS**, le système de fichiers distribué au cœur de Hadoop.