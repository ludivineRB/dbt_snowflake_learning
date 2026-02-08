# 03 - Premiers pas : Créer et gérer un dépôt

[← 02 - Configuration](02-installation-configuration.md) | [🏠 Accueil](README.md) | [04 - Maîtrise des branches →](04-maitrise-branches.md)

---

## 1. Initialiser ou Cloner un dépôt

### Nouveau projet local
```bash
mkdir mon-projet-data
cd mon-projet-data
git init
```

### Récupérer un projet existant
```bash
git clone https://github.com/username/projet.git
```

---

## 2. Le cycle de vie d'un fichier

### Vérifier l'état
```bash
git status
```

### Ajouter des modifications (Staging)
```bash
git add script.py      # Fichier spécifique
git add .              # Tout le dossier actuel
```

### Créer un commit (Snapshot)
```bash
git commit -m "feat: add initial data extraction script"
```

---

## 3. Consulter l'historique

### Liste des commits
```bash
git log                # Complet
git log --oneline      # Résumé
git log --graph        # Vue graphique des branches
```

### Voir un commit spécifique
```bash
git show <commit_hash>
```

---

## 💡 Conseil : Commits atomiques
Évitez de créer des commits géants. Un commit doit représenter une seule modification logique (ex: une fonction, une correction de bug). Cela facilite grandement la revue de code et le retour en arrière.

---

[← 02 - Configuration](02-installation-configuration.md) | [🏠 Accueil](README.md) | [04 - Maîtrise des branches →](04-maitrise-branches.md)
