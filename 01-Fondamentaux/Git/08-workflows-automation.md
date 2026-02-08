# 08 - Workflows et Automation

[← 07 - Pratiques Data](07-meilleures-pratiques-data.md) | [🏠 Accueil](README.md) | [09 - Exercices →](09-exercices.md)

---

## 1. Pre-commit Hooks
Automatisez les vérifications (linting, formatage) avant chaque commit.
1. Installez pre-commit : `pip install pre-commit`.
2. Configurez `.pre-commit-config.yaml`.
3. Installez les hooks : `pre-commit install`.

---

## 2. CI/CD avec Git
Liez vos commits à des actions automatiques sur GitHub/GitLab :
- Lancer des tests unitaires à chaque Pull Request.
- Déployer vos pipelines Data quand le code arrive sur `main`.

---

## 3. Git + Docker
Versionnez votre environnement en même temps que votre code avec un `Dockerfile`.
Utilisez le hash du commit Git pour tagger vos images Docker afin de garantir une traçabilité parfaite entre le code et l'image en production.

---

[← 07 - Pratiques Data](07-meilleures-pratiques-data.md) | [🏠 Accueil](README.md) | [09 - Exercices →](09-exercices.md)
