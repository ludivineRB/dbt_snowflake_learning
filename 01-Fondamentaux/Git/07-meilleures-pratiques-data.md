# 07 - Meilleures pratiques pour le Data Engineering

[← 06 - Avancé](06-commandes-avancees-debogage.md) | [🏠 Accueil](README.md) | [08 - Workflows et Automation →](08-workflows-automation.md)

---

## 1. Le .gitignore : Vital pour la Data
Évitez de commiter des données ou des secrets.

```text
# NE JAMAIS VERSIONNER LES DONNÉES
*.csv
*.parquet
data/

# Credentials
.env
config/secrets.yaml

# Notebooks
.ipynb_checkpoints/
```

### 💡 Astuce Jupyter Notebooks
Utilisez des outils comme `nbstripout` pour retirer les résultats d'exécution (images, tables) avant de committer, afin de garder un historique propre et léger.

---

## 2. Conventional Commits
Utilisez des messages structurés pour automatiser vos changelogs :
- `feat:` Nouvelle fonctionnalité.
- `fix:` Correction de bug.
- `docs:` Documentation.
- `perf:` Amélioration de performance.

---

## 3. Git LFS (Large File Storage)
Si vous **devez** versionner des fichiers volumineux (ex: modèles ML), utilisez Git LFS pour ne pas ralentir le dépôt.

---

[← 06 - Avancé](06-commandes-avancees-debogage.md) | [🏠 Accueil](README.md) | [08 - Workflows et Automation →](08-workflows-automation.md)
