## 🎯 Objectifs de cette Partie

- Manipuler HDFS avec des données réelles
- Créer des jobs MapReduce Python pas à pas
- Analyser des données avec Hive
- Résoudre des problèmes courants

## 📚 Exercice 1 : Manipulation HDFS (30 min)

### 🎯 Objectif

Maîtriser les commandes HDFS en créant une structure de données pour un projet d'analyse de logs.

### 📝 Contexte

Vous êtes Data Engineer et devez organiser les logs d'une application web.
Les logs sont répartis en plusieurs catégories : access, error, et performance.

### ✅ Étape 1 : Créer l'arborescence

```bash
# Se connecter à votre cluster Hadoop

# Créer l'arborescence de base
hdfs dfs -mkdir -p /user/$USER/logs/raw/access
hdfs dfs -mkdir -p /user/$USER/logs/raw/error
hdfs dfs -mkdir -p /user/$USER/logs/raw/performance
hdfs dfs -mkdir -p /user/$USER/logs/processed
hdfs dfs -mkdir -p /user/$USER/logs/archive

# Vérifier la structure
hdfs dfs -ls -R /user/$USER/logs
```

#### Résultat attendu

Vous devriez voir une arborescence avec 5 répertoires créés.

### ✅ Étape 2 : Générer des fichiers de logs de test

```bash
# Créer des logs d'accès (access logs)
cat > access.log << 'EOF'
192.168.1.10 - - [15/Jan/2025:10:23:45] "GET /home HTTP/1.1" 200 1234
192.168.1.11 - - [15/Jan/2025:10:24:12] "GET /products HTTP/1.1" 200 5678
192.168.1.10 - - [15/Jan/2025:10:25:33] "POST /api/login HTTP/1.1" 200 890
192.168.1.12 - - [15/Jan/2025:10:26:45] "GET /about HTTP/1.1" 200 432
192.168.1.11 - - [15/Jan/2025:10:27:22] "GET /contact HTTP/1.1" 200 234
EOF

# Créer des logs d'erreur (error logs)
cat > error.log << 'EOF'
[2025-01-15 10:30:15] ERROR Database connection failed: timeout
[2025-01-15 10:31:22] ERROR File not found: /data/config.xml
[2025-01-15 10:32:45] WARNING Slow query detected: SELECT * FROM users
[2025-01-15 10:33:10] ERROR Out of memory exception
[2025-01-15 10:34:55] ERROR API rate limit exceeded for user 12345
EOF

# Créer des logs de performance
cat > performance.log << 'EOF'
2025-01-15 10:00:00,homepage,250ms
2025-01-15 10:05:00,search,1200ms
2025-01-15 10:10:00,checkout,850ms
2025-01-15 10:15:00,homepage,180ms
2025-01-15 10:20:00,api_call,3500ms
EOF

# Afficher un aperçu
echo "=== Access Log ==="
head -3 access.log
echo -e "\n=== Error Log ==="
head -3 error.log
echo -e "\n=== Performance Log ==="
head -3 performance.log
```

### ✅ Étape 3 : Charger les logs dans HDFS

```bash
# Copier les fichiers dans HDFS
hdfs dfs -put access.log /user/$USER/logs/raw/access/
hdfs dfs -put error.log /user/$USER/logs/raw/error/
hdfs dfs -put performance.log /user/$USER/logs/raw/performance/

# Vérifier le chargement
hdfs dfs -ls /user/$USER/logs/raw/access/
hdfs dfs -ls /user/$USER/logs/raw/error/
hdfs dfs -ls /user/$USER/logs/raw/performance/

# Afficher le contenu d'un fichier
hdfs dfs -cat /user/$USER/logs/raw/access/access.log
```

### ✅ Étape 4 : Manipulations avancées

```bash
# Compter le nombre de lignes dans access.log
hdfs dfs -cat /user/$USER/logs/raw/access/access.log | wc -l

# Chercher les erreurs de type "ERROR"
hdfs dfs -cat /user/$USER/logs/raw/error/error.log | grep "ERROR"

# Voir la taille des fichiers
hdfs dfs -du -h /user/$USER/logs/raw/

# Copier un fichier dans HDFS
hdfs dfs -cp /user/$USER/logs/raw/access/access.log /user/$USER/logs/archive/access_backup.log

# Changer les permissions
hdfs dfs -chmod 755 /user/$USER/logs/raw/access/access.log

# Voir les statistiques d'un fichier
hdfs dfs -stat "Taille: %b bytes, Réplication: %r, Modifié: %y" /user/$USER/logs/raw/access/access.log
```

#### 📌 Points à retenir

- Les commandes HDFS sont similaires aux commandes Linux
- Toujours vérifier le résultat avec `-ls`
- Les pipes Unix fonctionnent avec `hdfs dfs -cat`

## 🐍 Exercice 2 : Job MapReduce - Analyse d'Access Logs (1h)

### 🎯 Objectif

Créer un job MapReduce Python pour compter le nombre de requêtes par adresse IP.

### ✅ Étape 1 : Créer le Mapper

```bash
#!/usr/bin/env python3
# Fichier: ip_count_mapper.py
"""
Mapper pour compter les requêtes par IP
Extrait l'IP de chaque ligne de log et émet (IP, 1)
"""
import sys
import re

def main():
# Pattern pour extraire l'IP (début de ligne)
    ip_pattern = re.compile(r'^(\d+\.\d+\.\d+\.\d+)')

    for line in sys.stdin:
        line = line.strip()

# Extraire l'IP
        match = ip_pattern.match(line)
        if match:
            ip = match.group(1)
# Émettre (IP, 1)
            print(f"{ip}\t1")

if __name__ == "__main__":
    main()
```

**💾 Créer le fichier :**

```bash
# Créer le mapper
cat > ip_count_mapper.py << 'EOF'
[Copier le code Python ci-dessus]
EOF

chmod +x ip_count_mapper.py
```

### ✅ Étape 2 : Créer le Reducer

```bash
#!/usr/bin/env python3
# Fichier: ip_count_reducer.py
"""
Reducer pour compter les requêtes par IP
Reçoit (IP, [1, 1, 1, ...]) et calcule le total
"""
import sys

def main():
    current_ip = None
    current_count = 0

    for line in sys.stdin:
        line = line.strip()

        try:
            ip, count = line.split('\t')
            count = int(count)
        except ValueError:
            continue

        if current_ip == ip:
            current_count += count
        else:
            if current_ip:
                print(f"{current_ip}\t{current_count}")
            current_ip = ip
            current_count = count

# Dernier IP
    if current_ip:
        print(f"{current_ip}\t{current_count}")

if __name__ == "__main__":
    main()
```

**💾 Créer le fichier :**

```bash
cat > ip_count_reducer.py << 'EOF'
[Copier le code Python ci-dessus]
EOF

chmod +x ip_count_reducer.py
```

### ✅ Étape 3 : Tester en Local

```bash
# Test du mapper seul
cat access.log | ./ip_count_mapper.py

# Résultat attendu :
# 192.168.1.10    1
# 192.168.1.11    1
# 192.168.1.10    1
# 192.168.1.12    1
# 192.168.1.11    1

# Test complet (mapper + sort + reducer)
cat access.log | ./ip_count_mapper.py | sort -k1,1 | ./ip_count_reducer.py

# Résultat attendu :
# 192.168.1.10    2
# 192.168.1.11    2
# 192.168.1.12    1
```

#### ✅ Validation

Si les tests locaux fonctionnent, vous êtes prêt pour Hadoop !

### ✅ Étape 4 : Exécuter sur Hadoop

```bash
# Lancer le job MapReduce
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
    -input /user/$USER/logs/raw/access/access.log \
    -output /user/$USER/logs/processed/ip_counts \
    -mapper ip_count_mapper.py \
    -reducer ip_count_reducer.py \
    -file ip_count_mapper.py \
    -file ip_count_reducer.py

# Voir les résultats
hdfs dfs -cat /user/$USER/logs/processed/ip_counts/part-00000

# Résultat attendu :
# 192.168.1.10    2
# 192.168.1.11    2
# 192.168.1.12    1
```

### ✅ Étape 5 : Analyser le Job

```bash
# Voir les logs du job
yarn logs -applicationId

# Ou via l'interface web YARN
# http://localhost:8088 (local)
# https://[cluster].azurehdinsight.net/yarnui (Azure)
```

## 📊 Exercice 3 : Analyse avec Hive (1h)

### 🎯 Objectif

Créer des tables Hive et effectuer des analyses SQL sur les logs.

### ✅ Étape 1 : Démarrer Hive

```bash
# Lancer Hive CLI
hive

# Ou Beeline (plus moderne)
beeline -u jdbc:hive2://localhost:10000
```

### ✅ Étape 2 : Créer une Table pour les Access Logs

```bash
-- Créer une table externe pour les access logs
CREATE EXTERNAL TABLE IF NOT EXISTS access_logs (
    ip STRING,
    identity STRING,
    user STRING,
    timestamp STRING,
    request STRING,
    status INT,
    size INT
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.RegexSerDe'
WITH SERDEPROPERTIES (
  "input.regex" = "^(\\S+) (\\S+) (\\S+) \\[([^\\]]+)\\] \"([^\"]+)\" (\\d+) (\\d+)"
)
STORED AS TEXTFILE
LOCATION '/user/$USER/logs/raw/access';

-- Vérifier que la table est créée
SHOW TABLES;

-- Voir la structure
DESCRIBE access_logs;
```

### ✅ Étape 3 : Requêtes d'Analyse

#### Requête 1 : Compter le nombre total de requêtes

```bash
SELECT COUNT(*) as total_requests
FROM access_logs;
```

#### Requête 2 : Top 3 des IPs les plus actives

```bash
SELECT ip, COUNT(*) as request_count
FROM access_logs
GROUP BY ip
ORDER BY request_count DESC
LIMIT 3;
```

#### Requête 3 : Requêtes réussies (status 200)

```bash
SELECT COUNT(*) as successful_requests
FROM access_logs
WHERE status = 200;
```

#### Requête 4 : Taille totale des données transférées par IP

```bash
SELECT ip, SUM(size) as total_bytes
FROM access_logs
GROUP BY ip
ORDER BY total_bytes DESC;
```

### ✅ Étape 4 : Créer une Table pour les Error Logs

```bash
-- Table pour les error logs
CREATE EXTERNAL TABLE IF NOT EXISTS error_logs (
    timestamp STRING,
    level STRING,
    message STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.RegexSerDe'
WITH SERDEPROPERTIES (
  "input.regex" = "\\[([^\\]]+)\\] (\\w+) (.+)"
)
STORED AS TEXTFILE
LOCATION '/user/$USER/logs/raw/error';

-- Compter les erreurs par niveau (ERROR, WARNING)
SELECT level, COUNT(*) as count
FROM error_logs
GROUP BY level;
```

### ✅ Étape 5 : Export des Résultats

```bash
-- Créer une table avec les résultats
CREATE TABLE ip_statistics AS
SELECT
    ip,
    COUNT(*) as request_count,
    SUM(size) as total_bytes,
    AVG(size) as avg_bytes
FROM access_logs
GROUP BY ip;

-- Exporter vers HDFS
INSERT OVERWRITE DIRECTORY '/user/$USER/logs/processed/ip_statistics'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
SELECT * FROM ip_statistics;
```

## 🔧 Exercice 4 : Job MapReduce Avancé - Top N (1h)

### 🎯 Objectif

Créer un job qui trouve les 3 pages les plus visitées dans les access logs.

### ✅ Étape 1 : Créer le Mapper

```bash
#!/usr/bin/env python3
# top_pages_mapper.py
import sys
import re

def extract_url(request):
    """Extrait l'URL de la requête HTTP"""
    match = re.search(r'GET (\S+)', request)
    if match:
        return match.group(1)
    return None

def main():
    for line in sys.stdin:
        parts = line.strip().split('"')
        if len(parts) >= 2:
            request = parts[1]
            url = extract_url(request)
            if url:
                print(f"{url}\t1")

if __name__ == "__main__":
    main()
```

### ✅ Étape 2 : Créer le Reducer avec Top N

```bash
#!/usr/bin/env python3
# top_pages_reducer.py
import sys
from heapq import nlargest

def main():
    url_counts = {}

# Agréger tous les comptages
    for line in sys.stdin:
        line = line.strip()
        try:
            url, count = line.split('\t')
            count = int(count)
            url_counts[url] = url_counts.get(url, 0) + count
        except ValueError:
            continue

# Trouver le top 3
    top_3 = nlargest(3, url_counts.items(), key=lambda x: x[1])

# Émettre le top 3
    for url, count in top_3:
        print(f"{url}\t{count}")

if __name__ == "__main__":
    main()
```

### ✅ Étape 3 : Test et Exécution

```bash
# Test local
cat access.log | ./top_pages_mapper.py | sort -k1,1 | ./top_pages_reducer.py

# Exécution Hadoop
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
    -input /user/$USER/logs/raw/access/access.log \
    -output /user/$USER/logs/processed/top_pages \
    -mapper top_pages_mapper.py \
    -reducer top_pages_reducer.py \
    -file top_pages_mapper.py \
    -file top_pages_reducer.py

# Résultats
hdfs dfs -cat /user/$USER/logs/processed/top_pages/part-00000
```

## 🐛 Exercice 5 : Dépannage (30 min)

### 🎯 Objectif

Apprendre à déboguer les problèmes courants de Hadoop.

### Problème 1 : Job MapReduce échoue

#### Erreur Simulée

`Error: java.lang.RuntimeException: PipeMapRed.waitOutputThreads()`

```bash
# Solutions :

# 1. Vérifier que les scripts sont exécutables
chmod +x mapper.py reducer.py

# 2. Vérifier le shebang
head -1 mapper.py
# Doit afficher : #!/usr/bin/env python3

# 3. Tester en local AVANT Hadoop
cat input.txt | ./mapper.py | sort | ./reducer.py

# 4. Voir les logs d'erreur
yarn logs -applicationId
```

### Problème 2 : Fichier HDFS introuvable

#### Erreur

`Input path does not exist: /user/data/file.txt`

```bash
# Solution :

# Vérifier le chemin exact
hdfs dfs -ls /user/
hdfs dfs -ls /user/$USER/

# Vérifier les permissions
hdfs dfs -ls -d /user/$USER/data

# Créer le répertoire si nécessaire
hdfs dfs -mkdir -p /user/$USER/data
```

### Problème 3 : Résultats vides ou incorrects

```bash
# Debugging :

# 1. Vérifier l'entrée
hdfs dfs -cat /input/file.txt | head -10

# 2. Tester le mapper seul
hdfs dfs -cat /input/file.txt | ./mapper.py

# 3. Ajouter des prints de debug dans le code Python
import sys
print(f"DEBUG: Processing line: {line}", file=sys.stderr)

# 4. Voir stderr dans les logs YARN
yarn logs -applicationId  2>&1 | grep DEBUG
```

## 📝 Résumé et Prochaines Étapes

### Compétences Acquises

- ✅ Manipulation HDFS : création, copie, permissions
- ✅ Jobs MapReduce Python avec Hadoop Streaming
- ✅ Test local avant exécution Hadoop
- ✅ Analyse de données avec Hive et HiveQL
- ✅ Debugging et résolution de problèmes
- ✅ Export de résultats depuis Hive

#### 🎓 Félicitations !

Vous avez terminé les exercices pratiques ! Vous êtes maintenant capable de :

- Gérer des données dans HDFS
- Créer des pipelines MapReduce
- Analyser des données avec Hive
- Résoudre les problèmes courants

**Prochaine étape :** Passez au Brief pratique complet pour un projet de bout en bout !