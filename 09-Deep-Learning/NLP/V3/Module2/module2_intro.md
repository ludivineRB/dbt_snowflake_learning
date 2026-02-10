---
title: 'Module 2 : Introduction au Preprocessing'
description: 'Formation NLP - Module 2 : Introduction au Preprocessing'
tags:
  - NLP
  - 09-Deep-Learning
category: 09-Deep-Learning
---

[📚 Module 1](../module1/module1_intro.html) → 🧹 Module 2 : Preprocessing

# 🧹 Module 2 : Preprocessing et Tokenisation

Transformer le texte brut en données exploitables pour le NLP

### 🎯 Objectifs du Module

À la fin de ce module, vous serez capable de :

*   Comprendre pourquoi le preprocessing est crucial en NLP
*   Maîtriser les étapes essentielles de nettoyage de texte
*   Implémenter différentes stratégies de tokenisation
*   Gérer les spécificités du français vs anglais
*   Construire un pipeline de preprocessing robuste
*   Évaluer la qualité d'un preprocessing

## ❗ Le Problème : Texte Brut vs Texte Exploitable

Imaginez que vous voulez analyser le sentiment de ces vrais exemples :

#### 😱 Texte Brut (Problématique)

"RT @user: LOL!!! C'est GÉNIAL 😍😍😍 https://bit.ly/xyz #amazing #best J'ADOOORE ce produit!!!" "Bof... pas terrible 😕 Service client = 💩 N'achetez PAS !!!" "Bon ben... c'est ok I guess 🤷‍♀️"

#### ✨ Après Preprocessing

\["génial", "adore", "produit"\] → POSITIF \["bof", "terrible", "achetez", "pas"\] → NÉGATIF \["bon", "ok"\] → NEUTRE

15-30%

Amélioration performance  
avec bon preprocessing

70%

Du temps NLP consacré  
au preprocessing

5-10x

Réduction taille  
vocabulaire

## 🔍 Pourquoi le Preprocessing est Crucial

#### ⚠️ Sans Preprocessing - Problèmes Typiques

*   **Vocabulaire explosif :** "SUPER", "super", "Super!" = 3 mots différents
*   **Bruit :** URLs, emails, hashtags polluent l'analyse
*   **Incohérence :** "n'est pas" vs "n est pas" vs "nest pas"
*   **Mots vides :** "le", "de", "et" dominent sans apporter d'info
*   **Variabilité :** "😍" vs "magnifique" = même sentiment, encodage différent

#### ✅ Avec Preprocessing - Bénéfices

*   **Cohérence :** Tous les mots en minuscules normalisées
*   **Focus :** Seuls les mots porteurs de sens sont conservés
*   **Efficacité :** Vocabulaire réduit = calculs plus rapides
*   **Performance :** Meilleure généralisation des modèles
*   **Robustesse :** Gestion des cas particuliers (fautes, abréviations)

## 🔧 Le Pipeline de Preprocessing

### 📋 Étapes Typiques (Ordre Important !)

**1\. Nettoyage**  
Casse, ponctuation

→

**2\. Normalisation**  
Accents, espaces

→

**3\. Tokenisation**  
Découpage en mots

→

**4\. Filtrage**  
Stopwords, longueur

→

**5\. Lemmatisation**  
Forme canonique

#### 💡 Principe Clé

Il n'existe pas de preprocessing "universel" ! Le bon preprocessing dépend de :

*   **Type de texte :** Tweet vs article académique vs SMS
*   **Tâche finale :** Sentiment vs traduction vs résumé
*   **Langue :** Français vs anglais vs multilingue
*   **Domaine :** Médical vs financier vs général

## 🧪 Démo Interactive : Avant/Après

### 🔬 Testez le Preprocessing en Temps Réel

Tapez du texte "sale" et voyez la transformation :

⚡ Préprocesser 🔄 Reset

#### 🔧 Étapes de Transformation :

**1\. Texte Original :**

**2\. Après Nettoyage (minuscules, URLs) :**

**3\. Après Suppression Ponctuation :**

**4\. Après Tokenisation :**

**5\. Après Filtrage (stopwords, longueur) :**

**📊 Résultat Final :**

## 📚 Ce que Vous Allez Apprendre

### 🧹 Nettoyage & Normalisation

*   Gestion de la casse
*   Suppression ponctuation
*   Normalisation Unicode
*   Suppression URLs, emails
*   Gestion des emojis

### ✂️ Tokenisation

*   Tokenisation par mots
*   Gestion des contractions
*   Tokenisation sous-mots
*   Spécificités du français
*   Comparaison NLTK vs spaCy

### ⚙️ Techniques Avancées

• Stopwords intelligents

• Lemmatisation française

• Stemming vs Lemmatisation

• Pipeline personnalisé

[⬅️ Module 1 Terminé](../module1/module1_resume.html) [🧹 Commencer le Nettoyage](module2_nettoyage.html)

### 🚀 Prochaine Étape

Maintenant que vous comprenez l'importance du preprocessing, plongeons dans les techniques concrètes de nettoyage de texte !

[Maîtriser le Nettoyage ✨](module2_nettoyage.html)

// Stopwords français basiques pour la démo const stopwordsFrancais = new Set(\[ 'le', 'de', 'et', 'à', 'un', 'il', 'être', 'et', 'en', 'avoir', 'que', 'pour', 'dans', 'ce', 'son', 'une', 'sur', 'avec', 'ne', 'se', 'pas', 'tout', 'plus', 'par', 'grand', 'en', 'le', 'son', 'que', 'ce', 'lui', 'au', 'du', 'des', 'la', 'les', 'je', 'tu', 'nous', 'vous', 'ils', 'elles', 'mon', 'ma', 'mes', 'ton', 'ta', 'tes', 'sa', 'ses', 'notre', 'nos', 'votre', 'vos', 'leur', 'leurs', 'est', 'sont', 'était', 'étaient', 'ai', 'as', 'a', 'avons', 'avez', 'ont' \]); function processText() { const rawText = document.getElementById('rawText').value.trim(); if (!rawText) { alert('Veuillez entrer du texte à préprocesser !'); return; } // Afficher la section des étapes document.getElementById('processingSteps').style.display = 'block'; // Étape 0 : Texte original document.getElementById('step0').textContent = rawText; // Étape 1 : Nettoyage initial let step1 = rawText.toLowerCase(); step1 = step1.replace(/https?:\\/\\/\[^\\s\]+/g, '\[URL\]'); // URLs step1 = step1.replace(/@\\w+/g, '\[MENTION\]'); // Mentions step1 = step1.replace(/#\\w+/g, '\[HASHTAG\]'); // Hashtags step1 = step1.replace(/rt\\s+/g, ''); // Retweets document.getElementById('step1').textContent = step1; // Étape 2 : Suppression ponctuation et emojis let step2 = step1.replace(/\[^\\w\\s\]/g, ' '); // Garde seulement lettres, chiffres et espaces step2 = step2.replace(/\\s+/g, ' ').trim(); // Normalise les espaces document.getElementById('step2').textContent = step2; // Étape 3 : Tokenisation let tokens = step2.split(/\\s+/).filter(token => token.length > 0); document.getElementById('step3').textContent = '\["' + tokens.join('", "') + '"\]'; // Étape 4 : Filtrage let filteredTokens = tokens.filter(token => { return token.length > 2 && // Mots de plus de 2 caractères !stopwordsFrancais.has(token) && // Pas un stopword !/^\\d+$/.test(token) && // Pas un nombre pur token !== 'url' && token !== 'mention' && token !== 'hashtag'; // Pas nos marqueurs }); document.getElementById('step4').textContent = '\["' + filteredTokens.join('", "') + '"\]'; // Résultat final avec statistiques const originalWords = rawText.split(/\\s+/).length; const finalWords = filteredTokens.length; const reduction = Math.round((1 - finalWords / originalWords) \* 100); document.getElementById('finalResult').innerHTML = \` <strong>Tokens finaux :</strong> \["${filteredTokens.join('", "')}"\]<br> <strong>Statistiques :</strong><br> • Mots originaux : ${originalWords}<br> • Mots après preprocessing : ${finalWords}<br> • Réduction : ${reduction}% \`; // Faire défiler vers les résultats document.getElementById('processingSteps').scrollIntoView({ behavior: 'smooth', block: 'center' }); } function resetDemo() { document.getElementById('rawText').value = ''; document.getElementById('processingSteps').style.display = 'none'; } // Exemples préremplis au clic document.getElementById('rawText').addEventListener('click', function() { if (!this.value) { const examples = \[ "RT @user: LOL!!! C'est GÉNIAL 😍😍😍 https://bit.ly/xyz #amazing #best J'ADOOORE ce produit!!!", "Bof... pas terrible 😕 Service client = 💩 N'achetez PAS !!!", "Salut! Comment ça va??? J'espère que tout va BIEN 🙂 @marie #bonnejournée" \]; this.value = examples\[Math.floor(Math.random() \* examples.length)\]; } });
