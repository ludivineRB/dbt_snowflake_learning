# 01 - Introduction à GitLab

[🏠 Retour à l'accueil](README.md) | [02 - Merge Requests →](02-merge-requests.md)

---

## 🎯 Objectifs de cette partie

- Comprendre ce qu'est GitLab et ses particularités
- Faire la distinction entre GitLab SaaS et Self-managed
- Comparer GitLab et GitHub
- Découvrir l'écosystème "All-in-one" de GitLab

---

## 1. Qu'est-ce que GitLab ?

**GitLab** est une plateforme complète de DevOps fournie sous forme d'une application unique. Contrairement à GitHub qui a longtemps été un hébergeur de code avant d'ajouter des outils, GitLab a été conçu dès le départ pour couvrir tout le cycle de vie du développement logiciel (SDLC).

![GitLab Logo](https://about.gitlab.com/images/press/logos/gitlab-icon-rgb.png)

### GitLab SaaS vs Self-managed
Une des grandes forces de GitLab est sa flexibilité :
- **GitLab.com (SaaS)** : Hébergé par GitLab, prêt à l'emploi.
- **GitLab Self-managed** : Vous installez GitLab sur vos propres serveurs (souvent via Docker ou Linux). C'est le choix privilégié des entreprises pour la souveraineté des données.

---

## 2. GitLab vs GitHub : Les différences clés

| Fonctionnalité | GitHub | GitLab |
| --- | --- | --- |
| **Collaboration** | Pull Requests (PR) | Merge Requests (MR) |
| **CI/CD** | GitHub Actions (YAML) | GitLab CI/CD (.gitlab-ci.yml) |
| **Intégration** | Écosystème d'Apps tiers | Tout-en-un (intégré nativement) |
| **Installation** | Principalement SaaS | SaaS ou Self-managed |
| **Open Source** | Propriétaire (Microsoft) | Core Open Source (GitLab Inc) |

---

## 3. Pourquoi utiliser GitLab en Data Engineering ?

- **GitLab CI/CD** : Considéré comme l'un des outils de CI/CD les plus matures et puissants du marché pour orchestrer des pipelines de données complexes.
- **Auto DevOps** : Configuration automatique de la compilation, des tests et du déploiement.
- **Souveraineté** : Possibilité d'héberger ses données et son code sur ses propres serveurs ou cloud privé.
- **Container Registry** : Stockage intégré de vos images Docker pour vos jobs Spark ou Airflow.

---

## 4. Concepts clés de GitLab

- **Project** : L'équivalent du Repository.
- **Group** : Pour organiser plusieurs projets et gérer les permissions à grande échelle.
- **Merge Request (MR)** : L'équivalent de la Pull Request.
- **Runner** : L'agent qui exécute vos pipelines de CI/CD.

---

## 💡 Points clés à retenir

- GitLab est une plateforme **DevOps complète** (All-in-one).
- Il est très populaire en entreprise grâce à sa version **Self-managed**.
- En Data Engineering, on l'apprécie particulièrement pour la puissance de son **CI/CD**.

---

[🏠 Retour à l'accueil](README.md) | [02 - Merge Requests →](02-merge-requests.md)
