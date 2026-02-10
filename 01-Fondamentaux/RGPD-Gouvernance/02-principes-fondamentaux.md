[← Precedent](01-introduction-enjeux.md) | [🏠 Accueil](README.md) | [Suivant →](03-droits-des-personnes.md)

# 📖 Cours 2 - Principes Fondamentaux du RGPD

## Les piliers de la protection des donnees personnelles

---

## 1. Les 6 Principes du RGPD (Article 5)

Le RGPD repose sur 6 principes fondamentaux que tout traitement de donnees doit respecter. En tant que Data Engineer, vous devez les integrer dans chaque pipeline, chaque base de donnees, chaque modele.

### 1.1 Principe 1 : Liceite, Loyaute et Transparence

> Les donnees doivent etre traitees de maniere licite, loyale et transparente au regard de la personne concernee.

**Ce que cela signifie pour le Data Engineer :**

- **Liceite** : chaque traitement doit reposer sur une des 6 bases legales (voir section 2)
- **Loyaute** : pas de collecte deloyale (dark patterns, cases pre-cochees, collecte cachee)
- **Transparence** : les personnes doivent etre informees de ce qu'on fait de leurs donnees

```python
# ❌ MAUVAISE PRATIQUE : collecte cachee de donnees
def track_user(request):
    # Collecte de donnees supplementaires sans information
    user_data = {
        "page": request.path,
        "ip": request.remote_addr,
        "user_agent": request.user_agent,
        "screen_resolution": request.headers.get('X-Screen-Res'),  # Collecte cachee
        "battery_level": request.headers.get('X-Battery'),          # Collecte cachee
        "installed_fonts": request.headers.get('X-Fonts'),          # Fingerprinting
    }
    save_to_analytics(user_data)

# ✅ BONNE PRATIQUE : collecte transparente et documentee
def track_user(request, consent_given=False):
    """Collecte les donnees de navigation avec consentement explicite."""
    # Donnees essentielles au fonctionnement (interet legitime)
    essential_data = {
        "page": request.path,
        "timestamp": datetime.now().isoformat(),
    }

    # Donnees analytiques (necessite consentement)
    if consent_given:
        essential_data.update({
            "ip_anonymized": anonymize_ip(request.remote_addr),  # IP tronquee
            "user_agent_category": categorize_ua(request.user_agent),  # Pas le UA brut
        })

    save_to_analytics(essential_data)
```

### 1.2 Principe 2 : Limitation des Finalites

> Les donnees sont collectees pour des finalites determinees, explicites et legitimes, et ne sont pas traitees ulterieurement de maniere incompatible avec ces finalites.

**Concretement :**

| Finalite initiale | Reutilisation compatible ✅ | Reutilisation incompatible ❌ |
|-------------------|---------------------------|-------------------------------|
| Gestion des commandes | Statistiques de vente agregees | Profilage publicitaire |
| Support client | Amelioration du service | Revente a des tiers |
| Paie des employes | Declarations sociales | Surveillance des performances |
| Livraison de colis | Optimisation des itineraires | Analyse des habitudes de vie |

```python
# ❌ MAUVAISE PRATIQUE : reutiliser les donnees pour une finalite differente
# Les donnees collectees pour la livraison sont reutilisees pour du marketing
def create_marketing_profile(delivery_data):
    return {
        "address": delivery_data['address'],
        "frequent_products": delivery_data['products'],
        "delivery_times": delivery_data['preferred_times'],  # Habitudes de vie !
        "neighborhood_wealth": estimate_wealth(delivery_data['address'])  # Profilage !
    }

# ✅ BONNE PRATIQUE : documenter et respecter les finalites
TREATMENT_PURPOSES = {
    "delivery_management": {
        "description": "Gestion et suivi des livraisons",
        "allowed_fields": ["order_id", "address", "delivery_date", "status"],
        "retention": "3 ans apres derniere commande",
        "legal_basis": "contrat"
    },
    "delivery_optimization": {
        "description": "Optimisation des itineraires de livraison",
        "allowed_fields": ["postal_code", "delivery_date", "time_slot"],  # Donnees minimisees
        "retention": "1 an glissant",
        "legal_basis": "interet_legitime"
    }
}
```

### 1.3 Principe 3 : Minimisation des Donnees

> Les donnees doivent etre adequates, pertinentes et limitees a ce qui est necessaire au regard des finalites.

C'est le principe le plus impactant pour le Data Engineer. Il faut resister a la tentation du "on collecte tout, on verra plus tard".

```sql
-- ❌ MAUVAISE PRATIQUE : SELECT * partout
SELECT * FROM clients WHERE region = 'IDF';
-- Recupere nom, prenom, email, telephone, adresse, date_naissance,
-- numero_secu, revenus... alors que seuls quelques champs sont necessaires

-- ✅ BONNE PRATIQUE : ne selectionner que les colonnes necessaires
SELECT client_id, ville, montant_total_achats
FROM clients
WHERE region = 'IDF';
-- Uniquement les donnees necessaires a l'analyse regionale
```

```python
# ❌ MAUVAISE PRATIQUE dans un pipeline ETL
def extract_customer_data():
    """Extrait TOUTES les donnees clients."""
    return pd.read_sql("SELECT * FROM customers", engine)

# ✅ BONNE PRATIQUE dans un pipeline ETL
def extract_customer_data(purpose: str):
    """Extrait les donnees clients necessaires selon la finalite."""
    QUERIES = {
        "monthly_revenue_report": """
            SELECT customer_segment, SUM(revenue) as total_revenue
            FROM orders
            GROUP BY customer_segment
        """,
        "churn_prediction": """
            SELECT
                customer_id,
                EXTRACT(YEAR FROM AGE(last_purchase_date)) as years_since_purchase,
                total_orders,
                avg_order_value
            FROM customer_metrics
        """
    }
    if purpose not in QUERIES:
        raise ValueError(f"Finalite non definie : {purpose}")
    return pd.read_sql(QUERIES[purpose], engine)
```

### 1.4 Principe 4 : Exactitude

> Les donnees doivent etre exactes et, si necessaire, tenues a jour. Les donnees inexactes doivent etre effacees ou rectifiees sans tarder.

**Implications pour le Data Engineer :**
- Mettre en place des processus de verification de qualite des donnees
- Permettre la rectification facile des donnees
- Gerer les donnees en doublon

```python
# Exemple : validation et nettoyage des donnees dans un pipeline
import pandas as pd

def validate_personal_data(df: pd.DataFrame) -> pd.DataFrame:
    """Valide et nettoie les donnees personnelles."""

    # Verifier les emails valides
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    invalid_emails = ~df['email'].str.match(email_pattern, na=False)
    if invalid_emails.any():
        print(f"⚠️ {invalid_emails.sum()} emails invalides detectes")
        df.loc[invalid_emails, 'email_valid'] = False

    # Verifier les dates de naissance coherentes
    df['date_naissance'] = pd.to_datetime(df['date_naissance'], errors='coerce')
    future_dates = df['date_naissance'] > pd.Timestamp.now()
    if future_dates.any():
        print(f"⚠️ {future_dates.sum()} dates de naissance dans le futur")
        df.loc[future_dates, 'date_naissance'] = pd.NaT

    # Detecter les doublons potentiels
    duplicates = df.duplicated(subset=['email'], keep=False)
    if duplicates.any():
        print(f"⚠️ {duplicates.sum()} doublons potentiels detectes sur l'email")

    return df
```

### 1.5 Principe 5 : Limitation de la Conservation

> Les donnees ne doivent pas etre conservees plus longtemps que necessaire pour les finalites du traitement.

**Durees recommandees par la CNIL :**

| Type de donnees | Duree de conservation | Base |
|----------------|----------------------|------|
| Donnees clients actifs | Duree de la relation commerciale | Contrat |
| Donnees prospects | 3 ans apres le dernier contact | Interet legitime |
| Cookies et traceurs | 13 mois maximum | Consentement |
| Logs de connexion | 1 an (6 mois recommande) | Obligation legale |
| Donnees RH (contrat en cours) | Duree du contrat + 5 ans | Obligation legale |
| Donnees de facturation | 10 ans (obligation comptable) | Obligation legale |
| Donnees de sante | 20 ans | Obligation legale |
| CV non retenus | 2 ans maximum | Interet legitime |

```python
# Exemple Airflow : DAG de purge automatique des donnees
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

def purge_expired_data(**context):
    """Purge les donnees dont la duree de conservation est depassee."""
    import psycopg2

    conn = psycopg2.connect(dsn="postgresql://...")
    cur = conn.cursor()

    purge_rules = [
        ("prospects", "last_contact_date", "3 years"),
        ("connection_logs", "created_at", "13 months"),
        ("newsletter_unsubscribed", "unsubscribed_at", "30 days"),
    ]

    for table, date_column, retention in purge_rules:
        cur.execute(f"""
            DELETE FROM {table}
            WHERE {date_column} < NOW() - INTERVAL %s
            RETURNING COUNT(*)
        """, (retention,))
        count = cur.fetchone()[0]
        print(f"Purge {table}: {count} lignes supprimees")

    conn.commit()
    conn.close()

dag = DAG(
    'rgpd_data_purge',
    schedule_interval='@weekly',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['rgpd', 'compliance']
)

purge_task = PythonOperator(
    task_id='purge_expired_data',
    python_callable=purge_expired_data,
    dag=dag
)
```

### 1.6 Principe 6 : Integrite et Confidentialite

> Les donnees doivent etre traitees de facon a garantir une securite appropriee, y compris la protection contre le traitement non autorise ou illicite, la perte, la destruction ou les degats accidentels.

Ce principe sera detaille dans le cours [07-securite-gouvernance.md](07-securite-gouvernance.md).

**Resume rapide des mesures :**
- 🔐 Chiffrement au repos (AES-256) et en transit (TLS 1.2+)
- 🔐 Controle d'acces strict (RBAC, principe du moindre privilege)
- 🔐 Journalisation des acces (audit logs)
- 🔐 Sauvegardes chiffrees et testees regulierement
- 🔐 Politique de mots de passe robuste (hachage bcrypt)

---

## 2. Les 6 Bases Legales du Traitement (Article 6)

Pour qu'un traitement soit licite, il doit reposer sur **au moins une** des 6 bases legales suivantes. Le choix de la base legale est **irreversible** pour un traitement donne.

### 2.1 Tableau comparatif des bases legales

| Base legale | Description | Exemple Data Engineering | Droits impactes | Revocable ? |
|-------------|-------------|-------------------------|-----------------|-------------|
| **Consentement** | La personne a donne son accord explicite | Cookies analytics, newsletter, profilage marketing | Tous les droits | Oui, a tout moment |
| **Contrat** | Necessaire a l'execution d'un contrat | Pipeline de gestion des commandes, CRM | Pas de droit d'opposition | Non (tant que le contrat est actif) |
| **Obligation legale** | Impose par la loi | Conservation des factures 10 ans, declarations fiscales | Pas de droit a l'effacement | Non |
| **Interets vitaux** | Protection de la vie de la personne | Systeme d'alerte sanitaire, donnees medicales d'urgence | Limite | Non |
| **Mission d'interet public** | Exercice de l'autorite publique | Statistiques INSEE, recherche medicale | Droit d'opposition possible | Non |
| **Interets legitimes** | Interet du responsable, balance avec les droits de la personne | Securite informatique (logs), prevention de la fraude | Droit d'opposition | Indirectement |

### 2.2 Consentement : les regles strictes

Le consentement RGPD doit etre **LLSE** :
- **Libre** : pas de consequence negative en cas de refus
- **Specifique** : un consentement par finalite
- **Eclaire** : information complete et comprehensible
- **Sans ambiguite** : acte positif clair (pas de case pre-cochee)

```python
# ❌ MAUVAISE PRATIQUE : consentement non conforme
consent_text = "En continuant a naviguer, vous acceptez nos cookies et le partage
de vos donnees avec nos 847 partenaires."
# Problemes : non specifique, pas libre (pas de choix), pas eclaire (847 partenaires?)

# ✅ BONNE PRATIQUE : consentement granulaire et explicite
consent_options = {
    "essential": {
        "description": "Cookies necessaires au fonctionnement du site",
        "required": True,
        "legal_basis": "interet_legitime"  # Pas besoin de consentement
    },
    "analytics": {
        "description": "Mesure d'audience anonymisee (Matomo)",
        "required": False,
        "default": False,  # Pas pre-coche !
        "legal_basis": "consentement"
    },
    "marketing": {
        "description": "Publicite personnalisee par [Nom du partenaire]",
        "required": False,
        "default": False,
        "legal_basis": "consentement"
    }
}
```

### 2.3 Interet legitime : le test de balance

L'interet legitime est la base legale la plus complexe. Elle necessite un **test de balance** en 3 etapes :

```
┌───────────────────────────────────────────────────────────┐
│              Test de balance - Interet Legitime            │
│                                                           │
│  Etape 1 : Identification de l'interet                   │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ L'interet est-il legitime, precis et reel ?         │ │
│  │ Ex: "Prevenir la fraude sur les paiements"          │ │
│  └───────────────────────┬─────────────────────────────┘ │
│                          │ OUI                            │
│  Etape 2 : Necessite     ▼                               │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ Le traitement est-il necessaire a cet interet ?     │ │
│  │ Existe-t-il un moyen moins intrusif ?               │ │
│  └───────────────────────┬─────────────────────────────┘ │
│                          │ OUI                            │
│  Etape 3 : Balance       ▼                               │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ L'interet du responsable l'emporte-t-il sur les     │ │
│  │ droits et libertes de la personne concernee ?       │ │
│  │ Facteurs : nature des donnees, attentes raisonnables│ │
│  │ des personnes, impact sur la vie privee, garanties  │ │
│  └─────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────┘
```

💡 **Conseil pratique** : Documentez systematiquement votre test de balance. En cas de controle CNIL, c'est ce document qui prouvera la legitimite de votre traitement.

### 2.4 Exemples concrets par type de pipeline

| Type de pipeline | Base legale recommandee | Justification |
|-----------------|------------------------|---------------|
| Pipeline ETL e-commerce (commandes) | Contrat | Necessaire a la livraison |
| Pipeline analytics web (cookies) | Consentement | Pas strictement necessaire |
| Pipeline logs de securite (SIEM) | Interet legitime | Securite du SI |
| Pipeline facturation/comptabilite | Obligation legale | Code de commerce |
| Pipeline scoring credit (banque) | Interet legitime + consentement | Depend du contexte |
| Pipeline RH (paie) | Obligation legale + contrat | Code du travail |
| Pipeline recherche medicale | Mission d'interet public | Cadre legal specifique |
| Pipeline ML recommendation produits | Consentement OU interet legitime | Balance des interets a evaluer |

---

## 3. Les Donnees Sensibles (Article 9)

### 3.1 Categories de donnees sensibles

Le RGPD interdit par principe le traitement de certaines categories de donnees, sauf exceptions :

| Categorie | Exemples | Risque |
|-----------|----------|--------|
| Origine raciale ou ethnique | Couleur de peau, origine geographique | Discrimination |
| Opinions politiques | Adhesion a un parti, votes | Persecution |
| Convictions religieuses ou philosophiques | Religion, croyances | Discrimination |
| Appartenance syndicale | Adhesion, activite syndicale | Discrimination professionnelle |
| Donnees genetiques | ADN, genome | Discrimination, assurance |
| Donnees biometriques | Empreintes digitales, reconnaissance faciale | Usurpation d'identite |
| Donnees de sante | Dossier medical, handicap, allergies | Discrimination, assurance |
| Vie sexuelle ou orientation sexuelle | Preferences, pratiques | Discrimination |
| Donnees relatives aux condamnations penales | Casier judiciaire | Discrimination |

### 3.2 Exceptions permettant le traitement

Le traitement de donnees sensibles est autorise si :
- La personne a donne son **consentement explicite**
- Le traitement est necessaire en matiere de **droit du travail** et de protection sociale
- Le traitement est necessaire pour des **motifs d'interet public** dans le domaine de la sante publique
- Le traitement est necessaire a la **recherche scientifique** (avec garanties appropriees)
- Les donnees sont manifestement **rendues publiques** par la personne

### 3.3 Impact pour le Data Engineer / Dev IA

```python
# ❌ MAUVAISE PRATIQUE : stocker des donnees sensibles sans protection renforcee
CREATE TABLE patients (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100),
    diagnostic TEXT,          -- Donnee de sante en clair !
    traitement TEXT,          -- Donnee de sante en clair !
    groupe_sanguin VARCHAR(5) -- Donnee de sante en clair !
);

# ✅ BONNE PRATIQUE : chiffrement au niveau colonne pour les donnees sensibles
CREATE TABLE patients (
    id SERIAL PRIMARY KEY,
    nom_chiffre BYTEA,                              -- Chiffre avec cle specifique
    diagnostic_chiffre BYTEA,                        -- Chiffre avec cle specifique
    traitement_chiffre BYTEA,                        -- Chiffre avec cle specifique
    groupe_sanguin_chiffre BYTEA,                    -- Chiffre avec cle specifique
    -- Seuls les utilisateurs autorises peuvent dechiffrer
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    access_level VARCHAR(20) DEFAULT 'restricted'    -- Controle d'acces renforce
);
```

---

## 4. Privacy by Design et Privacy by Default

### 4.1 Privacy by Design (Protection des donnees des la conception)

Les 7 principes fondateurs (Ann Cavoukian) :

1. **Proactif, pas reactif** : anticiper les risques, pas les corriger apres coup
2. **Protection par defaut** : pas d'action necessaire de l'utilisateur
3. **Protection integree** : fait partie de l'architecture, pas un ajout
4. **Somme positive** : protection ET fonctionnalite (pas l'un ou l'autre)
5. **Securite de bout en bout** : du debut a la fin du cycle de vie
6. **Visibilite et transparence** : processus verifiables
7. **Respect de la vie privee** : l'utilisateur au centre

### 4.2 Application concrete : checklist pour un nouveau pipeline

```
┌──────────────────────────────────────────────────────────────┐
│         Checklist Privacy by Design - Nouveau Pipeline        │
│                                                              │
│  Phase de conception :                                       │
│  □ La finalite du traitement est documentee                  │
│  □ La base legale est identifiee et validee par le DPO      │
│  □ Seules les donnees strictement necessaires sont collectees│
│  □ La duree de conservation est definie                      │
│  □ L'anonymisation/pseudonymisation est prevue si possible   │
│                                                              │
│  Phase de developpement :                                    │
│  □ Le chiffrement est implemente (repos + transit)           │
│  □ Les acces sont restreints (RBAC)                         │
│  □ Les logs d'acces sont en place                           │
│  □ Les mecanismes de purge sont automatises                 │
│  □ L'export de donnees (portabilite) est prevu              │
│  □ La suppression de donnees (effacement) est implementee   │
│                                                              │
│  Phase de mise en production :                               │
│  □ Le traitement est inscrit au registre                    │
│  □ L'analyse d'impact est realisee si necessaire            │
│  □ Les tests de securite sont effectues                     │
│  □ La documentation est a jour                              │
└──────────────────────────────────────────────────────────────┘
```

### 4.3 Privacy by Default (Protection par defaut)

```python
# ❌ MAUVAISE PRATIQUE : tout est active par defaut
class UserProfile:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.marketing_consent = True      # Pre-active !
        self.data_sharing = True           # Pre-active !
        self.profiling_consent = True      # Pre-active !
        self.third_party_access = True     # Pre-active !

# ✅ BONNE PRATIQUE : rien n'est active par defaut
class UserProfile:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.marketing_consent = False     # Desactive par defaut
        self.data_sharing = False          # Desactive par defaut
        self.profiling_consent = False     # Desactive par defaut
        self.third_party_access = False    # Desactive par defaut
        self.data_retention_days = 365     # Duree minimale par defaut
        self.profile_visibility = "private"  # Prive par defaut
```

---

## 5. Accountability (Principe de Responsabilite)

### 5.1 Definition

L'**accountability** (Article 5.2) oblige le responsable de traitement a :
- Mettre en oeuvre les mesures appropriees
- **Etre capable de demontrer** la conformite a tout moment

Ce n'est plus "je suis conforme jusqu'a preuve du contraire" mais "je dois prouver que je suis conforme".

### 5.2 Documents et preuves a maintenir

| Document | Description | Responsable |
|----------|-------------|-------------|
| Registre des traitements | Liste de tous les traitements | DPO / Equipe Data |
| Analyses d'impact (DPIA) | Evaluation des risques | DPO + Data Engineer |
| Contrats de sous-traitance | Clauses RGPD avec prestataires | Juridique + DPO |
| Politique de confidentialite | Information des personnes | DPO + Marketing |
| Procedures de gestion des droits | Processus DSAR | DPO + Data Engineer |
| Registre des violations | Incidents de securite | DPO + RSSI |
| Documentation technique | Architecture, flux de donnees | Data Engineer |
| Preuves de consentement | Horodatage, contexte | Data Engineer |

### 5.3 Stockage des preuves de consentement

```python
# Modele de stockage des consentements
import json
from datetime import datetime

def store_consent(user_id, consent_type, granted, context):
    """
    Stocke une preuve de consentement conforme RGPD.

    Le consentement doit pouvoir etre prouve :
    - Qui a consenti
    - A quoi
    - Quand
    - Comment (contexte)
    - Version des CGU/mentions au moment du consentement
    """
    consent_record = {
        "user_id": user_id,
        "consent_type": consent_type,          # ex: "marketing_email"
        "granted": granted,                     # True/False
        "timestamp": datetime.utcnow().isoformat(),
        "ip_address_hash": hash_ip(context.get("ip")),  # Hash, pas l'IP brute
        "user_agent": context.get("user_agent"),
        "consent_version": context.get("policy_version"),  # Version des CGU
        "collection_method": context.get("method"),  # "web_form", "api", etc.
        "consent_text_shown": context.get("text"),   # Le texte exact presente
    }

    # Stockage immutable (append-only)
    db.consent_log.insert(consent_record)

    return consent_record
```

---

## 6. Resume Visuel : Les 6 Principes en Action

```
┌──────────────────────────────────────────────────────────────────────┐
│                  Les 6 Principes RGPD pour le Data Engineer          │
│                                                                      │
│  1. LICEITE/LOYAUTE/TRANSPARENCE                                    │
│     → Quelle base legale pour ce traitement ?                       │
│     → Les utilisateurs sont-ils informes ?                          │
│                                                                      │
│  2. LIMITATION DES FINALITES                                        │
│     → Ce pipeline a-t-il une finalite claire et documentee ?        │
│     → Les donnees sont-elles reutilisees pour autre chose ?         │
│                                                                      │
│  3. MINIMISATION                                                    │
│     → Ai-je besoin de TOUTES ces colonnes ?                        │
│     → Puis-je utiliser des donnees agregees plutot qu'individuelles?│
│                                                                      │
│  4. EXACTITUDE                                                      │
│     → Les donnees sont-elles a jour ?                               │
│     → Ai-je un processus de rectification ?                        │
│                                                                      │
│  5. LIMITATION DE LA CONSERVATION                                   │
│     → Quelle est la duree de retention ?                            │
│     → Ai-je un mecanisme de purge automatique ?                    │
│                                                                      │
│  6. INTEGRITE ET CONFIDENTIALITE                                    │
│     → Les donnees sont-elles chiffrees ?                            │
│     → Qui a acces a quoi ?                                          │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 📝 Exercice Rapide

**Scenario** : Vous devez creer un pipeline ETL qui :
1. Extrait les donnees de commandes clients d'une API e-commerce
2. Les transforme pour calculer le panier moyen par client
3. Les charge dans un data warehouse pour le reporting

**Questions** :
- Quelle(s) base(s) legale(s) s'applique(nt) ?
- Quelles donnees sont strictement necessaires (minimisation) ?
- Quelle duree de conservation proposez-vous ?
- Quelles mesures de securite implementez-vous ?

> **Reponses** : voir [08-exercices.md](08-exercices.md)

---

[← Precedent](01-introduction-enjeux.md) | [🏠 Accueil](README.md) | [Suivant →](03-droits-des-personnes.md)

---

**Academy** - Formation Data Engineer
