# 02 - Merge Requests (MR) et Collaboration

[← 01 - Introduction](01-introduction-concepts.md) | [🏠 Accueil](README.md) | [03 - GitLab CI/CD →](03-gitlab-ci-cd.md)

---

## 🎯 Objectifs de cette partie

- Maîtriser le workflow de Merge Request
- Comprendre les différences avec les PR de GitHub
- Utiliser les outils de review de GitLab

---

## 1. Qu'est-ce qu'une Merge Request ?

La **Merge Request (MR)** est l'équivalent GitLab de la Pull Request. C'est l'endroit où vous proposez des modifications de code, où vous en discutez avec vos pairs, et où les pipelines de test s'exécutent automatiquement.

### Workflow standard
1. Création d'une branche : `git checkout -b feature/ma-feature`.
2. Push des modifications : `git push origin feature/ma-feature`.
3. Ouverture d'une **Merge Request** via l'interface GitLab.
4. Discussion et corrections.
5. Approbation et **Merge**.

---

## 2. Fonctionnalités spécifiques à GitLab

### Draft Merge Requests
Vous pouvez marquer une MR comme **Draft** (Brouillon) en préfixant son titre par `Draft:`. Cela indique que le travail est en cours et empêche le merge accidentel.

### Widgets de Pipeline
Dans une MR GitLab, vous voyez en temps réel l'état de votre pipeline CI/CD, la couverture de code, et même les scans de sécurité directement intégrés dans l'interface de discussion.

---

## 3. Revue de code (Code Review)

- **Commentaires de ligne** : Cliquez sur le `+` à côté d'une ligne de code pour commenter.
- **Résolution de discussion** : Chaque fil de discussion peut être marqué comme "Résolu". GitLab peut bloquer le merge tant que toutes les discussions ne sont pas closes.
- **Suggestions** : Vous pouvez suggérer un changement de code directement dans un commentaire, et l'auteur peut l'appliquer en un clic.

---

## 4. Stratégies de Merge
GitLab propose plusieurs options :
- **Merge Commit** : Historique complet avec commit de merge.
- **Merge commit with semi-linear history** : Force un rebase avant le merge pour garder une ligne droite.
- **Fast-forward merge** : Pas de commit de merge, uniquement si la branche est à jour.

---

## 💡 Points clés à retenir

- Utilisez le préfixe `Draft:` pour les travaux en cours.
- Résolvez toutes les discussions pour garantir une review complète.
- Surveillez le widget de pipeline pour valider vos tests avant de demander une review.

---

[← 01 - Introduction](01-introduction-concepts.md) | [🏠 Accueil](README.md) | [03 - GitLab CI/CD →](03-gitlab-ci-cd.md)
