[🏠 Accueil](README.md) | [Suivant →](02-principes-fondamentaux.md)

# 📖 Cours 1 - Introduction et Enjeux du RGPD

## Pourquoi le RGPD est l'affaire de chaque Data Engineer et Dev IA

---

## 1. Pourquoi le RGPD Concerne les Data Engineers et les Dev IA

### 1.1 Le Data Engineer au coeur des donnees personnelles

En tant que Data Engineer ou developpeur IA, vous etes au coeur du flux de donnees. Chaque pipeline que vous construisez, chaque modele que vous entrainez, chaque base de donnees que vous administrez est susceptible de manipuler des **donnees personnelles**.

```
┌──────────────────────────────────────────────────────────────┐
│                  Cycle de vie des donnees                     │
│                                                              │
│  Collecte ──► Stockage ──► Traitement ──► Analyse ──► Purge │
│     │            │            │             │           │     │
│  Consentement  Chiffrement  Minimisation  Anonymisat° Retent°│
│  Base legale   Acces ctrl   Finalite      Pseudonym.  Droit  │
│                                                     oubli    │
│                                                              │
│  ▲ A chaque etape, le RGPD s'applique ▲                     │
└──────────────────────────────────────────────────────────────┘
```

### 1.2 Les risques concrets pour un Data Engineer

Voici des scenarios reels ou un Data Engineer peut enfreindre le RGPD sans meme s'en rendre compte :

| Scenario | Violation RGPD | Risque |
|----------|---------------|--------|
| Copier la base de production en environnement de test | Donnees personnelles dans un environnement non securise | Fuite de donnees |
| Entrainer un modele ML sur des donnees clients sans consentement specifique | Absence de base legale pour le traitement | Sanction CNIL |
| Conserver des logs contenant des IP au-dela de 13 mois | Depassement de la duree de conservation | Mise en demeure |
| Partager un dataset avec une equipe sans anonymisation | Acces non autorise a des donnees personnelles | Violation de confidentialite |
| Ne pas implementer le droit a l'effacement dans l'API | Non-respect des droits des personnes | Plainte CNIL |
| Transferer des donnees vers un service cloud US sans garanties | Transfert hors UE non conforme | Sanction financiere |

### 1.3 Qu'est-ce qu'une donnee personnelle ?

> **Definition (Article 4 RGPD)** : Toute information se rapportant a une personne physique identifiee ou identifiable, directement ou indirectement.

**Donnees directement identifiantes :**
- Nom, prenom
- Adresse email nominative
- Numero de securite sociale
- Photo du visage

**Donnees indirectement identifiantes :**
- Adresse IP
- Identifiant de cookie
- Numero de telephone
- Donnees de geolocalisation
- Identifiant publicitaire (IDFA, GAID)
- Plaque d'immatriculation

💡 **Astuce pour les Data Engineers** : En cas de doute, considerez la donnee comme personnelle. Le croisement de plusieurs donnees apparemment anonymes peut permettre la re-identification d'une personne.

```python
# Exemple : ces donnees semblent anonymes individuellement...
donnees = {
    "code_postal": "75008",
    "date_naissance": "1987-03-15",
    "profession": "cardiologue"
}
# ... mais leur combinaison peut identifier une personne unique !
# C'est le probleme de la quasi-identification
```

---

## 2. Historique : De la Loi Informatique et Libertes au RGPD

### 2.1 La France, pionniere de la protection des donnees

```
Timeline de la protection des donnees personnelles en France et en Europe
═══════════════════════════════════════════════════════════════════════════

1978 ─── Loi Informatique et Libertes (France)
  │      Premiere loi au monde sur la protection des donnees
  │      Creation de la CNIL
  │      Contexte : projet SAFARI (fichage generalise)
  │
1995 ─── Directive 95/46/CE (Europe)
  │      Harmonisation europeenne
  │      Cadre minimal pour les Etats membres
  │
2004 ─── Revision de la Loi Informatique et Libertes
  │      Transposition de la directive europeenne
  │      Renforcement des pouvoirs de la CNIL
  │
2016 ─── Adoption du RGPD (Reglement UE 2016/679)
  │      Vote le 27 avril 2016
  │      Delai de 2 ans pour mise en conformite
  │
2018 ─── Application du RGPD (25 mai 2018)
  │      Directement applicable dans tous les Etats membres
  │      Pas besoin de transposition nationale
  │
2019 ─── Premiere grosse sanction : Google 50M€ (CNIL)
  │
2021 ─── Amazon 746M€ (CNPD Luxembourg)
  │      Plus grosse sanction RGPD a ce jour
  │
2022 ─── Meta/Facebook 405M€ (DPC Irlande)
  │      Google Analytics declare non conforme (CNIL)
  │
2023 ─── Meta 1,2 milliard € (DPC Irlande)
  │      Record absolu de sanction RGPD
  │
2024+ ── AI Act europeen + RGPD
         Nouvelles obligations pour l'IA
```

### 2.2 La CNIL : gardienne des donnees en France

La **Commission Nationale de l'Informatique et des Libertes** (CNIL) est l'autorite de controle francaise. Ses missions :

| Mission | Description |
|---------|-------------|
| **Informer** | Guider les professionnels et les particuliers |
| **Controler** | Verifier la conformite des traitements (sur place, en ligne) |
| **Sanctionner** | Prononcer des amendes et des mises en demeure |
| **Accompagner** | Publier des guides, referentiels, outils (PIA) |
| **Anticiper** | Veille technologique, lab innovation |

💡 **Bon a savoir** : La CNIL dispose d'un pouvoir de controle en ligne. Elle peut scanner vos applications web et verifier la conformite de vos cookies, traceurs et formulaires de collecte sans vous prevenir.

### 2.3 RGPD vs Loi Informatique et Libertes : ce qui change

| Aspect | Loi 1978 | RGPD 2018 |
|--------|----------|-----------|
| Portee | France uniquement | Toute l'Union Europeenne |
| Approche | Declarative (declaration a la CNIL) | Responsabilisation (accountability) |
| Sanctions | Max 300 000 € | Jusqu'a 20M€ ou 4% du CA mondial |
| DPO | Optionnel | Obligatoire dans certains cas |
| Consentement | Implicite accepte | Explicite, libre, eclaire, specifique |
| Portabilite | Non prevu | Droit fondamental |
| Notification breach | 72h a la CNIL | 72h a la CNIL + information des personnes |

---

## 3. Les Sanctions : des Montants qui Font Reflechir

### 3.1 Le bareme des sanctions

Le RGPD prevoit deux niveaux de sanctions administratives :

**Niveau 1 - Jusqu'a 10 millions d'euros ou 2% du CA mondial annuel :**
- Violations liees aux obligations du responsable de traitement / sous-traitant
- Violations liees aux organismes de certification
- Violations liees aux organismes de suivi des codes de conduite

**Niveau 2 - Jusqu'a 20 millions d'euros ou 4% du CA mondial annuel :**
- Violations des principes de base du traitement (dont le consentement)
- Violations des droits des personnes concernees
- Violations des regles de transfert de donnees hors UE

### 3.2 Exemples de sanctions marquantes

```
┌────────────────────────────────────────────────────────────────┐
│              TOP 5 des sanctions RGPD (en M€)                  │
│                                                                │
│  Meta (2023)      ████████████████████████████████ 1 200 M€   │
│  Amazon (2021)    ███████████████████ 746 M€                  │
│  Meta (2022)      ██████████ 405 M€                           │
│  Google IE (2022) ████████ 150 M€ *                           │
│  Google FR (2019) ██ 50 M€ **                                 │
│                                                                │
│  * Cookies/traceurs sans consentement valide                   │
│  ** Manque de transparence et consentement non valide          │
└────────────────────────────────────────────────────────────────┘
```

### 3.3 Sanctions specifiques au monde de la data

| Entreprise | Montant | Raison | Lecon pour le Data Engineer |
|-----------|---------|--------|----------------------------|
| Clearview AI | 20 M€ | Scraping de photos pour reconnaissance faciale | Ne pas collecter de donnees biometriques sans base legale |
| Criteo | 40 M€ | Consentement non valide pour le ciblage publicitaire | Verifier la validite du consentement en amont du pipeline |
| RATP | 400 K€ | Fichier d'evaluation des agents avec donnees syndicales | Ne pas stocker de donnees sensibles sans necessite |
| Carrefour | 3 M€ | Duree de conservation excessive, information insuffisante | Implementer des politiques de retention automatiques |

### 3.4 Au-dela des amendes : les autres consequences

❌ **Consequences directes :**
- Mise en demeure publique (atteinte a la reputation)
- Interdiction temporaire ou definitive de traitement
- Suspension des flux de donnees

❌ **Consequences indirectes :**
- Perte de confiance des clients et partenaires
- Cout de mise en conformite en urgence (beaucoup plus cher qu'une demarche proactive)
- Risque de class action (action de groupe)
- Impact sur la valorisation de l'entreprise

---

## 4. Violations Concretes dans le Monde de la Data

### 4.1 Entrainement de modeles ML sur des donnees personnelles sans consentement

```python
# ❌ MAUVAISE PRATIQUE : utiliser directement les donnees clients
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Chargement direct des donnees clients avec infos personnelles
df = pd.read_sql("SELECT nom, email, age, historique_achats, score_credit FROM clients", conn)
X = df[['age', 'historique_achats', 'score_credit']]
y = df['churn']
model = RandomForestClassifier()
model.fit(X, y)  # Entrainement sur donnees personnelles brutes !

# ✅ BONNE PRATIQUE : anonymiser AVANT l'entrainement
# 1. Verifier la base legale (interet legitime documente OU consentement)
# 2. Minimiser les donnees : ne garder que les features necessaires
# 3. Anonymiser les identifiants

df = pd.read_sql("""
    SELECT
        CASE WHEN age < 25 THEN '18-24'
             WHEN age < 35 THEN '25-34'
             WHEN age < 50 THEN '35-49'
             ELSE '50+' END as tranche_age,
        historique_achats,
        score_credit,
        churn
    FROM clients
""", conn)
# Plus de nom, plus d'email, age generalise
X = df[['tranche_age', 'historique_achats', 'score_credit']]
y = df['churn']
model = RandomForestClassifier()
model.fit(X, y)
```

### 4.2 Donnees de production en environnement de test

```python
# ❌ MAUVAISE PRATIQUE : copier la prod en test
# pg_dump production_db | pg_restore test_db
# Les developpeurs ont maintenant acces a TOUTES les donnees personnelles

# ✅ BONNE PRATIQUE : script d'anonymisation pour les environnements de test
import hashlib
import pandas as pd
from faker import Faker

fake = Faker('fr_FR')

def anonymize_for_test(df):
    """Anonymise un DataFrame pour utilisation en environnement de test."""
    df_anon = df.copy()

    # Remplacer les noms par des faux noms
    df_anon['nom'] = [fake.last_name() for _ in range(len(df))]
    df_anon['prenom'] = [fake.first_name() for _ in range(len(df))]

    # Remplacer les emails
    df_anon['email'] = [fake.email() for _ in range(len(df))]

    # Generaliser les dates de naissance (garder uniquement l'annee)
    df_anon['date_naissance'] = pd.to_datetime(df_anon['date_naissance']).dt.year

    # Masquer les numeros de telephone
    df_anon['telephone'] = [fake.phone_number() for _ in range(len(df))]

    return df_anon
```

### 4.3 Conservation des donnees au-dela de la duree legale

```sql
-- ❌ MAUVAISE PRATIQUE : aucune politique de retention
-- Les donnees s'accumulent indefiniment

-- ✅ BONNE PRATIQUE : politique de retention automatisee
-- Exemple : suppression des logs de connexion apres 13 mois (recommandation CNIL)

-- Procedure de purge automatique
CREATE OR REPLACE PROCEDURE purge_old_logs()
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM connection_logs
    WHERE created_at < NOW() - INTERVAL '13 months';

    RAISE NOTICE 'Purge des logs de connexion effectuee';
END;
$$;

-- Planification (via pg_cron ou equivalent)
-- SELECT cron.schedule('purge_logs', '0 2 * * 0', 'CALL purge_old_logs()');
```

---

## 5. Les Acteurs du RGPD : Qui Fait Quoi ?

### 5.1 Les trois roles principaux

```
┌─────────────────────────────────────────────────────────────────┐
│                    Ecosysteme RGPD                               │
│                                                                 │
│  ┌──────────────────────┐                                      │
│  │  Responsable de      │  Determine les finalites et les      │
│  │  Traitement          │  moyens du traitement                │
│  │  (Data Controller)   │  Ex: votre entreprise                │
│  └──────────┬───────────┘                                      │
│             │ mandate                                           │
│  ┌──────────▼───────────┐                                      │
│  │  Sous-traitant       │  Traite les donnees pour le compte   │
│  │  (Data Processor)    │  du responsable de traitement        │
│  │                      │  Ex: hebergeur cloud, outil SaaS     │
│  └──────────────────────┘                                      │
│                                                                 │
│  ┌──────────────────────┐                                      │
│  │  DPO                 │  Veille a la conformite RGPD         │
│  │  (Data Protection    │  Conseille et controle               │
│  │   Officer)           │  Point de contact avec la CNIL       │
│  └──────────────────────┘                                      │
│                                                                 │
│  ┌──────────────────────┐                                      │
│  │  Personne Concernee  │  La personne dont les donnees        │
│  │  (Data Subject)      │  sont traitees                       │
│  │                      │  Ex: utilisateur, client, employe    │
│  └──────────────────────┘                                      │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2 Ou se situe le Data Engineer ?

Le Data Engineer n'est pas un role defini par le RGPD, mais il agit **sous l'autorite du responsable de traitement**. Son role est crucial car il :

- **Concoit** les architectures de stockage des donnees personnelles
- **Implemente** les mecanismes de securite (chiffrement, acces)
- **Developpe** les pipelines de traitement de donnees
- **Automatise** les processus de conformite (purge, anonymisation, export)
- **Documente** les flux de donnees (lineage)

### 5.3 Le DPO : votre allie

Le **Delegue a la Protection des Donnees** (DPO) est obligatoire pour :
- Les autorites et organismes publics
- Les organismes dont l'activite de base necessite un suivi regulier et systematique a grande echelle
- Les organismes traitant a grande echelle des donnees sensibles

💡 **En tant que Data Engineer, le DPO est votre premier interlocuteur pour :**
- Valider la conformite d'un nouveau pipeline de donnees
- Verifier la base legale avant un nouveau traitement
- Evaluer la necessite d'une DPIA (analyse d'impact)
- Gerer les incidents de securite (data breach)

### 5.4 La relation Responsable de Traitement / Sous-traitant

```python
# Exemple concret : quand vous utilisez un service cloud
# Votre entreprise = Responsable de Traitement
# AWS / GCP / Azure = Sous-traitant

# Le contrat de sous-traitance (Article 28 RGPD) doit preciser :
obligations_sous_traitant = {
    "instructions_documentees": True,       # Ne traite que sur instruction
    "confidentialite": True,                # Personnel soumis a confidentialite
    "securite": True,                       # Mesures techniques et organisationnelles
    "sous_traitance_ulterieure": "accord",  # Accord prealable pour sous-sous-traitance
    "assistance_droits": True,              # Aide a repondre aux demandes des personnes
    "suppression_fin_contrat": True,        # Supprime ou restitue les donnees
    "audit": True,                          # Permet les audits du responsable
    "localisation_donnees": "UE"            # Localisation des serveurs
}
```

---

## 6. Le RGPD et l'Intelligence Artificielle

### 6.1 Les defis specifiques de l'IA

L'IA pose des defis uniques en matiere de protection des donnees :

| Defi | Probleme RGPD | Solution |
|------|---------------|----------|
| Donnees d'entrainement massives | Minimisation des donnees | Techniques de selection de features, donnees synthetiques |
| Biais algorithmiques | Equite, non-discrimination | Audit de biais, equite algorithmique |
| Decisions automatisees | Droit a l'explication (Art. 22) | Modeles interpretables, SHAP/LIME |
| Memorisation dans les modeles | Fuite de donnees personnelles | Differential privacy, federated learning |
| Scraping web pour LLM | Base legale pour la collecte | Consentement, interet legitime documente |

### 6.2 L'AI Act europeen et le RGPD

Depuis 2024, l'**AI Act** (Reglement europeen sur l'IA) vient completer le RGPD :

- **IA a risque inacceptable** : interdite (scoring social, reconnaissance faciale de masse)
- **IA a haut risque** : obligations strictes (recrutement, credit scoring, sante)
- **IA a risque limite** : obligations de transparence (chatbots, deepfakes)
- **IA a risque minimal** : pas d'obligations specifiques

💡 **Pour le Data Engineer / Dev IA** : Verifiez systematiquement la classification de risque de votre systeme IA et les obligations qui en decoulent, en plus de la conformite RGPD.

---

## 7. Resume et Points Cles

### 7.1 A retenir

✅ **Le RGPD concerne tous les metiers de la data**, pas seulement les juristes

✅ **Une donnee personnelle** = toute information permettant d'identifier directement ou indirectement une personne

✅ **Les sanctions sont lourdes** : jusqu'a 4% du CA mondial ou 20M€

✅ **Le Data Engineer est en premiere ligne** : il concoit et opere les systemes qui traitent les donnees personnelles

✅ **Le DPO est votre allie** : consultez-le avant chaque nouveau projet data

✅ **L'IA amplifie les enjeux** : donnees massives, decisions automatisees, biais

### 7.2 Checklist du Data Engineer RGPD-aware

- [ ] Je connais la base legale de chaque traitement que j'implemente
- [ ] Je ne copie jamais de donnees de production en environnement de test sans anonymisation
- [ ] Mes pipelines respectent le principe de minimisation des donnees
- [ ] J'ai implemente des mecanismes de retention automatique
- [ ] Je sais qui est le DPO de mon organisation et comment le contacter
- [ ] Je documente les flux de donnees (data lineage)
- [ ] Je chiffre les donnees au repos et en transit
- [ ] Je suis capable de repondre a une demande d'acces ou d'effacement

---

## 📝 Exercice Rapide

**Question** : Pour chacune des situations suivantes, indiquez si le RGPD s'applique et pourquoi.

1. Vous stockez des adresses IP dans vos logs Apache
2. Vous analysez des donnees de vente agregees par region (sans detail client)
3. Vous entrainez un modele de NLP sur des emails clients
4. Vous utilisez des donnees meteo publiques dans votre pipeline
5. Vous gerez une base de donnees de CV pour le recrutement

> **Reponses** : voir [08-exercices.md](08-exercices.md)

---

[🏠 Accueil](README.md) | [Suivant →](02-principes-fondamentaux.md)

---

**Academy** - Formation Data Engineer
