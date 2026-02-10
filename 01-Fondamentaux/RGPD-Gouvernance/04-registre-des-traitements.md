[← Precedent](03-droits-des-personnes.md) | [🏠 Accueil](README.md) | [Suivant →](05-anonymisation-pseudonymisation.md)

# 📖 Cours 4 - Registre des Traitements

## Documenter vos traitements de donnees conformement a l'Article 30

---

## 1. Qu'est-ce que le Registre des Traitements ?

### 1.1 Definition et cadre legal

Le **registre des traitements** (Article 30 du RGPD) est un document obligatoire qui recense l'ensemble des traitements de donnees personnelles effectues par un organisme.

> **Article 30.1** : Chaque responsable du traitement tient un registre des activites de traitement effectuees sous sa responsabilite.

C'est l'equivalent d'un "inventaire" de tous vos traitements de donnees personnelles. Pour un Data Engineer, c'est la **documentation de reference** qui guide la conception et l'operation de chaque pipeline.

### 1.2 Qui doit le maintenir ?

```
┌──────────────────────────────────────────────────────────────────┐
│           Qui doit tenir un registre des traitements ?           │
│                                                                  │
│  ✅ TOUTES les entreprises de 250+ salaries                     │
│                                                                  │
│  ✅ TOUTES les entreprises, meme < 250 salaries, si :           │
│     - Le traitement est susceptible de comporter un risque      │
│       pour les droits et libertes des personnes                 │
│     - Le traitement n'est pas occasionnel                       │
│     - Le traitement porte sur des donnees sensibles             │
│       ou des condamnations penales                              │
│                                                                  │
│  ⚠️ En pratique : quasiment TOUTES les entreprises qui         │
│     traitent des donnees personnelles                           │
│                                                                  │
│  💡 En tant que Data Engineer, vous contribuez au registre      │
│     meme si sa tenue est la responsabilite du DPO              │
└──────────────────────────────────────────────────────────────────┘
```

### 1.3 Deux registres distincts

| Registre | Tenu par | Contenu |
|----------|----------|---------|
| **Registre du responsable de traitement** (Art. 30.1) | L'entreprise qui determine les finalites | Tous les traitements dont elle est responsable |
| **Registre du sous-traitant** (Art. 30.2) | Le prestataire qui traite pour le compte d'un autre | Tous les traitements effectues pour le compte de clients |

---

## 2. Contenu Obligatoire du Registre

### 2.1 Champs requis par l'Article 30

Pour chaque traitement, le registre doit contenir :

| # | Champ | Description | Exemple |
|---|-------|-------------|---------|
| 1 | **Nom du traitement** | Intitule clair et explicite | "Pipeline ETL comportement utilisateur" |
| 2 | **Responsable de traitement** | Identite et coordonnees | "Societe XYZ - DPO : dpo@xyz.com" |
| 3 | **Finalite(s)** | Objectif du traitement | "Analyse comportementale pour optimisation UX" |
| 4 | **Base legale** | Fondement juridique | "Consentement (cookie analytics)" |
| 5 | **Categories de personnes** | Qui est concerne | "Visiteurs du site web" |
| 6 | **Categories de donnees** | Types de donnees traitees | "Donnees de navigation, IP anonymisee, pages vues" |
| 7 | **Destinataires** | Qui accede aux donnees | "Equipe Data, Equipe Produit" |
| 8 | **Transferts hors UE** | Si applicable | "Non / Oui : USA - Clauses contractuelles types" |
| 9 | **Duree de conservation** | Combien de temps | "13 mois maximum" |
| 10 | **Mesures de securite** | Protections en place | "Chiffrement AES-256, RBAC, logs d'acces" |

### 2.2 Champs recommandes (bonnes pratiques)

En plus des champs obligatoires, ajoutez :

| Champ supplementaire | Utilite |
|---------------------|---------|
| Date de creation / mise a jour | Suivi de l'evolution |
| Service responsable | Identification interne |
| Sous-traitants impliques | Cartographie des flux |
| Logiciels / outils utilises | Inventaire technique |
| DPIA necessaire ? (oui/non) | Suivi de conformite |
| Lien vers la documentation technique | Reference rapide |
| Statut (actif / archive / en cours) | Suivi du cycle de vie |

---

## 3. Template du Registre des Traitements

### 3.1 Template Markdown

Voici un template utilisable directement dans un depot Git :

```markdown
# Registre des Traitements - [Nom de l'Entreprise]

## Informations Generales
- **Responsable de traitement** : [Nom, adresse]
- **DPO** : [Nom, email, telephone]
- **Derniere mise a jour** : [Date]
- **Version** : [X.Y]

---

## Traitement #[ID]

| Champ | Valeur |
|-------|--------|
| **Identifiant** | TRT-[YYYY]-[NNN] |
| **Nom du traitement** | [Intitule] |
| **Service responsable** | [Equipe] |
| **Date de creation** | [Date] |
| **Derniere mise a jour** | [Date] |
| **Statut** | Actif / Archive / En developpement |
| **Finalite(s)** | [Description des objectifs] |
| **Base legale** | [Consentement / Contrat / Obligation legale / ...] |
| **Categories de personnes** | [Clients, prospects, employes...] |
| **Categories de donnees** | [Liste des types de donnees] |
| **Donnees sensibles** | Oui / Non - Si oui, lesquelles |
| **Source des donnees** | [Comment les donnees sont collectees] |
| **Destinataires internes** | [Services ayant acces] |
| **Destinataires externes** | [Sous-traitants, partenaires] |
| **Transfert hors UE** | Oui / Non - Si oui, pays et garanties |
| **Duree de conservation** | [Duree + critere] |
| **Mesures de securite** | [Liste des mesures techniques et organisationnelles] |
| **DPIA necessaire** | Oui / Non |
| **Lien documentation** | [URL vers doc technique] |
```

---

## 4. Exemple Concret 1 : Pipeline ETL de Comportement Utilisateur

### 4.1 Description du traitement

```
┌──────────────────────────────────────────────────────────────────┐
│            Pipeline ETL - Comportement Utilisateur               │
│                                                                  │
│  Source          Traitement         Destination                  │
│  ┌─────────┐    ┌──────────┐      ┌──────────────┐            │
│  │Site Web │───►│ Kafka    │─────►│ Data         │            │
│  │(events) │    │ Stream   │      │ Warehouse    │            │
│  └─────────┘    └──────────┘      │ (BigQuery)   │            │
│                      │             └──────────────┘            │
│  ┌─────────┐         │                    │                     │
│  │App      │─────────┘                    ▼                     │
│  │Mobile   │              ┌──────────────────────┐             │
│  └─────────┘              │ Dashboard Analytics  │             │
│                           │ (Looker/Metabase)    │             │
│                           └──────────────────────┘             │
└──────────────────────────────────────────────────────────────────┘
```

### 4.2 Fiche du registre

| Champ | Valeur |
|-------|--------|
| **Identifiant** | TRT-2024-001 |
| **Nom du traitement** | Pipeline ETL - Analyse comportement utilisateur |
| **Service responsable** | Equipe Data Engineering |
| **Date de creation** | 15/01/2024 |
| **Derniere mise a jour** | 20/03/2024 |
| **Statut** | Actif |
| **Finalite(s)** | 1. Mesure d'audience du site web et de l'application mobile 2. Amelioration de l'experience utilisateur 3. Reporting produit (taux de conversion, parcours utilisateur) |
| **Base legale** | Consentement (cookie analytics - bandeau conforme) |
| **Categories de personnes** | Visiteurs du site web et utilisateurs de l'application mobile ayant consenti |
| **Categories de donnees** | - Identifiant utilisateur pseudonymise (hash) - Pages visitees et horodatage - Duree de session - Type d'appareil et navigateur (categorise, pas le UA complet) - Actions effectuees (clics, scroll, ajout panier) - Referrer (page d'origine) |
| **Donnees sensibles** | Non |
| **Source des donnees** | Collecte directe via SDK analytics (Segment) |
| **Destinataires internes** | Equipe Data (acces complet), Equipe Produit (dashboards agreges uniquement) |
| **Destinataires externes** | Segment (collecte), Google BigQuery (stockage UE), Looker (visualisation) |
| **Transfert hors UE** | Non - Stockage BigQuery region europe-west1 (Belgique) |
| **Duree de conservation** | 13 mois a compter de la collecte (conforme recommandation CNIL) |
| **Mesures de securite** | - Pseudonymisation des identifiants utilisateur (SHA-256) - Chiffrement au repos (AES-256 natif BigQuery) - Chiffrement en transit (TLS 1.3) - RBAC : acces limite aux equipes Data et Produit - Logs d'acces BigQuery actives - IP tronquee au dernier octet avant stockage - Purge automatique via scheduled query (> 13 mois) |
| **DPIA necessaire** | Non (pas de profilage, pas de donnees sensibles, echelle non massive) |
| **Lien documentation** | `docs/pipelines/etl-user-behavior.md` |

---

## 5. Exemple Concret 2 : Modele ML de Prediction de Churn

### 5.1 Description du traitement

```
┌──────────────────────────────────────────────────────────────────┐
│          Pipeline ML - Prediction du Churn Client                │
│                                                                  │
│  Sources                  Entrainement        Inference          │
│  ┌──────────┐            ┌──────────┐       ┌──────────┐       │
│  │ CRM      │───────────►│          │       │          │       │
│  │ (clients)│            │ Feature  │──────►│ Modele   │──┐    │
│  └──────────┘            │ Store    │       │ ML       │  │    │
│  ┌──────────┐            │          │       │ (Random  │  │    │
│  │ Commandes│───────────►│          │       │  Forest) │  │    │
│  │ (orders) │            └──────────┘       └──────────┘  │    │
│  └──────────┘                                             │    │
│  ┌──────────┐                               ┌──────────┐  │    │
│  │ Support  │───────────────────────────────►│ Scores   │◄─┘   │
│  │ (tickets)│                               │ de churn │       │
│  └──────────┘                               └─────┬────┘       │
│                                                    │            │
│                                              ┌─────▼────┐      │
│                                              │ Actions   │      │
│                                              │ retention │      │
│                                              └──────────┘      │
└──────────────────────────────────────────────────────────────────┘
```

### 5.2 Fiche du registre

| Champ | Valeur |
|-------|--------|
| **Identifiant** | TRT-2024-005 |
| **Nom du traitement** | Modele ML - Prediction du churn client |
| **Service responsable** | Equipe Data Science / ML Engineering |
| **Date de creation** | 01/03/2024 |
| **Derniere mise a jour** | 15/06/2024 |
| **Statut** | Actif |
| **Finalite(s)** | 1. Prediction de la probabilite de depart des clients 2. Declenchement d'actions de retention personnalisees 3. Optimisation du taux de retention global |
| **Base legale** | Interet legitime (balance des interets documentee - voir DPIA TRT-2024-005) : l'entreprise a un interet economique a anticiper le churn, les clients peuvent raisonnablement s'attendre a ce que leurs donnees d'usage soient utilisees pour ameliorer le service |
| **Categories de personnes** | Clients actifs (contrat en cours ou derniere commande < 12 mois) |
| **Categories de donnees** | - Identifiant client pseudonymise - Anciennete client (en mois) - Frequence d'achat (commandes / mois) - Montant moyen des commandes - Nombre de tickets support ouverts - Delai moyen de resolution des tickets - Score NPS (si disponible) - Categorie de produits achetes (agregee) |
| **Donnees sensibles** | Non |
| **Donnees NON utilisees** | Nom, prenom, email, adresse, telephone, donnees de paiement (exclus par design) |
| **Source des donnees** | Bases de donnees internes (CRM, base commandes, base support) |
| **Destinataires internes** | Equipe Data Science (entrainement), Equipe CRM (scores de churn), Equipe Marketing (actions retention) |
| **Destinataires externes** | Aucun |
| **Transfert hors UE** | Non - Infrastructure on-premise + cloud OVH (France) |
| **Duree de conservation** | - Donnees d'entrainement : 24 mois glissants - Scores de churn : 6 mois - Modeles entraines : 12 mois (versionnes, les anciens sont archives puis supprimes) |
| **Mesures de securite** | - Pseudonymisation des identifiants (pas de donnees directement identifiantes dans le feature store) - Chiffrement du feature store au repos (AES-256) - Acces au modele et aux scores via API authentifiee (JWT) - RBAC : seuls Data Scientists et ML Engineers ont acces aux donnees d'entrainement - Logs d'acces au modele et aux predictions - Pas de stockage des donnees individuelles dans les artefacts du modele - Audit de biais trimestriel |
| **DPIA necessaire** | Oui - Realisee le 01/03/2024 (profilage a grande echelle) |
| **Lien documentation** | `docs/ml/churn-prediction-model.md` |
| **Droit d'opposition** | Implemente - Les clients peuvent s'opposer au profilage via le service client ou l'espace personnel |
| **Intervention humaine** | Oui - Les actions de retention sont validees par l'equipe CRM avant execution |

---

## 6. Maintenir le Registre dans une Equipe Data

### 6.1 Integration avec Git

```
┌──────────────────────────────────────────────────────────────────┐
│        Workflow de maintenance du registre avec Git              │
│                                                                  │
│  1. Le registre est stocke dans le repo Git de l'equipe        │
│                                                                  │
│     data-team-repo/                                             │
│     ├── pipelines/                                              │
│     ├── models/                                                 │
│     ├── docs/                                                   │
│     └── rgpd/                                                   │
│         ├── registre-des-traitements.md   ← Le registre        │
│         ├── dpia/                                               │
│         │   ├── DPIA-TRT-2024-005.md                           │
│         │   └── DPIA-TRT-2024-008.md                           │
│         ├── templates/                                          │
│         │   ├── fiche-traitement-template.md                   │
│         │   └── dpia-template.md                               │
│         └── procedures/                                         │
│             ├── procedure-dsar.md                               │
│             └── procedure-data-breach.md                       │
│                                                                  │
│  2. Toute modification passe par une Pull Request              │
│     → Revue par le DPO ou le referent RGPD de l'equipe        │
│                                                                  │
│  3. Historique Git = preuve de l'evolution du registre          │
│     → Demonstre l'accountability                                │
└──────────────────────────────────────────────────────────────────┘
```

### 6.2 Automatisation : verifier la presence au registre dans la CI/CD

```python
# Script CI/CD : verifier qu'un nouveau pipeline a une fiche au registre
# .github/workflows/rgpd-check.yml (concept)

import os
import re
import sys

def check_registry_entry(pipeline_name: str, registry_path: str) -> bool:
    """
    Verifie qu'un pipeline a une entree dans le registre des traitements.
    A executer dans la CI/CD avant le merge.
    """
    with open(registry_path, 'r') as f:
        registry_content = f.read()

    # Chercher une reference au pipeline dans le registre
    if pipeline_name.lower() in registry_content.lower():
        print(f"✅ Pipeline '{pipeline_name}' trouve dans le registre")
        return True
    else:
        print(f"❌ Pipeline '{pipeline_name}' NON TROUVE dans le registre !")
        print(f"   Veuillez ajouter une fiche au registre avant de deployer.")
        print(f"   Template disponible dans : rgpd/templates/fiche-traitement-template.md")
        return False

def check_new_pipelines():
    """Verifie les nouveaux pipelines dans la PR."""
    registry_path = "rgpd/registre-des-traitements.md"

    # Lister les fichiers modifies dans la PR
    changed_files = os.popen("git diff --name-only origin/main...HEAD").read().strip().split('\n')

    new_pipelines = [f for f in changed_files if f.startswith("pipelines/") and f.endswith(".py")]

    all_ok = True
    for pipeline_file in new_pipelines:
        pipeline_name = os.path.basename(pipeline_file).replace('.py', '')
        if not check_registry_entry(pipeline_name, registry_path):
            all_ok = False

    if not all_ok:
        sys.exit(1)  # Faire echouer la CI

if __name__ == "__main__":
    check_new_pipelines()
```

### 6.3 Bonnes pratiques pour le maintien du registre

💡 **Conseil 1 : Nommer un referent RGPD dans l'equipe Data**
- Ce n'est pas necessairement le DPO, mais quelqu'un de l'equipe technique
- Il/elle valide les fiches de traitement avant la mise en production

💡 **Conseil 2 : Integrer la creation de la fiche dans le Definition of Done**
- Pas de nouveau pipeline en production sans fiche au registre
- Checklist dans le template de Pull Request

💡 **Conseil 3 : Revue trimestrielle**
- Verifier que les traitements actifs sont toujours pertinents
- Archiver les traitements obsoletes
- Mettre a jour les durees de conservation et les mesures de securite

💡 **Conseil 4 : Automatiser ce qui peut l'etre**
- Script de verification dans la CI/CD
- Alertes automatiques a l'approche des echeances de conservation
- Dashboard de suivi du nombre de traitements, de leur statut, des DPIA a jour

### 6.4 Template de fiche en YAML (alternative pour l'automatisation)

```yaml
# rgpd/traitements/TRT-2024-001.yaml
---
id: "TRT-2024-001"
name: "Pipeline ETL - Analyse comportement utilisateur"
status: "actif"
created_at: "2024-01-15"
updated_at: "2024-03-20"
owner:
  team: "Data Engineering"
  contact: "data-team@xyz.com"

treatment:
  purpose:
    - "Mesure d'audience du site web"
    - "Amelioration de l'experience utilisateur"
  legal_basis: "consentement"
  legal_basis_detail: "Cookie analytics - bandeau conforme"

data:
  subjects:
    - "Visiteurs du site web"
    - "Utilisateurs de l'application mobile"
  categories:
    - "Identifiant pseudonymise"
    - "Pages visitees"
    - "Duree de session"
    - "Type d'appareil"
  sensitive_data: false
  source: "Collecte directe via SDK analytics"

recipients:
  internal:
    - team: "Data Engineering"
      access_level: "complet"
    - team: "Produit"
      access_level: "dashboards agreges uniquement"
  external:
    - name: "Segment"
      role: "Collecte"
      contract_date: "2024-01-01"
    - name: "Google BigQuery"
      role: "Stockage"
      region: "europe-west1"

transfers:
  outside_eu: false

retention:
  duration: "13 mois"
  criteria: "A compter de la collecte"
  purge_mechanism: "Scheduled query BigQuery"

security:
  encryption_at_rest: "AES-256 (BigQuery natif)"
  encryption_in_transit: "TLS 1.3"
  access_control: "RBAC via IAM BigQuery"
  audit_logs: true
  pseudonymization: "SHA-256 sur identifiants utilisateur"
  ip_truncation: true

compliance:
  dpia_required: false
  dpia_reference: null
  last_review: "2024-03-20"
  next_review: "2024-06-20"
  documentation: "docs/pipelines/etl-user-behavior.md"
```

---

## 7. Resume et Points Cles

### 7.1 Checklist du registre des traitements

- [ ] Chaque traitement de donnees personnelles a une fiche au registre
- [ ] Les 10 champs obligatoires sont renseignes pour chaque fiche
- [ ] Les fiches sont a jour (revue trimestrielle minimum)
- [ ] Le registre est versionne (Git) avec historique des modifications
- [ ] Un referent RGPD est designe dans l'equipe Data
- [ ] La creation d'une fiche est integree dans le processus de developpement (DoD)
- [ ] Les traitements archives sont marques comme tels (pas supprimes)
- [ ] Le DPO a acces au registre et le valide regulierement

### 7.2 Erreurs courantes a eviter

❌ Registre jamais mis a jour apres la creation initiale

❌ Fiches trop vagues ("Traitement de donnees clients" sans precision)

❌ Oublier les traitements "secondaires" (logs, backups, environnements de test)

❌ Ne pas mentionner les sous-traitants (hebergeur cloud, outils SaaS)

❌ Confondre le registre avec la politique de confidentialite (ce sont deux documents differents)

---

## 📝 Exercice Rapide

**Scenario** : Votre equipe deploie un nouveau pipeline Airflow qui :
- Extrait quotidiennement les donnees de satisfaction client (NPS) d'un outil SaaS (Typeform)
- Enrichit ces donnees avec le profil client depuis le CRM (Salesforce)
- Stocke le resultat dans un data warehouse (Snowflake, region UE)
- Genere un dashboard hebdomadaire pour l'equipe Customer Success

**Mission** : Redigez la fiche du registre des traitements pour ce pipeline en utilisant le template ci-dessus.

> **Correction** : voir [08-exercices.md](08-exercices.md)

---

[← Precedent](03-droits-des-personnes.md) | [🏠 Accueil](README.md) | [Suivant →](05-anonymisation-pseudonymisation.md)

---

**Academy** - Formation Data Engineer
