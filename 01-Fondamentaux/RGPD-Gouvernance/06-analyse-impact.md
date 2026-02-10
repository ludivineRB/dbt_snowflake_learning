[← Precedent](05-anonymisation-pseudonymisation.md) | [🏠 Accueil](README.md) | [Suivant →](07-securite-gouvernance.md)

# 📖 Cours 6 - Analyse d'Impact (DPIA / AIPD)

## Evaluer et attenuer les risques pour les droits et libertes des personnes

---

## 1. Qu'est-ce qu'une DPIA ?

### 1.1 Definition

La **DPIA** (Data Protection Impact Assessment), appelee en francais **AIPD** (Analyse d'Impact relative a la Protection des Donnees), est une evaluation systematique des risques qu'un traitement de donnees fait peser sur la vie privee des personnes concernees.

> **Article 35 RGPD** : Lorsqu'un type de traitement, en particulier par le recours a de nouvelles technologies, est susceptible d'engendrer un **risque eleve** pour les droits et libertes des personnes physiques, le responsable du traitement effectue, avant le traitement, une analyse de l'impact des operations de traitement envisagees sur la protection des donnees a caractere personnel.

### 1.2 Objectifs de la DPIA

```
┌──────────────────────────────────────────────────────────────────┐
│                  Objectifs de la DPIA                             │
│                                                                  │
│  1. DECRIRE le traitement envisage                              │
│     → Quoi, pourquoi, comment, combien de donnees ?             │
│                                                                  │
│  2. EVALUER la necessite et la proportionnalite                 │
│     → Est-ce vraiment necessaire ? Existe-t-il une alternative  │
│       moins intrusive ?                                         │
│                                                                  │
│  3. IDENTIFIER les risques pour les droits et libertes          │
│     → Quels sont les scenarios de risque ?                      │
│     → Quelle est la gravite et la probabilite ?                 │
│                                                                  │
│  4. DEFINIR les mesures d'attenuation                           │
│     → Comment reduire les risques a un niveau acceptable ?      │
│                                                                  │
│  5. DOCUMENTER pour prouver la conformite (accountability)      │
└──────────────────────────────────────────────────────────────────┘
```

---

## 2. Quand la DPIA est-elle Obligatoire ?

### 2.1 Criteres de l'Article 35

La DPIA est obligatoire quand le traitement est susceptible d'engendrer un **risque eleve**. Le Comite Europeen de la Protection des Donnees (CEPD) a defini 9 criteres. Si votre traitement remplit **au moins 2 criteres**, une DPIA est obligatoire.

| # | Critere | Exemple en Data Engineering |
|---|---------|----------------------------|
| 1 | **Evaluation/scoring** (y compris profilage) | Score de credit, prediction de churn, scoring RH |
| 2 | **Decision automatisee avec effet juridique** | Acceptation/refus automatique de pret, tri de CV |
| 3 | **Surveillance systematique** | Tracking comportemental sur un site, analyse de logs |
| 4 | **Donnees sensibles** a grande echelle | Traitement de donnees de sante, biometriques |
| 5 | **Donnees a grande echelle** | Big data, data lake avec millions d'enregistrements |
| 6 | **Croisement de jeux de donnees** | Enrichissement de profils, fusion de bases |
| 7 | **Personnes vulnerables** | Donnees de mineurs, patients, employes |
| 8 | **Usage innovant de technologies** | IA, reconnaissance faciale, IoT, blockchain |
| 9 | **Exclusion d'un droit/service** | Si le traitement peut empecher l'acces a un service |

### 2.2 Arbre de decision rapide

```
┌──────────────────────────────────────────────────────────────────┐
│            Dois-je faire une DPIA ?                              │
│                                                                  │
│  Le traitement figure-t-il dans la liste CNIL des               │
│  traitements necessitant une DPIA ?                             │
│         │                                                        │
│    ┌────┴────┐                                                  │
│   OUI      NON                                                  │
│    │         │                                                   │
│    ▼         │  Le traitement remplit-il au moins 2 des         │
│  DPIA       │  9 criteres du CEPD ?                            │
│  OBLIGATOIRE │         │                                        │
│              │    ┌────┴────┐                                   │
│              │   OUI      NON                                   │
│              │    │         │                                    │
│              │    ▼         │  Le traitement est-il dans la     │
│              │  DPIA       │  liste CNIL d'exemption ?         │
│              │  OBLIGATOIRE│         │                          │
│              │             │    ┌────┴────┐                     │
│              │             │   OUI      NON                     │
│              │             │    │         │                      │
│              │             │    ▼         ▼                      │
│              │             │  PAS DE   DPIA                     │
│              │             │  DPIA     RECOMMANDEE              │
│              │             │           (bonne pratique)         │
└──────────────────────────────────────────────────────────────────┘
```

### 2.3 Liste CNIL des traitements necessitant une DPIA (extraits)

| Traitement | Pourquoi |
|-----------|---------|
| Traitements de donnees de sante a grande echelle | Donnees sensibles + grande echelle |
| Profilage de personnes a des fins marketing | Evaluation + grande echelle |
| Traitements de donnees biometriques pour l'identification | Donnees sensibles + technologie innovante |
| Traitements utilisant des donnees de geolocalisation | Surveillance systematique |
| Traitements de donnees d'infractions | Donnees tres sensibles |
| Decisions automatisees produisant des effets juridiques | Decision auto + effet significatif |
| Traitements impliquant le croisement de donnees | Croisement + grande echelle |

---

## 3. Methodologie en 4 Etapes

### 3.1 Vue d'ensemble

```
┌──────────────────────────────────────────────────────────────────┐
│               4 Etapes de la DPIA                                │
│                                                                  │
│  ┌─────────────────────────────────┐                            │
│  │ ETAPE 1 : Description du        │                            │
│  │ traitement                       │                            │
│  │ Quoi ? Pourquoi ? Comment ?     │                            │
│  └───────────────┬─────────────────┘                            │
│                  │                                               │
│  ┌───────────────▼─────────────────┐                            │
│  │ ETAPE 2 : Evaluation de la      │                            │
│  │ necessite et proportionnalite   │                            │
│  │ Bases legales, droits, finalite │                            │
│  └───────────────┬─────────────────┘                            │
│                  │                                               │
│  ┌───────────────▼─────────────────┐                            │
│  │ ETAPE 3 : Evaluation des        │                            │
│  │ risques                         │                            │
│  │ Scenarios, gravite, probabilite │                            │
│  └───────────────┬─────────────────┘                            │
│                  │                                               │
│  ┌───────────────▼─────────────────┐                            │
│  │ ETAPE 4 : Mesures               │                            │
│  │ d'attenuation                   │                            │
│  │ Solutions techniques et org.    │                            │
│  └─────────────────────────────────┘                            │
└──────────────────────────────────────────────────────────────────┘
```

### 3.2 Etape 1 : Description du traitement

Questions a documenter :

| Question | Detail |
|----------|--------|
| **Quel traitement ?** | Description fonctionnelle et technique |
| **Quelles donnees ?** | Liste exhaustive des categories de donnees |
| **Qui est concerne ?** | Categories de personnes concernees |
| **Combien de personnes ?** | Volume estimatif |
| **Quelle finalite ?** | Objectif(s) du traitement |
| **Quelle base legale ?** | Consentement, contrat, interet legitime... |
| **Qui a acces ?** | Destinataires internes et externes |
| **Ou sont stockees les donnees ?** | Localisation, hebergement |
| **Combien de temps ?** | Duree de conservation |
| **Quels outils/technologies ?** | Stack technique utilisee |

### 3.3 Etape 2 : Evaluation de la necessite et proportionnalite

Verifier que :

✅ La finalite est **determinee, explicite et legitime**

✅ La base legale est **valide et documentee**

✅ Les donnees collectees sont **strictement necessaires** (minimisation)

✅ La duree de conservation est **justifiee et limitee**

✅ Les personnes sont **informees** de maniere complete

✅ Les droits des personnes sont **implementes** (acces, effacement, etc.)

✅ Les sous-traitants offrent des **garanties suffisantes**

✅ Il n'existe **pas d'alternative moins intrusive**

### 3.4 Etape 3 : Evaluation des risques

#### 3.4.1 Identification des evenements redoutes

Les 3 categories d'evenements redoutes :

| Evenement | Description | Exemples |
|-----------|-------------|----------|
| **Acces illegitime** | Donnees accessibles a des personnes non autorisees | Fuite de donnees, piratage, erreur d'acces |
| **Modification non desiree** | Donnees alterees de maniere non souhaitee | Corruption de base, modification malveillante |
| **Disparition** | Perte des donnees | Crash serveur, ransomware, suppression accidentelle |

#### 3.4.2 Matrice de risques (Probabilite x Gravite)

```
┌──────────────────────────────────────────────────────────────────┐
│              Matrice de Risques DPIA                              │
│                                                                  │
│  Gravite ▲                                                      │
│          │                                                       │
│  4 MAX   │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐  │
│          │  │ MODERE  │ │  ELEVE  │ │TRES ELEV│ │TRES ELEV│  │
│          │  │   (4)   │ │   (8)   │ │  (12)   │ │  (16)   │  │
│          │  └─────────┘ └─────────┘ └─────────┘ └─────────┘  │
│  3 IMPORT│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐  │
│          │  │ FAIBLE  │ │ MODERE  │ │  ELEVE  │ │TRES ELEV│  │
│          │  │   (3)   │ │   (6)   │ │   (9)   │ │  (12)   │  │
│          │  └─────────┘ └─────────┘ └─────────┘ └─────────┘  │
│  2 LIMITE│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐  │
│          │  │NEGLIGEAB│ │ FAIBLE  │ │ MODERE  │ │  ELEVE  │  │
│          │  │   (2)   │ │   (4)   │ │   (6)   │ │   (8)   │  │
│          │  └─────────┘ └─────────┘ └─────────┘ └─────────┘  │
│  1 NEGLIG│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐  │
│          │  │NEGLIGEAB│ │NEGLIGEAB│ │ FAIBLE  │ │ MODERE  │  │
│          │  │   (1)   │ │   (2)   │ │   (3)   │ │   (4)   │  │
│          │  └─────────┘ └─────────┘ └─────────┘ └─────────┘  │
│          │                                                       │
│          └──────────────────────────────────────────────────────►│
│            1 NEGLIG   2 LIMITE   3 IMPORT   4 MAXIMUM           │
│                         Probabilite                              │
│                                                                  │
│  Score = Gravite x Probabilite                                  │
│  1-3 : Risque acceptable (vert)                                 │
│  4-6 : Risque modere - mesures d'attenuation (jaune)           │
│  8-9 : Risque eleve - mesures obligatoires (orange)            │
│  12-16 : Risque tres eleve - consulter la CNIL (rouge)         │
└──────────────────────────────────────────────────────────────────┘
```

#### 3.4.3 Echelle de gravite

| Niveau | Description | Exemples d'impact |
|--------|-------------|-------------------|
| 1 - Negligeable | Desagrement sans consequence reelle | Recevoir un email non sollicite |
| 2 - Limitee | Desagrement significatif mais surmontable | Spam cible, publicite non desiree |
| 3 - Importante | Consequences serieuses | Discrimination, perte financiere, atteinte a la reputation |
| 4 - Maximale | Consequences irreversibles | Danger pour la vie, detention illegale, perte d'emploi |

#### 3.4.4 Echelle de probabilite

| Niveau | Description | Justification |
|--------|-------------|---------------|
| 1 - Negligeable | Tres peu probable | Mesures de securite robustes, pas de motivation d'attaque |
| 2 - Limitee | Peu probable mais possible | Mesures de securite standards, motivation faible |
| 3 - Importante | Probable | Donnees attractives, mesures perfectibles |
| 4 - Maximale | Tres probable | Donnees tres sensibles, mesures insuffisantes |

### 3.5 Etape 4 : Mesures d'attenuation

Pour chaque risque identifie, definir des mesures :

| Type de mesure | Exemples |
|---------------|----------|
| **Techniques** | Chiffrement, pseudonymisation, anonymisation, RBAC, MFA, backup |
| **Organisationnelles** | Formation, politique de securite, procedure d'incident, DPO |
| **Juridiques** | Contrats de sous-traitance, clauses de confidentialite, CGU |
| **Physiques** | Controle d'acces physique, video-surveillance des serveurs |

---

## 4. Exemple Complet : DPIA pour un Modele de Prediction du Churn

### 4.1 Contexte

L'entreprise e-commerce "ShopXYZ" souhaite deployer un modele de machine learning pour predire le depart des clients (churn) et declencher des actions de retention personnalisees.

### 4.2 Etape 1 : Description du traitement

| Element | Description |
|---------|-------------|
| **Nom du traitement** | Modele ML de prediction du churn client |
| **Responsable** | ShopXYZ SAS, representee par M. Dupont (DG) |
| **DPO** | Mme Martin (dpo@shopxyz.com) |
| **Finalite** | Predire la probabilite de depart des clients pour declencher des actions de retention personnalisees (offre promotionnelle, contact telephone, email de reactivation) |
| **Base legale** | Interet legitime (balance des interets documentee ci-dessous) |
| **Personnes concernees** | Clients actifs (derniere commande < 12 mois) : environ 500 000 personnes |
| **Donnees utilisees** | Anciennete, frequence d'achat, montant moyen, nombre de tickets support, score NPS, categorie de produits |
| **Donnees NON utilisees** | Nom, email, adresse, telephone, donnees de paiement (exclus du feature store) |
| **Destinataires** | Equipe Data Science (entrainement), Equipe CRM (scores), Equipe Marketing (actions) |
| **Sous-traitants** | OVH (hebergement, France), MLflow (tracking experiments, on-premise) |
| **Stockage** | Serveurs OVH Roubaix (France), feature store PostgreSQL chiffre |
| **Conservation** | Donnees d'entrainement : 24 mois glissants. Scores : 6 mois. Modeles : 12 mois |
| **Technologies** | Python, scikit-learn, PostgreSQL, Airflow, MLflow |

**Balance des interets (interet legitime) :**

| Critere | Evaluation |
|---------|-----------|
| **Interet de l'entreprise** | Reduire le churn de 15% a 10% represente environ 2M€/an de CA preserve |
| **Necessite** | Le modele predictif est le moyen le plus efficace pour cibler les actions de retention |
| **Alternative moins intrusive** | Pas d'alternative equivalente ; les campagnes generiques sont 3x moins efficaces |
| **Attentes des personnes** | Les clients peuvent raisonnablement s'attendre a ce que leur historique d'achat soit utilise pour leur proposer des offres |
| **Impact sur les personnes** | Impact positif (offres avantageuses) ; aucune decision negative (pas d'exclusion de service) |
| **Garanties** | Pseudonymisation, minimisation, droit d'opposition, intervention humaine |

### 4.3 Etape 2 : Necessite et proportionnalite

| Critere | Evaluation | Conforme ? |
|---------|-----------|------------|
| Finalite determinee et explicite | Prediction du churn pour la retention client | ✅ |
| Base legale valide | Interet legitime (balance documentee) | ✅ |
| Minimisation des donnees | Pas de donnees directement identifiantes dans le modele | ✅ |
| Duree de conservation limitee | 24 mois (donnees), 6 mois (scores), 12 mois (modeles) | ✅ |
| Information des personnes | Mention dans la politique de confidentialite | ✅ |
| Droit d'acces | API de consultation du score (via service client) | ✅ |
| Droit d'opposition | Formulaire en ligne + service client | ✅ |
| Droit a l'explication | SHAP values pour chaque prediction | ✅ |
| Intervention humaine | Actions de retention validees par l'equipe CRM | ✅ |
| Pas d'alternative moins intrusive | Campagnes generiques 3x moins efficaces | ✅ |

### 4.4 Etape 3 : Evaluation des risques

| # | Evenement redoute | Gravite | Probabilite | Score | Niveau |
|---|-------------------|---------|-------------|-------|--------|
| R1 | Fuite du feature store (acces illegitime aux donnees pseudonymisees) | 2 - Limitee | 2 - Limitee | 4 | Modere |
| R2 | Re-identification par croisement avec la base CRM | 3 - Importante | 2 - Limitee | 6 | Modere |
| R3 | Biais discriminatoire dans le modele (exclusion d'un segment) | 3 - Importante | 2 - Limitee | 6 | Modere |
| R4 | Utilisation detournee des scores de churn (ex: licenciement de commerciaux) | 3 - Importante | 1 - Negligeable | 3 | Faible |
| R5 | Perte des donnees d'entrainement (disparition) | 2 - Limitee | 1 - Negligeable | 2 | Negligeable |
| R6 | Modification malveillante du modele (model poisoning) | 3 - Importante | 1 - Negligeable | 3 | Faible |
| R7 | Decision automatisee sans recours (action de retention inadaptee) | 2 - Limitee | 3 - Importante | 6 | Modere |

### 4.5 Etape 4 : Mesures d'attenuation

| Risque | Mesures d'attenuation | Score apres mesures |
|--------|----------------------|---------------------|
| **R1** Fuite du feature store | - Chiffrement AES-256 au repos - Acces restreint par RBAC (equipe Data Science uniquement) - Journalisation de tous les acces - MFA obligatoire | 4 → **2** |
| **R2** Re-identification | - Separation physique feature store / base CRM - Pseudonymisation irreversible (hash sans acces au sel cote ML) - Controle d'acces differencie | 6 → **3** |
| **R3** Biais discriminatoire | - Audit de biais trimestriel (par genre, age, region) - Test de fairness (equalized odds) avant chaque deploiement - Monitoring continu des predictions par segment | 6 → **3** |
| **R4** Utilisation detournee | - Politique d'usage documentee et signee - Formation des equipes CRM et Marketing - Acces aux scores restreint aux use cases valides | 3 → **2** |
| **R5** Perte de donnees | - Backups quotidiens chiffres (retention 30j) - Replication multi-zone - Procedure de restauration testee trimestriellement | 2 → **1** |
| **R6** Model poisoning | - Versionning des modeles (MLflow) - Validation automatisee avant deploiement (tests de performance) - Acces en ecriture restreint au pipeline CI/CD | 3 → **1** |
| **R7** Decision sans recours | - Intervention humaine obligatoire avant action de retention > 100€ - Mecanisme de contestation (formulaire en ligne) - Explication de la prediction fournie au client sur demande | 6 → **2** |

### 4.6 Conclusion de la DPIA

```
┌──────────────────────────────────────────────────────────────────┐
│              Synthese de la DPIA - Modele Churn                  │
│                                                                  │
│  Niveau de risque residuel : ACCEPTABLE                         │
│                                                                  │
│  Tous les risques identifies ont ete ramenes a un niveau        │
│  acceptable (score <= 3) grace aux mesures d'attenuation.       │
│                                                                  │
│  ✅ Pas de consultation prealable de la CNIL necessaire         │
│                                                                  │
│  Actions de suivi :                                             │
│  - Revue de la DPIA dans 12 mois ou en cas de changement       │
│    significatif du traitement                                   │
│  - Audit de biais trimestriel                                  │
│  - Monitoring continu des acces et des predictions              │
│                                                                  │
│  Validation :                                                   │
│  - DPO : Mme Martin - Date : 01/03/2024                       │
│  - Responsable Data : M. Garcia - Date : 01/03/2024           │
│  - Direction Generale : M. Dupont - Date : 05/03/2024         │
└──────────────────────────────────────────────────────────────────┘
```

---

## 5. Outils et Ressources de la CNIL

### 5.1 Outil PIA de la CNIL

La CNIL met a disposition un **logiciel gratuit et open-source** pour realiser vos DPIA :

| Caracteristique | Detail |
|----------------|--------|
| **Nom** | PIA (Privacy Impact Assessment) |
| **Telechargement** | https://www.cnil.fr/fr/outil-pia-telechargez-et-installez-le-logiciel-de-la-cnil |
| **Formats** | Application desktop (Windows, macOS, Linux) + version web |
| **Open source** | Oui (GitHub) |
| **Fonctionnalites** | Guide pas a pas, modeles pre-remplis, export PDF, partage |

### 5.2 Guides de la CNIL

| Ressource | URL |
|-----------|-----|
| Guide DPIA de la CNIL | https://www.cnil.fr/fr/DPIA-analyse-impact-protection-des-donnees |
| Liste des traitements necessitant une DPIA | https://www.cnil.fr/fr/liste-des-traitements-pour-lesquels-une-analyse-dimpact-est-requise |
| Referentiels sectoriels | https://www.cnil.fr/fr/les-referentiels |
| FAQ DPIA | https://www.cnil.fr/fr/ce-quil-faut-savoir-sur-lanalyse-dimpact-relative-la-protection-des-donnees-aipd |

### 5.3 Quand consulter la CNIL ?

Si apres la DPIA, le risque residuel reste **eleve** (score >= 8 apres mesures d'attenuation), vous devez consulter la CNIL **avant** de mettre en oeuvre le traitement.

La CNIL dispose de 8 semaines pour rendre son avis (extensible a 6 semaines supplementaires).

---

## 6. Integrer la DPIA dans le Cycle de Vie des Projets Data

### 6.1 Quand realiser la DPIA dans le projet

```
┌──────────────────────────────────────────────────────────────────┐
│       Integration de la DPIA dans le cycle projet               │
│                                                                  │
│  Phase de cadrage           Phase de dev        Phase de prod   │
│  ┌──────────────┐          ┌──────────┐        ┌──────────┐   │
│  │ Expression   │          │ Develop- │        │ Deploy-  │   │
│  │ du besoin    │          │ pement   │        │ ment     │   │
│  └──────┬───────┘          └────┬─────┘        └────┬─────┘   │
│         │                       │                     │         │
│         ▼                       ▼                     ▼         │
│  ┌──────────────┐          ┌──────────┐        ┌──────────┐   │
│  │ DPIA initiale│          │ DPIA     │        │ Monitoring│   │
│  │ (pre-check)  │          │ complete │        │ continu  │   │
│  │              │          │          │        │          │   │
│  │ Faut-il une  │          │ 4 etapes │        │ Revue    │   │
│  │ DPIA ?       │          │ detaillees│        │ annuelle │   │
│  └──────────────┘          └──────────┘        └──────────┘   │
│                                                                  │
│  💡 La DPIA est un document vivant : elle doit etre mise a     │
│     jour a chaque changement significatif du traitement         │
└──────────────────────────────────────────────────────────────────┘
```

### 6.2 Script de pre-check automatise

```python
def dpia_pre_check(treatment_config: dict) -> dict:
    """
    Pre-check rapide pour determiner si une DPIA est necessaire.
    Base sur les 9 criteres du CEPD (Comite Europeen de la Protection des Donnees).
    """
    criteria = {
        "evaluation_scoring": treatment_config.get("involves_scoring", False),
        "automated_decision": treatment_config.get("automated_decision_with_legal_effect", False),
        "systematic_monitoring": treatment_config.get("systematic_monitoring", False),
        "sensitive_data": treatment_config.get("processes_sensitive_data", False),
        "large_scale": treatment_config.get("data_subjects_count", 0) > 10000,
        "data_matching": treatment_config.get("crosses_datasets", False),
        "vulnerable_persons": treatment_config.get("involves_vulnerable_persons", False),
        "innovative_technology": treatment_config.get("uses_ai_or_innovative_tech", False),
        "exclusion_from_right": treatment_config.get("can_exclude_from_service", False),
    }

    criteria_met = sum(criteria.values())

    result = {
        "criteria_checked": criteria,
        "criteria_met_count": criteria_met,
        "dpia_required": criteria_met >= 2,
        "recommendation": ""
    }

    if criteria_met >= 2:
        result["recommendation"] = (
            f"⚠️ DPIA OBLIGATOIRE : {criteria_met} criteres sur 9 sont remplis. "
            f"Criteres actifs : {[k for k, v in criteria.items() if v]}. "
            f"Realisez la DPIA AVANT de commencer le developpement."
        )
    elif criteria_met == 1:
        result["recommendation"] = (
            f"💡 DPIA RECOMMANDEE : 1 critere sur 9 est rempli ({[k for k, v in criteria.items() if v][0]}). "
            f"Bien que non obligatoire, une DPIA est une bonne pratique."
        )
    else:
        result["recommendation"] = (
            "✅ DPIA NON REQUISE : aucun critere du CEPD n'est rempli. "
            "Documentez tout de meme le traitement dans le registre."
        )

    return result

# Exemple d'utilisation : modele de prediction de churn
churn_model_config = {
    "involves_scoring": True,                        # Profilage/scoring
    "automated_decision_with_legal_effect": False,   # Pas d'effet juridique direct
    "systematic_monitoring": False,
    "processes_sensitive_data": False,
    "data_subjects_count": 500000,                   # Grande echelle
    "crosses_datasets": True,                        # Croisement CRM + commandes + support
    "involves_vulnerable_persons": False,
    "uses_ai_or_innovative_tech": True,              # Machine Learning
    "can_exclude_from_service": False,
}

result = dpia_pre_check(churn_model_config)
print(result["recommendation"])
# ⚠️ DPIA OBLIGATOIRE : 4 criteres sur 9 sont remplis.
# Criteres actifs : ['evaluation_scoring', 'large_scale', 'data_matching', 'innovative_technology'].
```

---

## 7. Resume et Points Cles

✅ La DPIA est obligatoire des que 2 des 9 criteres du CEPD sont remplis

✅ Elle doit etre realisee **avant** le debut du traitement

✅ Elle comprend 4 etapes : description, necessite, risques, mesures

✅ La matrice probabilite x gravite permet d'objectiver les risques

✅ La CNIL doit etre consultee si le risque residuel reste eleve

✅ La DPIA est un document vivant, a mettre a jour regulierement

✅ L'outil PIA de la CNIL facilite grandement la realisation

---

## 📝 Exercice Rapide

**Scenario** : Votre entreprise souhaite mettre en place un systeme de detection de fraude en temps reel qui :
- Analyse toutes les transactions bancaires des clients (2 millions)
- Utilise un modele de deep learning
- Bloque automatiquement les transactions suspectes
- Stocke les donnees pendant 5 ans

**Questions** :
1. Une DPIA est-elle necessaire ? Quels criteres sont remplis ?
2. Identifiez au moins 3 risques majeurs
3. Proposez des mesures d'attenuation pour chaque risque

> **Reponses** : voir [08-exercices.md](08-exercices.md)

---

[← Precedent](05-anonymisation-pseudonymisation.md) | [🏠 Accueil](README.md) | [Suivant →](07-securite-gouvernance.md)

---

**Academy** - Formation Data Engineer
