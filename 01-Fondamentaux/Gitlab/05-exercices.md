# 05 - Exercices : GitLab

[← 04 - Registry et Sécurité](04-registry-securite.md) | [🏠 Accueil](README.md)

---

Mettez en pratique vos connaissances sur GitLab.

## Exercice 1 : Navigation et Profil
1. Explorez l'interface d'un projet GitLab.
2. Identifiez où se configurent les clés SSH (spoiler: c'est dans votre profil utilisateur).
3. Quelle est la différence visuelle majeure entre un groupe et un projet ?

## Exercice 2 : Merge Request
1. Créez une branche `fix/typo-readme`.
2. Modifiez le fichier `README.md`.
3. Ouvrez une Merge Request et préfixez-la par `Draft:`.
4. Ajoutez un commentaire sur une ligne de votre changement et marquez-le comme "Résolu".

## Exercice 3 : Premier Pipeline CI/CD
1. À la racine de votre projet, créez un fichier `.gitlab-ci.yml`.
2. Définissez deux stages : `build` et `test`.
3. Dans le job `test`, utilisez une image Python et affichez la version de Python : `python --version`.
4. Validez le fichier et observez l'exécution dans le menu **Build > Pipelines**.

## Exercice 4 : Variables Secrètes
1. Allez dans **Settings > CI/CD > Variables**.
2. Créez une variable masquée nommée `API_KEY`.
3. Modifiez votre `.gitlab-ci.yml` pour afficher (partiellement) cette variable dans un job.

---

[← 04 - Registry et Sécurité](04-registry-securite.md) | [🏠 Accueil](README.md)
