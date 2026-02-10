[← Precedent](07-securite-gouvernance.md) | [🏠 Accueil](README.md)

# 📝 Exercices - RGPD & Gouvernance des Donnees

## Mettez en pratique vos connaissances

---

## Niveau 1 - Quiz (15 Questions)

### Questions

**Q1.** Quel est le montant maximal d'une amende RGPD pour les violations les plus graves ?

- A) 10 millions d'euros ou 2% du CA mondial
- B) 20 millions d'euros ou 4% du CA mondial
- C) 50 millions d'euros ou 10% du CA mondial
- D) Pas de montant maximal

---

**Q2.** Parmi les donnees suivantes, laquelle n'est PAS consideree comme une donnee personnelle au sens du RGPD ?

- A) Une adresse IP
- B) Le chiffre d'affaires annuel d'une entreprise (personne morale)
- C) Un identifiant de cookie
- D) Un numero de telephone

---

**Q3.** Combien de bases legales le RGPD prevoit-il pour justifier un traitement de donnees personnelles ?

- A) 3
- B) 4
- C) 6
- D) 8

---

**Q4.** Quel est le delai maximum pour repondre a une demande d'exercice de droits (DSAR) ?

- A) 15 jours
- B) 30 jours
- C) 60 jours
- D) 90 jours

---

**Q5.** Quelle est la difference fondamentale entre anonymisation et pseudonymisation ?

- A) L'anonymisation est plus rapide a implementer
- B) L'anonymisation est irreversible, la pseudonymisation est reversible
- C) La pseudonymisation offre une meilleure protection
- D) Il n'y a pas de difference, ce sont des synonymes

---

**Q6.** Quand une DPIA (Analyse d'Impact) est-elle obligatoire selon le CEPD ?

- A) Pour tout traitement de donnees personnelles
- B) Quand au moins 2 des 9 criteres du CEPD sont remplis
- C) Uniquement pour les donnees sensibles
- D) Uniquement pour les entreprises de plus de 250 salaries

---

**Q7.** Quel algorithme est recommande pour le hachage des mots de passe ?

- A) MD5
- B) SHA-1
- C) SHA-256 seul
- D) bcrypt

---

**Q8.** Quelle est la duree maximale de conservation recommandee par la CNIL pour les cookies et traceurs ?

- A) 6 mois
- B) 13 mois
- C) 24 mois
- D) Illimitee si consentement

---

**Q9.** Le principe de "Privacy by Default" signifie que :

- A) Toutes les donnees doivent etre chiffrees
- B) Les options les plus protectrices de la vie privee sont activees par defaut
- C) Il faut demander l'autorisation de la CNIL avant tout traitement
- D) Seul le DPO peut acceder aux donnees personnelles

---

**Q10.** Dans le cadre du RBAC (Role-Based Access Control), le principe du moindre privilege signifie :

- A) Chaque utilisateur a un mot de passe minimal
- B) Les administrateurs ont moins de droits que les utilisateurs
- C) Chaque utilisateur ne dispose que des permissions strictement necessaires a sa tache
- D) L'acces est limite aux heures de bureau

---

**Q11.** Qu'est-ce que le k-anonymat ?

- A) Un algorithme de chiffrement utilisant k cles
- B) Une technique garantissant que chaque combinaison de quasi-identifiants apparait au moins k fois
- C) Un protocole de communication anonyme entre k serveurs
- D) Une methode de hachage avec k iterations

---

**Q12.** Le registre des traitements (Article 30) est obligatoire pour :

- A) Uniquement les entreprises de plus de 250 salaries
- B) Uniquement les entreprises traitant des donnees sensibles
- C) En pratique, quasiment toutes les entreprises traitant des donnees personnelles
- D) Uniquement les entreprises du secteur de la sante

---

**Q13.** Quelle base legale est la plus appropriee pour un pipeline ETL de gestion des commandes e-commerce ?

- A) Consentement
- B) Contrat
- C) Interet legitime
- D) Obligation legale

---

**Q14.** L'Article 22 du RGPD concerne :

- A) Le droit a la portabilite des donnees
- B) Le droit de ne pas faire l'objet d'une decision fondee exclusivement sur un traitement automatise
- C) L'obligation de notifier les violations de donnees
- D) Le droit a l'effacement

---

**Q15.** Parmi les elements suivants, lequel ne fait PAS partie des 6 principes fondamentaux du RGPD (Article 5) ?

- A) Minimisation des donnees
- B) Exactitude
- C) Gratuite
- D) Integrite et confidentialite

---

### Solutions du Quiz

<details>
<summary>Cliquez pour afficher les reponses</summary>

| Question | Reponse | Explication |
|----------|---------|-------------|
| Q1 | **B** | 20M€ ou 4% du CA mondial annuel (le montant le plus eleve) pour les violations les plus graves (Art. 83.5) |
| Q2 | **B** | Le RGPD protege les personnes physiques, pas les personnes morales. Le CA d'une entreprise n'est pas une donnee personnelle |
| Q3 | **C** | 6 bases legales : consentement, contrat, obligation legale, interets vitaux, mission d'interet public, interets legitimes (Art. 6) |
| Q4 | **B** | 30 jours calendaires, extensible a 60 jours supplementaires pour les demandes complexes (Art. 12.3) |
| Q5 | **B** | L'anonymisation est irreversible (les donnees ne sont plus personnelles), la pseudonymisation est reversible avec la cle (les donnees restent personnelles) |
| Q6 | **B** | Le CEPD a defini 9 criteres ; si au moins 2 sont remplis, la DPIA est obligatoire (lignes directrices WP248) |
| Q7 | **D** | bcrypt (ou argon2, scrypt) car il integre un sel automatique et un cout adaptatif. MD5 et SHA-1 sont vulnerables, SHA-256 seul n'a pas de sel |
| Q8 | **B** | 13 mois maximum (recommandation CNIL sur les cookies et traceurs) |
| Q9 | **B** | Privacy by Default = les parametres les plus protecteurs sont actives par defaut, sans action de l'utilisateur (Art. 25.2) |
| Q10 | **C** | Le moindre privilege = chaque acteur (utilisateur, processus) ne dispose que des droits strictement necessaires |
| Q11 | **B** | Le k-anonymat garantit que chaque individu est indistinguable d'au moins k-1 autres dans le jeu de donnees |
| Q12 | **C** | En pratique, toutes les entreprises, car les exceptions (< 250 salaries + traitement occasionnel + pas de risque) sont tres rares |
| Q13 | **B** | Contrat : le traitement des donnees est necessaire a l'execution de la commande (livraison, facturation) |
| Q14 | **B** | L'Article 22 protege contre les decisions entierement automatisees produisant des effets juridiques ou significatifs |
| Q15 | **C** | La gratuite n'est pas un principe du RGPD. Les 6 principes sont : liceite/loyaute/transparence, limitation des finalites, minimisation, exactitude, limitation de la conservation, integrite/confidentialite |

</details>

---

## Niveau 2 - Cas Pratiques

### Exercice 2.1 : Rediger un Registre des Traitements

**Scenario** : L'entreprise "HealthFit" developpe une application mobile de suivi sportif. L'application :
- Collecte les donnees GPS pendant les sessions de course a pied
- Mesure la frequence cardiaque via un bracelet connecte
- Stocke l'age, le poids et la taille de l'utilisateur
- Calcule des statistiques de performance
- Envoie des notifications push de motivation
- Partage un classement anonymise entre amis

**Mission** : Redigez la fiche complete du registre des traitements pour cette application.

**Points a couvrir** :
1. Identifiez les categories de donnees (dont les donnees sensibles)
2. Determinez la base legale appropriee
3. Listez les destinataires
4. Definissez les durees de conservation
5. Proposez les mesures de securite

<details>
<summary>Cliquez pour afficher la correction</summary>

### Correction - Registre HealthFit

| Champ | Valeur |
|-------|--------|
| **Identifiant** | TRT-2024-010 |
| **Nom du traitement** | Application mobile HealthFit - Suivi sportif |
| **Responsable** | HealthFit SAS, 15 rue du Sport, 75001 Paris |
| **DPO** | dpo@healthfit.fr |
| **Statut** | Actif |
| **Finalite(s)** | 1. Suivi de l'activite sportive de l'utilisateur 2. Calcul de statistiques de performance 3. Envoi de notifications de motivation 4. Classement social entre amis |
| **Base legale** | **Consentement explicite** (Art. 9.2.a) car traitement de donnees de sante (frequence cardiaque) + **Contrat** pour le fonctionnement de base de l'application |
| **Categories de personnes** | Utilisateurs de l'application (> 16 ans) |
| **Categories de donnees** | **Donnees d'identification** : pseudo, email, age **Donnees de sante (SENSIBLES)** : frequence cardiaque, poids, taille, IMC calcule **Donnees de geolocalisation** : traces GPS des sessions **Donnees d'usage** : statistiques de course, objectifs |
| **Donnees sensibles** | **OUI** - Frequence cardiaque = donnee de sante (Art. 9) |
| **Source des donnees** | Collecte directe aupres de l'utilisateur (saisie + capteurs) |
| **Destinataires internes** | Equipe Dev (maintenance), Equipe Data (analytics anonymisees) |
| **Destinataires externes** | Hebergement cloud OVH (France), service de notifications Firebase (Google - transfert hors UE avec clauses contractuelles types) |
| **Transfert hors UE** | Oui - Firebase (Google LLC, USA) - Clauses contractuelles types |
| **Duree de conservation** | - Compte actif : duree de vie du compte - Compte supprime : suppression sous 30 jours - Donnees de sante : suppression immediate sur demande - Traces GPS : 24 mois glissants - Statistiques anonymisees : conservation illimitee |
| **Mesures de securite** | - Consentement explicite pour les donnees de sante (ecran dedie) - Chiffrement au repos AES-256 (donnees de sante) - Chiffrement en transit TLS 1.3 - Stockage des donnees de sante separe (base chiffree specifique) - Authentification forte (MFA) pour le back-office - RBAC : acces aux donnees de sante limite a 2 personnes - Logs d'acces sur les donnees de sante - Pseudonymisation pour le classement social - Audit de securite annuel |
| **DPIA necessaire** | **OUI** (donnees de sante a grande echelle + geolocalisation + donnees sensibles) |

**Points cles de la correction :**

✅ La frequence cardiaque est une **donnee de sante** (donnee sensible au sens du RGPD) → consentement explicite obligatoire

✅ Les traces GPS sont des **donnees de geolocalisation** → risque de surveillance → DPIA necessaire

✅ Le transfert vers Firebase (Google) constitue un **transfert hors UE** → necessite des garanties (CCT)

✅ Le classement entre amis necessite une **pseudonymisation** pour ne pas reveler l'identite aux tiers

</details>

---

### Exercice 2.2 : Mini-DPIA

**Scenario** : L'entreprise "RecrutPlus" souhaite deployer un systeme d'IA pour le tri automatique de CV. Le systeme :
- Recoit les CV par email et via un formulaire web
- Extrait automatiquement les informations (NLP)
- Attribue un score de pertinence (0-100) base sur le poste
- Classe les candidats en 3 categories : "Entretien", "Vivier", "Non retenu"
- Envoie automatiquement un email de reponse aux "Non retenus"

**Mission** : Realisez une mini-DPIA en repondant aux questions suivantes :

1. **La DPIA est-elle obligatoire ?** Identifiez les criteres du CEPD concernes.
2. **Description du traitement** : completez un tableau descriptif.
3. **Risques** : identifiez au moins 4 risques (gravite + probabilite).
4. **Mesures** : proposez des mesures d'attenuation pour chaque risque.

<details>
<summary>Cliquez pour afficher la correction</summary>

### Correction - Mini-DPIA RecrutPlus

**1. La DPIA est obligatoire (au moins 4 criteres remplis) :**

| Critere CEPD | Rempli ? | Justification |
|-------------|----------|---------------|
| Evaluation/scoring | ✅ OUI | Score de pertinence des candidats |
| Decision automatisee avec effet juridique | ✅ OUI | Email de refus automatique = effet significatif |
| Donnees a grande echelle | ✅ OUI | Potentiellement des milliers de CV |
| Usage innovant de technologies | ✅ OUI | NLP / IA pour l'extraction et le scoring |
| Personnes vulnerables | ✅ OUI (potentiellement) | Candidats = situation de dependance economique |

→ **5 criteres sur 9 remplis : DPIA OBLIGATOIRE**

**2. Description du traitement :**

| Element | Description |
|---------|-------------|
| **Finalite** | Tri automatique des candidatures pour optimiser le processus de recrutement |
| **Base legale** | Interet legitime (balance des interets a documenter soigneusement) OU consentement explicite du candidat |
| **Donnees traitees** | CV complet (nom, prenom, email, telephone, adresse, photo, experience, formation, competences, centres d'interet) |
| **Donnees sensibles potentielles** | Photo (origine ethnique potentielle), centres d'interet (convictions religieuses/politiques potentielles), situation de handicap |
| **Personnes concernees** | Candidats a l'embauche |
| **Volume estimatif** | 5 000 a 50 000 CV par an |

**3. Risques identifies :**

| # | Risque | Gravite | Probabilite | Score |
|---|--------|---------|-------------|-------|
| R1 | **Biais discriminatoire** : le modele reproduit des biais historiques (genre, age, origine) | 4 - Maximale | 3 - Importante | **12** |
| R2 | **Decision sans recours** : un candidat competent est automatiquement rejete sans possibilite de contestation | 3 - Importante | 3 - Importante | **9** |
| R3 | **Traitement de donnees sensibles** : extraction non controlee de l'origine ethnique via la photo ou le nom | 4 - Maximale | 2 - Limitee | **8** |
| R4 | **Fuite de CV** : acces non autorise a la base de CV (donnees personnelles detaillees) | 3 - Importante | 2 - Limitee | **6** |
| R5 | **Conservation excessive** : CV conserves au-dela de la duree legale (2 ans max) | 2 - Limitee | 3 - Importante | **6** |
| R6 | **Manque de transparence** : les candidats ne savent pas qu'un algorithme decide de leur sort | 3 - Importante | 3 - Importante | **9** |

**4. Mesures d'attenuation :**

| Risque | Mesures | Score apres |
|--------|---------|-------------|
| **R1** Biais | - Audit de biais avant deploiement (metriques de fairness par genre, age, origine) - Retrait de la photo, du nom et de l'age du processus de scoring - Test A/B : comparer les decisions IA vs humaines - Re-audit trimestriel du modele - Dataset d'entrainement diversifie et equilibre | 12 → **4** |
| **R2** Sans recours | - JAMAIS de rejet 100% automatique (intervention humaine obligatoire Art. 22) - Mecanisme de contestation facile (lien dans l'email) - Revue humaine de tous les "Non retenus" avant envoi de l'email - Droit a l'explication du score | 9 → **3** |
| **R3** Donnees sensibles | - Suppression systematique des photos avant traitement NLP - Anonymisation du nom/prenom pour le scoring (le recruteur ne voit le nom qu'apres le scoring) - Exclusion des champs "centres d'interet" du scoring - Pas de stockage de categories ethniques/religieuses | 8 → **2** |
| **R4** Fuite | - Chiffrement de la base de CV (AES-256) - RBAC strict (seuls les recruteurs du poste concerne) - MFA pour l'acces - Logs d'acces a chaque CV | 6 → **3** |
| **R5** Conservation | - Purge automatique apres 24 mois - Consentement renouvele pour le vivier - Droit de retrait a tout moment | 6 → **2** |
| **R6** Transparence | - Mention explicite dans l'annonce : "Les candidatures sont pre-selectionnees avec l'aide d'un algorithme" - Information claire dans le formulaire de candidature - Score et criteres communicables sur demande | 9 → **3** |

**Conclusion** : Apres mesures d'attenuation, tous les risques sont ramenes a un niveau acceptable (score <= 4). Le risque de biais discriminatoire (R1) reste le plus eleve et necessite un suivi particulier.

⚠️ **Recommandation forte** : ne JAMAIS envoyer d'email de refus automatique sans validation humaine. L'Article 22 du RGPD l'interdit pour les decisions produisant des effets significatifs.

</details>

---

## Niveau 3 - Exercices Avances

### Exercice 3.1 : Script Python d'anonymisation d'un dataset CSV

**Enonce** : Ecrivez un script Python complet qui :

1. Lit un fichier CSV contenant : `id, nom, prenom, email, date_naissance, code_postal, telephone, salaire, departement_entreprise`
2. Applique les transformations suivantes :
   - Supprime `nom`, `prenom`, `telephone`
   - Hache `email` avec SHA-256 + sel pour creer un `pseudo_id`
   - Remplace `id` par le `pseudo_id`
   - Generalise `date_naissance` en tranche d'age
   - Generalise `code_postal` en departement (2 premiers chiffres)
   - Generalise `salaire` en tranches
3. Verifie le k-anonymat (k >= 3) sur les quasi-identifiants
4. Exporte le resultat dans un nouveau fichier CSV

<details>
<summary>Cliquez pour afficher la correction</summary>

```python
#!/usr/bin/env python3
"""
Script d'anonymisation de dataset CSV - Conforme RGPD
Formation Data Engineer - Exercice 3.1
"""

import pandas as pd
import hashlib
import sys
from datetime import datetime
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

# Sel pour le hachage (en production : variable d'environnement)
HASH_SALT = "formation_rgpd_2024_secret"

# Colonnes a supprimer (identifiants directs)
COLUMNS_TO_DROP = ['nom', 'prenom', 'telephone']

# Tranches d'age pour la generalisation
AGE_BINS = [0, 25, 35, 45, 55, 65, 100]
AGE_LABELS = ['18-24', '25-34', '35-44', '45-54', '55-64', '65+']

# Tranches de salaire pour la generalisation
SALARY_BINS = [0, 25000, 35000, 45000, 60000, 80000, float('inf')]
SALARY_LABELS = ['<25k', '25-35k', '35-45k', '45-60k', '60-80k', '80k+']

# Seuil de k-anonymat
K_THRESHOLD = 3


# ============================================================
# FONCTIONS D'ANONYMISATION
# ============================================================

def hash_with_salt(value: str, salt: str = HASH_SALT) -> str:
    """Hache une valeur avec un sel en utilisant SHA-256."""
    salted = f"{salt}:{value}"
    return hashlib.sha256(salted.encode()).hexdigest()[:16]


def compute_age(date_naissance: str) -> int:
    """Calcule l'age a partir d'une date de naissance."""
    try:
        birth = pd.to_datetime(date_naissance)
        today = datetime.now()
        age = (today - birth).days // 365
        return age
    except Exception:
        return None


def generalize_age(age: int) -> str:
    """Generalise un age en tranche d'age."""
    if age is None:
        return 'inconnu'
    for i, (low, high) in enumerate(zip(AGE_BINS[:-1], AGE_BINS[1:])):
        if low <= age < high:
            return AGE_LABELS[i]
    return AGE_LABELS[-1]


def generalize_postal_code(code_postal: str) -> str:
    """Generalise un code postal en departement (2 premiers chiffres)."""
    if pd.isna(code_postal):
        return 'inconnu'
    code = str(code_postal).strip()
    if len(code) >= 2:
        return code[:2]
    return 'inconnu'


def generalize_salary(salaire: float) -> str:
    """Generalise un salaire en tranche."""
    if pd.isna(salaire):
        return 'inconnu'
    for i, (low, high) in enumerate(zip(SALARY_BINS[:-1], SALARY_BINS[1:])):
        if low <= salaire < high:
            return SALARY_LABELS[i]
    return SALARY_LABELS[-1]


def check_k_anonymity(df: pd.DataFrame, quasi_identifiers: list, k: int) -> dict:
    """Verifie le k-anonymat d'un DataFrame."""
    if not quasi_identifiers:
        return {'is_k_anonymous': True, 'k_achieved': float('inf')}

    groups = df.groupby(quasi_identifiers).size()
    min_group = groups.min()
    violating = groups[groups < k]

    result = {
        'k_target': k,
        'k_achieved': int(min_group),
        'is_k_anonymous': min_group >= k,
        'total_groups': len(groups),
        'violating_groups': len(violating),
        'records_at_risk': int(violating.sum()) if len(violating) > 0 else 0,
        'total_records': len(df)
    }

    return result


# ============================================================
# PIPELINE PRINCIPAL
# ============================================================

def anonymize_csv(input_path: str, output_path: str):
    """
    Pipeline d'anonymisation complet.

    Etapes :
    1. Lecture du CSV
    2. Suppression des identifiants directs
    3. Pseudonymisation de l'email -> pseudo_id
    4. Generalisation des quasi-identifiants
    5. Verification du k-anonymat
    6. Export du resultat
    """
    print("=" * 60)
    print("PIPELINE D'ANONYMISATION RGPD")
    print("=" * 60)

    # 1. Lecture
    print("\n[1/6] Lecture du fichier source...")
    df = pd.read_csv(input_path)
    print(f"      {len(df)} enregistrements, {len(df.columns)} colonnes")
    print(f"      Colonnes : {list(df.columns)}")

    # 2. Suppression des identifiants directs
    print("\n[2/6] Suppression des identifiants directs...")
    cols_to_drop = [c for c in COLUMNS_TO_DROP if c in df.columns]
    df_anon = df.drop(columns=cols_to_drop)
    print(f"      Colonnes supprimees : {cols_to_drop}")

    # 3. Pseudonymisation email -> pseudo_id
    print("\n[3/6] Pseudonymisation (email -> pseudo_id)...")
    if 'email' in df_anon.columns:
        df_anon['pseudo_id'] = df_anon['email'].apply(
            lambda x: hash_with_salt(str(x)) if pd.notna(x) else 'unknown'
        )
        df_anon = df_anon.drop(columns=['email'])
    if 'id' in df_anon.columns:
        df_anon = df_anon.drop(columns=['id'])
    print(f"      pseudo_id genere (SHA-256 + sel, tronque a 16 caracteres)")

    # 4. Generalisation des quasi-identifiants
    print("\n[4/6] Generalisation des quasi-identifiants...")

    # Age
    if 'date_naissance' in df_anon.columns:
        df_anon['tranche_age'] = df_anon['date_naissance'].apply(
            lambda x: generalize_age(compute_age(x))
        )
        df_anon = df_anon.drop(columns=['date_naissance'])
        print("      date_naissance -> tranche_age")

    # Code postal
    if 'code_postal' in df_anon.columns:
        df_anon['departement'] = df_anon['code_postal'].apply(generalize_postal_code)
        df_anon = df_anon.drop(columns=['code_postal'])
        print("      code_postal -> departement (2 chiffres)")

    # Salaire
    if 'salaire' in df_anon.columns:
        df_anon['tranche_salaire'] = df_anon['salaire'].apply(generalize_salary)
        df_anon = df_anon.drop(columns=['salaire'])
        print("      salaire -> tranche_salaire")

    # 5. Verification du k-anonymat
    print(f"\n[5/6] Verification du k-anonymat (k >= {K_THRESHOLD})...")
    quasi_ids = [c for c in ['tranche_age', 'departement', 'departement_entreprise'] if c in df_anon.columns]
    k_result = check_k_anonymity(df_anon, quasi_ids, K_THRESHOLD)

    print(f"      Quasi-identifiants verifies : {quasi_ids}")
    print(f"      K atteint : {k_result['k_achieved']}")
    print(f"      Nombre de groupes : {k_result['total_groups']}")

    if k_result['is_k_anonymous']:
        print(f"      RESULTAT : k-anonymat RESPECTE (k = {k_result['k_achieved']})")
    else:
        print(f"      RESULTAT : k-anonymat NON RESPECTE !")
        print(f"      {k_result['violating_groups']} groupes en violation")
        print(f"      {k_result['records_at_risk']} enregistrements a risque")
        print(f"      RECOMMANDATION : generaliser davantage les quasi-identifiants")

    # 6. Export
    print(f"\n[6/6] Export du fichier anonymise...")
    df_anon.to_csv(output_path, index=False)
    print(f"      Fichier exporte : {output_path}")
    print(f"      {len(df_anon)} enregistrements, {len(df_anon.columns)} colonnes")
    print(f"      Colonnes : {list(df_anon.columns)}")

    print("\n" + "=" * 60)
    print("ANONYMISATION TERMINEE")
    print("=" * 60)

    return df_anon


# ============================================================
# POINT D'ENTREE
# ============================================================

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python anonymize.py <input.csv> <output.csv>")
        print("Exemple: python anonymize.py clients.csv clients_anonymise.csv")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not Path(input_file).exists():
        print(f"Erreur : fichier '{input_file}' introuvable")
        sys.exit(1)

    anonymize_csv(input_file, output_file)
```

**Pour tester**, creez un fichier `test_data.csv` :

```csv
id,nom,prenom,email,date_naissance,code_postal,telephone,salaire,departement_entreprise
1,Dupont,Jean,jean.dupont@email.fr,1987-03-15,75008,0612345678,45000,Marketing
2,Martin,Sophie,sophie.martin@email.fr,1992-07-22,69001,0623456789,38000,Marketing
3,Durand,Paul,paul.durand@email.fr,1975-11-08,13001,0634567890,62000,IT
4,Leroy,Marie,marie.leroy@email.fr,1988-01-30,31000,0645678901,41000,RH
5,Moreau,Pierre,pierre.moreau@email.fr,1995-06-14,75015,0656789012,35000,IT
6,Simon,Isabelle,isabelle.simon@email.fr,1982-09-03,69003,0667890123,52000,Finance
7,Laurent,Thomas,thomas.laurent@email.fr,1990-12-25,75011,0678901234,48000,Marketing
8,Michel,Claire,claire.michel@email.fr,1978-04-17,13008,0689012345,55000,IT
```

Puis executez : `python anonymize.py test_data.csv output.csv`

</details>

---

### Exercice 3.2 : SQL - Soft Delete + RBAC

**Enonce** : Ecrivez les scripts SQL (PostgreSQL) pour :

1. Creer une table `customers` avec support du soft delete
2. Creer une procedure de soft delete en cascade (anonymiser les commandes liees)
3. Creer les roles RBAC : `customer_service` (lecture + soft delete), `data_analyst` (lecture vues anonymisees), `admin` (tout)
4. Creer une vue anonymisee pour les analystes
5. Creer une table d'audit qui trace toutes les suppressions

<details>
<summary>Cliquez pour afficher la correction</summary>

```sql
-- ================================================================
-- EXERCICE 3.2 : SOFT DELETE + RBAC
-- Formation Data Engineer - RGPD
-- ================================================================

-- ============================================================
-- 1. TABLE CUSTOMERS AVEC SOFT DELETE
-- ============================================================

CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    date_naissance DATE,
    telephone VARCHAR(20),
    adresse TEXT,
    ville VARCHAR(100),
    code_postal VARCHAR(10),
    segment VARCHAR(20) DEFAULT 'standard',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Champs RGPD soft delete
    is_deleted BOOLEAN DEFAULT FALSE,
    deleted_at TIMESTAMP,
    deletion_reason VARCHAR(100),
    deletion_requested_by VARCHAR(100),

    -- Champ limitation du traitement
    processing_limited BOOLEAN DEFAULT FALSE,
    limited_at TIMESTAMP
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    amount DECIMAL(10, 2),
    status VARCHAR(20),
    shipping_name VARCHAR(200),
    shipping_address TEXT,
    shipping_phone VARCHAR(20),
    is_anonymized BOOLEAN DEFAULT FALSE,
    anonymized_at TIMESTAMP
);

-- Index pour performance
CREATE INDEX idx_customers_active ON customers(id) WHERE is_deleted = FALSE;
CREATE INDEX idx_customers_deleted ON customers(deleted_at) WHERE is_deleted = TRUE;
CREATE INDEX idx_orders_customer ON orders(customer_id);

-- ============================================================
-- 2. TABLE D'AUDIT
-- ============================================================

CREATE TABLE deletion_audit_log (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER,
    action VARCHAR(50) NOT NULL,
    details JSONB,
    performed_by VARCHAR(100) NOT NULL,
    performed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- 3. PROCEDURE DE SOFT DELETE EN CASCADE
-- ============================================================

CREATE OR REPLACE PROCEDURE soft_delete_customer(
    p_customer_id INTEGER,
    p_reason VARCHAR(100),
    p_requested_by VARCHAR(100)
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_customer_email VARCHAR(255);
    v_orders_count INTEGER;
BEGIN
    -- Verifier que le client existe et n'est pas deja supprime
    SELECT email INTO v_customer_email
    FROM customers
    WHERE id = p_customer_id AND is_deleted = FALSE;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Client % non trouve ou deja supprime', p_customer_id;
    END IF;

    -- 1. Soft delete du client
    UPDATE customers SET
        is_deleted = TRUE,
        deleted_at = NOW(),
        deletion_reason = p_reason,
        deletion_requested_by = p_requested_by,
        -- Anonymiser les donnees personnelles
        email = 'deleted_' || p_customer_id || '@removed.local',
        nom = 'SUPPRIME',
        prenom = 'SUPPRIME',
        telephone = NULL,
        adresse = NULL,
        updated_at = NOW()
    WHERE id = p_customer_id;

    -- 2. Anonymiser les commandes (garder les montants pour la comptabilite)
    UPDATE orders SET
        shipping_name = 'ANONYMISE',
        shipping_address = 'ANONYMISE',
        shipping_phone = NULL,
        is_anonymized = TRUE,
        anonymized_at = NOW()
    WHERE customer_id = p_customer_id AND is_anonymized = FALSE;

    GET DIAGNOSTICS v_orders_count = ROW_COUNT;

    -- 3. Logger dans l'audit
    INSERT INTO deletion_audit_log (customer_id, action, details, performed_by)
    VALUES (
        p_customer_id,
        'SOFT_DELETE_CASCADE',
        jsonb_build_object(
            'reason', p_reason,
            'original_email_hash', md5(v_customer_email),
            'orders_anonymized', v_orders_count
        ),
        p_requested_by
    );

    RAISE NOTICE 'Client % supprime (soft). % commandes anonymisees.',
        p_customer_id, v_orders_count;
END;
$$;

-- Utilisation :
-- CALL soft_delete_customer(42, 'Demande utilisateur (DSAR)', 'support_agent_alice');

-- ============================================================
-- 4. PROCEDURE DE PURGE DEFINITIVE
-- ============================================================

CREATE OR REPLACE PROCEDURE hard_purge_deleted_customers(p_delay_days INTEGER DEFAULT 30)
LANGUAGE plpgsql
AS $$
DECLARE
    v_purged_count INTEGER;
BEGIN
    -- Supprimer definitivement les clients soft-deleted depuis plus de N jours
    WITH purged AS (
        DELETE FROM customers
        WHERE is_deleted = TRUE
        AND deleted_at < NOW() - (p_delay_days || ' days')::INTERVAL
        RETURNING id
    )
    SELECT COUNT(*) INTO v_purged_count FROM purged;

    -- Logger
    INSERT INTO deletion_audit_log (customer_id, action, details, performed_by)
    VALUES (
        NULL,
        'HARD_PURGE_BATCH',
        jsonb_build_object('purged_count', v_purged_count, 'delay_days', p_delay_days),
        'system_scheduled_job'
    );

    RAISE NOTICE '% clients definitivement purges', v_purged_count;
END;
$$;

-- ============================================================
-- 5. VUE ANONYMISEE POUR LES ANALYSTES
-- ============================================================

CREATE VIEW v_customers_anonymized AS
SELECT
    -- Pas d'identifiants directs
    md5(email::TEXT) AS pseudo_id,
    segment,
    EXTRACT(YEAR FROM AGE(date_naissance))::INTEGER / 10 * 10 AS tranche_age_dizaine,
    LEFT(code_postal, 2) AS departement,
    ville,
    created_at::DATE AS date_inscription,
    CASE WHEN is_deleted THEN 'supprime' ELSE 'actif' END AS statut
FROM customers
WHERE is_deleted = FALSE;

CREATE VIEW v_orders_stats AS
SELECT
    md5(c.email::TEXT) AS pseudo_customer_id,
    c.segment,
    COUNT(o.id) AS nb_commandes,
    ROUND(AVG(o.amount), 2) AS montant_moyen,
    ROUND(SUM(o.amount), 2) AS montant_total,
    MIN(o.order_date) AS premiere_commande,
    MAX(o.order_date) AS derniere_commande
FROM customers c
JOIN orders o ON c.id = o.customer_id
WHERE c.is_deleted = FALSE
GROUP BY c.email, c.segment;

-- ============================================================
-- 6. ROLES RBAC
-- ============================================================

-- Roles
CREATE ROLE customer_service NOLOGIN;
CREATE ROLE data_analyst_role NOLOGIN;
CREATE ROLE data_admin_role NOLOGIN;

-- Customer Service : lecture des clients actifs + execution du soft delete
GRANT SELECT ON customers TO customer_service;
GRANT SELECT ON orders TO customer_service;
GRANT UPDATE (is_deleted, deleted_at, deletion_reason, deletion_requested_by,
              email, nom, prenom, telephone, adresse, updated_at)
    ON customers TO customer_service;
GRANT UPDATE (shipping_name, shipping_address, shipping_phone,
              is_anonymized, anonymized_at)
    ON orders TO customer_service;
GRANT INSERT ON deletion_audit_log TO customer_service;
GRANT USAGE, SELECT ON SEQUENCE deletion_audit_log_id_seq TO customer_service;
-- Donner acces a la procedure
GRANT EXECUTE ON PROCEDURE soft_delete_customer TO customer_service;

-- Data Analyst : lecture des vues anonymisees UNIQUEMENT
GRANT SELECT ON v_customers_anonymized TO data_analyst_role;
GRANT SELECT ON v_orders_stats TO data_analyst_role;
-- PAS d'acces aux tables sous-jacentes !

-- Admin : tout
GRANT ALL ON ALL TABLES IN SCHEMA public TO data_admin_role;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO data_admin_role;
GRANT EXECUTE ON ALL PROCEDURES IN SCHEMA public TO data_admin_role;

-- Creation des utilisateurs
CREATE USER alice_support WITH PASSWORD 'strong_password_alice';
GRANT customer_service TO alice_support;

CREATE USER bob_analyst WITH PASSWORD 'strong_password_bob';
GRANT data_analyst_role TO bob_analyst;

CREATE USER charlie_admin WITH PASSWORD 'strong_password_charlie';
GRANT data_admin_role TO charlie_admin;

-- ============================================================
-- 7. TESTS
-- ============================================================

-- Inserer des donnees de test
INSERT INTO customers (email, nom, prenom, date_naissance, telephone, code_postal, ville, segment)
VALUES
    ('jean.dupont@test.fr', 'Dupont', 'Jean', '1985-03-15', '0601020304', '75008', 'Paris', 'premium'),
    ('sophie.martin@test.fr', 'Martin', 'Sophie', '1990-07-22', '0605060708', '69001', 'Lyon', 'standard');

INSERT INTO orders (customer_id, amount, status, shipping_name, shipping_address, shipping_phone)
VALUES
    (1, 150.00, 'delivered', 'Jean Dupont', '10 rue de la Paix, Paris', '0601020304'),
    (1, 89.90, 'delivered', 'Jean Dupont', '10 rue de la Paix, Paris', '0601020304'),
    (2, 210.50, 'pending', 'Sophie Martin', '5 place Bellecour, Lyon', '0605060708');

-- Test du soft delete
-- CALL soft_delete_customer(1, 'Test exercice', 'exercice_user');

-- Verifier que l'analyste ne voit que des donnees anonymisees
-- SET ROLE bob_analyst;
-- SELECT * FROM v_customers_anonymized;
-- SELECT * FROM v_orders_stats;
-- SELECT * FROM customers;  -- Erreur : permission denied
-- RESET ROLE;
```

</details>

---

### Exercice 3.3 : Concevoir une Politique de Retention des Donnees

**Enonce** : L'entreprise "DataCorp" dispose des types de donnees suivants. Pour chacun, definissez :
- La duree de conservation en base active
- La duree d'archivage
- Le mecanisme de purge (automatique/manuel)
- Le fondement juridique de la duree choisie

**Donnees a traiter :**
1. Donnees clients (profils, preferences)
2. Historique des commandes et factures
3. Logs de connexion a l'application
4. Cookies et donnees de navigation
5. CV de candidats non retenus
6. Donnees d'entrainement de modeles ML
7. Backups de base de donnees
8. Donnees de paie des employes

<details>
<summary>Cliquez pour afficher la correction</summary>

| Type de donnees | Conservation active | Archivage | Purge totale | Mecanisme | Fondement |
|----------------|-------------------|-----------|-------------|-----------|-----------|
| **1. Profils clients** | Duree de la relation commerciale | 3 ans apres fin de relation | 3 ans apres archivage | Automatique (Airflow DAG hebdomadaire) | Contrat (relation active) puis interet legitime (prospection = 3 ans, recommandation CNIL) |
| **2. Commandes/Factures** | 3 ans (base active) | 10 ans (obligation comptable) | Apres 10 ans | Automatique (job SQL annuel) | Obligation legale : Code de commerce Art. L123-22 (conservation 10 ans des pieces comptables) |
| **3. Logs de connexion** | 6 mois (base active) | 13 mois maximum | Apres 13 mois | Automatique (pg_cron quotidien) | Recommandation CNIL (13 mois max pour les logs contenant des donnees personnelles comme l'IP) |
| **4. Cookies/Navigation** | 13 mois maximum | Pas d'archivage | Apres 13 mois | Automatique (expiration cookie + purge serveur) | Directive ePrivacy + recommandation CNIL (13 mois max, consentement renouvele) |
| **5. CV non retenus** | 6 mois apres decision | 2 ans maximum | Apres 2 ans | Semi-automatique (alerte + validation RH) | Interet legitime (vivier) avec consentement du candidat pour > 6 mois. La CNIL recommande 2 ans max |
| **6. Donnees entrainement ML** | Duree de vie du modele | 6 mois apres deprecation du modele | Apres archivage | Manuel (revue trimestrielle) + automatique si donnees source purgees | Depend de la base legale du traitement source. Anonymiser si possible pour conservation longue |
| **7. Backups BDD** | 30 jours (rolling) | Pas d'archivage longue duree des backups contenant des PII | Rotation automatique | Automatique (politique de rotation des backups) | Les backups doivent respecter les memes regles de retention que les donnees source. Un backup contenant des donnees purgees doit lui-meme etre purge |
| **8. Donnees paie employes** | Duree du contrat | 5 ans apres depart (prescription civile) | Apres 5 ans (sauf contentieux) | Semi-automatique (alerte + validation RH/Juridique) | Obligation legale : Code du travail (conservation des bulletins de paie), delai de prescription de 5 ans (Art. 2224 Code civil) |

**Points importants de la correction :**

💡 Les **factures** ont une duree de conservation legale de **10 ans** (Code de commerce) : on ne peut PAS les supprimer avant, meme si le client exerce son droit a l'effacement. On anonymise les donnees personnelles mais on conserve le document comptable.

💡 Les **backups** sont souvent oublies dans les politiques de retention. Si un client est supprime de la base active, ses donnees persistent dans les backups. Solution : rotation courte (30 jours) OU chiffrement avec cle unique par client (suppression de la cle = suppression effective).

💡 Les **donnees d'entrainement ML** sont un cas complexe. La meilleure approche est de les anonymiser des le depart (Privacy by Design) pour pouvoir les conserver plus longtemps sans contrainte RGPD.

💡 Pour les **CV**, la CNIL recommande d'informer le candidat et d'obtenir son consentement si on souhaite conserver son CV au-dela de la duree du processus de recrutement.

</details>

---

## Reponses aux Exercices Rapides des Cours

### Reponses du Cours 1 (Introduction)

**Question : Le RGPD s'applique-t-il ?**

1. **Adresses IP dans les logs Apache** → ✅ OUI. L'adresse IP est une donnee personnelle (identification indirecte). RGPD s'applique.
2. **Donnees de vente agregees par region** → ❌ NON (si veritablement agregees et anonymes). Pas de donnee personnelle.
3. **Modele NLP sur des emails clients** → ✅ OUI. Les emails contiennent des donnees personnelles (contenu + metadata). RGPD s'applique pleinement.
4. **Donnees meteo publiques** → ❌ NON. Ce ne sont pas des donnees personnelles.
5. **Base de CV pour le recrutement** → ✅ OUI. Les CV contiennent de nombreuses donnees personnelles (identite, parcours, parfois photo). RGPD s'applique avec une attention particuliere aux donnees sensibles potentielles.

---

### Reponses du Cours 2 (Principes Fondamentaux)

**Pipeline ETL e-commerce :**

- **Base legale** : Contrat (execution de la commande) pour les donnees de commande. Interet legitime pour le calcul du panier moyen (statistique interne).
- **Donnees necessaires** : `order_id`, `customer_id` (pseudonymise), `date`, `montant`, `categorie_produit`. Pas besoin du nom, email, adresse pour le calcul du panier moyen.
- **Duree de conservation** : 3 ans pour les donnees de commande, 10 ans pour les factures (obligation legale comptable).
- **Mesures de securite** : Chiffrement en transit (TLS), RBAC (equipe data uniquement), pseudonymisation du customer_id dans le data warehouse, purge automatique a 3 ans.

---

### Reponses du Cours 3 (Droits des Personnes)

**L'email de l'utilisateur :**

1. **Droits exerces** : Droit d'acces (Art. 15) + Droit a la portabilite (Art. 20) + Droit a l'effacement (Art. 17)
2. **Delai** : 30 jours calendaires a compter de la reception de la demande
3. **Etapes techniques** :
   - Verifier l'identite du demandeur
   - Extraire toutes les donnees de toutes les sources (BDD, logs, CRM, backups...)
   - Compiler dans un format lisible (JSON/CSV pour la portabilite, PDF pour l'acces)
   - Executer le soft delete en cascade sur tous les systemes
   - Envoyer la reponse avec les donnees et la confirmation de suppression
4. **Donnees non supprimables** : Les factures (obligation legale 10 ans), les logs necessaires a la securite (si anonymises), les donnees necessaires a la defense en justice (si contentieux en cours)

---

### Reponses du Cours 5 (Anonymisation)

**Analyse du dataset medical :**

1. **Identifiants directs** : `nom`, `email`
2. **Quasi-identifiants** : `date_naissance`, `code_postal` (la combinaison peut identifier une personne)
3. **Donnee sensible** : `diagnostic_medical` (donnee de sante, Art. 9 RGPD)
4. **Strategie d'anonymisation** :
   - Supprimer `nom` et `email`
   - Generaliser `date_naissance` en tranche d'age (10 ans)
   - Generaliser `code_postal` en departement
   - Generaliser `salaire` en tranches
   - Verifier le k-anonymat (k >= 5) et la l-diversite (l >= 3 pour `diagnostic_medical`)
   - Si k-anonymat insuffisant : generaliser davantage ou supprimer les enregistrements uniques

---

### Reponses du Cours 6 (DPIA)

**Systeme de detection de fraude :**

1. **DPIA obligatoire** - Criteres remplis :
   - Evaluation/scoring (detection d'anomalies)
   - Decision automatisee avec effet significatif (blocage de transaction)
   - Donnees a grande echelle (2 millions de clients)
   - Usage innovant de technologies (deep learning)
   → 4 criteres = DPIA obligatoire

2. **3 risques majeurs** :
   - Faux positifs : blocage injustifie de transactions legitimes (gravite 3, probabilite 3 = 9)
   - Biais : certaines populations plus affectees par les faux positifs (gravite 4, probabilite 2 = 8)
   - Fuite : acces aux donnees de transactions de 2M de personnes (gravite 4, probabilite 2 = 8)

3. **Mesures d'attenuation** :
   - Faux positifs : seuil de blocage eleve + deblocage rapide + notification immediate + recours facile
   - Biais : audit de fairness par segment demographique + monitoring continu + equipe diversifiee
   - Fuite : chiffrement AES-256 + RBAC strict + MFA + logs d'acces + retention limitee

---

[← Precedent](07-securite-gouvernance.md) | [🏠 Accueil](README.md)

---

**Academy** - Formation Data Engineer
