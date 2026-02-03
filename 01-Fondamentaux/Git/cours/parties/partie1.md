## 1. Introduction à Git et au versionnage

### Qu'est-ce que Git ?

**Git** est un système de contrôle de version distribué créé par Linus Torvalds en 2005.
C'est l'outil le plus utilisé au monde pour gérer les versions de code source et suivre l'historique
des modifications d'un projet.

![Git Logo](https://git-scm.com/images/logos/downloads/Git-Logo-2Color.png)

Logo officiel de Git

### Pourquoi Git est essentiel en Data Engineering ?

#### 📊 Versionnage des pipelines

Suivez l'évolution de vos scripts ETL, transformations et orchestrations avec un historique complet.

#### 🤝 Collaboration d'équipe

Plusieurs Data Engineers travaillent simultanément sur les mêmes pipelines sans conflits.

#### 🔄 Reproductibilité

Retournez à n'importe quelle version antérieure en cas de bug ou de régression.

#### 🚀 CI/CD Integration

Déployez automatiquement vos pipelines de données dans différents environnements.

#### 📝 Documentation automatique

Les messages de commit servent de journal des modifications et décisions.

#### 🔍 Audit et traçabilité

Identifiez qui a fait quoi, quand et pourquoi dans votre codebase.

### Les concepts fondamentaux

| Concept | Description | Analogie |
| --- | --- | --- |
| **Repository (Dépôt)** | Conteneur qui stocke tout l'historique du projet | Une bibliothèque avec tous les livres et leurs versions |
| **Commit** | Snapshot (photo) de votre code à un instant T | Une sauvegarde de jeu vidéo |
| **Branch (Branche)** | Ligne de développement indépendante | Une version alternative de votre projet |
| **Merge (Fusion)** | Combinaison de deux branches | Fusionner deux documents Word |
| **Remote** | Version du dépôt hébergée sur un serveur distant | Votre cloud storage (GitHub, GitLab) |
| **Clone** | Copie locale d'un dépôt distant | Télécharger un projet depuis le cloud |

### Architecture Git : Distribué vs Centralisé

![Git Branches](https://git-scm.com/images/about/branches@2x.png)

Git permet un développement parallèle avec des branches

#### Git vs SVN/CVS

Contrairement aux systèmes centralisés (SVN, CVS), Git est **distribué**.
Chaque développeur possède une copie complète de l'historique, permettant de travailler hors ligne
et de créer des branches sans toucher au serveur central.

### Les trois états de Git

```bash
┌─────────────────────┐      ┌─────────────────────┐      ┌─────────────────────┐
│                     │      │                     │      │                     │
│  Working Directory  │─────▶│   Staging Area      │─────▶│   Repository        │
│   (Modifié)         │      │   (Préparé)         │      │   (Commité)         │
│                     │      │                     │      │                     │
└─────────────────────┘      └─────────────────────┘      └─────────────────────┘
        ▲                            ▲                            │
        │                            │                            │
        │        git checkout        │         git add            │   git commit
        └────────────────────────────┴────────────────────────────┘
                                                (Modifie/Stage/Commit)
```

- **Working Directory** : Vos fichiers actuels sur lesquels vous travaillez
- **Staging Area (Index)** : Zone de préparation avant le commit
- **Repository (.git)** : Base de données contenant tout l'historique

#### ✅ Partie 1 terminée !

Vous avez appris les bases de Git et compris pourquoi c'est essentiel en Data Engineering.
Passez maintenant aux exercices ou continuez avec la Partie 2 sur l'installation.

[🎯 Faire les exercices](../exercices.md)
[Partie 2 →](partie2.md)