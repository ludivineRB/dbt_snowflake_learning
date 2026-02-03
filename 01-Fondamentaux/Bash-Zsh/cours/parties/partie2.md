## 2. Navigation et Gestion de Fichiers

### Navigation dans le système de fichiers

#### Structure des répertoires Linux/Unix

```bash
/                    (root - racine du système)
├── bin/            (binaires essentiels)
├── etc/            (fichiers de configuration)
├── home/           (répertoires utilisateurs)
│   └── username/   (votre home directory)
├── opt/            (logiciels optionnels)
├── tmp/            (fichiers temporaires)
├── usr/            (programmes utilisateur)
├── var/            (données variables: logs, caches)
└── data/           (souvent utilisé pour les données)
```

#### Commandes de navigation essentielles

| Commande | Description | Exemple |
| --- | --- | --- |
| `pwd` | Print Working Directory - affiche le répertoire courant | `pwd` |
| `cd` | Change Directory - changer de répertoire | `cd /home/data` |
| `cd ~` | Aller au home directory | `cd ~` |
| `cd -` | Revenir au répertoire précédent | `cd -` |
| `cd ..` | Remonter d'un niveau | `cd ..` |
| `ls` | Lister les fichiers et dossiers | `ls -lah` |

```bash
# Afficher le répertoire courant
pwd
# /home/guillaume/projects

# Aller au home directory
cd ~
pwd
# /home/guillaume

# Aller dans un dossier spécifique
cd /var/log

# Remonter d'un niveau
cd ..

# Revenir au répertoire précédent
cd -

# Chemins relatifs vs absolus
cd data/raw              # relatif (depuis le répertoire courant)
cd /home/data/raw        # absolu (depuis la racine)
```

### Lister les fichiers avec ls

| Option | Description | Exemple |
| --- | --- | --- |
| `ls` | Liste simple | `ls` |
| `ls -l` | Format long (détails) | `ls -l` |
| `ls -a` | Afficher les fichiers cachés (commençant par .) | `ls -a` |
| `ls -h` | Tailles lisibles (human-readable) | `ls -lh` |
| `ls -t` | Trier par date de modification | `ls -lt` |
| `ls -S` | Trier par taille | `ls -lS` |
| `ls -R` | Récursif (sous-dossiers) | `ls -R` |

```bash
# Liste complète avec détails et tailles lisibles
ls -lah

# Résultat :
# drwxr-xr-x  5 user group  160B Jan 15 10:30 .
# drwxr-xr-x  8 user group  256B Jan 15 09:00 ..
# -rw-r--r--  1 user group  2.3M Jan 15 10:25 data.csv
# -rw-r--r--  1 user group  156K Jan 15 10:20 config.json
# drwxr-xr-x  3 user group   96B Jan 15 10:00 scripts

# Lister les fichiers CSV uniquement
ls *.csv

# Lister les fichiers par taille décroissante
ls -lhS

# Afficher les 5 plus gros fichiers
ls -lhS | head -6

# Lister avec arborescence (nécessite tree)
tree -L 2 -h
```

#### Comprendre les permissions

Dans `ls -l`, la première colonne indique les permissions :

```bash
-rw-r--r--
│││ │ │ │
│││ │ │ └─ Others (autres)
│││ │ └─── Group (groupe)
│││ └───── Owner (propriétaire)
││└─────── Type (- = fichier, d = dossier, l = lien)
│└──────── r=read, w=write, x=execute
```

### Créer des fichiers et dossiers

```bash
# Créer un dossier
mkdir data

# Créer plusieurs dossiers d'un coup
mkdir raw processed cleaned

# Créer une arborescence complète
mkdir -p data/raw/2024/01
# -p crée les dossiers parents si nécessaire

# Créer un fichier vide
touch config.json

# Créer plusieurs fichiers
touch file1.txt file2.txt file3.txt

# Exemple : structure d'un projet data
mkdir -p project/{data/{raw,processed,cleaned},scripts,logs,config}
tree project/
# project/
# ├── config
# ├── data
# │   ├── cleaned
# │   ├── processed
# │   └── raw
# ├── logs
# └── scripts
```

### Copier et déplacer des fichiers

```bash
# Copier un fichier
cp source.csv destination.csv

# Copier avec confirmation
cp -i source.csv destination.csv

# Copier en préservant les métadonnées
cp -p config.json config_backup.json

# Copier un dossier entier (récursif)
cp -r data/ data_backup/

# Copier plusieurs fichiers vers un dossier
cp file1.csv file2.csv file3.csv /data/raw/

# Déplacer / renommer un fichier
mv old_name.csv new_name.csv

# Déplacer vers un autre dossier
mv data.csv /data/processed/

# Déplacer plusieurs fichiers
mv *.csv /data/raw/

# Renommer avec pattern
for file in *.txt; do
    mv "$file" "${file%.txt}_backup.txt"
done
```

### Supprimer des fichiers et dossiers

#### ⚠️ Attention

La suppression avec `rm` est **définitive**. Il n'y a pas de corbeille en ligne de commande.
Soyez toujours prudent avec `rm -rf` !

```bash
# Supprimer un fichier
rm file.txt

# Supprimer avec confirmation
rm -i file.txt

# Supprimer plusieurs fichiers
rm file1.txt file2.txt file3.txt

# Supprimer tous les CSV
rm *.csv

# Supprimer un dossier vide
rmdir empty_folder

# Supprimer un dossier et son contenu
rm -r folder/

# Forcer la suppression sans confirmation
rm -rf folder/

# DANGER : Ne jamais faire ça !
# rm -rf /    # Détruit tout le système
# rm -rf /*   # Détruit tout le système

# Bonne pratique : vérifier avant de supprimer
ls *.log
rm *.log
```

### Rechercher des fichiers avec find

```bash
# Trouver tous les fichiers CSV
find . -name "*.csv"

# Trouver tous les fichiers modifiés dans les dernières 24h
find . -name "*.csv" -mtime -1

# Trouver les fichiers de plus de 100MB
find . -type f -size +100M

# Trouver et supprimer les fichiers temporaires
find . -name "*.tmp" -delete

# Trouver les fichiers et exécuter une commande
find . -name "*.csv" -exec wc -l {} \;

# Trouver les dossiers vides
find . -type d -empty

# Exemple pratique : trouver les gros fichiers de logs
find /var/log -name "*.log" -size +50M -ls

# Trouver par date de modification
find . -type f -mtime -7          # Modifiés il y a moins de 7 jours
find . -type f -mtime +30         # Modifiés il y a plus de 30 jours

# Combinaison de critères
find . -name "*.csv" -size +10M -mtime -7
```

### Rechercher avec locate (plus rapide)

```bash
# Mettre à jour la base de données locate
sudo updatedb

# Rechercher un fichier
locate data.csv

# Rechercher avec limite de résultats
locate -n 10 "*.csv"

# Rechercher en ignorant la casse
locate -i CONFIG.JSON

# Note : locate est plus rapide que find car il utilise une base de données
# mais elle doit être mise à jour régulièrement
```

### Utilisation du disque : du et df

```bash
# df : Disk Free - espace disque disponible
df -h
# Filesystem      Size   Used  Avail Capacity  Mounted on
# /dev/disk1s1   466Gi  350Gi  100Gi    78%    /

# Afficher uniquement les systèmes de fichiers locaux
df -h --type=ext4

# du : Disk Usage - utilisation de l'espace par répertoire
du -h data/
# 2.3G    data/raw
# 1.8G    data/processed
# 4.1G    data/

# Taille totale d'un dossier
du -sh data/
# 4.1G    data/

# Les 10 plus gros dossiers
du -h . | sort -rh | head -10

# Afficher la taille de chaque sous-dossier
du -h --max-depth=1 . | sort -rh

# Exemple pratique : trouver ce qui prend de la place
du -h --max-depth=2 /var/log | sort -rh | head -20
```

### Permissions et propriétaires

| Commande | Description | Exemple |
| --- | --- | --- |
| `chmod` | Change les permissions | `chmod 755 script.sh` |
| `chown` | Change le propriétaire | `chown user:group file.txt` |
| `chgrp` | Change le groupe | `chgrp dataeng file.csv` |

```bash
# Rendre un script exécutable
chmod +x script.sh

# Permissions en notation numérique
chmod 644 file.txt    # rw-r--r--  (fichier)
chmod 755 script.sh   # rwxr-xr-x  (exécutable)
chmod 700 secret.key  # rwx------  (privé)
chmod 777 shared/     # rwxrwxrwx  (tout le monde)

# Notation numérique expliquée :
# r = 4, w = 2, x = 1
# 7 = 4+2+1 = rwx
# 6 = 4+2   = rw-
# 5 = 4+1   = r-x
# 4 = 4     = r--

# Permissions récursives
chmod -R 755 scripts/

# Changer le propriétaire
sudo chown user:group file.csv

# Changer récursivement
sudo chown -R user:group data/

# Exemples pratiques pour data engineering
chmod 644 *.csv               # Fichiers de données lisibles
chmod 755 *.sh                # Scripts exécutables
chmod 700 ~/.ssh/id_rsa       # Clé SSH privée
chmod 600 config/secrets.env  # Fichier de secrets
```

### Wildcards et Globbing

### 💡 Patterns de glob

- `*` : Correspond à n'importe quelle chaîne de caractères
- `?` : Correspond à un seul caractère
- `[...]` : Correspond à un caractère dans la liste
- `{...,...}` : Expansion d'accolades

```bash
# * : n'importe quoi
ls *.csv                    # Tous les fichiers CSV
ls data*                    # Tous les fichiers commençant par "data"
ls *2024*                   # Tous les fichiers contenant "2024"

# ? : un seul caractère
ls data?.csv                # data1.csv, data2.csv, dataA.csv
ls report_202?-01.csv       # report_2020-01.csv, report_2024-01.csv

# [...] : plage de caractères
ls data[123].csv            # data1.csv, data2.csv, data3.csv
ls file[a-z].txt            # filea.txt, fileb.txt, ...
ls log[0-9][0-9].txt        # log00.txt, log01.txt, ..., log99.txt

# {...} : expansion
ls {data,logs,config}.csv   # data.csv, logs.csv, config.csv
mkdir -p data/{raw,processed,cleaned}

# Combinaisons avancées
ls data_{2023,2024}_*.csv
ls report_[0-9][0-9]_{jan,feb,mar}.csv

# Exemples pratiques en data engineering
# Copier tous les CSV d'une année
cp data/raw/2024*.csv data/processed/

# Supprimer tous les fichiers temporaires
rm *.tmp *.temp *~

# Archiver tous les logs par mois
tar -czf logs_2024-01.tar.gz logs/2024/01/*.log

# Compter les lignes de tous les CSV
wc -l *.csv

# Globbing avec find (plus puissant)
find . -name "data_2024-*.csv"
```

### Exemple pratique : Organisation d'un projet data

```bash
# Créer une structure de projet complète
mkdir -p ~/data_project/{data/{raw,processed,cleaned,archive},scripts,logs,config,docs}

# Créer des sous-dossiers par date
mkdir -p ~/data_project/data/raw/$(date +%Y/%m/%d)

# Copier des données brutes
cp /source/*.csv ~/data_project/data/raw/$(date +%Y/%m/%d)/

# Trouver tous les fichiers de données
find ~/data_project/data -name "*.csv" -o -name "*.json" -o -name "*.parquet"

# Vérifier l'espace utilisé par catégorie
du -sh ~/data_project/data/*

# Archiver les anciennes données (plus de 30 jours)
find ~/data_project/data/raw -type f -mtime +30 -exec mv {} ~/data_project/data/archive/ \;

# Rendre les scripts exécutables
chmod +x ~/data_project/scripts/*.sh

# Lister les fichiers triés par taille
ls -lhS ~/data_project/data/raw/ | head -10

# Nettoyer les fichiers temporaires
find ~/data_project -name "*.tmp" -o -name "*.log" -mtime +7 -delete
```

### Exercices pratiques

#### 🎯 Exercice 1 : Navigation de base

1. Créez un dossier `data_training` dans votre home
2. Créez la structure : `data_training/{raw,processed,scripts}`
3. Naviguez dans le dossier `raw`
4. Créez 3 fichiers vides : `data1.csv`, `data2.csv`, `data3.csv`
5. Listez les fichiers avec leurs détails

💡 Voir la solution

```bash
# 1. Créer le dossier principal
cd ~
mkdir data_training

# 2. Créer la structure
mkdir -p data_training/{raw,processed,scripts}

# 3. Naviguer dans raw
cd data_training/raw

# 4. Créer les fichiers
touch data1.csv data2.csv data3.csv

# 5. Lister avec détails
ls -lh
```

#### 🎯 Exercice 2 : Copie et déplacement

1. Copiez tous les CSV de `raw/` vers `processed/`
2. Renommez les fichiers dans `processed/` en ajoutant le préfixe `clean_`
3. Trouvez la taille totale du dossier `data_training`
4. Listez tous les fichiers CSV dans toute l'arborescence

💡 Voir la solution

```bash
# 1. Copier vers processed
cd ~/data_training
cp raw/*.csv processed/

# 2. Renommer avec préfixe
cd processed
for file in *.csv; do
    mv "$file" "clean_$file"
done

# 3. Taille totale
cd ~/data_training
du -sh .

# 4. Lister tous les CSV
find . -name "*.csv"
```

#### 🎯 Exercice 3 : Permissions et recherche

1. Créez un script `process.sh` dans `scripts/`
2. Rendez-le exécutable
3. Trouvez tous les fichiers modifiés dans la dernière heure
4. Calculez l'espace utilisé par chaque sous-dossier

💡 Voir la solution

```bash
# 1. Créer le script
cd ~/data_training/scripts
touch process.sh

# 2. Rendre exécutable
chmod +x process.sh

# 3. Fichiers récents
cd ~/data_training
find . -type f -mmin -60

# 4. Espace par sous-dossier
du -h --max-depth=1 .
```

#### 💡 Points clés à retenir

- `cd`, `pwd`, `ls` : navigation de base
- `mkdir -p` : créer des arborescences complètes
- `cp -r`, `mv`, `rm -rf` : gestion de fichiers
- `find` : recherche puissante avec critères multiples
- `du -sh`, `df -h` : surveillance de l'espace disque
- `chmod`, `chown` : gestion des permissions
- Wildcards `*`, `?`, `[]`, `{}` : patterns de fichiers

#### ✅ Partie 2 terminée !

Vous maîtrisez maintenant la navigation et la gestion de fichiers. Ces commandes sont essentielles
pour organiser et manipuler vos données. Passez à la Partie 3 pour apprendre à manipuler le contenu des fichiers.

[Partie 3 : Manipulation de Texte et Données →](partie3.md)