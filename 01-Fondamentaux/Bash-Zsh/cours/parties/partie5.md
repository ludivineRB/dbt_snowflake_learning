## 5. Structures de Contrôle et Boucles

Les structures de contrôle permettent de créer des scripts intelligents qui prennent des décisions et répètent des opérations. Essentielles pour l'automatisation.

### Conditions : if / elif / else

```bash
#!/bin/bash

# Syntaxe de base
if [ condition ]; then
# commandes si vrai
fi

# Avec else
if [ condition ]; then
# commandes si vrai
else
# commandes si faux
fi

# Avec elif (else if)
if [ condition1 ]; then
# commandes si condition1 vraie
elif [ condition2 ]; then
# commandes si condition2 vraie
else
# commandes si toutes fausses
fi

# Exemples pratiques
age=25

if [ $age -ge 18 ]; then
    echo "Majeur"
else
    echo "Mineur"
fi

# Multiple conditions
if [ $age -ge 18 ] && [ $age -le 65 ]; then
    echo "Âge actif"
elif [ $age -gt 65 ]; then
    echo "Senior"
else
    echo "Jeune"
fi

# Vérifier l'existence d'un fichier
filename="data.csv"

if [ -f "$filename" ]; then
    echo "Le fichier existe"
    lines=$(wc -l < "$filename")
    echo "Nombre de lignes: $lines"
else
    echo "Le fichier n'existe pas"
    exit 1
fi

# Forme compacte (une ligne)
[ -f "$filename" ] && echo "File exists" || echo "File not found"
```

### Tests : [ ], [[ ]], et test

#### Différences entre [ ] et [[ ]]

`[ ]` : Syntaxe POSIX classique (compatible partout)
`[[ ]]` : Syntaxe Bash/Zsh moderne (plus puissante, recommandée)
`test` : Équivalent de [ ]

```bash
# [ ] : Syntaxe classique
if [ "$var" = "value" ]; then
    echo "Equal"
fi

# [[ ]] : Syntaxe moderne (recommandée)
if [[ "$var" == "value" ]]; then
    echo "Equal"
fi

# Avantages de [[ ]]
# - Pas besoin de quoter les variables
# - Support des regex
# - Opérateurs && et || directement
# - Pattern matching

# Exemples avec [[ ]]
name="Alice"

if [[ $name == "Alice" ]]; then
    echo "Hello Alice"
fi

# Pattern matching
if [[ $name == A* ]]; then
    echo "Name starts with A"
fi

# Regex
if [[ $name =~ ^[A-Z][a-z]+$ ]]; then
    echo "Valid name format"
fi

# Opérateurs logiques
if [[ $age -gt 18 && $age -lt 65 ]]; then
    echo "Working age"
fi

# Avec [ ] il faut utiliser -a et -o ou séparer
if [ $age -gt 18 ] && [ $age -lt 65 ]; then
    echo "Working age"
fi
```

### Opérateurs de comparaison

#### Comparaisons numériques

| Opérateur | Description | Exemple |
| --- | --- | --- |
| `-eq` | Égal (equal) | `[ $a -eq $b ]` |
| `-ne` | Différent (not equal) | `[ $a -ne $b ]` |
| `-gt` | Plus grand (greater than) | `[ $a -gt $b ]` |
| `-ge` | Plus grand ou égal (greater or equal) | `[ $a -ge $b ]` |
| `-lt` | Plus petit (less than) | `[ $a -lt $b ]` |
| `-le` | Plus petit ou égal (less or equal) | `[ $a -le $b ]` |

#### Comparaisons de chaînes

| Opérateur | Description | Exemple |
| --- | --- | --- |
| `=` ou `==` | Égal | `[ "$a" = "$b" ]` |
| `!=` | Différent | `[ "$a" != "$b" ]` |
| `-z` | Chaîne vide (zero length) | `[ -z "$var" ]` |
| `-n` | Chaîne non vide | `[ -n "$var" ]` |
| `<` | Avant dans l'ordre alphabétique | `[[ "$a" < "$b" ]]` |
| `>` | Après dans l'ordre alphabétique | `[[ "$a" > "$b" ]]` |

#### Tests de fichiers

| Opérateur | Description | Exemple |
| --- | --- | --- |
| `-f` | Fichier existe et est régulier | `[ -f file.txt ]` |
| `-d` | Répertoire existe | `[ -d /path ]` |
| `-e` | Fichier ou répertoire existe | `[ -e path ]` |
| `-s` | Fichier existe et non vide | `[ -s file.txt ]` |
| `-r` | Fichier lisible | `[ -r file.txt ]` |
| `-w` | Fichier modifiable | `[ -w file.txt ]` |
| `-x` | Fichier exécutable | `[ -x script.sh ]` |
| `-L` | Lien symbolique | `[ -L link ]` |

```bash
#!/bin/bash

# Comparaisons numériques
count=10

if [ $count -eq 10 ]; then
    echo "Count is 10"
fi

if [ $count -gt 5 ]; then
    echo "Count is greater than 5"
fi

# Comparaisons de chaînes
name="Alice"

if [ "$name" = "Alice" ]; then
    echo "Hello Alice"
fi

if [ -z "$name" ]; then
    echo "Name is empty"
fi

if [ -n "$name" ]; then
    echo "Name is not empty"
fi

# Tests de fichiers
file="data.csv"

if [ -f "$file" ]; then
    echo "File exists"

    if [ -s "$file" ]; then
        echo "File is not empty"
    fi

    if [ -r "$file" ]; then
        echo "File is readable"
    fi
fi

if [ -d "/tmp" ]; then
    echo "/tmp directory exists"
fi

# Tests combinés
if [ -f "$file" ] && [ -s "$file" ]; then
    echo "File exists and is not empty"
fi

# Avec [[]]
if [[ -f "$file" && -s "$file" ]]; then
    echo "File exists and is not empty"
fi

# Pattern matching
filename="data.csv"

if [[ $filename == *.csv ]]; then
    echo "This is a CSV file"
fi

if [[ $filename =~ ^data_[0-9]+\.csv$ ]]; then
    echo "Matches pattern: data_NUMBER.csv"
fi

# Exemple pratique : validation d'entrées
validate_input() {
    local input=$1

# Vérifier que l'input n'est pas vide
    if [ -z "$input" ]; then
        echo "Error: Input is empty"
        return 1
    fi

# Vérifier que c'est un nombre
    if ! [[ $input =~ ^[0-9]+$ ]]; then
        echo "Error: Input is not a number"
        return 1
    fi

# Vérifier la plage
    if [ $input -lt 1 ] || [ $input -gt 100 ]; then
        echo "Error: Input must be between 1 and 100"
        return 1
    fi

    echo "Input is valid"
    return 0
}
```

### Boucle for

```bash
#!/bin/bash

# Boucle sur une liste
for item in item1 item2 item3; do
    echo "Item: $item"
done

# Boucle sur des fichiers
for file in *.csv; do
    echo "Processing $file"
    wc -l "$file"
done

# Boucle sur une séquence de nombres
for i in {1..5}; do
    echo "Number: $i"
done

# Boucle avec seq
for i in $(seq 1 10); do
    echo "Iteration $i"
done

# Style C (arithmétique)
for ((i=1; i<=10; i++)); do
    echo "Count: $i"
done

# Boucle sur les arguments du script
for arg in "$@"; do
    echo "Argument: $arg"
done

# Boucle sur les lignes d'un fichier
for line in $(cat file.txt); do
    echo "Line: $line"
done

# Meilleure méthode pour lire un fichier (préserve les espaces)
while IFS= read -r line; do
    echo "Line: $line"
done < file.txt

# Exemples pratiques en Data Engineering

# 1. Traiter tous les CSV d'un dossier
for csv_file in data/raw/*.csv; do
    echo "Processing $csv_file..."
# Compter les lignes
    lines=$(wc -l < "$csv_file")
    echo "  Lines: $lines"

# Extraire le nom sans extension
    basename=$(basename "$csv_file" .csv)
    echo "  Basename: $basename"

# Copier vers processed
    cp "$csv_file" "data/processed/${basename}_processed.csv"
done

# 2. Créer des dossiers pour chaque mois
for month in {01..12}; do
    mkdir -p "data/2024/$month"
    echo "Created data/2024/$month"
done

# 3. Télécharger plusieurs fichiers
urls=(
    "https://example.com/data1.csv"
    "https://example.com/data2.csv"
    "https://example.com/data3.csv"
)

for url in "${urls[@]}"; do
    filename=$(basename "$url")
    echo "Downloading $filename..."
    curl -O "$url"
done

# 4. Traiter des fichiers avec pattern
for year in 2020 2021 2022 2023; do
    for month in {01..12}; do
        file="sales_${year}_${month}.csv"
        if [ -f "$file" ]; then
            echo "Processing $file"
# Votre traitement ici
        fi
    done
done

# 5. Renommer des fichiers en masse
for file in *.txt; do
    newname="${file%.txt}_backup.txt"
    mv "$file" "$newname"
    echo "Renamed $file to $newname"
done

# 6. Exécuter une commande sur plusieurs serveurs
servers=(server1 server2 server3)

for server in "${servers[@]}"; do
    echo "Connecting to $server..."
    ssh "$server" "df -h"
done
```

### Boucle while

```bash
#!/bin/bash

# While basique
counter=1
while [ $counter -le 5 ]; do
    echo "Counter: $counter"
    ((counter++))
done

# While avec lecture de fichier (méthode recommandée)
while IFS= read -r line; do
    echo "Line: $line"
done < data.txt

# While avec CSV (séparateur personnalisé)
while IFS=',' read -r col1 col2 col3; do
    echo "Col1: $col1, Col2: $col2, Col3: $col3"
done < data.csv

# While infini (avec break)
while true; do
    read -p "Enter command (or 'quit'): " cmd

    if [ "$cmd" = "quit" ]; then
        break
    fi

    echo "You entered: $cmd"
done

# While avec condition de fichier
while [ ! -f "signal.txt" ]; do
    echo "Waiting for signal file..."
    sleep 5
done
echo "Signal file found!"

# Exemples pratiques

# 1. Lire un CSV ligne par ligne
while IFS=',' read -r id name age salary; do
# Ignorer le header
    if [ "$id" = "id" ]; then
        continue
    fi

# Traiter chaque ligne
    echo "Processing employee: $name"

# Filtrer par condition
    if [ $salary -gt 50000 ]; then
        echo "$name has high salary: $salary"
    fi
done < employees.csv

# 2. Attendre qu'un processus se termine
while pgrep -x "process_name" > /dev/null; do
    echo "Process still running..."
    sleep 10
done
echo "Process finished"

# 3. Monitorer l'espace disque
while true; do
    usage=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')

    if [ $usage -gt 80 ]; then
        echo "WARNING: Disk usage is ${usage}%"
# Envoyer une alerte
    fi

    sleep 3600  # Vérifier chaque heure
done

# 4. Traiter des fichiers jusqu'à ce qu'il n'y en ait plus
while [ -n "$(ls queue/*.csv 2>/dev/null)" ]; do
    for file in queue/*.csv; do
        echo "Processing $file"
# Traiter le fichier
        process_file "$file"
# Déplacer vers processed
        mv "$file" processed/
    done
    sleep 60  # Attendre 1 minute
done

# 5. Lire des logs en temps réel et filtrer
tail -f application.log | while read -r line; do
    if [[ $line =~ ERROR ]]; then
        echo "ERROR DETECTED: $line"
# Envoyer une notification
    fi
done
```

### Boucle until

```bash
#!/bin/bash

# Until : boucle jusqu'à ce que la condition soit vraie
# (opposé de while)

counter=1
until [ $counter -gt 5 ]; do
    echo "Counter: $counter"
    ((counter++))
done

# Attendre qu'un fichier existe
until [ -f "data.csv" ]; do
    echo "Waiting for data.csv..."
    sleep 5
done
echo "File found!"

# Attendre qu'un service soit prêt
until curl -s http://localhost:8080/health > /dev/null; do
    echo "Waiting for service to be ready..."
    sleep 2
done
echo "Service is ready!"

# Exemple pratique : retry mechanism
max_retries=5
retry_count=0

until process_data || [ $retry_count -eq $max_retries ]; do
    ((retry_count++))
    echo "Attempt $retry_count failed. Retrying..."
    sleep 5
done

if [ $retry_count -eq $max_retries ]; then
    echo "Failed after $max_retries attempts"
    exit 1
fi
```

### Case statements (switch)

```bash
#!/bin/bash

# Syntaxe case
case $variable in
    pattern1)
# commandes
        ;;
    pattern2)
# commandes
        ;;
    *)
# défaut
        ;;
esac

# Exemple simple
read -p "Enter a choice (a/b/c): " choice

case $choice in
    a)
        echo "You chose A"
        ;;
    b)
        echo "You chose B"
        ;;
    c)
        echo "You chose C"
        ;;
    *)
        echo "Invalid choice"
        ;;
esac

# Patterns multiples
read -p "Enter yes or no: " answer

case $answer in
    yes|y|Y|YES)
        echo "You said yes"
        ;;
    no|n|N|NO)
        echo "You said no"
        ;;
    *)
        echo "Please answer yes or no"
        ;;
esac

# Pattern matching
filename="data.csv"

case $filename in
    *.csv)
        echo "CSV file"
        ;;
    *.json)
        echo "JSON file"
        ;;
    *.xml)
        echo "XML file"
        ;;
    *)
        echo "Unknown file type"
        ;;
esac

# Exemple pratique : menu de script
show_menu() {
    echo "========== Data Pipeline Menu =========="
    echo "1. Extract data"
    echo "2. Transform data"
    echo "3. Load data"
    echo "4. Run full pipeline"
    echo "5. Generate report"
    echo "q. Quit"
    echo "========================================"
}

while true; do
    show_menu
    read -p "Enter your choice: " choice

    case $choice in
        1)
            echo "Extracting data..."
            extract_data
            ;;
        2)
            echo "Transforming data..."
            transform_data
            ;;
        3)
            echo "Loading data..."
            load_data
            ;;
        4)
            echo "Running full pipeline..."
            extract_data
            transform_data
            load_data
            ;;
        5)
            echo "Generating report..."
            generate_report
            ;;
        q|Q)
            echo "Goodbye!"
            exit 0
            ;;
        *)
            echo "Invalid choice. Please try again."
            ;;
    esac

    echo ""
done

# Parser des options avec case
while [ $# -gt 0 ]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -v|--verbose)
            VERBOSE=1
            shift
            ;;
        -o|--output)
            OUTPUT_FILE=$2
            shift 2
            ;;
        -f|--format)
            case $2 in
                csv|json|xml)
                    FORMAT=$2
                    shift 2
                    ;;
                *)
                    echo "Invalid format: $2"
                    exit 1
                    ;;
            esac
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done
```

### Break et Continue

```bash
#!/bin/bash

# break : sortir de la boucle
for i in {1..10}; do
    if [ $i -eq 5 ]; then
        echo "Breaking at $i"
        break
    fi
    echo "Number: $i"
done
# Output: 1, 2, 3, 4, Breaking at 5

# continue : passer à l'itération suivante
for i in {1..10}; do
    if [ $i -eq 5 ]; then
        echo "Skipping $i"
        continue
    fi
    echo "Number: $i"
done
# Output: 1, 2, 3, 4, Skipping 5, 6, 7, 8, 9, 10

# Exemple pratique : traiter des fichiers avec erreurs
for file in *.csv; do
# Vérifier que le fichier existe et n'est pas vide
    if [ ! -s "$file" ]; then
        echo "Skipping empty file: $file"
        continue
    fi

    echo "Processing $file..."

# Si erreur critique, arrêter tout
    if ! validate_csv "$file"; then
        echo "Critical error in $file. Stopping."
        break
    fi

# Traiter le fichier
    process_csv "$file"
done

# break avec niveau (sortir de plusieurs boucles)
for i in {1..3}; do
    for j in {1..3}; do
        echo "i=$i, j=$j"
        if [ $i -eq 2 ] && [ $j -eq 2 ]; then
            break 2  # Sortir des 2 boucles
        fi
    done
done

# Exemple : chercher un fichier dans plusieurs dossiers
found=0
for dir in dir1 dir2 dir3; do
    for file in "$dir"/*.csv; do
        if [[ $file =~ important ]]; then
            echo "Found: $file"
            found=1
            break 2
        fi
    done
done

if [ $found -eq 0 ]; then
    echo "File not found"
fi
```

### Exemple complet : Script de traitement batch

```bash
#!/usr/bin/env bash
#
# Script: batch_processor.sh
# Description: Traite plusieurs fichiers CSV en batch
#

set -euo pipefail

# Variables
readonly INPUT_DIR="data/raw"
readonly OUTPUT_DIR="data/processed"
readonly ERROR_DIR="data/errors"
readonly LOG_FILE="batch_$(date +%Y%m%d_%H%M%S).log"

# Compteurs
total_files=0
processed_files=0
error_files=0

# Créer les dossiers nécessaires
mkdir -p "$OUTPUT_DIR" "$ERROR_DIR"

# Fonction de logging
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

# Fonction de validation
validate_csv() {
    local file=$1

# Vérifier que le fichier n'est pas vide
    if [ ! -s "$file" ]; then
        log "ERROR: File is empty: $file"
        return 1
    fi

# Vérifier le nombre de colonnes
    local expected_cols=5
    local actual_cols=$(head -1 "$file" | awk -F',' '{print NF}')

    if [ $actual_cols -ne $expected_cols ]; then
        log "ERROR: Expected $expected_cols columns, got $actual_cols in $file"
        return 1
    fi

    return 0
}

# Fonction de traitement
process_csv() {
    local input_file=$1
    local basename=$(basename "$input_file" .csv)
    local output_file="$OUTPUT_DIR/${basename}_processed.csv"

    log "Processing: $input_file"

# Traitement : supprimer les lignes vides et nettoyer
    sed '/^$/d' "$input_file" | \
        sed 's/^[[:space:]]*//; s/[[:space:]]*$//' > "$output_file"

# Vérifier le résultat
    if [ -s "$output_file" ]; then
        local input_lines=$(wc -l < "$input_file")
        local output_lines=$(wc -l < "$output_file")
        log "SUCCESS: $input_file -> $output_file ($input_lines -> $output_lines lines)"
        return 0
    else
        log "ERROR: Output file is empty: $output_file"
        rm -f "$output_file"
        return 1
    fi
}

# Fonction principale
main() {
    log "=== Batch Processing Started ==="
    log "Input directory: $INPUT_DIR"
    log "Output directory: $OUTPUT_DIR"

# Vérifier que le dossier input existe
    if [ ! -d "$INPUT_DIR" ]; then
        log "ERROR: Input directory not found: $INPUT_DIR"
        exit 1
    fi

# Compter les fichiers
    total_files=$(find "$INPUT_DIR" -name "*.csv" -type f | wc -l)

    if [ $total_files -eq 0 ]; then
        log "WARNING: No CSV files found in $INPUT_DIR"
        exit 0
    fi

    log "Found $total_files files to process"

# Traiter chaque fichier
    for csv_file in "$INPUT_DIR"/*.csv; do
# Vérifier que le fichier existe (pour éviter l'erreur si aucun CSV)
        [ -f "$csv_file" ] || continue

# Validation
        if ! validate_csv "$csv_file"; then
            log "SKIPPING: Validation failed for $csv_file"
            mv "$csv_file" "$ERROR_DIR/"
            ((error_files++))
            continue
        fi

# Traitement
        if process_csv "$csv_file"; then
            ((processed_files++))
        else
            log "MOVING TO ERROR: $csv_file"
            mv "$csv_file" "$ERROR_DIR/"
            ((error_files++))
        fi

# Pause courte entre les fichiers
        sleep 0.5
    done

# Rapport final
    log "=== Batch Processing Completed ==="
    log "Total files: $total_files"
    log "Successfully processed: $processed_files"
    log "Errors: $error_files"
    log "Success rate: $(( processed_files * 100 / total_files ))%"

# Code de retour
    if [ $error_files -gt 0 ]; then
        exit 1
    else
        exit 0
    fi
}

# Exécuter
main "$@"
```

### Exercices pratiques

#### 🎯 Exercice 1 : Validation avec conditions

Créez un script qui valide un fichier CSV :

1. Vérifie que le fichier existe
2. Vérifie qu'il n'est pas vide
3. Compte le nombre de lignes
4. Affiche "VALID" si plus de 10 lignes, "TOO SHORT" sinon

💡 Voir la solution

```bash
#!/bin/bash
set -euo pipefail

file=$1

if [ ! -f "$file" ]; then
    echo "ERROR: File not found"
    exit 1
fi

if [ ! -s "$file" ]; then
    echo "ERROR: File is empty"
    exit 1
fi

lines=$(wc -l < "$file")
echo "Lines: $lines"

if [ $lines -gt 10 ]; then
    echo "VALID"
else
    echo "TOO SHORT"
fi
```

#### 🎯 Exercice 2 : Boucle de traitement

Créez un script qui :

1. Boucle sur tous les fichiers CSV d'un dossier
2. Pour chaque fichier, compte les lignes
3. Si plus de 100 lignes : copie dans "large/"
4. Si moins de 100 lignes : copie dans "small/"
5. Affiche un résumé à la fin

💡 Voir la solution

```bash
#!/bin/bash
set -euo pipefail

mkdir -p large small

large_count=0
small_count=0

for file in *.csv; do
    [ -f "$file" ] || continue

    lines=$(wc -l < "$file")

    if [ $lines -gt 100 ]; then
        cp "$file" large/
        echo "$file -> large/ ($lines lines)"
        ((large_count++))
    else
        cp "$file" small/
        echo "$file -> small/ ($lines lines)"
        ((small_count++))
    fi
done

echo ""
echo "Summary:"
echo "Large files: $large_count"
echo "Small files: $small_count"
echo "Total: $((large_count + small_count))"
```

#### 💡 Points clés à retenir

- `if [ condition ]; then ... fi` : conditions
- `[[ ]]` : préférer à `[ ]` (plus puissant)
- `-eq, -ne, -gt, -lt` : comparaisons numériques
- `-f, -d, -s, -z, -n` : tests de fichiers et chaînes
- `for item in list; do ... done` : boucle for
- `while [ condition ]; do ... done` : boucle while
- `case var in pattern) ... ;; esac` : switch
- `break` et `continue` : contrôle de boucles

#### ✅ Partie 5 terminée !

Vous maîtrisez maintenant les structures de contrôle et les boucles. Vous pouvez créer des scripts
intelligents et automatisés. Passez à la Partie 6 pour les fonctions et outils avancés.

[Partie 6 : Fonctions et Outils Avancés →](partie6.md)