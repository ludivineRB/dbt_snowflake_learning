================================================================================
         STARGATE COMMAND - DOCUMENT CLASSIFIE NIVEAU OMEGA
================================================================================

DE: General George Hammond
A: Tout le personnel autorise
OBJET: ENQUETE INTERNE - INFILTRATION SUSPECTEE
DATE: 16 Mars 2024
CLASSIFICATION: OMEGA - YEUX SEULEMENT

--------------------------------------------------------------------------------

A l'attention de l'enqueteur,

Une situation critique a ete detectee au sein du Stargate Command.

Au cours des trois dernieres semaines, nous avons releve des activites
non autorisees dans le complexe:

  - Activations de la Porte des Etoiles en dehors des creneaux planifies
  - Transmissions chiffrees vers des destinations inconnues
  - Acces a des zones restreintes pendant les heures de nuit
  - Modification suspecte de badges d'acces dans notre systeme

Tout indique qu'un espion du NID s'est infiltre parmi nous.

Votre mission: analyser les logs de securite, les fiches du personnel
et les preuves materielles pour identifier le traitre.

================================================================================
                         PROCEDURE D'ENQUETE
================================================================================

Suivez les 5 etapes dans le dossier analyse/ :

  Etape 1 - analyse/etape1_compter_acces.txt
    -> Comptez les acces nocturnes (grep, wc, sort, uniq)

  Etape 2 - analyse/etape2_reseau_suspect.txt
    -> Analysez les connexions reseau suspectes (grep, awk)

  Etape 3 - analyse/etape3_croiser_donnees.txt
    -> Croisez avec les fiches personnel (grep, awk sur CSV)

  Etape 4 - analyse/etape4_comparer_badges.txt
    -> Comparez les badges avec diff

  Etape 5 - analyse/etape5_conclusion.txt
    -> Assemblez les preuves et identifiez le traitre

Une fois le coupable identifie, rendez-vous dans resolution/ pour
le demasquer officiellement.

DOSSIERS DISPONIBLES:
  dossier_enquete/    - Rapport initial et liste du personnel
  logs_securite/      - Logs d'acces porte, labo et reseau
  fiches_personnel/   - Fiches detaillees par service
  preuves/            - Preuves materielles collectees
  analyse/            - Guide d'enquete en 5 etapes
  resolution/         - Script de resolution finale

Bonne chance. La securite de cette base en depend.

General Hammond
Commandant du SGC

================================================================================
       "DANS L'OMBRE, LA VERITE ATTEND D'ETRE DECOUVERTE"
================================================================================
