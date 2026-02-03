#### Attention

Ces solutions sont fournies à titre indicatif. Essayez toujours de résoudre les exercices par vous-même
avant de consulter les solutions. C'est en pratiquant que vous apprendrez le mieux !

## 📝 Solutions Partie 1-2 : Premiers pas

#### Solution 1.1 : Configuration initiale

```bash
# 1. Vérifier Git
git --version

# 2. Configurer identité
git config --global user.name "Votre Nom"
git config --global user.email "votre.email@example.com"

# 3. Configurer éditeur
git config --global core.editor "code --wait"

# 4. Créer des alias
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.lg "log --oneline --graph --all --decorate"

# 5. Afficher la configuration
git config --list
```

#### Solution 1.2 : Créer votre premier dépôt

```bash
# 1. Créer le dossier
mkdir mon-premier-projet
cd mon-premier-projet

# 2. Initialiser Git
git init

# 3. Créer README
echo "# Mon Premier Projet" > README.md
echo "Ce projet sert à apprendre Git" >> README.md

# 4. Ajouter à la staging area
git add README.md

# 5. Premier commit
git commit -m "docs: Initial commit with README"

# 6. Créer script Python
cat > script.py << 'EOF'
#!/usr/bin/env python3

def hello_git():
    print("Hello Git!")

if __name__ == "__main__":
    hello_git()
EOF

# 7. Commiter le script
git add script.py
git commit -m "feat: Add hello_git script"

# 8. Voir l'historique
git log --oneline
```

## 🌿 Solutions Partie 3-4 : Branches et Merge

#### Solution 2.1 : Travailler avec les branches

```bash
# 1-2. Créer et basculer sur la branche
git checkout -b feature/add-database

# 3. Créer database.py
cat > database.py << 'EOF'
import psycopg2

def connect_db():
    conn = psycopg2.connect(
        host="localhost",
        database="mydb",
        user="user",
        password="password"
    )
    return conn
EOF

# 4. Commiter
git add database.py
git commit -m "feat(db): Add PostgreSQL connection function"

# 5. Retour sur main
git checkout main

# 6. Créer nouvelle branche
git checkout -b feature/add-api

# 7. Créer api.py
cat > api.py << 'EOF'
from flask import Flask

app = Flask(__name__)

@app.route('/health')
def health():
    return {"status": "ok"}
EOF

# 8. Commiter
git add api.py
git commit -m "feat(api): Add Flask health endpoint"

# 9. Lister les branches
git branch -a
```

#### Solution 2.2 : Merger les branches

```bash
# 1. Retour sur main
git checkout main

# 2. Merger database
git merge feature/add-database

# 3. Merger api
git merge feature/add-api

# 4. Vérifier les fichiers
ls -la
# Devrait montrer: README.md, script.py, database.py, api.py

# 5. Visualiser l'historique
git log --oneline --graph --all --decorate

# 6. Supprimer les branches
git branch -d feature/add-database
git branch -d feature/add-api
```

#### Solution 2.3 : Résoudre un conflit de merge 🔥

```bash
# 1. Modifier README sur main
echo "Version 1.0" >> README.md
git commit -am "docs: Add version to README"

# 3-4. Créer branche et modifier
git checkout -b feature/update-readme
# Ouvrir README.md et remplacer "Version 1.0" par "Beta Version"
sed -i '' 's/Version 1.0/Beta Version/g' README.md
git commit -am "docs: Update version info"

# 6-7. Retour sur main et merge
git checkout main
git merge feature/update-readme
# CONFLICT!

# 8. Ouvrir README.md et résoudre
# Le fichier contient:
# <<<<<<< HEAD
# Version 1.0
# =======
# Beta Version
# >>>>>>> feature/update-readme

# Modifier pour garder :
# Version 1.0 (Beta)

# 9. Marquer comme résolu
git add README.md
git commit -m "docs: Merge and resolve version conflict"
```

## 🤝 Solutions Partie 5 : Collaboration avec GitHub

#### Solution 3.1 : Créer un dépôt sur GitHub

```bash
# 3. Ajouter le remote (remplacer USERNAME par votre nom)
git remote add origin https://github.com/USERNAME/git-training.git

# Ou avec SSH (recommandé)
git remote add origin git@github.com:USERNAME/git-training.git

# 4. Pousser vers GitHub
git push -u origin main

# Vérifier les remotes
git remote -v
```

#### Solution 3.2 : Workflow Pull Request

```bash
# 1. Créer la branche
git checkout -b feature/add-tests

# 2. Créer le fichier de tests
cat > test_script.py << 'EOF'
import unittest
from script import hello_git

class TestScript(unittest.TestCase):
    def test_hello_git(self):
# Test that the function runs without error
        try:
            hello_git()
            success = True
        except:
            success = False
        self.assertTrue(success)

if __name__ == '__main__':
    unittest.main()
EOF

# 3. Commiter et pousser
git add test_script.py
git commit -m "test: Add unit tests for hello_git function"
git push -u origin feature/add-tests

# 4-7. Sur GitHub :
# - Cliquez sur "Compare & pull request"
# - Ajoutez titre : "Add unit tests for script.py"
# - Description :
#   ## Summary
#   - Add unit tests for hello_git function
#   - Ensures code quality
#
#   ## Test Plan
#   - [x] Run tests locally
#   - [ ] Add more tests for edge cases
# - Créez la PR
# - Ajoutez un commentaire de review
# - Cliquez "Merge pull request"

# 8. Mettre à jour main local
git checkout main
git pull origin main
```

## 🔥 Solutions Défis avancés

#### Solution Défi 1 : Récupérer un commit perdu

```bash
# 1. Créer commit important
echo "IMPORTANT DATA" > important.txt
git add important.txt
git commit -m "feat: Add critical data"

# 2. Noter le hash
git log -1 --oneline
# Exemple: abc1234 feat: Add critical data

# 3. Reset (OUPS!)
git reset --hard HEAD~1
# Le fichier important.txt a disparu !

# 4. Utiliser reflog pour retrouver
git reflog
# Chercher : abc1234 HEAD@{1}: commit: feat: Add critical data

# 5. Récupérer le commit
git reset --hard abc1234
# OU
git reset --hard HEAD@{1}

# Le fichier important.txt est de retour ! 🎉
```

#### Solution Défi 2 : Cherry-pick intelligent

```bash
# 1. Créer branche avec 3 commits
git checkout -b feature/big-feature

echo "Feature work 1" > feature1.txt
git add feature1.txt
git commit -m "feat: Add feature part 1"

echo "Bug fix: validation" > bugfix.txt
git add bugfix.txt
git commit -m "fix: Correct validation logic"
# Noter ce hash : def5678

echo "Feature work 2" > feature2.txt
git add feature2.txt
git commit -m "feat: Add feature part 2"

# 2-3. Cherry-pick uniquement le fix
git checkout main
git cherry-pick def5678

# 4. Vérifier
ls -la
# bugfix.txt est présent
# feature1.txt et feature2.txt ne sont PAS là ✅
```

#### Solution Défi 3 : Nettoyer l'historique avec rebase interactif

```bash
# 1. Créer commits
git checkout -b feature/messy

echo "Code" > code.py
git add code.py
git commit -m "feat: Add code"

echo "print('debug')" >> code.py
git commit -am "WIP debug"

echo "# Fixed" >> code.py
git commit -am "fix bug"

echo "# Clean" >> code.py
git commit -am "debug: testing"

# 2. Rebase interactif
git rebase -i HEAD~4

# Dans l'éditeur qui s'ouvre, vous verrez :
# pick abc1234 feat: Add code
# pick def5678 WIP debug
# pick ghi9012 fix bug
# pick jkl3456 debug: testing

# Changez en :
# pick abc1234 feat: Add code
# squash def5678 WIP debug
# squash ghi9012 fix bug
# squash jkl3456 debug: testing

# Sauvegardez. Git ouvrira un autre éditeur pour le message final :
# feat: Add code with bug fixes

# 3. Vérifier
git log --oneline
# Un seul commit propre ! ✅
```

## ✅ Réponses des Quiz

#### Quiz : Concepts fondamentaux

- **Question 1:** Réponse **a) git status**
- **Question 2:** Réponse **b) Préparer les fichiers avant le commit**
- **Question 3:** Réponse **c) Chaque développeur possède une copie complète de l'historique**

#### Quiz : Branches et Merge

- **Question 4:** Réponse **b) git checkout -b nouvelle-branche**
- **Question 5:** Réponse **c) Quand deux branches modifient la même ligne**
- **Question 6:** Réponse **d) Ne jamais rebaser des commits déjà pushés**

#### Quiz : Collaboration

- **Question 7:** Réponse **b) git pull**
- **Question 8:** Réponse **c) À créer le lien de tracking entre branches locale et distante**

#### Quiz final : Git Hero

- **Question 9:** Réponse **c) git restore fichier.py**
- **Question 10:** Réponse **b) Non, jamais (utiliser S3/GCS)**
- **Question 11:** Réponse **d) Utiliser nbstripout**
- **Question 12:** Réponse **a) Utiliser Conventional Commits (feat:, fix:, etc.)**

#### 💡 Continuez à pratiquer

Ces solutions sont là pour vous guider, mais la meilleure façon d'apprendre Git est de pratiquer régulièrement.
Essayez de refaire les exercices plusieurs fois jusqu'à ce que les commandes deviennent naturelles.

[← Retour aux exercices](exercices.md)
[🚀 Projet fil rouge](projet-fil-rouge.md)