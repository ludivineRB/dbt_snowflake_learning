[← Precedent](04-registre-des-traitements.md) | [🏠 Accueil](README.md) | [Suivant →](06-analyse-impact.md)

# 📖 Cours 5 - Anonymisation & Pseudonymisation

## Proteger les donnees personnelles dans vos pipelines de donnees

---

## 1. Distinction Fondamentale : Anonymisation vs Pseudonymisation

### 1.1 Definitions

```
┌──────────────────────────────────────────────────────────────────┐
│        Anonymisation vs Pseudonymisation                         │
│                                                                  │
│  PSEUDONYMISATION                ANONYMISATION                  │
│  (reversible)                    (irreversible)                 │
│                                                                  │
│  ┌──────────┐  cle  ┌──────┐    ┌──────────┐    ┌──────────┐  │
│  │ Donnees  │──────►│Pseudo│    │ Donnees  │───►│ Donnees  │  │
│  │ origin.  │◄──────│nyms. │    │ origin.  │    │ anonymes │  │
│  └──────────┘  cle  └──────┘    └──────────┘    └──────────┘  │
│                                       ╳                         │
│  La re-identification est         Impossible de revenir         │
│  possible avec la cle             aux donnees d'origine         │
│                                                                  │
│  → Toujours des donnees          → Plus des donnees             │
│    personnelles au sens            personnelles au sens          │
│    du RGPD                         du RGPD                      │
│                                                                  │
│  → Le RGPD s'applique            → Le RGPD ne s'applique       │
│                                     plus                        │
└──────────────────────────────────────────────────────────────────┘
```

### 1.2 Consequences juridiques

| Aspect | Pseudonymisation | Anonymisation |
|--------|-----------------|---------------|
| **Statut RGPD** | Donnees personnelles | Hors scope RGPD |
| **Droits des personnes** | S'appliquent | Ne s'appliquent plus |
| **Registre des traitements** | Necessaire | Non necessaire |
| **DPIA** | Peut etre necessaire | Non necessaire |
| **Base legale** | Requise | Non requise |
| **Duree de conservation** | Limitee | Illimitee |
| **Transfert hors UE** | Restrictions | Libre |
| **Notification de violation** | Obligatoire | Non applicable |

💡 **Attention** : L'anonymisation veritable est **extremement difficile** a atteindre. Le RGPD considere qu'une donnee est anonyme uniquement si la re-identification est **impossible** en utilisant **tous les moyens raisonnablement susceptibles** d'etre utilises (Considerant 26).

### 1.3 Arbre de decision : que choisir ?

```
┌──────────────────────────────────────────────────────────────────┐
│         Arbre de Decision : Anonymisation ou Pseudonymisation ?  │
│                                                                  │
│  Avez-vous besoin de pouvoir re-identifier les personnes ?      │
│                │                                                 │
│          ┌─────┴─────┐                                          │
│          │           │                                           │
│         OUI         NON                                          │
│          │           │                                           │
│          ▼           │                                           │
│  PSEUDONYMISATION    │                                           │
│  (ex: hachage avec   │  Les donnees doivent-elles etre          │
│   sel, chiffrement,  │  de haute precision ?                    │
│   tokenisation)      │         │                                 │
│                      │   ┌─────┴─────┐                          │
│                      │  OUI         NON                          │
│                      │   │           │                           │
│                      │   ▼           ▼                           │
│                      │  PSEUDONYM.  ANONYMISATION                │
│                      │  + acces     (generalisation,            │
│                      │  restreint   k-anonymat,                 │
│                      │  a la cle    differential privacy)       │
│                      │                                           │
│  Cas d'usage :       │  Cas d'usage :                           │
│  - DSAR responses    │  - Statistiques agregees                 │
│  - Recherche avec    │  - Donnees de test                       │
│    suivi longitudinal│  - Open data                             │
│  - Feature store ML  │  - Entrainement ML                      │
│    (avec re-jointure)│  - Partage avec tiers                   │
└──────────────────────────────────────────────────────────────────┘
```

---

## 2. Techniques d'Anonymisation

### 2.1 Suppression (Masquage)

La technique la plus simple : supprimer completement les champs identifiants.

```python
import pandas as pd

# Donnees originales
df = pd.DataFrame({
    'nom': ['Dupont', 'Martin', 'Durand'],
    'email': ['jean.dupont@email.fr', 'sophie.martin@email.fr', 'paul.durand@email.fr'],
    'age': [34, 28, 52],
    'ville': ['Paris', 'Lyon', 'Marseille'],
    'montant_achat': [150.0, 89.90, 210.50]
})

# Suppression des colonnes identifiantes
df_anonyme = df.drop(columns=['nom', 'email'])
print(df_anonyme)
#    age      ville  montant_achat
# 0   34      Paris         150.00
# 1   28       Lyon          89.90
# 2   52  Marseille         210.50
```

⚠️ **Attention** : La suppression seule ne garantit pas l'anonymisation ! La combinaison age + ville peut suffire a re-identifier une personne.

### 2.2 Generalisation

Reduire la precision des donnees pour empecher l'identification.

```python
import pandas as pd
import numpy as np

def generalize_data(df: pd.DataFrame) -> pd.DataFrame:
    """Generalise les donnees pour reduire le risque de re-identification."""
    df_gen = df.copy()

    # Generaliser l'age en tranches
    df_gen['tranche_age'] = pd.cut(
        df_gen['age'],
        bins=[0, 18, 25, 35, 50, 65, 100],
        labels=['<18', '18-24', '25-34', '35-49', '50-64', '65+']
    )
    df_gen = df_gen.drop(columns=['age'])

    # Generaliser le code postal (garder les 2 premiers chiffres = departement)
    df_gen['departement'] = df_gen['code_postal'].str[:2]
    df_gen = df_gen.drop(columns=['code_postal'])

    # Generaliser la ville en region
    ville_to_region = {
        'Paris': 'Ile-de-France',
        'Lyon': 'Auvergne-Rhone-Alpes',
        'Marseille': 'Provence-Alpes-Cote-d-Azur',
        'Toulouse': 'Occitanie',
        'Bordeaux': 'Nouvelle-Aquitaine'
    }
    df_gen['region'] = df_gen['ville'].map(ville_to_region)
    df_gen = df_gen.drop(columns=['ville'])

    # Generaliser les montants en tranches
    df_gen['tranche_montant'] = pd.cut(
        df_gen['montant_achat'],
        bins=[0, 50, 100, 200, 500, float('inf')],
        labels=['0-50', '50-100', '100-200', '200-500', '500+']
    )
    df_gen = df_gen.drop(columns=['montant_achat'])

    # Generaliser les dates en mois
    if 'date_achat' in df_gen.columns:
        df_gen['mois_achat'] = pd.to_datetime(df_gen['date_achat']).dt.to_period('M')
        df_gen = df_gen.drop(columns=['date_achat'])

    return df_gen

# Utilisation
df_generalise = generalize_data(df)
```

### 2.3 K-anonymat

Le **k-anonymat** garantit que chaque combinaison de quasi-identifiants apparait au moins **k fois** dans le jeu de donnees. Autrement dit, chaque individu est "cache" parmi au moins k-1 autres.

```python
def check_k_anonymity(df: pd.DataFrame, quasi_identifiers: list, k: int) -> dict:
    """
    Verifie si un DataFrame respecte le k-anonymat
    pour un ensemble de quasi-identifiants.
    """
    # Grouper par combinaisons de quasi-identifiants
    groups = df.groupby(quasi_identifiers).size().reset_index(name='count')

    # Verifier le k-anonymat
    min_group_size = groups['count'].min()
    violating_groups = groups[groups['count'] < k]

    result = {
        'k_target': k,
        'k_achieved': min_group_size,
        'is_k_anonymous': min_group_size >= k,
        'total_groups': len(groups),
        'violating_groups': len(violating_groups),
        'records_at_risk': violating_groups['count'].sum() if len(violating_groups) > 0 else 0
    }

    if not result['is_k_anonymous']:
        print(f"⚠️ K-anonymat non atteint ! k cible = {k}, k reel = {min_group_size}")
        print(f"   {result['violating_groups']} groupes en violation ({result['records_at_risk']} enregistrements)")
        print(f"   Solution : generaliser davantage les quasi-identifiants")
    else:
        print(f"✅ K-anonymat respecte (k = {min_group_size})")

    return result

# Exemple d'utilisation
quasi_ids = ['tranche_age', 'departement', 'profession']
result = check_k_anonymity(df_generalise, quasi_ids, k=5)
```

### 2.4 L-diversite

Le **l-diversite** etend le k-anonymat en exigeant que chaque groupe k-anonyme contienne au moins **l valeurs distinctes** pour les attributs sensibles.

```python
def check_l_diversity(df: pd.DataFrame, quasi_identifiers: list,
                      sensitive_attr: str, l: int) -> dict:
    """
    Verifie si un DataFrame respecte la l-diversite.
    Chaque groupe de quasi-identifiants doit avoir au moins l valeurs
    distinctes pour l'attribut sensible.
    """
    groups = df.groupby(quasi_identifiers)

    violations = []
    for name, group in groups:
        n_distinct = group[sensitive_attr].nunique()
        if n_distinct < l:
            violations.append({
                'group': name,
                'distinct_values': n_distinct,
                'group_size': len(group)
            })

    result = {
        'l_target': l,
        'is_l_diverse': len(violations) == 0,
        'violating_groups': len(violations),
        'violations': violations[:5]  # Afficher les 5 premieres violations
    }

    if violations:
        print(f"⚠️ L-diversite non atteinte pour '{sensitive_attr}'")
        for v in violations[:3]:
            print(f"   Groupe {v['group']}: seulement {v['distinct_values']} valeurs distinctes")
    else:
        print(f"✅ L-diversite respectee (l = {l}) pour '{sensitive_attr}'")

    return result

# Verifier que chaque groupe a au moins 3 diagnostics differents
result = check_l_diversity(df, ['tranche_age', 'region'], 'diagnostic', l=3)
```

### 2.5 Differential Privacy (Confidentialite Differentielle)

La **differential privacy** est la technique la plus avancee. Elle ajoute du bruit statistique aux donnees de sorte qu'il est **mathematiquement impossible** de determiner si un individu particulier est present dans le jeu de donnees.

```python
import numpy as np

def add_laplace_noise(value: float, sensitivity: float, epsilon: float) -> float:
    """
    Ajoute du bruit de Laplace pour garantir l'epsilon-differential privacy.

    Parametres :
    - value : la vraie valeur
    - sensitivity : la sensibilite de la requete (impact max d'un individu)
    - epsilon : parametre de confidentialite (plus petit = plus de confidentialite)
    """
    scale = sensitivity / epsilon
    noise = np.random.laplace(0, scale)
    return value + noise

def private_count(df: pd.DataFrame, column: str, value: str,
                  epsilon: float = 1.0) -> float:
    """Comptage avec differential privacy."""
    true_count = len(df[df[column] == value])
    # Sensibilite d'un comptage = 1 (ajouter/retirer une personne change le compte de 1)
    noisy_count = add_laplace_noise(true_count, sensitivity=1, epsilon=epsilon)
    return max(0, round(noisy_count))  # Pas de comptage negatif

def private_mean(df: pd.DataFrame, column: str,
                 value_range: tuple, epsilon: float = 1.0) -> float:
    """Moyenne avec differential privacy."""
    true_mean = df[column].mean()
    n = len(df)
    # Sensibilite de la moyenne = (max - min) / n
    sensitivity = (value_range[1] - value_range[0]) / n
    noisy_mean = add_laplace_noise(true_mean, sensitivity=sensitivity, epsilon=epsilon)
    return round(noisy_mean, 2)

# Exemple d'utilisation
print(f"Nombre de clients a Paris (epsilon=1.0) : {private_count(df, 'ville', 'Paris', epsilon=1.0)}")
print(f"Montant moyen d'achat (epsilon=0.5) : {private_mean(df, 'montant_achat', (0, 1000), epsilon=0.5)}")

# Plus epsilon est petit, plus la confidentialite est forte (mais le resultat est plus bruite)
# epsilon = 0.1 → forte confidentialite, resultat bruite
# epsilon = 1.0 → bonne confidentialite, resultat raisonnablement precis
# epsilon = 10.0 → faible confidentialite, resultat tres precis
```

---

## 3. Techniques de Pseudonymisation

### 3.1 Hachage (SHA-256)

```python
import hashlib

def hash_identifier(value: str, salt: str = "") -> str:
    """
    Pseudonymise un identifiant par hachage SHA-256 avec sel.
    Le sel rend le hachage unique a votre organisation.
    """
    salted_value = f"{salt}:{value}"
    return hashlib.sha256(salted_value.encode()).hexdigest()

# Utilisation
email = "jean.dupont@email.fr"
salt = "xyz_company_secret_2024"  # A stocker de maniere securisee !

pseudo_id = hash_identifier(email, salt)
print(f"Email: {email}")
print(f"Pseudo: {pseudo_id}")
# Pseudo: a3f2b8c9d1e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0

# ⚠️ ATTENTION : un hash sans sel peut etre reverse par dictionnaire !
# ❌ hashlib.sha256("jean.dupont@email.fr".encode()).hexdigest()
# ✅ hashlib.sha256(f"{salt}:jean.dupont@email.fr".encode()).hexdigest()
```

### 3.2 Chiffrement (AES-256)

```python
from cryptography.fernet import Fernet
import base64
import os

class DataEncryptor:
    """Chiffrement reversible pour pseudonymisation."""

    def __init__(self, key: bytes = None):
        """
        Initialise avec une cle de chiffrement.
        La cle doit etre stockee de maniere securisee
        (vault, KMS, HSM), jamais dans le code !
        """
        if key is None:
            key = Fernet.generate_key()
        self.cipher = Fernet(key)
        self.key = key

    def encrypt(self, data: str) -> str:
        """Chiffre une donnee personnelle."""
        return self.cipher.encrypt(data.encode()).decode()

    def decrypt(self, encrypted_data: str) -> str:
        """Dechiffre une donnee (necessaire pour les DSAR)."""
        return self.cipher.decrypt(encrypted_data.encode()).decode()

# Utilisation
encryptor = DataEncryptor()

# Pseudonymisation par chiffrement
nom_chiffre = encryptor.encrypt("Jean Dupont")
email_chiffre = encryptor.encrypt("jean.dupont@email.fr")

print(f"Nom chiffre : {nom_chiffre}")
print(f"Email chiffre : {email_chiffre}")

# Re-identification (pour repondre a une DSAR)
print(f"Nom dechiffre : {encryptor.decrypt(nom_chiffre)}")
```

### 3.3 Tokenisation

```python
import uuid
import json

class Tokenizer:
    """
    Remplace les valeurs sensibles par des tokens aleatoires.
    La table de correspondance doit etre stockee de maniere securisee.
    """

    def __init__(self):
        self.token_vault = {}  # En production : utiliser un vault securise
        self.reverse_vault = {}

    def tokenize(self, value: str) -> str:
        """Remplace une valeur par un token unique."""
        if value in self.token_vault:
            return self.token_vault[value]

        token = f"TOK-{uuid.uuid4().hex[:12]}"
        self.token_vault[value] = token
        self.reverse_vault[token] = value
        return token

    def detokenize(self, token: str) -> str:
        """Retrouve la valeur originale a partir du token."""
        if token not in self.reverse_vault:
            raise ValueError(f"Token inconnu : {token}")
        return self.reverse_vault[token]

    def delete_token(self, token: str):
        """Supprime un token (droit a l'effacement)."""
        if token in self.reverse_vault:
            original = self.reverse_vault.pop(token)
            self.token_vault.pop(original, None)

# Utilisation
tokenizer = Tokenizer()

email_token = tokenizer.tokenize("jean.dupont@email.fr")
print(f"Token : {email_token}")  # TOK-a1b2c3d4e5f6
print(f"Original : {tokenizer.detokenize(email_token)}")

# Effacement : supprimer le token rend la re-identification impossible
tokenizer.delete_token(email_token)
```

---

## 4. Exemple Complet : Anonymiser un Dataset Client avec Pandas

### 4.1 Dataset original

```python
import pandas as pd
import hashlib
import numpy as np
from datetime import datetime

# Dataset client original (donnees personnelles)
df_original = pd.DataFrame({
    'client_id': [1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008],
    'nom': ['Dupont', 'Martin', 'Durand', 'Leroy', 'Moreau', 'Simon', 'Laurent', 'Michel'],
    'prenom': ['Jean', 'Sophie', 'Paul', 'Marie', 'Pierre', 'Isabelle', 'Thomas', 'Claire'],
    'email': [
        'jean.dupont@email.fr', 'sophie.martin@gmail.com',
        'paul.durand@outlook.fr', 'marie.leroy@email.fr',
        'pierre.moreau@gmail.com', 'isabelle.simon@email.fr',
        'thomas.laurent@outlook.fr', 'claire.michel@email.fr'
    ],
    'date_naissance': [
        '1987-03-15', '1992-07-22', '1975-11-08', '1988-01-30',
        '1995-06-14', '1982-09-03', '1990-12-25', '1978-04-17'
    ],
    'telephone': [
        '0612345678', '0623456789', '0634567890', '0645678901',
        '0656789012', '0667890123', '0678901234', '0689012345'
    ],
    'code_postal': ['75008', '69001', '13001', '31000', '75015', '69003', '75011', '13008'],
    'montant_total_achats': [1250.50, 89.90, 3420.00, 567.80, 2100.00, 45.50, 890.30, 1567.00],
    'nb_commandes': [15, 2, 42, 8, 25, 1, 12, 18],
    'derniere_commande': [
        '2024-01-15', '2024-02-20', '2023-11-30', '2024-03-01',
        '2024-01-28', '2023-08-15', '2024-02-14', '2024-03-10'
    ]
})

print("=== Dataset Original ===")
print(df_original.to_string())
```

### 4.2 Pipeline d'anonymisation complet

```python
class DataAnonymizer:
    """
    Pipeline d'anonymisation complet pour datasets clients.
    Applique differentes techniques selon le type de donnee.
    """

    def __init__(self, salt: str, anonymization_level: str = "standard"):
        """
        Parametres :
        - salt : sel pour le hachage (secret)
        - anonymization_level : 'light', 'standard', 'strict'
        """
        self.salt = salt
        self.level = anonymization_level

    def anonymize(self, df: pd.DataFrame) -> pd.DataFrame:
        """Pipeline d'anonymisation principal."""
        df_anon = df.copy()

        # 1. Supprimer les identifiants directs
        df_anon = self._remove_direct_identifiers(df_anon)

        # 2. Pseudonymiser l'ID client (garder un identifiant non-nominatif)
        df_anon = self._pseudonymize_id(df_anon)

        # 3. Generaliser les donnees
        df_anon = self._generalize(df_anon)

        # 4. Masquer les donnees sensibles restantes
        df_anon = self._mask_remaining(df_anon)

        # 5. Verifier le k-anonymat
        self._check_quality(df_anon)

        return df_anon

    def _remove_direct_identifiers(self, df: pd.DataFrame) -> pd.DataFrame:
        """Supprime les identifiants directs."""
        columns_to_remove = ['nom', 'prenom', 'email', 'telephone']
        existing = [c for c in columns_to_remove if c in df.columns]
        return df.drop(columns=existing)

    def _pseudonymize_id(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remplace le client_id par un hash."""
        if 'client_id' in df.columns:
            df['pseudo_id'] = df['client_id'].apply(
                lambda x: hashlib.sha256(f"{self.salt}:{x}".encode()).hexdigest()[:16]
            )
            df = df.drop(columns=['client_id'])
        return df

    def _generalize(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generalise les quasi-identifiants."""

        # Generaliser la date de naissance en tranche d'age
        if 'date_naissance' in df.columns:
            today = datetime.now()
            df['date_naissance'] = pd.to_datetime(df['date_naissance'])
            ages = ((today - df['date_naissance']).dt.days / 365.25).astype(int)
            df['tranche_age'] = pd.cut(
                ages,
                bins=[0, 25, 35, 45, 55, 65, 100],
                labels=['18-24', '25-34', '35-44', '45-54', '55-64', '65+']
            )
            df = df.drop(columns=['date_naissance'])

        # Generaliser le code postal en departement
        if 'code_postal' in df.columns:
            df['departement'] = df['code_postal'].str[:2]
            df = df.drop(columns=['code_postal'])

        # Generaliser les montants en tranches
        if 'montant_total_achats' in df.columns and self.level == 'strict':
            df['tranche_montant'] = pd.cut(
                df['montant_total_achats'],
                bins=[0, 100, 500, 1000, 2000, 5000, float('inf')],
                labels=['0-100', '100-500', '500-1000', '1000-2000', '2000-5000', '5000+']
            )
            df = df.drop(columns=['montant_total_achats'])

        # Generaliser les dates en mois
        if 'derniere_commande' in df.columns:
            df['derniere_commande'] = pd.to_datetime(df['derniere_commande']).dt.to_period('M').astype(str)

        return df

    def _mask_remaining(self, df: pd.DataFrame) -> pd.DataFrame:
        """Masque les donnees restantes si niveau strict."""
        if self.level == 'strict':
            if 'nb_commandes' in df.columns:
                df['nb_commandes'] = pd.cut(
                    df['nb_commandes'],
                    bins=[0, 5, 10, 20, 50, float('inf')],
                    labels=['1-5', '6-10', '11-20', '21-50', '50+']
                )
        return df

    def _check_quality(self, df: pd.DataFrame):
        """Verifie la qualite de l'anonymisation."""
        quasi_ids = [c for c in ['tranche_age', 'departement'] if c in df.columns]
        if quasi_ids:
            groups = df.groupby(quasi_ids).size()
            min_k = groups.min()
            print(f"\n📊 Verification qualite anonymisation :")
            print(f"   Quasi-identifiants : {quasi_ids}")
            print(f"   K-anonymat atteint : k = {min_k}")
            if min_k < 3:
                print(f"   ⚠️ k < 3 : generaliser davantage pour reduire le risque")
            else:
                print(f"   ✅ Niveau de protection acceptable")


# Utilisation du pipeline d'anonymisation
anonymizer = DataAnonymizer(
    salt="xyz_company_secret_2024",
    anonymization_level="standard"
)

df_anonymise = anonymizer.anonymize(df_original)
print("\n=== Dataset Anonymise ===")
print(df_anonymise.to_string())
```

### 4.3 Resultat attendu

```
=== Dataset Anonymise ===
   montant_total_achats  nb_commandes derniere_commande       pseudo_id tranche_age departement
0               1250.50            15           2024-01  a3f2b8c9d1e4f5a6       35-44          75
1                 89.90             2           2024-02  b7c8d9e0f1a2b3c4       25-34          69
2               3420.00            42           2023-11  c4d5e6f7a8b9c0d1       45-54          13
3                567.80             8           2024-03  d1e2f3a4b5c6d7e8       35-44          31
4               2100.00            25           2024-01  e8f9a0b1c2d3e4f5       25-34          75
5                 45.50             1           2023-08  f5a6b7c8d9e0f1a2       35-44          69
6                890.30            12           2024-02  a2b3c4d5e6f7a8b9       25-34          75
7               1567.00            18           2024-03  b9c0d1e2f3a4b5c6       45-54          13
```

---

## 5. Quand Utiliser Quelle Technique : Resume

### 5.1 Tableau de decision

| Cas d'usage | Technique recommandee | Justification |
|-------------|----------------------|---------------|
| Environnement de test / dev | Donnees synthetiques (Faker) + generalisation | Pas besoin de donnees reelles |
| Analytics / reporting | Generalisation + agregation | Tendances sans details individuels |
| Entrainement ML | Pseudonymisation (hash) + minimisation | Besoin de patterns, pas d'identites |
| Partage avec tiers | Anonymisation complete (k-anonymat + l-diversite) | Pas de controle sur le destinataire |
| Open data | Anonymisation stricte (differential privacy) | Donnees accessibles a tous |
| Feature store ML | Pseudonymisation (token) | Besoin de jointures reversibles |
| Sauvegarde / archivage | Chiffrement (AES-256) | Reversible si besoin legal |
| Logs applicatifs | Hachage (SHA-256 + sel) + troncation IP | Securite sans identification |

### 5.2 Tableau comparatif des techniques

| Technique | Reversible | Protection | Impact qualite | Complexite | Performance |
|-----------|-----------|-----------|----------------|------------|-------------|
| Suppression | Non | Maximale | Elevee (perte de colonnes) | Faible | Excellente |
| Generalisation | Non | Bonne | Moderee | Faible | Excellente |
| K-anonymat | Non | Bonne | Moderee | Moyenne | Bonne |
| L-diversite | Non | Tres bonne | Moderee a elevee | Moyenne | Bonne |
| Differential Privacy | Non | Maximale | Variable (selon epsilon) | Elevee | Variable |
| Hachage (SHA-256) | Non* | Moyenne | Faible | Faible | Excellente |
| Chiffrement (AES) | Oui | Elevee (si cle protegee) | Nulle | Moyenne | Bonne |
| Tokenisation | Oui | Elevee (si vault protege) | Nulle | Moyenne | Bonne |

*Le hachage sans sel peut etre reverse par attaque par dictionnaire

---

## 6. Risques de Re-identification

### 6.1 Exemples celebres

| Cas | Annee | Description | Lecon |
|-----|-------|-------------|-------|
| Netflix Prize | 2006 | Dataset de notations "anonyme" de-anonymise en croisant avec IMDb | Le croisement de sources permet la re-identification |
| AOL Search Data | 2006 | Requetes de recherche "anonymes" permettent d'identifier des utilisateurs | Les patterns comportementaux sont identifiants |
| NYC Taxi Data | 2014 | Courses de taxi "anonymes" revelent les habitudes de celebrites | Le hachage MD5 sans sel est facilement reversible |
| Strava Heatmap | 2018 | Donnees de sport "agregees" revelent des bases militaires secretes | L'agregation geographique peut etre insuffisante |

### 6.2 Facteurs augmentant le risque de re-identification

```
┌──────────────────────────────────────────────────────────────────┐
│          Facteurs de risque de re-identification                 │
│                                                                  │
│  RISQUE ELEVE                                                   │
│  ┌─────────────────────────────────────────────────┐            │
│  │ - Donnees geographiques precises (GPS, adresse) │            │
│  │ - Donnees temporelles precises (horodatage)     │            │
│  │ - Combinaison de quasi-identifiants             │            │
│  │ - Petits jeux de donnees (< 1000 enregistr.)   │            │
│  │ - Valeurs extremes (age > 95, salaire > 500k)  │            │
│  │ - Professions rares (chirurgien, depute...)     │            │
│  └─────────────────────────────────────────────────┘            │
│                                                                  │
│  RISQUE MODERE                                                  │
│  ┌─────────────────────────────────────────────────┐            │
│  │ - Donnees de navigation (user agent, patterns)  │            │
│  │ - Donnees d'achat (combinaisons de produits)    │            │
│  │ - Donnees de mobilite (trajets reguliers)       │            │
│  └─────────────────────────────────────────────────┘            │
│                                                                  │
│  RISQUE FAIBLE                                                  │
│  ┌─────────────────────────────────────────────────┐            │
│  │ - Donnees fortement agregees (par region, mois) │            │
│  │ - Grands jeux de donnees (> 100k enregistr.)    │            │
│  │ - Ajout de bruit (differential privacy)         │            │
│  └─────────────────────────────────────────────────┘            │
└──────────────────────────────────────────────────────────────────┘
```

---

## 7. Impact sur la Qualite des Donnees et l'Analytics

### 7.1 Le compromis confidentialite / utilite

```
     Utilite des donnees
     ▲
     │  ★ Donnees brutes (aucune protection)
     │
     │     ★ Pseudonymisation
     │
     │        ★ Generalisation legere
     │
     │           ★ K-anonymat (k=3)
     │
     │              ★ K-anonymat (k=10)
     │
     │                 ★ Differential Privacy (epsilon=1)
     │
     │                    ★ Differential Privacy (epsilon=0.1)
     │
     │                        ★ Donnees completement anonymes
     │
     └──────────────────────────────────────────────────────►
                                              Confidentialite
```

### 7.2 Recommandations par type d'analyse

| Type d'analyse | Niveau d'anonymisation recommande | Impact sur la qualite |
|---------------|----------------------------------|----------------------|
| Comptages / volumes | Generalisation + aggregation | Faible |
| Tendances temporelles | Generalisation des dates (mois) | Faible |
| Segmentation client | K-anonymat (k >= 5) | Modere |
| Prediction ML | Pseudonymisation + minimisation | Faible a modere |
| Analyse geographique | Generalisation au departement/region | Modere |
| Analyse de survie / cohortes | Generalisation temporelle | Modere |
| Analyse individuelle precis | Impossible apres anonymisation | Maximal |

---

## 📝 Exercice Rapide

**Mission** : Vous avez un fichier CSV contenant les donnees suivantes :
```
nom, email, date_naissance, code_postal, salaire, diagnostic_medical
```

1. Quelles donnees sont directement identifiantes ?
2. Quelles donnees sont des quasi-identifiants ?
3. Quelle donnee est sensible ?
4. Proposez une strategie d'anonymisation pour un partage avec une equipe de recherche externe

> **Reponses** : voir [08-exercices.md](08-exercices.md)

---

[← Precedent](04-registre-des-traitements.md) | [🏠 Accueil](README.md) | [Suivant →](06-analyse-impact.md)

---

**Academy** - Formation Data Engineer
