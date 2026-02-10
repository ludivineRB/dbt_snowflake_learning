=============================================
    GIT QUEST - VOYAGE TEMPOREL
    "L'Histoire est ecrite par les vainqueurs...
     et versionnee par les developpeurs."
=============================================

CONTEXTE:
Le Dr. Daniel Jackson a decouvert les coordonnees
d'une arme Ancienne dans un ancien depot de fichiers
versionne. Mais l'historique a ete corrompu par les
Goa'uld et les informations sont eparpillees dans
les branches temporelles.

PREPARATION:
Executez le script d'initialisation:
  bash setup_git_quest.sh

Cela creera un depot Git "depot_ancien/" avec
un historique complexe. Entrez dedans:
  cd depot_ancien

MISSIONS:
=========

MISSION 1 - Explorer l'historique (git log)
  "Combien de commits existent dans ce depot?"
  Commandes utiles:
    git log --oneline
    git log --oneline | wc -l

MISSION 2 - Lire le passe (git show)
  "Le 3eme commit contient un indice. Lisez-le."
  Commandes utiles:
    git log --oneline  (notez le hash du 3eme commit)
    git show <hash>

MISSION 3 - Voir les changements (git diff)
  "Qu'est-ce qui a change entre le 1er et le dernier commit?"
  Commandes utiles:
    git diff <hash_ancien> <hash_recent>
    git diff HEAD~5 HEAD

MISSION 4 - Explorer les branches (git branch)
  "Il y a des branches cachees. Trouvez-les toutes."
  Commandes utiles:
    git branch -a
    git checkout <nom_branche>
    cat coordonnees.txt  (lire le fichier dans chaque branche)

MISSION 5 - Visualiser l'arbre (git log --graph)
  "Visualisez l'historique complet avec toutes les branches."
  Commande utile:
    git log --all --oneline --graph --decorate

MISSION 6 - Fusionner les timelines (git merge)
  "La branche 'fragments_anciens' contient une partie
   des coordonnees. Fusionnez-la dans main."
  Commandes utiles:
    git checkout main
    git merge fragments_anciens

  ATTENTION: il y aura un conflit de merge!
  Ouvrez le fichier en conflit, choisissez la bonne
  version (gardez LES DEUX parties), sauvegardez, puis:
    git add <fichier>
    git commit -m "Fusion des coordonnees"

MISSION FINALE:
  Quand vous avez fusionne avec succes, executez:
    bash verification.sh

Bonne chance, SG-nouveau. L'histoire vous attend.
=============================================
