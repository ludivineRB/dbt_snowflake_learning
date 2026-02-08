# 03 - GitLab CI/CD

[← 02 - Merge Requests](02-merge-requests.md) | [🏠 Accueil](README.md) | [04 - Registry et Sécurité →](04-registry-securite.md)

---

## 🎯 Objectifs de cette partie

- Comprendre le fichier `.gitlab-ci.yml`
- Maîtriser les concepts de Stages, Jobs et Artifacts
- Utiliser les GitLab Runners

---

## 1. Le fichier .gitlab-ci.yml

Tout le pipeline est défini dans un fichier à la racine du projet nommé `.gitlab-ci.yml`.

### Exemple simple pour Python :
```yaml
stages:
  - test
  - deploy

run_tests:
  stage: test
  image: python:3.11
  script:
    - pip install pytest
    - pytest tests/

deploy_prod:
  stage: deploy
  script:
    - echo "Déploiement en cours..."
  only:
    - main
```

---

## 2. Concepts Fondamentaux

- **Stages** : Groupes de jobs (ex: Build, Test, Deploy). Les jobs d'un même stage s'exécutent en parallèle.
- **Jobs** : Tâches spécifiques à exécuter.
- **Artifacts** : Fichiers générés par un job que vous voulez conserver ou passer au job suivant (ex: un rapport de test, un fichier JAR).
- **Variables** : GitLab propose des variables prédéfinies (ex: `$CI_COMMIT_BRANCH`) et vous permet d'en ajouter des secrètes (Settings > CI/CD > Variables).

---

## 3. Les GitLab Runners

Le **Runner** est l'agent qui exécute réellement les commandes définies dans votre YAML.
- **Shared Runners** : Fournis par GitLab.com.
- **Specific Runners** : Serveurs que vous installez vous-même pour vos propres projets (souvent sur Kubernetes ou des instances cloud).

---

## 4. CI/CD pour la Data

Dans un contexte Data Engineering, GitLab CI/CD est idéal pour :
- **Lancer des tests dba** sur votre entrepôt de données.
- **Valider des schémas JSON/Avro**.
- **Builder des images Docker** contenant vos jobs Spark.
- **Déployer des DAGs Airflow**.

---

## 💡 Points clés à retenir

- Tout se passe dans le fichier `.gitlab-ci.yml`.
- Les stages s'exécutent séquentiellement, les jobs d'un stage en parallèle.
- Utilisez les **Artifacts** pour sauvegarder vos résultats de tests ou vos builds.

---

[← 02 - Merge Requests](02-merge-requests.md) | [🏠 Accueil](README.md) | [04 - Registry et Sécurité →](04-registry-securite.md)
