## 3. Premiers pas : Créer et gérer un dépôt

### Initialiser un nouveau dépôt

```bash
# Créer un nouveau dossier et initialiser Git
mkdir mon-projet-data
cd mon-projet-data
git init

# Résultat : Initialized empty Git repository in .../mon-projet-data/.git/

# Voir le contenu du dossier .git
ls -la
# Vous verrez un dossier .git/ qui contient toute la base de données Git
```

### Cloner un dépôt existant

```bash
# Cloner un dépôt depuis GitHub
git clone https://github.com/username/projet.git

# Cloner avec un nom de dossier personnalisé
git clone https://github.com/username/projet.git mon-dossier

# Cloner via SSH (recommandé pour l'authentification)
git clone git@github.com:username/projet.git
```

### Workflow de base : Le cycle de vie d'un fichier

```bash
    Untracked ──────┐
        ↓           │
    Unmodified      │
        ↓           │       git add
    Modified ───────┴──────────────▶ Staged
        ↑                               │
        │         git commit            │
        └───────────────────────────────┘
```

### Vérifier l'état du dépôt

```bash
# Voir l'état actuel
git status

# Version courte (plus concise)
git status -s
# ?? = untracked
# A  = staged
# M  = modified
# D  = deleted
```

### Exemple pratique : Premier commit

```bash
# 1. Créer un fichier Python pour un pipeline ETL
echo "# Pipeline ETL Sales Data" > etl_sales.py
echo "import pandas as pd" >> etl_sales.py

# 2. Vérifier le statut
git status
# On branch main
# Untracked files:
#   etl_sales.py

# 3. Ajouter le fichier à la staging area
git add etl_sales.py

# 4. Vérifier à nouveau
git status
# Changes to be committed:
#   new file:   etl_sales.py

# 5. Créer le commit
git commit -m "Initial commit: Add sales ETL pipeline skeleton"

# 6. Vérifier l'historique
git log
```

### Ajouter des fichiers : Les différentes méthodes

```bash
# Ajouter un fichier spécifique
git add fichier.py

# Ajouter plusieurs fichiers
git add fichier1.py fichier2.py config.yaml

# Ajouter tous les fichiers Python
git add *.py

# Ajouter tous les fichiers modifiés/nouveaux
git add .

# Ajouter tous les fichiers d'un dossier
git add src/

# Mode interactif (choisir fichier par fichier)
git add -i

# Ajouter par morceaux (patch mode)
git add -p
# Vous permet de choisir quelles parties d'un fichier ajouter
```

### Créer des commits efficaces

```bash
# Commit simple avec message court
git commit -m "Fix data validation bug in ETL pipeline"

# Commit avec message détaillé (ouvre l'éditeur)
git commit

# Ajouter tous les fichiers modifiés ET committer (ne fonctionne pas pour les nouveaux fichiers)
git commit -am "Update database connection string"

# Modifier le dernier commit (ajouter des fichiers oubliés ou corriger le message)
git commit --amend

# Commit avec un message multi-ligne
git commit -m "Add data quality checks" -m "- Check for null values
- Validate email format
- Ensure date consistency"
```

#### Convention de messages de commit

Suivez le format **Conventional Commits** :

- `feat:` Nouvelle fonctionnalité
- `fix:` Correction de bug
- `docs:` Modification de documentation
- `style:` Formatage, points-virgules manquants, etc.
- `refactor:` Refactorisation du code
- `test:` Ajout de tests
- `chore:` Mise à jour de dépendances, config, etc.

**Exemple :** `feat: Add MongoDB data extraction module`

### Consulter l'historique

```bash
# Voir tous les commits
git log

# Format condensé (une ligne par commit)
git log --oneline

# Voir les modifications de chaque commit
git log -p

# Limiter aux N derniers commits
git log -5

# Voir l'historique avec un graphe des branches
git log --oneline --graph --all --decorate

# Filtrer par auteur
git log --author="John Doe"

# Filtrer par date
git log --since="2 weeks ago"
git log --after="2024-01-01" --before="2024-12-31"

# Rechercher dans les messages de commit
git log --grep="ETL"

# Voir quels fichiers ont été modifiés
git log --stat

# Format personnalisé
git log --pretty=format:"%h - %an, %ar : %s"
```

### Voir les détails d'un commit spécifique

```bash
# Afficher un commit spécifique
git show

# Exemple
git show a3f5b21

# Voir uniquement les fichiers modifiés
git show --name-only a3f5b21
```

#### Attention aux commits trop gros

Évitez de créer des commits qui contiennent trop de modifications différentes.
Préférez des commits atomiques (une modification logique = un commit).
Cela facilite la revue de code et le débogage.

#### ✅ Partie 3 terminée !

Vous savez maintenant créer un dépôt, faire vos premiers commits et consulter l'historique.
Prêt pour les branches !

[🎯 Faire les exercices](../exercices.md)
[Partie 4 →](partie4.md)