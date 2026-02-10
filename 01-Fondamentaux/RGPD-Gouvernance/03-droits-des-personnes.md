[← Precedent](02-principes-fondamentaux.md) | [🏠 Accueil](README.md) | [Suivant →](04-registre-des-traitements.md)

# 📖 Cours 3 - Droits des Personnes

## Implementer les droits RGPD dans vos systemes de donnees

---

## 1. Les 8 Droits des Personnes Concernees

Le RGPD confere aux personnes physiques 8 droits fondamentaux sur leurs donnees personnelles. En tant que Data Engineer, vous devez etre capable d'implementer **techniquement** chacun de ces droits.

### 1.1 Vue d'ensemble

```
┌──────────────────────────────────────────────────────────────────┐
│                Les 8 Droits des Personnes RGPD                   │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │ 1. INFORMA-  │  │ 2. ACCES     │  │ 3. RECTIFICATION     │  │
│  │    TION      │  │              │  │                      │  │
│  │ Art. 13-14   │  │ Art. 15      │  │ Art. 16              │  │
│  │ Savoir quoi  │  │ Obtenir une  │  │ Corriger les         │  │
│  │ et pourquoi  │  │ copie de ses │  │ donnees inexactes    │  │
│  │              │  │ donnees      │  │                      │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │ 4. EFFACE-   │  │ 5. LIMITA-   │  │ 6. PORTABILITE       │  │
│  │    MENT      │  │    TION      │  │                      │  │
│  │ Art. 17      │  │ Art. 18      │  │ Art. 20              │  │
│  │ Droit a      │  │ Geler le     │  │ Recuperer ses        │  │
│  │ l'oubli      │  │ traitement   │  │ donnees dans un      │  │
│  │              │  │              │  │ format exploitable   │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
│                                                                  │
│  ┌──────────────┐  ┌──────────────────────────────────────────┐ │
│  │ 7. OPPOSI-   │  │ 8. DECISION INDIVIDUELLE AUTOMATISEE     │ │
│  │    TION      │  │                                          │ │
│  │ Art. 21      │  │ Art. 22                                  │ │
│  │ Refuser un   │  │ Ne pas faire l'objet d'une decision      │ │
│  │ traitement   │  │ fondee uniquement sur un traitement      │ │
│  │              │  │ automatise (y compris le profilage)      │ │
│  └──────────────┘  └──────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
```

### 1.2 Droit a l'information (Articles 13-14)

Les personnes doivent etre informees de maniere **concise, transparente, comprehensible et aisement accessible** :

| Information a fournir | Exemple |
|----------------------|---------|
| Identite du responsable de traitement | "Societe XYZ, 10 rue de la Paix, Paris" |
| Coordonnees du DPO | "dpo@xyz.com" |
| Finalites du traitement | "Gestion de votre commande et livraison" |
| Base legale | "Execution du contrat de vente" |
| Destinataires | "Service logistique, transporteur DHL" |
| Transferts hors UE | "Vos donnees restent dans l'UE" |
| Duree de conservation | "3 ans apres votre derniere commande" |
| Droits de la personne | Liste des droits + droit de reclamation CNIL |

### 1.3 Droit d'acces (Article 15)

La personne peut demander une copie de **toutes** les donnees la concernant, ainsi que des informations sur le traitement.

```python
# Implementation d'un endpoint d'acces aux donnees
def get_user_data(user_id: str) -> dict:
    """
    Retourne toutes les donnees personnelles d'un utilisateur.
    Doit couvrir TOUTES les bases de donnees et systemes.
    """
    user_data = {
        "metadata": {
            "request_date": datetime.utcnow().isoformat(),
            "user_id": user_id,
            "data_controller": "Societe XYZ",
            "dpo_contact": "dpo@xyz.com"
        },
        "profile": db_users.find_one({"user_id": user_id}),
        "orders": list(db_orders.find({"user_id": user_id})),
        "support_tickets": list(db_support.find({"user_id": user_id})),
        "payment_info": get_masked_payment_info(user_id),  # Masquer le numero complet
        "consent_history": list(db_consents.find({"user_id": user_id})),
        "login_history": list(db_logs.find({"user_id": user_id})),
        "newsletter_preferences": db_newsletter.find_one({"user_id": user_id}),
        "analytics_data": get_analytics_for_user(user_id),
    }

    # Inclure aussi les informations sur le traitement
    user_data["treatment_info"] = {
        "purposes": ["Gestion des commandes", "Support client", "Amelioration du service"],
        "legal_basis": "Contrat + Consentement (newsletter)",
        "recipients": ["Service logistique", "Prestataire paiement (Stripe)"],
        "retention_period": "3 ans apres derniere commande",
        "rights": "Acces, rectification, effacement, portabilite, opposition"
    }

    return user_data
```

### 1.4 Droit de rectification (Article 16)

```sql
-- Implementation de la rectification avec historique
-- Table d'audit pour tracer les modifications
CREATE TABLE data_modifications_log (
    id SERIAL PRIMARY KEY,
    table_name VARCHAR(100) NOT NULL,
    record_id INTEGER NOT NULL,
    field_name VARCHAR(100) NOT NULL,
    old_value TEXT,
    new_value TEXT,
    modified_by VARCHAR(100) NOT NULL,
    modification_reason VARCHAR(50) DEFAULT 'rectification_request',
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Procedure de rectification avec audit
CREATE OR REPLACE PROCEDURE rectify_user_data(
    p_user_id INTEGER,
    p_field VARCHAR(100),
    p_new_value TEXT,
    p_requested_by VARCHAR(100)
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_old_value TEXT;
BEGIN
    -- Recuperer l'ancienne valeur
    EXECUTE format('SELECT %I::TEXT FROM users WHERE id = $1', p_field)
    INTO v_old_value
    USING p_user_id;

    -- Logger la modification
    INSERT INTO data_modifications_log (table_name, record_id, field_name, old_value, new_value, modified_by)
    VALUES ('users', p_user_id, p_field, v_old_value, p_new_value, p_requested_by);

    -- Effectuer la modification
    EXECUTE format('UPDATE users SET %I = $1, updated_at = NOW() WHERE id = $2', p_field)
    USING p_new_value, p_user_id;

    RAISE NOTICE 'Rectification effectuee pour user % : % = %', p_user_id, p_field, p_new_value;
END;
$$;

-- Utilisation
-- CALL rectify_user_data(42, 'email', 'nouveau@email.com', 'DSAR-2024-0042');
```

### 1.5 Droit a l'effacement - Droit a l'oubli (Article 17)

C'est le droit le plus complexe a implementer techniquement. Il implique de supprimer les donnees de **tous** les systemes.

**Quand le droit a l'effacement s'applique :**
- Les donnees ne sont plus necessaires
- La personne retire son consentement
- La personne exerce son droit d'opposition
- Le traitement est illicite
- Obligation legale d'effacement

**Quand on peut refuser l'effacement :**
- Obligation legale de conservation (factures, declarations fiscales)
- Exercice du droit a la liberte d'expression
- Motifs d'interet public dans le domaine de la sante
- Archivage dans l'interet public, recherche scientifique
- Constatation, exercice ou defense de droits en justice

### 1.6 Droit a la limitation du traitement (Article 18)

La personne peut demander le "gel" de ses donnees : elles sont conservees mais plus traitees.

```python
# Implementation de la limitation du traitement
class UserDataManager:

    def limit_processing(self, user_id: str, reason: str):
        """
        Marque un utilisateur comme 'traitement limite'.
        Les donnees sont conservees mais exclues de tout traitement.
        """
        # Marquer le profil comme limite
        db.users.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "processing_limited": True,
                    "limitation_date": datetime.utcnow(),
                    "limitation_reason": reason
                }
            }
        )

        # Exclure des pipelines de traitement
        db.processing_exclusions.insert_one({
            "user_id": user_id,
            "excluded_from": ["analytics", "marketing", "profiling", "ml_training"],
            "since": datetime.utcnow()
        })

        print(f"⚠️ Traitement limite pour {user_id}. Raison : {reason}")

    def check_processing_allowed(self, user_id: str, processing_type: str) -> bool:
        """Verifie si le traitement est autorise pour cet utilisateur."""
        exclusion = db.processing_exclusions.find_one({"user_id": user_id})
        if exclusion and processing_type in exclusion.get("excluded_from", []):
            return False
        return True
```

### 1.7 Droit a la portabilite (Article 20)

Les donnees doivent etre fournies dans un **format structure, couramment utilise et lisible par machine** (JSON, CSV, XML).

```python
import json
import csv
import io

def export_user_data_portable(user_id: str, format: str = "json") -> str:
    """
    Exporte les donnees utilisateur dans un format portable.
    Conforme a l'Article 20 du RGPD.
    """
    # Collecter toutes les donnees fournies par l'utilisateur
    # (uniquement les donnees fournies, pas les donnees deduites)
    user_data = {
        "profil": {
            "nom": db.users.find_one({"id": user_id}).get("nom"),
            "prenom": db.users.find_one({"id": user_id}).get("prenom"),
            "email": db.users.find_one({"id": user_id}).get("email"),
            "telephone": db.users.find_one({"id": user_id}).get("telephone"),
            "adresse": db.users.find_one({"id": user_id}).get("adresse"),
        },
        "commandes": [
            {
                "date": str(order["date"]),
                "produits": order["produits"],
                "montant": order["montant"]
            }
            for order in db.orders.find({"user_id": user_id})
        ],
        "preferences": db.preferences.find_one({"user_id": user_id}),
        "messages": [
            {
                "date": str(msg["date"]),
                "contenu": msg["contenu"]
            }
            for msg in db.messages.find({"user_id": user_id})
        ]
    }

    if format == "json":
        return json.dumps(user_data, indent=2, ensure_ascii=False)
    elif format == "csv":
        return convert_to_csv(user_data)
    else:
        raise ValueError(f"Format non supporte : {format}")
```

### 1.8 Droit d'opposition (Article 21)

```python
# Gestion du droit d'opposition
def handle_opposition(user_id: str, treatment_type: str):
    """
    Gere le droit d'opposition d'un utilisateur.

    Pour le prospection commerciale : opposition TOUJOURS valide, sans motif.
    Pour les autres traitements bases sur l'interet legitime :
    necessite un motif tenant a la situation particuliere.
    """
    if treatment_type == "marketing":
        # Opposition au marketing : toujours valide, sans condition
        db.marketing_exclusions.insert_one({
            "user_id": user_id,
            "excluded_since": datetime.utcnow(),
            "type": "marketing_opposition"
        })
        # Supprimer de toutes les listes de diffusion
        remove_from_all_mailing_lists(user_id)
        return {"status": "accepted", "message": "Opposition au marketing enregistree"}

    elif treatment_type == "profiling":
        # Opposition au profilage : necessite evaluation
        db.opposition_requests.insert_one({
            "user_id": user_id,
            "treatment_type": treatment_type,
            "status": "pending_review",
            "requested_at": datetime.utcnow()
        })
        return {"status": "pending", "message": "Demande d'opposition transmise au DPO"}
```

### 1.9 Droit relatif a la decision individuelle automatisee (Article 22)

> La personne a le droit de ne pas faire l'objet d'une decision fondee exclusivement sur un traitement automatise, y compris le profilage, produisant des effets juridiques ou l'affectant de maniere significative.

**Exemples concrets :**

| Systeme automatise | Effet significatif | Obligation |
|-------------------|-------------------|------------|
| Scoring credit automatique | Refus de pret | Intervention humaine requise |
| Tri automatique de CV | Non-selection | Intervention humaine requise |
| Tarification dynamique assurance | Surprime basee sur profil | Droit a l'explication |
| Modele de prediction churn | Offre de retention differenciee | Information sur la logique |
| Detection de fraude automatique | Blocage de compte | Droit de contestation |

```python
# ❌ MAUVAISE PRATIQUE : decision 100% automatisee sans recours
def process_loan_application(applicant_data):
    score = ml_model.predict_creditworthiness(applicant_data)
    if score < 0.5:
        return {"decision": "REFUSE", "reason": None}  # Pas d'explication !
    return {"decision": "ACCEPTE"}

# ✅ BONNE PRATIQUE : decision assistee avec explication et recours humain
def process_loan_application(applicant_data):
    """
    Traitement de demande de pret conforme a l'Article 22 RGPD.
    """
    # 1. Prediction du modele
    score = ml_model.predict_creditworthiness(applicant_data)

    # 2. Explication de la decision (SHAP values)
    import shap
    explainer = shap.TreeExplainer(ml_model)
    shap_values = explainer.shap_values(applicant_data)

    # 3. Facteurs principaux de la decision
    top_factors = get_top_factors(shap_values, applicant_data, n=5)

    result = {
        "score": round(score, 2),
        "recommendation": "FAVORABLE" if score >= 0.5 else "DEFAVORABLE",
        "decision_type": "RECOMMANDATION_AUTOMATIQUE",  # Pas une decision finale !
        "explanation": {
            "main_factors": top_factors,
            "description": generate_human_readable_explanation(top_factors)
        },
        "human_review_required": True,  # Toujours une revue humaine
        "contestation_info": {
            "process": "Vous pouvez contester cette recommandation",
            "contact": "reclamation@banque.fr",
            "deadline": "30 jours"
        }
    }

    # 4. Logger pour audit
    log_automated_decision(applicant_data["id"], result)

    return result
```

---

## 2. DSAR : Data Subject Access Request

### 2.1 Processus de traitement d'une DSAR

```
┌──────────────────────────────────────────────────────────────────┐
│                Processus DSAR (Demande d'Acces)                  │
│                                                                  │
│  Jour 0        Reception de la demande                          │
│  │              │                                                │
│  │              ▼                                                │
│  │         Verification d'identite (obligatoire)                │
│  │              │                                                │
│  │              ├─── Identite non confirmee → Demande de         │
│  │              │    preuves supplementaires (ne suspend pas      │
│  │              │    le delai !)                                  │
│  │              │                                                │
│  │              ▼                                                │
│  │         Identification des sources de donnees                │
│  │              │                                                │
│  │              ▼                                                │
│  │         Extraction des donnees de chaque systeme             │
│  │         (BDD, CRM, logs, backups, ML models...)              │
│  │              │                                                │
│  │              ▼                                                │
│  │         Compilation et verification                          │
│  │              │                                                │
│  │              ▼                                                │
│  │         Revue par le DPO                                     │
│  │              │                                                │
│  Jour 30  ◄────┘  Envoi de la reponse                          │
│  (max)         Format : PDF securise ou plateforme en ligne     │
│                                                                  │
│  ⚠️ Delai : 30 jours calendaires (extensible a 60 jours si     │
│     demande complexe, mais obligation d'informer sous 30 jours) │
└──────────────────────────────────────────────────────────────────┘
```

### 2.2 Automatisation d'un processus DSAR en Python

```python
import json
from datetime import datetime, timedelta
from typing import Dict, List
import hashlib

class DSARProcessor:
    """
    Processeur automatise de demandes DSAR.
    Conforme aux Articles 15-22 du RGPD.
    """

    DEADLINE_DAYS = 30

    def __init__(self, db_connections: Dict):
        self.dbs = db_connections
        self.data_sources = [
            "users_db", "orders_db", "analytics_db",
            "support_db", "marketing_db", "logs_db"
        ]

    def create_request(self, requester_email: str, request_type: str) -> Dict:
        """Cree une nouvelle demande DSAR."""
        request = {
            "id": f"DSAR-{datetime.now().strftime('%Y%m%d')}-{hashlib.md5(requester_email.encode()).hexdigest()[:6]}",
            "requester_email": requester_email,
            "type": request_type,  # "access", "erasure", "portability", "rectification"
            "status": "received",
            "created_at": datetime.utcnow().isoformat(),
            "deadline": (datetime.utcnow() + timedelta(days=self.DEADLINE_DAYS)).isoformat(),
            "identity_verified": False,
            "data_collected": {},
            "response_sent": False
        }

        self.dbs["dsar_db"].insert(request)
        self._notify_dpo(request)
        return request

    def verify_identity(self, request_id: str, verification_doc: str) -> bool:
        """Verifie l'identite du demandeur."""
        # En pratique : verification de piece d'identite, double authentification, etc.
        verified = perform_identity_check(verification_doc)
        self.dbs["dsar_db"].update(
            {"id": request_id},
            {"$set": {"identity_verified": verified}}
        )
        return verified

    def collect_all_data(self, request_id: str, user_identifier: str) -> Dict:
        """Collecte les donnees de toutes les sources."""
        all_data = {}

        for source in self.data_sources:
            try:
                data = self._extract_from_source(source, user_identifier)
                all_data[source] = {
                    "record_count": len(data) if isinstance(data, list) else 1,
                    "data": data,
                    "extracted_at": datetime.utcnow().isoformat()
                }
            except Exception as e:
                all_data[source] = {"error": str(e), "record_count": 0}

        self.dbs["dsar_db"].update(
            {"id": request_id},
            {"$set": {"data_collected": all_data, "status": "data_collected"}}
        )

        return all_data

    def generate_response(self, request_id: str, format: str = "json") -> str:
        """Genere la reponse a la demande DSAR."""
        request = self.dbs["dsar_db"].find_one({"id": request_id})

        response = {
            "request_id": request_id,
            "generated_at": datetime.utcnow().isoformat(),
            "data_controller": {
                "name": "Societe XYZ",
                "address": "10 rue de la Paix, 75002 Paris",
                "dpo_contact": "dpo@xyz.com"
            },
            "processing_info": {
                "purposes": self._get_processing_purposes(),
                "legal_bases": self._get_legal_bases(),
                "recipients": self._get_recipients(),
                "retention_periods": self._get_retention_periods(),
                "rights": self._get_rights_info()
            },
            "personal_data": request.get("data_collected", {}),
        }

        return json.dumps(response, indent=2, ensure_ascii=False, default=str)

    def _extract_from_source(self, source: str, user_id: str) -> list:
        """Extrait les donnees d'une source specifique."""
        queries = {
            "users_db": "SELECT * FROM users WHERE user_id = %s",
            "orders_db": "SELECT * FROM orders WHERE user_id = %s",
            "analytics_db": "SELECT * FROM user_events WHERE user_id = %s",
            "support_db": "SELECT * FROM tickets WHERE user_id = %s",
            "marketing_db": "SELECT * FROM campaigns_sent WHERE user_id = %s",
            "logs_db": "SELECT * FROM access_logs WHERE user_id = %s"
        }
        return self.dbs[source].execute(queries[source], (user_id,)).fetchall()

    def _notify_dpo(self, request: Dict):
        """Notifie le DPO d'une nouvelle demande."""
        send_email(
            to="dpo@xyz.com",
            subject=f"Nouvelle demande DSAR : {request['id']}",
            body=f"Type: {request['type']}\nDeadline: {request['deadline']}"
        )
```

---

## 3. Impact sur les Bases de Donnees

### 3.1 Soft Delete vs Hard Delete

Le choix entre soft delete (marquage) et hard delete (suppression physique) est crucial pour la conformite RGPD.

```
┌──────────────────────────────────────────────────────────────────┐
│               Soft Delete vs Hard Delete                         │
│                                                                  │
│  SOFT DELETE                      HARD DELETE                    │
│  ┌─────────────────────┐         ┌─────────────────────┐       │
│  │ UPDATE users         │         │ DELETE FROM users    │       │
│  │ SET deleted = true,  │         │ WHERE id = 42;      │       │
│  │     deleted_at = NOW()│         │                     │       │
│  │ WHERE id = 42;       │         │ (donnee supprimee   │       │
│  │                      │         │  physiquement)      │       │
│  │ (donnee toujours     │         └─────────────────────┘       │
│  │  en base)            │                                        │
│  └─────────────────────┘                                        │
│                                                                  │
│  ✅ Avantages soft delete   ✅ Avantages hard delete             │
│  - Reversible               - Conformite totale effacement      │
│  - Integrite referentielle  - Pas de donnee residuelle          │
│  - Audit possible           - Performance (moins de donnees)    │
│  - Obligations legales      - Simple a comprendre               │
│                                                                  │
│  ❌ Inconvenients            ❌ Inconvenients                    │
│  - Donnee toujours          - Irreversible                      │
│    presente en base         - Casse l'integrite referentielle   │
│  - Risque de fuite          - Audit impossible apres coup       │
│  - Performance              - Obligations legales ?             │
│                                                                  │
│  💡 RECOMMANDATION : Approche hybride                           │
│  Soft delete + purge differee + anonymisation des archives      │
└──────────────────────────────────────────────────────────────────┘
```

### 3.2 Implementation SQL complete du soft delete

```sql
-- Schema avec support du soft delete et des droits RGPD
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    nom VARCHAR(100),
    prenom VARCHAR(100),
    date_naissance DATE,
    telephone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Champs RGPD
    is_deleted BOOLEAN DEFAULT FALSE,
    deleted_at TIMESTAMP,
    deletion_reason VARCHAR(50),  -- 'user_request', 'retention_expired', 'admin'
    processing_limited BOOLEAN DEFAULT FALSE,
    limited_at TIMESTAMP,

    -- Index pour performance (exclure les supprimes des requetes courantes)
    CONSTRAINT idx_active_users EXCLUDE USING btree (email WITH =) WHERE (is_deleted = FALSE)
);

-- Vue pour les requetes courantes (exclut automatiquement les supprimes)
CREATE VIEW active_users AS
SELECT id, email, nom, prenom, date_naissance, telephone, created_at, updated_at
FROM users
WHERE is_deleted = FALSE AND processing_limited = FALSE;

-- Procedure de soft delete avec cascade
CREATE OR REPLACE PROCEDURE delete_user_data(p_user_id INTEGER, p_reason VARCHAR(50))
LANGUAGE plpgsql
AS $$
BEGIN
    -- 1. Soft delete de l'utilisateur
    UPDATE users SET
        is_deleted = TRUE,
        deleted_at = NOW(),
        deletion_reason = p_reason
    WHERE id = p_user_id;

    -- 2. Anonymiser les commandes (obligation comptable : garder le montant)
    UPDATE orders SET
        shipping_name = 'ANONYMISE',
        shipping_address = 'ANONYMISE',
        shipping_phone = NULL,
        customer_email = NULL,
        anonymized_at = NOW()
    WHERE user_id = p_user_id;

    -- 3. Supprimer les donnees non soumises a obligation legale
    DELETE FROM user_preferences WHERE user_id = p_user_id;
    DELETE FROM user_sessions WHERE user_id = p_user_id;
    DELETE FROM newsletter_subscriptions WHERE user_id = p_user_id;
    DELETE FROM user_consents WHERE user_id = p_user_id;

    -- 4. Anonymiser les logs (garder pour securite, anonymiser l'identite)
    UPDATE access_logs SET
        user_id = NULL,
        ip_address = 'ANONYMISE',
        user_agent = NULL
    WHERE user_id = p_user_id;

    -- 5. Logger l'operation de suppression
    INSERT INTO data_deletion_log (user_id, deletion_type, reason, performed_at)
    VALUES (p_user_id, 'soft_delete_cascade', p_reason, NOW());

    RAISE NOTICE 'Suppression effectuee pour user %', p_user_id;
END;
$$;

-- Procedure de purge definitive (a executer apres le delai legal)
CREATE OR REPLACE PROCEDURE hard_purge_deleted_users()
LANGUAGE plpgsql
AS $$
DECLARE
    v_count INTEGER;
BEGIN
    -- Purger les utilisateurs supprimes depuis plus de 30 jours
    -- (delai pour annulation eventuelle)
    DELETE FROM users
    WHERE is_deleted = TRUE
    AND deleted_at < NOW() - INTERVAL '30 days'
    RETURNING COUNT(*) INTO v_count;

    RAISE NOTICE '% utilisateurs definitivement purges', v_count;
END;
$$;
```

### 3.3 Export de donnees pour la portabilite

```sql
-- Fonction d'export des donnees utilisateur au format JSON
CREATE OR REPLACE FUNCTION export_user_data(p_user_id INTEGER)
RETURNS JSON
LANGUAGE plpgsql
AS $$
DECLARE
    v_result JSON;
BEGIN
    SELECT json_build_object(
        'export_date', NOW(),
        'profile', (
            SELECT row_to_json(u)
            FROM (SELECT nom, prenom, email, telephone, date_naissance FROM users WHERE id = p_user_id) u
        ),
        'orders', (
            SELECT json_agg(row_to_json(o))
            FROM (
                SELECT order_id, order_date, total_amount, status
                FROM orders WHERE user_id = p_user_id
            ) o
        ),
        'preferences', (
            SELECT row_to_json(p)
            FROM (SELECT * FROM user_preferences WHERE user_id = p_user_id) p
        )
    ) INTO v_result;

    RETURN v_result;
END;
$$;

-- Utilisation
-- SELECT export_user_data(42);
```

---

## 4. Impact sur les Pipelines ML

### 4.1 Model Retraining apres suppression de donnees

Lorsqu'un utilisateur exerce son droit a l'effacement, ses donnees ont potentiellement ete utilisees pour entrainer un modele ML. Que faire ?

```
┌──────────────────────────────────────────────────────────────────┐
│      Impact de l'effacement sur les modeles ML                   │
│                                                                  │
│  Scenario : Un client demande l'effacement de ses donnees       │
│  Son historique d'achats a servi a entrainer le modele de       │
│  recommandation                                                  │
│                                                                  │
│  Options :                                                       │
│                                                                  │
│  1. Re-entrainer le modele sans les donnees supprimees          │
│     ✅ Conformite maximale                                      │
│     ❌ Couteux en temps et ressources                           │
│     → Recommande si volume de suppressions significatif         │
│                                                                  │
│  2. Machine Unlearning (desapprentissage)                       │
│     ✅ Plus rapide que le re-entrainement complet               │
│     ❌ Techniques encore experimentales                         │
│     → Pour les cas ou le re-entrainement est trop couteux      │
│                                                                  │
│  3. Entrainement sur donnees anonymisees des le depart          │
│     ✅ Pas d'impact lors de l'effacement                        │
│     ❌ Possible perte de performance du modele                  │
│     → Meilleure approche Privacy by Design                      │
│                                                                  │
│  4. Differential Privacy lors de l'entrainement                 │
│     ✅ Garantie mathematique de protection                      │
│     ❌ Compromis precision/confidentialite                      │
│     → Pour les donnees sensibles                                │
└──────────────────────────────────────────────────────────────────┘
```

### 4.2 Droit a l'explication pour les decisions automatisees

```python
# Implementation du droit a l'explication avec SHAP
import shap
import numpy as np

class ExplainableModel:
    """Wrapper pour rendre un modele ML conforme a l'Article 22 RGPD."""

    def __init__(self, model, feature_names):
        self.model = model
        self.feature_names = feature_names
        self.explainer = shap.TreeExplainer(model)

    def predict_with_explanation(self, input_data):
        """
        Fait une prediction et fournit une explication comprehensible.
        Conforme au droit a l'explication (Article 22 RGPD).
        """
        # Prediction
        prediction = self.model.predict_proba(input_data)[0]

        # Calcul des SHAP values pour l'explication
        shap_values = self.explainer.shap_values(input_data)

        # Identifier les facteurs les plus influents
        feature_importance = list(zip(
            self.feature_names,
            shap_values[0] if isinstance(shap_values, list) else shap_values[0]
        ))
        feature_importance.sort(key=lambda x: abs(x[1]), reverse=True)

        # Generer une explication en langage naturel
        explanation = self._generate_explanation(prediction, feature_importance[:5])

        return {
            "prediction": {
                "class": "positif" if prediction[1] > 0.5 else "negatif",
                "confidence": round(max(prediction) * 100, 1)
            },
            "explanation": explanation,
            "top_factors": [
                {
                    "factor": name,
                    "impact": "positif" if value > 0 else "negatif",
                    "importance": round(abs(value), 4)
                }
                for name, value in feature_importance[:5]
            ],
            "human_review": True,
            "contestation_possible": True
        }

    def _generate_explanation(self, prediction, top_factors):
        """Genere une explication en francais comprehensible."""
        explanation_parts = []
        for name, value in top_factors[:3]:
            direction = "favorablement" if value > 0 else "defavorablement"
            explanation_parts.append(
                f"Votre {name} a influence {direction} la decision"
            )
        return ". ".join(explanation_parts) + "."
```

---

## 5. Resume : Matrice des Droits et Implementations

| Droit | Article | Delai | Implementation technique | Complexite |
|-------|---------|-------|------------------------|------------|
| Information | 13-14 | Au moment de la collecte | Politique de confidentialite, bandeaux | Faible |
| Acces | 15 | 30 jours | API d'export multi-sources | Moyenne |
| Rectification | 16 | 30 jours | Procedure UPDATE + audit log | Faible |
| Effacement | 17 | 30 jours | Soft delete + cascade + purge | Elevee |
| Limitation | 18 | 30 jours | Flag + exclusion des pipelines | Moyenne |
| Portabilite | 20 | 30 jours | Export JSON/CSV structure | Moyenne |
| Opposition | 21 | 30 jours | Exclusion lists + unsubscribe | Moyenne |
| Decision auto. | 22 | Variable | Explainability (SHAP) + review humaine | Elevee |

---

## 📝 Exercice Rapide

**Scenario** : Un utilisateur vous envoie l'email suivant :

> "Bonjour, je souhaite savoir quelles donnees vous avez sur moi, obtenir une copie, et supprimer mon compte ainsi que toutes mes donnees."

**Questions** :
1. Quels droits sont exerces dans cette demande ?
2. Quel est votre delai de reponse ?
3. Decrivez les etapes techniques pour traiter cette demande
4. Quelles donnees pouvez-vous eventuellement refuser de supprimer ?

> **Reponses** : voir [08-exercices.md](08-exercices.md)

---

[← Precedent](02-principes-fondamentaux.md) | [🏠 Accueil](README.md) | [Suivant →](04-registre-des-traitements.md)

---

**Academy** - Formation Data Engineer
