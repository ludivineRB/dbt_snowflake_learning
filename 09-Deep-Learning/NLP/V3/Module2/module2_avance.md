---
title: Module 2 - Techniques Avancées de Preprocessing
description: Formation NLP - Module 2 - Techniques Avancées de Preprocessing
tags:
  - NLP
  - 09-Deep-Learning
category: 09-Deep-Learning
---

# ⚙️Techniques Avancées de Preprocessing

Stopwords, Lemmatisation, Stemming et Normalisation Avancée

## 🎯Techniques Avancées

Maintenant que vous maîtrisez le nettoyage et la tokenisation, découvrons les techniques avancées pour optimiser vos données textuelles !

🛑 Stopwords

Mots très fréquents mais peu informatifs ("le", "de", "et")

**Quand :** Classification, recherche

🌱 Lemmatisation

Réduction à la forme canonique ("mangeaient" → "manger")

**Quand :** Analyse sémantique précise

✂️ Stemming

Suppression des suffixes ("mangeons" → "mang")

**Quand :** Recherche rapide, peu précise

🏷️ Entités Nommées

Préservation des noms propres, dates, montants

**Quand :** Extraction d'informations

## 🛑Gestion des Stopwords

Concept Français Démo Personnalisés

### Qu'est-ce que les Stopwords ?

**Définition :** Mots très fréquents dans une langue mais qui apportent peu d'information sémantique.

#### Exemples en français :

**Articles :** le, la, les, un, une, des  
**Prépositions :** de, du, à, avec, pour, dans  
**Pronoms :** je, tu, il, elle, nous, vous  
**Conjonctions :** et, ou, mais, donc, car  
**Auxiliaires :** être, avoir, faire

#### Quand supprimer les stopwords ?

*   ✅ **Classification de documents** (topic, sentiment)
*   ✅ **Recherche d'information** (moteur de recherche)
*   ✅ **Clustering de texte**
*   ❌ **Traduction automatique** (structure grammaticale importante)
*   ❌ **Analyse syntaxique** (relations grammaticales)
*   ❌ **Génération de texte** (fluidité nécessaire)

### Spécificités du Français

Le français a des particularités que n'ont pas l'anglais :

Caractéristique

Français

Anglais

Impact

**Contractions**

du, des, au, aux

don't, won't, I'm

Plus de variations

**Genre/Nombre**

le/la/les, un/une/des

the, a/an

Liste plus longue

**Conjugaisons**

suis, es, est, sommes...

am, is, are

Variabilité élevée

**Accents**

à, où, déjà

Rares

Normalisation nécessaire

📓 stopwords\_francais.ipynb

Notebook pour gérer les stopwords français avec NLTK et spaCy

[📓 Ouvrir le Notebook](notebook/stopwords_francais.ipynb)

### Démo Interactive : Impact des Stopwords

**Entrez un texte français :** Le chat noir mange des croquettes avec grand appétit dans le jardin ensoleillé. 🧹 Analyser l'impact des stopwords

Cliquez sur "Analyser" pour voir l'impact de la suppression des stopwords...

### Stopwords Personnalisés

Selon votre domaine, vous pouvez avoir besoin de stopwords spécifiques :

#### 🏥 Médical

**Ajouter :** patient, traitement, médecin, diagnostic

#### 💼 Business

**Ajouter :** entreprise, société, business, client

#### 🎥 Cinéma

**Ajouter :** film, acteur, réalisateur, cinéma

#### 💻 Tech

**Supprimer :** python, java, code (importants !)

📓 stopwords\_custom.ipynb

Notebook pour créer et gérer des listes de stopwords personnalisées

[📓 Ouvrir le Notebook](notebook/stopwords_custom.ipynb)

## 🌱Lemmatisation vs Stemming

Concepts Comparaison Démo Français

### Stemming vs Lemmatisation

#### ✂️ Stemming

**Principe :** Suppression mécanique des suffixes

**Exemple :**

*   "mangent" → "mang"
*   "mangeait" → "mange"
*   "mangeur" → "mang"

**Avantages :** Rapide, simple

**Inconvénients :** Résultats parfois incorrects

#### 🌱 Lemmatisation

**Principe :** Réduction à la forme canonique via dictionnaire

**Exemple :**

*   "mangent" → "manger"
*   "mangeait" → "manger"
*   "mangeur" → "mangeur"

**Avantages :** Précis, mots valides

**Inconvénients :** Plus lent, complexe

### Tableau Comparatif Détaillé

Critère

Stemming

Lemmatisation

Recommandation

**Vitesse**

⚡ Très rapide

🐌 Plus lent

Stemming si performance critique

**Précision**

❌ Approximative

✅ Élevée

Lemmatisation si qualité importante

**Lisibilité**

❌ Mots tronqués

✅ Mots valides

Lemmatisation pour interface utilisateur

**Taille vocabulaire**

📉 Réduit beaucoup

📊 Réduit modérément

Stemming pour compression maximale

**Gestion erreurs**

❌ Propagation d'erreurs

✅ Robuste

Lemmatisation pour données bruitées

**Domaine spécialisé**

❌ Difficile à adapter

✅ Dictionnaires spécialisés

Lemmatisation pour médical, juridique...

#### 💡 Conseils de Choix

**Utilisez le Stemming quand :**

*   Vous traitez de gros volumes (millions de documents)
*   La précision n'est pas critique (recherche approximative)
*   Vous voulez maximiser la réduction du vocabulaire

**Utilisez la Lemmatisation quand :**

*   Vous analysez le sens (sentiment, thématiques)
*   Vous voulez des résultats lisibles par l'utilisateur
*   Vous travaillez dans un domaine spécialisé

### Comparaison Interactive

**Entrez des mots français conjugués :** mangeons, mangeait, mangeur, courions, courait, coureur, finissons, finissait, finisseur ⚔️ Comparer Stemming vs Lemmatisation

Entrez des mots et cliquez sur "Comparer" pour voir la différence...

### Défis du Français

Le français présente des défis particuliers pour la lemmatisation :

#### 🔄 Verbes Irréguliers

**Exemple :** "vais", "va", "irai" → "aller"

Nécessite un dictionnaire complet

#### 👥 Homonymie

**Exemple :** "fils" → "fil" (objet) OU "fils" (enfant)

Dépend du contexte

#### 📝 Accord

**Exemple :** "mangées" → "manger" (pas "mangée")

Analyser la nature grammaticale

📓 lemmatisation\_francais.ipynb

Notebook complet sur la lemmatisation française avec spaCy et comparaison avec stemming

[📓 Ouvrir le Notebook](notebook/lemmatisation_francais.ipynb)

## 🔧Normalisation Avancée

### Types de Normalisation

📅 Dates

"3 mars 2024", "03/03/2024" → "2024-03-03"

💰 Montants

"1.500,50€", "1500.5 euros" → "MONTANT"

📧 Emails

"contact@exemple.fr" → "EMAIL"

🌐 URLs

"https://www.exemple.com" → "URL"

📱 Téléphones

"01 23 45 67 89", "+33123456789" → "TELEPHONE"

🔢 Nombres

"mille", "1000", "1 000" → "NOMBRE"

### Démo : Normalisation Complète

**Entrez un texte avec des entités à normaliser :** Rendez-vous le 15 mars 2024 à 14h30. Contactez-moi au 01.23.45.67.89 ou jean.dupont@email.fr. Le budget est de 1.500,50€. 🔧 Normaliser les entités

Entrez du texte et cliquez sur "Normaliser" pour voir la transformation...

📓 normalisation\_avancee.ipynb

Notebook complet de normalisation des entités en français

[📓 Ouvrir le Notebook](notebook/normalisation_avancee.ipynb)

## 🏗️Pipeline de Preprocessing Complet

### Architecture du Pipeline

**📝 Texte Brut**  
Données d'entrée

→

**🧹 Nettoyage**  
Casse, ponctuation

→

**✂️ Tokenisation**  
Division en mots

→

**🛑 Stopwords**  
Filtrage

→

**🌱 Lemmatisation**  
Forme canonique

→

**✅ Texte Prêt**  
Pour ML

### Configurateur de Pipeline

 🔤 Minuscules  📝 Supprimer ponctuation  🔢 Supprimer nombres  🌐 Nettoyer URLs  🛑 Supprimer stopwords  🌱 Lemmatiser  📏 Longueur min (3 char)  🏷️ Normaliser entités

**Testez votre pipeline personnalisé :** Bonjour ! Je suis très CONTENT de ce COURS sur https://nlp-course.com. Rendez-vous le 15/03/2024 à contact@exemple.fr ! 🔧 Exécuter le pipeline

Configurez les options et testez votre pipeline...

📓 pipeline\_complet.ipynb

Notebook avec classe Pipeline configurable intégrant toutes les techniques avancées

[📓 Ouvrir le Notebook](notebook/pipeline_complet.ipynb)

## 💡Bonnes Pratiques et Pièges à Éviter

### ✅ Bonnes Pratiques

*   🎯 **Adapter au domaine :** Stopwords spécifiques au contexte
*   📊 **Mesurer l'impact :** Comparer avant/après preprocessing
*   🔄 **Pipeline reproductible :** Sauvegarder la configuration
*   🧪 **Tester sur échantillon :** Vérifier manuellement
*   ⚡ **Optimiser progressivement :** Ajouter étapes une par une
*   📝 **Documenter les choix :** Justifier chaque étape

### ❌ Pièges à Éviter

*   🚫 **Trop nettoyer :** Perdre de l'information importante
*   ⚠️ **Ordre des étapes :** Lemmatiser avant de supprimer stopwords
*   🎭 **Ignorer le contexte :** Même pipeline pour tous les cas
*   🐌 **Pipeline trop lourd :** Impact sur les performances
*   🔍 **Pas de validation :** Ne pas vérifier les résultats
*   🧠 **Oublier l'humain :** Preprocessing illisible

### Checklist de Validation

#### Avant de finaliser votre preprocessing :

 📊 J'ai mesuré la taille du vocabulaire avant/après  🎯 J'ai testé sur des exemples représentatifs  ⚡ Le temps de traitement est acceptable  👀 Les résultats restent lisibles  🔄 Le pipeline est reproductible  📝 J'ai documenté mes choix  🧪 J'ai validé sur un échantillon test  🎭 J'ai adapté au domaine d'application

[← Tokenisation](module2_tokenisation.html) [Mini-Projet →](module2_projet.html)

// Gestion des onglets function showTab(tabId) { // Cacher tous les contenus const contents = document.querySelectorAll('.tab-content'); contents.forEach(content => content.classList.remove('active')); // Désactiver tous les onglets const tabs = document.querySelectorAll('.tab'); tabs.forEach(tab => tab.classList.remove('active')); // Activer l'onglet et contenu sélectionnés document.getElementById(tabId).classList.add('active'); event.target.classList.add('active'); } // Démonstration des stopwords function demonstrateStopwords() { const input = document.getElementById('stopwords-input').value; const resultDiv = document.getElementById('stopwords-result'); // Simulation - remplacer par appel à stopwords\_francais.py const stopwords = \['le', 'la', 'les', 'un', 'une', 'des', 'de', 'du', 'avec', 'dans', 'grand'\]; const words = input.toLowerCase().split(/\\s+/); const filtered = words.filter(word => !stopwords.includes(word)); const originalCount = words.length; const filteredCount = filtered.length; const reduction = ((originalCount - filteredCount) / originalCount \* 100).toFixed(1); resultDiv.innerHTML = \` <strong>📊 Analyse des stopwords :</strong> 🔸 Texte original (${originalCount} mots) : ${words.join(', ')} 🔸 Après suppression des stopwords (${filteredCount} mots) : ${filtered.join(', ')} 📉 Réduction du vocabulaire : ${reduction}% 🛑 Stopwords supprimés : ${words.filter(word => stopwords.includes(word)).join(', ')} 💡 ${reduction > 30 ? 'Forte réduction ! Bon pour la classification.' : 'Réduction modérée. Normal pour ce type de texte.'}\`; } // Comparaison Lemmatisation vs Stemming function compareLemmaVsStem() { const input = document.getElementById('lemma-input').value; const resultDiv = document.getElementById('lemma-result'); // Simulation - remplacer par appel à lemmatisation\_francais.py const words = input.split(/\[,\\s\]+/).filter(w => w.trim()); const stemResults = words.map(word => { // Simulation de stemming simple return word.replace(/ons$|ait$|eur$|ons$|ez$|ent$/, ''); }); const lemmaResults = words.map(word => { // Simulation de lemmatisation const lemmaDict = { 'mangeons': 'manger', 'mangeait': 'manger', 'mangeur': 'mangeur', 'courions': 'courir', 'courait': 'courir', 'coureur': 'coureur', 'finissons': 'finir', 'finissait': 'finir', 'finisseur': 'finisseur' }; return lemmaDict\[word.toLowerCase()\] || word; }); resultDiv.innerHTML = \` <strong>⚔️ Comparaison Stemming vs Lemmatisation :</strong> 📝 Mots originaux : ${words.join(', ')} ✂️ Stemming : ${stemResults.join(', ')} 🌱 Lemmatisation : ${lemmaResults.join(', ')} 🎯 Observations : • Stemming : ${stemResults.some(w => w.length < 4) ? 'Certains mots sont trop courts' : 'Longueurs correctes'} • Lemmatisation : ${lemmaResults.every(w => w.endsWith('er') || w.endsWith('ir') || w.endsWith('eur')) ? 'Formes valides du français' : 'Résultats mixtes'} 💡 Pour ce cas : ${lemmaResults.join(' ').length > stemResults.join(' ').length ? 'La lemmatisation préserve mieux le sens' : 'Le stemming est plus compact'}\`; } // Normalisation avancée function normalizeAdvanced() { const input = document.getElementById('normalize-input').value; const resultDiv = document.getElementById('normalize-result'); // Simulation - remplacer par appel à normalisation\_avancee.py let normalized = input; // Dates normalized = normalized.replace(/\\d{1,2}\\s+(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)\\s+\\d{4}/gi, 'DATE'); normalized = normalized.replace(/\\d{1,2}\\/\\d{1,2}\\/\\d{4}/g, 'DATE'); // Heures normalized = normalized.replace(/\\d{1,2}h\\d{2}/g, 'HEURE'); // Téléphones normalized = normalized.replace(/\\d{2}\[\\.\\s\]\\d{2}\[\\.\\s\]\\d{2}\[\\.\\s\]\\d{2}\[\\.\\s\]\\d{2}/g, 'TELEPHONE'); // Emails normalized = normalized.replace(/\[a-zA-Z0-9.\_%+-\]+@\[a-zA-Z0-9.-\]+\\.\[a-zA-Z\]{2,}/g, 'EMAIL'); // Montants normalized = normalized.replace(/\\d{1,3}(?:\[.\\s\]\\d{3})\*,\\d{2}€?/g, 'MONTANT'); resultDiv.innerHTML = \` <strong>🔧 Normalisation des entités :</strong> 🔸 Texte original : ${input} 🔸 Texte normalisé : ${normalized} 🏷️ Entités détectées : ${input.match(/\\d{1,2}\\s+mars\\s+\\d{4}/) ? '• DATE : "15 mars 2024"' : ''} ${input.match(/\\d{1,2}h\\d{2}/) ? '• HEURE : "14h30"' : ''} ${input.match(/\\d{2}\[\\.\\s\]\\d{2}/) ? '• TELEPHONE : "01.23.45.67.89"' : ''} ${input.match(/@/) ? '• EMAIL : "jean.dupont@email.fr"' : ''} ${input.match(/\\d.\*€/) ? '• MONTANT : "1.500,50€"' : ''} 💡 Avantages : Vocabulaire réduit, focus sur le contenu textuel, anonymisation partielle\`; } // Pipeline personnalisé function runCustomPipeline() { const input = document.getElementById('pipeline-input').value; const resultDiv = document.getElementById('pipeline-result'); let processed = input; const steps = \[\]; // Minuscules if (document.getElementById('clean-case').checked) { processed = processed.toLowerCase(); steps.push('🔤 Conversion en minuscules'); } // Ponctuation if (document.getElementById('clean-punct').checked) { processed = processed.replace(/\[^\\w\\s\]/g, ' '); steps.push('📝 Suppression de la ponctuation'); } // URLs if (document.getElementById('clean-urls').checked) { processed = processed.replace(/https?:\\/\\/\[^\\s\]+/g, ''); steps.push('🌐 Suppression des URLs'); } // Nombres if (document.getElementById('clean-numbers').checked) { processed = processed.replace(/\\d+/g, ''); steps.push('🔢 Suppression des nombres'); } // Normalisation des espaces processed = processed.replace(/\\s+/g, ' ').trim(); // Tokenisation let tokens = processed.split(' ').filter(t => t.length > 0); // Longueur minimale if (document.getElementById('min-length').checked) { tokens = tokens.filter(t => t.length >= 3); steps.push('📏 Filtrage longueur minimale (3 caractères)'); } // Stopwords if (document.getElementById('remove-stopwords').checked) { const stopwords = \['le', 'la', 'les', 'un', 'une', 'des', 'de', 'du', 'je', 'tu', 'il', 'elle', 'nous', 'vous', 'ils', 'elles', 'ce', 'cette', 'ces', 'et', 'ou', 'mais', 'donc', 'car', 'sur', 'avec', 'dans', 'pour', 'par', 'à', 'très'\]; tokens = tokens.filter(t => !stopwords.includes(t)); steps.push('🛑 Suppression des stopwords'); } // Lemmatisation (simulation) if (document.getElementById('lemmatize').checked) { // Simulation simple tokens = tokens.map(token => { if (token.endsWith('ent')) return token.slice(0, -3) + 'er'; if (token.endsWith('ait')) return token.slice(0, -3) + 'er'; return token; }); steps.push('🌱 Lemmatisation'); } // Entités if (document.getElementById('normalize-entities').checked) { tokens = tokens.map(token => { if (token.includes('@')) return 'EMAIL'; if (/\\d{2}\\/\\d{2}\\/\\d{4}/.test(token)) return 'DATE'; return token; }); steps.push('🏷️ Normalisation des entités'); } resultDiv.innerHTML = \` <strong>🔧 Résultats du pipeline personnalisé :</strong> 📝 Texte original (${input.split(' ').length} mots) : ${input} ✅ Texte traité (${tokens.length} tokens) : ${tokens.join(', ')} 🛠️ Étapes appliquées : ${steps.map(step => \`• ${step}\`).join('\\n')} 📊 Statistiques : • Réduction du vocabulaire : ${((input.split(' ').length - tokens.length) / input.split(' ').length \* 100).toFixed(1)}% • Tokens finaux : ${tokens.length} • Caractères économisés : ${input.length - tokens.join(' ').length} 💡 ${tokens.length < 5 ? 'Attention : vocabulaire très réduit, vérifiez les paramètres' : 'Pipeline équilibré pour l\\'analyse'}\`; }
