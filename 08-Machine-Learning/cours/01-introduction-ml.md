# Chapitre 1 : Introduction au Machine Learning

## 🎯 Objectifs

- Comprendre ce qu'est le Machine Learning et pourquoi il existe
- Distinguer les types d'apprentissage (supervisé, non-supervisé, par renforcement)
- Connaître le workflow ML complet de bout en bout
- Savoir quand utiliser (et ne **PAS** utiliser) le ML
- Maîtriser le vocabulaire essentiel du domaine
- Découvrir l'écosystème Python pour le Machine Learning

---

## 1. 🧠 Qu'est-ce que le Machine Learning ?

### 1.1 Définition

Le **Machine Learning** (apprentissage automatique) est une branche de l'intelligence artificielle qui permet aux machines d'**apprendre à partir de données** sans être explicitement programmées pour chaque cas.

> 💡 **Conseil** : Retenez cette définition simple — le ML, c'est **donner des exemples** à un programme pour qu'il **apprenne les règles tout seul**, plutôt que de coder les règles à la main.

### 1.2 ML vs Programmation traditionnelle

La différence fondamentale réside dans l'approche :

| Aspect | Programmation traditionnelle | Machine Learning |
|--------|------------------------------|------------------|
| **Entrée** | Données + Règles | Données + Résultats attendus |
| **Sortie** | Résultats | Règles (modèle) |
| **Approche** | Déductive (règles → résultats) | Inductive (exemples → règles) |
| **Maintenance** | Modifier les règles manuellement | Réentraîner avec de nouvelles données |
| **Complexité** | Difficile si beaucoup de cas | Gère bien la complexité |

**Programmation traditionnelle :**

```
Données + Règles → Programme → Résultats
```

**Machine Learning :**

```
Données + Résultats → Algorithme ML → Modèle (les règles)
```

### 1.3 Analogie : reconnaître un chat

**Approche traditionnelle** : écrire des règles comme "si l'image contient deux triangles (oreilles) + deux cercles (yeux) + des moustaches → chat". C'est extrêmement difficile et fragile.

**Approche ML** : montrer 10 000 photos de chats et 10 000 photos de non-chats à un algorithme. Il apprend **tout seul** les caractéristiques qui distinguent un chat.

> 🧠 **Pour aller plus loin** : Cette analogie illustre pourquoi le ML excelle dans les tâches où les règles sont trop complexes ou trop nombreuses pour être codées manuellement — reconnaissance d'images, traduction automatique, recommandation de contenu, etc.

### 1.4 Bref historique

| Année | Événement | Impact |
|-------|-----------|--------|
| 1950 | Alan Turing propose le "Test de Turing" | Fondation conceptuelle de l'IA |
| 1957 | Perceptron (Frank Rosenblatt) | Premier réseau de neurones |
| 1997 | Deep Blue bat Kasparov aux échecs | Règles + force brute, pas du ML |
| 2012 | AlexNet gagne ImageNet | Explosion du Deep Learning |
| 2016 | AlphaGo bat Lee Sedol au Go | Apprentissage par renforcement |
| 2022+ | ChatGPT, LLMs | Modèles de langage à grande échelle |

---

## 2. 📊 Les types d'apprentissage

### 2.1 Apprentissage supervisé

**Principe** : on fournit au modèle des données **étiquetées** (avec la réponse attendue). Le modèle apprend la relation entre les entrées (features) et la sortie (target/label).

```
Données d'entraînement = Features (X) + Labels (y)
         ↓
    Algorithme ML
         ↓
    Modèle entraîné
         ↓
Nouvelles données (X) → Modèle → Prédictions (ŷ)
```

L'apprentissage supervisé se divise en deux grandes catégories :

#### Régression vs Classification

| Aspect | Régression | Classification |
|--------|-----------|----------------|
| **Type de sortie** | Valeur continue (nombre) | Catégorie (classe) |
| **Exemple** | Prédire un prix (€) | Prédire spam / non-spam |
| **Métriques** | MSE, RMSE, MAE, R² | Accuracy, Precision, Recall, F1, AUC |
| **Algorithmes** | Régression linéaire, Ridge, Lasso | Logistique, SVM, KNN, Arbres |

#### Exemples concrets

| Problème | Type | Entrée (Features) | Sortie (Target) |
|----------|------|-------------------|-----------------|
| Prédire le prix d'un appartement | Régression | Surface, quartier, étage | Prix (€) |
| Diagnostiquer une maladie | Classification binaire | Symptômes, analyses | Malade / Sain |
| Estimer le temps de livraison | Régression | Distance, trafic, météo | Durée (min) |
| Reconnaître un chiffre manuscrit | Classification multi-classes | Pixels de l'image | Chiffre (0-9) |
| Prédire le taux de désabonnement | Classification binaire | Historique client | Churn / No churn |
| Estimer la consommation électrique | Régression | Température, heure, jour | kWh |

> 💡 **Conseil de pro** : Pour savoir si c'est de la régression ou de la classification, posez-vous la question : "Est-ce que la sortie est un **nombre** ou une **catégorie** ?" Si c'est un nombre → régression. Si c'est une catégorie → classification.

### 2.2 Apprentissage non-supervisé

**Principe** : on fournit au modèle des données **sans étiquettes**. Le modèle doit trouver des **structures cachées** dans les données.

```
Données (X uniquement, pas de y)
         ↓
    Algorithme ML
         ↓
    Structures / Groupes / Patterns
```

#### Principales techniques

| Technique | Objectif | Algorithmes | Exemple |
|-----------|----------|------------|---------|
| **Clustering** | Regrouper des données similaires | K-Means, DBSCAN, Hierarchique | Segmentation clients |
| **Réduction de dimension** | Simplifier les données | PCA, t-SNE, UMAP | Visualisation de données complexes |
| **Détection d'anomalies** | Trouver les points inhabituels | Isolation Forest, LOF | Détection de fraude |
| **Règles d'association** | Trouver des relations | Apriori, FP-Growth | Panier d'achat (qui achète X achète aussi Y) |

> 💡 **Conseil** : Le non-supervisé est souvent utilisé en **exploration** — pour comprendre ses données avant de construire un modèle supervisé.

#### Exemples concrets

- **Segmentation clients** : regrouper les clients par comportement d'achat (sans savoir a priori combien de segments il y a)
- **Détection d'anomalies** : identifier des transactions bancaires frauduleuses (les fraudes sont rares et différentes de la norme)
- **Compression d'images** : réduire la dimensionalité tout en gardant l'essentiel de l'information

### 2.3 Apprentissage par renforcement

**Principe** : un **agent** interagit avec un **environnement**, prend des **actions**, reçoit des **récompenses** (ou pénalités) et apprend à maximiser la récompense totale.

```
Agent → Action → Environnement
                      ↓
              État + Récompense
                      ↓
                    Agent (apprend et s'améliore)
```

| Composant | Rôle | Exemple (jeu vidéo) |
|-----------|------|---------------------|
| **Agent** | Celui qui prend les décisions | Le joueur IA |
| **Environnement** | Le monde dans lequel l'agent évolue | Le jeu |
| **Action** | Ce que l'agent peut faire | Aller à gauche, sauter, tirer |
| **État** | La situation actuelle | Position, score, ennemis |
| **Récompense** | Le feedback | +1 point, -1 vie, game over |

#### Exemples concrets

- **Jeux** : AlphaGo, AlphaZero (échecs, Go, Shogi)
- **Robotique** : un robot qui apprend à marcher
- **Recommandation** : optimiser le fil d'actualités pour maximiser l'engagement
- **Trading** : optimiser une stratégie d'investissement

> 🧠 **Pour aller plus loin** : L'apprentissage par renforcement est le plus proche de la façon dont les humains apprennent — par essai-erreur. Cependant, il nécessite beaucoup d'interactions avec l'environnement, ce qui le rend souvent impraticable dans le monde réel.

### 2.4 Tableau récapitulatif des types d'apprentissage

| Critère | Supervisé | Non-supervisé | Par renforcement |
|---------|-----------|---------------|------------------|
| **Données** | Étiquetées (X, y) | Non étiquetées (X) | Pas de dataset fixe |
| **Objectif** | Prédire y | Trouver des structures | Maximiser récompense |
| **Feedback** | Direct (labels) | Aucun | Récompense différée |
| **Exemples** | Classification, Régression | Clustering, PCA | Jeux, Robotique |
| **Difficulté** | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Données nécessaires** | Labels coûteux | Données brutes | Simulateur souvent nécessaire |

---

## 3. ⚙️ Le workflow ML complet

Tout projet de Machine Learning suit un pipeline structuré. Voici les étapes clés :

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  1. Définir  │    │  2. Collecter│    │  3. Explorer │    │  4. Préparer │
│  le problème │───▶│  les données │───▶│  (EDA)       │───▶│  (Preprocess)│
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
                                                                    │
       ┌────────────────────────────────────────────────────────────┘
       ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  5. Entraîner│    │  6. Évaluer  │    │  7. Optimiser│    │  8. Déployer │
│  le modèle   │───▶│  (Métriques) │───▶│  (Tuning)    │───▶│  (Production)│
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
```

### Étape 1 : Définir le problème

- Quel est l'objectif métier ?
- Est-ce un problème de régression ou classification ?
- Quelle métrique d'évaluation ?
- Quel est le critère de succès ?

> 💡 **Conseil de pro** : "Passez du temps à bien définir le problème. Un modèle parfait qui résout le **mauvais problème** est inutile."

### Étape 2 : Collecter les données

- Sources : bases de données, APIs, fichiers CSV, web scraping
- Qualité > Quantité (dans un premier temps)
- Vérifier les aspects légaux (RGPD)

### Étape 3 : Explorer les données (EDA)

- Statistiques descriptives
- Visualisations (distributions, corrélations)
- Identifier les valeurs manquantes, aberrantes
- Comprendre les relations entre variables

### Étape 4 : Préparer les données (Preprocessing)

- Nettoyer les données (manquantes, aberrantes)
- Encoder les variables catégorielles
- Normaliser/Standardiser les variables numériques
- Séparer en train/test sets

### Étape 5 : Entraîner le modèle

- Choisir un ou plusieurs algorithmes
- Entraîner sur les données d'entraînement
- Commencer simple (baseline), puis complexifier

### Étape 6 : Évaluer le modèle

- Calculer les métriques sur le **test set** (jamais sur le train set !)
- Comparer avec la baseline
- Analyser les erreurs

### Étape 7 : Optimiser

- Tuning des hyperparamètres (GridSearch, RandomSearch)
- Feature engineering
- Essayer d'autres algorithmes

### Étape 8 : Déployer

- Mettre le modèle en production (API, batch)
- Monitorer les performances
- Réentraîner si nécessaire

> 💡 **Conseil** : "80% du temps d'un data scientist est passé sur les étapes 2, 3 et 4 — les données — pas sur le modèle lui-même."

> ⚠️ **Attention** : "L'évaluation (étape 6) est **critique**. Un modèle qui semble bon sur les données d'entraînement peut être catastrophique en production. Toujours évaluer sur des données que le modèle n'a **jamais vues**."

---

## 4. 🔍 Quand utiliser le ML ?

Le Machine Learning n'est pas une solution universelle. Savoir quand l'utiliser (et quand ne **pas** l'utiliser) est une compétence essentielle.

### ✅ Bons cas d'usage

| Situation | Pourquoi le ML est adapté | Exemple |
|-----------|--------------------------|---------|
| Patterns complexes | Trop de règles à coder manuellement | Reconnaissance d'images |
| Beaucoup de données | Le ML a besoin de données pour apprendre | Recommandation Netflix |
| Le problème évolue | Les règles changent avec le temps | Détection de spam |
| Prédiction | Anticiper un résultat futur | Prévision de ventes |
| Personnalisation | Adapter à chaque utilisateur | Fil d'actualités |

### ❌ Mauvais cas d'usage

| Situation | Pourquoi éviter le ML | Alternative |
|-----------|----------------------|-------------|
| Règles simples et claires | Un `if/else` suffit | Programmation classique |
| Très peu de données | Le ML ne peut pas apprendre | Règles métier, heuristiques |
| Besoin d'explicabilité totale | Les modèles ML sont souvent des "boîtes noires" | Systèmes experts |
| Le coût d'erreur est inacceptable | Le ML fait toujours des erreurs | Systèmes déterministes |
| Pas de données historiques | Rien à apprendre | Collecte de données d'abord |

### Tableau de décision

| Problème | ML ou pas ? | Pourquoi |
|----------|-------------|----------|
| Calculer une TVA | ❌ Non | Règle simple : prix * 0.20 |
| Détecter des e-mails de phishing | ✅ Oui | Patterns complexes, évolutifs |
| Trier des fichiers par date | ❌ Non | Algorithme de tri classique |
| Prédire le cours d'une action | ⚠️ Peut-être | Données disponibles, mais très difficile |
| Segmenter une base clients | ✅ Oui | Patterns cachés dans les données |
| Convertir des degrés C en F | ❌ Non | Formule : F = C * 9/5 + 32 |
| Détecter des tumeurs sur des radios | ✅ Oui | Pattern visuel complexe |

> 💡 **Conseil de pro** : "Commencez **toujours** par une baseline simple (moyenne, règle métier, `if/else`) avant de construire un modèle ML. Si la baseline suffit, pas besoin de ML. Si elle ne suffit pas, vous avez un point de comparaison pour évaluer votre modèle."

> 💡 **Conseil** : "Posez-vous la question : est-ce qu'un humain expert pourrait résoudre ce problème avec les mêmes données ? Si oui, le ML a de bonnes chances d'y arriver aussi."

---

## 5. 🛠️ Les bibliothèques Python pour le ML

Python est le langage de référence pour le Machine Learning. Voici les bibliothèques essentielles :

### Écosystème ML Python

| Bibliothèque | Rôle | Utilisation principale |
|--------------|------|----------------------|
| **NumPy** | Calcul numérique | Tableaux, opérations mathématiques |
| **Pandas** | Manipulation de données | DataFrames, nettoyage, exploration |
| **Matplotlib** | Visualisation | Graphiques de base |
| **Seaborn** | Visualisation statistique | Graphiques avancés, heatmaps |
| **scikit-learn** | Machine Learning classique | Modèles, métriques, preprocessing |
| **XGBoost** | Gradient Boosting | Modèles performants (compétitions) |
| **TensorFlow / PyTorch** | Deep Learning | Réseaux de neurones |

### Quand utiliser quoi ?

```python
# NumPy : calcul numérique de base
import numpy as np
vecteur = np.array([1, 2, 3, 4, 5])
moyenne = np.mean(vecteur)

# Pandas : manipulation de données tabulaires
import pandas as pd
df = pd.read_csv("donnees.csv")
df.describe()  # Statistiques descriptives

# Matplotlib : visualisation
import matplotlib.pyplot as plt
plt.scatter(df["surface"], df["prix"])
plt.xlabel("Surface (m²)")
plt.ylabel("Prix (€)")
plt.title("Prix en fonction de la surface")
plt.show()

# Seaborn : visualisations statistiques avancées
import seaborn as sns
sns.heatmap(df.corr(), annot=True, cmap="coolwarm")
plt.title("Matrice de corrélation")
plt.show()

# scikit-learn : Machine Learning
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
modele = LinearRegression()
modele.fit(X_train, y_train)
predictions = modele.predict(X_test)
mse = mean_squared_error(y_test, predictions)
```

> 💡 **Conseil de pro** : "scikit-learn est votre meilleur ami pour débuter. Son API est **cohérente** : tous les modèles utilisent `.fit()`, `.predict()`, `.score()`. Apprenez cette API et vous pourrez utiliser n'importe quel algorithme."

### Installation rapide

```bash
uv add numpy pandas matplotlib seaborn scikit-learn jupyter
```

---

## 6. 📖 Vocabulaire essentiel

Maîtriser le vocabulaire est indispensable pour comprendre la documentation, les articles et communiquer avec d'autres data scientists.

### Termes fondamentaux

| Terme | Définition | Exemple |
|-------|-----------|---------|
| **Feature** (variable) | Une caractéristique d'entrée | Surface, nombre de pièces |
| **Target** (cible) | La variable à prédire | Prix de l'appartement |
| **Label** (étiquette) | La valeur connue de la target (supervisé) | "spam" ou "non-spam" |
| **Sample** (échantillon) | Une observation / une ligne | Un appartement spécifique |
| **Training set** | Données pour entraîner le modèle | 80% des données |
| **Test set** | Données pour évaluer le modèle | 20% des données |
| **Prédiction** | La sortie du modèle | Prix prédit = 250 000€ |
| **Modèle** | La fonction apprise par l'algorithme | La "formule" qui prédit |

### Concepts clés

| Terme | Définition | Analogie |
|-------|-----------|----------|
| **Overfitting** (sur-apprentissage) | Le modèle apprend le bruit des données d'entraînement | Un étudiant qui apprend les réponses par cœur sans comprendre |
| **Underfitting** (sous-apprentissage) | Le modèle est trop simple pour capturer les patterns | Un étudiant qui n'a pas assez révisé |
| **Biais** (bias) | Erreur due à des hypothèses trop simplistes | Supposer que toute relation est linéaire |
| **Variance** | Sensibilité du modèle aux fluctuations des données | Un modèle qui change beaucoup d'un dataset à l'autre |
| **Généralisation** | Capacité à bien performer sur des données inédites | Réussir un examen avec des questions nouvelles |

### Le compromis Biais-Variance

```
Erreur totale = Biais² + Variance + Bruit irréductible

     Erreur
       │
  High │  Underfitting                    Overfitting
       │     ╲                              ╱
       │      ╲    Biais²                  ╱ Variance
       │       ╲       ╲                ╱
       │        ╲        ╲           ╱
       │         ╲         ╲       ╱
       │          ╲          Zone optimale
       │           ╲            ╱
       └──────────────────────────────── Complexité du modèle
           Simple                   Complexe
```

> 💡 **Conseil** : "L'objectif n'est pas de minimiser l'erreur sur les données d'entraînement, mais de **minimiser l'erreur sur des données jamais vues** (généralisation). C'est le cœur du ML."

### Hyperparamètres vs Paramètres

| | Paramètres | Hyperparamètres |
|--|-----------|-----------------|
| **Définition** | Appris par le modèle pendant l'entraînement | Fixés par le data scientist avant l'entraînement |
| **Exemple** | Coefficients d'une régression linéaire | Nombre de voisins (K) dans KNN |
| **Comment les trouver** | Algorithme d'apprentissage | GridSearch, RandomSearch, expérience |
| **Modifiables pendant l'entraînement** | Oui (c'est le but) | Non (fixés avant) |

> 🧠 **Pour aller plus loin** : Le réglage des hyperparamètres (hyperparameter tuning) est une étape cruciale qui peut significativement améliorer les performances d'un modèle. Nous verrons les techniques de GridSearch et RandomSearch dans les chapitres suivants.

---

## 7. 📈 Les métriques : pourquoi c'est fondamental

Les métriques sont la **boussole** d'un projet ML. Sans métriques appropriées, impossible de savoir si votre modèle est bon ou non.

### Principe fondamental

> ⚠️ **Attention** : "Un modèle sans métrique d'évaluation, c'est comme conduire sans tableau de bord. Vous ne savez pas si vous allez dans la bonne direction."

### Aperçu des métriques

| Type de problème | Métriques principales | Détails |
|-----------------|----------------------|---------|
| **Régression** | MSE, RMSE, MAE, R², MAPE | Voir Chapitre 4 |
| **Classification** | Accuracy, Precision, Recall, F1, AUC-ROC | Voir Chapitre 5 |
| **Clustering** | Silhouette Score, Inertie | Voir chapitres avancés |

### La métrique dépend du contexte métier

| Contexte | Métrique privilégiée | Raison |
|----------|---------------------|--------|
| Diagnostic médical | **Recall** (sensibilité) | Ne pas rater un malade (FN coûteux) |
| Filtre anti-spam | **Precision** | Ne pas classer un vrai mail en spam (FP coûteux) |
| Prédiction de prix | **RMSE** ou **MAE** | Erreur en unité de la cible (€) |
| Classes déséquilibrées | **F1-Score** ou **AUC-ROC** | Accuracy est trompeuse |

> 💡 **Conseil de pro** : "Choisissez **toujours** votre métrique d'évaluation **AVANT** de commencer à modéliser. Cette métrique doit refléter le **coût métier** des erreurs."

---

## 🎯 Points clés à retenir

1. **Le ML apprend à partir de données** plutôt que de règles codées en dur
2. **Trois types d'apprentissage** : supervisé (avec labels), non-supervisé (sans labels), par renforcement (récompenses)
3. **Supervisé** se divise en régression (valeur continue) et classification (catégorie)
4. **Le workflow ML** : Problème → Données → Exploration → Preprocessing → Modèle → Évaluation → Optimisation → Déploiement
5. **80% du travail** porte sur les données, pas sur le modèle
6. **Ne pas tout résoudre avec le ML** : si un `if/else` suffit, inutile de complexifier
7. **Toujours commencer par une baseline simple** avant un modèle complexe
8. **Les métriques sont fondamentales** : choisir la bonne métrique selon le contexte métier
9. **Overfitting** est l'ennemi principal : évaluer toujours sur des données inédites
10. **scikit-learn** est la bibliothèque de référence pour le ML classique en Python

---

## ✅ Checklist de validation

- [ ] Je sais expliquer la différence entre ML et programmation traditionnelle
- [ ] Je sais distinguer apprentissage supervisé, non-supervisé et par renforcement
- [ ] Je sais si un problème est de la régression ou de la classification
- [ ] Je connais les 8 étapes du workflow ML
- [ ] Je sais quand utiliser le ML et quand ne pas l'utiliser
- [ ] Je comprends les concepts d'overfitting et underfitting
- [ ] Je connais la différence entre paramètres et hyperparamètres
- [ ] Je sais ce que sont les features, la target, le training set et le test set
- [ ] J'ai installé scikit-learn, pandas, numpy et matplotlib
- [ ] Je comprends pourquoi le choix de la métrique est crucial

---

**Suivant** : [Chapitre 2 : Environnement et Outils](02-environnement-setup.md)
