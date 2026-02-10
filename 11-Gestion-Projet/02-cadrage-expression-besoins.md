[← Precedent](01-introduction-projet-data.md) | [🏠 Accueil](README.md) | [Suivant →](03-methodes-agiles.md)

# Lecon 2 - Cadrage et Expression de Besoins

## 🎯 Objectifs

- Comprendre pourquoi le cadrage est la phase la plus critique d'un projet data
- Maitriser les techniques d'entretien pour recueillir les besoins metier
- Rediger un cahier des charges fonctionnel structure
- Ecrire des User Stories avec des criteres d'acceptation au format Given/When/Then
- Definir une Definition of Done adaptee aux projets data

---

## 1. La Phase de Cadrage : Pourquoi c'est Critique

### 1.1 Le cout d'un mauvais cadrage

Le principe "Garbage In, Garbage Out" s'applique aussi aux besoins. Un besoin mal exprime ou mal compris genere :
- Du developpement inutile (fonctionnalites non utilisees)
- Des retards (retour en arriere pour reclarifier)
- De la frustration (equipe technique vs equipe metier)
- Du gaspillage budgetaire (jusqu'a 50% du budget projet dans les cas extremes)

### 1.2 Cout de correction d'une erreur selon la phase

| Phase de decouverte de l'erreur | Cout relatif de correction |
|--------------------------------|:------------------------:|
| Cadrage | x1 |
| Exploration | x5 |
| Developpement | x10 |
| Deploiement | x50 |
| Production | x100 |

💡 **Astuce** : Investir 2 semaines supplementaires dans le cadrage peut economiser 2 mois de developpement. C'est le meilleur investissement possible sur un projet data.

### 1.3 Les livrables de la phase de cadrage

1. **Compte-rendu des entretiens** avec les parties prenantes
2. **Cartographie des parties prenantes** (stakeholder map)
3. **Cahier des charges fonctionnel** (expression de besoins)
4. **User Stories** avec criteres d'acceptation
5. **Backlog initial** priorise
6. **Evaluation de faisabilite** (technique et financiere)
7. **Decision Go/No-Go** documentee

---

## 2. Audit des Besoins Metiers

### 2.1 Cartographie des parties prenantes (Stakeholder Mapping)

Avant de mener des entretiens, il faut identifier **qui** interviewer et dans **quel ordre**.

```
                    INFLUENCE ELEVEE
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        │   SATISFAIRE   │    GERER DE    │
        │   (Sponsor,    │    PRES        │
        │    Direction)   │   (PO, Metier  │
        │                │    principal)   │
 INTERET├────────────────┼────────────────┤ INTERET
 FAIBLE │                │                │  ELEVE
        │   SURVEILLER   │   INFORMER     │
        │   (Equipes     │   (Utilisateurs│
        │    peripheriques)│   finaux)     │
        │                │                │
        └────────────────┼────────────────┘
                         │
                    INFLUENCE FAIBLE
```

**Ordre recommande pour les entretiens** :

1. **Sponsor / Commanditaire** : comprendre la vision strategique et les contraintes budgetaires
2. **Product Owner / Responsable metier** : comprendre les besoins fonctionnels detailles
3. **Utilisateurs finaux** : comprendre les usages concrets et les irritants
4. **Equipe technique existante** : comprendre l'existant, les contraintes techniques
5. **DPO** : comprendre les contraintes reglementaires (RGPD)

### 2.2 Techniques d'entretien

#### Les 4 regles d'or de l'entretien

1. **Questions ouvertes d'abord** : "Decrivez-moi votre processus actuel" plutot que "Utilisez-vous Excel ?"
2. **Reformulation systematique** : "Si je comprends bien, vous avez besoin de... C'est correct ?"
3. **Exploration des cas limites** : "Que se passe-t-il quand la donnee est manquante ?"
4. **Ne jamais proposer de solution technique** pendant l'entretien : le but est de comprendre le besoin, pas de le resoudre

#### Les pieges a eviter

❌ **Question orientee** : "Vous trouvez aussi que le systeme actuel est lent, n'est-ce pas ?"
✅ **Question neutre** : "Comment evaluez-vous la performance du systeme actuel ?"

❌ **Question fermee prematuree** : "Avez-vous besoin d'un dashboard ?"
✅ **Question ouverte** : "Comment suivez-vous vos indicateurs aujourd'hui ?"

❌ **Jargon technique** : "On va mettre un Kafka pour le streaming des events"
✅ **Langage metier** : "Les donnees seront disponibles en temps reel"

### 2.3 Grille d'entretien - Template pour un projet data

Voici un template de 15 questions a adapter selon le contexte :

#### Bloc 1 : Contexte et objectifs (5 questions)

| # | Question | Objectif |
|---|----------|----------|
| 1 | Pouvez-vous me decrire votre role et vos responsabilites ? | Comprendre le profil de l'interlocuteur |
| 2 | Quel est le probleme ou l'opportunite que ce projet doit adresser ? | Identifier le "pourquoi" du projet |
| 3 | Comment mesurez-vous le succes aujourd'hui ? Quels KPIs suivez-vous ? | Identifier les metriques de succes |
| 4 | A quoi ressemblerait la solution ideale pour vous ? | Comprendre la vision cible |
| 5 | Quelles sont les contraintes (budget, delai, reglementaire) dont je dois tenir compte ? | Cadrer les contraintes |

#### Bloc 2 : Donnees et processus actuels (5 questions)

| # | Question | Objectif |
|---|----------|----------|
| 6 | D'ou viennent les donnees que vous utilisez aujourd'hui ? | Identifier les sources |
| 7 | Comment accedez-vous a ces donnees ? (outils, frequence, format) | Comprendre l'existant technique |
| 8 | Quels sont les problemes de qualite que vous rencontrez ? | Identifier les irritants data |
| 9 | Combien de temps passez-vous a preparer / nettoyer les donnees manuellement ? | Quantifier la douleur |
| 10 | Qui d'autre utilise ces memes donnees dans l'organisation ? | Identifier les dependances |

#### Bloc 3 : Besoins et priorites (5 questions)

| # | Question | Objectif |
|---|----------|----------|
| 11 | Quelles sont les 3 informations les plus critiques pour votre activite ? | Prioriser les besoins |
| 12 | A quelle frequence avez-vous besoin de ces donnees ? (temps reel, quotidien, hebdomadaire) | Definir les SLA |
| 13 | Qui seront les utilisateurs de la solution ? Combien sont-ils ? | Dimensionner la solution |
| 14 | Que se passe-t-il si les donnees sont indisponibles pendant 1 heure / 1 jour ? | Evaluer la criticite |
| 15 | Y a-t-il des donnees sensibles ou personnelles impliquees ? | Identifier les enjeux RGPD |

💡 **Astuce** : Enregistrez les entretiens (avec accord) et prenez des notes structurees. Un entretien de 45 minutes peut generer 3-4 pages de notes exploitables.

---

## 3. Expression de Besoins

### 3.1 Cahier des Charges Fonctionnel - Structure

Le cahier des charges fonctionnel (CDCF) est le document de reference qui formalise les besoins. Voici sa structure recommandee pour un projet data :

```
CAHIER DES CHARGES FONCTIONNEL
==============================

1. CONTEXTE ET OBJECTIFS
   1.1 Contexte du projet
   1.2 Problematique metier
   1.3 Objectifs du projet (SMART)
   1.4 Perimetre (in scope / out of scope)
   1.5 Parties prenantes

2. BESOINS FONCTIONNELS
   2.1 User Stories par epic
   2.2 Criteres d'acceptation
   2.3 Maquettes / wireframes (si dashboard)
   2.4 Regles metier

3. BESOINS NON-FONCTIONNELS
   3.1 Performance (SLA, latence, debit)
   3.2 Volumetrie (donnees actuelles et projection)
   3.3 Disponibilite (uptime cible)
   3.4 Securite et conformite (RGPD, chiffrement)
   3.5 Accessibilite (RGAA)

4. DONNEES
   4.1 Sources de donnees identifiees
   4.2 Description des jeux de donnees
   4.3 Qualite actuelle des donnees
   4.4 Transformations attendues

5. CONTRAINTES
   5.1 Budget
   5.2 Delais
   5.3 Contraintes techniques (stack existante, integration)
   5.4 Contraintes reglementaires

6. CRITERES DE SUCCES
   6.1 KPIs de succes du projet
   6.2 Definition of Done

7. ANNEXES
   7.1 Comptes-rendus des entretiens
   7.2 Glossaire metier
   7.3 References et documents existants
```

### 3.2 User Stories - Le Format Standard

#### Format

```
En tant que [role],
je veux [action/fonctionnalite],
afin de [benefice/valeur metier].
```

#### Regles d'ecriture (INVEST)

| Lettre | Critere | Description |
|--------|---------|-------------|
| **I** | Independent | La story peut etre developpee independamment |
| **N** | Negotiable | Les details peuvent etre discutes |
| **V** | Valuable | Elle apporte de la valeur au metier |
| **E** | Estimable | L'equipe peut l'estimer en effort |
| **S** | Small | Elle tient dans un sprint |
| **T** | Testable | On peut verifier qu'elle est "done" |

### 3.3 Criteres d'Acceptation - Format Given/When/Then

Les criteres d'acceptation definissent **quand** une User Story est consideree comme terminee. Le format Given/When/Then (ou Etant donne/Quand/Alors en francais) est le plus repandu :

```
Etant donne [un contexte initial],
Quand [une action se produit],
Alors [un resultat attendu].
```

### 3.4 Exemple Complet : 5 User Stories pour un Dashboard de Ventes

#### Contexte
Une entreprise de e-commerce souhaite un dashboard de suivi des ventes en temps quasi-reel pour son equipe commerciale.

---

**User Story 1 : Vue globale du chiffre d'affaires**

```
En tant que Directeur Commercial,
je veux voir le chiffre d'affaires en temps reel sur un dashboard,
afin de suivre la performance commerciale sans attendre les rapports mensuels.
```

**Criteres d'acceptation :**

```
CA-1.1 : Etant donne que je suis connecte au dashboard,
         Quand la page se charge,
         Alors je vois le CA du jour, de la semaine et du mois en cours,
         avec la comparaison N-1 en pourcentage.

CA-1.2 : Etant donne qu'une nouvelle commande est validee,
         Quand le pipeline rafraichit les donnees (toutes les 15 minutes),
         Alors le CA affiche est mis a jour automatiquement.

CA-1.3 : Etant donne que le CA du jour depasse l'objectif,
         Quand le seuil de 100% est atteint,
         Alors l'indicateur passe en vert avec un icone de validation.
```

---

**User Story 2 : Analyse par categorie de produit**

```
En tant que Responsable Marketing,
je veux pouvoir filtrer les ventes par categorie de produit,
afin d'identifier les categories les plus performantes et ajuster mes campagnes.
```

**Criteres d'acceptation :**

```
CA-2.1 : Etant donne que je suis sur le dashboard,
         Quand je selectionne une categorie dans le filtre deroulant,
         Alors tous les graphiques se mettent a jour pour cette categorie.

CA-2.2 : Etant donne que je selectionne "Toutes les categories",
         Quand le filtre est applique,
         Alors je vois un graphique en barres avec le classement des categories par CA.

CA-2.3 : Etant donne que les donnees d'une categorie sont manquantes,
         Quand le dashboard charge,
         Alors un message "Donnees indisponibles" s'affiche au lieu d'un graphique vide.
```

---

**User Story 3 : Alerte sur les anomalies de ventes**

```
En tant que Directeur Commercial,
je veux recevoir une alerte quand les ventes chutent de plus de 20% par rapport a la moyenne,
afin de reagir rapidement a un probleme potentiel.
```

**Criteres d'acceptation :**

```
CA-3.1 : Etant donne que la moyenne des ventes horaires est calculee sur les 30 derniers jours,
         Quand les ventes de l'heure en cours sont inferieures a 80% de cette moyenne,
         Alors une alerte email est envoyee au Directeur Commercial.

CA-3.2 : Etant donne qu'une alerte a ete envoyee,
         Quand les ventes reviennent au-dessus du seuil,
         Alors une notification de retour a la normale est envoyee.

CA-3.3 : Etant donne que nous sommes un dimanche ou un jour ferie,
         Quand les ventes sont faibles,
         Alors aucune alerte n'est declenchee (jours exclus de la surveillance).
```

---

**User Story 4 : Export des donnees**

```
En tant qu'Analyste Commercial,
je veux pouvoir exporter les donnees du dashboard en CSV et Excel,
afin de realiser des analyses complementaires dans mes propres outils.
```

**Criteres d'acceptation :**

```
CA-4.1 : Etant donne que je visualise un tableau de donnees,
         Quand je clique sur le bouton "Exporter",
         Alors je peux choisir entre CSV et Excel comme format de sortie.

CA-4.2 : Etant donne que les filtres actifs limitent les donnees affichees,
         Quand j'exporte,
         Alors seules les donnees filtrees sont exportees.

CA-4.3 : Etant donne que le jeu de donnees depasse 100 000 lignes,
         Quand j'exporte,
         Alors un message m'informe que l'export peut prendre quelques minutes
         et je recois le fichier par email.
```

---

**User Story 5 : Historique et tendances**

```
En tant que Directeur General,
je veux voir l'evolution des ventes sur les 12 derniers mois,
afin de valider la strategie commerciale et preparer les previsions budgetaires.
```

**Criteres d'acceptation :**

```
CA-5.1 : Etant donne que je suis sur la page "Tendances",
         Quand je selectionne une periode (3 mois, 6 mois, 12 mois),
         Alors un graphique en courbes affiche l'evolution du CA mensuel.

CA-5.2 : Etant donne que je survole un point du graphique,
         Quand le tooltip s'affiche,
         Alors je vois le CA exact, le nombre de commandes et le panier moyen du mois.

CA-5.3 : Etant donne que des mois n'ont pas de donnees completes,
         Quand le graphique est affiche,
         Alors les mois incomplets sont clairement identifies (couleur differente, mention "partiel").
```

---

## 4. Definition of Done (DoD) pour les Projets Data

### 4.1 Pourquoi une DoD specifique aux projets data ?

Dans un projet logiciel classique, la DoD peut se limiter a : "le code est merge, les tests passent, c'est deploye". Dans un projet data, il faut ajouter des criteres specifiques lies a la **qualite des donnees**, au **monitoring** et a la **documentation**.

### 4.2 Template de Definition of Done

#### DoD pour un Pipeline de Donnees

- [ ] Le code est revise (code review approuvee par au moins 1 pair)
- [ ] Les tests unitaires couvrent les transformations critiques (couverture > 80%)
- [ ] Les tests de qualite de donnees sont en place :
  - [ ] Tests de nullite sur les colonnes obligatoires
  - [ ] Tests d'unicite sur les cles primaires
  - [ ] Tests de coherence referentielle
  - [ ] Tests de plage de valeurs sur les colonnes numeriques
- [ ] Le pipeline est idempotent (re-execution sans duplication)
- [ ] Le monitoring et les alertes sont configures
- [ ] La documentation technique est a jour :
  - [ ] Description du pipeline (source, transformations, destination)
  - [ ] Schema des donnees (dictionnaire de donnees)
  - [ ] Instructions de deploiement et de rollback
- [ ] La conformite RGPD est validee (si donnees personnelles)
- [ ] Les performances sont acceptables (temps d'execution < SLA)
- [ ] Le pipeline est deploye sur l'environnement de staging et valide

#### DoD pour un Dashboard

- [ ] Tous les criteres ci-dessus pour les pipelines alimentant le dashboard
- [ ] Les visualisations sont validees par le Product Owner
- [ ] Les filtres et interactions fonctionnent correctement
- [ ] L'accessibilite est verifiee (contraste, navigation clavier)
- [ ] Les performances de chargement sont acceptables (< 5 secondes)
- [ ] La documentation utilisateur est redigee

#### DoD pour un Modele ML

- [ ] Tous les criteres ci-dessus pour les pipelines
- [ ] Les metriques du modele atteignent les seuils definis (accuracy, precision, recall, F1)
- [ ] Le modele est teste sur un jeu de donnees de validation independant
- [ ] Les biais potentiels sont documentes et evalues
- [ ] Le monitoring de drift est en place
- [ ] Le processus de retraining est documente
- [ ] Les predictions sont explicables (SHAP, LIME, ou equivalent)

### 4.3 Checklist visuelle

```
DEFINITION OF DONE - PROJET DATA
=================================

Code          [x] Code review
              [x] Tests unitaires > 80%
              [x] Linting / formatage

Donnees       [x] Tests de qualite
              [x] Schema documente
              [x] Lineage trace

Operations    [x] Monitoring / Alertes
              [x] Idempotence verifiee
              [x] Performance < SLA

Documentation [x] Documentation technique
              [x] Documentation utilisateur
              [x] Changelog a jour

Conformite    [x] RGPD valide
              [x] Accessibilite verifiee
              [x] Securite verifiee
```

---

## 5. Cas Pratique : Cadrage d'un Projet de Dashboard RH

### 5.1 Contexte

Une entreprise de 500 salaries souhaite un dashboard RH pour suivre l'absenteisme, le turnover et la satisfaction des employes.

### 5.2 Stakeholder Mapping

| Partie prenante | Influence | Interet | Strategie |
|----------------|:---------:|:-------:|-----------|
| DRH (Sponsor) | Elevee | Eleve | Gerer de pres : reunion hebdomadaire |
| Responsables d'equipe | Moyenne | Eleve | Informer regulierement |
| DSI | Elevee | Moyen | Satisfaire : valider l'architecture |
| DPO | Elevee | Moyen | Satisfaire : valider la conformite RGPD |
| Salaries (CSE) | Faible | Eleve | Informer : transparence sur les donnees utilisees |

### 5.3 Questions prioritaires pour l'entretien avec le DRH

1. Quels indicateurs suivez-vous aujourd'hui ? Comment ?
2. Quels sont les 3 indicateurs dont vous avez le plus besoin en temps reel ?
3. A qui le dashboard sera-t-il accessible ?
4. Quelles decisions prenez-vous sur la base de ces donnees ?
5. Quelles sont les sources de donnees RH actuelles (SIRH, pointeuse, enquetes) ?

---

## 6. Synthese

| Concept | Point cle |
|---------|-----------|
| Phase de cadrage | La plus critique : investir ici economise enormement en aval |
| Entretiens | Questions ouvertes, reformulation, pas de solution technique |
| Cahier des charges | Structure en 7 sections, adapte aux projets data |
| User Stories | Format "En tant que... je veux... afin de..." + criteres Given/When/Then |
| Definition of Done | Inclure tests de qualite de donnees, monitoring, documentation |

---

📝 **Exercice** : Choisissez un projet data fictif (dashboard de suivi logistique). Redigez 3 User Stories completes avec criteres d'acceptation au format Given/When/Then.

---

[← Precedent](01-introduction-projet-data.md) | [🏠 Accueil](README.md) | [Suivant →](03-methodes-agiles.md)

---

**Academy** - Formation Data Engineer
