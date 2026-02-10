---
title: Module 3 - TF-IDF Démonstrations
description: Formation NLP - Module 3 - TF-IDF Démonstrations
tags:
  - NLP
  - 09-Deep-Learning
category: 09-Deep-Learning
---

# ⚖️ TF-IDF - Démonstrations Interactives

Expérimentez avec le calcul et les applications du TF-IDF

[← Concepts TF-IDF](module3_tfidf_concepts.html) [N-grams →](module3_ngrams_concepts.html) [🏠 Index Module 3](module3_index.html)

## 🧮 Calculateur TF-IDF Interactif

🎯 Calcul Basique ⚙️ Options Avancées 📋 Étape par Étape

### ✍️ Entrez vos documents (un par ligne) :

Le machine learning transforme l'intelligence artificielle Les algorithmes d'apprentissage automatique sont puissants Le deep learning utilise des réseaux de neurones L'intelligence artificielle révolutionne de nombreux domaines ⚖️ Calculer TF-IDF

Cliquez sur "Calculer TF-IDF" pour voir les résultats...

0

Documents

0

Mots Uniques

0.000

TF-IDF Moyen

0.000

TF-IDF Max

### ⚙️ Configuration Avancée TF-IDF :

L'intelligence artificielle révolutionne le secteur de la santé Le machine learning permet des diagnostics plus précis Les algorithmes de deep learning analysent les images médicales La data science exploite les données cliniques massives L'IA conversationnelle améliore l'interaction patient-médecin

Schéma TF : Normalisé (défaut) Comptage brut Logarithmique Booléen

Schéma IDF : Standard Smooth (+1) IDF Max

 Normalisation L2

Seuil d'affichage : 

🔧 Calculer TF-IDF Avancé

Configurez les options et calculez...

### 📋 Calcul Détaillé Étape par Étape

Entrez un petit corpus pour voir chaque étape du calcul :

Python machine learning Java développement web Machine learning intelligence artificielle 📋 Calcul Détaillé

Calcul étape par étape apparaîtra ici...

## 🔑 Extracteur de Mots-Clés TF-IDF

### 📄 Texte à analyser :

L'intelligence artificielle révolutionne le secteur de la santé en permettant des diagnostics plus précis et rapides. Les algorithmes de machine learning analysent des millions de données médicales pour identifier des patterns invisibles à l'œil humain. Les radiologues utilisent maintenant des outils d'IA pour détecter les cancers plus efficacement. Cette technologie transforme également la recherche pharmaceutique en accélérant la découverte de nouveaux médicaments. Les hôpitaux intègrent progressivement ces solutions innovantes pour améliorer les soins aux patients et optimiser leurs processus internes.

Nombre de mots-clés : 

 Exclure les mots vides

Longueur min. mot : 

🔑 Extraire Mots-Clés

Mots-clés extraits apparaîtront ici...

## 🔍 Moteur de Recherche TF-IDF

### 📚 Base de documents :

Doc1: Machine learning révolutionne l'analyse de données massives Doc2: Intelligence artificielle transforme les entreprises modernes Doc3: Python simplifie le développement d'applications web Doc4: Deep learning améliore la reconnaissance d'images Doc5: Data science exploite les algorithmes d'apprentissage Doc6: Réseaux de neurones imitent le fonctionnement du cerveau Doc7: Big data nécessite des outils de traitement spécialisés Doc8: Cloud computing facilite l'accès aux ressources

### 🔎 Votre recherche :

Nombre de résultats : 

Seuil de similarité : 

🔍 Rechercher

Résultats de recherche apparaîtront ici...

## ⚔️ Comparaison BoW vs TF-IDF

### 🧪 Test Comparatif :

Les spécialistes en intelligence artificielle développent des algorithmes avancés. Les développeurs utilisent Python pour programmer des applications modernes. L'intelligence artificielle transforme les méthodes de développement logiciel. Python facilite l'implémentation d'algorithmes de machine learning. Les algorithmes d'apprentissage automatique révolutionnent l'industrie. ⚔️ Comparer BoW vs TF-IDF

Comparaison apparaîtra ici...

**📊 Qu'observe-t-on ?**  
• **BoW** : Privilégie les mots fréquents dans chaque document  
• **TF-IDF** : Valorise les mots rares et discriminants  
• **Résultat** : TF-IDF est plus efficace pour identifier les thèmes spécifiques

## 💼 Applications Pratiques

### 🎯 Classification de Documents

Testez la classification avec TF-IDF :

#### 📚 Documents d'entraînement :

TECH: Python machine learning IA développement algorithmes SPORT: Football équipe joueur match victoire championnat SANTE: Médecin patient traitement hôpital diagnostic TECH: JavaScript web application programmation software SPORT: Tennis tournoi joueur raquette court victoire SANTE: Chirurgie opération patient médecin clinique

#### 🧪 Document à classer :

Les développeurs utilisent Python pour créer des applications d'intelligence artificielle sophistiquées

🎯 Classifier

Résultat de classification...

### 📈 Analyse de Performance

Comparez les performances TF-IDF selon différents paramètres :

Intelligence artificielle révolutionne secteur médical Python développement applications web modernes Machine learning analyse données clients Blockchain technologie sécurise transactions Cloud computing optimise infrastructures

Max features : 1000 3000 5000 10000

Min DF : 1 2 3

📈 Analyser Performance

Analyse de performance...

[← Concepts TF-IDF](module3_tfidf_concepts.html) [N-grams →](module3_ngrams_concepts.html) [🏠 Index Module 3](module3_index.html)

// Variables globales let currentTFIDFMatrix = null; let currentVocab = null; // Stopwords français const STOPWORDS\_FR = new Set(\[ 'le', 'de', 'et', 'à', 'un', 'il', 'être', 'en', 'avoir', 'que', 'pour', 'dans', 'ce', 'son', 'une', 'sur', 'avec', 'ne', 'se', 'pas', 'tout', 'plus', 'par', 'grand', 'son', 'que', 'ce', 'lui', 'au', 'du', 'des', 'la', 'les', 'est', 'cette', 'ces', 'mais', 'ou', 'si', 'nous', 'vous', 'ils', 'elles', 'aussi', 'très', 'bien', 'comme', 'donc', 'peut', 'fait', 'sans' \]); // Gestion des onglets function openTab(evt, tabName) { var i, tabcontent, tabs; tabcontent = document.getElementsByClassName("tab-content"); for (i = 0; i < tabcontent.length; i++) { tabcontent\[i\].classList.remove("active"); } tabs = document.getElementsByClassName("tab"); for (i = 0; i < tabs.length; i++) { tabs\[i\].classList.remove("active"); } document.getElementById(tabName).classList.add("active"); evt.currentTarget.classList.add("active"); } // Preprocessing du texte function preprocessText(text, removeStopwords = true) { let processed = text.toLowerCase(); processed = processed.replace(/\[^\\w\\s\]/g, ' '); let tokens = processed.split(/\\s+/).filter(token => token.length > 0); if (removeStopwords) { tokens = tokens.filter(token => !STOPWORDS\_FR.has(token)); } return tokens; } // Calcul TF-IDF basique function calculateBasicTFIDF() { const text = document.getElementById('tfidfInput').value.trim(); if (!text) { document.getElementById('basicTFIDFResult').textContent = 'Veuillez entrer des documents !'; return; } const docs = text.split('\\n').filter(doc => doc.trim()); const result = computeTFIDF(docs); displayTFIDFResult(result, 'basicTFIDFResult'); updateTFIDFStats(result); } // Calcul TF-IDF avancé function calculateAdvancedTFIDF() { const text = document.getElementById('advancedInput').value.trim(); if (!text) { document.getElementById('advancedResult').textContent = 'Veuillez entrer des documents !'; return; } const docs = text.split('\\n').filter(doc => doc.trim()); const options = { tfScheme: document.getElementById('tfScheme').value, idfScheme: document.getElementById('idfScheme').value, normalizeL2: document.getElementById('normalizeL2').checked, threshold: parseFloat(document.getElementById('displayThreshold').value) }; const result = computeTFIDF(docs, options); displayTFIDFResult(result, 'advancedResult', options); } // Calcul étape par étape function calculateStepByStep() { const text = document.getElementById('stepByStepInput').value.trim(); if (!text) { document.getElementById('stepByStepResult').textContent = 'Veuillez entrer des documents !'; return; } const docs = text.split('\\n').filter(doc => doc.trim()); let html = \`<strong>📋 CALCUL TF-IDF ÉTAPE PAR ÉTAPE</strong>\\n\`; html += '=' \* 50 + '\\n\\n'; // Étape 1: Preprocessing const processedDocs = docs.map(doc => preprocessText(doc)); html += \`<strong>1️⃣ PREPROCESSING :</strong>\\n\`; processedDocs.forEach((tokens, i) => { html += \`Doc ${i+1}: \[${tokens.join(', ')}\]\\n\`; }); // Étape 2: Vocabulaire const vocab = \[...new Set(processedDocs.flat())\].sort(); html += \`\\n<strong>2️⃣ VOCABULAIRE (${vocab.length} mots) :</strong>\\n\`; html += vocab.join(', ') + '\\n'; // Étape 3: Calcul TF html += '\\n<strong>3️⃣ CALCUL TERM FREQUENCY (TF) :</strong>\\n'; const tfMatrix = processedDocs.map((tokens, docIdx) => { html += \`\\nDoc ${docIdx + 1} (${tokens.length} mots) :\\n\`; const tf = {}; vocab.forEach(word => { const count = tokens.filter(t => t === word).length; tf\[word\] = count / tokens.length; if (count > 0) { html += \` TF("${word}") = ${count}/${tokens.length} = ${tf\[word\].toFixed(3)}\\n\`; } }); return tf; }); // Étape 4: Calcul IDF html += '\\n<strong>4️⃣ CALCUL INVERSE DOCUMENT FREQUENCY (IDF) :</strong>\\n'; const N = docs.length; const idf = {}; vocab.forEach(word => { const df = processedDocs.filter(tokens => tokens.includes(word)).length; idf\[word\] = Math.log(N / df); html += \`IDF("${word}") = log(${N}/${df}) = ${idf\[word\].toFixed(3)}\\n\`; }); // Étape 5: Calcul TF-IDF final html += '\\n<strong>5️⃣ CALCUL TF-IDF FINAL :</strong>\\n'; processedDocs.forEach((tokens, docIdx) => { html += \`\\nDoc ${docIdx + 1} - Top mots importants :\\n\`; const docTFIDF = \[\]; vocab.forEach(word => { const tfValue = tfMatrix\[docIdx\]\[word\]; const idfValue = idf\[word\]; const tfidfValue = tfValue \* idfValue; if (tfidfValue > 0) { docTFIDF.push({word, tfidf: tfidfValue, tf: tfValue, idf: idfValue}); } }); docTFIDF.sort((a, b) => b.tfidf - a.tfidf); docTFIDF.slice(0, 5).forEach(item => { html += \` "${item.word}": ${item.tf.toFixed(3)} × ${item.idf.toFixed(3)} = ${item.tfidf.toFixed(3)}\\n\`; }); }); document.getElementById('stepByStepResult').textContent = html; } // Fonction principale de calcul TF-IDF function computeTFIDF(docs, options = {}) { const opts = { tfScheme: 'normalized', idfScheme: 'standard', normalizeL2: true, threshold: 0.01, ...options }; // Preprocessing const processedDocs = docs.map(doc => preprocessText(doc)); const vocab = \[...new Set(processedDocs.flat())\].sort(); // Calcul IDF const N = docs.length; const idf = {}; vocab.forEach(word => { const df = processedDocs.filter(tokens => tokens.includes(word)).length; if (opts.idfScheme === 'smooth') { idf\[word\] = Math.log(N / (df + 1)) + 1; } else if (opts.idfScheme === 'max') { const maxDf = Math.max(...vocab.map(w => processedDocs.filter(tokens => tokens.includes(w)).length)); idf\[word\] = Math.log(maxDf / df); } else { // standard idf\[word\] = Math.log(N / df); } }); // Calcul TF-IDF const matrix = processedDocs.map(tokens => { const docLength = tokens.length; const tfidf = {}; vocab.forEach(word => { const count = tokens.filter(t => t === word).length; let tf = 0; if (opts.tfScheme === 'raw') { tf = count; } else if (opts.tfScheme === 'normalized') { tf = docLength > 0 ? count / docLength : 0; } else if (opts.tfScheme === 'log') { tf = count > 0 ? 1 + Math.log(count) : 0; } else if (opts.tfScheme === 'boolean') { tf = count > 0 ? 1 : 0; } tfidf\[word\] = tf \* idf\[word\]; }); // Normalisation L2 if (opts.normalizeL2) { const norm = Math.sqrt(Object.values(tfidf).reduce((sum, val) => sum + val \* val, 0)); if (norm > 0) { Object.keys(tfidf).forEach(word => { tfidf\[word\] /= norm; }); } } return tfidf; }); return { docs, processedDocs, vocab, idf, matrix, options: opts }; } // Affichage des résultats TF-IDF function displayTFIDFResult(result, targetId, options = {}) { let html = \`<strong>⚖️ RÉSULTATS TF-IDF</strong>\\n\`; html += '=' \* 35 + '\\n\\n'; if (options.tfScheme) { html += \`<strong>⚙️ Configuration :</strong>\\n\`; html += \`- Schéma TF: ${options.tfScheme}\\n\`; html += \`- Schéma IDF: ${options.idfScheme}\\n\`; html += \`- Normalisation L2: ${options.normalizeL2}\\n\`; html += \`- Seuil: ${options.threshold}\\n\\n\`; } html += \`<strong>📚 Vocabulaire :</strong> ${result.vocab.length} mots\\n\`; html += \`<strong>📄 Documents :</strong> ${result.docs.length}\\n\\n\`; // Top mots par document result.matrix.forEach((docTFIDF, docIdx) => { html += \`<strong>📄 Document ${docIdx + 1}:</strong> "${result.docs\[docIdx\].substring(0, 50)}..."\\n\`; const sortedWords = Object.entries(docTFIDF) .filter((\[word, score\]) => score >= (options.threshold || 0.01)) .sort((a, b) => b\[1\] - a\[1\]); html += 'Top mots importants :\\n'; sortedWords.slice(0, 8).forEach((\[word, score\]) => { html += \` "${word}": ${score.toFixed(3)}\\n\`; }); html += '\\n'; }); document.getElementById(targetId).textContent = html; // Sauvegarder pour autres fonctions currentTFIDFMatrix = result.matrix; currentVocab = result.vocab; } // Mise à jour des statistiques function updateTFIDFStats(result) { const allValues = result.matrix.flatMap(doc => Object.values(doc)).filter(v => v > 0); const avgTFIDF = allValues.length > 0 ? allValues.reduce((sum, val) => sum + val, 0) / allValues.length : 0; const maxTFIDF = Math.max(...allValues, 0); document.getElementById('totalDocs').textContent = result.docs.length; document.getElementById('uniqueWords').textContent = result.vocab.length; document.getElementById('avgTFIDF').textContent = avgTFIDF.toFixed(3); document.getElementById('maxTFIDF').textContent = maxTFIDF.toFixed(3); document.getElementById('tfidfStats').style.display = 'grid'; } // Extraction de mots-clés function extractKeywords() { const text = document.getElementById('keywordInput').value.trim(); if (!text) { document.getElementById('keywordResult').textContent = 'Veuillez entrer du texte !'; return; } const numKeywords = parseInt(document.getElementById('numKeywords').value); const removeStopwords = document.getElementById('removeStopwords').checked; const minLength = parseInt(document.getElementById('minWordLength').value); // Diviser le texte en phrases pour simuler plusieurs documents const sentences = text.split(/\[.!?\]+/).filter(s => s.trim()); if (sentences.length < 2) { document.getElementById('keywordResult').textContent = 'Le texte doit contenir plusieurs phrases !'; return; } const result = computeTFIDF(sentences, {normalizeL2: true}); // Calculer le score TF-IDF global pour chaque mot const globalScores = {}; result.vocab.forEach(word => { globalScores\[word\] = result.matrix.reduce((sum, doc) => sum + doc\[word\], 0); }); // Filtrer et trier let keywords = Object.entries(globalScores) .filter((\[word, score\]) => word.length >= minLength) .sort((a, b) => b\[1\] - a\[1\]) .slice(0, numKeywords); let html = \`<strong>🔑 MOTS-CLÉS EXTRAITS (Top ${numKeywords})</strong>\\n\`; html += '=' \* 45 + '\\n\\n'; html += \`<strong>📝 Texte analysé :</strong> ${text.length} caractères, ${sentences.length} phrases\\n\`; html += \`<strong>📊 Vocabulaire :</strong> ${result.vocab.length} mots uniques\\n\\n\`; html += \`<strong>🏆 Mots-clés les plus importants :</strong>\\n\`; keywords.forEach((\[word, score\], index) => { const medal = index < 3 ? \['🥇', '🥈', '🥉'\]\[index\] : \`${index + 1}.\`; html += \`${medal} "${word}" (score: ${score.toFixed(3)})\\n\`; }); document.getElementById('keywordResult').textContent = html; // Affichage visuel des mots-clés const displayDiv = document.getElementById('keywordDisplay'); displayDiv.innerHTML = keywords.map((\[word, score\]) => \`<span class="keyword-tag">${word}<span class="keyword-score">${score.toFixed(3)}</span></span>\` ).join(''); displayDiv.style.display = 'flex'; } // Recherche par similarité function searchSimilarity() { const corpusText = document.getElementById('searchCorpus').value.trim(); const query = document.getElementById('searchQuery').value.trim(); if (!query) { document.getElementById('searchResults').textContent = 'Veuillez entrer une requête !'; return; } const numResults = parseInt(document.getElementById('numResults').value); const threshold = parseFloat(document.getElementById('similarityThreshold').value); // Extraire les documents const docs = corpusText.split('\\n').map(line => { const colonIndex = line.indexOf(':'); return colonIndex > 0 ? line.substring(colonIndex + 1).trim() : line.trim(); }).filter(doc => doc); // Ajouter la requête comme dernier document const allDocs = \[...docs, query\]; const result = computeTFIDF(allDocs); // Calculer la similarité cosinus entre la requête et chaque document const queryVector = result.matrix\[result.matrix.length - 1\]; const similarities = \[\]; for (let i = 0; i < docs.length; i++) { const docVector = result.matrix\[i\]; const similarity = cosineSimilarity(queryVector, docVector, result.vocab); if (similarity >= threshold) { similarities.push({ index: i, doc: docs\[i\], similarity: similarity }); } } // Trier par similarité décroissante similarities.sort((a, b) => b.similarity - a.similarity); let html = \`<strong>🔍 RÉSULTATS DE RECHERCHE</strong>\\n\`; html += '=' \* 35 + '\\n\\n'; html += \`<strong>🔎 Requête :</strong> "${query}"\\n\`; html += \`<strong>📚 Corpus :</strong> ${docs.length} documents\\n\`; html += \`<strong>🎯 Seuil :</strong> ${threshold}\\n\`; html += \`<strong>📊 Trouvés :</strong> ${similarities.length} documents\\n\\n\`; if (similarities.length === 0) { html += \`❌ Aucun document ne dépasse le seuil de similarité de ${threshold}\\n\`; html += \`💡 Essayez de réduire le seuil ou modifier votre requête\`; } else { html += \`<strong>🏆 Top ${Math.min(numResults, similarities.length)} résultats :</strong>\\n\`; similarities.slice(0, numResults).forEach((result, index) => { const medal = index < 3 ? \['🥇', '🥈', '🥉'\]\[index\] : \`${index + 1}.\`; html += \`\\n${medal} Similarité: ${(result.similarity \* 100).toFixed(1)}%\\n\`; html += \` "${result.doc}"\\n\`; }); } document.getElementById('searchResults').textContent = html; } // Calcul de similarité cosinus function cosineSimilarity(vectorA, vectorB, vocab) { let dotProduct = 0; let normA = 0; let normB = 0; vocab.forEach(word => { const a = vectorA\[word\] || 0; const b = vectorB\[word\] || 0; dotProduct += a \* b; normA += a \* a; normB += b \* b; }); const denominator = Math.sqrt(normA) \* Math.sqrt(normB); return denominator > 0 ? dotProduct / denominator : 0; } // Comparaison BoW vs TF-IDF function compareBowTFIDF() { const text = document.getElementById('comparisonInput').value.trim(); if (!text) { document.getElementById('comparisonResult').textContent = 'Veuillez entrer du texte !'; return; } const docs = text.split('\\n').filter(doc => doc.trim()); // Calcul BoW (comptages simples) const processedDocs = docs.map(doc => preprocessText(doc)); const vocab = \[...new Set(processedDocs.flat())\].sort(); const bowMatrix = processedDocs.map(tokens => { const counts = {}; vocab.forEach(word => { counts\[word\] = tokens.filter(t => t === word).length; }); return counts; }); // Calcul TF-IDF const tfidfResult = computeTFIDF(docs); let html = \`<strong>⚔️ COMPARAISON BOW vs TF-IDF</strong>\\n\`; html += '=' \* 45 + '\\n\\n'; // Analyse comparative pour chaque document processedDocs.forEach((tokens, docIdx) => { html += \`<strong>📄 Document ${docIdx + 1}:</strong> "${docs\[docIdx\].substring(0, 40)}..."\\n\`; // Top mots BoW const bowTop = Object.entries(bowMatrix\[docIdx\]) .filter((\[word, count\]) => count > 0) .sort((a, b) => b\[1\] - a\[1\]) .slice(0, 5); // Top mots TF-IDF const tfidfTop = Object.entries(tfidfResult.matrix\[docIdx\]) .filter((\[word, score\]) => score > 0) .sort((a, b) => b\[1\] - a\[1\]) .slice(0, 5); html += \`BoW Top 5 : ${bowTop.map((\[w, c\]) => \`${w}(${c})\`).join(', ')}\\n\`; html += \`TF-IDF Top 5 : ${tfidfTop.map((\[w, s\]) => \`${w}(${s.toFixed(3)})\`).join(', ')}\\n\\n\`; }); html += \`<strong>🔍 OBSERVATIONS :</strong>\\n\`; html += \`• BoW privilégie les mots fréquents dans chaque document\\n\`; html += \`• TF-IDF valorise les mots rares et discriminants\\n\`; html += \`• TF-IDF est plus efficace pour identifier les thèmes spécifiques\\n\`; html += \`• BoW peut être dominé par des mots communs peu informatifs\`; document.getElementById('comparisonResult').textContent = html; } // Classification de documents function classifyDocument() { const trainText = document.getElementById('trainDocs').value.trim(); const testText = document.getElementById('testDoc').value.trim(); if (!testText) { document.getElementById('classificationResult').textContent = 'Veuillez entrer un document à classifier !'; return; } // Parser les documents d'entraînement const trainDocs = trainText.split('\\n').map(line => { const colonIndex = line.indexOf(':'); return { label: line.substring(0, colonIndex).trim(), content: line.substring(colonIndex + 1).trim() }; }); // Créer les profils par catégorie avec TF-IDF const allDocs = trainDocs.map(doc => doc.content).concat(\[testText\]); const result = computeTFIDF(allDocs); // Moyenner les profils par catégorie const categoryProfiles = {}; trainDocs.forEach((doc, idx) => { if (!categoryProfiles\[doc.label\]) { categoryProfiles\[doc.label\] = {}; } result.vocab.forEach(word => { if (!categoryProfiles\[doc.label\]\[word\]) { categoryProfiles\[doc.label\]\[word\] = 0; } categoryProfiles\[doc.label\]\[word\] += result.matrix\[idx\]\[word\]; }); }); // Normaliser les profils Object.keys(categoryProfiles).forEach(label => { const count = trainDocs.filter(doc => doc.label === label).length; result.vocab.forEach(word => { categoryProfiles\[label\]\[word\] /= count; }); }); // Calculer la similarité avec le document test const testVector = result.matrix\[result.matrix.length - 1\]; const similarities = {}; Object.entries(categoryProfiles).forEach((\[label, profile\]) => { similarities\[label\] = cosineSimilarity(testVector, profile, result.vocab); }); // Prédiction const predicted = Object.entries(similarities).sort((a, b) => b\[1\] - a\[1\]); let html = \`<strong>🎯 CLASSIFICATION AVEC TF-IDF</strong>\\n\`; html += '=' \* 40 + '\\n\\n'; html += \`<strong>📄 Document test :</strong>\\n"${testText}"\\n\\n\`; html += \`<strong>📊 Scores de similarité :</strong>\\n\`; predicted.forEach((\[label, score\], index) => { const percentage = (score \* 100).toFixed(1); const bar = '█'.repeat(Math.round(score \* 20)); const prediction = index === 0 ? ' ← PRÉDICTION' : ''; html += \`${label.padEnd(8)} : ${bar.padEnd(20)} ${percentage}%${prediction}\\n\`; }); html += \`\\n<strong>🏆 Catégorie prédite :</strong> ${predicted\[0\]\[0\].toUpperCase()}\\n\`; html += \`<strong>📈 Confiance :</strong> ${(predicted\[0\]\[1\] \* 100).toFixed(1)}%\`; document.getElementById('classificationResult').textContent = html; } // Analyse de performance function analyzePerformance() { const text = document.getElementById('performanceInput').value.trim(); if (!text) { document.getElementById('performanceResult').textContent = 'Veuillez entrer du corpus !'; return; } const docs = text.split('\\n').filter(doc => doc.trim()); const maxFeatures = parseInt(document.getElementById('maxFeatures').value); const minDF = parseInt(document.getElementById('minDF').value); let html = \`<strong>📈 ANALYSE DE PERFORMANCE TF-IDF</strong>\\n\`; html += '=' \* 45 + '\\n\\n'; html += \`<strong>📊 Corpus analysé :</strong>\\n\`; html += \` Documents : ${docs.length}\\n\`; html += \` Caractères totaux : ${docs.join('').length}\\n\`; html += \` Mots moyens/doc : ${Math.round(docs.reduce((sum, doc) => sum + doc.split(' ').length, 0) / docs.length)}\\n\\n\`; // Test avec différentes configurations const configs = \[ {name: 'Standard', maxFeatures: 1000, minDF: 1}, {name: 'Optimisé', maxFeatures: maxFeatures, minDF: minDF}, {name: 'Complet', maxFeatures: 10000, minDF: 1} \]; html += \`<strong>⚙️ COMPARAISON CONFIGURATIONS :</strong>\\n\`; html += \`Configuration Vocabulaire Temps Sparsité\\n\`; html += \`-\`.repeat(50) + '\\n'; configs.forEach(config => { const startTime = performance.now(); const result = computeTFIDF(docs, {}); const endTime = performance.now(); const time = (endTime - startTime).toFixed(1); const vocabSize = result.vocab.length; // Calculer la sparsité const totalValues = result.matrix.length \* result.vocab.length; const zeroValues = result.matrix.reduce((sum, doc) => { return sum + result.vocab.filter(word => doc\[word\] === 0).length; }, 0); const sparsity = ((zeroValues / totalValues) \* 100).toFixed(1); html += \`${config.name.padEnd(12)} ${vocabSize.toString().padEnd(9)} ${time.padEnd(6)}ms ${sparsity}%\\n\`; }); html += \`\\n<strong>💡 RECOMMANDATIONS :</strong>\\n\`; html += \`✅ max\_features: Commencer avec 3000-5000\\n\`; html += \`✅ min\_df: Utiliser 2-3 pour filtrer le bruit\\n\`; html += \`✅ TF-IDF généralement > BoW pour classification\\n\`; html += \`⚠️ Attention à l'overfitting avec trop de features\`; document.getElementById('performanceResult').textContent = html; } // Initialisation window.addEventListener('load', function() { // Animation des sections const sections = document.querySelectorAll('.section'); sections.forEach((section, index) => { setTimeout(() => { section.style.opacity = '1'; section.style.transform = 'translateY(0)'; }, index \* 200); }); });
