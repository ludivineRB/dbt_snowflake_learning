# 07 - Fonctionnalités avancées

[← 06 - Sécurité](06-securite-bonnes-pratiques.md) | [🏠 Accueil](README.md) | [08 - Exercices →](08-exercices.md)

---

## Objectifs de cette partie

- Maîtriser GitHub CLI (gh)
- Partager du code avec Gists
- Utiliser GitHub Codespaces
- Héberger des packages sur GitHub
- Animer une communauté avec Discussions

## GitHub CLI (gh)

**gh** est l'outil en ligne de commande officiel de GitHub pour gérer repositories,
PR, issues, etc. depuis le terminal.

### Installation

```bash
# macOS
brew install gh

# Linux
sudo apt install gh

# Windows
winget install GitHub.cli
```

### Authentification

```bash
# Se connecter à GitHub
gh auth login

# Choisissez GitHub.com
# Choisissez HTTPS ou SSH
# Authentifiez-vous via le navigateur
```

### Commandes utiles

```bash
# Créer un repository
gh repo create my-new-repo --public --clone

# Créer une Pull Request
gh pr create --title "Add feature X" --body "Description"

# Lister les PR
gh pr list

# Voir le détail d'une PR
gh pr view 42

# Checkout une PR localement
gh pr checkout 42

# Merger une PR
gh pr merge 42 --squash

# Créer une issue
gh issue create --title "Bug found" --body "Description"

# Lister les issues
gh issue list

# Voir les workflows
gh workflow list

# Voir les runs d'un workflow
gh run list --workflow=tests.yml

# Cloner un repo
gh repo clone username/repo
```

## GitHub Gists

Les **Gists** permettent de partager rapidement des snippets de code.

```bash
# Créer un Gist
gh gist create script.py --desc "Useful data cleaning script"

# Lister vos Gists
gh gist list

# Voir un Gist
gh gist view <gist-id>
```

## GitHub Codespaces

**Codespaces** est un environnement de développement cloud complet avec VS Code dans le
navigateur.

- Environnement de dev prêt en quelques secondes
- Accessible de n'importe où
- Gratuit jusqu'à 60h/mois pour les comptes personnels

Pour créer un Codespace :

1. Sur votre repository, cliquez sur **Code**
2. Onglet **Codespaces**
3. Cliquez sur **Create codespace on main**

## GitHub Packages

Hébergez vos packages Python, Docker, npm, etc. directement sur GitHub.

```bash
# Publier une image Docker
docker tag myimage ghcr.io/username/myimage:latest
docker push ghcr.io/username/myimage:latest

# Installer un package Python depuis GitHub Packages
pip install --index-url https://pypi.github.com/username mypackage
```

## GitHub Discussions

Forum de discussion intégré au repository pour :

- Questions et réponses
- Annonces
- Idées et propositions
- Discussions générales

Activer Discussions :

1. **Settings** → **General**
2. Cochez **Discussions**

### Récapitulatif des bonnes pratiques

- Protégez la branche main avec branch protection rules
- Utilisez Pull Requests pour toutes les modifications
- Écrivez des descriptions de PR complètes et claires
- Faites des reviews de code constructives
- Configurez CI/CD avec GitHub Actions
- Activez Dependabot et Secret Scanning
- Utilisez Issues et Projects pour organiser le travail
- Documentez avec un README complet
- Ajoutez des badges pour montrer l'état du projet
- Ne committez JAMAIS de secrets ou credentials

### Aide-mémoire : Workflow quotidien sur GitHub

```bash
1. Synchroniser main
   git checkout main && git pull origin main

2. Créer une branche feature
   git checkout -b feature/nouvelle-fonctionnalite

3. Développer et committer
# ... coder ...
   git add . && git commit -m "feat: add feature X"

4. Pousser et créer une PR
   git push -u origin feature/nouvelle-fonctionnalite
   gh pr create --title "Add feature X" --body "Description"

5. Review et intégration des feedbacks
# ... corrections ...
   git add . && git commit -m "fix: address review comments"
   git push

6. Merge de la PR
   gh pr merge --squash

7. Nettoyage
   git checkout main && git pull origin main
   git branch -d feature/nouvelle-fonctionnalite
```

## 📚 Ressources et liens utiles

[**Documentation officielle GitHub**

Guide complet de toutes les fonctionnalités GitHub](https://docs.github.com)
[**GitHub Skills**

Cours interactifs gratuits pour apprendre GitHub](https://skills.github.com)
[**GitHub Learning Lab**

Exercices pratiques dans de vrais repositories](https://lab.github.com)
[**GitHub Actions Marketplace**

Des milliers d'actions prêtes à l'emploi](https://github.com/marketplace?type=actions)
[**GitHub CLI Documentation**

Documentation de l'outil en ligne de commande gh](https://cli.github.com)
[**Awesome Lists**

Listes curées de ressources sur tous les sujets tech](https://github.com/awesome-lists)

#### Prochaines étapes

Maintenant que vous maîtrisez GitHub, explorez :

- **GitHub Advanced Security** : Features de sécurité avancées (GHAS)
- **GitHub Enterprise** : Fonctionnalités pour les grandes entreprises
- **GitHub GraphQL API** : API puissante pour automatiser GitHub
- **GitHub Apps** : Créer des intégrations personnalisées

#### 🎉 Félicitations !

Vous avez terminé la formation GitHub ! Vous maîtrisez maintenant :

- ✅ Les concepts fondamentaux de GitHub
- ✅ Le workflow de collaboration avec Pull Requests
- ✅ La gestion de projet avec Issues et Projects
- ✅ L'automatisation avec GitHub Actions
- ✅ La sécurisation de vos projets
- ✅ Les outils avancés pour être plus productif

Continuez à pratiquer sur vos propres projets et n'hésitez pas à contribuer à l'open source !

---

[← 06 - Sécurité](06-securite-bonnes-pratiques.md) | [🏠 Accueil](README.md) | [08 - Exercices →](08-exercices.md)
