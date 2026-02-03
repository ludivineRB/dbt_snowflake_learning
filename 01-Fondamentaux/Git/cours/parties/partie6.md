## 6. Commandes avancées et débogage

### Annuler des modifications

```bash
# Annuler les modifications d'un fichier non stagé
git checkout -- fichier.py
# ou (Git 2.23+)
git restore fichier.py

# Restaurer tous les fichiers non stagés
git restore .

# Retirer un fichier de la staging area (unstage)
git reset HEAD fichier.py
# ou
git restore --staged fichier.py

# Annuler le dernier commit (garde les modifications)
git reset --soft HEAD~1

# Annuler le dernier commit ET les modifications
git reset --hard HEAD~1

# Annuler les N derniers commits
git reset --hard HEAD~3

# Revenir à un commit spécifique
git reset --hard
```

### Différences entre reset --soft, --mixed, --hard

| Commande | HEAD | Staging Area | Working Directory |
| --- | --- | --- | --- |
| `--soft` | ✓ Modifié | ✗ Intact | ✗ Intact |
| `--mixed` (défaut) | ✓ Modifié | ✓ Réinitialisé | ✗ Intact |
| `--hard` | ✓ Modifié | ✓ Réinitialisé | ✓ Réinitialisé |

### Modifier l'historique avec commit --amend

```bash
# Modifier le message du dernier commit
git commit --amend -m "Nouveau message corrigé"

# Ajouter des fichiers oubliés au dernier commit
git add fichier_oublie.py
git commit --amend --no-edit
# --no-edit garde le message existant

# Modifier l'auteur du dernier commit
git commit --amend --author="Nouveau Nom "
```

#### Attention avec --amend

N'utilisez `--amend` que si vous n'avez PAS encore pushé le commit.
Sinon, vous devrez faire un force push.

### Stash : Mettre de côté temporairement

Le **stash** permet de sauvegarder temporairement vos modifications en cours
sans créer de commit, utile pour changer de branche rapidement.

```bash
# Sauvegarder les modifications en cours
git stash

# Stash avec un message descriptif
git stash save "Work in progress on MongoDB connector"

# Lister tous les stashes
git stash list
# Résultat :
# stash@{0}: WIP on main: abc1234 Last commit message
# stash@{1}: On feature: xyz5678 Previous stash

# Voir le contenu d'un stash
git stash show stash@{0}
git stash show -p stash@{0}  # Voir le diff

# Réappliquer le dernier stash ET le supprimer
git stash pop

# Réappliquer un stash sans le supprimer
git stash apply stash@{1}

# Supprimer un stash spécifique
git stash drop stash@{0}

# Supprimer tous les stashes
git stash clear

# Créer une branche depuis un stash
git stash branch nouvelle-branche stash@{0}
```

### Voir les différences (diff)

```bash
# Voir les modifications non stagées
git diff

# Voir les modifications stagées (prêtes à être commitées)
git diff --staged
# ou
git diff --cached

# Différence pour un fichier spécifique
git diff fichier.py

# Différence entre deux branches
git diff main..feature/api-rest

# Différence entre deux commits
git diff abc123..def456

# Voir uniquement les noms des fichiers modifiés
git diff --name-only

# Statistiques des modifications
git diff --stat

# Différence d'un commit spécifique
git diff ^!
```

### Chercher dans l'historique

```bash
# Trouver quand un mot a été introduit ou supprimé
git log -S "extract_data" --source --all

# Chercher dans les messages de commit
git log --grep="MongoDB"

# Voir qui a modifié chaque ligne d'un fichier
git blame fichier.py

# Blame avec plus de contexte
git blame -L 10,20 fichier.py  # Lignes 10 à 20

# Trouver le commit qui a introduit un bug (bisect)
git bisect start
git bisect bad                  # Le commit actuel est mauvais
git bisect good v1.0           # v1.0 était bon
# Git va checkout des commits intermédiaires
# Testez et indiquez :
git bisect good   # ou git bisect bad
# Répétez jusqu'à trouver le commit fautif
git bisect reset  # Terminer la recherche
```

### Tags : Versionner vos releases

```bash
# Créer un tag lightweight
git tag v1.0.0

# Créer un tag annoté (recommandé)
git tag -a v1.0.0 -m "Release version 1.0.0 - Initial production release"

# Lister tous les tags
git tag

# Lister les tags avec un pattern
git tag -l "v1.0.*"

# Voir les détails d'un tag
git show v1.0.0

# Taguer un commit passé
git tag -a v0.9.0 abc1234 -m "Retroactive tag for beta release"

# Pousser un tag vers le remote
git push origin v1.0.0

# Pousser tous les tags
git push --tags

# Supprimer un tag local
git tag -d v1.0.0

# Supprimer un tag distant
git push origin --delete v1.0.0

# Checkout sur un tag spécifique
git checkout v1.0.0
```

#### Semantic Versioning

Utilisez le format **vMAJOR.MINOR.PATCH** :

- **MAJOR** : Changements incompatibles avec les versions précédentes
- **MINOR** : Nouvelles fonctionnalités rétrocompatibles
- **PATCH** : Corrections de bugs rétrocompatibles

**Exemple :** v2.3.1

### Cherry-pick : Appliquer un commit spécifique

```bash
# Appliquer un commit d'une autre branche
git cherry-pick

# Cherry-pick sans créer de commit (permet de modifier)
git cherry-pick -n

# Cherry-pick plusieurs commits
git cherry-pick abc123 def456 ghi789
```

### Reflog : L'historique de vos actions Git

Le **reflog** enregistre tous les mouvements de HEAD. C'est votre filet de sécurité !

```bash
# Voir l'historique de HEAD
git reflog

# Résultat typique :
# abc1234 HEAD@{0}: commit: Add new feature
# def5678 HEAD@{1}: checkout: moving from main to feature
# ghi9012 HEAD@{2}: reset: moving to HEAD~1

# Revenir à un état précédent
git reset --hard HEAD@{2}

# Voir le reflog d'une branche spécifique
git reflog show main
```

#### Récupérer un commit perdu

Vous avez fait un `git reset --hard` par erreur ? Pas de panique !
Utilisez `git reflog` pour retrouver le hash du commit perdu,
puis `git reset --hard <hash>` pour y revenir.

### Git Worktree : Travailler sur plusieurs branches simultanément

**Git worktree** permet de créer plusieurs copies de votre dépôt,
chacune sur une branche différente. Utile pour tester rapidement une branche
sans perdre votre travail en cours !

```bash
# Créer un nouveau worktree pour tester une branche
git worktree add ../mon-projet-hotfix hotfix/urgent-bug

# Maintenant vous avez deux dossiers :
# ./mon-projet/        (branche main ou feature)
# ../mon-projet-hotfix/ (branche hotfix/urgent-bug)

# Lister tous les worktrees
git worktree list

# Travailler dans le nouveau worktree
cd ../mon-projet-hotfix
# Vous êtes automatiquement sur la branche hotfix/urgent-bug
git status

# Faire vos modifications et commits
echo "fix" >> bug.py
git commit -am "fix: Resolve urgent production bug"

# Retourner au worktree principal
cd ../mon-projet

# Supprimer un worktree quand vous avez fini
git worktree remove ../mon-projet-hotfix

# Ou supprimer de force (si non commité)
git worktree remove --force ../mon-projet-hotfix

# Nettoyer les worktrees obsolètes
git worktree prune
```

#### Cas d'usage de git worktree

- **Hotfix urgent** : Corriger un bug en prod sans perdre votre travail en cours
- **Code review** : Tester la branche d'un collègue sans changer votre branche actuelle
- **Tests parallèles** : Lancer des tests sur plusieurs branches simultanément
- **Comparaison** : Comparer visuellement deux branches côte à côte

#### Avantages de worktree vs stash

**Worktree :**

- ✅ Garder plusieurs branches actives en même temps
- ✅ Pas besoin de commiter ou stasher
- ✅ Voir le code de deux branches dans deux éditeurs

**Stash :**

- ✅ Plus rapide pour un changement temporaire
- ✅ Pas de dossier supplémentaire

#### ✅ Partie 6 terminée !

Vous maîtrisez maintenant les commandes avancées de Git ! Passez à la Partie 7 pour découvrir
les meilleures pratiques spécifiques au Data Engineering.

[🎯 Faire les exercices](../exercices.md)
[Partie 7 →](partie7.md)