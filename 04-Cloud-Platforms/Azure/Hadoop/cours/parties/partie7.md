## 🎯 Objectifs d'Apprentissage

- Comprendre HDInsight, le service Hadoop managé d'Azure
- Créer un cluster Hadoop sur Azure pas à pas
- Configurer le stockage Azure pour HDFS
- Exécuter des jobs MapReduce sur Azure
- Monitorer et gérer le cluster

## ☁️ 1. Introduction à Azure HDInsight

### Qu'est-ce que HDInsight ?

**Azure HDInsight** est un service cloud managé qui facilite le déploiement et la gestion
de clusters Hadoop, Spark, Hive, HBase, et d'autres frameworks Big Data sur Microsoft Azure.

#### ✅ Avantages

- Déploiement rapide (minutes vs heures)
- Scalabilité élastique
- Paiement à l'usage
- Maintenance simplifiée

#### 💰 Modèle de Tarification

- Facturation par nœud/heure
- Arrêt du cluster pour économiser
- Stockage Azure facturé séparément

#### 🔧 Types de Clusters

- Hadoop (MapReduce, HDFS, YARN)
- Spark (traitement in-memory)
- HBase (NoSQL)
- Interactive Query (Hive LLAP)

#### 💾 Stockage

- Azure Blob Storage
- Azure Data Lake Storage Gen2
- Compatible HDFS

#### Prérequis

- Un compte Microsoft Azure (essai gratuit disponible)
- Crédits Azure (200$ offerts pour les nouveaux comptes)
- Un abonnement Azure actif

## 🚀 2. Création d'un Compte Azure (si nécessaire)

### Étape 1 : S'inscrire sur Azure

```bash
# 1. Aller sur https://azure.microsoft.com/free/
# 2. Cliquer sur "Commencer gratuitement"
# 3. Se connecter avec un compte Microsoft (ou en créer un)
# 4. Remplir les informations de facturation (carte requise mais pas débitée)
# 5. Vérifier votre identité par téléphone
# 6. Accepter les conditions
```

#### Crédits Gratuits

Nouveau compte Azure = **200$ de crédits valables 30 jours** + services gratuits 12 mois

### Étape 2 : Accéder au Portail Azure

1. Se connecter sur <https://portal.azure.com>
2. Vérifier que votre abonnement est actif (menu "Abonnements")
3. Vous êtes prêt à créer votre cluster !

## 🔧 3. Création d'un Cluster HDInsight - Pas à Pas

### Étape 1 : Créer un Groupe de Ressources

#### Qu'est-ce qu'un Groupe de Ressources ?

Un conteneur logique qui regroupe toutes les ressources Azure liées (cluster, stockage, réseau).
Permet de gérer et supprimer facilement toutes les ressources d'un projet.

```bash
# Dans le Portail Azure :

1. Cliquer sur "Groupes de ressources" dans le menu
2. Cliquer sur "+ Créer"
3. Remplir les informations :
   - Abonnement : Votre abonnement Azure
   - Nom du groupe : hadoop-formation-rg
   - Région : France Central (ou la plus proche)
4. Cliquer sur "Vérifier + créer"
5. Cliquer sur "Créer"
```

### Étape 2 : Créer un Compte de Stockage Azure

Le cluster HDInsight a besoin d'un stockage pour HDFS.

```bash
# Dans le Portail Azure :

1. Cliquer sur "+ Créer une ressource"
2. Rechercher "Compte de stockage"
3. Cliquer sur "Créer"
4. Remplir :
   - Groupe de ressources : hadoop-formation-rg
   - Nom du compte : hadoopstorage[votreID] (doit être unique)
   - Région : France Central
   - Performances : Standard
   - Redondance : LRS (Stockage localement redondant)
5. Cliquer sur "Vérifier + créer"
6. Cliquer sur "Créer"
7. Attendre la fin du déploiement (1-2 minutes)
```

### Étape 3 : Créer un Conteneur Blob

```bash
# Une fois le compte de stockage créé :

1. Aller dans le compte de stockage créé
2. Dans le menu à gauche, cliquer sur "Conteneurs"
3. Cliquer sur "+ Conteneur"
4. Nom : hadoop-data
5. Niveau d'accès public : Privé
6. Cliquer sur "Créer"
```

### Étape 4 : Créer le Cluster HDInsight

```bash
# Dans le Portail Azure :

1. Cliquer sur "+ Créer une ressource"
2. Rechercher "HDInsight"
3. Cliquer sur "Azure HDInsight"
4. Cliquer sur "Créer"

# Onglet "Informations de base" :
─────────────────────────────────────
- Abonnement : Votre abonnement
- Groupe de ressources : hadoop-formation-rg
- Nom du cluster : hadoop-cluster-[votreID]
- Région : France Central
- Type de cluster : Hadoop
- Version : Hadoop 3.1.1 (ou la plus récente)
- Nom d'utilisateur du cluster : admin
- Mot de passe : [Créer un mot de passe fort]
  (ex: Hadoop@2025!)
- Nom d'utilisateur SSH : sshuser
- Utiliser le même mot de passe : Oui

Cliquer sur "Suivant : Stockage"

# Onglet "Stockage" :
─────────────────────────────────────
- Type de stockage principal : Azure Storage
- Méthode de sélection : Sélectionner dans la liste
- Compte de stockage : hadoopstorage[votreID]
- Conteneur : hadoop-data
- Identité managée : (laisser par défaut)

Cliquer sur "Suivant : Sécurité + réseau"

# Onglet "Sécurité + réseau" :
─────────────────────────────────────
- Laisser les paramètres par défaut
Cliquer sur "Suivant : Configuration + tarification"

# Onglet "Configuration + tarification" :
─────────────────────────────────────
- Type de nœud : Standard_D3_v2 (ou Standard_D4_v2)
- Nombre de nœuds Worker : 2
- Nombre de nœuds Head : 2 (défaut)

Cliquer sur "Suivant : Étiquettes" (optionnel)
Cliquer sur "Suivant : Vérifier + créer"
Vérifier le récapitulatif
Cliquer sur "Créer"
```

#### ⏱️ Temps de Création

La création du cluster prend entre **15 et 30 minutes**.
Vous pouvez suivre la progression dans les notifications (icône cloche en haut à droite).

#### 💰 Attention aux Coûts

Un cluster HDInsight avec 2 nœuds worker coûte environ **5-10€/jour**.
Pensez à **supprimer le cluster** après vos tests pour éviter les frais !

## 🔌 4. Connexion au Cluster

### Méthode 1 : Interface Web Ambari

```bash
# Une fois le cluster créé :

1. Aller dans votre cluster HDInsight
2. Dans le menu à gauche, cliquer sur "Tableaux de bord du cluster"
3. Cliquer sur "Ambari home"
4. Se connecter avec :
   - Utilisateur : admin
   - Mot de passe : [le mot de passe que vous avez créé]

# URL directe :
https://hadoop-cluster-[votreID].azurehdinsight.net
```

### Méthode 2 : SSH vers le Nœud Head

```bash
# Depuis votre terminal local :

ssh sshuser@hadoop-cluster-[votreID]-ssh.azurehdinsight.net

# Entrer le mot de passe SSH
# Vous êtes maintenant connecté au nœud Head du cluster !

# Vérifier Hadoop
hadoop version

# Vérifier HDFS
hdfs dfs -ls /

# Vérifier YARN
yarn node -list
```

## 📂 5. Utiliser le Stockage Azure avec Hadoop

### Azure Blob Storage comme HDFS

HDInsight utilise Azure Blob Storage comme système de fichiers par défaut,
compatible avec les commandes HDFS.

#### Format des Chemins

```bash
# Format WASB (Windows Azure Storage Blob)
wasb://[conteneur]@[compte-stockage].blob.core.windows.net/[chemin]

# Exemple :
wasb://hadoop-data@hadoopstorage123.blob.core.windows.net/user/data

# Format court (si c'est le stockage par défaut)
/user/data
```

#### Commandes HDFS sur Azure Storage

```bash
# Lister les fichiers
hdfs dfs -ls /

# Créer un répertoire
hdfs dfs -mkdir /user/sshuser/test

# Créer un fichier local et le copier
echo "Hello Azure Hadoop" > test.txt
hdfs dfs -put test.txt /user/sshuser/

# Lire le fichier
hdfs dfs -cat /user/sshuser/test.txt

# Le fichier est stocké dans Azure Blob Storage !
# Vous pouvez le voir dans le Portail Azure :
# Compte de stockage → Conteneurs → hadoop-data
```

## 🎯 6. Exécuter un Job MapReduce sur Azure

### Exemple : WordCount en Python

#### Étape 1 : Créer les Scripts Python

```bash
# Connecté en SSH au cluster

# Créer mapper.py
cat > mapper.py << 'EOF'
#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()
    words = line.split()
    for word in words:
        print(f"{word}\t1")
EOF

# Créer reducer.py
cat > reducer.py << 'EOF'
#!/usr/bin/env python3
import sys

current_word = None
current_count = 0

for line in sys.stdin:
    line = line.strip()
    word, count = line.split('\t')
    count = int(count)

    if current_word == word:
        current_count += count
    else:
        if current_word:
            print(f"{current_word}\t{current_count}")
        current_word = word
        current_count = count

if current_word:
    print(f"{current_word}\t{current_count}")
EOF

# Rendre exécutables
chmod +x mapper.py reducer.py
```

#### Étape 2 : Préparer les Données

```bash
# Créer un fichier de test
cat > input.txt << EOF
Azure Hadoop HDInsight
Cloud Computing with Hadoop
Big Data on Azure
EOF

# Créer le répertoire dans HDFS (Azure Storage)
hdfs dfs -mkdir -p /user/sshuser/wordcount/input

# Copier le fichier
hdfs dfs -put input.txt /user/sshuser/wordcount/input/

# Vérifier
hdfs dfs -cat /user/sshuser/wordcount/input/input.txt
```

#### Étape 3 : Lancer le Job

```bash
# Lancer le job Hadoop Streaming
hadoop jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-streaming.jar \
    -input /user/sshuser/wordcount/input \
    -output /user/sshuser/wordcount/output \
    -mapper mapper.py \
    -reducer reducer.py \
    -file mapper.py \
    -file reducer.py

# Voir les résultats
hdfs dfs -cat /user/sshuser/wordcount/output/part-00000
```

#### Étape 4 : Suivre le Job dans YARN

```bash
# URL YARN ResourceManager :
https://hadoop-cluster-[votreID].azurehdinsight.net/yarnui

# Se connecter avec :
- Utilisateur : admin
- Mot de passe : [votre mot de passe]
```

## 📊 7. Utiliser Hive sur HDInsight

### Connexion à Hive

```bash
# Depuis SSH sur le cluster
beeline -u 'jdbc:hive2://localhost:10001/;transportMode=http'

# Ou connectez-vous à Hive View dans Ambari
```

### Exemple de Requêtes Hive

```bash
-- Créer une table
CREATE TABLE sales (
    product STRING,
    quantity INT,
    price DOUBLE
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;

-- Charger des données depuis Azure Storage
LOAD DATA INPATH '/user/sshuser/sales.csv' INTO TABLE sales;

-- Requête
SELECT product, SUM(quantity * price) as revenue
FROM sales
GROUP BY product
ORDER BY revenue DESC;
```

## 🔍 8. Monitoring et Gestion

### Interfaces de Monitoring

| Interface | URL | Utilisation |
| --- | --- | --- |
| Ambari | https://[cluster].azurehdinsight.net | Gestion complète du cluster |
| YARN UI | https://[cluster].azurehdinsight.net/yarnui | Suivi des jobs YARN |
| Job History | https://[cluster].azurehdinsight.net/jobhistory | Historique des jobs |
| Portail Azure | portal.azure.com | Métriques et alertes |

### Scaler le Cluster

```bash
# Dans le Portail Azure :

1. Aller dans votre cluster HDInsight
2. Menu à gauche → "Taille du cluster"
3. Modifier le nombre de nœuds Worker (2 à 10+)
4. Cliquer sur "Enregistrer"
5. Le scaling prend 5-10 minutes
```

## 🗑️ 9. Nettoyage et Suppression

#### ⚠️ Important : Éviter les Frais

Après vos tests, **supprimez le cluster** pour arrêter la facturation !
Le stockage Azure (quelques centimes) peut être conservé si vous voulez garder vos données.

### Supprimer le Cluster

```bash
# Méthode 1 : Portail Azure
1. Aller dans votre cluster HDInsight
2. Cliquer sur "Supprimer" en haut
3. Taper le nom du cluster pour confirmer
4. Cliquer sur "Supprimer"

# Méthode 2 : Azure CLI
az hdinsight delete --name hadoop-cluster-[votreID] --resource-group hadoop-formation-rg

# Pour tout supprimer (cluster + stockage + groupe de ressources) :
az group delete --name hadoop-formation-rg --yes
```

### Vérifier les Coûts

```bash
# Dans le Portail Azure :

1. Menu → "Cost Management + Billing"
2. → "Cost analysis"
3. Vérifier les coûts par ressource
4. Vérifier qu'aucune ressource n'est en cours d'exécution
```

## 📝 Résumé de la Partie 7

### Points Clés à Retenir

- Azure HDInsight = Hadoop managé dans le cloud
- Création d'un cluster en 15-30 minutes via le Portail Azure
- Azure Blob Storage remplace HDFS (compatible)
- Même commandes Hadoop que sur un cluster local
- Interfaces Ambari et YARN pour la gestion et le monitoring
- Scaling facile du nombre de nœuds
- ⚠️ Supprimer le cluster après usage pour éviter les frais

#### ✅ Prêt pour la Suite ?

Vous savez maintenant déployer Hadoop sur Azure ! Dans la partie suivante, nous allons pratiquer pas à pas avec des exercices guidés.