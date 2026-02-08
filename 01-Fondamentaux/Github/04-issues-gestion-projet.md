# 04 - Issues et Gestion de projet

[← 03 - Pull Requests](03-pull-requests-code-review.md) | [🏠 Accueil](README.md) | [05 - GitHub Actions →](05-github-actions-cicd.md)

---

## Objectifs de cette partie

- Créer et gérer des Issues efficacement
- Utiliser Labels et Milestones pour organiser
- Maîtriser GitHub Projects avec tableaux Kanban
- Lier Issues et Pull Requests automatiquement
- Automatiser la gestion de projet

## Les Issues GitHub

Les **Issues** sont le système de tickets de GitHub. Elles servent à :

- 📋 Suivre les bugs
- 💡 Proposer de nouvelles fonctionnalités
- ❓ Poser des questions
- 📝 Documenter des tâches à faire
- 💬 Discuter d'améliorations

### Créer une Issue

1. Allez dans l'onglet **Issues**
2. Cliquez sur **New issue**
3. Choisissez un template (si configuré) ou créez une issue vide

#### Exemple d'issue bien rédigée

#### 🐛 Bug: Data pipeline fails with null timestamp

**Description**
Le pipeline ETL échoue quand un timestamp est null dans les données source.

**Steps to reproduce**

1. Lancer le pipeline avec `python run_etl.py`
2. Utiliser le fichier de test `data/test_null_timestamp.csv`
3. Observer l'erreur dans les logs

**Expected behavior**
Le pipeline devrait ignorer ou remplacer les timestamps null avec une valeur par défaut.

**Actual behavior**
Le pipeline crash avec l'erreur : `ValueError: cannot parse null timestamp`

**Environment**

- Python 3.11
- pandas 2.0.3
- OS: macOS

**Additional context**
Cette erreur est apparue après le merge de la PR #45.

### Labels : Organiser les Issues

Les **labels** permettent de catégoriser les issues :

| Label | Utilisation |
| --- | --- |
| bug | Quelque chose ne fonctionne pas |
| enhancement | Nouvelle fonctionnalité ou amélioration |
| documentation | Amélioration de la documentation |
| good first issue | Bon pour les nouveaux contributeurs |
| help wanted | Besoin d'aide de la communauté |
| priority: high | Urgent à traiter |
| wontfix | Ne sera pas corrigé |

### Milestones : Planifier des versions

Les **Milestones** regroupent des issues pour une release ou un objectif spécifique.

#### Exemple : Milestone "v2.0.0 - Production Ready"

- Date cible : 31 décembre 2024
- Description : Première version prête pour la production
- Issues liées : 15 issues (10 fermées, 5 ouvertes)
- Progression : 67%

### GitHub Projects : Tableau Kanban

**GitHub Projects** est un système de gestion de projet intégré, similaire à Jira ou
Trello.

#### Créer un Project

1. Allez dans l'onglet **Projects**
2. Cliquez sur **New project**
3. Choisissez un template : **Board** (Kanban), **Table**, ou
   **Roadmap**
4. Donnez un nom : "Data Platform Q1 2025"

#### Colonnes typiques d'un Kanban

```bash
┌─────────────┬─────────────┬─────────────┬─────────────┬─────────────┐
│   Backlog   │   To Do     │ In Progress │   Review    │    Done     │
│             │             │             │             │             │
│  Issue #45  │  Issue #52  │  Issue #48  │  PR #50     │  Issue #42  │
│  Issue #46  │  Issue #53  │  Issue #49  │             │  Issue #43  │
│             │             │             │             │  Issue #44  │
└─────────────┴─────────────┴─────────────┴─────────────┴─────────────┘
```

- **Backlog** : Idées et tâches futures
- **To Do** : Prêt à être commencé
- **In Progress** : En cours de développement
- **Review** : En code review (PR ouverte)
- **Done** : Terminé et mergé

#### Automatisation

GitHub Projects peut automatiquement déplacer les issues et PR entre les colonnes
(ex: passer en "Review" quand une PR est créée, en "Done" quand elle est mergée).

### Lier Issues et Pull Requests

Utilisez des mots-clés dans vos PR pour fermer automatiquement des issues :

```bash
## Description

Correction du bug de parsing des timestamps null.

## Closes

Closes #45
Fixes #46
Resolves #47

## Related

See also #48
```

Mots-clés reconnus : `closes`, `fixes`, `resolves`

#### Avantage

Quand la PR est mergée, les issues liées sont automatiquement fermées.
Cela maintient votre backlog à jour sans effort manuel.

### 💡 Points clés à retenir

- Les Issues sont le système de tickets central pour suivre bugs et features
- Utilisez Labels pour catégoriser et Milestones pour planifier les releases
- GitHub Projects offre des tableaux Kanban pour visualiser le travail
- Liez automatiquement Issues et PR avec closes/fixes/resolves
- L'automatisation réduit la gestion manuelle du projet

---

[← 03 - Pull Requests](03-pull-requests-code-review.md) | [🏠 Accueil](README.md) | [05 - GitHub Actions →](05-github-actions-cicd.md)
