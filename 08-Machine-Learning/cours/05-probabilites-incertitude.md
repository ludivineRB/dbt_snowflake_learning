# Chapitre 5 : Probabilités pour ne plus avoir Peur de l'Incertitude

## 🎯 Objectifs

- Comprendre ce qu'est une probabilité et ce qu'elle n'est PAS
- Connaître les distributions essentielles (normale, uniforme, binomiale, Poisson)
- Maîtriser la distribution normale et la règle 68-95-99.7
- Comprendre les intervalles de confiance et la notion de "confiance" dans les prédictions
- Découvrir la régression logistique comme classification probabiliste
- Comprendre le théorème de Bayes avec des exemples concrets
- Faire le lien entre probabilités et Machine Learning

---

## 1. 🧠 Probabilité ≠ prédiction parfaite

### 1.1 Ce que "70% de chances" veut dire

Quand la météo annonce **"il y a 70% de chances qu'il pleuve demain"**, cela ne signifie PAS :
- ❌ "Il va pleuvoir à 70% d'intensité"
- ❌ "Il va pleuvoir pendant 70% de la journée"
- ❌ "On est sûr à 70% qu'il va pleuvoir"

Cela signifie :
- ✅ "Sur 100 jours avec des conditions météo identiques, il pleuvrait environ 70 fois"

```
100 jours similaires :
🌧🌧🌧🌧🌧🌧🌧🌧🌧🌧  → 10 jours de pluie
🌧🌧🌧🌧🌧🌧🌧🌧🌧🌧  → 20
🌧🌧🌧🌧🌧🌧🌧🌧🌧🌧  → 30
🌧🌧🌧🌧🌧🌧🌧🌧🌧🌧  → 40
🌧🌧🌧🌧🌧🌧🌧🌧🌧🌧  → 50
🌧🌧🌧🌧🌧🌧🌧🌧🌧🌧  → 60
🌧🌧🌧🌧🌧🌧🌧🌧🌧🌧  → 70 jours de pluie (70%)
☀️☀️☀️☀️☀️☀️☀️☀️☀️☀️  → 80
☀️☀️☀️☀️☀️☀️☀️☀️☀️☀️  → 90
☀️☀️☀️☀️☀️☀️☀️☀️☀️☀️  → 100 (30% sans pluie)
```

> 💡 **Conseil** : "Une probabilité est une **fréquence à long terme**. Dire 'P = 0.7' signifie 'si on répétait l'expérience un grand nombre de fois, l'événement se produirait environ 70% du temps'."

### 1.2 Propriétés fondamentales

| Propriété | Formule | Explication |
|-----------|---------|-------------|
| Toujours entre 0 et 1 | 0 ≤ P(A) ≤ 1 | 0 = impossible, 1 = certain |
| Somme = 1 | P(A) + P(non A) = 1 | Il pleut OU il ne pleut pas |
| Événements indépendants | P(A et B) = P(A) × P(B) | Si A n'influence pas B |

```python
import numpy as np

# Simulation : lancer un dé 10000 fois
np.random.seed(42)
lancers = np.random.randint(1, 7, size=10000)

# Probabilité d'obtenir un 6
p_six = np.mean(lancers == 6)
print(f"P(6) théorique : {1/6:.4f}")
print(f"P(6) simulée   : {p_six:.4f}")

# Plus on lance, plus on se rapproche de la théorie
for n in [10, 100, 1000, 10000]:
    p = np.mean(lancers[:n] == 6)
    print(f"  n={n:>5} → P(6) = {p:.4f}")
```

### 1.3 Fréquentiste vs bayésien (intuitivement)

| Approche | Interprétation de P = 0.7 | Analogie |
|----------|--------------------------|----------|
| **Fréquentiste** | "Sur 100 répétitions, l'événement arrive ~70 fois" | Lancer un dé 1000 fois |
| **Bayésien** | "Mon degré de croyance est de 70%" | "Je suis confiant à 70% que c'est vrai" |

```
Fréquentiste :
  "La pièce est tombée sur face 70 fois sur 100.
   Donc P(face) ≈ 0.7"
  → Basé sur l'observation répétée

Bayésien :
  "Je crois initialement que P(face) = 0.5 (pièce équilibrée).
   Après avoir vu 70 faces sur 100, je mets à jour ma croyance :
   P(face) ≈ 0.7"
  → Basé sur des croyances mises à jour par les données
```

> 💡 **Conseil** : "En Machine Learning, on utilise souvent les deux approches. La régression logistique est fréquentiste, tandis que les modèles bayésiens mettent à jour leurs 'croyances' au fur et à mesure des données."

---

## 2. 📊 Distribution normale (la fameuse courbe en cloche)

### 2.1 Pourquoi elle est partout

La distribution normale (ou gaussienne) est la distribution la plus importante en statistique. Elle apparaît **naturellement** dans de nombreux phénomènes :

- Taille des personnes dans une population
- Scores à un examen
- Erreurs de mesure
- Temps de trajet quotidien
- Poids des bébés à la naissance

**Pourquoi ?** À cause du **théorème central limite** (TCL) :

> Quand on fait la **moyenne** de beaucoup de variables aléatoires indépendantes, le résultat suit toujours une distribution normale, **quelle que soit** la distribution d'origine.

```
Théorème Central Limite (intuition) :

  Distribution originale       Moyenne de 2 tirages      Moyenne de 30 tirages
  (peut être n'importe quoi)

      ▄▄▄▄                         ▄▄                          ▄▄
      ████                       ▄████▄                      ▄████▄
      ████▄                     ██████████                 ▄████████▄
  ▄▄▄▄██████                   ████████████              ▄████████████▄
  ████████████                ████████████████          ▄████████████████▄

  → Forme bizarre            → Commence à ressembler   → Presque parfaitement
                                à une cloche                une courbe en cloche !
```

### 2.2 Moyenne et écart-type : les deux paramètres

Une distribution normale est entièrement définie par **deux nombres** :
- **μ (mu)** : la **moyenne** (centre de la cloche)
- **σ (sigma)** : l'**écart-type** (largeur de la cloche)

```
σ petit (données serrées) :          σ grand (données étalées) :

         ▄████▄                            ▄▄▄▄▄▄
       ▄████████▄                       ▄▄████████▄▄
     ▄████████████▄                   ▄████████████████▄
   ▄████████████████▄              ▄████████████████████████▄
  ████████████████████           ████████████████████████████████
──────────┼──────────           ────────────────┼────────────────
          μ                                     μ

→ Prédictions très précises        → Prédictions plus incertaines
```

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Générer des données normales
np.random.seed(42)

# Distribution de la taille (en cm) de 1000 personnes
tailles = np.random.normal(loc=170, scale=10, size=1000)

print(f"Moyenne (μ) : {np.mean(tailles):.1f} cm")
print(f"Écart-type (σ) : {np.std(tailles):.1f} cm")
print(f"Min : {np.min(tailles):.1f} cm")
print(f"Max : {np.max(tailles):.1f} cm")

# Visualiser
plt.figure(figsize=(12, 6))
plt.hist(tailles, bins=40, density=True, alpha=0.7, color='steelblue',
         edgecolor='black', label='Données simulées')

# Superposer la courbe théorique
x = np.linspace(130, 210, 200)
plt.plot(x, stats.norm.pdf(x, 170, 10), 'r-', linewidth=2,
         label='Distribution normale théorique')

plt.xlabel("Taille (cm)")
plt.ylabel("Densité de probabilité")
plt.title("Distribution de la taille — Courbe en cloche")
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```

### 2.3 La règle 68-95-99.7

C'est la règle la plus utile des statistiques. Elle vous dit quelle proportion des données se trouve à 1, 2 ou 3 écarts-types de la moyenne.

```
                        99.7% (μ ± 3σ)
                 ┌──────────────────────────────────┐
                 │     95% (μ ± 2σ)                 │
                 │  ┌────────────────────────────┐  │
                 │  │   68% (μ ± 1σ)             │  │
                 │  │ ┌────────────────────┐     │  │
                 │  │ │                    │     │  │
                 │  │ │     ▄████▄         │     │  │
                 │  │ │   ▄████████▄       │     │  │
                 │  │ │ ▄████████████▄     │     │  │
                 │  │ ▄████████████████▄   │     │  │
              ▄▄▄████████████████████████████▄▄▄▄
─────────────────────────┼───────────────────────────────
             μ-3σ  μ-2σ  μ-σ   μ   μ+σ  μ+2σ  μ+3σ
```

| Intervalle | % des données | Exemple (taille : μ=170, σ=10) |
|:----------:|:-------------:|-------------------------------|
| μ ± 1σ | **68%** | Entre 160 et 180 cm |
| μ ± 2σ | **95%** | Entre 150 et 190 cm |
| μ ± 3σ | **99.7%** | Entre 140 et 200 cm |

```python
# Vérifier la règle 68-95-99.7
mu, sigma = 170, 10

dans_1_sigma = np.mean((tailles >= mu - sigma) & (tailles <= mu + sigma))
dans_2_sigma = np.mean((tailles >= mu - 2*sigma) & (tailles <= mu + 2*sigma))
dans_3_sigma = np.mean((tailles >= mu - 3*sigma) & (tailles <= mu + 3*sigma))

print(f"Dans μ ± 1σ : {dans_1_sigma:.1%} (théorique : 68.3%)")
print(f"Dans μ ± 2σ : {dans_2_sigma:.1%} (théorique : 95.4%)")
print(f"Dans μ ± 3σ : {dans_3_sigma:.1%} (théorique : 99.7%)")
```

> 💡 **Conseil** : "La règle 68-95-99.7 est **extrêmement utile** pour détecter les anomalies. Si une valeur est à plus de 3 écarts-types de la moyenne, elle est probablement un outlier (seulement 0.3% de chances d'être 'normale')."

### 2.4 Application : détecter des anomalies

```python
# Transactions bancaires (montant en €)
np.random.seed(42)
transactions = np.random.normal(loc=50, scale=15, size=1000)

# Ajouter quelques transactions frauduleuses
transactions = np.append(transactions, [250, 300, -50, 280])

mu = np.mean(transactions)
sigma = np.std(transactions)

# Détecter les anomalies (> 3 écarts-types)
anomalies = np.abs(transactions - mu) > 3 * sigma
print(f"Transactions normales : {np.sum(~anomalies)}")
print(f"Anomalies détectées : {np.sum(anomalies)}")
print(f"Valeurs anormales : {transactions[anomalies]}")

# Visualiser
plt.figure(figsize=(12, 5))
plt.scatter(range(len(transactions)), transactions, c=['red' if a else 'steelblue' for a in anomalies],
            alpha=0.5, s=10)
plt.axhline(y=mu + 3*sigma, color='red', linestyle='--', label=f'μ + 3σ = {mu + 3*sigma:.0f}€')
plt.axhline(y=mu - 3*sigma, color='red', linestyle='--', label=f'μ - 3σ = {mu - 3*sigma:.0f}€')
plt.axhline(y=mu, color='green', linestyle='-', alpha=0.5, label=f'μ = {mu:.0f}€')
plt.xlabel("Transaction #")
plt.ylabel("Montant (€)")
plt.title("Détection d'anomalies avec la règle des 3 écarts-types")
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```

---

## 3. 📈 Autres distributions utiles

### 3.1 Distribution uniforme

Tous les résultats ont la **même probabilité**.

```
Distribution uniforme (dé à 6 faces) :

 P(x)
 1/6 │  ▄▄  ▄▄  ▄▄  ▄▄  ▄▄  ▄▄
     │  ██  ██  ██  ██  ██  ██
     │  ██  ██  ██  ██  ██  ██
     └──1───2───3───4───5───6── x
```

```python
# Distribution uniforme
uniform = np.random.uniform(low=0, high=10, size=10000)

plt.figure(figsize=(10, 4))
plt.hist(uniform, bins=50, density=True, alpha=0.7, color='steelblue', edgecolor='black')
plt.title("Distribution uniforme [0, 10]")
plt.xlabel("Valeur")
plt.ylabel("Densité")
plt.grid(True, alpha=0.3)
plt.show()
```

| Caractéristique | Valeur |
|----------------|--------|
| **Quand l'utiliser** | Quand rien ne favorise un résultat |
| **Exemples** | Dé, générateur aléatoire, initialisation de poids |
| **Paramètres** | a (min), b (max) |

### 3.2 Distribution binomiale

Nombre de **succès** sur N essais indépendants, avec probabilité p de succès à chaque essai.

```
Distribution binomiale (n=10, p=0.5) :
"Sur 10 lancers de pièce, combien de faces ?"

 P(x)
  0.25│        ▄▄
      │      ▄████▄
  0.20│    ▄████████▄
      │  ▄████████████▄
  0.10│▄████████████████▄
      │████████████████████▄
  0.00└─0──1──2──3──4──5──6──7──8──9──10─ x (nb de faces)
```

```python
from scipy import stats

# Exemple : sur 100 emails, 30% sont du spam
# Combien de spams dans un lot de 20 emails ?
n, p = 20, 0.3

x = np.arange(0, 21)
probas = stats.binom.pmf(x, n, p)

plt.figure(figsize=(10, 5))
plt.bar(x, probas, color='steelblue', edgecolor='black', alpha=0.7)
plt.xlabel("Nombre de spams sur 20 emails")
plt.ylabel("Probabilité")
plt.title(f"Distribution binomiale (n={n}, p={p})")
plt.grid(True, alpha=0.3, axis='y')
plt.show()

# Statistiques
print(f"Espérance : {n * p:.1f} spams")
print(f"P(exactement 6 spams) : {stats.binom.pmf(6, n, p):.4f}")
print(f"P(au moins 10 spams) : {1 - stats.binom.cdf(9, n, p):.4f}")
```

| Caractéristique | Valeur |
|----------------|--------|
| **Quand l'utiliser** | Compter des succès/échecs |
| **Exemples** | Nb de clics sur une pub, nb de clients qui résitient, nb de pièces défectueuses |
| **Paramètres** | n (nb essais), p (probabilité de succès) |

### 3.3 Distribution de Poisson

Nombre d'événements qui se produisent dans un **intervalle fixe** (temps, espace).

```
Distribution de Poisson (λ=4) :
"Nombre de clients qui arrivent par heure"

 P(x)
  0.20│     ▄▄
      │   ▄████▄
  0.15│ ▄████████▄
      │████████████▄
  0.10│██████████████▄
      │████████████████▄
  0.05│██████████████████▄▄
      │████████████████████████▄▄▄
  0.00└─0──1──2──3──4──5──6──7──8──9──10─ x
```

```python
# Exemple : 4 clients arrivent en moyenne par heure
lambda_param = 4

x = np.arange(0, 15)
probas = stats.poisson.pmf(x, lambda_param)

plt.figure(figsize=(10, 5))
plt.bar(x, probas, color='steelblue', edgecolor='black', alpha=0.7)
plt.xlabel("Nombre de clients par heure")
plt.ylabel("Probabilité")
plt.title(f"Distribution de Poisson (λ={lambda_param})")
plt.grid(True, alpha=0.3, axis='y')
plt.show()

print(f"P(0 clients) : {stats.poisson.pmf(0, lambda_param):.4f}")
print(f"P(exactement 4) : {stats.poisson.pmf(4, lambda_param):.4f}")
print(f"P(plus de 8) : {1 - stats.poisson.cdf(8, lambda_param):.4f}")
```

| Caractéristique | Valeur |
|----------------|--------|
| **Quand l'utiliser** | Événements rares dans un intervalle fixe |
| **Exemples** | Nb d'appels au support/heure, nb d'erreurs/page, nb de pannes/mois |
| **Paramètres** | λ (taux moyen d'occurrence) |

### 3.4 Tableau récapitulatif

| Distribution | Type | Paramètres | Exemple ML | Forme |
|-------------|------|-----------|------------|-------|
| **Normale** | Continue | μ, σ | Erreurs de prédiction, features | Cloche |
| **Uniforme** | Continue | a, b | Initialisation aléatoire | Rectangle |
| **Binomiale** | Discrète | n, p | Nb de conversions sur n visiteurs | Cloche discrète |
| **Poisson** | Discrète | λ | Nb d'événements par unité de temps | Asymétrique |

---

## 4. 🎯 Intervalles de confiance : quantifier l'incertitude

### 4.1 Pourquoi parler de "confiance" ?

En ML, un modèle ne donne jamais une réponse **certaine**. Il donne une estimation avec une **marge d'erreur**.

```
Prédiction sans confiance :          Prédiction avec confiance :
  "Le prix est de 250 000€"           "Le prix est de 250 000€ ± 30 000€
                                        (intervalle de confiance à 95%)"

  → Aucune idée de la fiabilité       → On sait que le vrai prix est
                                         probablement entre 220k et 280k€
```

### 4.2 Intervalle de confiance visualisé

```
                    Intervalle de confiance à 95%
                 ┌──────────────────────────────┐
                 │                              │
                 │          ▄████▄              │
                 │        ▄████████▄            │
                 │      ▄████████████▄          │
               ▄▄████████████████████████▄▄
─────────────────────────┼───────────────────────
               220k     250k               280k
                          ↑
                    Estimation ponctuelle

"On est sûr à 95% que le vrai prix est entre 220k et 280k€"
```

```python
from scipy import stats

# Exemple : estimer le prix moyen à partir d'un échantillon
np.random.seed(42)
prix_echantillon = np.random.normal(loc=250000, scale=40000, size=50)

# Calculer l'intervalle de confiance à 95%
moyenne = np.mean(prix_echantillon)
erreur_standard = stats.sem(prix_echantillon)  # Standard Error of the Mean
ic_95 = stats.t.interval(
    confidence=0.95,
    df=len(prix_echantillon) - 1,
    loc=moyenne,
    scale=erreur_standard
)

print(f"Moyenne de l'échantillon : {moyenne:,.0f}€")
print(f"Intervalle de confiance 95% : [{ic_95[0]:,.0f}€ ; {ic_95[1]:,.0f}€]")
print(f"Marge d'erreur : ±{(ic_95[1] - moyenne):,.0f}€")

# Visualiser
plt.figure(figsize=(10, 4))
plt.hist(prix_echantillon, bins=20, density=True, alpha=0.7,
         color='steelblue', edgecolor='black')
plt.axvline(x=moyenne, color='red', linewidth=2, label=f'Moyenne = {moyenne:,.0f}€')
plt.axvline(x=ic_95[0], color='orange', linewidth=2, linestyle='--',
            label=f'IC 95% = [{ic_95[0]:,.0f} ; {ic_95[1]:,.0f}]€')
plt.axvline(x=ic_95[1], color='orange', linewidth=2, linestyle='--')
plt.xlabel("Prix (€)")
plt.ylabel("Densité")
plt.title("Estimation du prix moyen avec intervalle de confiance")
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```

### 4.3 Plus de données = plus de précision

```python
# Impact de la taille de l'échantillon sur l'intervalle de confiance
tailles_echantillon = [10, 30, 50, 100, 500, 1000]

print(f"{'Taille':>8} {'Moyenne':>12} {'IC 95% inf':>12} {'IC 95% sup':>12} {'Largeur':>10}")
print("-" * 60)

for n in tailles_echantillon:
    ech = np.random.normal(loc=250000, scale=40000, size=n)
    moy = np.mean(ech)
    se = stats.sem(ech)
    ic = stats.t.interval(0.95, df=n-1, loc=moy, scale=se)
    largeur = ic[1] - ic[0]
    print(f"{n:>8} {moy:>12,.0f} {ic[0]:>12,.0f} {ic[1]:>12,.0f} {largeur:>10,.0f}")
```

> 💡 **Conseil** : "Plus vous avez de données, plus votre intervalle de confiance est **étroit** (précis). C'est une raison fondamentale pour laquelle le ML a besoin de **beaucoup de données**."

---

## 5. 🤖 Application : Classification probabiliste

### 5.1 Prédire non pas "oui/non" mais "probabilité de oui"

La plupart des algorithmes de classification ne prédisent pas simplement une classe — ils prédisent une **probabilité**.

```
Prédiction binaire :                 Prédiction probabiliste :
  "Ce client va résilier : OUI"        "Ce client a 82% de chances de résilier"

  → Pas de nuance                     → On peut agir en fonction du risque :
                                        - 82% → Appeler en urgence !
                                        - 55% → Envoyer une promotion
                                        - 20% → Ne rien faire
```

> 💡 **Conseil** : "Les probabilités permettent de **prioriser les actions**. Un client à 90% de chances de résilier ne nécessite pas la même intervention qu'un client à 30%. C'est beaucoup plus utile qu'un simple oui/non."

### 5.2 Introduction à la régression logistique

Malgré son nom, la régression logistique est un algorithme de **classification** (pas de régression). Elle prédit la **probabilité** qu'un point appartienne à une classe.

**Le problème** : la régression linéaire peut donner des valeurs < 0 ou > 1, ce qui n'est pas une probabilité valide.

```
Régression linéaire (mauvais pour la classification) :

  P(spam)
   1.5│           /
      │         /
   1.0│───────/──────── ← dépasse 1 ! (pas une proba valide)
      │     /
   0.5│   /
      │ /
   0.0│/─────────────── ← en dessous de 0 !
  -0.5│
      └────────────── nb mots suspects
```

**La solution** : utiliser la **fonction sigmoïde** pour "compresser" la sortie entre 0 et 1.

### 5.3 La fonction sigmoïde

```
σ(z) = 1 / (1 + e⁻ᶻ)

    P(spam)
    1.0│                    ─────────────
       │                 ╱
    0.8│               ╱
       │             ╱
    0.5│─ ─ ─ ─ ─ ● ─ ─ ─ ─ ─ ─ ─ ─  ← seuil de décision
       │         ╱
    0.2│       ╱
       │     ╱
    0.0│────╱────────────────────────
       └────────────┼──────────── z = ax + b
                     0

    z < 0 → σ(z) < 0.5 → Classe 0 (pas spam)
    z > 0 → σ(z) > 0.5 → Classe 1 (spam)
    z = 0 → σ(z) = 0.5 → Incertain (pile entre les deux)
```

```python
import numpy as np
import matplotlib.pyplot as plt

def sigmoid(z):
    """La fonction sigmoïde."""
    return 1 / (1 + np.exp(-z))

# Visualiser la sigmoïde
z = np.linspace(-8, 8, 200)

plt.figure(figsize=(10, 6))
plt.plot(z, sigmoid(z), 'b-', linewidth=3)
plt.axhline(y=0.5, color='red', linestyle='--', alpha=0.5, label='Seuil = 0.5')
plt.axhline(y=0, color='grey', linewidth=0.5)
plt.axhline(y=1, color='grey', linewidth=0.5)
plt.axvline(x=0, color='grey', linewidth=0.5)
plt.xlabel("z (score linéaire)")
plt.ylabel("σ(z) = probabilité")
plt.title("La fonction sigmoïde transforme tout nombre en probabilité [0, 1]")
plt.legend()
plt.grid(True, alpha=0.3)

# Annotations
plt.annotate('P ≈ 0\n(Très improbable)', xy=(-6, 0.05), fontsize=10, color='blue')
plt.annotate('P ≈ 1\n(Très probable)', xy=(4, 0.9), fontsize=10, color='blue')
plt.annotate('P = 0.5\n(Incertain)', xy=(0.5, 0.55), fontsize=10, color='red')

plt.show()
```

### 5.4 Régression logistique avec scikit-learn

```python
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import numpy as np

# Générer un dataset
X, y = make_classification(
    n_samples=500,
    n_features=2,
    n_redundant=0,
    n_informative=2,
    random_state=42
)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Entraîner la régression logistique
model = LogisticRegression()
model.fit(X_train, y_train)

# Prédire les classes
y_pred = model.predict(X_test)

# Prédire les PROBABILITÉS
y_proba = model.predict_proba(X_test)

print("=== Premiers résultats ===")
print(f"{'Classe prédite':>15} {'P(classe 0)':>12} {'P(classe 1)':>12} {'Vrai label':>12}")
print("-" * 55)
for i in range(10):
    print(f"{y_pred[i]:>15} {y_proba[i, 0]:>12.4f} {y_proba[i, 1]:>12.4f} {y_test[i]:>12}")

print(f"\nAccuracy : {accuracy_score(y_test, y_pred):.2%}")
print(f"\n{classification_report(y_test, y_pred)}")
```

### 5.5 Utiliser les probabilités pour prendre des décisions

```python
# Exemple métier : prédire le churn
# Action différente selon le niveau de risque

seuils = {
    'Risque faible': (0.0, 0.3),
    'Risque moyen': (0.3, 0.6),
    'Risque élevé': (0.6, 0.8),
    'Risque critique': (0.8, 1.0),
}

actions = {
    'Risque faible': 'Ne rien faire',
    'Risque moyen': 'Envoyer un email promotionnel',
    'Risque élevé': 'Appeler le client',
    'Risque critique': 'Offre exceptionnelle + appel du manager',
}

# Probabilités de churn pour 5 clients
proba_churn = y_proba[:5, 1]

print(f"{'Client':>8} {'P(churn)':>10} {'Niveau':>18} {'Action':>40}")
print("-" * 80)
for i, p in enumerate(proba_churn):
    for niveau, (low, high) in seuils.items():
        if low <= p < high:
            print(f"{'Client ' + str(i+1):>8} {p:>10.2%} {niveau:>18} {actions[niveau]:>40}")
            break
```

> ⚠️ **Attention** : "Le seuil de 0.5 n'est pas toujours optimal ! En médecine, on préfère un seuil bas (0.3) pour ne pas rater de malades. En anti-spam, on préfère un seuil haut (0.7) pour ne pas bloquer de vrais emails."

---

## 6. 📖 Le théorème de Bayes

### 6.1 L'intuition avec un exemple concret

**Problème** : Vous avez un filtre anti-spam. Un email contient le mot "gratuit". Quelle est la probabilité que ce soit du spam ?

Ce qu'on sait :
- 30% des emails sont du spam → P(spam) = 0.30
- 80% des spams contiennent "gratuit" → P(gratuit | spam) = 0.80
- 10% des emails légitimes contiennent "gratuit" → P(gratuit | légitime) = 0.10

Ce qu'on cherche :
- P(spam | gratuit) = "sachant que l'email contient 'gratuit', quelle proba que ce soit du spam ?"

### 6.2 La formule de Bayes

```
                    P(B | A) × P(A)
P(A | B) = ─────────────────────────
                      P(B)

En français :
                    P(gratuit | spam) × P(spam)
P(spam | gratuit) = ──────────────────────────────
                             P(gratuit)
```

### 6.3 Calcul pas à pas

```
Étape 1 : Calculer P(gratuit)
  P(gratuit) = P(gratuit | spam) × P(spam) + P(gratuit | légitime) × P(légitime)
             = 0.80 × 0.30 + 0.10 × 0.70
             = 0.24 + 0.07
             = 0.31

Étape 2 : Appliquer Bayes
  P(spam | gratuit) = (0.80 × 0.30) / 0.31
                    = 0.24 / 0.31
                    ≈ 0.774

→ Il y a 77.4% de chances que ce soit du spam !
```

```python
# Théorème de Bayes : exemple spam
p_spam = 0.30
p_legitime = 0.70
p_gratuit_sachant_spam = 0.80
p_gratuit_sachant_legitime = 0.10

# P(gratuit)
p_gratuit = (p_gratuit_sachant_spam * p_spam +
             p_gratuit_sachant_legitime * p_legitime)

# P(spam | gratuit)
p_spam_sachant_gratuit = (p_gratuit_sachant_spam * p_spam) / p_gratuit

print(f"P(gratuit) = {p_gratuit:.4f}")
print(f"P(spam | contient 'gratuit') = {p_spam_sachant_gratuit:.4f}")
print(f"\n→ Un email contenant 'gratuit' a {p_spam_sachant_gratuit:.1%} de chances d'être du spam")
```

### 6.4 Visualisation avec un arbre

```
                    Tous les emails (100%)
                    ╱                    ╲
               Spam (30%)           Légitime (70%)
              ╱        ╲            ╱           ╲
     "gratuit"    pas "gratuit"  "gratuit"    pas "gratuit"
       (80%)        (20%)         (10%)         (90%)
       = 24%        = 6%          = 7%          = 63%

   Parmi les emails avec "gratuit" (24% + 7% = 31%) :
   → 24% sont du spam → P(spam | gratuit) = 24/31 ≈ 77.4%
```

### 6.5 Bayes avec plusieurs mots

```python
# Extension : Bayes naïf avec plusieurs mots
# (C'est le principe du Naive Bayes classifier !)

def bayes_spam(mots_observes, p_mots_spam, p_mots_legit, p_spam=0.3):
    """
    Classifieur bayésien naïf pour le spam.

    Args:
        mots_observes: liste de mots trouvés dans l'email
        p_mots_spam: dict {mot: P(mot | spam)}
        p_mots_legit: dict {mot: P(mot | légitime)}
        p_spam: probabilité a priori d'être du spam
    """
    p_legit = 1 - p_spam

    # Hypothèse "naïve" : les mots sont indépendants
    # P(mots | spam) = P(mot1 | spam) × P(mot2 | spam) × ...
    p_mots_si_spam = np.prod([p_mots_spam.get(m, 0.01) for m in mots_observes])
    p_mots_si_legit = np.prod([p_mots_legit.get(m, 0.01) for m in mots_observes])

    # Bayes
    p_spam_sachant_mots = (p_mots_si_spam * p_spam) / \
                          (p_mots_si_spam * p_spam + p_mots_si_legit * p_legit)

    return p_spam_sachant_mots

# Probabilités conditionnelles apprises des données
p_mots_spam = {
    'gratuit': 0.80, 'gagner': 0.60, 'urgent': 0.50,
    'cliquez': 0.70, 'offre': 0.55, 'bonjour': 0.30,
}
p_mots_legit = {
    'gratuit': 0.10, 'gagner': 0.05, 'urgent': 0.15,
    'cliquez': 0.08, 'offre': 0.12, 'bonjour': 0.80,
}

# Tester avec différents emails
emails = [
    ['gratuit', 'gagner', 'cliquez'],    # Très spam
    ['bonjour', 'offre'],                 # Ambigu
    ['bonjour'],                          # Probablement légitime
    ['urgent', 'gratuit', 'offre', 'gagner'],  # Très très spam
]

for email in emails:
    p = bayes_spam(email, p_mots_spam, p_mots_legit)
    label = "SPAM" if p > 0.5 else "Légitime"
    print(f"Email contenant {email}")
    print(f"  → P(spam) = {p:.4f} → {label}\n")
```

### 6.6 Naive Bayes avec scikit-learn

```python
from sklearn.naive_bayes import GaussianNB
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Dataset
X, y = make_classification(n_samples=1000, n_features=10,
                           n_informative=5, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Naive Bayes
nb = GaussianNB()
nb.fit(X_train, y_train)

# Prédictions et probabilités
y_pred = nb.predict(X_test)
y_proba = nb.predict_proba(X_test)

print(f"Accuracy : {accuracy_score(y_test, y_pred):.2%}")
print(f"\nExemple de probabilités :")
for i in range(5):
    print(f"  P(classe 0) = {y_proba[i, 0]:.4f}, P(classe 1) = {y_proba[i, 1]:.4f} → Prédit {y_pred[i]}")
```

> 💡 **Conseil** : "Le classifieur Naive Bayes est **rapide, simple et étonnamment efficace** pour la classification de texte (spam, sentiment, catégorisation). C'est souvent un excellent point de départ (baseline)."

---

## 7. 🔗 Lien avec le ML : maximum de vraisemblance (intuition)

### 7.1 L'idée centrale

Le **maximum de vraisemblance** (Maximum Likelihood Estimation, MLE) est le principe fondamental derrière l'entraînement de nombreux modèles de ML.

**Question** : "Quels paramètres du modèle rendent les données observées les **plus probables** ?"

```
On a observé ces données :  [2.1, 1.8, 2.3, 1.9, 2.0]

Quelle distribution normale les a le plus probablement générées ?

  Hypothèse 1 : μ=0, σ=1     Hypothèse 2 : μ=2, σ=0.2    Hypothèse 3 : μ=5, σ=1

      ▄████▄                       ▄██▄                         ▄████▄
    ▄████████▄                   ▄██████▄                     ▄████████▄
  ▄████████████▄               ▄██████████▄                 ▄████████████▄
──┼────────────────       ──────┼──────────────         ──────────────┼────
  0    ●●●●●                    2  ●●●●●                              5
  ↑ Données loin              ↑ Données au centre !          ↑ Données loin
  du centre                    → Vraisemblance HAUTE          du centre
  → Vraisemblance basse                                      → Vraisemblance basse

  ⟹ Hypothèse 2 est la meilleure ! (μ=2, σ=0.2)
```

### 7.2 En pratique

```python
from scipy import stats
import numpy as np

# Données observées
donnees = np.array([2.1, 1.8, 2.3, 1.9, 2.0, 2.2, 1.7, 2.1])

# Estimer les paramètres par maximum de vraisemblance
mu_mle = np.mean(donnees)      # La moyenne est l'estimateur MLE de μ
sigma_mle = np.std(donnees)    # L'écart-type est l'estimateur MLE de σ

print(f"Estimation MLE : μ = {mu_mle:.3f}, σ = {sigma_mle:.3f}")

# Visualiser
x = np.linspace(0, 4, 200)

plt.figure(figsize=(10, 6))
plt.hist(donnees, bins=8, density=True, alpha=0.7, color='steelblue',
         edgecolor='black', label='Données observées')
plt.plot(x, stats.norm.pdf(x, mu_mle, sigma_mle), 'r-', linewidth=2,
         label=f'MLE : N({mu_mle:.2f}, {sigma_mle:.2f})')
plt.plot(x, stats.norm.pdf(x, 0, 1), 'g--', linewidth=2, alpha=0.5,
         label='N(0, 1) — mauvais fit')
plt.plot(x, stats.norm.pdf(x, 5, 1), 'purple', linewidth=2, alpha=0.5,
         linestyle='--', label='N(5, 1) — mauvais fit')

plt.xlabel("Valeur")
plt.ylabel("Densité")
plt.title("Maximum de vraisemblance : trouver la distribution qui 'explique' le mieux les données")
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```

### 7.3 Lien avec les modèles ML

| Modèle | Ce que le MLE optimise |
|--------|----------------------|
| **Régression linéaire** | Minimiser MSE = maximiser la vraisemblance (si erreurs normales) |
| **Régression logistique** | Maximiser la vraisemblance des classes observées |
| **Naive Bayes** | Estimer P(feature \| classe) directement par comptage |
| **Réseaux de neurones** | Minimiser la cross-entropy ≈ maximiser la vraisemblance |

> 💡 **Conseil** : "Quand vous minimisez la MSE en régression, vous faites en réalité du maximum de vraisemblance en supposant que les erreurs suivent une distribution normale. C'est pour ça que la normalité des résidus est importante !"

### 7.4 Vérifier la normalité des résidus

```python
from sklearn.linear_model import LinearRegression
from sklearn.datasets import fetch_california_housing
from scipy import stats

# Entraîner une régression
housing = fetch_california_housing()
X, y = housing.data, housing.target
model = LinearRegression()
model.fit(X, y)

# Calculer les résidus
residus = y - model.predict(X)

# Visualiser
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].hist(residus, bins=50, density=True, alpha=0.7,
             color='steelblue', edgecolor='black')
x_norm = np.linspace(residus.min(), residus.max(), 200)
axes[0].plot(x_norm, stats.norm.pdf(x_norm, np.mean(residus), np.std(residus)),
             'r-', linewidth=2)
axes[0].set_title("Distribution des résidus")
axes[0].set_xlabel("Résidu")

stats.probplot(residus, dist="norm", plot=axes[1])
axes[1].set_title("Q-Q Plot (normalité)")

plt.tight_layout()
plt.show()

# Test de normalité
stat, p_value = stats.shapiro(residus[:5000])
print(f"Test de Shapiro-Wilk : p-value = {p_value:.6f}")
print(f"→ {'Résidus normaux' if p_value > 0.05 else 'Résidus NON normaux'}")
```

> ⚠️ **Attention** : "Si les résidus ne sont pas normaux, les intervalles de confiance et les tests statistiques ne sont plus fiables. Dans ce cas, envisagez des transformations (log, Box-Cox) ou des modèles non-paramétriques."

---

## 🎯 Points clés à retenir

1. **Une probabilité** est une fréquence à long terme (0 = impossible, 1 = certain)
2. **La distribution normale** est définie par μ (moyenne) et σ (écart-type), et apparaît partout grâce au théorème central limite
3. **La règle 68-95-99.7** : 68% des données sont à ±1σ, 95% à ±2σ, 99.7% à ±3σ
4. **L'intervalle de confiance** quantifie l'incertitude : plus de données = intervalle plus étroit
5. **La régression logistique** prédit des probabilités (pas juste des classes) grâce à la fonction sigmoïde
6. **Les probabilités sont plus utiles** qu'une simple prédiction binaire pour prendre des décisions métier
7. **Le théorème de Bayes** permet de mettre à jour une croyance à partir d'une nouvelle observation
8. **Le classifieur Naive Bayes** applique Bayes en supposant l'indépendance des features — simple et efficace
9. **Le maximum de vraisemblance** cherche les paramètres qui rendent les données observées les plus probables
10. **Minimiser la MSE** en régression = maximiser la vraisemblance sous hypothèse de normalité des erreurs

---

## ✅ Checklist de validation

- [ ] Je sais expliquer ce que signifie "70% de chances qu'il pleuve"
- [ ] Je connais la différence intuitive entre fréquentiste et bayésien
- [ ] Je sais ce qu'est une distribution normale et ses deux paramètres (μ, σ)
- [ ] Je connais la règle 68-95-99.7 et je sais l'utiliser pour détecter des anomalies
- [ ] Je sais distinguer les distributions normale, uniforme, binomiale et Poisson
- [ ] Je comprends ce qu'est un intervalle de confiance et pourquoi il rétrécit avec plus de données
- [ ] Je sais utiliser la régression logistique avec scikit-learn
- [ ] Je comprends la fonction sigmoïde et son rôle dans la régression logistique
- [ ] Je sais appliquer le théorème de Bayes sur un exemple simple (spam)
- [ ] Je comprends l'intuition du maximum de vraisemblance
- [ ] Je sais utiliser `predict_proba()` pour obtenir des probabilités et non juste des classes
- [ ] Je comprends pourquoi les probabilités sont plus utiles qu'une prédiction binaire

---

**Précédent** : [Chapitre 4 : Fonctions, Erreurs et l'Art de s'Améliorer](04-fonctions-erreurs-gradient.md)

**Suivant** : [Chapitre 6 : Méthodes d'Ensemble](06-ensemble-methods.md)
