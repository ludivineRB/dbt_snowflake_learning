---
title: 'Module 7: Métriques et Optimisation des CNN'
description: 'Formation CNN - Module 7: Métriques et Optimisation des CNN'
tags:
  - CNN
  - 09-Deep-Learning
category: 09-Deep-Learning
---

# 📊 Module 7: Métriques et Optimisation des CNN

📚 Niveau: Avancé | ⏱️ Durée: 2h | 🎯 Objectif: Maîtriser l'évaluation et l'amélioration

## 📈 Décrypter les Métriques d'Entraînement

#### 🎯 Exemple Concret d'Entraînement

Analysons ligne par ligne ce que nous disent les métriques d'un entraînement CNN réel :

Epoch 1/50  
1563/1563 ━━━━━━━━━━━━━━━━━━━━ 220s 137ms/step - accuracy: 0.3300 - loss: 2.1425 - val\_accuracy: 0.5032 - val\_loss: 1.4824

Epoch 2/50  
1563/1563 ━━━━━━━━━━━━━━━━━━━━ 260s 136ms/step - accuracy: 0.5592 - loss: 1.2421 - val\_accuracy: 0.5507 - val\_loss: 1.3214

Epoch 20/50  
1563/1563 ━━━━━━━━━━━━━━━━━━━━ 265s 139ms/step - accuracy: 0.8310 - loss: 0.4850 - val\_accuracy: 0.8025 - val\_loss: 0.5852

Epoch 21/50  
1563/1563 ━━━━━━━━━━━━━━━━━━━━ 216s 138ms/step - accuracy: 0.8465 - loss: 0.4378 - val\_accuracy: 0.8304 - val\_loss: 0.5089

### 🔍 Anatomie d'une Ligne de Métrique

Epoch 21/50

1563/1563 ━━━━━━━━━━━━━━━━━━━━

216s 138ms/step

accuracy: 0.8465

loss: 0.4378

val\_accuracy: 0.8304

val\_loss: 0.5089

📅 Epoch 21/50

**Époque actuelle :** 21e itération sur 50 prévues

**Signification :** Le modèle a vu 21 fois l'ensemble des données d'entraînement

🔄 1563/1563 Batches

**Progression :** 1563 mini-batches traités sur 1563 total

**Calcul :** Si dataset = 50000 images et batch\_size = 32, alors 50000/32 ≈ 1563 batches

⏱️ 216s 138ms/step

**Temps total :** 216 secondes pour cette époque

**Temps par batch :** 138ms par mini-batch (216s / 1563 batches)

✅ Accuracy: 0.8465

**Précision d'entraînement :** 84.65% des prédictions correctes

**Tendance :** Le modèle apprend bien sur les données d'entraînement

📉 Loss: 0.4378

**Perte d'entraînement :** Mesure de l'erreur du modèle

**Objectif :** Plus cette valeur est basse, mieux c'est

🔍 Val\_accuracy: 0.8304

**Précision de validation :** 83.04% sur données non vues

**Comparaison :** Proche du training accuracy = bon signe

## 📊 Métriques Principales Expliquées

🎯

### Accuracy (Précision)

Pourcentage de prédictions correctes

Accuracy = (Prédictions Correctes) / (Total Prédictions) Accuracy = (TP + TN) / (TP + TN + FP + FN)

**💡 Utilisation :** Métrique principale pour les problèmes équilibrés

**⚠️ Attention :** Peut être trompeuse avec des classes déséquilibrées

📉

### Loss (Perte)

Mesure de l'erreur du modèle

Categorical Crossentropy = -Σ y\_true \* log(y\_pred) Plus la perte est faible, mieux c'est !

**💡 Rôle :** Guide l'optimisation, ce que le modèle cherche à minimiser

**🎯 Objectif :** Perte décroissante et stable

🔍

### Precision (Précision)

Proportion de vrais positifs parmi les positifs prédits

Precision = TP / (TP + FP) "De tous ceux que j'ai dit positifs, combien le sont vraiment ?"

**💡 Important quand :** Les faux positifs coûtent cher

**📧 Exemple :** Détection de spam (éviter de classer un email important comme spam)

🎣

### Recall (Rappel)

Proportion de vrais positifs détectés

Recall = TP / (TP + FN) "De tous les vrais positifs, combien ai-je détectés ?"

**💡 Important quand :** Les faux négatifs coûtent cher

**🏥 Exemple :** Détection de cancer (ne pas rater un vrai cas)

⚖️

### F1-Score

Moyenne harmonique de Precision et Recall

F1 = 2 \* (Precision \* Recall) / (Precision + Recall) Équilibre entre Precision et Recall

**💡 Avantage :** Synthèse en une métrique unique

**🎯 Usage :** Quand Precision et Recall sont également importants

### 🧮 Matrice de Confusion - Comprendre les Métriques

Prédit Positif

Prédit Négatif

Vrai Positif

TP  
✅ Correct

FN  
❌ Manqué

Vrai Négatif

FP  
❌ Fausse alerte

TN  
✅ Correct

## 🔍 Diagnostic des Problèmes d'Entraînement

Symptômes Observés

Diagnostic

Problème

Solutions

• Train accuracy ↗️ 95%  
• Val accuracy 📉 65%  
• Gap croissant

Overfitting

Le modèle mémorise au lieu d'apprendre

Dropout, regularization, plus de données

• Train accuracy 📉 55%  
• Val accuracy 📉 53%  
• Les deux stagnent

Underfitting

Le modèle est trop simple

Modèle plus complexe, plus d'époques

• Train accuracy ↗️ 85%  
• Val accuracy ↗️ 83%  
• Gap stable ~2%

Normal

Apprentissage sain

Continuer l'entraînement

• Loss oscille beaucoup  
• Accuracy monte/descend  
• Pas de tendance claire

Instable

Learning rate trop élevé

Réduire learning rate, scheduler

#### 📊 Simulateur de Courbes d'Entraînement

Cliquez pour voir différents scénarios d'entraînement :

📈 Entraînement Normal 📊 Overfitting 📉 Underfitting 📊 Instabilité

## 🚀 Stratégies d'Amélioration du Modèle

📊 Augmentation des Données

**Quand :** Overfitting, dataset petit

**Techniques :**

*   Rotation, flip, zoom
*   Ajustement luminosité/contraste
*   Bruit aléatoire
*   Mixup, CutMix

🛡️ Régularisation

**Quand :** Overfitting

**Techniques :**

*   Dropout (0.2 - 0.5)
*   L1/L2 regularization
*   Batch Normalization
*   Early Stopping

⚙️ Ajustement Architecture

**Underfitting :** Plus de couches/neurones

**Overfitting :** Architecture plus simple

**Options :**

*   Nombre de filtres
*   Profondeur du réseau
*   Skip connections

📈 Optimisation Learning Rate

**Trop élevé :** Instabilité, divergence

**Trop bas :** Convergence lente

**Solutions :**

*   Learning rate scheduler
*   Adaptive optimizers (Adam)
*   Learning rate finder
*   Cosine annealing

🔄 Transfer Learning

**Quand :** Dataset petit, domaine similaire

**Approches :**

*   Feature extraction
*   Fine-tuning
*   Modèles pré-entraînés
*   Progressive unfreezing

⚡ Optimisation Performance

**Objectif :** Accélérer l'entraînement

**Techniques :**

*   Mixed precision training
*   Batch size optimal
*   Multi-GPU training
*   Gradient accumulation

### 🎯 Guide de Décision Rapide

#### 🤔 "Mon modèle ne marche pas bien, que faire ?"

##### ❌ Si Accuracy < 60% :

1.  Vérifier les données (labels corrects ?)
2.  Augmenter la complexité du modèle
3.  Réduire le learning rate
4.  Plus d'époques d'entraînement
5.  Préprocessing des données

##### ⚠️ Si Gap Train/Val > 10% :

1.  Ajouter du Dropout
2.  Data augmentation
3.  Réduire la complexité
4.  Plus de données
5.  Early stopping

## 🔬 Métriques Avancées pour l'Évaluation

📏

### AUC-ROC

Area Under the Receiver Operating Characteristic Curve

AUC = ∫ TPR d(FPR) de 0 à 1 TPR = Recall = TP/(TP+FN) FPR = FP/(FP+TN)

**💡 Usage :** Classification binaire, évalue tous les seuils

**🎯 Interprétation :** 0.5 = aléatoire, 1.0 = parfait

📊

### Top-K Accuracy

Précision dans les K meilleures prédictions

Top-5 Accuracy = (Vraie classe dans les 5 premières) / Total Utile pour classification avec nombreuses classes

**💡 Exemple :** ImageNet utilise Top-1 et Top-5 accuracy

**🎯 Avantage :** Plus indulgent que l'accuracy stricte

⚖️

### Weighted F1-Score

F1-Score pondéré par la fréquence des classes

Weighted F1 = Σ (nombre\_échantillons\_classe\_i / total) × F1\_classe\_i Compense les déséquilibres de classes

**💡 Usage :** Datasets déséquilibrés

**🎯 Avantage :** Évite que les classes majoritaires dominent

### 📱 Métriques de Production

⚡ Latence (ms)

**Mesure :** Temps de prédiction par image

**Objectifs typiques :**

*   Temps réel : < 33ms (30 FPS)
*   Interactive : < 100ms
*   Batch : < 1s

📦 Taille Modèle (MB)

**Importance :** Déploiement mobile/edge

**Objectifs :**

*   Mobile : < 50MB
*   Edge : < 10MB
*   IoT : < 1MB

🔋 Consommation (Watts)

**Mesure :** Énergie par inférence

**Solutions :**

*   Quantization
*   Pruning
*   Knowledge distillation

## 🎬 Cas Pratiques d'Optimisation

#### 📋 Étude de Cas : Optimisation CIFAR-10

Suivez l'évolution d'un modèle CNN sur CIFAR-10 :

🚀 Modèle Baseline 📊 + Data Augmentation 🛡️ + Régularisation 🏗️ + Architecture Avancée ✨ Résultat Final

### 🔄 Processus d'Amélioration Itératif

#### 📈 Méthodologie Recommandée

1.  **Baseline :** Modèle simple qui fonctionne
2.  **Analyse :** Identifier le problème principal
3.  **Hypothèse :** Choisir UNE amélioration
4.  **Test :** Implémenter et mesurer
5.  **Validation :** Confirmer l'amélioration
6.  **Itération :** Répéter le processus

**⚠️ Erreur Commune :** Changer plusieurs choses à la fois. Il devient impossible de savoir ce qui améliore vraiment le modèle !

## 📋 Résumé du Module 7

### 🎯 Ce que vous avez appris :

*   ✅ **Lecture des métriques :** Interpréter accuracy, loss, val\_accuracy, val\_loss
*   ✅ **Diagnostic :** Identifier overfitting, underfitting, instabilité
*   ✅ **Métriques avancées :** Precision, Recall, F1-Score, AUC-ROC
*   ✅ **Stratégies d'amélioration :** Data augmentation, régularisation, architecture
*   ✅ **Optimisation :** Learning rate, transfer learning, métriques de production
*   ✅ **Méthodologie :** Processus itératif d'amélioration

### 🚀 Prochaines étapes :

Vous maîtrisez maintenant l'évaluation et l'optimisation des CNN ! Utilisez ces connaissances pour :

*   Diagnostiquer rapidement les problèmes d'entraînement
*   Choisir les bonnes métriques selon votre problème
*   Optimiser méthodiquement vos modèles
*   Déployer en production avec confiance

[← Module 6: Projets & Exercices](cnn_module6.html)

**Module 7 (Bonus)**  
Métriques & Optimisation

[🏠 Retour à l'Index](index.html)

// Données pour les cas d'étude const caseStudies = { baseline: { title: "🚀 Modèle Baseline", description: "CNN simple : Conv2D → MaxPool → Conv2D → MaxPool → Dense", metrics: { accuracy: "65%", val\_accuracy: "62%", loss: "1.2", parameters: "50K", training\_time: "5 min" }, problems: \["Underfitting léger", "Performance limitée"\], next: "Ajouter de la complexité et des données" }, augmentation: { title: "📊 + Data Augmentation", description: "Ajout de rotation, flip, zoom, ajustement de luminosité", metrics: { accuracy: "72%", val\_accuracy: "70%", loss: "0.9", parameters: "50K", training\_time: "8 min" }, problems: \["Gap train/val réduit", "Amélioration significative"\], next: "Prévenir l'overfitting potentiel" }, regularization: { title: "🛡️ + Régularisation", description: "Dropout (0.3), Batch Normalization, L2 regularization", metrics: { accuracy: "78%", val\_accuracy: "76%", loss: "0.7", parameters: "52K", training\_time: "10 min" }, problems: \["Modèle stable", "Bon équilibre"\], next: "Améliorer l'architecture" }, architecture: { title: "🏗️ + Architecture Avancée", description: "ResNet blocks, Skip connections, Plus de filtres", metrics: { accuracy: "85%", val\_accuracy: "83%", loss: "0.5", parameters: "180K", training\_time: "15 min" }, problems: \["Excellent équilibre", "Performance compétitive"\], next: "Fine-tuning final" }, final: { title: "✨ Résultat Final", description: "Optimisation learning rate, Early stopping, Ensemble", metrics: { accuracy: "88%", val\_accuracy: "86%", loss: "0.4", parameters: "180K", training\_time: "20 min" }, problems: \["Objectif atteint !", "Prêt pour production"\], next: "Déploiement et monitoring" } }; // Données pour les courbes d'entraînement const trainingCurves = { normal: { title: "📈 Entraînement Normal", description: "Convergence saine avec gap stable entre train et validation", train\_acc: \[0.3, 0.5, 0.65, 0.75, 0.82, 0.86, 0.88, 0.89, 0.90, 0.91\], val\_acc: \[0.35, 0.48, 0.62, 0.72, 0.79, 0.83, 0.85, 0.86, 0.87, 0.88\], characteristics: \[ "Gap train/val stable (~3%)", "Progression continue", "Convergence douce", "Pas de sur-apprentissage" \] }, overfitting: { title: "📊 Overfitting", description: "Le modèle mémorise les données d'entraînement", train\_acc: \[0.3, 0.6, 0.75, 0.85, 0.92, 0.96, 0.98, 0.99, 0.995, 0.999\], val\_acc: \[0.35, 0.55, 0.68, 0.72, 0.70, 0.68, 0.65, 0.63, 0.61, 0.58\], characteristics: \[ "Gap train/val croissant (>40%)", "Train accuracy très élevée", "Val accuracy plafonne puis baisse", "Mémorisation vs apprentissage" \] }, underfitting: { title: "📉 Underfitting", description: "Le modèle est trop simple pour apprendre", train\_acc: \[0.25, 0.28, 0.32, 0.35, 0.38, 0.40, 0.41, 0.42, 0.43, 0.43\], val\_acc: \[0.24, 0.27, 0.31, 0.34, 0.37, 0.39, 0.40, 0.41, 0.42, 0.42\], characteristics: \[ "Performance faible sur les deux", "Progression très lente", "Plateau précoce", "Capacité insuffisante" \] }, unstable: { title: "📊 Instabilité", description: "Learning rate trop élevé, gradients explosent", train\_acc: \[0.1, 0.6, 0.3, 0.8, 0.2, 0.7, 0.4, 0.75, 0.35, 0.65\], val\_acc: \[0.12, 0.55, 0.35, 0.72, 0.25, 0.68, 0.42, 0.70, 0.38, 0.62\], characteristics: \[ "Oscillations importantes", "Pas de convergence claire", "Learning rate trop élevé", "Gradients instables" \] } }; // Explication des éléments de confusion matrix const confusionElements = { tp: { title: "True Positive (TP) - Vrai Positif ✅", description: "Le modèle prédit POSITIF et c'est CORRECT", example: "📧 Email de spam détecté comme spam → ✅ Correct !", impact: "Contribue positivement à Precision et Recall" }, fp: { title: "False Positive (FP) - Faux Positif ❌", description: "Le modèle prédit POSITIF mais c'est FAUX", example: "📧 Email important classé comme spam → ❌ Problématique !", impact: "Diminue la Precision (fausse alerte)" }, fn: { title: "False Negative (FN) - Faux Négatif ❌", description: "Le modèle prédit NÉGATIF mais c'est FAUX", example: "🏥 Cancer non détecté → ❌ Très grave !", impact: "Diminue le Recall (cas manqué)" }, tn: { title: "True Negative (TN) - Vrai Négatif ✅", description: "Le modèle prédit NÉGATIF et c'est CORRECT", example: "📧 Email normal classé comme normal → ✅ Parfait !", impact: "Contribue à la Specificity et Accuracy" } }; // Explication des époques function explainEpoch(epochNum) { // Reset previous selections document.querySelectorAll('.epoch-line').forEach(line => { line.classList.remove('selected'); }); // Select current line event.target.classList.add('selected'); const explanationDiv = document.getElementById('epochExplanation'); let content = ''; if (epochNum === 1) { content = \` <h4>🚀 Analyse Époque 1/50</h4> <p><strong>Situation :</strong> Début d'entraînement, le modèle découvre les données</p> <ul> <li><strong>Accuracy 33% :</strong> Performance aléatoire (CIFAR-10 = 10 classes, hasard = 10%)</li> <li><strong>Val\_accuracy 50% :</strong> Validation meilleure que train (normal au début)</li> <li><strong>Loss élevée (2.14) :</strong> Le modèle fait encore beaucoup d'erreurs</li> <li><strong>220s :</strong> Premier passage, compilation et optimisations</li> </ul> <p><strong>📊 Diagnostic :</strong> Démarrage normal, le modèle apprend les bases</p> \`; } else if (epochNum === 2) { content = \` <h4>📈 Analyse Époque 2/50</h4> <p><strong>Situation :</strong> Première amélioration visible</p> <ul> <li><strong>Accuracy 56% :</strong> +23% d'amélioration, excellent signe</li> <li><strong>Val\_accuracy 55% :</strong> Équilibre train/val, pas d'overfitting</li> <li><strong>Loss 1.24 :</strong> Réduction significative (-0.9)</li> <li><strong>260s :</strong> Temps stable</li> </ul> <p><strong>📊 Diagnostic :</strong> Apprentissage sain, continuer l'entraînement</p> \`; } else if (epochNum === 20) { content = \` <h4>🎯 Analyse Époque 20/50</h4> <p><strong>Situation :</strong> Milieu d'entraînement, performance mature</p> <ul> <li><strong>Accuracy 83% :</strong> Performance élevée, modèle bien entraîné</li> <li><strong>Val\_accuracy 80% :</strong> Gap de 3%, équilibre excellent</li> <li><strong>Loss 0.48 :</strong> Faible, modèle confiant</li> <li><strong>265s :</strong> Temps constant</li> </ul> <p><strong>📊 Diagnostic :</strong> Entraînement optimal, proche de la convergence</p> \`; } else if (epochNum === 21) { content = \` <h4>✨ Analyse Époque 21/50</h4> <p><strong>Situation :</strong> Amélioration continue</p> <ul> <li><strong>Accuracy 84.6% :</strong> +1.6% d'amélioration</li> <li><strong>Val\_accuracy 83% :</strong> +3% d'amélioration, rattrape le train</li> <li><strong>Gap réduit :</strong> 1.6% seulement, excellent équilibre</li> <li><strong>Learning rate :</strong> Probablement réduit automatiquement</li> </ul> <p><strong>📊 Diagnostic :</strong> Entraînement parfait, peut continuer ou s'arrêter</p> \`; } explanationDiv.innerHTML = content; explanationDiv.style.display = 'block'; } // Explication des éléments de la matrice de confusion function explainConfusion(element) { const data = confusionElements\[element\]; const explanationDiv = document.getElementById('confusionExplanation'); explanationDiv.innerHTML = \` <h4>${data.title}</h4> <p><strong>Définition :</strong> ${data.description}</p> <p><strong>Exemple concret :</strong> ${data.example}</p> <p><strong>Impact sur métriques :</strong> ${data.impact}</p> \`; explanationDiv.style.display = 'block'; } // Affichage des courbes d'entraînement function showTrainingCurve(type) { const data = trainingCurves\[type\]; const canvas = document.getElementById('trainingChart'); const ctx = canvas.getContext('2d'); // Clear canvas ctx.clearRect(0, 0, canvas.width, canvas.height); // Set canvas size canvas.width = canvas.offsetWidth; canvas.height = canvas.offsetHeight; const width = canvas.width; const height = canvas.height; const padding = 50; // Draw axes ctx.strokeStyle = '#333'; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(padding, height - padding); ctx.lineTo(width - padding, height - padding); ctx.moveTo(padding, height - padding); ctx.lineTo(padding, padding); ctx.stroke(); // Draw labels ctx.fillStyle = '#333'; ctx.font = '12px Arial'; ctx.fillText('Accuracy', 10, height/2); ctx.fillText('Epochs', width/2, height - 10); // Draw training curve ctx.strokeStyle = '#e74c3c'; ctx.lineWidth = 3; ctx.beginPath(); for (let i = 0; i < data.train\_acc.length; i++) { const x = padding + (i \* (width - 2\*padding) / (data.train\_acc.length - 1)); const y = height - padding - (data.train\_acc\[i\] \* (height - 2\*padding)); if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y); } ctx.stroke(); // Draw validation curve ctx.strokeStyle = '#3498db'; ctx.lineWidth = 3; ctx.beginPath(); for (let i = 0; i < data.val\_acc.length; i++) { const x = padding + (i \* (width - 2\*padding) / (data.val\_acc.length - 1)); const y = height - padding - (data.val\_acc\[i\] \* (height - 2\*padding)); if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y); } ctx.stroke(); // Legend ctx.fillStyle = '#e74c3c'; ctx.fillText('Train Accuracy', width - 150, 30); ctx.fillStyle = '#3498db'; ctx.fillText('Val Accuracy', width - 150, 50); // Show explanation const explanationDiv = document.getElementById('curveExplanation'); explanationDiv.innerHTML = \` <h5 style="color: white;">${data.title}</h5> <p style="margin: 10px 0;">${data.description}</p> <ul style="margin: 10px 0; padding-left: 20px;"> ${data.characteristics.map(char => \`<li>${char}</li>\`).join('')} </ul> \`; explanationDiv.style.display = 'block'; } // Affichage des cas d'étude function showCase(caseType) { const data = caseStudies\[caseType\]; const display = document.getElementById('caseStudyDisplay'); display.innerHTML = \` <div style="color: white;"> <h5 style="color: white; margin-bottom: 15px;">${data.title}</h5> <p style="margin: 15px 0; font-style: italic;">${data.description}</p> <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 15px; margin: 20px 0;"> <div style="background: rgba(255,255,255,0.1); padding: 10px; border-radius: 8px; text-align: center;"> <strong>Accuracy</strong><br> ${data.metrics.accuracy} </div> <div style="background: rgba(255,255,255,0.1); padding: 10px; border-radius: 8px; text-align: center;"> <strong>Val Accuracy</strong><br> ${data.metrics.val\_accuracy} </div> <div style="background: rgba(255,255,255,0.1); padding: 10px; border-radius: 8px; text-align: center;"> <strong>Loss</strong><br> ${data.metrics.loss} </div> <div style="background: rgba(255,255,255,0.1); padding: 10px; border-radius: 8px; text-align: center;"> <strong>Paramètres</strong><br> ${data.metrics.parameters} </div> <div style="background: rgba(255,255,255,0.1); padding: 10px; border-radius: 8px; text-align: center;"> <strong>Temps</strong><br> ${data.metrics.training\_time} </div> </div> <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px; margin: 15px 0;"> <strong>📊 Observations :</strong> <ul style="margin: 10px 0; padding-left: 20px;"> ${data.problems.map(problem => \`<li>${problem}</li>\`).join('')} </ul> </div> <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px;"> <strong>🚀 Prochaine étape :</strong> ${data.next} </div> </div> \`; display.style.display = 'block'; } // Initialize canvas on load document.addEventListener('DOMContentLoaded', () => { // Show normal training curve by default setTimeout(() => showTrainingCurve('normal'), 1000); });
