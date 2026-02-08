# TD : Conception conceptuelle d'un Data Warehouse

## Informations

| Critère | Valeur |
|---------|--------|
| **Durée** | 2h30 |
| **Niveau** | Débutant-Intermédiaire |
| **Modalité** | Individuel ou binôme |
| **Prérequis** | [Module 01 - Introduction](../cours/01-introduction.md), [Module 03 - Modélisation](../cours/03-modelisation.md) |
| **Livrables** | Schéma étoile + schéma flocon + réponses aux questions |

## Objectifs

- Identifier les faits et les dimensions à partir d'un besoin métier
- Concevoir un schéma en étoile (Star Schema)
- Concevoir un schéma en flocon (Snowflake Schema)
- Choisir les mesures et leur type (additive, semi-additive, non-additive)
- Définir les clés surrogate et naturelles
- Anticiper les Slowly Changing Dimensions

---

## Contexte : CinéStar - Chaîne de cinémas

**CinéStar** est une chaîne de 25 cinémas répartis dans 10 villes françaises. La direction souhaite créer un Data Warehouse pour analyser les performances de l'entreprise.

### Système opérationnel existant (OLTP)

Le système de billetterie enregistre les données suivantes :

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   CINEMA     │     │   SALLE      │     │   SEANCE     │
├──────────────┤     ├──────────────┤     ├──────────────┤
│ cinema_id    │◄────│ cinema_id    │◄────│ salle_id     │
│ nom          │     │ salle_id     │     │ seance_id    │
│ adresse      │     │ nom_salle    │     │ film_id      │
│ ville        │     │ nb_places    │     │ date_heure   │
│ region       │     │ type (IMAX,  │     │ tarif_base   │
│ directeur    │     │  3D, standard│     │              │
└──────────────┘     └──────────────┘     └──────┬───────┘
                                                  │
┌──────────────┐     ┌──────────────┐     ┌──────▼───────┐
│   FILM       │     │   CLIENT     │     │   BILLET     │
├──────────────┤     ├──────────────┤     ├──────────────┤
│ film_id      │     │ client_id    │     │ billet_id    │
│ titre        │     │ nom          │     │ seance_id    │
│ realisateur  │     │ prenom       │     │ client_id    │
│ genre        │     │ email        │     │ type_tarif   │
│ duree_min    │     │ date_naiss   │     │ (plein/réduit│
│ pays_origine │     │ ville        │     │  étudiant/   │
│ distributeur │     │ date_inscr   │     │  senior)     │
│ date_sortie  │     │ carte_fid    │     │ prix_paye    │
│ budget       │     │ (oui/non)    │     │ date_achat   │
│ classification│    └──────────────┘     │ canal_achat  │
│ (TP/-12/-16) │                          │ (guichet/    │
└──────────────┘                          │  web/appli)  │
                                          └──────────────┘
```

### Données volumétriques

- 25 cinémas, 150 salles au total
- ~500 films projetés par an
- ~2 000 séances par jour (toute la chaîne)
- ~15 000 billets vendus par jour
- Historique souhaité : 3 ans
- ~16 millions de billets sur 3 ans

### Questions business de la direction

La direction veut pouvoir répondre à ces questions :

1. Quel est le **chiffre d'affaires** par cinéma, par mois ?
2. Quel est le **taux de remplissage** moyen par salle, par cinéma ?
3. Quels **films** génèrent le plus de revenus ?
4. Quelle est la répartition des **types de tarifs** (plein, réduit, étudiant) ?
5. Quel est l'impact du **canal d'achat** (guichet, web, appli) sur le CA ?
6. Quels sont les **créneaux horaires** les plus rentables ?
7. Comment évolue la **fréquentation** d'un mois sur l'autre ?
8. Quel est le **panier moyen** par segment client (carte fidélité ou non) ?

---

## Partie 1 : Identifier faits et dimensions (30 min)

### Exercice 1.1 : Identifier le processus métier

> Quel est le **processus métier principal** à modéliser ? Quel est l'événement mesurable ?

Répondez :
- Le grain (niveau de détail le plus fin) : _______________
- L'événement qui crée un fait : _______________

### Exercice 1.2 : Identifier les mesures

Listez toutes les mesures (métriques quantitatives) pertinentes et classez-les :

| Mesure | Type (additive / semi-additive / non-additive) | Agrégation possible |
|--------|------------------------------------------------|---------------------|
| | | |
| | | |
| | | |
| | | |
| | | |

**Indice :** Pensez au prix payé, au nombre de billets, au nombre de places, au taux de remplissage...

### Exercice 1.3 : Identifier les dimensions

Pour chaque question de la direction, identifiez la ou les dimensions nécessaires :

| Question business | Dimensions nécessaires |
|-------------------|----------------------|
| CA par cinéma, par mois | |
| Taux de remplissage par salle | |
| Films les plus rentables | |
| Répartition types de tarifs | |
| Impact du canal d'achat | |
| Créneaux horaires rentables | |
| Évolution fréquentation | |
| Panier moyen par segment | |

**Synthèse :** Listez toutes les dimensions uniques identifiées :
1. _______________
2. _______________
3. _______________
4. _______________
5. _______________
6. _______________

---

## Partie 2 : Schéma en étoile (45 min)

### Exercice 2.1 : Concevoir la table de faits

Dessinez la table de faits `FACT_BILLETTERIE` avec :
- Les clés étrangères (FK) vers chaque dimension
- Les mesures identifiées en 1.2
- Les colonnes de degenerate dimensions (si applicable)

```
┌────────────────────────────────────────┐
│         FACT_BILLETTERIE               │
├────────────────────────────────────────┤
│                                        │
│  (Complétez les FK)                    │
│  _________________ FK                  │
│  _________________ FK                  │
│  _________________ FK                  │
│  _________________ FK                  │
│  _________________ FK                  │
│  _________________ FK                  │
│                                        │
│  (Complétez les mesures)               │
│  _________________                     │
│  _________________                     │
│  _________________                     │
│  _________________                     │
│                                        │
└────────────────────────────────────────┘
```

### Exercice 2.2 : Concevoir les dimensions

Pour chaque dimension, définissez les attributs. Pensez aux **hiérarchies** implicites.

**DIM_DATE** (pré-remplie comme guide) :

```
┌────────────────────────────────────────┐
│            DIM_DATE                     │
├────────────────────────────────────────┤
│ date_key         (PK, surrogate)       │
│ date             (natural key)         │
│ jour                                   │
│ jour_semaine     (Lundi, Mardi...)     │
│ est_weekend      (oui/non)             │
│ semaine                                │
│ mois                                   │
│ nom_mois                               │
│ trimestre                              │
│ annee                                  │
│ est_vacances_scolaires                 │
│ est_jour_ferie                         │
└────────────────────────────────────────┘
Hiérarchie : Jour → Semaine → Mois → Trimestre → Année
```

**A vous de concevoir :**

- `DIM_CINEMA` (inclure la hiérarchie géographique)
- `DIM_FILM` (inclure genre, classification, pays)
- `DIM_CLIENT` (inclure segment fidélité)
- `DIM_TARIF` (ou DIM_TYPE_BILLET)
- `DIM_HEURE` (si vous séparez date et heure)

### Exercice 2.3 : Dessiner le schéma étoile complet

Dessinez le schéma en étoile complet avec toutes les dimensions autour de la table de faits. Indiquez les clés (PK, FK) et les cardinalités.

```
                         ┌─────────────────┐
                         │    DIM_DATE     │
                         └────────┬────────┘
                                  │
┌─────────────────┐      ┌────────▼────────┐      ┌─────────────────┐
│   DIM_????      │      │  FACT_BILLET-   │      │   DIM_????      │
│                 │◄─────│  TERIE          │─────►│                 │
└─────────────────┘      └────────┬────────┘      └─────────────────┘
                                  │
                         ┌────────▼────────┐
                         │   DIM_????      │
                         └─────────────────┘

(Complétez avec toutes vos dimensions)
```

---

## Partie 3 : Schéma en flocon (30 min)

### Exercice 3.1 : Normaliser les dimensions

Transformez votre schéma étoile en schéma flocon en normalisant les dimensions qui contiennent des **hiérarchies**.

**Exemple de normalisation :**

```
Star Schema (dénormalisé) :          Snowflake (normalisé) :

┌─────────────────┐                 ┌──────────────┐
│   DIM_CINEMA    │                 │  DIM_REGION  │
├─────────────────┤                 ├──────────────┤
│ cinema_key      │                 │ region_key   │◄─────┐
│ nom             │                 │ nom_region   │      │
│ ville           │        ──►     └──────────────┘      │
│ region          │                                       │
│ directeur       │                 ┌──────────────┐      │
└─────────────────┘                 │  DIM_VILLE   │      │
                                    ├──────────────┤      │
                                    │ ville_key    │◄──┐  │
                                    │ nom_ville    │   │  │
                                    │ region_key FK│───┘  │
                                    └──────────────┘   │
                                                       │
                                    ┌──────────────────┤
                                    │   DIM_CINEMA     │
                                    ├──────────────────┤
                                    │ cinema_key       │
                                    │ nom              │
                                    │ ville_key FK     │
                                    │ directeur        │
                                    └──────────────────┘
```

**A vous :** Normalisez au moins 2 dimensions de votre schéma :

1. `DIM_CINEMA` → séparer Ville et Région
2. `DIM_FILM` → séparer Genre, Distributeur, Pays

### Exercice 3.2 : Comparaison Star vs Snowflake

Répondez aux questions :

1. Combien de **JOINs** faut-il pour obtenir le CA par région dans le schéma étoile ? Et dans le flocon ?
2. Quelle approche recommanderiez-vous pour CinéStar ? Pourquoi ?
3. Dans quel cas le flocon serait-il préférable ?

---

## Partie 4 : SCD et questions avancées (30 min)

### Exercice 4.1 : Identifier les SCD

Pour chaque dimension, identifiez quels attributs sont susceptibles de changer et quel type de SCD appliquer :

| Dimension | Attribut qui change | Type SCD | Justification |
|-----------|-------------------|----------|---------------|
| DIM_CLIENT | ville | ? | |
| DIM_CLIENT | carte_fidelite | ? | |
| DIM_CINEMA | directeur | ? | |
| DIM_FILM | classification | ? | |

### Exercice 4.2 : Implémenter un SCD Type 2

Montrez comment évolue la table `DIM_CLIENT` quand le client "Martin Dupont" (client_id = C001) :
- S'inscrit le 2024-01-15 à Paris, sans carte fidélité
- Déménage à Lyon le 2024-06-01
- Prend la carte fidélité le 2024-09-15

Remplissez le tableau :

| customer_key | customer_id | nom | ville | carte_fid | valid_from | valid_to | is_current |
|--------------|-------------|-----|-------|-----------|------------|----------|------------|
| | | | | | | | |
| | | | | | | | |
| | | | | | | | |

### Exercice 4.3 : Grain de la table de faits

Répondez :
1. Pourquoi est-il important de définir le grain **avant** de concevoir les dimensions ?
2. Si on choisit le grain "1 ligne = 1 billet vendu", peut-on répondre à la question du taux de remplissage ? Sinon, quelle solution proposez-vous ?
3. Faut-il créer une deuxième table de faits ? Si oui, laquelle ?

---

## Partie 5 : Estimation volumétrique (15 min)

### Exercice 5.1 : Calculer le volume

Estimez le volume de votre Data Warehouse :

| Table | Nb lignes (3 ans) | Nb colonnes | Taille estimée par ligne | Volume total estimé |
|-------|-------------------|-------------|--------------------------|---------------------|
| FACT_BILLETTERIE | ~16M | | | |
| DIM_DATE | | | | |
| DIM_CINEMA | | | | |
| DIM_FILM | | | | |
| DIM_CLIENT | | | | |
| **TOTAL** | | | | |

**Questions :**
1. Ce volume est-il adapté à PostgreSQL ? A BigQuery ?
2. Quel partitionnement recommanderiez-vous pour la table de faits ?

---

## Livrables attendus

1. **Schéma en étoile** complet (dessiné ou diagramme) avec tous les attributs
2. **Schéma en flocon** avec au moins 2 dimensions normalisées
3. **Tableau des mesures** classées par type (additive, semi-additive, non-additive)
4. **Tableau des SCD** avec justification des choix
5. **Réponses** aux questions des exercices 3.2, 4.3 et 5.1

---

## Pour aller plus loin

- Comparez votre schéma avec celui d'un camarade : quelles différences ? Pourquoi ?
- Comment adapteriez-vous le modèle si CinéStar ouvre des cinémas à l'étranger ?
- Quelle dimension ajouteriez-vous pour analyser les ventes de confiserie au bar ?

---

[Retour au sommaire](../cours/README.md)
