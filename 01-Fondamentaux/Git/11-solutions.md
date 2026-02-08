# 11 - Solutions des exercices

[← 10 - Projet Fil Rouge](10-projet-fil-rouge.md) | [🏠 Accueil](README.md)

---

## 📝 Solution Niveau 1 : Bases
```bash
# Identité
git config --global user.name "Nom"
git config --global user.email "email@test.com"

# Repo
mkdir git-data-practice && cd git-data-practice
git init

# Commit
touch requirements.txt
git add requirements.txt
git commit -m "chore: initial requirements"

# Alias
git config --global alias.st status
```

## 🌿 Solution Niveau 2 : Branches
```bash
git switch -c feature/add-extractor
touch extractor.py
git add extractor.py
git commit -m "feat: add extractor script"
git switch main
git merge feature/add-extractor
git branch -d feature/add-extractor
```

## 🤝 Solution Niveau 3 : Collaboration
```bash
git remote add origin https://github.com/user/repo.git
git push -u origin main
```

---

[← 10 - Projet Fil Rouge](10-projet-fil-rouge.md) | [🏠 Accueil](README.md)
