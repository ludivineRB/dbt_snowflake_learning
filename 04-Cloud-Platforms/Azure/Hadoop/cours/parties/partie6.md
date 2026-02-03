## 🎯 Objectifs d'Apprentissage

- Comprendre les modes de déploiement Hadoop
- Installer Hadoop en mode Pseudo-distribué
- Configurer HDFS et YARN
- Démarrer et arrêter les services Hadoop
- Vérifier l'installation

## 🔧 1. Modes de Déploiement

| Mode | Description | Cas d'Usage |
| --- | --- | --- |
| **Standalone** | Processus unique, pas de HDFS ni YARN | Développement, débogage local |
| **Pseudo-distribué** | Tous les démons sur une seule machine | Apprentissage, tests, développement |
| **Distribué** | Cluster multi-nœuds (production) | Production, environnements réels |

#### Pour ce TP

Nous allons installer Hadoop en **mode Pseudo-distribué** sur une machine Linux unique.
C'est le meilleur mode pour apprendre car il simule un vrai cluster avec tous les démons Hadoop.

## 📋 2. Prérequis

### Environnement Requis

#### 💻 Système d'Exploitation

Linux (Ubuntu, CentOS, Debian) ou macOS

#### ☕ Java

OpenJDK 8 ou 11 (JDK 8 recommandé pour Hadoop 3.x)

#### 🔑 SSH

OpenSSH installé et configuré

#### 💾 Ressources

Minimum 4 GB RAM, 20 GB disque

### Installation de Java

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install openjdk-8-jdk -y

# CentOS/RHEL
sudo yum install java-1.8.0-openjdk-devel -y

# Vérifier l'installation
java -version

# Configurer JAVA_HOME
echo 'export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64' >> ~/.bashrc
echo 'export PATH=$PATH:$JAVA_HOME/bin' >> ~/.bashrc
source ~/.bashrc
```

### Configuration SSH sans mot de passe

```bash
# Installer SSH (si nécessaire)
sudo apt install openssh-server openssh-client -y

# Générer une clé SSH
ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa

# Autoriser la connexion sans mot de passe
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
chmod 0600 ~/.ssh/authorized_keys

# Tester
ssh localhost
# Tapez 'exit' pour quitter
```

## 📥 3. Téléchargement et Installation de Hadoop

### Télécharger Hadoop

```bash
# Aller dans le répertoire home
cd ~

# Télécharger Hadoop 3.3.6 (version stable)
wget https://downloads.apache.org/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz

# Extraire l'archive
tar -xzvf hadoop-3.3.6.tar.gz

# Renommer pour simplifier
mv hadoop-3.3.6 hadoop

# Supprimer l'archive
rm hadoop-3.3.6.tar.gz
```

### Configurer les Variables d'Environnement

```bash
# Ajouter à ~/.bashrc
cat >> ~/.bashrc << 'EOF'
# Hadoop Environment Variables
export HADOOP_HOME=$HOME/hadoop
export HADOOP_INSTALL=$HADOOP_HOME
export HADOOP_MAPRED_HOME=$HADOOP_HOME
export HADOOP_COMMON_HOME=$HADOOP_HOME
export HADOOP_HDFS_HOME=$HADOOP_HOME
export YARN_HOME=$HADOOP_HOME
export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
export HADOOP_OPTS="-Djava.library.path=$HADOOP_HOME/lib/native"
EOF

# Recharger le fichier
source ~/.bashrc

# Vérifier
hadoop version
```

## ⚙️ 4. Configuration de Hadoop

Les fichiers de configuration se trouvent dans `$HADOOP_HOME/etc/hadoop/`

### 1. hadoop-env.sh

```bash
# Éditer le fichier
nano $HADOOP_HOME/etc/hadoop/hadoop-env.sh

# Ajouter/modifier cette ligne :
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
```

### 2. core-site.xml

```bash
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
    <!-- URI du système de fichiers par défaut (HDFS NameNode) -->
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://localhost:9000</value>
    </property>

    <!-- Répertoire temporaire -->
    <property>
        <name>hadoop.tmp.dir</name>
        <value>/home/<votreuser>/hadoop_tmp</value>
    </property>
</configuration>
```

#### Important

Remplacez `<votreuser>` par votre nom d'utilisateur Linux.

### 3. hdfs-site.xml

```bash
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
    <!-- Facteur de réplication (1 car une seule machine) -->
    <property>
        <name>dfs.replication</name>
        <value>1</value>
    </property>

    <!-- Répertoire du NameNode -->
    <property>
        <name>dfs.namenode.name.dir</name>
        <value>/home/<votreuser>/hadoop_data/namenode</value>
    </property>

    <!-- Répertoire du DataNode -->
    <property>
        <name>dfs.datanode.data.dir</name>
        <value>/home/<votreuser>/hadoop_data/datanode</value>
    </property>
</configuration>
```

### 4. mapred-site.xml

```bash
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
    <!-- Framework MapReduce utilise YARN -->
    <property>
        <name>mapreduce.framework.name</name>
        <value>yarn</value>
    </property>

    <!-- ApplicationMaster pour MapReduce -->
    <property>
        <name>yarn.app.mapreduce.am.env</name>
        <value>HADOOP_MAPRED_HOME=$HADOOP_HOME</value>
    </property>

    <property>
        <name>mapreduce.map.env</name>
        <value>HADOOP_MAPRED_HOME=$HADOOP_HOME</value>
    </property>

    <property>
        <name>mapreduce.reduce.env</name>
        <value>HADOOP_MAPRED_HOME=$HADOOP_HOME</value>
    </property>
</configuration>
```

### 5. yarn-site.xml

```bash
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <!-- Classe du shuffle handler pour MapReduce -->
    <property>
        <name>yarn.nodemanager.aux-services</name>
        <value>mapreduce_shuffle</value>
    </property>

    <!-- ResourceManager hostname -->
    <property>
        <name>yarn.resourcemanager.hostname</name>
        <value>localhost</value>
    </property>

    <!-- Mémoire disponible pour YARN (ajuster selon vos ressources) -->
    <property>
        <name>yarn.nodemanager.resource.memory-mb</name>
        <value>4096</value>
    </property>

    <!-- VCores disponibles -->
    <property>
        <name>yarn.nodemanager.resource.cpu-vcores</name>
        <value>2</value>
    </property>
</configuration>
```

### Créer les Répertoires

```bash
# Créer les répertoires de données
mkdir -p ~/hadoop_tmp
mkdir -p ~/hadoop_data/namenode
mkdir -p ~/hadoop_data/datanode
```

## 🚀 5. Démarrage de Hadoop

### Formater le NameNode

#### ⚠️ Attention

Ne formater qu'à la **première installation**. Formater à nouveau supprime toutes les données HDFS !

```bash
# Formater le NameNode
hdfs namenode -format

# Vous devriez voir : "Storage directory ... has been successfully formatted."
```

### Démarrer HDFS

```bash
# Démarrer NameNode et DataNode
start-dfs.sh

# Vérifier les processus actifs
jps

# Vous devriez voir :
# - NameNode
# - DataNode
# - SecondaryNameNode
# - Jps
```

### Démarrer YARN

```bash
# Démarrer ResourceManager et NodeManager
start-yarn.sh

# Vérifier avec jps
jps

# Vous devriez maintenant voir en plus :
# - ResourceManager
# - NodeManager
```

### Arrêter Hadoop

```bash
# Arrêter YARN
stop-yarn.sh

# Arrêter HDFS
stop-dfs.sh

# Ou tout arrêter d'un coup
stop-all.sh
```

## ✅ 6. Vérification de l'Installation

### 1. Interfaces Web

| Service | URL | Description |
| --- | --- | --- |
| NameNode | <http://localhost:9870> | Interface HDFS |
| ResourceManager | <http://localhost:8088> | Interface YARN |
| Secondary NameNode | <http://localhost:9868> | Checkpoint NameNode |

### 2. Tests en Ligne de Commande

```bash
# Créer un répertoire dans HDFS
hdfs dfs -mkdir -p /user/$USER

# Créer un fichier de test local
echo "Hello Hadoop World" > test.txt

# Copier le fichier dans HDFS
hdfs dfs -put test.txt /user/$USER/

# Lister les fichiers
hdfs dfs -ls /user/$USER/

# Afficher le contenu
hdfs dfs -cat /user/$USER/test.txt

# Voir l'espace disque HDFS
hdfs dfs -df -h

# Rapport HDFS
hdfs dfsadmin -report
```

### 3. Test avec un Job MapReduce

```bash
# Préparer les données d'entrée
hdfs dfs -mkdir -p /user/$USER/wordcount/input
echo "Hello Hadoop Hello World" > words.txt
echo "Hadoop is powerful" >> words.txt
hdfs dfs -put words.txt /user/$USER/wordcount/input/

# Exécuter l'exemple WordCount fourni avec Hadoop
hadoop jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-*.jar \
    wordcount \
    /user/$USER/wordcount/input \
    /user/$USER/wordcount/output

# Voir les résultats
hdfs dfs -cat /user/$USER/wordcount/output/part-r-00000

# Résultat attendu :
# Hadoop  2
# Hello   2
# World   1
# is      1
# powerful 1
```

## 🛠️ 7. Dépannage

### Problèmes Courants

#### Les démons ne démarrent pas

**Vérifier les logs :**

```bash
# Logs dans $HADOOP_HOME/logs/
tail -f $HADOOP_HOME/logs/hadoop-*-namenode-*.log
```

**Causes fréquentes :**

- JAVA\_HOME mal configuré
- Ports déjà utilisés
- SSH sans mot de passe non configuré
- Permissions incorrectes sur les répertoires

#### DataNode ne se connecte pas au NameNode

**Solutions :**

```bash
# Arrêter tout
stop-all.sh

# Nettoyer les données
rm -rf ~/hadoop_data/*
rm -rf ~/hadoop_tmp/*

# Reformater
hdfs namenode -format

# Redémarrer
start-dfs.sh
start-yarn.sh
```

#### Commandes Utiles de Diagnostic

```bash
# Vérifier les processus Java en cours
jps

# Tester la connectivité SSH
ssh localhost

# Vérifier les ports ouverts
netstat -tuln | grep -E '9870|8088|9000'

# Voir la version de Hadoop
hadoop version

# Rapport détaillé HDFS
hdfs dfsadmin -report
```

## 🔒 8. Bonnes Pratiques et Sécurité

#### 📊 Monitoring

- Consulter régulièrement les UI web
- Surveiller les logs
- Vérifier l'espace disque HDFS

#### 💾 Backups

- Sauvegarder les données critiques
- Exporter les métadonnées du NameNode
- Documenter la configuration

#### 🔐 Sécurité

- Configurer Kerberos en production
- Utiliser des ACLs HDFS
- Sécuriser les ports avec firewall

#### ⚡ Performance

- Ajuster la mémoire YARN
- Optimiser le facteur de réplication
- Utiliser la compression

## 📝 Résumé de la Partie 6

### Points Clés à Retenir

- 3 modes de déploiement : Standalone, Pseudo-distribué, Distribué
- Prérequis : Java, SSH, ressources système suffisantes
- Configuration principale via 5 fichiers XML dans etc/hadoop/
- Formater le NameNode uniquement à la première installation
- Démarrage : start-dfs.sh puis start-yarn.sh
- Vérification via interfaces web (ports 9870 et 8088) et commandes CLI
- Les logs sont essentiels pour le dépannage

#### 🎉 Félicitations !

Vous avez terminé le cours Hadoop ! Vous êtes maintenant capable d'installer, configurer et utiliser
un cluster Hadoop. Pour mettre en pratique vos connaissances, passez au **Brief pratique**
qui vous guidera dans la création d'un pipeline Big Data complet.