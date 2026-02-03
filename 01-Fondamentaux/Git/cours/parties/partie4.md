## 4. Maîtriser les branches

### Pourquoi utiliser des branches ?

Les branches sont l'une des fonctionnalités les plus puissantes de Git. Elles permettent de :

- **Isoler le développement** : Travailler sur une feature sans affecter la branche principale
- **Expérimenter** : Tester des idées sans risque
- **Collaborer** : Chaque membre de l'équipe travaille sur sa branche
- **Gérer les releases** : Avoir des versions stables en production
- **Code review** : Faire relire le code avant de merger

![Git Branching](https://git-scm.com/book/en/v2/images/advance-master.png)

Les branches permettent un développement parallèle

### Créer et naviguer entre les branches

```bash
# Lister toutes les branches locales
git branch

# Lister toutes les branches (locales et distantes)
git branch -a

# Créer une nouvelle branche
git branch feature/mongodb-connector

# Basculer sur une branche existante
git checkout feature/mongodb-connector

# Créer ET basculer sur une nouvelle branche (raccourci)
git checkout -b feature/api-rest

# Syntaxe moderne (Git 2.23+)
git switch feature/mongodb-connector      # Changer de branche
git switch -c feature/new-dashboard       # Créer et changer

# Renommer une branche
git branch -m ancien-nom nouveau-nom

# Supprimer une branche (seulement si elle est mergée)
git branch -d feature/old-feature

# Forcer la suppression d'une branche
git branch -D feature/experimental
```

#### git checkout vs git switch

**git switch** est la commande moderne (Git 2.23+) pour changer de branche.
Elle est plus simple et moins ambiguë que `git checkout` qui fait plusieurs choses.

- `git switch` : Changer de branche uniquement
- `git checkout` : Changer de branche OU restaurer des fichiers (ambigu)

**Recommandation :** Utilisez `git switch` pour les branches et `git restore` pour les fichiers.

### Stratégies de branches courantes

#### 1. Git Flow (pour projets complexes)

```bash
main (production) ──────●────────●────────●──────▶
                         ↑        ↑        ↑
                         │        │        │
develop ─────●─────●─────┴────●───┴────●───┴──────▶
             ↑     ↑          ↑        ↑
             │     │          │        │
feature/A ───┴─────┘          │        │
                               │        │
feature/B ─────────────────────┴────────┘
```

- **main** : Code en production (toujours stable)
- **develop** : Branche de développement principale
- **feature/\*** : Nouvelles fonctionnalités
- **hotfix/\*** : Corrections urgentes en production
- **release/\*** : Préparation d'une release

#### 2. GitHub Flow (plus simple)

```bash
main ─────●─────────●───────────●─────────▶
          ↑         ↑           ↑
          │         │           │
feature/A ┴─────────┘           │
                                │
feature/B ──────────────────────┘
```

- Une seule branche principale : **main**
- Chaque feature part de main et y retourne via Pull Request
- Déploiement continu depuis main

### Fusionner des branches (Merge)

```bash
# 1. Se placer sur la branche de destination
git checkout main

# 2. Fusionner la branche feature
git merge feature/mongodb-connector

# Merge avec message personnalisé
git merge feature/api-rest -m "Merge API REST implementation"

# Merge sans fast-forward (crée toujours un commit de merge)
git merge --no-ff feature/dashboard

# Annuler un merge en cours (en cas de conflit)
git merge --abort
```

### Types de merge

#### Fast-Forward Merge

Quand il n'y a pas eu de commit sur la branche cible depuis la création de la branche feature.

```bash
Avant :
main      ●───●
               ↘
feature        ●───●

Après :
main      ●───●───●───●
```

#### 3-Way Merge

Quand les deux branches ont divergé. Git crée un commit de merge.

```bash
Avant :
main      ●───●───●
               ↘   ↘
feature        ●───●

Après :
main      ●───●───●───M
               ↘   ↗
feature        ●───●
```

### Résoudre les conflits de merge

Un conflit survient quand Git ne peut pas fusionner automatiquement des modifications contradictoires.

#### Quand surviennent les conflits ?

- Deux branches modifient la même ligne d'un fichier
- Un fichier est supprimé dans une branche et modifié dans l'autre
- Le même fichier est renommé différemment dans les deux branches

#### Étapes de résolution d'un conflit

```bash
# 1. Tenter le merge
git merge feature/new-pipeline

# Git affiche :
# Auto-merging etl_pipeline.py
# CONFLICT (content): Merge conflict in etl_pipeline.py
# Automatic merge failed; fix conflicts and then commit the result.

# 2. Voir les fichiers en conflit
git status
# Unmerged paths:
#   both modified:   etl_pipeline.py

# 3. Ouvrir le fichier en conflit
cat etl_pipeline.py
```

Le fichier contiendra des marqueurs de conflit :

```bash
def extract_data():
    """Extract data from source"""
<<<<<<< HEAD
    source = "postgresql://prod-db:5432/sales"
    engine = create_engine(source)
=======
    source = "mongodb://prod-mongo:27017/sales"
    client = MongoClient(source)
>>>>>>> feature/new-pipeline
    return data
```

- `<<<<<<< HEAD` : Code de la branche actuelle (main)
- `=======` : Séparateur
- `>>>>>>> feature/new-pipeline` : Code de la branche à merger

```bash
# 4. Éditer le fichier pour résoudre le conflit
# Supprimez les marqueurs et gardez le bon code

# 5. Marquer le conflit comme résolu
git add etl_pipeline.py

# 6. Finaliser le merge
git commit -m "Merge feature/new-pipeline - Resolved conflicts in etl_pipeline.py"

# Ou simplement :
git commit
# Git pré-remplit le message de commit
```

#### Outils pour résoudre les conflits

- **VS Code** : Détection automatique avec boutons "Accept Current/Incoming/Both"
- **Meld** : Outil de diff visuel
- **KDiff3** : Merge tool avancé
- `git mergetool` : Lancer l'outil configuré

### Rebase : Une alternative au merge

Le **rebase** réécrit l'historique en "rejouant" vos commits sur une autre base.

```bash
# Se placer sur la branche feature
git checkout feature/api-rest

# Rebaser sur main
git rebase main

# Si conflit, résoudre puis :
git add fichier-resolu.py
git rebase --continue

# Annuler le rebase
git rebase --abort
```

```bash
Avant rebase :
main      ●───●───●───●
               ↘
feature        ●───●

Après rebase :
main      ●───●───●───●
                       ↘
feature                ●───●
```

#### Règle d'or du rebase

**Ne JAMAIS rebaser des commits qui ont été pushés sur un dépôt public !**
Le rebase réécrit l'historique et peut causer des problèmes pour vos collaborateurs.

Utilisez le rebase uniquement sur vos branches locales non partagées.

#### ✅ Partie 4 terminée !

Vous maîtrisez maintenant les branches, le merge et la résolution de conflits.
Passez à la collaboration avec des dépôts distants !

[🎯 Faire les exercices](../exercices.md)
[Partie 5 →](partie5.md)