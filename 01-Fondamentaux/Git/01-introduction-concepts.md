# 01 - Introduction à Git et au versionnage

[🏠 Accueil](README.md) | [02 - Installation et Configuration →](02-installation-configuration.md)

---

## 1. Qu'est-ce que Git ?

**Git** est un système de contrôle de version distribué créé par Linus Torvalds en 2005.
C'est l'outil le plus utilisé au monde pour gérer les versions de code source et suivre l'historique
des modifications d'un projet.

![Git Logo](https://git-scm.com/images/logos/downloads/Git-Logo-2Color.png)

### Pourquoi Git est essentiel en Data Engineering ?

- **📊 Versionnage des pipelines** : Suivez l'évolution de vos scripts ETL et orchestrations.
- **🤝 Collaboration d'équipe** : Plusieurs Data Engineers travaillent simultanément sans conflits.
- **🔄 Reproductibilité** : Retournez à n'importe quelle version antérieure en cas de bug.
- **🚀 Intégration CI/CD** : Déployez automatiquement vos pipelines dans différents environnements.
- **🔍 Audit et traçabilité** : Identifiez qui a fait quoi, quand et pourquoi.

---

## 2. Les concepts fondamentaux

| Concept | Description | Analogie |
| --- | --- | --- |
| **Repository (Dépôt)** | Conteneur qui stocke tout l'historique du projet | Une bibliothèque avec toutes ses versions |
| **Commit** | Snapshot (photo) de votre code à un instant T | Une sauvegarde de jeu vidéo |
| **Branch (Branche)** | Ligne de développement indépendante | Une version alternative de votre projet |
| **Merge (Fusion)** | Combinaison de deux branches | Fusionner deux documents Word |
| **Remote** | Version du dépôt hébergée sur un serveur | Votre cloud storage (GitHub, GitLab) |

---

## 3. Architecture Git : Distribué vs Centralisé

Contrairement aux systèmes centralisés (SVN, CVS), Git est **distribué**.
Chaque développeur possède une copie complète de l'historique, permettant de travailler hors ligne et de créer des branches sans toucher au serveur central.

### Les trois états de Git

1. **Working Directory** : Vos fichiers actuels sur lesquels vous travaillez.
2. **Staging Area (Index)** : Zone de préparation avant le commit.
3. **Repository (.git)** : Base de données contenant tout l'historique.

```text
Working Directory  ─────►  Staging Area  ─────►  Repository
      (Modifié)             (Préparé)             (Commité)
```

---

[🏠 Accueil](README.md) | [02 - Installation et Configuration →](02-installation-configuration.md)
