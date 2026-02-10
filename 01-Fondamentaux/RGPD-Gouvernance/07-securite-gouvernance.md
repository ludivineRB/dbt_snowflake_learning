[← Precedent](06-analyse-impact.md) | [🏠 Accueil](README.md) | [Suivant →](08-exercices.md)

# 📖 Cours 7 - Securite & Gouvernance des Donnees

## Proteger, controler et documenter le cycle de vie des donnees

---

## 1. Securite des Donnees

### 1.1 Chiffrement au repos (Data at Rest)

Le chiffrement au repos protege les donnees stockees contre les acces physiques non autorises (vol de disque, acces non autorise au serveur).

```
┌──────────────────────────────────────────────────────────────────┐
│                Chiffrement au Repos (AES-256)                    │
│                                                                  │
│  Donnees en clair          Cle AES-256          Donnees chiffrees│
│  ┌──────────────┐         ┌──────────┐         ┌──────────────┐│
│  │ nom: "Dupont"│  ──────►│ ******** │────────►│ 0xA3F2...    ││
│  │ email: "j@.."│         │ (stockee │         │ 0x7B8C...    ││
│  │ tel: "06..." │         │  dans un │         │ 0xD1E4...    ││
│  └──────────────┘         │  vault)  │         └──────────────┘│
│                           └──────────┘                          │
│                                                                  │
│  AES-256 : Advanced Encryption Standard avec cle de 256 bits   │
│  → Standard de l'industrie, approuve par la NSA pour les       │
│    documents classifies TOP SECRET                              │
└──────────────────────────────────────────────────────────────────┘
```

**Implementation au niveau base de donnees (PostgreSQL) :**

```sql
-- Activer l'extension pgcrypto pour le chiffrement au niveau colonne
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Table avec colonnes chiffrees
CREATE TABLE clients_secure (
    id SERIAL PRIMARY KEY,
    -- Donnees non sensibles (en clair pour les requetes)
    client_segment VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Donnees personnelles chiffrees
    nom_encrypted BYTEA,
    email_encrypted BYTEA,
    telephone_encrypted BYTEA,
    adresse_encrypted BYTEA
);

-- Insertion avec chiffrement
INSERT INTO clients_secure (client_segment, nom_encrypted, email_encrypted, telephone_encrypted)
VALUES (
    'premium',
    pgp_sym_encrypt('Jean Dupont', 'ma_cle_secrete_a_ne_pas_stocker_ici'),
    pgp_sym_encrypt('jean.dupont@email.fr', 'ma_cle_secrete_a_ne_pas_stocker_ici'),
    pgp_sym_encrypt('0612345678', 'ma_cle_secrete_a_ne_pas_stocker_ici')
);

-- Lecture avec dechiffrement (seuls les utilisateurs autorises ont la cle)
SELECT
    id,
    client_segment,
    pgp_sym_decrypt(nom_encrypted, 'ma_cle_secrete_a_ne_pas_stocker_ici') AS nom,
    pgp_sym_decrypt(email_encrypted, 'ma_cle_secrete_a_ne_pas_stocker_ici') AS email
FROM clients_secure;

-- ⚠️ En production : la cle de chiffrement doit etre stockee dans un vault
-- (HashiCorp Vault, AWS KMS, Azure Key Vault, GCP KMS)
-- JAMAIS en dur dans le code ou les requetes SQL !
```

**Implementation en Python :**

```python
from cryptography.fernet import Fernet
import os

class SecureDataStore:
    """Gestionnaire de donnees chiffrees au repos."""

    def __init__(self):
        # En production : recuperer la cle depuis un vault
        self.key = os.environ.get('ENCRYPTION_KEY', Fernet.generate_key())
        self.cipher = Fernet(self.key)

    def encrypt_field(self, value: str) -> bytes:
        """Chiffre un champ de donnee."""
        return self.cipher.encrypt(value.encode())

    def decrypt_field(self, encrypted_value: bytes) -> str:
        """Dechiffre un champ de donnee."""
        return self.cipher.decrypt(encrypted_value).decode()

    def encrypt_dataframe(self, df, sensitive_columns: list):
        """Chiffre les colonnes sensibles d'un DataFrame."""
        import pandas as pd
        df_encrypted = df.copy()
        for col in sensitive_columns:
            df_encrypted[col] = df[col].apply(
                lambda x: self.encrypt_field(str(x)) if pd.notna(x) else None
            )
        return df_encrypted

# Utilisation
store = SecureDataStore()

# Chiffrer des donnees avant stockage
encrypted_email = store.encrypt_field("jean.dupont@email.fr")
print(f"Chiffre : {encrypted_email}")

# Dechiffrer pour utilisation autorisee
decrypted_email = store.decrypt_field(encrypted_email)
print(f"Dechiffre : {decrypted_email}")
```

### 1.2 Chiffrement en transit (Data in Transit)

```
┌──────────────────────────────────────────────────────────────────┐
│              Chiffrement en Transit (TLS 1.3)                    │
│                                                                  │
│  Client                        Serveur                          │
│  ┌──────────┐     TLS 1.3     ┌──────────┐                    │
│  │          │ ◄═════════════► │          │                    │
│  │ Navigat. │   Certificat    │ API      │                    │
│  │ App      │   + cle pub.    │ Base DD  │                    │
│  │ Pipeline │                 │ Serveur  │                    │
│  └──────────┘                 └──────────┘                    │
│                                                                  │
│  ✅ A verifier :                                                │
│  - TLS 1.2 minimum (1.3 recommande)                            │
│  - Certificats valides et a jour                                │
│  - HTTPS partout (pas de HTTP)                                  │
│  - Connexions BDD chiffrees (SSL mode = require)               │
│  - Communications inter-services chiffrees (mTLS)              │
└──────────────────────────────────────────────────────────────────┘
```

```python
# Exemple : connexion chiffree a PostgreSQL
import psycopg2

# ❌ MAUVAISE PRATIQUE : connexion sans chiffrement
conn = psycopg2.connect(
    host="db.example.com",
    dbname="production",
    user="data_engineer",
    password="motdepasse"
    # Pas de SSL !
)

# ✅ BONNE PRATIQUE : connexion chiffree avec verification du certificat
conn = psycopg2.connect(
    host="db.example.com",
    dbname="production",
    user="data_engineer",
    password="motdepasse",
    sslmode="verify-full",             # Verifie le certificat du serveur
    sslrootcert="/path/to/ca-cert.pem" # Certificat racine
)
```

### 1.3 Hachage des mots de passe (bcrypt)

```python
import bcrypt

class PasswordManager:
    """Gestion securisee des mots de passe avec bcrypt."""

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hache un mot de passe avec bcrypt.
        bcrypt inclut automatiquement un sel unique.
        Le cout (rounds) de 12 est un bon compromis securite/performance.
        """
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(password.encode(), salt)
        return hashed.decode()

    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """Verifie un mot de passe contre son hash."""
        return bcrypt.checkpw(password.encode(), hashed.encode())

# Utilisation
pm = PasswordManager()

# Stockage : ne JAMAIS stocker le mot de passe en clair
hashed = pm.hash_password("MonMotDePasse123!")
print(f"Hash : {hashed}")
# $2b$12$LJ3m4... (le hash change a chaque appel grace au sel)

# Verification
print(pm.verify_password("MonMotDePasse123!", hashed))   # True
print(pm.verify_password("mauvais_mdp", hashed))          # False
```

```
┌──────────────────────────────────────────────────────────────────┐
│     Comparaison des algorithmes de hachage de mots de passe     │
│                                                                  │
│  Algorithme  │ Recommande  │ Sel integre │ Cout adaptatif       │
│  ────────────┼─────────────┼─────────────┼──────────────────    │
│  MD5         │ ❌ JAMAIS   │ Non         │ Non                  │
│  SHA-1       │ ❌ JAMAIS   │ Non         │ Non                  │
│  SHA-256     │ ❌ Seul     │ Non         │ Non                  │
│  bcrypt      │ ✅ OUI      │ Oui         │ Oui (rounds)        │
│  Argon2      │ ✅ OUI      │ Oui         │ Oui (memoire+temps) │
│  scrypt      │ ✅ OUI      │ Oui         │ Oui (memoire+temps) │
└──────────────────────────────────────────────────────────────────┘
```

---

## 2. Controle d'Acces (RBAC)

### 2.1 Principe du Moindre Privilege

> Chaque utilisateur, processus ou systeme ne doit avoir que les **permissions strictement necessaires** a l'accomplissement de sa tache.

```
┌──────────────────────────────────────────────────────────────────┐
│                 RBAC - Role-Based Access Control                 │
│                                                                  │
│  Utilisateur ──► Role ──► Permissions                           │
│                                                                  │
│  ┌──────────────┐   ┌──────────────────┐   ┌────────────────┐  │
│  │ Alice        │──►│ data_engineer     │──►│ SELECT, INSERT │  │
│  │ (Data Eng.)  │   │                  │   │ sur tables ETL │  │
│  └──────────────┘   └──────────────────┘   └────────────────┘  │
│                                                                  │
│  ┌──────────────┐   ┌──────────────────┐   ┌────────────────┐  │
│  │ Bob          │──►│ data_analyst      │──►│ SELECT seulemt │  │
│  │ (Analyst)    │   │                  │   │ sur vues       │  │
│  └──────────────┘   └──────────────────┘   └────────────────┘  │
│                                                                  │
│  ┌──────────────┐   ┌──────────────────┐   ┌────────────────┐  │
│  │ Charlie      │──►│ ml_engineer       │──►│ SELECT sur     │  │
│  │ (ML Eng.)    │   │                  │   │ feature store  │  │
│  └──────────────┘   └──────────────────┘   └────────────────┘  │
│                                                                  │
│  ┌──────────────┐   ┌──────────────────┐   ┌────────────────┐  │
│  │ Dana         │──►│ dba_admin         │──►│ ALL (avec      │  │
│  │ (DBA)        │   │                  │   │ restrictions)  │  │
│  └──────────────┘   └──────────────────┘   └────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
```

### 2.2 Implementation RBAC complete en SQL (PostgreSQL)

```sql
-- ================================================================
-- IMPLEMENTATION RBAC COMPLETE POUR UNE PLATEFORME DATA
-- ================================================================

-- 1. CREATION DES ROLES
-- ================================================================

-- Role de base : aucun privilege par defaut
CREATE ROLE data_reader NOLOGIN;        -- Lecture seule
CREATE ROLE data_writer NOLOGIN;        -- Lecture + ecriture
CREATE ROLE data_engineer NOLOGIN;      -- Operations ETL
CREATE ROLE data_analyst NOLOGIN;       -- Analyse et reporting
CREATE ROLE ml_engineer NOLOGIN;        -- Machine Learning
CREATE ROLE data_admin NOLOGIN;         -- Administration
CREATE ROLE dpo_auditor NOLOGIN;        -- Audit RGPD (DPO)

-- 2. SCHEMAS POUR ISOLATION
-- ================================================================

CREATE SCHEMA IF NOT EXISTS raw_data;       -- Donnees brutes (sensibles)
CREATE SCHEMA IF NOT EXISTS staging;        -- Donnees en cours de traitement
CREATE SCHEMA IF NOT EXISTS warehouse;      -- Donnees transformees
CREATE SCHEMA IF NOT EXISTS ml_features;    -- Feature store
CREATE SCHEMA IF NOT EXISTS analytics;      -- Vues pour le reporting
CREATE SCHEMA IF NOT EXISTS rgpd_audit;     -- Logs d'audit RGPD

-- 3. ATTRIBUTION DES PRIVILEGES PAR ROLE
-- ================================================================

-- Data Reader : lecture seule sur analytics et warehouse
GRANT USAGE ON SCHEMA analytics TO data_reader;
GRANT SELECT ON ALL TABLES IN SCHEMA analytics TO data_reader;
ALTER DEFAULT PRIVILEGES IN SCHEMA analytics GRANT SELECT ON TABLES TO data_reader;

-- Data Analyst : reader + creation de vues
GRANT data_reader TO data_analyst;
GRANT USAGE ON SCHEMA warehouse TO data_analyst;
GRANT SELECT ON ALL TABLES IN SCHEMA warehouse TO data_analyst;
GRANT CREATE ON SCHEMA analytics TO data_analyst;

-- Data Engineer : lecture/ecriture sur raw, staging, warehouse
GRANT USAGE ON SCHEMA raw_data, staging, warehouse TO data_engineer;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA raw_data TO data_engineer;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA staging TO data_engineer;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA warehouse TO data_engineer;
GRANT CREATE ON SCHEMA raw_data, staging, warehouse TO data_engineer;
ALTER DEFAULT PRIVILEGES IN SCHEMA raw_data GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO data_engineer;
ALTER DEFAULT PRIVILEGES IN SCHEMA staging GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO data_engineer;
ALTER DEFAULT PRIVILEGES IN SCHEMA warehouse GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO data_engineer;

-- ML Engineer : lecture sur warehouse + lecture/ecriture sur ml_features
GRANT USAGE ON SCHEMA warehouse, ml_features TO ml_engineer;
GRANT SELECT ON ALL TABLES IN SCHEMA warehouse TO ml_engineer;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA ml_features TO ml_engineer;
GRANT CREATE ON SCHEMA ml_features TO ml_engineer;

-- DPO Auditor : lecture seule sur tout + lecture sur les logs d'audit
GRANT USAGE ON SCHEMA raw_data, staging, warehouse, ml_features, analytics, rgpd_audit TO dpo_auditor;
GRANT SELECT ON ALL TABLES IN SCHEMA rgpd_audit TO dpo_auditor;
-- Le DPO peut voir les metadonnees mais PAS les donnees personnelles en clair
-- -> utiliser des vues masquees

-- Data Admin : tous les privileges (avec precautions)
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA raw_data TO data_admin;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA staging TO data_admin;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA warehouse TO data_admin;
GRANT data_engineer TO data_admin;

-- 4. CREATION DES UTILISATEURS
-- ================================================================

CREATE USER alice_engineer WITH PASSWORD 'strong_password_here' LOGIN;
GRANT data_engineer TO alice_engineer;

CREATE USER bob_analyst WITH PASSWORD 'strong_password_here' LOGIN;
GRANT data_analyst TO bob_analyst;

CREATE USER charlie_ml WITH PASSWORD 'strong_password_here' LOGIN;
GRANT ml_engineer TO charlie_ml;

CREATE USER dana_dba WITH PASSWORD 'strong_password_here' LOGIN;
GRANT data_admin TO dana_dba;

CREATE USER eve_dpo WITH PASSWORD 'strong_password_here' LOGIN;
GRANT dpo_auditor TO eve_dpo;

-- 5. VUES MASQUEES POUR LE DPO (voir les metadonnees sans les donnees)
-- ================================================================

CREATE VIEW rgpd_audit.users_overview AS
SELECT
    id,
    '***' AS nom,
    LEFT(email, 3) || '***@***' AS email_masked,
    created_at,
    is_deleted,
    processing_limited,
    CASE WHEN date_naissance IS NOT NULL THEN 'oui' ELSE 'non' END AS a_date_naissance
FROM raw_data.users;

GRANT SELECT ON rgpd_audit.users_overview TO dpo_auditor;

-- 6. VERIFICATION DES PRIVILEGES
-- ================================================================

-- Voir les privileges d'un utilisateur
SELECT
    grantee, table_schema, table_name, privilege_type
FROM information_schema.table_privileges
WHERE grantee = 'alice_engineer'
ORDER BY table_schema, table_name;
```

### 2.3 Matrice des acces

| Role | raw_data | staging | warehouse | ml_features | analytics | rgpd_audit |
|------|----------|---------|-----------|-------------|-----------|------------|
| **data_reader** | - | - | - | - | SELECT | - |
| **data_analyst** | - | - | SELECT | - | SELECT + CREATE | - |
| **data_engineer** | ALL DML | ALL DML | ALL DML | - | - | - |
| **ml_engineer** | - | - | SELECT | ALL DML | - | - |
| **dpo_auditor** | Vues masquees | Vues masquees | Vues masquees | Vues masquees | SELECT | SELECT |
| **data_admin** | ALL | ALL | ALL | ALL | ALL | SELECT |

---

## 3. Audit Logs (Journalisation)

### 3.1 Que faut-il journaliser ?

| Categorie | Evenements a logger | Pourquoi |
|-----------|--------------------|----------|
| **Acces aux donnees** | Qui a accede a quelles donnees, quand | Tracabilite |
| **Modifications** | INSERT, UPDATE, DELETE avec avant/apres | Integrite |
| **Acces administratifs** | Connexions admin, modifications de schema | Securite |
| **Exercice des droits** | DSAR, effacements, oppositions | Conformite RGPD |
| **Tentatives echouees** | Connexions ratees, acces refuses | Detection d'intrusion |
| **Exports de donnees** | Qui a exporte quoi, quand | Prevention de fuites |

### 3.2 Implementation en Python

```python
import logging
import json
from datetime import datetime
from functools import wraps

# Configuration du logger d'audit
class AuditLogger:
    """Logger d'audit conforme RGPD."""

    def __init__(self, log_file: str = "audit.log"):
        self.logger = logging.getLogger("rgpd_audit")
        self.logger.setLevel(logging.INFO)

        # Handler fichier avec rotation
        from logging.handlers import RotatingFileHandler
        handler = RotatingFileHandler(
            log_file,
            maxBytes=50 * 1024 * 1024,  # 50 MB
            backupCount=12               # 12 fichiers = ~12 mois
        )

        # Format JSON pour faciliter l'analyse
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log_event(self, event_type: str, user: str, details: dict):
        """Enregistre un evenement d'audit."""
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "user": user,
            "details": details
        }
        self.logger.info(json.dumps(event, ensure_ascii=False))

    def log_data_access(self, user: str, table: str, query_type: str,
                        record_count: int = None, columns: list = None):
        """Journalise un acces aux donnees."""
        self.log_event("DATA_ACCESS", user, {
            "table": table,
            "query_type": query_type,
            "record_count": record_count,
            "columns_accessed": columns
        })

    def log_data_modification(self, user: str, table: str, record_id: str,
                              action: str, old_values: dict = None, new_values: dict = None):
        """Journalise une modification de donnees."""
        self.log_event("DATA_MODIFICATION", user, {
            "table": table,
            "record_id": record_id,
            "action": action,  # INSERT, UPDATE, DELETE
            "old_values": old_values,
            "new_values": new_values
        })

    def log_dsar_request(self, user: str, request_type: str, data_subject: str,
                         request_id: str):
        """Journalise une demande d'exercice de droits."""
        self.log_event("DSAR_REQUEST", user, {
            "request_type": request_type,  # access, erasure, portability, etc.
            "data_subject_hash": hash(data_subject),  # Ne pas logger l'identite !
            "request_id": request_id
        })

    def log_export(self, user: str, table: str, format: str, record_count: int):
        """Journalise un export de donnees."""
        self.log_event("DATA_EXPORT", user, {
            "table": table,
            "export_format": format,
            "record_count": record_count
        })

    def log_failed_access(self, user: str, resource: str, reason: str):
        """Journalise une tentative d'acces echouee."""
        self.log_event("ACCESS_DENIED", user, {
            "resource": resource,
            "reason": reason
        })


# Decorateur pour automatiser le logging des acces
audit = AuditLogger()

def audit_data_access(table_name: str):
    """Decorateur pour logger automatiquement les acces aux donnees."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user = kwargs.get('current_user', 'unknown')
            audit.log_data_access(
                user=user,
                table=table_name,
                query_type=func.__name__
            )
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Utilisation du decorateur
@audit_data_access("customers")
def get_customer_data(customer_id: int, current_user: str = "system"):
    """Recupere les donnees d'un client."""
    # ... logique de requete ...
    return {"id": customer_id, "data": "..."}
```

### 3.3 Exemple de log genere (format JSON)

```json
{"timestamp": "2024-03-15T14:23:45.123Z", "event_type": "DATA_ACCESS", "user": "alice_engineer", "details": {"table": "customers", "query_type": "get_customer_data", "record_count": 1, "columns_accessed": ["id", "segment", "last_order"]}}
{"timestamp": "2024-03-15T14:25:12.456Z", "event_type": "DATA_MODIFICATION", "user": "bob_analyst", "details": {"table": "customers", "record_id": "42", "action": "UPDATE", "old_values": {"email": "old@email.com"}, "new_values": {"email": "new@email.com"}}}
{"timestamp": "2024-03-15T14:30:00.789Z", "event_type": "ACCESS_DENIED", "user": "charlie_ml", "details": {"resource": "raw_data.customers", "reason": "Insufficient privileges"}}
{"timestamp": "2024-03-15T15:00:00.000Z", "event_type": "DSAR_REQUEST", "user": "support_agent", "details": {"request_type": "erasure", "data_subject_hash": 7834521098, "request_id": "DSAR-2024-0042"}}
```

---

## 4. Data Lifecycle : Retention et Purge Automatique

### 4.1 Politique de retention

```
┌──────────────────────────────────────────────────────────────────┐
│              Cycle de Vie des Donnees                             │
│                                                                  │
│  Collecte → Stockage actif → Archivage → Suppression           │
│                                                                  │
│  ┌────────┐  ┌────────────┐  ┌──────────┐  ┌──────────────┐   │
│  │Collecte│─►│ Base       │─►│ Archive  │─►│ Suppression  │   │
│  │        │  │ operationn.│  │ (froid)  │  │ definitive   │   │
│  └────────┘  └────────────┘  └──────────┘  └──────────────┘   │
│              │ Acces courant│  │ Acces rare│  │ Irreversible│   │
│              │ Haute perf. │  │ Stockage  │  │             │   │
│              │             │  │ economique│  │             │   │
│                                                                  │
│  Durees type :                                                  │
│  Clients actifs : duree de la relation + 3 ans                  │
│  Prospects : 3 ans apres dernier contact                        │
│  Logs : 13 mois                                                 │
│  Factures : 10 ans (obligation legale)                          │
│  Donnees de sante : 20 ans                                      │
└──────────────────────────────────────────────────────────────────┘
```

### 4.2 DAG Airflow pour la purge automatique

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from datetime import datetime, timedelta
import psycopg2
import logging

logger = logging.getLogger(__name__)

# Configuration des regles de retention
RETENTION_RULES = [
    {
        "name": "Prospects inactifs",
        "table": "prospects",
        "condition": "last_contact_date < NOW() - INTERVAL '3 years'",
        "action": "hard_delete",
        "description": "Suppression des prospects non contactes depuis 3 ans"
    },
    {
        "name": "Logs de connexion",
        "table": "connection_logs",
        "condition": "created_at < NOW() - INTERVAL '13 months'",
        "action": "hard_delete",
        "description": "Purge des logs de connexion > 13 mois (CNIL)"
    },
    {
        "name": "Comptes supprimes",
        "table": "users",
        "condition": "is_deleted = TRUE AND deleted_at < NOW() - INTERVAL '30 days'",
        "action": "hard_delete",
        "description": "Purge definitive des comptes supprimes depuis 30 jours"
    },
    {
        "name": "Sessions expirees",
        "table": "user_sessions",
        "condition": "expires_at < NOW() - INTERVAL '7 days'",
        "action": "hard_delete",
        "description": "Nettoyage des sessions expirees"
    },
    {
        "name": "Clients inactifs - anonymisation",
        "table": "customers",
        "condition": "last_order_date < NOW() - INTERVAL '3 years' AND is_anonymized = FALSE",
        "action": "anonymize",
        "description": "Anonymisation des clients inactifs depuis 3 ans"
    }
]

def execute_retention_rule(rule: dict, **context):
    """Execute une regle de retention."""
    conn = psycopg2.connect(dsn="postgresql://...")
    cur = conn.cursor()

    if rule["action"] == "hard_delete":
        query = f"DELETE FROM {rule['table']} WHERE {rule['condition']}"
    elif rule["action"] == "anonymize":
        query = f"""
            UPDATE {rule['table']} SET
                nom = 'ANONYMISE',
                prenom = 'ANONYMISE',
                email = 'anonymise_' || id || '@removed.local',
                telephone = NULL,
                adresse = NULL,
                is_anonymized = TRUE,
                anonymized_at = NOW()
            WHERE {rule['condition']}
        """

    cur.execute(query)
    affected_rows = cur.rowcount
    conn.commit()

    logger.info(f"Regle '{rule['name']}': {affected_rows} enregistrements traites")

    # Logger l'operation dans la table d'audit
    cur.execute("""
        INSERT INTO rgpd_audit.retention_log (rule_name, table_name, action, affected_rows, executed_at)
        VALUES (%s, %s, %s, %s, NOW())
    """, (rule['name'], rule['table'], rule['action'], affected_rows))
    conn.commit()
    conn.close()

    return affected_rows

# Definition du DAG
default_args = {
    'owner': 'data-engineering',
    'depends_on_past': False,
    'email_on_failure': True,
    'email': ['data-team@xyz.com', 'dpo@xyz.com'],
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'rgpd_data_retention',
    default_args=default_args,
    description='Purge automatique des donnees conformement au RGPD',
    schedule_interval='@weekly',  # Execution hebdomadaire
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['rgpd', 'compliance', 'retention'],
)

start = DummyOperator(task_id='start', dag=dag)
end = DummyOperator(task_id='end', dag=dag)

for rule in RETENTION_RULES:
    task = PythonOperator(
        task_id=f"retention_{rule['table']}",
        python_callable=execute_retention_rule,
        op_kwargs={"rule": rule},
        dag=dag,
    )
    start >> task >> end
```

### 4.3 Planification SQL (pg_cron)

```sql
-- Alternative : utiliser pg_cron pour les purges simples
-- Installation : CREATE EXTENSION pg_cron;

-- Purge des logs chaque dimanche a 3h du matin
SELECT cron.schedule(
    'purge_connection_logs',
    '0 3 * * 0',  -- Cron : dimanche 3h00
    $$DELETE FROM connection_logs WHERE created_at < NOW() - INTERVAL '13 months'$$
);

-- Purge des sessions expirees chaque jour a minuit
SELECT cron.schedule(
    'purge_expired_sessions',
    '0 0 * * *',  -- Cron : tous les jours minuit
    $$DELETE FROM user_sessions WHERE expires_at < NOW() - INTERVAL '7 days'$$
);

-- Verifier les jobs planifies
SELECT * FROM cron.job;
```

---

## 5. Data Lineage (Lignee des Donnees)

### 5.1 Qu'est-ce que le Data Lineage ?

Le **data lineage** documente le parcours des donnees depuis leur source jusqu'a leur utilisation finale. C'est essentiel pour :
- Repondre aux demandes DSAR ("ou sont mes donnees ?")
- Comprendre l'impact d'une modification de source
- Prouver la conformite RGPD (accountability)
- Faciliter le debugging des pipelines

```
┌──────────────────────────────────────────────────────────────────┐
│                    Exemple de Data Lineage                       │
│                                                                  │
│  Sources              Transformations         Destinations      │
│                                                                  │
│  ┌──────────┐        ┌──────────────┐        ┌──────────────┐  │
│  │ API CRM  │───────►│ Extract &    │───────►│ Table        │  │
│  │ (clients)│        │ Clean        │        │ dim_customers │  │
│  └──────────┘        └──────────────┘        └──────┬───────┘  │
│                                                      │          │
│  ┌──────────┐        ┌──────────────┐        ┌──────▼───────┐  │
│  │ BDD      │───────►│ Join &       │───────►│ Table        │  │
│  │ Commandes│        │ Aggregate    │        │ fact_orders  │  │
│  └──────────┘        └──────────────┘        └──────┬───────┘  │
│                                                      │          │
│  ┌──────────┐        ┌──────────────┐        ┌──────▼───────┐  │
│  │ Logs     │───────►│ Anonymize &  │───────►│ Dashboard    │  │
│  │ Web      │        │ Aggregate    │        │ Analytics    │  │
│  └──────────┘        └──────────────┘        └──────────────┘  │
│                                                                  │
│  Chaque fleche represente un flux de donnees documente :        │
│  - Source et destination                                        │
│  - Transformations appliquees                                   │
│  - Frequence de mise a jour                                     │
│  - Donnees personnelles impliquees                              │
└──────────────────────────────────────────────────────────────────┘
```

### 5.2 Documentation du lineage

```python
# Exemple de documentation du lineage dans le code
LINEAGE = {
    "pipeline_id": "etl_customer_analytics",
    "version": "2.1",
    "sources": [
        {
            "name": "CRM API",
            "type": "api",
            "personal_data": True,
            "fields": ["customer_id", "name", "email", "segment", "created_at"],
            "refresh_frequency": "daily"
        },
        {
            "name": "Orders DB",
            "type": "postgresql",
            "personal_data": True,
            "fields": ["order_id", "customer_id", "amount", "date"],
            "refresh_frequency": "hourly"
        }
    ],
    "transformations": [
        {
            "step": 1,
            "name": "Pseudonymize",
            "description": "Hash customer_id with SHA-256 + salt",
            "input_fields": ["customer_id"],
            "output_fields": ["pseudo_customer_id"]
        },
        {
            "step": 2,
            "name": "Aggregate",
            "description": "Calculate average order value per customer segment",
            "input_fields": ["pseudo_customer_id", "amount", "segment"],
            "output_fields": ["segment", "avg_order_value", "order_count"]
        },
        {
            "step": 3,
            "name": "Remove PII",
            "description": "Drop all personally identifiable fields",
            "removed_fields": ["name", "email"]
        }
    ],
    "destinations": [
        {
            "name": "warehouse.customer_analytics",
            "type": "bigquery",
            "personal_data": False,  # Anonymise apres transformation
            "retention": "24 months"
        }
    ]
}
```

---

## 6. Data Catalog (Catalogue de Donnees)

### 6.1 Qu'est-ce qu'un Data Catalog ?

Un **data catalog** est un inventaire centralise de toutes les donnees de l'organisation, avec leurs metadonnees. C'est l'outil de reference pour savoir :
- Quelles donnees existent et ou elles se trouvent
- Qui en est responsable
- Quelles donnees sont personnelles / sensibles
- Comment elles sont classifiees

### 6.2 Classification des donnees

```
┌──────────────────────────────────────────────────────────────────┐
│            Classification des Donnees                            │
│                                                                  │
│  Niveau 1 : PUBLIQUE                                            │
│  ┌────────────────────────────────────────┐                     │
│  │ Donnees publiables sans restriction    │                     │
│  │ Ex: nom de l'entreprise, prix publics  │                     │
│  │ Mesures: aucune mesure specifique      │                     │
│  └────────────────────────────────────────┘                     │
│                                                                  │
│  Niveau 2 : INTERNE                                             │
│  ┌────────────────────────────────────────┐                     │
│  │ Donnees internes non sensibles         │                     │
│  │ Ex: organigramme, procedures internes  │                     │
│  │ Mesures: controle d'acces basique      │                     │
│  └────────────────────────────────────────┘                     │
│                                                                  │
│  Niveau 3 : CONFIDENTIEL                                        │
│  ┌────────────────────────────────────────┐                     │
│  │ Donnees personnelles, donnees business │                     │
│  │ Ex: donnees clients, CA, contrats      │                     │
│  │ Mesures: RBAC, chiffrement, audit logs │                     │
│  └────────────────────────────────────────┘                     │
│                                                                  │
│  Niveau 4 : RESTREINT / SECRET                                  │
│  ┌────────────────────────────────────────┐                     │
│  │ Donnees sensibles RGPD, secrets        │                     │
│  │ Ex: donnees sante, mots de passe, cles │                     │
│  │ Mesures: chiffrement renforce, MFA,    │                     │
│  │ acces nominatif, audit temps reel      │                     │
│  └────────────────────────────────────────┘                     │
└──────────────────────────────────────────────────────────────────┘
```

### 6.3 Exemple d'entree de catalogue

```yaml
# data_catalog/tables/raw_data_customers.yaml
---
table:
  name: "raw_data.customers"
  description: "Table principale des clients"
  owner: "data-engineering-team"
  classification: "CONFIDENTIEL"
  contains_pii: true
  contains_sensitive: false
  retention_period: "duree relation + 3 ans"
  legal_basis: "contrat"
  registered_treatment_id: "TRT-2024-001"

columns:
  - name: "id"
    type: "integer"
    description: "Identifiant technique unique"
    pii: false
    classification: "INTERNE"

  - name: "email"
    type: "varchar(255)"
    description: "Adresse email du client"
    pii: true
    pii_type: "identifiant_direct"
    classification: "CONFIDENTIEL"

  - name: "nom"
    type: "varchar(100)"
    description: "Nom de famille du client"
    pii: true
    pii_type: "identifiant_direct"
    classification: "CONFIDENTIEL"

  - name: "date_naissance"
    type: "date"
    description: "Date de naissance"
    pii: true
    pii_type: "quasi_identifiant"
    classification: "CONFIDENTIEL"

  - name: "code_postal"
    type: "varchar(5)"
    description: "Code postal de l'adresse"
    pii: true
    pii_type: "quasi_identifiant"
    classification: "CONFIDENTIEL"

  - name: "segment"
    type: "varchar(20)"
    description: "Segment commercial (gold, silver, bronze)"
    pii: false
    classification: "INTERNE"

access:
  read: ["data_engineer", "data_analyst", "dpo_auditor"]
  write: ["data_engineer"]
  admin: ["data_admin"]

lineage:
  source: "API CRM (Salesforce)"
  refresh: "quotidien (06:00 UTC)"
  downstream:
    - "warehouse.dim_customers"
    - "ml_features.customer_features"
    - "analytics.customer_dashboard"
```

---

## 7. Resume et Points Cles

### 7.1 Checklist de securite pour le Data Engineer

🔐 **Chiffrement :**
- [ ] Donnees chiffrees au repos (AES-256)
- [ ] Communications chiffrees en transit (TLS 1.2+)
- [ ] Mots de passe haches (bcrypt, argon2)
- [ ] Cles de chiffrement dans un vault (pas dans le code !)

🔐 **Controle d'acces :**
- [ ] RBAC implemente avec principe du moindre privilege
- [ ] Comptes nominatifs (pas de comptes partages)
- [ ] MFA active pour les acces administratifs
- [ ] Revue des acces trimestrielle

🔐 **Audit :**
- [ ] Logs d'acces aux donnees personnelles
- [ ] Logs de modifications (avec avant/apres)
- [ ] Logs des exercices de droits (DSAR)
- [ ] Logs des tentatives d'acces echouees

🔐 **Cycle de vie :**
- [ ] Politique de retention definie pour chaque type de donnee
- [ ] Purge automatisee (Airflow, pg_cron)
- [ ] Processus d'archivage documente
- [ ] Test de restauration des backups

🔐 **Gouvernance :**
- [ ] Data lineage documente pour chaque pipeline
- [ ] Data catalog avec classification des donnees
- [ ] Registre des traitements a jour
- [ ] DPO informe de chaque nouveau traitement

---

## 📝 Exercice Rapide

**Scenario** : Vous devez securiser un nouveau data warehouse qui contiendra :
- Les donnees clients (nom, email, commandes)
- Les donnees RH (employes, salaires)
- Les logs applicatifs
- Les modeles ML

**Questions** :
1. Definissez les roles RBAC necessaires
2. Proposez une politique de retention pour chaque type de donnees
3. Quels evenements devez-vous journaliser ?

> **Reponses** : voir [08-exercices.md](08-exercices.md)

---

[← Precedent](06-analyse-impact.md) | [🏠 Accueil](README.md) | [Suivant →](08-exercices.md)

---

**Academy** - Formation Data Engineer
