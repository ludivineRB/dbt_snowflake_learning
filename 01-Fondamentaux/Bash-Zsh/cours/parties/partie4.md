## 4. Scripts Shell et Automatisation

Un script shell est un fichier contenant une série de commandes qui peuvent être exécutées automatiquement. C'est la base de l'automatisation en Data Engineering.

### Créer votre premier script

```bash
# Créer un fichier script
touch hello.sh

# Ajouter le contenu
cat > hello.sh << 'EOF'
#!/bin/bash
# Mon premier script

echo "Hello, World!"
echo "Date: $(date)"
echo "User: $(whoami)"
EOF

# Rendre exécutable
chmod +x hello.sh

# Exécuter
./hello.sh
```

### Le Shebang (#!/bin/bash)

#### Qu'est-ce que le shebang ?

La première ligne d'un script shell doit commencer par `#!` (shebang) suivi du chemin vers l'interpréteur.
Cela indique au système quel programme utiliser pour exécuter le script.

| Shebang | Description | Usage |
| --- | --- | --- |
| `#!/bin/bash` | Utilise Bash | Scripts Bash classiques |
| `#!/bin/zsh` | Utilise Zsh | Scripts Zsh spécifiques |
| `#!/bin/sh` | Utilise sh (POSIX) | Scripts portables |
| `#!/usr/bin/env bash` | Cherche bash dans le PATH | Portabilité maximale |

```bash
#!/bin/bash
# Script avec shebang Bash

#!/usr/bin/env bash
# Meilleure portabilité (recommandé)

#!/bin/zsh
# Script Zsh spécifique

#!/usr/bin/env python3
# Oui, ça marche aussi pour Python !
```

### Variables

```bash
#!/bin/bash

# Définir une variable (pas d'espace autour du =)
name="Alice"
age=30
city="Paris"

# Utiliser une variable avec $
echo "Name: $name"
echo "Age: $age"
echo "City: $city"

# Meilleure pratique : utiliser des accolades
echo "Hello, ${name}!"

# Variables en lecture seule (constantes)
readonly DB_HOST="localhost"
readonly DB_PORT=5432

# Variables d'environnement
export API_KEY="secret123"
export ENV="production"

# Command substitution (capturer la sortie d'une commande)
current_date=$(date +%Y-%m-%d)
file_count=$(ls | wc -l)
current_dir=$(pwd)

echo "Date: $current_date"
echo "Files: $file_count"
echo "Directory: $current_dir"

# Ancienne syntaxe (backticks) - à éviter
old_syntax=`date`

# Variables spéciales
echo "Script name: $0"
echo "PID: $$"
echo "Home: $HOME"
echo "User: $USER"
echo "Path: $PATH"
```

### Paramètres et arguments

| Variable | Description | Exemple |
| --- | --- | --- |
| `$0` | Nom du script | `echo $0` |
| `$1, $2, $3...` | Arguments positionnels | `echo $1` |
| `$@` | Tous les arguments (liste) | `echo "$@"` |
| `$*` | Tous les arguments (chaîne unique) | `echo "$*"` |
| `$#` | Nombre d'arguments | `echo $#` |
| `$?` | Code de retour de la dernière commande | `echo $?` |

```bash
#!/bin/bash
# Script: process_data.sh

echo "Script name: $0"
echo "First argument: $1"
echo "Second argument: $2"
echo "All arguments: $@"
echo "Number of arguments: $#"

# Exemple d'utilisation
# ./process_data.sh input.csv output.csv
# Output:
# Script name: ./process_data.sh
# First argument: input.csv
# Second argument: output.csv
# All arguments: input.csv output.csv
# Number of arguments: 2

# Vérifier le nombre d'arguments
if [ $# -ne 2 ]; then
    echo "Usage: $0  "
    exit 1
fi

input_file=$1
output_file=$2

echo "Processing $input_file..."
echo "Output will be saved to $output_file"

# Traiter tous les arguments
for arg in "$@"; do
    echo "Argument: $arg"
done
```

### Lecture d'entrées utilisateur

```bash
#!/bin/bash

# Lecture simple
echo "Enter your name:"
read name
echo "Hello, $name!"

# Lecture avec prompt
read -p "Enter your age: " age
echo "You are $age years old"

# Lecture sécurisée (masquer la saisie) - pour passwords
read -sp "Enter password: " password
echo  # Nouvelle ligne
echo "Password saved"

# Lecture avec valeur par défaut
read -p "Enter environment [dev]: " env
env=${env:-dev}
echo "Environment: $env"

# Lecture de plusieurs valeurs
read -p "Enter first and last name: " first last
echo "First: $first, Last: $last"

# Lire ligne par ligne depuis un fichier
while IFS= read -r line; do
    echo "Line: $line"
done < data.txt

# Exemple pratique : configuration interactive
read -p "Enter database host [localhost]: " db_host
db_host=${db_host:-localhost}

read -p "Enter database port [5432]: " db_port
db_port=${db_port:-5432}

read -p "Enter database name: " db_name

echo "Configuration:"
echo "  Host: $db_host"
echo "  Port: $db_port"
echo "  Database: $db_name"
```

### set -euo pipefail : Mode strict

#### ⚠️ Bonnes pratiques : Mode strict

Ajoutez toujours `set -euo pipefail` au début de vos scripts de production.
Cela rend vos scripts plus robustes et évite les erreurs silencieuses.

| Option | Description | Effet |
| --- | --- | --- |
| `set -e` | Exit on error | Arrête le script si une commande échoue |
| `set -u` | Unset variables | Erreur si utilisation d'une variable non définie |
| `set -o pipefail` | Pipeline failure | Pipeline échoue si une commande échoue |
| `set -x` | Debug mode | Affiche chaque commande avant exécution |

```bash
#!/bin/bash

# Mode strict (recommandé pour tous les scripts de production)
set -euo pipefail

# Explication :
# -e : Exit immédiatement si une commande retourne un code non-zero
# -u : Traite les variables non définies comme des erreurs
# -o pipefail : Le code de retour d'un pipeline est celui de la dernière commande qui a échoué

# Exemple sans set -e
echo "Starting script"
false  # Cette commande échoue
echo "This will still execute"  # S'exécute quand même

# Exemple avec set -e
set -e
echo "Starting script"
false  # Cette commande échoue
echo "This will NOT execute"  # Ne s'exécute jamais

# Exemple avec set -u
set -u
echo $undefined_variable  # Erreur : variable non définie

# Exemple avec set -o pipefail
set -o pipefail
cat non_existent_file | grep "pattern"  # Tout le pipeline échoue

# Désactiver temporairement
set +e
command_that_might_fail || true
set -e

# Script complet avec gestion d'erreurs
#!/bin/bash
set -euo pipefail

# Fonction de nettoyage en cas d'erreur
cleanup() {
    echo "Error occurred. Cleaning up..."
    rm -f temp_files*
}

# Appeler cleanup si erreur
trap cleanup ERR

echo "Processing data..."
# Vos commandes ici
```

### Codes de retour et gestion d'erreurs

```bash
#!/bin/bash

# Codes de retour standards
# 0 = succès
# 1-255 = erreur

# Vérifier le code de retour
ls /existing_directory
echo "Return code: $?"  # 0 (succès)

ls /non_existent_directory
echo "Return code: $?"  # 2 (erreur)

# Utiliser le code de retour dans une condition
if ls /tmp > /dev/null 2>&1; then
    echo "Directory exists"
else
    echo "Directory does not exist"
fi

# Retourner un code d'erreur depuis un script
exit 0   # Succès
exit 1   # Erreur générique
exit 2   # Erreur d'utilisation
exit 127 # Commande non trouvée

# Exemple complet avec gestion d'erreurs
#!/bin/bash
set -euo pipefail

INPUT_FILE=$1

# Vérifier que le fichier existe
if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: File '$INPUT_FILE' not found" >&2
    exit 1
fi

# Vérifier que le fichier n'est pas vide
if [ ! -s "$INPUT_FILE" ]; then
    echo "Error: File '$INPUT_FILE' is empty" >&2
    exit 2
fi

# Traiter le fichier
if ! process_file "$INPUT_FILE"; then
    echo "Error: Failed to process file" >&2
    exit 3
fi

echo "Success"
exit 0

# Utiliser || et && pour gérer les erreurs
command1 && command2  # command2 s'exécute SI command1 réussit
command1 || command2  # command2 s'exécute SI command1 échoue

# Exemples pratiques
mkdir /tmp/mydir || { echo "Failed to create directory"; exit 1; }
cd /tmp/mydir && echo "Directory changed successfully"

# Forcer le succès (ignorer les erreurs)
command_that_might_fail || true

# Capturer le code de retour
command
return_code=$?
if [ $return_code -ne 0 ]; then
    echo "Command failed with code $return_code"
fi
```

### Debugging de scripts

| Méthode | Description | Usage |
| --- | --- | --- |
| `bash -x script.sh` | Exécuter en mode debug | Affiche chaque commande |
| `set -x` | Activer le debug dans le script | Trace l'exécution |
| `set +x` | Désactiver le debug | Arrêter la trace |
| `echo "DEBUG: ..."` | Messages de debug manuels | Points de contrôle |
| `bash -n script.sh` | Vérifier la syntaxe | Sans exécuter |

```bash
# Méthode 1 : Exécuter avec -x
bash -x script.sh

# Output avec traces :
# + echo 'Starting script'
# Starting script
# + date
# Mon Jan 15 10:30:00 UTC 2024

# Méthode 2 : set -x dans le script
#!/bin/bash
set -x  # Activer le debug

echo "Processing data"
ls /tmp
date

set +x  # Désactiver le debug
echo "Debug off"

# Méthode 3 : Debug conditionnel
#!/bin/bash

DEBUG=${DEBUG:-0}

debug() {
    if [ $DEBUG -eq 1 ]; then
        echo "DEBUG: $*" >&2
    fi
}

debug "Starting processing"
process_data
debug "Processing complete"

# Utilisation : DEBUG=1 ./script.sh

# Méthode 4 : Vérifier la syntaxe sans exécuter
bash -n script.sh

# Méthode 5 : Fonction de logging
#!/bin/bash

log() {
    local level=$1
    shift
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] [$level] $*" >&2
}

log INFO "Script started"
log DEBUG "Processing file: $filename"
log ERROR "File not found"
log WARN "Disk space low"

# Méthode 6 : Tracer seulement une partie
#!/bin/bash

echo "Normal execution"

set -x
# Section à debugger
complex_operation
another_operation
set +x

echo "Back to normal"

# Méthode 7 : Sauvegarder les traces dans un fichier
#!/bin/bash
exec 2> debug.log  # Rediriger stderr vers un fichier
set -x

# Toutes les traces iront dans debug.log
command1
command2

# Méthode 8 : Variables de débogage
#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT_NAME="$(basename "${BASH_SOURCE[0]}")"

echo "Script: $SCRIPT_NAME"
echo "Directory: $SCRIPT_DIR"
echo "Arguments: $@"
echo "Number of args: $#"
```

### Exemple complet : Script de traitement de données

```bash
#!/usr/bin/env bash
#
# Script: process_sales_data.sh
# Description: Traite les fichiers de ventes et génère un rapport
# Usage: ./process_sales_data.sh
#

set -euo pipefail

# Variables globales
readonly SCRIPT_NAME=$(basename "$0")
readonly TIMESTAMP=$(date +%Y%m%d_%H%M%S)
readonly LOG_FILE="process_${TIMESTAMP}.log"

# Couleurs pour les messages
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly NC='\033[0m' # No Color

# Fonctions de logging
log_info() {
    echo -e "${GREEN}[INFO]${NC} $*" | tee -a "$LOG_FILE"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $*" | tee -a "$LOG_FILE"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $*" | tee -a "$LOG_FILE" >&2
}

# Fonction d'aide
usage() {
    cat << EOF
Usage: $SCRIPT_NAME

Process sales data and generate reports.

Arguments:
    input_csv   Path to input CSV file
    output_dir  Directory for output files

Example:
    $SCRIPT_NAME sales_2024.csv ./reports
EOF
    exit 1
}

# Vérification des arguments
if [ $# -ne 2 ]; then
    log_error "Invalid number of arguments"
    usage
fi

INPUT_FILE=$1
OUTPUT_DIR=$2

# Validation des entrées
log_info "Validating inputs..."

if [ ! -f "$INPUT_FILE" ]; then
    log_error "Input file not found: $INPUT_FILE"
    exit 1
fi

if [ ! -s "$INPUT_FILE" ]; then
    log_error "Input file is empty: $INPUT_FILE"
    exit 2
fi

# Créer le répertoire de sortie
mkdir -p "$OUTPUT_DIR"

# Fonction de nettoyage en cas d'erreur
cleanup() {
    log_warn "Cleaning up temporary files..."
    rm -f "${OUTPUT_DIR}"/temp_*
}

trap cleanup EXIT ERR

# Traitement principal
log_info "Starting data processing..."
log_info "Input: $INPUT_FILE"
log_info "Output directory: $OUTPUT_DIR"

# Compter les lignes
total_lines=$(wc -l < "$INPUT_FILE")
log_info "Total lines: $total_lines"

# Générer le rapport de résumé
report_file="${OUTPUT_DIR}/summary_${TIMESTAMP}.txt"
log_info "Generating summary report..."

{
    echo "Sales Data Summary Report"
    echo "========================="
    echo "Generated: $(date)"
    echo "Input file: $INPUT_FILE"
    echo ""
    echo "Statistics:"
    echo "- Total records: $((total_lines - 1))"
    echo ""
    echo "Top 10 products by sales:"
    tail -n +2 "$INPUT_FILE" | \
        awk -F',' '{print $2}' | \
        sort | uniq -c | sort -rn | head -10
} > "$report_file"

log_info "Summary report saved to: $report_file"

# Filtrer les ventes importantes (>1000)
high_value_file="${OUTPUT_DIR}/high_value_${TIMESTAMP}.csv"
log_info "Filtering high-value sales..."

head -1 "$INPUT_FILE" > "$high_value_file"
awk -F',' 'NR>1 && $4 > 1000' "$INPUT_FILE" >> "$high_value_file"

high_value_count=$(( $(wc -l < "$high_value_file") - 1 ))
log_info "Found $high_value_count high-value sales"

# Calculer le total
total_sales=$(awk -F',' 'NR>1 {sum += $4} END {print sum}' "$INPUT_FILE")
log_info "Total sales amount: $total_sales"

# Succès
log_info "Processing completed successfully!"
log_info "Output files:"
log_info "  - $report_file"
log_info "  - $high_value_file"
log_info "Log file: $LOG_FILE"

exit 0
```

### Template de script robuste

```bash
#!/usr/bin/env bash
#
# Script: template.sh
# Description: Template pour scripts robustes
# Author: Your Name
# Date: 2024-01-15
#

# Mode strict
set -euo pipefail

# Variables globales (constantes en majuscules)
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly SCRIPT_NAME="$(basename "${BASH_SOURCE[0]}")"
readonly TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Configuration
DEBUG=${DEBUG:-0}
VERBOSE=${VERBOSE:-0}

# Fonctions utilitaires
die() {
    echo "ERROR: $*" >&2
    exit 1
}

log_debug() {
    [ $DEBUG -eq 1 ] && echo "DEBUG: $*" >&2
}

log_verbose() {
    [ $VERBOSE -eq 1 ] && echo "INFO: $*" >&2
}

usage() {
    cat << EOF
Usage: $SCRIPT_NAME [OPTIONS]

Description of what the script does.

OPTIONS:
    -h, --help      Show this help message
    -v, --verbose   Verbose output
    -d, --debug     Debug mode

ARGUMENTS:
    arg1            Description of arg1
    arg2            Description of arg2

EXAMPLES:
    $SCRIPT_NAME input.csv output.csv
    DEBUG=1 $SCRIPT_NAME input.csv output.csv
EOF
    exit 0
}

# Nettoyage à la sortie
cleanup() {
    log_debug "Cleanup function called"
# Ajoutez votre code de nettoyage ici
}

trap cleanup EXIT

# Parser les options
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            usage
            ;;
        -v|--verbose)
            VERBOSE=1
            shift
            ;;
        -d|--debug)
            DEBUG=1
            shift
            ;;
        -*)
            die "Unknown option: $1"
            ;;
        *)
            break
            ;;
    esac
done

# Validation des arguments
[ $# -lt 1 ] && usage

# Votre logique principale ici
log_verbose "Script started"
log_debug "Arguments: $*"

# ... votre code ...

log_verbose "Script completed successfully"
exit 0
```

### Exercices pratiques

#### 🎯 Exercice 1 : Script basique

Créez un script `backup.sh` qui :

1. Prend un répertoire en argument
2. Vérifie que le répertoire existe
3. Crée une archive tar.gz avec la date dans le nom
4. Affiche un message de succès avec la taille de l'archive

💡 Voir la solution

```bash
#!/bin/bash
set -euo pipefail

# Vérifier les arguments
if [ $# -ne 1 ]; then
    echo "Usage: $0 "
    exit 1
fi

DIR=$1

# Vérifier que le répertoire existe
if [ ! -d "$DIR" ]; then
    echo "Error: Directory '$DIR' not found"
    exit 1
fi

# Créer l'archive
BACKUP_NAME="backup_$(basename "$DIR")_$(date +%Y%m%d_%H%M%S).tar.gz"
tar -czf "$BACKUP_NAME" "$DIR"

# Afficher le résultat
SIZE=$(du -h "$BACKUP_NAME" | cut -f1)
echo "Backup created successfully: $BACKUP_NAME"
echo "Size: $SIZE"
```

#### 🎯 Exercice 2 : Script avec options

Créez un script `analyze.sh` qui :

1. Accepte un fichier CSV en argument
2. Option -c : compter les lignes
3. Option -h : afficher le header
4. Option -s : afficher les statistiques (nombre de colonnes)
5. Sans option : afficher les 10 premières lignes

💡 Voir la solution

```bash
#!/bin/bash
set -euo pipefail

usage() {
    echo "Usage: $0 [-c|-h|-s] "
    echo "  -c  Count lines"
    echo "  -h  Show header"
    echo "  -s  Show statistics"
    exit 1
}

# Parser les options
while getopts "chs" opt; do
    case $opt in
        c) MODE="count" ;;
        h) MODE="header" ;;
        s) MODE="stats" ;;
        *) usage ;;
    esac
done

shift $((OPTIND-1))

# Vérifier le fichier
[ $# -ne 1 ] && usage
FILE=$1

[ ! -f "$FILE" ] && { echo "Error: File not found"; exit 1; }

# Exécuter selon le mode
case ${MODE:-preview} in
    count)
        wc -l < "$FILE"
        ;;
    header)
        head -1 "$FILE"
        ;;
    stats)
        echo "Lines: $(wc -l < "$FILE")"
        echo "Columns: $(head -1 "$FILE" | awk -F',' '{print NF}')"
        ;;
    preview)
        head -10 "$FILE"
        ;;
esac
```

#### 💡 Points clés à retenir

- `#!/usr/bin/env bash` : shebang portable
- `set -euo pipefail` : mode strict obligatoire
- `$1, $2, $@, $#` : gestion des arguments
- `read` : lire les entrées utilisateur
- `exit 0/1` : codes de retour
- `bash -x` : debug mode
- Toujours valider les entrées et gérer les erreurs
- Utiliser des fonctions de logging

#### ✅ Partie 4 terminée !

Vous savez maintenant créer des scripts shell robustes et automatisés. Passez à la Partie 5
pour apprendre les structures de contrôle (conditions, boucles).

[Partie 5 : Structures de Contrôle et Boucles →](partie5.md)