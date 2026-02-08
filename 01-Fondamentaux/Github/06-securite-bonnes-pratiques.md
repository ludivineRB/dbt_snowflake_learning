# 06 - Sécurité et bonnes pratiques

[← 05 - GitHub Actions](05-github-actions-cicd.md) | [🏠 Accueil](README.md) | [07 - Fonctionnalités avancées →](07-fonctionnalites-avancees.md)

---

## Objectifs de cette partie

- Activer et configurer Dependabot
- Utiliser Secret Scanning pour détecter les credentials
- Mettre en place Code Scanning avec CodeQL
- Protéger la branche main avec des règles
- Créer un README parfait pour un projet Data

## GitHub Security Features

### 1. Dependabot

**Dependabot** surveille vos dépendances et crée automatiquement des PR pour les
mettre à jour.

Activer Dependabot :

1. Allez dans **Settings** → **Code security and analysis**
2. Activez **Dependabot alerts**
3. Activez **Dependabot security updates**
4. Activez **Dependabot version updates**

Configurer avec `.github/dependabot.yml` :

```yaml
version: 2
updates:
# Python dependencies
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5

# GitHub Actions
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

### 2. Secret Scanning

GitHub scanne automatiquement votre code pour détecter des secrets commités par erreur
(API keys, tokens, passwords).

#### Si vous commitez un secret par erreur

1. **Révoquez-le immédiatement** (changez l'API key, le password)
2. Supprimez-le de l'historique Git avec `git filter-repo`
3. Ne faites PAS qu'un simple commit de suppression (il reste dans l'historique !)

### 3. Code Scanning

**CodeQL** analyse votre code pour détecter des vulnérabilités de sécurité.

Activer Code Scanning :

1. Allez dans **Security** → **Code scanning**
2. Cliquez sur **Set up code scanning**
3. Choisissez **CodeQL Analysis**
4. Un fichier `.github/workflows/codeql.yml` est créé automatiquement

### Protéger la branche main

Empêchez les push directs sur main et forcez les PR avec review :

1. Allez dans **Settings** → **Branches**
2. Cliquez sur **Add branch protection rule**
3. Branch name pattern : `main`
4. Cochez les options :
   - ✅ **Require a pull request before merging**
     - ✅ Require approvals (minimum 1)
     - ✅ Dismiss stale reviews
   - ✅ **Require status checks to pass**
     - Sélectionnez vos workflows (tests, lint, etc.)
   - ✅ **Require conversation resolution before merging**
   - ✅ **Include administrators** (même vous !)

#### Résultat

Personne ne peut pusher directement sur main. Toutes les modifications passent par une PR
avec au moins 1 approbation et tests qui passent.

### README parfait pour un projet Data

Un bon README contient :

```bash
# 📊 Nom du Projet

![CI Status](https://github.com/user/repo/workflows/Tests/badge.svg)
![Coverage](https://codecov.io/gh/user/repo/branch/main/graph/badge.svg)
![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)

Courte description du projet en une phrase.

## 🎯 Objectif

Description détaillée : quel problème résout ce projet ?

## 🚀 Quick Start

\`\`\`bash
# Cloner le projet
git clone https://github.com/user/repo.git
cd repo

# Installer les dépendances
pip install -r requirements.txt

# Lancer le pipeline
python run_pipeline.py
\`\`\`

## 📁 Structure du projet

\`\`\`
project/
├── src/              # Code source
│   ├── extract.py
│   ├── transform.py
│   └── load.py
├── tests/            # Tests unitaires
├── data/             # Données (non versionné)
├── docs/             # Documentation
└── .github/          # CI/CD workflows
\`\`\`

## 🛠️ Technologies

- Python 3.11
- pandas, SQLAlchemy
- PostgreSQL
- Apache Airflow
- Docker

## 📖 Documentation

[Lien vers la documentation complète](https://docs.example.com)

## 🤝 Contributing

Les contributions sont les bienvenues ! Voir [CONTRIBUTING.md](CONTRIBUTING.md).

## 📄 License

MIT License - voir [LICENSE](LICENSE)

## 👥 Authors

- [@username](https://github.com/username) - Initial work

## 🙏 Acknowledgments

- Inspiré par [projet-X](https://github.com/...)
- Merci à [@contributor](https://github.com/contributor) pour l'aide
```

### Badges pour votre README

Ajoutez des badges pour montrer l'état de votre projet :

- **CI Status** :
  `![CI](https://github.com/user/repo/workflows/Tests/badge.svg)`
- **Coverage** :
  `![Coverage](https://codecov.io/gh/user/repo/branch/main/graph/badge.svg)`
- **License** : `![License](https://img.shields.io/badge/license-MIT-blue.svg)`
- **Version** :
  `![Version](https://img.shields.io/badge/version-1.0.0-brightgreen)`

Créez des badges personnalisés sur [shields.io](https://shields.io)

### 💡 Points clés à retenir

- Dependabot maintient vos dépendances à jour automatiquement
- Secret Scanning détecte les credentials commités par erreur
- CodeQL analyse votre code pour trouver des vulnérabilités
- Protégez main avec des branch protection rules
- Un README complet facilite l'onboarding et la collaboration
- Les badges montrent l'état du projet en un coup d'œil

---

[← 05 - GitHub Actions](05-github-actions-cicd.md) | [🏠 Accueil](README.md) | [07 - Fonctionnalités avancées →](07-fonctionnalites-avancees.md)
