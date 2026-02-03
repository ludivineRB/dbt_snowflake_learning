## 3. Manipulation de Texte et Données

Cette partie couvre les outils essentiels pour traiter des données textuelles. Ces commandes sont au cœur du Data Engineering en shell.

### Afficher le contenu de fichiers

| Commande | Description | Usage |
| --- | --- | --- |
| `cat` | Afficher tout le contenu | Fichiers courts |
| `less` | Naviguer dans le fichier | Fichiers longs |
| `head` | Afficher le début (10 lignes par défaut) | Aperçu rapide |
| `tail` | Afficher la fin (10 lignes par défaut) | Logs récents |
| `wc` | Compter lignes, mots, caractères | Statistiques |

```bash
# cat : afficher tout le fichier
cat data.csv

# Numéroter les lignes
cat -n data.csv

# Concaténer plusieurs fichiers
cat file1.txt file2.txt > combined.txt

# head : afficher les premières lignes
head data.csv                    # 10 premières lignes
head -n 20 data.csv              # 20 premières lignes
head -5 data.csv                 # 5 premières lignes (raccourci)

# tail : afficher les dernières lignes
tail data.csv                    # 10 dernières lignes
tail -n 50 data.csv              # 50 dernières lignes
tail -f server.log               # Suivre en temps réel (logs)

# wc : compter
wc data.csv                      # lignes mots caractères
wc -l data.csv                   # nombre de lignes seulement
wc -w data.csv                   # nombre de mots
wc -c data.csv                   # nombre d'octets

# less : naviguer (plus puissant que more)
less data.csv
# Raccourcis dans less :
# - espace : page suivante
# - b : page précédente
# - / : rechercher
# - q : quitter
# - G : aller à la fin
# - g : aller au début
```

### Redirections et Pipelines

### 💡 Opérateurs de redirection

- `>` : Redirige la sortie vers un fichier (écrase)
- `>>` : Ajoute à la fin d'un fichier
- `<` : Lit depuis un fichier
- `|` : Pipe - envoie la sortie d'une commande vers une autre
- `2>` : Redirige les erreurs
- `&>` : Redirige sortie et erreurs

```bash
# > : redirection (écrase le fichier)
echo "Nouvelle ligne" > output.txt
ls -l > file_list.txt

# >> : ajout à la fin
echo "Ligne supplémentaire" >> output.txt
date >> log.txt

# < : lire depuis un fichier
wc -l < data.csv

# | : pipeline (chaîner des commandes)
cat data.csv | wc -l
ls -l | grep ".csv"
ps aux | grep python

# Combiner plusieurs pipes
cat data.csv | grep "ERROR" | wc -l

# 2> : rediriger les erreurs
ls fichier_inexistant 2> errors.log

# &> : rediriger sortie ET erreurs
command &> all_output.log

# Séparer sortie et erreurs
command > output.log 2> error.log

# Ignorer les erreurs
command 2> /dev/null

# Exemple pratique : analyser des logs
cat server.log | grep "ERROR" | tail -100 > recent_errors.txt
```

### grep - Rechercher dans des fichiers

`grep` est l'outil le plus utilisé pour rechercher des patterns dans des fichiers. Essentiel en Data Engineering.

| Option | Description | Exemple |
| --- | --- | --- |
| `grep pattern file` | Recherche basique | `grep "ERROR" log.txt` |
| `-i` | Ignorer la casse | `grep -i "error" log.txt` |
| `-v` | Inverser (lignes ne contenant PAS) | `grep -v "DEBUG" log.txt` |
| `-c` | Compter les correspondances | `grep -c "ERROR" log.txt` |
| `-n` | Afficher les numéros de ligne | `grep -n "ERROR" log.txt` |
| `-r` | Récursif dans les dossiers | `grep -r "TODO" .` |
| `-l` | Afficher uniquement les noms de fichiers | `grep -l "ERROR" *.log` |
| `-A n` | Afficher n lignes après | `grep -A 3 "ERROR" log.txt` |
| `-B n` | Afficher n lignes avant | `grep -B 2 "ERROR" log.txt` |
| `-C n` | Afficher n lignes avant et après | `grep -C 5 "ERROR" log.txt` |

```bash
# Recherche simple
grep "ERROR" server.log

# Ignorer la casse
grep -i "error" server.log

# Compter les occurrences
grep -c "ERROR" server.log

# Avec numéros de ligne
grep -n "ERROR" server.log

# Inverser (tout sauf ERROR)
grep -v "ERROR" server.log

# Recherche récursive dans tous les fichiers
grep -r "database_connection" .

# Afficher uniquement les noms de fichiers
grep -l "ERROR" *.log

# Contexte : 3 lignes avant et après
grep -C 3 "CRITICAL" server.log

# Expressions régulières
grep "ERROR.*database" server.log          # ERROR suivi de database
grep "^ERROR" server.log                   # Lignes commençant par ERROR
grep "ERROR$" server.log                   # Lignes finissant par ERROR
grep "[0-9]{3}" server.log                 # 3 chiffres consécutifs
grep -E "ERROR|CRITICAL|FATAL" server.log  # Plusieurs patterns

# Exemples pratiques en Data Engineering

# Trouver les erreurs SQL dans les logs
grep -i "sql.*error" application.log

# Compter les requêtes par code HTTP
grep -o "HTTP/[0-9]\.[0-9]\" [0-9]*" access.log | cut -d' ' -f2 | sort | uniq -c

# Extraire les emails d'un fichier
grep -Eo "\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b" data.txt

# Trouver les lignes avec des montants en dollars
grep -E '\$[0-9,]+\.[0-9]{2}' transactions.txt

# Filtrer les logs d'une date spécifique
grep "2024-01-15" server.log

# Exclure les lignes de debug et info
grep -v -E "DEBUG|INFO" server.log

# Rechercher dans des CSV
grep "John Doe" customers.csv
```

### sed - Transformation de texte

`sed` (Stream EDitor) permet de transformer du texte à la volée. Très puissant pour le nettoyage de données.

```bash
# Substitution basique : s/ancien/nouveau/
echo "Hello World" | sed 's/World/Universe/'
# Output: Hello Universe

# Remplacer dans un fichier (sans modifier l'original)
sed 's/old/new/' data.txt

# Modifier le fichier directement (-i)
sed -i 's/old/new/' data.txt           # Linux
sed -i '' 's/old/new/' data.txt        # macOS

# Remplacer toutes les occurrences sur chaque ligne (g = global)
sed 's/ERROR/WARNING/g' log.txt

# Remplacer uniquement la 2ème occurrence
sed 's/ERROR/WARNING/2' log.txt

# Supprimer des lignes
sed '/pattern/d' file.txt              # Supprimer les lignes contenant pattern
sed '1d' file.txt                      # Supprimer la première ligne
sed '1,3d' file.txt                    # Supprimer les lignes 1 à 3
sed '$d' file.txt                      # Supprimer la dernière ligne

# Afficher certaines lignes
sed -n '1,10p' file.txt                # Afficher lignes 1 à 10
sed -n '/pattern/p' file.txt           # Afficher lignes contenant pattern

# Exemples pratiques en Data Engineering

# Remplacer les séparateurs CSV
sed 's/;/,/g' data_semicolon.csv > data_comma.csv

# Nettoyer les espaces en double
sed 's/  */ /g' data.txt

# Supprimer les lignes vides
sed '/^$/d' data.txt

# Supprimer les espaces en début et fin de ligne
sed 's/^[[:space:]]*//; s/[[:space:]]*$//' data.txt

# Ajouter un préfixe à chaque ligne
sed 's/^/PREFIX_/' data.txt

# Remplacer NULL par une valeur par défaut
sed 's/NULL/0/g' data.csv

# Extraire une colonne d'un CSV (colonne 2)
sed 's/^[^,]*,\([^,]*\).*/\1/' data.csv

# Remplacer plusieurs patterns en une commande
sed -e 's/ERROR/ERR/g' -e 's/WARNING/WARN/g' log.txt

# Supprimer les commentaires (lignes commençant par #)
sed '/^#/d' config.txt

# Conversion : minuscules en majuscules (GNU sed)
sed 's/.*/\U&/' data.txt

# Nettoyer un CSV : supprimer header et footer
sed '1d; $d' data.csv
```

### awk - Traitement de données structurées

`awk` est un langage de programmation complet spécialisé dans le traitement de données textuelles structurées. Extrêmement puissant pour les CSV/TSV.

#### Structure d'une commande awk

```bash
awk 'pattern { action }' file

pattern : condition optionnelle
action  : traitement à effectuer
NR      : numéro de ligne
NF      : nombre de colonnes
$1, $2  : colonnes 1, 2, etc.
$0      : ligne complète
```

```bash
# Afficher une colonne spécifique
awk '{print $1}' data.txt              # Première colonne
awk '{print $2}' data.txt              # Deuxième colonne
awk '{print $1, $3}' data.txt          # Colonnes 1 et 3

# Définir le séparateur de champs (-F)
awk -F',' '{print $1}' data.csv        # CSV
awk -F'\t' '{print $1}' data.tsv       # TSV

# Afficher avec formatage
awk '{print $1 " - " $2}' data.txt

# Numéros de ligne (NR)
awk '{print NR, $0}' data.txt          # Numéroter les lignes
awk 'NR==5' data.txt                   # Afficher ligne 5
awk 'NR>=10 && NR<=20' data.txt        # Lignes 10 à 20

# Nombre de colonnes (NF)
awk '{print NF}' data.csv              # Nombre de colonnes par ligne
awk '{print $NF}' data.csv             # Dernière colonne

# Conditions
awk '$3 > 100' data.txt                # Lignes où colonne 3 > 100
awk '$1 == "ERROR"' log.txt            # Lignes où colonne 1 = ERROR
awk '$2 != "NULL"' data.csv            # Colonne 2 différente de NULL

# Expressions régulières
awk '/ERROR/' log.txt                  # Lignes contenant ERROR
awk '$2 ~ /^[0-9]+$/' data.txt         # Colonne 2 = nombre

# Opérations mathématiques
awk '{sum += $3} END {print sum}' data.csv           # Somme de la colonne 3
awk '{sum += $3} END {print sum/NR}' data.csv        # Moyenne
awk '{if($3>max) max=$3} END {print max}' data.csv   # Maximum

# BEGIN et END
awk 'BEGIN {print "Start"} {print $0} END {print "End"}' data.txt

# Exemples pratiques en Data Engineering

# Fichier CSV : id,name,age,salary
# 1,Alice,30,50000
# 2,Bob,25,45000
# 3,Charlie,35,60000

# Extraire les noms (colonne 2)
awk -F',' '{print $2}' employees.csv

# Filtrer les salaires > 50000
awk -F',' '$4 > 50000' employees.csv

# Calculer le salaire total
awk -F',' '{sum += $4} END {print "Total:", sum}' employees.csv

# Calculer le salaire moyen
awk -F',' 'NR>1 {sum += $4; count++} END {print "Average:", sum/count}' employees.csv

# Ajouter une colonne calculée
awk -F',' '{print $0 "," $4*0.2}' employees.csv    # Ajouter bonus 20%

# Compter les occurrences par catégorie
awk -F',' '{count[$2]++} END {for(c in count) print c, count[c]}' data.csv

# Filtrer et transformer
awk -F',' '$3 >= 30 {print $2, $4}' employees.csv

# Supprimer le header
awk -F',' 'NR>1 {print $0}' data.csv

# Reformater un CSV en JSON (simple)
awk -F',' '{print "{\"id\":" $1 ",\"name\":\"" $2 "\"}"}' data.csv

# Analyser des logs Apache/Nginx
awk '{print $1}' access.log | sort | uniq -c | sort -rn    # IPs les plus fréquentes

# Calculer des statistiques
awk '{sum+=$1; sumsq+=$1*$1} END {print "Mean:", sum/NR, "StdDev:", sqrt(sumsq/NR - (sum/NR)^2)}' numbers.txt

# Pivoter des données
awk -F',' '{a[$1]+=$2} END {for(i in a) print i, a[i]}' data.csv
```

### Combinaisons puissantes : grep + sed + awk

```bash
# Pipeline complet : extraire, filtrer, transformer, agréger

# Exemple 1 : Analyser des logs d'erreurs
cat server.log | \
    grep "ERROR" | \                          # Filtrer les erreurs
    awk '{print $5}' | \                      # Extraire le type d'erreur
    sort | \                                  # Trier
    uniq -c | \                               # Compter les doublons
    sort -rn | \                              # Trier par fréquence
    head -10                                  # Top 10

# Exemple 2 : Nettoyer un CSV et calculer des stats
cat sales.csv | \
    sed '1d' | \                              # Supprimer le header
    sed 's/NULL/0/g' | \                      # Remplacer NULL par 0
    awk -F',' '{sum += $3} END {print sum}'   # Somme de la colonne 3

# Exemple 3 : Extraire des emails et compter par domaine
grep -Eo "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}" contacts.txt | \
    awk -F'@' '{print $2}' | \
    sort | \
    uniq -c | \
    sort -rn

# Exemple 4 : Analyser un fichier de transactions
cat transactions.csv | \
    awk -F',' 'NR>1 {print $2, $4}' | \       # Date et montant
    grep "2024-01" | \                        # Janvier 2024
    awk '{sum += $2} END {print "Total:", sum}'

# Exemple 5 : Nettoyer et formatter des données
cat raw_data.txt | \
    sed 's/^[[:space:]]*//; s/[[:space:]]*$//' | \  # Trim
    sed '/^$/d' | \                                  # Supprimer lignes vides
    awk '{print toupper($0)}' | \                    # Majuscules
    sort -u                                          # Trier et dédupliquer

# Exemple 6 : Analyser des accès API
cat api_access.log | \
    grep "POST" | \
    awk '{print $7}' | \                      # Endpoint
    sed 's/?.*$//' | \                        # Retirer les query params
    sort | \
    uniq -c | \
    sort -rn | \
    head -20

# Exemple 7 : Extraire et reformater des données
cat data.json | \
    grep "user_id" | \
    sed 's/.*"user_id": "\([^"]*\)".*/\1/' | \
    sort | \
    uniq > user_ids.txt

# Exemple 8 : Comparer deux fichiers CSV
diff <(sort file1.csv) <(sort file2.csv)

# Exemple 9 : Générer un rapport de logs
cat application.log | \
    awk '{print $1, $4}' | \                  # Date et niveau
    sed 's/\[//; s/\]//' | \                  # Nettoyer les brackets
    awk '{count[$2]++} END {for (level in count) print level, count[level]}'
```

### Utilitaires complémentaires

| Commande | Description | Exemple |
| --- | --- | --- |
| `sort` | Trier des lignes | `sort data.txt` |
| `uniq` | Supprimer les doublons consécutifs | `sort data.txt | uniq` |
| `cut` | Extraire des colonnes | `cut -d',' -f1,3 data.csv` |
| `paste` | Fusionner des fichiers colonne par colonne | `paste file1.txt file2.txt` |
| `tr` | Traduire/supprimer des caractères | `tr '[:lower:]' '[:upper:]'` |
| `column` | Formatter en colonnes | `column -t -s',' data.csv` |

```bash
# sort : trier
sort data.txt                     # Tri alphabétique
sort -n data.txt                  # Tri numérique
sort -r data.txt                  # Tri inverse
sort -k2 data.txt                 # Trier par colonne 2
sort -t',' -k3n data.csv          # CSV : trier par colonne 3 numériquement

# uniq : dédupliquer (nécessite un tri préalable)
sort data.txt | uniq              # Supprimer les doublons
sort data.txt | uniq -c           # Compter les occurrences
sort data.txt | uniq -d           # Afficher uniquement les doublons
sort data.txt | uniq -u           # Afficher uniquement les uniques

# cut : extraire des colonnes
cut -d',' -f1 data.csv            # Colonne 1 d'un CSV
cut -d',' -f1,3,5 data.csv        # Colonnes 1, 3 et 5
cut -d',' -f2- data.csv           # À partir de la colonne 2
cut -c1-10 data.txt               # Caractères 1 à 10

# paste : fusionner horizontalement
paste file1.txt file2.txt         # Fusionner deux fichiers
paste -d',' file1.txt file2.txt   # Avec virgule comme séparateur

# tr : transformer des caractères
echo "hello" | tr '[:lower:]' '[:upper:]'     # HELLO
echo "hello world" | tr ' ' '_'               # hello_world
echo "hello123" | tr -d '[:digit:]'           # hello
echo "hello\n\nworld" | tr -s '\n'            # Supprimer lignes vides

# column : formatter joliment
cat data.csv | column -t -s','    # Aligner un CSV en colonnes

# Exemples pratiques

# Compter les valeurs uniques d'une colonne
cut -d',' -f2 data.csv | sort | uniq | wc -l

# Top 10 des valeurs les plus fréquentes
cut -d',' -f3 data.csv | sort | uniq -c | sort -rn | head -10

# Fusionner deux CSV par ligne
paste -d',' file1.csv file2.csv > merged.csv

# Convertir CSV en TSV
cat data.csv | tr ',' '\t' > data.tsv

# Nettoyer les espaces
cat data.txt | tr -s ' ' > cleaned.txt
```

### Cas pratique complet : Analyse de logs

```bash
# Fichier de log : server.log
# Format : [2024-01-15 10:30:25] ERROR database Connection timeout user_id=123
# Format : [2024-01-15 10:31:12] INFO  api     Request received user_id=456

# 1. Compter les erreurs par type
cat server.log | \
    grep "ERROR" | \
    awk '{print $4}' | \
    sort | \
    uniq -c | \
    sort -rn
# Output:
# 145 database
#  89 network
#  34 authentication

# 2. Extraire les user_ids des erreurs
cat server.log | \
    grep "ERROR" | \
    grep -o "user_id=[0-9]*" | \
    cut -d'=' -f2 | \
    sort | \
    uniq > error_users.txt

# 3. Créer un rapport par heure
cat server.log | \
    awk '{print $2}' | \
    cut -d':' -f1 | \
    sort | \
    uniq -c
# Output:
# 234 10
# 456 11
# 389 12

# 4. Filtrer les erreurs d'une date spécifique et les exporter
cat server.log | \
    grep "2024-01-15" | \
    grep "ERROR" | \
    awk '{print $2, $3, $4, $5}' > errors_2024-01-15.txt

# 5. Analyser les erreurs par service et sévérité
cat server.log | \
    awk '{print $3, $4}' | \
    sort | \
    uniq -c | \
    sort -rn | \
    column -t
```

### Exercices pratiques

#### 🎯 Exercice 1 : Manipulation de fichiers CSV

Créez un fichier `employees.csv` avec ce contenu :

```bash
id,name,department,salary
1,Alice,Engineering,75000
2,Bob,Marketing,65000
3,Charlie,Engineering,80000
4,Diana,Sales,70000
5,Eve,Engineering,72000
```

1. Affichez uniquement les noms (colonne 2)
2. Filtrez les employés de Engineering
3. Calculez le salaire total
4. Calculez le salaire moyen du département Engineering

💡 Voir la solution

```bash
# 1. Noms uniquement
awk -F',' 'NR>1 {print $2}' employees.csv

# 2. Engineering seulement
grep "Engineering" employees.csv

# 3. Salaire total
awk -F',' 'NR>1 {sum += $4} END {print sum}' employees.csv

# 4. Salaire moyen Engineering
awk -F',' 'NR>1 && $3=="Engineering" {sum+=$4; count++} END {print sum/count}' employees.csv
```

#### 🎯 Exercice 2 : Analyse de logs

Créez un fichier `app.log` :

```bash
2024-01-15 10:00:00 INFO User login user_id=100
2024-01-15 10:05:00 ERROR Database timeout user_id=101
2024-01-15 10:10:00 INFO User logout user_id=100
2024-01-15 10:15:00 ERROR Network failure user_id=102
2024-01-15 10:20:00 ERROR Database timeout user_id=103
```

1. Comptez le nombre total d'erreurs
2. Listez les types d'erreurs uniques
3. Extrayez tous les user\_ids ayant eu une erreur
4. Comptez les erreurs par type

💡 Voir la solution

```bash
# 1. Compter les erreurs
grep -c "ERROR" app.log

# 2. Types d'erreurs uniques
grep "ERROR" app.log | awk '{print $4, $5}' | sort -u

# 3. User IDs avec erreurs
grep "ERROR" app.log | grep -o "user_id=[0-9]*" | cut -d'=' -f2 | sort -u

# 4. Erreurs par type
grep "ERROR" app.log | awk '{print $4}' | sort | uniq -c
```

#### 🎯 Exercice 3 : Pipeline complet

Créez un fichier `sales.csv` :

```bash
date,product,quantity,price
2024-01-01,Laptop,2,1000
2024-01-01,Mouse,5,25
2024-01-02,Laptop,1,1000
2024-01-02,Keyboard,3,75
2024-01-03,Mouse,10,25
```

Créez un pipeline qui :

1. Supprime le header
2. Calcule le montant total (quantity \* price) pour chaque ligne
3. Fait la somme totale de toutes les ventes

💡 Voir la solution

```bash
# Solution complète
cat sales.csv | \
    sed '1d' | \
    awk -F',' '{total = $3 * $4; sum += total} END {print "Total:", sum}'

# OU avec affichage détaillé
cat sales.csv | \
    sed '1d' | \
    awk -F',' '{total = $3 * $4; print $1, $2, total; sum += total} END {print "Grand Total:", sum}'
```

#### 💡 Points clés à retenir

- `cat`, `head`, `tail`, `less` : visualiser les fichiers
- `grep` : rechercher des patterns (-i, -v, -c, -r, -A, -B, -C)
- `sed` : transformer du texte (s/old/new/g, /pattern/d)
- `awk` : traiter des données structurées (colonnes, agrégations)
- Pipelines `|` : chaîner les commandes
- Redirections `>`, `>>` : sauvegarder les résultats
- `sort | uniq -c | sort -rn` : pattern classique d'agrégation

#### ✅ Partie 3 terminée !

Vous maîtrisez maintenant les outils essentiels de manipulation de texte et de données. Ces commandes
sont le cœur du Data Engineering en shell. Passez à la Partie 4 pour apprendre à créer des scripts automatisés.

[Partie 4 : Scripts Shell et Automatisation →](partie4.md)