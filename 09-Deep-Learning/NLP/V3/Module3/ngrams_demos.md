---
title: Module 3 - N-grams Démonstrations
description: Formation NLP - Module 3 - N-grams Démonstrations
tags:
  - NLP
  - 09-Deep-Learning
category: 09-Deep-Learning
---

# 🔗 N-grams - Démonstrations Interactives

Explorez la génération et les applications des séquences de mots

[← Concepts N-grams](module3_ngrams_concepts.html) [Classification →](classification_final.html) [🏠 Index Module 3](index.html)

## 🧪 Générateur de N-grams Interactif

🎯 Génération Basique ⚙️ Options Avancées 📊 Comparaison Tailles

### ✍️ Entrez votre texte :

New York est une ville fantastique avec beaucoup d'attractions touristiques intéressantes

Taille N-gram : Unigrammes (1) Bigrammes (2) Trigrammes (3) Quadrigrammes (4) 5-grammes

 Supprimer mots vides

🔗 Générer N-grams

N-grams apparaîtront ici...

0

N-grams Totaux

0

N-grams Uniques

0%

Ratio Unique

0

Long. Moyenne

### ⚙️ Configuration Avancée :

Le machine learning et l'intelligence artificielle transforment notre société moderne. Ces technologies révolutionnaires permettent d'automatiser de nombreuses tâches complexes. Les algorithmes d'apprentissage automatique analysent des quantités massives de données pour extraire des insights précieux.

Plage N-grams :

 à 

Fréquence minimale : 

Max N-grams : 

Séparateur : Underscore (\_) Espace ( ) Tiret (-) Pipe (|)

🔧 Générer avec Options

N-grams avancés apparaîtront ici...

### 📊 Comparaison des Tailles de N-grams

L'intelligence artificielle et le machine learning révolutionnent le traitement automatique du langage naturel. Ces technologies permettent de créer des systèmes intelligents capables de comprendre et générer du texte humain avec une précision remarquable. 📈 Comparer les Tailles

Comparaison apparaîtra ici...

#### 📊 Impact de la Taille N sur le Vocabulaire

0

N=1

0

N=2

0

N=3

0

N=4

## 🔍 Extracteur d'Expressions

### 📄 Texte technique à analyser :

L'intelligence artificielle et le machine learning transforment notre société moderne. Le deep learning, une branche du machine learning, révolutionne la computer vision et le natural language processing. Les réseaux de neurones artificiels imitent le fonctionnement du cerveau humain. La data science exploite les big data pour extraire des insights précieux grâce aux algorithmes de machine learning.

Seuil de fréquence :  2

Types d'expressions : Toutes Tech seulement Business seulement

N-gram max : Bigrammes Trigrammes Quadrigrammes

🔍 Extraire Expressions

Expressions extraites apparaîtront ici...

## 🌍 Détecteur de Langue avec N-grams

### 🧪 Testez la Détection de Langue :

Hello, how are you today? I hope you're having a great day and everything is going well!

Méthode : Trigrammes de caractères Bigrammes de mots Combinée

 Afficher détails

🌍 Détecter la Langue

Langue détectée apparaîtra ici...

#### 🧪 Exemples de Test :

🇫🇷 Français 🇺🇸 Anglais 🇪🇸 Espagnol 🇮🇹 Italien 🇩🇪 Allemand

## 🎯 Classification avec N-grams

### 📊 Comparaison : Mots seuls vs N-grams

Testez l'amélioration apportée par les N-grams en classification :

#### 📚 Documents d'entraînement :

TECH: machine learning intelligence artificielle algorithmes deep learning SPORT: football match équipe victoire championnat coupe monde CUISINE: restaurant chef plat recette cuisine gastronomie française TECH: développement web application mobile programmation software SPORT: tennis tournoi joueur raquette court set match point CUISINE: pâtisserie dessert chocolat four cuisson température

#### 🧪 Document à classer :

Le deep learning et le machine learning révolutionnent l'intelligence artificielle moderne

Méthode : Unigrammes seulement Bigrammes seulement Uni + Bigrammes Jusqu'aux trigrammes

🎯 Classifier

Résultat de classification...

## 📊 Analyse de Performance

### ⚖️ Trade-offs des N-grams

**🚨 Attention à l'explosion combinatoire !**  
• Vocabulaire qui augmente exponentiellement  
• Matrice de plus en plus sparse  
• Risque d'overfitting sur des séquences rares

#### 📈 Analyseur d'Impact Performance

Testez l'impact des N-grams sur la taille du vocabulaire :

L'intelligence artificielle et le machine learning transforment notre monde. Le deep learning permet des avancées révolutionnaires en computer vision. Les réseaux de neurones artificiels imitent le fonctionnement du cerveau. La data science exploite les big data pour extraire des insights. Les algorithmes d'apprentissage automatique s'améliorent constamment.

N maximum :  3

 Estimer mémoire

📊 Analyser Performance

Analyse de performance...

#### 📊 Croissance du Vocabulaire par N

0

N=1

0

N=2

0

N=3

0

N=4

0

N=5

### 💡 Bonnes Pratiques

#### ✅ Recommandations

*   Commencer par uni+bigrammes
*   Filtrer par fréquence minimale
*   Limiter le vocabulaire total
*   Tester sur données de validation
*   Surveiller l'overfitting

#### ❌ À Éviter

*   N-grams > 4 sauf cas spéciaux
*   Garder tous les N-grams rares
*   Ignorer la sparsité
*   Ne pas valider l'amélioration
*   Vocabulaire sans limite

#### 🎯 Cas d'Usage

*   Classification de texte
*   Détection de langue
*   Extraction d'entités
*   Analyse de sentiment
*   Détection de plagiat

#### ⚡ Alternatives Modernes

*   Word embeddings
*   Modèles contextuels
*   Transformers
*   BERT, GPT, etc.
*   Réseaux récurrents

[← Concepts N-grams](module3_ngrams_concepts.html) [Classification →](classification_final.html) [🏠 Index Module 3](index.html)

// Variables globales let currentNgrams = null; let currentStats = null; // Stopwords français const STOPWORDS\_FR = new Set(\[ 'le', 'de', 'et', 'à', 'un', 'il', 'être', 'en', 'avoir', 'que', 'pour', 'dans', 'ce', 'son', 'une', 'sur', 'avec', 'ne', 'se', 'pas', 'tout', 'plus', 'par', 'grand', 'son', 'que', 'ce', 'lui', 'au', 'du', 'des', 'la', 'les', 'est', 'cette', 'ces', 'mais', 'ou', 'si', 'nous', 'vous', 'ils', 'elles', 'aussi', 'très', 'bien', 'comme', 'donc', 'peut', 'fait', 'sans' \]); // Gestion des onglets function openTab(evt, tabName) { var i, tabcontent, tabs; tabcontent = document.getElementsByClassName("tab-content"); for (i = 0; i < tabcontent.length; i++) { tabcontent\[i\].classList.remove("active"); } tabs = document.getElementsByClassName("tab"); for (i = 0; i < tabs.length; i++) { tabs\[i\].classList.remove("active"); } document.getElementById(tabName).classList.add("active"); evt.currentTarget.classList.add("active"); } // Preprocessing du texte function preprocessText(text, removeStopwords = true) { let processed = text.toLowerCase(); processed = processed.replace(/\[^\\w\\s\]/g, ' '); let tokens = processed.split(/\\s+/).filter(token => token.length > 0); if (removeStopwords) { tokens = tokens.filter(token => !STOPWORDS\_FR.has(token)); } return tokens; } // Génération de N-grams function generateNgrams(tokens, n, separator = '\_') { if (tokens.length < n) return \[\]; const ngrams = \[\]; for (let i = 0; i <= tokens.length - n; i++) { const ngram = tokens.slice(i, i + n).join(separator); ngrams.push(ngram); } return ngrams; } // Génération basique de N-grams function generateBasicNgrams() { const text = document.getElementById('ngramInput').value.trim(); if (!text) { document.getElementById('ngramResult').textContent = 'Veuillez entrer du texte !'; return; } const n = parseInt(document.getElementById('ngramSize').value); const removeStopwords = document.getElementById('removeStopwords').checked; const tokens = preprocessText(text, removeStopwords); const ngrams = generateNgrams(tokens, n); const unique = \[...new Set(ngrams)\]; let html = \`<strong>🔗 N-GRAMS GÉNÉRÉS (N=${n})</strong>\\n\`; html += '=' \* 35 + '\\n\\n'; html += \`<strong>📝 Texte original :</strong>\\n"${text}"\\n\\n\`; html += \`<strong>🔤 Tokens après preprocessing :</strong>\\n\[${tokens.join(', ')}\]\\n\\n\`; html += \`<strong>🔗 ${ngrams.length} ${n}-grammes générés :</strong>\\n\`; ngrams.forEach((ngram, i) => { html += \`${(i + 1).toString().padStart(2, ' ')}. ${ngram}\\n\`; }); html += \`\\n<strong>📊 Statistiques :</strong>\\n\`; html += \` Total: ${ngrams.length}\\n\`; html += \` Uniques: ${unique.length}\\n\`; html += \` Répétitions: ${ngrams.length - unique.length}\\n\`; html += \` Ratio unique: ${(unique.length / ngrams.length \* 100).toFixed(1)}%\\n\`; if (unique.length !== ngrams.length) { html += \`\\n<strong>🔄 N-grammes répétés :</strong>\\n\`; const counts = {}; ngrams.forEach(ngram => { counts\[ngram\] = (counts\[ngram\] || 0) + 1; }); Object.entries(counts) .filter((\[ngram, count\]) => count > 1) .forEach((\[ngram, count\]) => { html += \` "${ngram}" × ${count}\\n\`; }); } document.getElementById('ngramResult').textContent = html; updateNgramsStats(ngrams, unique); } // Mise à jour des statistiques function updateNgramsStats(ngrams, unique) { const ratio = unique.length > 0 ? ((unique.length / ngrams.length) \* 100).toFixed(1) : 0; const avgLength = ngrams.length > 0 ? (ngrams.reduce((sum, ng) => sum + ng.length, 0) / ngrams.length).toFixed(1) : 0; document.getElementById('totalNgrams').textContent = ngrams.length; document.getElementById('uniqueNgrams').textContent = unique.length; document.getElementById('ngramRatio').textContent = ratio + '%'; document.getElementById('avgLength').textContent = avgLength; document.getElementById('ngramStats').style.display = 'grid'; } // N-grams avancés function generateAdvancedNgrams() { const text = document.getElementById('advancedInput').value.trim(); if (!text) { document.getElementById('advancedResult').textContent = 'Veuillez entrer du texte !'; return; } const minN = parseInt(document.getElementById('minN').value); const maxN = parseInt(document.getElementById('maxN').value); const minFreq = parseInt(document.getElementById('minFreq').value); const maxNgrams = parseInt(document.getElementById('maxNgrams').value); const separator = document.getElementById('separator').value; if (minN > maxN) { document.getElementById('advancedResult').textContent = 'Erreur : N min doit être ≤ N max !'; return; } const tokens = preprocessText(text, true); // Générer tous les N-grams de la plage let allNgrams = \[\]; for (let n = minN; n <= maxN; n++) { const ngrams = generateNgrams(tokens, n, separator); allNgrams.push(...ngrams); } // Compter les fréquences const frequencies = {}; allNgrams.forEach(ngram => { frequencies\[ngram\] = (frequencies\[ngram\] || 0) + 1; }); // Filtrer par fréquence const filtered = Object.entries(frequencies) .filter((\[ngram, freq\]) => freq >= minFreq) .sort((a, b) => b\[1\] - a\[1\]) .slice(0, maxNgrams); let html = \`<strong>🔧 N-GRAMS AVANCÉS (${minN}-${maxN})</strong>\\n\`; html += '=' \* 40 + '\\n\\n'; html += \`<strong>⚙️ Configuration :</strong>\\n\`; html += \` Plage N: ${minN} à ${maxN}\\n\`; html += \` Fréquence min: ${minFreq}\\n\`; html += \` Max N-grams: ${maxNgrams}\\n\`; html += \` Séparateur: "${separator}"\\n\\n\`; html += \`<strong>📊 Résultats (${filtered.length} N-grams) :</strong>\\n\`; filtered.forEach((\[ngram, freq\], i) => { const n = ngram.split(separator).length; const medal = i < 3 ? \['🥇', '🥈', '🥉'\]\[i\] : \`${(i + 1).toString().padStart(2, ' ')}.\`; html += \`${medal} ${ngram} (N=${n}, freq=${freq})\\n\`; }); if (filtered.length === 0) { html += '❌ Aucun N-gram ne respecte les critères.\\n'; html += '💡 Essayez de réduire la fréquence minimale.'; } document.getElementById('advancedResult').textContent = html; } // Comparaison des tailles de N-grams function compareNgramSizes() { const text = document.getElementById('comparisonInput').value.trim(); if (!text) { document.getElementById('comparisonResult').textContent = 'Veuillez entrer du texte !'; return; } const tokens = preprocessText(text, true); const sizes = \[1, 2, 3, 4\]; const results = {}; let html = \`<strong>📊 COMPARAISON TAILLES N-GRAMS</strong>\\n\`; html += '=' \* 45 + '\\n\\n'; html += \`<strong>📝 Texte analysé :</strong> "${text.substring(0, 60)}..."\\n\`; html += \`<strong>🔤 Tokens :</strong> ${tokens.length} mots après preprocessing\\n\\n\`; sizes.forEach(n => { if (tokens.length >= n) { const ngrams = generateNgrams(tokens, n); const unique = \[...new Set(ngrams)\]; results\[n\] = { total: ngrams.length, unique: unique.length, ratio: unique.length / ngrams.length \* 100 }; html += \`<strong>${n}-grammes :</strong>\\n\`; html += \` Total: ${ngrams.length}\\n\`; html += \` Uniques: ${unique.length}\\n\`; html += \` Ratio unique: ${results\[n\].ratio.toFixed(1)}%\\n\`; html += \` Exemples: ${unique.slice(0, 3).join(', ')}\\n\\n\`; } else { html += \`<strong>${n}-grammes :</strong> Impossible (texte trop court)\\n\\n\`; } }); html += \`<strong>💡 OBSERVATIONS :</strong>\\n\`; html += \`• Plus N augmente, plus on a de variété\\n\`; html += \`• Mais aussi plus de sparsité (N-grams uniques)\\n\`; html += \`• Trade-off entre contexte et généralisation\\n\`; html += \`• Optimal souvent entre N=2 et N=3\`; document.getElementById('comparisonResult').textContent = html; updateComparisonChart(results); } // Mise à jour du graphique de comparaison function updateComparisonChart(results) { const chart = document.getElementById('performanceChart'); if (!chart) return; const maxValue = Math.max(...Object.values(results).map(r => r.unique)); \[1, 2, 3, 4\].forEach(n => { const bar = document.getElementById(\`bar${n}\`); const value = document.getElementById(\`value${n}\`); if (bar && value && results\[n\]) { const height = (results\[n\].unique / maxValue) \* 100; bar.style.height = height + '%'; value.textContent = results\[n\].unique; } }); chart.style.display = 'block'; } // Extraction d'expressions function extractExpressions() { const text = document.getElementById('expressionInput').value.trim(); if (!text) { document.getElementById('expressionResult').textContent = 'Veuillez entrer du texte !'; return; } const threshold = parseInt(document.getElementById('freqThreshold').value); const type = document.getElementById('expressionType').value; const maxN = parseInt(document.getElementById('maxNExpression').value); // Découper le texte en phrases pour avoir plusieurs documents const sentences = text.split(/\[.!?\]+/).filter(s => s.trim()); if (sentences.length < 2) { document.getElementById('expressionResult').textContent = 'Le texte doit contenir plusieurs phrases !'; return; } // Générer N-grams de 2 à maxN let allNgrams = \[\]; sentences.forEach(sentence => { const tokens = preprocessText(sentence, true); for (let n = 2; n <= maxN; n++) { const ngrams = generateNgrams(tokens, n); allNgrams.push(...ngrams); } }); // Compter les fréquences const frequencies = {}; allNgrams.forEach(ngram => { frequencies\[ngram\] = (frequencies\[ngram\] || 0) + 1; }); // Filtrer par fréquence et type let expressions = Object.entries(frequencies) .filter((\[ngram, freq\]) => freq >= threshold) .sort((a, b) => b\[1\] - a\[1\]); // Filtrer par type si spécifié if (type === 'tech') { const techWords = \['intelligence', 'artificielle', 'machine', 'learning', 'deep', 'algorithm', 'data', 'science', 'neural', 'network'\]; expressions = expressions.filter((\[ngram\]) => techWords.some(word => ngram.toLowerCase().includes(word)) ); } else if (type === 'business') { const businessWords = \['startup', 'entrepreneur', 'business', 'marketing', 'finance', 'management', 'strategy'\]; expressions = expressions.filter((\[ngram\]) => businessWords.some(word => ngram.toLowerCase().includes(word)) ); } let html = \`<strong>🔍 EXPRESSIONS EXTRAITES</strong>\\n\`; html += '=' \* 35 + '\\n\\n'; html += \`<strong>⚙️ Paramètres :</strong>\\n\`; html += \` Seuil fréquence: ${threshold}\\n\`; html += \` Type: ${type}\\n\`; html += \` N-gram max: ${maxN}\\n\`; html += \` Phrases analysées: ${sentences.length}\\n\\n\`; if (expressions.length > 0) { html += \`<strong>🔑 ${expressions.length} expressions trouvées :</strong>\\n\`; expressions.slice(0, 15).forEach((\[expr, freq\], i) => { const rank = i + 1; const medal = rank <= 3 ? \['🥇', '🥈', '🥉'\]\[rank - 1\] : \`${rank.toString().padStart(2, ' ')}.\`; const n = expr.split('\_').length; // Catégoriser l'expression let category = "💡 Général"; if (\['intelligence', 'artificielle', 'machine', 'learning'\].some(word => expr.toLowerCase().includes(word))) { category = "🤖 IA/ML"; } else if (\['data', 'big', 'science'\].some(word => expr.toLowerCase().includes(word))) { category = "📊 Data"; } else if (\['deep', 'réseaux', 'neurones'\].some(word => expr.toLowerCase().includes(word))) { category = "🧠 Deep Learning"; } html += \`${medal} ${expr.replace(/\_/g, ' ')} (×${freq}, ${n}-gram) ${category}\\n\`; }); // Affichage visuel const displayDiv = document.getElementById('expressionDisplay'); displayDiv.innerHTML = expressions.slice(0, 10).map((\[expr, freq\]) => \`<span class="ngram-token">${expr.replace(/\_/g, ' ')} (${freq})</span>\` ).join(''); displayDiv.style.display = 'flex'; } else { html += \`❌ Aucune expression trouvée.\\n\`; html += \`💡 Essayez de réduire le seuil de fréquence.\`; } document.getElementById('expressionResult').textContent = html; } // Détection de langue function detectLanguage() { const text = document.getElementById('languageInput').value.trim(); if (!text) { document.getElementById('languageResult').textContent = 'Veuillez entrer du texte !'; return; } const method = document.getElementById('detectionMethod').value; const showDetails = document.getElementById('showDetails').checked; // Profils de langues const languageProfiles = { 'français': { char\_trigrams: \['les', 'des', 'une', 'que', 'est', 'ent', 'ion', 'tion', 'eur', 'eau', 'ant', 'ment'\], word\_bigrams: \['de\_la', 'de\_le', 'et\_de', 'dans\_le', 'pour\_le', 'avec\_le'\] }, 'anglais': { char\_trigrams: \['the', 'and', 'ing', 'ion', 'tion', 'ent', 'ers', 'all', 'you', 'ork', 'arn', 'ive'\], word\_bigrams: \['of\_the', 'in\_the', 'to\_the', 'and\_the', 'for\_the', 'with\_the'\] }, 'espagnol': { char\_trigrams: \['que', 'los', 'las', 'ión', 'ado', 'osa', 'nte', 'era', 'mos', 'dad', 'cia', 'sta'\], word\_bigrams: \['de\_la', 'de\_los', 'en\_el', 'para\_el', 'con\_el', 'por\_el'\] }, 'italien': { char\_trigrams: \['che', 'gli', 'lla', 'nte', 'ama', 'ono', 'ere', 'ato', 'ivo', 'sta', 'ria', 'ica'\], word\_bigrams: \['di\_la', 'in\_il', 'per\_il', 'con\_il', 'del\_la', 'nel\_la'\] }, 'allemand': { char\_trigrams: \['und', 'der', 'die', 'ich', 'ung', 'eit', 'ein', 'ern', 'sch', 'ver', 'end', 'nen'\], word\_bigrams: \['in\_der', 'auf\_der', 'mit\_der', 'von\_der', 'zu\_der', 'bei\_der'\] } }; let scores = {}; if (method === 'char\_trigrams' || method === 'combined') { // Trigrammes de caractères const textClean = text.toLowerCase().replace(/\[^\\w\\s\]/g, ''); const charTrigrams = \[\]; for (let i = 0; i <= textClean.length - 3; i++) { charTrigrams.push(textClean.substring(i, i + 3)); } Object.entries(languageProfiles).forEach((\[lang, profile\]) => { if (!scores\[lang\]) scores\[lang\] = 0; const score = charTrigrams.filter(trigram => profile.char\_trigrams.includes(trigram)).length; scores\[lang\] += score / charTrigrams.length; }); } if (method === 'word\_bigrams' || method === 'combined') { // Bigrammes de mots const tokens = preprocessText(text, false); const wordBigrams = generateNgrams(tokens, 2); Object.entries(languageProfiles).forEach((\[lang, profile\]) => { if (!scores\[lang\]) scores\[lang\] = 0; const score = wordBigrams.filter(bigram => profile.word\_bigrams.includes(bigram)).length; scores\[lang\] += score / wordBigrams.length; }); } // Trier par score const results = Object.entries(scores).sort((a, b) => b\[1\] - a\[1\]); let html = \`<strong>🌍 DÉTECTION DE LANGUE</strong>\\n\`; html += '=' \* 35 + '\\n\\n'; html += \`<strong>📝 Texte analysé :</strong>\\n"${text}"\\n\\n\`; html += \`<strong>🔧 Méthode :</strong> ${method}\\n\`; html += \`<strong>📊 Caractères :</strong> ${text.length}\\n\\n\`; html += \`<strong>🎯 Résultats de détection :</strong>\\n\`; results.forEach((\[lang, score\], index) => { const percentage = (score \* 100).toFixed(1); const confidence = score > 0.1 ? 'ÉLEVÉE' : score > 0.05 ? 'MOYENNE' : 'FAIBLE'; const flags = { 'français': '🇫🇷', 'anglais': '🇺🇸', 'espagnol': '🇪🇸', 'italien': '🇮🇹', 'allemand': '🇩🇪' }; const flag = flags\[lang\] || '🌍'; const prediction = index === 0 ? ' ← DÉTECTÉE' : ''; html += \`${flag} ${lang.padEnd(10)} : ${percentage.padStart(5)}% (${confidence})${prediction}\\n\`; }); const bestMatch = results\[0\]; html += \`\\n<strong>🏆 Langue détectée :</strong> ${bestMatch\[0\].toUpperCase()}\\n\`; html += \`<strong>📈 Score de confiance :</strong> ${(bestMatch\[1\] \* 100).toFixed(1)}%\`; document.getElementById('languageResult').textContent = html; } // Charger des exemples de langues function loadLanguageExample(language) { const examples = { 'french': "L'intelligence artificielle transforme notre façon de travailler et d'apprendre. Les algorithmes de machine learning analysent des quantités massives de données.", 'english': "Artificial intelligence is transforming the way we work and learn. Machine learning algorithms analyze massive amounts of data.", 'spanish': "La inteligencia artificial está transformando la forma en que trabajamos y aprendemos. Los algoritmos de aprendizaje automático analizan cantidades masivas de datos.", 'italian': "L'intelligenza artificiale sta trasformando il modo in cui lavoriamo e impariamo. Gli algoritmi di machine learning analizzano quantità massive di dati.", 'german': "Künstliche Intelligenz verändert die Art, wie wir arbeiten und lernen. Machine-Learning-Algorithmen analysieren massive Datenmengen." }; document.getElementById('languageInput').value = examples\[language\]; } // Classification avec N-grams function classifyWithNgrams() { const trainText = document.getElementById('trainDocsNgrams').value.trim(); const testText = document.getElementById('testDocNgrams').value.trim(); const method = document.getElementById('classificationMethod').value; if (!testText) { document.getElementById('ngramClassificationResult').textContent = 'Veuillez entrer un document à classifier !'; return; } // Parser les documents d'entraînement const trainDocs = trainText.split('\\n').map(line => { const colonIndex = line.indexOf(':'); return { label: line.substring(0, colonIndex).trim(), content: line.substring(colonIndex + 1).trim() }; }); // Créer les profils par catégorie avec N-grams const categoryProfiles = {}; trainDocs.forEach(doc => { if (!categoryProfiles\[doc.label\]) { categoryProfiles\[doc.label\] = {}; } const tokens = preprocessText(doc.content, true); let ngrams = \[\]; if (method === 'unigrams') { ngrams = generateNgrams(tokens, 1); } else if (method === 'bigrams') { ngrams = generateNgrams(tokens, 2); } else if (method === 'mixed') { ngrams = \[ ...generateNgrams(tokens, 1), ...generateNgrams(tokens, 2) \]; } else if (method === 'trigrams') { ngrams = \[ ...generateNgrams(tokens, 1), ...generateNgrams(tokens, 2), ...generateNgrams(tokens, 3) \]; } ngrams.forEach(ngram => { categoryProfiles\[doc.label\]\[ngram\] = (categoryProfiles\[doc.label\]\[ngram\] || 0) + 1; }); }); // Analyser le document test const testTokens = preprocessText(testText, true); let testNgrams = \[\]; if (method === 'unigrams') { testNgrams = generateNgrams(testTokens, 1); } else if (method === 'bigrams') { testNgrams = generateNgrams(testTokens, 2); } else if (method === 'mixed') { testNgrams = \[ ...generateNgrams(testTokens, 1), ...generateNgrams(testTokens, 2) \]; } else if (method === 'trigrams') { testNgrams = \[ ...generateNgrams(testTokens, 1), ...generateNgrams(testTokens, 2), ...generateNgrams(testTokens, 3) \]; } // Calculer les scores const scores = {}; Object.entries(categoryProfiles).forEach((\[label, profile\]) => { let score = 0; testNgrams.forEach(ngram => { if (profile\[ngram\]) { score += profile\[ngram\]; } }); scores\[label\] = score / testNgrams.length; // Normaliser }); // Prédiction const predicted = Object.entries(scores).sort((a, b) => b\[1\] - a\[1\]); let html = \`<strong>🎯 CLASSIFICATION AVEC N-GRAMS</strong>\\n\`; html += '=' \* 45 + '\\n\\n'; html += \`<strong>📄 Document test :</strong>\\n"${testText}"\\n\\n\`; html += \`<strong>🔧 Méthode :</strong> ${method}\\n\`; html += \`<strong>🔗 N-grams extraits :</strong> ${testNgrams.length}\\n\`; html += \`<strong>📝 Exemples :</strong> ${testNgrams.slice(0, 5).join(', ')}\\n\\n\`; html += \`<strong>📊 Scores par catégorie :</strong>\\n\`; predicted.forEach((\[label, score\], index) => { const percentage = (score \* 100).toFixed(1); const bar = '█'.repeat(Math.round(score \* 20)); const prediction = index === 0 ? ' ← PRÉDICTION' : ''; html += \`${label.padEnd(8)} : ${bar.padEnd(20)} ${percentage}%${prediction}\\n\`; }); html += \`\\n<strong>🎯 Catégorie prédite :</strong> ${predicted\[0\]\[0\].toUpperCase()}\\n\`; html += \`<strong>📈 Confiance :</strong> ${(predicted\[0\]\[1\] \* 100).toFixed(1)}%\`; document.getElementById('ngramClassificationResult').textContent = html; } // Analyse de performance function analyzePerformance() { const text = document.getElementById('performanceInput').value.trim(); if (!text) { document.getElementById('performanceResult').textContent = 'Veuillez entrer du texte !'; return; } const maxN = parseInt(document.getElementById('maxNPerf').value); const showMemory = document.getElementById('showMemory').checked; const docs = text.split('\\n').filter(doc => doc.trim()); const tokens = docs.map(doc => preprocessText(doc, true)); let html = \`<strong>📊 ANALYSE DE PERFORMANCE N-GRAMS</strong>\\n\`; html += '=' \* 50 + '\\n\\n'; html += \`<strong>📄 Corpus analysé :</strong>\\n\`; html += \` Documents : ${docs.length}\\n\`; html += \` Mots totaux : ${tokens.flat().length}\\n\`; html += \` Mots moyens/doc : ${Math.round(tokens.flat().length / docs.length)}\\n\\n\`; const performanceData = {}; for (let n = 1; n <= maxN; n++) { let allNgrams = \[\]; tokens.forEach(docTokens => { const ngrams = generateNgrams(docTokens, n); allNgrams.push(...ngrams); }); const unique = \[...new Set(allNgrams)\]; performanceData\[n\] = { total: allNgrams.length, unique: unique.length, sparsity: allNgrams.length > 0 ? (1 - unique.length / allNgrams.length) \* 100 : 0 }; html += \`<strong>📊 ${n}-grammes :</strong>\\n\`; html += \` Total généré : ${allNgrams.length}\\n\`; html += \` Vocabulaire unique : ${unique.length}\\n\`; html += \` Taux de répétition : ${(100 - (unique.length / Math.max(allNgrams.length, 1) \* 100)).toFixed(1)}%\\n\`; if (showMemory) { // Estimation mémoire (très approximative) const avgLength = unique.reduce((sum, ng) => sum + ng.length, 0) / unique.length; const memoryKB = (unique.length \* avgLength \* 2) / 1024; // 2 bytes par char html += \` Mémoire estimée : ${memoryKB.toFixed(1)} KB\\n\`; } html += '\\n'; } // Analyse de l'explosion combinatoire html += \`<strong>🚨 ANALYSE DE L'EXPLOSION COMBINATOIRE :</strong>\\n\`; for (let n = 1; n <= maxN; n++) { const ratio = n > 1 ? (performanceData\[n\].unique / performanceData\[n - 1\].unique).toFixed(2) : 'N/A'; html += \` N=${n} : ${performanceData\[n\].unique} mots (×${ratio} vs N=${n - 1})\\n\`; } html += \`\\n<strong>💡 RECOMMANDATIONS :</strong>\\n\`; if (performanceData\[2\] && performanceData\[2\].unique > 1000) { html += \`⚠️ Vocabulaire déjà important avec bigrammes\\n\`; } if (performanceData\[3\] && performanceData\[3\].unique > 5000) { html += \`🚨 Explosion combinatoire avec trigrammes\\n\`; } html += \`✅ Optimal probablement entre N=1 et N=${maxN <= 3 ? maxN : 3}\\n\`; html += \`🎯 Considérer filtrage par fréquence minimale\`; document.getElementById('performanceResult').textContent = html; updatePerformanceChart(performanceData, maxN); } // Mise à jour du graphique de performance function updatePerformanceChart(data, maxN) { const chart = document.getElementById('performanceVizChart'); if (!chart) return; const maxValue = Math.max(...Object.values(data).map(d => d.unique)); for (let n = 1; n <= 5; n++) { const bar = document.getElementById(\`perfBar${n}\`); const value = document.getElementById(\`perfValue${n}\`); if (bar && value) { if (n <= maxN && data\[n\]) { const height = (data\[n\].unique / maxValue) \* 100; bar.style.height = height + '%'; value.textContent = data\[n\].unique; bar.style.opacity = '1'; } else { bar.style.height = '0%'; value.textContent = '0'; bar.style.opacity = '0.3'; } } } chart.style.display = 'block'; } // Fonctions utilitaires function updateThresholdValue(value) { document.getElementById('thresholdValue').textContent = value; } function updateMaxNValue(value) { document.getElementById('maxNValue').textContent = value; } // Initialisation window.addEventListener('load', function () { // Animation des sections const sections = document.querySelectorAll('.section'); sections.forEach((section, index) => { setTimeout(() => { section.style.opacity = '1'; section.style.transform = 'translateY(0)'; }, index \* 200); }); });
