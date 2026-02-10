# Exercice 3 : Preprocessing et Pipeline — Préparer les Données Proprement

**Phase 2 — Chapitres 6, 7 & 8** | Durée estimée : 3h | Niveau : Intermédiaire

---

## 🎯 Objectifs

- Nettoyer un dataset réel (valeurs manquantes, outliers)
- Appliquer les bons encodages selon le type de variable
- Construire un Pipeline scikit-learn robuste
- Détecter et corriger un data leakage

---

## 📋 Contexte

Votre pipeline de données doit être **reproductible** et **sans fuite d'information**. Un collègue vous a laissé un notebook avec un pipeline "qui marche"... mais qui contient 3 erreurs critiques de data leakage. À vous de les trouver et de tout refaire proprement.

---

## 📝 Instructions

### Partie 1 : Nettoyage du dataset churn (45 min)

Chargez `data/clients_churn.csv` et effectuez :

1. **Valeurs manquantes** :
   - Identifiez les colonnes avec des valeurs manquantes
   - Pour les numériques : testez imputation par médiane et par moyenne — quel impact ?
   - Pour les catégorielles : imputez par le mode (valeur la plus fréquente)

2. **Valeurs aberrantes** :
   - Utilisez la méthode IQR sur les variables numériques
   - Visualisez avec des boxplots
   - Décidez : supprimer, capper (winsorize), ou garder ?

3. **Doublons** :
   - Y en a-t-il ? Si oui, supprimez-les

### Partie 2 : Feature Engineering (45 min)

4. **Variables catégorielles** :
   - Identifiez toutes les variables catégorielles
   - Pour chaque variable, choisissez le bon encodage :
     - One-Hot si < 5 catégories ET modèle linéaire
     - Ordinal si ordre naturel (ex: Low < Medium < High)
   - Justifiez chaque choix

5. **Variables numériques** :
   - Appliquez StandardScaler — pourquoi StandardScaler et pas MinMaxScaler ici ?

6. **Créez au moins 2 nouvelles features** à partir des données existantes (combinaisons, ratios, bins...)

### Partie 3 : Pipeline scikit-learn (45 min)

7. Construisez un `ColumnTransformer` qui applique :
   - Imputation + Scaling sur les numériques
   - Imputation + OneHotEncoding sur les catégorielles

8. Encapsulez dans un `Pipeline` avec un modèle de votre choix (LogisticRegression pour commencer)

9. Vérifiez que le pipeline fait `fit` uniquement sur le train set

### Partie 4 : Chasse au leakage (45 min)

10. Voici un code piégé. Trouvez les **3 erreurs de data leakage** :

```python
# CODE PIÉGÉ — Trouvez les 3 erreurs !
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

df = pd.read_csv("../data/clients_churn.csv")
X = df.drop("churn", axis=1)
y = df["churn"]

# Erreur 1 quelque part ici...
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Erreur 2 quelque part ici...
X_scaled = pd.DataFrame(X_scaled)
X_scaled['mean_encoded_contract'] = df.groupby('contract')['churn'].transform('mean')

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

# Erreur 3 : pensez au random_state et stratify
model = LogisticRegression()
model.fit(X_train, y_train)
print(f"Accuracy: {model.score(X_test, y_test):.4f}")
```

11. Réécrivez le code **sans leakage** en utilisant un Pipeline

---

## 💡 Indices

```python
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

# Erreurs typiques de leakage :
# 1. fit_transform sur TOUT le dataset avant le split
# 2. Target encoding calculé sur tout le dataset
# 3. Pas de stratify dans le train_test_split
```

---

## ✅ Critères de réussite

- [ ] Les valeurs manquantes sont traitées avec la bonne stratégie
- [ ] Les outliers sont identifiés et traités (avec justification)
- [ ] Le ColumnTransformer sépare correctement numériques et catégorielles
- [ ] Le Pipeline fait fit uniquement sur le train set
- [ ] Les 3 erreurs de leakage sont trouvées et expliquées
- [ ] Le code final est sans leakage et reproductible
