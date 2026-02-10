[← Precedent](06-documentation-communication.md) | [🏠 Accueil](README.md) | [Suivant →](08-exercices.md)

# Lecon 7 - Accessibilite et Eco-conception

## 🎯 Objectifs

- Comprendre les obligations legales en matiere d'accessibilite numerique (RGAA, WCAG)
- Appliquer les principes d'accessibilite aux produits data (dashboards, rapports, applications)
- Maitriser les principes d'eco-conception et de Green IT pour les projets data
- Calculer et optimiser l'empreinte carbone des traitements de donnees
- Utiliser les outils de mesure et d'amelioration (WAVE, Lighthouse, CodeCarbon)

---

## 1. Accessibilite Numerique

### 1.1 Pourquoi l'accessibilite ?

L'accessibilite numerique consiste a rendre les contenus et services numeriques **utilisables par tous**, y compris les personnes en situation de handicap.

**Quelques chiffres** :
- 12 millions de personnes en situation de handicap en France (environ 18% de la population)
- 80% des handicaps sont invisibles
- L'accessibilite beneficie a tout le monde (principe du "curb cut effect")

### 1.2 Le cadre legal : RGAA

#### Qu'est-ce que le RGAA ?

Le **Referentiel General d'Amelioration de l'Accessibilite** (RGAA) est le referentiel francais d'accessibilite numerique. Il est **obligatoire** pour :

| Organisation | Obligation |
|-------------|-----------|
| Services publics de l'Etat | RGAA obligatoire |
| Collectivites territoriales | RGAA obligatoire |
| Entreprises avec CA > 250M EUR | RGAA obligatoire depuis 2020 |
| Toute entreprise | Recommande (et souvent exige par les clients grands comptes) |

**Sanctions** : Amende de 20 000 EUR par an et par service non conforme.

#### Le RGAA en pratique

Le RGAA est base sur les **WCAG** (Web Content Accessibility Guidelines) du W3C et definit 106 criteres repartis en 13 thematiques :

| # | Thematique | Exemples de criteres |
|---|-----------|---------------------|
| 1 | Images | Alternative textuelle pour chaque image |
| 2 | Cadres | Titre pour chaque cadre (iframe) |
| 3 | Couleurs | Ne pas transmettre l'information uniquement par la couleur |
| 4 | Multimedia | Sous-titres pour les videos, transcription pour les audios |
| 5 | Tableaux | En-tetes de colonnes et lignes definis |
| 6 | Liens | Intitule de lien explicite |
| 7 | Scripts | Accessibilite des composants interactifs JavaScript |
| 8 | Elements obligatoires | Langue de la page, titre de page |
| 9 | Structuration | Hierarchie des titres, listes, zones de navigation |
| 10 | Presentation | Contenu lisible sans CSS, redimensionnement |
| 11 | Formulaires | Labels associes aux champs, messages d'erreur |
| 12 | Navigation | Navigation au clavier, fil d'Ariane, plan du site |
| 13 | Consultation | Controle des contenus en mouvement, limites de temps |

### 1.3 WCAG 2.1 - Les 3 niveaux

Les **WCAG 2.1** definissent 3 niveaux de conformite :

| Niveau | Description | Objectif |
|:------:|------------|---------|
| **A** | Niveau minimal. Sans ces criteres, le contenu est inutilisable pour certains utilisateurs. | **Obligatoire** pour tout produit |
| **AA** | Niveau intermediaire. Couvre la majorite des situations de handicap. | **Cible recommandee** (et exigee par le RGAA) |
| **AAA** | Niveau maximal. Accessibilite optimale pour le plus grand nombre. | Ideal mais rarement atteint a 100% |

Les WCAG s'articulent autour de 4 principes fondamentaux (**POUR**) :

| Principe | Signification | Exemple data |
|----------|--------------|-------------|
| **P**erceptible | L'information doit etre presentable de differentes manieres | Un graphique doit avoir une alternative textuelle ou un tableau de donnees |
| **O**perable (Utilisable) | L'interface doit etre navigable au clavier et avec des technologies d'assistance | Les filtres du dashboard doivent etre utilisables au clavier |
| **U**nderstandable (Comprehensible) | L'information et l'interface doivent etre comprehensibles | Les labels des axes d'un graphique doivent etre explicites |
| **R**obuste | Le contenu doit fonctionner avec les technologies d'assistance actuelles et futures | Le dashboard doit fonctionner avec les lecteurs d'ecran (NVDA, JAWS, VoiceOver) |

### 1.4 Impact sur les produits data

Les produits data (dashboards, rapports, applications de donnees) presentent des defis specifiques en matiere d'accessibilite :

#### Dashboards et rapports

| Probleme courant | Impact | Solution |
|-----------------|--------|---------|
| Graphiques sans alternative textuelle | Les utilisateurs de lecteurs d'ecran ne peuvent pas acceder aux donnees | Ajouter un tableau de donnees en alternative a chaque graphique |
| Couleurs seules pour distinguer les series | Les daltoniens ne peuvent pas distinguer les series | Utiliser des motifs, des formes ou des labels en plus de la couleur |
| Contraste insuffisant | Difficulte de lecture pour les malvoyants | Ratio de contraste >= 4.5:1 (texte) et >= 3:1 (grands textes) |
| Filtres interactifs inaccessibles au clavier | Les utilisateurs ne pouvant pas utiliser une souris sont bloques | S'assurer que tous les filtres sont navigables au Tab et activables au Enter |
| Tooltips uniquement au survol souris | Les utilisateurs clavier/tactile n'y ont pas acces | Rendre les tooltips accessibles au focus clavier |
| Tableaux sans en-tetes | Les lecteurs d'ecran ne peuvent pas interpreter la structure | Utiliser les balises `<th>` avec `scope` |

#### Applications data (Streamlit, Dash, Gradio)

| Framework | Niveau d'accessibilite natif | Points d'attention |
|-----------|:---------------------------:|-------------------|
| **Streamlit** | Moyen | Les widgets natifs sont globalement accessibles. Attention aux composants custom. |
| **Dash (Plotly)** | Bon | Plotly genere du SVG accessible. Ajouter des `aria-label` sur les composants custom. |
| **Gradio** | Moyen | Bonne accessibilite de base. Verifier les composants de saisie. |
| **Power BI** | Bon | Support natif de l'accessibilite. Utiliser les alt-text sur les visuels. |
| **Tableau** | Bon | Support natif. Verifier les dashboards publies. |

### 1.5 Checklist pratique d'accessibilite pour les produits data

#### Contraste et couleurs
- [ ] Ratio de contraste texte/fond >= 4.5:1 (texte normal) et >= 3:1 (grand texte)
- [ ] L'information n'est jamais transmise uniquement par la couleur
- [ ] Les graphiques utilisent des motifs ou des labels en plus des couleurs
- [ ] Les palettes de couleurs sont testees pour le daltonisme

#### Navigation clavier
- [ ] Tous les elements interactifs (filtres, boutons, onglets) sont accessibles au clavier (Tab)
- [ ] L'ordre de tabulation est logique
- [ ] Le focus est visible (outline visible sur l'element actif)
- [ ] Les menus deroulants s'ouvrent et se ferment avec Enter/Escape

#### Lecteur d'ecran
- [ ] Chaque graphique a une alternative textuelle (tableau de donnees ou description)
- [ ] Les images decoratives ont un `alt=""` (alt vide)
- [ ] Les tableaux ont des en-tetes (`<th>`) correctement associes
- [ ] Les formulaires ont des labels explicites (`<label for="...">`)

#### Structure et comprehension
- [ ] La hierarchie des titres est logique (h1 > h2 > h3, sans saut de niveau)
- [ ] La langue de la page est definie (`lang="fr"`)
- [ ] Les abreviations sont explicitees au premier usage
- [ ] Les messages d'erreur sont clairs et associes au champ concerne

### 1.6 Outils de test d'accessibilite

| Outil | Type | Gratuit | Usage |
|-------|------|:-------:|-------|
| **WAVE** | Extension navigateur | Oui | Analyse rapide d'une page web |
| **axe DevTools** | Extension navigateur | Oui (base) | Audit detaille, integration CI |
| **Lighthouse** | Integre a Chrome DevTools | Oui | Score d'accessibilite global |
| **NVDA** | Lecteur d'ecran (Windows) | Oui | Tester l'experience lecteur d'ecran |
| **VoiceOver** | Lecteur d'ecran (macOS/iOS) | Oui (integre) | Tester l'experience lecteur d'ecran |
| **Contrast Checker** | Web | Oui | Verifier les ratios de contraste |
| **Colour Blindness Simulator** | Extension | Oui | Simuler le daltonisme |
| **Pa11y** | CLI / CI | Oui | Tests automatises dans la CI/CD |

---

## 2. Eco-conception / Green IT

### 2.1 Pourquoi ca compte

**Le numerique, c'est concret** :
- Les data centers representent **1 a 2%** de la consommation electrique mondiale
- L'entrainement d'un modele GPT-3 a genere environ **552 tonnes de CO2** (equivalent a 120 voitures pendant 1 an)
- Un email avec une piece jointe de 1 Mo genere environ **19 g de CO2**
- Une requete Google genere environ **0.2 g de CO2**
- Le stockage de 1 To de donnees pendant 1 an genere environ **2 kg de CO2**

**Pour les projets data specifiquement** :
- Un pipeline ETL qui tourne inutilement consomme de l'electricite et du compute
- Un modele ML sur-entraine ou mal optimise gaspille des ressources GPU
- Des donnees stockees "au cas ou" mais jamais utilisees occupent du stockage inutilement
- Des requetes non optimisees consomment 10 a 100 fois plus de ressources que necessaire

### 2.2 Calculer l'empreinte carbone des traitements data

#### Facteurs d'emission par type de ressource

| Ressource | Emission estimee | Source |
|-----------|:---------------:|--------|
| 1 heure de compute (CPU moyen, cloud) | ~20-40 g CO2 | Cloud Carbon Footprint |
| 1 heure de GPU (V100/A100) | ~100-200 g CO2 | CodeCarbon |
| 1 To de stockage / an (SSD cloud) | ~2-5 kg CO2 | Cloud Carbon Footprint |
| 1 To de stockage / an (HDD cloud) | ~1-2 kg CO2 | Cloud Carbon Footprint |
| 1 requete BigQuery (1 To scanne) | ~5-10 g CO2 | Google estimation |
| 1 entrainement de modele BERT | ~30 kg CO2 | Strubell et al., 2019 |
| 1 entrainement de modele GPT-3 | ~552 tonnes CO2 | Patterson et al., 2021 |

#### Impact de la region cloud

| Region cloud | Facteur carbone (g CO2/kWh) | Classification |
|-------------|:---------------------------:|:--------------:|
| France (AWS eu-west-3) | ~55 | ✅ Tres bon (nucleaire) |
| Suede (AWS eu-north-1) | ~10 | ✅ Excellent (hydro/eolien) |
| Allemagne (AWS eu-central-1) | ~350 | ❌ Mauvais (charbon/gaz) |
| USA Est (AWS us-east-1) | ~380 | ❌ Mauvais |
| USA Ouest (AWS us-west-2) | ~120 | 🟡 Moyen |

💡 **Astuce** : A performance egale, **choisir une region cloud "verte"** peut reduire l'empreinte carbone de 80%. La France et les pays nordiques sont les meilleurs choix en Europe grace au nucleaire et a l'hydraulique.

### 2.3 Strategies d'optimisation

#### Strategie 1 : Reduire le volume de donnees

| Pratique | Economie estimee | Difficulte |
|----------|:---------------:|:----------:|
| Filtrer tot (pushdown predicates) | 50-90% de compute | Faible |
| Echantillonner pour l'exploration | 90-99% de compute | Faible |
| Compresser les donnees (Parquet vs CSV) | 70-90% de stockage | Faible |
| Supprimer les colonnes inutiles (pas de `SELECT *`) | 30-80% de compute | Faible |
| Partitionner les tables | 50-90% de scan | Moyenne |
| Archiver les donnees anciennes | 50-80% de stockage | Moyenne |

#### Strategie 2 : Optimiser les requetes

```
❌ REQUETE NON OPTIMISEE (scan complet)
=======================================
SELECT *
FROM sales
WHERE YEAR(sale_date) = 2025

Donnees scannees : 500 Go (toute la table)
Cout : ~2.50 EUR (BigQuery)
CO2 : ~5 g
```

```
✅ REQUETE OPTIMISEE (partition + colonnes)
============================================
SELECT sale_id, sale_date, amount
FROM sales
WHERE sale_date BETWEEN '2025-01-01' AND '2025-12-31'

Donnees scannees : 50 Go (partition 2025, 3 colonnes)
Cout : ~0.25 EUR (BigQuery)
CO2 : ~0.5 g

Economie : 90% de compute, 90% de cout, 90% de CO2
```

#### Strategie 3 : Right-sizing de l'infrastructure

| Pratique | Description | Economie |
|----------|------------|---------|
| **Auto-scaling** | Adapter automatiquement la capacite a la charge | 30-60% |
| **Spot/Preemptible instances** | Utiliser des instances interruptibles pour le batch | 60-90% du prix |
| **Auto-suspend** | Eteindre les warehouses Snowflake quand inactifs | 40-70% |
| **Serverless** | Cloud Functions / Lambda pour les taches ponctuelles | Variable, souvent 50%+ |
| **Right-size des VMs** | Ne pas prendre un t3.xlarge quand un t3.small suffit | 50-75% |

#### Strategie 4 : Politiques de retention des donnees

| Type de donnee | Retention recommandee | Action |
|---------------|:--------------------:|--------|
| Donnees brutes (raw/bronze) | 1-2 ans | Archiver vers cold storage, puis supprimer |
| Donnees nettoyees (silver) | 3-5 ans | Compresser et archiver |
| Donnees metier (gold) | 5-7 ans | Conserver (volume reduit) |
| Logs applicatifs | 3-6 mois | Supprimer regulierement |
| Donnees de test/dev | 1 mois | Supprimer automatiquement |
| Backups | 30 jours (recents) + 1/mois (archive) | Rotation automatique |

💡 **Astuce** : Mettez en place un **data lifecycle management** automatise. Exemple avec AWS S3 :
- 0-30 jours : S3 Standard
- 30-90 jours : S3 Infrequent Access (-40% cout)
- 90-365 jours : S3 Glacier (-80% cout)
- > 365 jours : Suppression automatique (sauf obligation legale)

#### Strategie 5 : Green coding pour le ML

| Pratique | Description | Impact |
|----------|------------|--------|
| **Transfer learning** | Reutiliser un modele pre-entraine plutot que d'entrainer from scratch | Division par 10-100 du cout d'entrainement |
| **Early stopping** | Arreter l'entrainement quand le modele n'apprend plus | 20-50% d'economie |
| **Hyperparameter search intelligent** | Bayesian optimization plutot que grid search | 50-80% d'economie |
| **Distillation de modeles** | Creer un petit modele a partir d'un gros (teacher -> student) | 90%+ d'economie en inference |
| **Quantization** | Reduire la precision des poids (float32 -> int8) | 50-75% d'economie en inference |
| **Batch inference** | Predire en batch plutot qu'en temps reel quand possible | 30-60% d'economie |

### 2.4 Outils de mesure

| Outil | Usage | Integration |
|-------|-------|------------|
| **Cloud Carbon Footprint** | Mesure l'empreinte carbone de votre usage cloud (AWS, GCP, Azure) | Dashboard web, API |
| **CodeCarbon** | Bibliotheque Python qui mesure le CO2 de votre code ML | `pip install codecarbon`, decorateur Python |
| **Green Algorithms** | Calculateur en ligne pour estimer le CO2 d'un calcul | Web |
| **Electricity Maps** | Carte en temps reel de l'intensite carbone par region | API |
| **AWS Customer Carbon Footprint Tool** | Rapport mensuel de l'empreinte carbone AWS | Console AWS |
| **Google Carbon Footprint** | Rapport de l'empreinte carbone GCP | Console GCP |

#### Exemple d'utilisation de CodeCarbon

```python
from codecarbon import EmissionsTracker

# Mesurer l'empreinte carbone de l'entrainement d'un modele
tracker = EmissionsTracker(
    project_name="churn_prediction_model",
    output_dir="./emissions",
    country_iso_code="FRA"  # France (nucleaire = faible emission)
)

tracker.start()

# --- Votre code d'entrainement ML ici ---
model.fit(X_train, y_train)
# -----------------------------------------

emissions = tracker.stop()

print(f"Emissions : {emissions:.4f} kg CO2")
print(f"Equivalent : {emissions * 1000 / 19:.1f} emails avec piece jointe")
```

### 2.5 Tableau comparatif : pratiques eco-responsables vs gaspillage

| Dimension | ❌ Pratique gaspilleuse | ✅ Pratique eco-responsable | Economie |
|-----------|----------------------|---------------------------|:--------:|
| **Requetes** | `SELECT * FROM table` sans filtre | `SELECT col1, col2 WHERE date > '2025-01-01'` | 80-95% |
| **Stockage** | Tout garder indefiniment en hot storage | Lifecycle management (hot -> warm -> cold -> delete) | 50-80% |
| **Compute** | VM allumee 24/7 pour un batch quotidien de 2h | Auto-scaling ou serverless | 60-90% |
| **ML Training** | Grid search exhaustif sur toutes les combinaisons | Bayesian optimization + early stopping | 50-80% |
| **ML Inference** | GPU 24/7 pour 100 predictions/jour | Batch inference quotidien sur CPU | 90%+ |
| **Format** | CSV non compresse | Parquet compresse | 70-90% stockage |
| **Region cloud** | US-East-1 (charbon) par defaut | EU-West-3 (France, nucleaire) | 80% CO2 |
| **Donnees dev/test** | Copie complete de la production | Echantillon de 1% des donnees | 99% |
| **Monitoring** | Pas de monitoring des couts/consommation | Dashboard de suivi couts + CO2 | Prise de conscience |

### 2.6 Integrer l'eco-conception dans le cycle de projet

| Phase | Actions eco-conception |
|-------|----------------------|
| **Cadrage** | Definir des objectifs de sobriete numerique. Inclure un indicateur CO2 dans les KPIs. |
| **Exploration** | Estimer l'empreinte carbone du POC. Comparer les options (batch vs streaming). |
| **Developpement** | Optimiser les requetes, compresser les donnees, right-sizer l'infra. Mesurer avec CodeCarbon. |
| **Deploiement** | Choisir une region cloud verte. Configurer l'auto-scaling et l'auto-suspend. |
| **Maintenance** | Monitorer la consommation. Mettre en place les politiques de retention. Revue trimestrielle. |
| **Evolution** | Challenger chaque nouvelle fonctionnalite : "Est-ce que le benefice justifie le cout environnemental ?" |

---

## 3. Synthese

| Concept | Point cle |
|---------|-----------|
| RGAA | Referentiel francais d'accessibilite, obligatoire pour les services publics et grandes entreprises |
| WCAG 2.1 | 4 principes (POUR) et 3 niveaux (A, AA, AAA). Viser le niveau AA. |
| Accessibilite data | Alternatives textuelles aux graphiques, navigation clavier, contraste suffisant |
| Eco-conception | Reduire les donnees, optimiser les requetes, right-sizer l'infra, choisir des regions vertes |
| CodeCarbon | Mesurer l'empreinte carbone de vos traitements ML en Python |
| Retention des donnees | Ne pas tout garder indefiniment, lifecycle management automatise |

### Les 3 regles d'or

1. **L'accessibilite n'est pas optionnelle** - C'est une obligation legale et un enjeu d'inclusion
2. **Mesurer avant d'optimiser** - Utilisez les outils (CodeCarbon, Cloud Carbon Footprint) pour identifier les gisements d'economies
3. **Sobriete numerique = valeur metier** - Moins de donnees inutiles = moins de couts, plus de performance, moins de CO2

---

📝 **Exercice** : Pour un dashboard Power BI existant dans votre contexte, realisez un audit d'accessibilite en utilisant Lighthouse et WAVE. Identifiez 5 problemes et proposez des corrections. Ensuite, estimez l'empreinte carbone du pipeline qui alimente ce dashboard et proposez 3 optimisations eco-responsables.

---

[← Precedent](06-documentation-communication.md) | [🏠 Accueil](README.md) | [Suivant →](08-exercices.md)

---

**Academy** - Formation Data Engineer
