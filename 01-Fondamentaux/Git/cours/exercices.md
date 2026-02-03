#### 📚 Comment utiliser cette page

Essayez de résoudre les exercices par vous-même avant de consulter les solutions.
Les solutions détaillées sont disponibles dans un fichier séparé pour vous encourager
à chercher par vous-même d'abord !

[📖 Voir toutes les solutions](solutions.md)

## 📝 Exercices Partie 1-2 : Premiers pas

#### Exercice 1.1 : Configuration initiale

**Objectif :** Configurer votre environnement Git

1. Vérifiez que Git est installé sur votre machine
2. Configurez votre nom et email
3. Définissez votre éditeur par défaut
4. Créez 3 alias utiles
5. Affichez toute votre configuration

[📖 Voir la solution](solutions.html#solution-1-1)

#### Exercice 1.2 : Créer votre premier dépôt

**Objectif :** Initialiser un dépôt et créer vos premiers commits

1. Créez un dossier `mon-premier-projet`
2. Initialisez un dépôt Git
3. Créez un fichier `README.md` avec une description
4. Ajoutez-le à la staging area
5. Créez votre premier commit
6. Créez un fichier `script.py` avec du code Python
7. Commitez ce nouveau fichier
8. Consultez l'historique

[📖 Voir la solution](solutions.html#solution-1-2)

#### 📝 Quiz : Concepts fondamentaux

**Question 1:** Quelle commande permet de voir l'état actuel du dépôt ?

- git status
- git state
- git info
- git current

**Question 2:** Quel est le rôle de la staging area ?

- Stocker les fichiers définitivement
- Préparer les fichiers avant le commit
- Supprimer les fichiers modifiés
- Synchroniser avec le remote

**Question 3:** Que signifie un système de contrôle de version "distribué" ?

- Le code est stocké sur plusieurs serveurs
- Plusieurs personnes peuvent travailler en même temps
- Chaque développeur possède une copie complète de l'historique
- Le code est divisé en plusieurs parties

## 🌿 Exercices Partie 3-4 : Branches et Merge

#### Exercice 2.1 : Travailler avec les branches

**Objectif :** Créer et gérer des branches

1. Dans votre dépôt, créez une branche `feature/add-database`
2. Basculez sur cette branche
3. Créez un fichier `database.py` avec une fonction de connexion
4. Commitez sur la branche feature
5. Retournez sur `main`
6. Créez une autre branche `feature/add-api`
7. Créez un fichier `api.py`
8. Commitez sur cette branche
9. Listez toutes les branches

[📖 Voir la solution](solutions.html#solution-2-1)

#### Exercice 2.2 : Merger les branches

**Objectif :** Fusionner les branches dans main

1. Retournez sur `main`
2. Mergez `feature/add-database`
3. Mergez `feature/add-api`
4. Vérifiez que les deux fichiers sont présents dans main
5. Visualisez l'historique sous forme de graphe
6. Supprimez les branches feature

[📖 Voir la solution](solutions.html#solution-2-2)

#### Exercice 2.3 : Résoudre un conflit de merge 🔥

**Objectif :** Apprendre à gérer les conflits

1. Sur `main`, modifiez `README.md` : ajoutez "Version 1.0" en bas
2. Commitez : `git commit -am "docs: Add version to README"`
3. Créez une branche `feature/update-readme`
4. Sur cette branche, modifiez `README.md` : ajoutez "Beta Version" à la même ligne
5. Commitez sur la branche feature
6. Retournez sur main
7. Tentez de merger : `git merge feature/update-readme`
8. CONFLIT ! Résolvez-le en gardant les deux informations
9. Marquez comme résolu et finalisez le merge

[📖 Voir la solution](solutions.html#solution-2-3)

#### 📝 Quiz : Branches et Merge

**Question 4:** Quelle commande crée ET bascule sur une nouvelle branche ?

- git branch -c nouvelle-branche
- git checkout -b nouvelle-branche
- git create nouvelle-branche
- git new branch nouvelle-branche

**Question 5:** Quand survient un conflit de merge ?

- Quand on merge deux branches vides
- Quand on crée trop de branches
- Quand deux branches modifient la même ligne
- Quand on oublie de commit

**Question 6:** Quelle est la règle d'or du rebase ?

- Toujours rebaser avant de merger
- Ne jamais rebaser sur main
- Rebaser tous les jours
- Ne jamais rebaser des commits déjà pushés

## 🤝 Exercices Partie 5 : Collaboration avec GitHub

#### Exercice 3.1 : Créer un dépôt sur GitHub

**Objectif :** Pousser votre projet local vers GitHub

1. Créez un compte GitHub (si vous n'en avez pas)
2. Créez un nouveau dépôt public `git-training`
3. Ajoutez le remote à votre dépôt local
4. Poussez votre branche main vers GitHub
5. Vérifiez sur GitHub que tout est bien présent

[📖 Voir la solution](solutions.html#solution-3-1)

#### Exercice 3.2 : Workflow Pull Request

**Objectif :** Créer une Pull Request complète

1. Créez une branche `feature/add-tests`
2. Créez un fichier `test_script.py` avec des tests
3. Commitez et poussez la branche vers GitHub
4. Sur GitHub, créez une Pull Request
5. Ajoutez une description détaillée
6. Simulez une review : ajoutez un commentaire
7. Mergez la PR
8. Mettez à jour votre branche main locale

[📖 Voir la solution](solutions.html#solution-3-2)

#### 📝 Quiz : Collaboration

**Question 7:** Quelle commande récupère ET fusionne les modifications du remote ?

- git fetch
- git pull
- git merge
- git sync

**Question 8:** À quoi sert le flag -u dans git push -u origin main ?

- À pousser plus rapidement
- À pousser de manière urgente
- À créer le lien de tracking entre branches locale et distante
- À pousser en mode univers

## 🔥 Défis avancés

#### Défi 1 : Récupérer un commit perdu

**Scénario :** Vous avez fait un `git reset --hard` par erreur et perdu un commit important !

1. Créez un commit avec un fichier important
2. Notez son hash
3. Faites `git reset --hard HEAD~1` (le commit disparaît !)
4. Utilisez `git reflog` pour le retrouver
5. Récupérez le commit perdu

[📖 Voir la solution](solutions.html#solution-defi-1)

#### Défi 2 : Cherry-pick intelligent

**Scénario :** Vous devez appliquer un fix urgent d'une branche feature dans main

1. Créez une branche `feature/big-feature` avec 3 commits
2. Le 2ème commit contient un fix de bug important
3. Sans merger toute la branche, appliquez UNIQUEMENT le fix dans main
4. Vérifiez que main a le fix mais pas les autres changements

[📖 Voir la solution](solutions.html#solution-defi-2)

#### Défi 3 : Nettoyer l'historique avec rebase interactif

**Scénario :** Vous avez fait plusieurs petits commits de debug à nettoyer

1. Créez une branche avec 4 commits dont 2 sont des "WIP" ou "debug"
2. Utilisez `git rebase -i HEAD~4` pour les fusionner
3. Réécrivez l'historique proprement

[📖 Voir la solution](solutions.html#solution-defi-3)

### 🎓 Quiz final : Êtes-vous un Git Hero ?

**Question 9:** Quelle commande annule les modifications d'un fichier non stagé ?

- git reset fichier.py
- git undo fichier.py
- git restore fichier.py
- git revert fichier.py

**Question 10:** En Data Engineering, faut-il versionner les fichiers .csv ?

- Oui, toujours
- Non, jamais (utiliser S3/GCS)
- Oui, mais seulement avec Git LFS
- Oui, si moins de 1GB

**Question 11:** Comment nettoyer les outputs des Jupyter notebooks avant commit ?

- Les supprimer manuellement dans le .ipynb
- Ne jamais versionner les .ipynb
- Utiliser git clean
- Utiliser nbstripout

**Question 12:** Quelle est la meilleure pratique pour les messages de commit ?

- Utiliser Conventional Commits (feat:, fix:, etc.)
- Écrire des messages très longs
- Utiliser des emojis uniquement
- Écrire "update" pour tout

📊 Voir mon score

#### 🎉 Félicitations !

Vous avez terminé tous les exercices ! Vous êtes maintenant prêt à appliquer vos connaissances
sur un projet réel avec le **Projet fil rouge : Pipeline ETL Sales Data**.

[🚀 Démarrer le projet fil rouge](projet-fil-rouge.md)