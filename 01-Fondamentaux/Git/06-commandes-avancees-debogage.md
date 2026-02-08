# 06 - Commandes avancées et débogage

[← 05 - Collaboration](05-collaboration-remotes.md) | [🏠 Accueil](README.md) | [07 - Meilleures Pratiques Data →](07-meilleures-pratiques-data.md)

---

## 1. Annuler des modifications

### Restaurer un fichier (Undo local)
```bash
git restore script.py
```

### Unstage un fichier
```bash
git restore --staged script.py
```

### Annuler des commits (Reset)
- `--soft` : Annule le commit, garde les modifs stagées.
- `--hard` : Annule tout (DANGER : perte de données possible).
```bash
git reset --hard HEAD~1
```

---

## 2. Stash : Mettre de côté
Utile pour changer de branche sans committer un travail inachevé.
```bash
git stash              # Sauvegarder
git stash list         # Voir la liste
git stash pop          # Récupérer et supprimer
```

---

## 3. Débogage et Recherche
- **Blame** : Qui a modifié quelle ligne ?
  ```bash
  git blame script.py
  ```
- **Bisect** : Trouver quel commit a introduit un bug via une recherche binaire.
- **Reflog** : L'historique de toutes vos actions Git (votre filet de sécurité !).

---

## 4. Tags
Marquez vos versions importantes (ex: releases prod).
```bash
git tag -a v1.0.0 -m "Production release"
git push origin v1.0.0
```

---

[← 05 - Collaboration](05-collaboration-remotes.md) | [🏠 Accueil](README.md) | [07 - Meilleures Pratiques Data →](07-meilleures-pratiques-data.md)
