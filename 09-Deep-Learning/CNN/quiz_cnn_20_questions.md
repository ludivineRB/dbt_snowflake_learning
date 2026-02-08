---
title: Quiz CNN - 20 questions
description: Formation CNN - Quiz CNN - 20 questions
tags:
  - CNN
  - 09-Deep-Learning
category: 09-Deep-Learning
---
 Quiz CNN - 20 questions body { font-family: Arial, sans-serif; background: linear-gradient(135deg, #667eea, #764ba2); color: #333; padding: 20px; } .quiz-container { background: #fff; padding: 30px; max-width: 900px; margin: auto; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.2); } h1 { text-align: center; color: #2c3e50; } .question { margin-top: 25px; } .answers label { display: block; margin-bottom: 8px; cursor: pointer; } button { margin-top: 20px; padding: 12px 25px; font-size: 16px; background: #3498db; color: white; border: none; border-radius: 8px; cursor: pointer; } button:hover { background: #2980b9; } .result { font-size: 18px; font-weight: bold; margin-top: 25px; } .correction { background: #f1f1f1; padding: 10px; border-left: 4px solid #27ae60; margin-top: 10px; border-radius: 5px; } .incorrect { border-left-color: #e74c3c; }

# 🧠 Quiz CNN - 20 Questions avec Correction

**1\. Que signifie "profondeur" dans un réseau de neurones profond ?**

 Le nombre d'images traitées Le nombre de couches dans le réseau La taille de l'image d'entrée

**2\. Quel est le rôle d’un filtre dans une convolution ?**

 Extraire des motifs (bords, textures...) Appliquer une rotation à l’image Colorier l’image en noir et blanc

**3\. À quoi sert la Batch Normalization ?**

 Réduire la taille des images Stabiliser l'entraînement et accélérer la convergence Supprimer les doublons dans les données

**4\. Quelle est l'innovation principale de ResNet ?**

 Les filtres 7×7 Les connexions résiduelles (skip connections) Le max pooling adaptatif

**5\. Quelle est la chaîne de traitement typique dans une application CNN ?**

 Modèle → Données → Prétraitement → Résultat Données → Prétraitement → Modèle → Post-traitement → Résultat Résultat → Filtrage → Normalisation → Image

**6\. Quel est l'avantage principal du Max Pooling dans un CNN ?**

 Augmenter la taille des images Réduire la complexité et extraire les caractéristiques dominantes Ajouter de la couleur aux images

**7\. Que fait la fonction d'activation ReLU ?**

 Supprime les pixels blancs Remplace les valeurs négatives par zéro Multiplie tous les pixels par 2

**8\. Pourquoi utilise-t-on la fonction softmax en sortie d’un CNN pour la classification ?**

 Pour normaliser l’image Pour transformer les sorties en probabilités Pour augmenter la résolution

**9\. À quoi sert le Flatten dans un CNN ?**

 Aplatir les pixels noirs Transformer une image en noir et blanc Transformer une matrice 2D en vecteur 1D

**10\. Qu'est-ce qu'une couche Dense ?**

 Une couche qui supprime des neurones Une couche totalement connectée entre neurones Une couche qui ajoute du bruit

**11\. Quel est l’effet d’un taux de Dropout trop élevé ?**

 Surapprentissage Sous-apprentissage Rien du tout

**12\. Quelle technique permet de stabiliser l’apprentissage dans les CNN ?**

 Data augmentation Batch Normalization Convolution 1x1

**13\. Quelle architecture utilise des connexions résiduelles ?**

 AlexNet ResNet VGG

**14\. Dans quel domaine les CNN sont-ils le plus utilisés ?**

 Texte Images Audio

**15\. Quel est l'intérêt des couches de normalisation ?**

 Rendre l’image plus belle Réduire la variance entre lots et stabiliser l'apprentissage Créer des filtres flous

Valider

const corrections = { c1: "✅ Bonne réponse : Le nombre de couches dans le réseau (profondeur).", c2: "✅ Bonne réponse : Le filtre extrait des motifs comme des bords ou textures.", c3: "✅ Bonne réponse : La Batch Normalization stabilise l'entraînement.", c4: "✅ Bonne réponse : Les connexions résiduelles permettent des réseaux très profonds.", c5: "✅ Bonne réponse : Données → Prétraitement → Modèle → Post-traitement → Résultat.", c6: "✅ Bonne réponse : Le Max Pooling réduit la complexité tout en conservant les caractéristiques essentielles.", c7: "✅ Bonne réponse : ReLU remplace toutes les valeurs négatives par 0, ce qui introduit de la non-linéarité.", c8: "✅ Bonne réponse : Softmax transforme les scores en probabilités pour chaque classe.", c9: "✅ Bonne réponse : Flatten convertit une matrice 2D en vecteur 1D pour la couche dense.", c10: "✅ Bonne réponse : Une couche Dense connecte tous les neurones d’entrée à tous les neurones de sortie.", c11: "✅ Bonne réponse : Un Dropout trop élevé désactive trop de neurones, menant à un sous-apprentissage.", c12: "✅ Bonne réponse : La Batch Normalization stabilise l’apprentissage et accélère la convergence.", c13: "✅ Bonne réponse : ResNet introduit les connexions résiduelles (skip connections).", c14: "✅ Bonne réponse : Les CNN sont principalement utilisés pour le traitement d’images.", c15: "✅ Bonne réponse : Elles réduisent la variance d’activation entre lots et facilitent l’apprentissage.", }; function calculateScore() { const form = document.forms\["quizForm"\]; let score = 0; for (let i = 1; i <= 20; i++) { const value = form\["q" + i\]?.value; const correctionDiv = document.getElementById("c" + i); if (value === "1") { score++; correctionDiv.innerText = corrections\["c" + i\]; correctionDiv.classList.remove("incorrect"); } else { correctionDiv.innerText = "❌ Mauvaise réponse. " + corrections\["c" + i\]; correctionDiv.classList.add("incorrect"); } } document.getElementById("result").innerText = \`🎯 Score final : ${score}/20\`; }
