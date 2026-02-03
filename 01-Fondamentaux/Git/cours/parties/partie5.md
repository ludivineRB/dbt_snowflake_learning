## 5. Collaboration avec des dépôts distants (Remote)

### Qu'est-ce qu'un remote ?

Un **remote** est une version de votre projet hébergée sur un serveur (GitHub, GitLab, Bitbucket).
Il permet la collaboration et la sauvegarde du code.

![Remote Branches](https://git-scm.com/book/en/v2/images/remote-branches-1.png)

Schéma de synchronisation entre dépôt local et remote

### Gérer les remotes

```bash
# Lister les remotes configurés
git remote -v

# Résultat typique :
# origin  https://github.com/user/repo.git (fetch)
# origin  https://github.com/user/repo.git (push)

# Ajouter un remote
git remote add origin https://github.com/username/projet.git

# Renommer un remote
git remote rename origin upstream

# Supprimer un remote
git remote remove upstream

# Voir les détails d'un remote
git remote show origin

# Changer l'URL d'un remote
git remote set-url origin https://github.com/newuser/newrepo.git
```

### Fetch, Pull et Push

#### 📥 git fetch

Télécharge les commits du remote sans les fusionner

```bash
git fetch origin
git fetch --all
```

#### ⬇️ git pull

Télécharge ET fusionne les commits (fetch + merge)

```bash
git pull origin main
git pull --rebase
```

#### ⬆️ git push

Envoie vos commits locaux vers le remote

```bash
git push origin main
git push -u origin feature
```

### Workflow de collaboration complet

```bash
# 1. Cloner le projet
git clone https://github.com/team/data-platform.git
cd data-platform

# 2. Créer une branche pour votre feature
git checkout -b feature/mongodb-etl

# 3. Développer votre feature
echo "def extract_mongodb():" > mongodb_extractor.py
git add mongodb_extractor.py
git commit -m "feat: Add MongoDB data extractor"

# 4. Récupérer les dernières modifications de main
git fetch origin
git checkout main
git pull origin main

# 5. Rebaser votre branche sur main (optionnel mais recommandé)
git checkout feature/mongodb-etl
git rebase main

# 6. Pousser votre branche vers le remote
git push -u origin feature/mongodb-etl
# Le -u (--set-upstream) crée le lien entre la branche locale et distante

# 7. Créer une Pull Request sur GitHub/GitLab

# 8. Après validation et merge de la PR, mettre à jour main
git checkout main
git pull origin main

# 9. Supprimer la branche locale
git branch -d feature/mongodb-etl

# 10. Supprimer la branche distante
git push origin --delete feature/mongodb-etl
```

### Commandes push avancées

```bash
# Pousser une nouvelle branche et créer le lien
git push -u origin feature/new-dashboard

# Pousser tous les tags
git push --tags

# Pousser toutes les branches
git push --all

# Forcer le push (DANGER : réécrit l'historique distant)
git push --force origin feature/experimental

# Force push plus sûr (échoue si quelqu'un a pushé entre-temps)
git push --force-with-lease origin feature/api-rest

# Supprimer une branche distante
git push origin --delete feature/old-feature
```

#### Attention au force push !

`git push --force` peut détruire le travail de vos collaborateurs.
Utilisez toujours `--force-with-lease` à la place, qui échoue si quelqu'un
a pushé des commits dont vous n'avez pas connaissance.

### Suivre des branches distantes

```bash
# Voir toutes les branches (locales et distantes)
git branch -a

# Créer une branche locale depuis une branche distante
git checkout -b feature/api origin/feature/api
# ou plus simplement :
git checkout --track origin/feature/api

# Voir les branches de suivi
git branch -vv

# Mettre à jour les références des branches distantes
git fetch --prune
# Supprime les références locales de branches qui n'existent plus sur le remote
```

### Pull Request / Merge Request

Les **Pull Requests** (GitHub) ou **Merge Requests** (GitLab)
sont le mécanisme standard pour intégrer du code dans un projet collaboratif.

#### Créer une PR

1. Pusher votre branche feature
2. Aller sur GitHub/GitLab
3. Cliquer sur "New Pull Request"
4. Sélectionner base (main) et compare (votre feature)
5. Ajouter description et captures d'écran
6. Assigner des reviewers

#### Processus de review

1. Les reviewers commentent le code
2. Vous effectuez les modifications
3. Push les corrections sur la même branche
4. La PR se met à jour automatiquement
5. Approbation et merge par le lead

#### Bonnes pratiques pour les PR

- Gardez les PR petites (< 400 lignes si possible)
- Écrivez une description claire avec le contexte
- Ajoutez des captures d'écran pour les changements UI
- Liez les issues/tickets associés
- Répondez rapidement aux commentaires de review
- Assurez-vous que les tests passent avant de demander une review

#### ✅ Partie 5 terminée !

Vous savez maintenant collaborer avec des dépôts distants et créer des Pull Requests.
Passons aux commandes avancées !

[🎯 Faire les exercices](../exercices.md)
[Partie 6 →](partie6.md)