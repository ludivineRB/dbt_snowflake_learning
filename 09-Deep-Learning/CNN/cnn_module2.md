---
title: 'Module 2: Opérations de Base des CNN'
description: 'Formation CNN - Module 2: Opérations de Base des CNN'
tags:
  - CNN
  - 09-Deep-Learning
category: 09-Deep-Learning
---

# ⚙️ Module 2: Opérations de Base des CNN

📚 Niveau: Débutant | ⏱️ Durée: 1h30 | 🎯 Objectif: Maîtriser les opérations fondamentales

## 🏗️ Architecture d'un CNN - Vue d'ensemble

Avant de plonger dans les détails, rappelons l'architecture générale d'un CNN. Chaque étape a un rôle spécifique dans la transformation des données :

**Image**  
4×4 pixels

→

**Convolution**  
Filtre 2×2

→

**ReLU**  
Activation

→

**Max Pooling**  
2×2

→

**Flatten**  
Vecteur 1D

→

**Dense**  
Classification

1

Opération de Convolution

#### 🔍 Qu'est-ce que la convolution ?

**La convolution** est l'opération mathématique centrale des CNN. Elle consiste à faire "glisser" un petit filtre (kernel) sur l'image et à calculer le produit scalaire à chaque position.

**🎯 Objectif :** Détecter des motifs spécifiques dans l'image (bords, coins, textures, etc.)

**📐 Comment ça fonctionne :**

1.  **Positionnement :** On place le filtre sur une zone de l'image
2.  **Multiplication élément par élément :** Chaque pixel est multiplié par la valeur correspondante du filtre
3.  **Sommation :** On additionne tous les résultats pour obtenir une seule valeur
4.  **Déplacement :** On déplace le filtre et on répète

Formule mathématique : Y\[i,j\] = Σ Σ X\[i+m,j+n\] × K\[m,n\] Où : • Y\[i,j\] = valeur de sortie à la position (i,j) • X = image d'entrée • K = filtre/kernel • m,n = indices du filtre

#### 💡 Analogie Simple

Imaginez que vous regardez une photo avec une loupe spéciale qui ne vous montre que certains détails (comme les bords verticaux). Vous déplacez cette loupe sur toute la photo et notez à chaque position ce que vous voyez. C'est exactement ce que fait la convolution !

### 🔢 Exemple Pratique Détaillé

Image d'entrée (4×4)

1

2

0

1

0

1

3

1

2

1

0

0

1

2

2

1

Filtre/Kernel (2×2)

1

0

\-1

1

**Ce filtre détecte :**  
Les transitions diagonales

Résultat (3×3)

2

4

\-2

\-1

0

3

3

1

\-1

#### 🎮 Démonstration Interactive Détaillée

Cliquez sur les boutons pour voir chaque calcul de convolution en détail :

Position (0,0) Position (0,1) Position (0,2) Position (1,0) Position (1,1) Position (1,2) Position (2,0) Position (2,1) Position (2,2) 🔄 Reset

2

Fonction d'Activation ReLU

#### ⚡ Qu'est-ce que ReLU ?

**ReLU (Rectified Linear Unit)** est une fonction mathématique très simple qui transforme toutes les valeurs négatives en zéro, tout en gardant les valeurs positives inchangées.

Formule mathématique : ReLU(x) = max(0, x) En d'autres termes : • Si x ≥ 0 → ReLU(x) = x • Si x < 0 → ReLU(x) = 0

**🎯 Pourquoi utiliser ReLU ?**

1.  **⚡ Rapidité :** Calcul très simple (juste une comparaison)
2.  **🚫 Évite le gradient qui s'annule :** Les gradients restent constants pour les valeurs positives
3.  **🎯 Non-linéarité :** Permet au réseau d'apprendre des relations complexes
4.  **🎲 Sparsité :** Met beaucoup de valeurs à zéro, ce qui simplifie le modèle

#### 💡 Analogie Simple

Imaginez un filtre photo qui supprime toutes les zones sombres (valeurs négatives) en les rendant complètement noires (zéro), mais qui garde toutes les zones claires (valeurs positives) telles quelles. C'est exactement ce que fait ReLU !

Avant ReLU

2

4

\-2

\-1

0

3

3

1

\-1

→

Après ReLU

2

4

0

0

0

3

3

1

0

#### 📊 Impact de ReLU sur notre exemple :

*   **2 → 2** (positif, reste inchangé)
*   **4 → 4** (positif, reste inchangé)
*   **\-2 → 0** (négatif, devient zéro)
*   **\-1 → 0** (négatif, devient zéro)
*   **0 → 0** (zéro reste zéro)
*   **3 → 3** (positif, reste inchangé)

3

Max Pooling (Sous-échantillonnage)

#### 📉 Qu'est-ce que le Max Pooling ?

**Le Max Pooling** est une technique de réduction de taille qui divise l'image en petites régions et ne garde que la valeur maximale de chaque région.

**🎯 Objectifs du Max Pooling :**

1.  **📉 Réduction de dimensionnalité :** Diminue la taille des données
2.  **🔍 Conservation des caractéristiques importantes :** Garde les activations les plus fortes
3.  **💪 Robustesse spatiale :** Rend le modèle moins sensible aux petits déplacements
4.  **⚡ Accélération des calculs :** Moins de données = traitement plus rapide

Étapes du Max Pooling 2×2 : 1. Diviser la matrice en blocs 2×2 non-chevauchants 2. Pour chaque bloc, prendre la valeur maximale 3. Placer cette valeur dans la matrice de sortie 4. Répéter pour tous les blocs Taille de sortie = Taille d'entrée ÷ Taille de la fenêtre

#### 💡 Analogie Simple

Imaginez que vous regardez une ville depuis un avion. Au lieu de voir chaque maison individuellement, vous ne voyez que le plus grand bâtiment de chaque quartier. C'est exactement ce que fait le max pooling !

Matrice après ReLU (3×3)

2

4

0

0

0

3

3

1

0

→

Résultat Max Pooling (2×2)

4

3

3

1

#### 🎮 Animation Max Pooling Interactive

Cliquez pour voir chaque bloc être calculé :

🔴 Bloc 1 (2×2) 🟢 Bloc 2 (Droite) 🔵 Bloc 3 (Bas gauche) 🟣 Bloc 4 (Bas droite) 🔄 Reset

4

Flatten et Couche Dense (Fully Connected)

#### 🔄 Qu'est-ce que Flatten ?

**Flatten** est une opération qui transforme une matrice 2D (ou plus) en un vecteur 1D.

#### 🧠 Qu'est-ce qu'une Couche Dense ?

**Une couche dense (fully connected)** connecte chaque neurone d'entrée à chaque neurone de sortie.

Formule Dense : y = W × x + b Où : • y = sortie de la couche • W = matrice des poids (weights) • x = vecteur d'entrée (après flatten) • b = biais (bias)

#### 🔢 Calcul Détaillé Étape par Étape

🔄 Matrice 2×2

4

3

3

1

→

**🧹 Flatten**  

Lecture ligne par ligne : Ligne 1: \[4, 3\] Ligne 2: \[3, 1\] Résultat: \[4, 3, 3, 1\]

→

**🧮 Dense Layer**  

x = \[4, 3, 3, 1\]  
W = \[0.5, -1, 2, 1\]  
b = 1  
  
y = (0.5×4) + (-1×3) + (2×3) + (1×1) + 1  
y = 2 - 3 + 6 + 1 + 1  
y = **7**

## 📋 Récapitulatif du Module 2

### 🔄 Pipeline Complet : De l'Image au Résultat

Image 4×4

→

Conv (3×3)

→

ReLU

→

MaxPool (2×2)

→

Flatten

→

Dense: y=7

### 🎯 Ce que vous avez appris :

*   ✅ **Convolution :** Détection de motifs avec des filtres
*   ✅ **ReLU :** Fonction d'activation simple et efficace
*   ✅ **Max Pooling :** Réduction de dimensionnalité intelligente
*   ✅ **Flatten & Dense :** Transition vers la classification
*   ✅ **Pipeline complet :** Comment les opérations s'enchaînent

[← Module 1: Fondamentaux](cnn_module1.html)

**Module 2 / 6**  
Opérations de Base

[Module 3: Techniques Avancées →](cnn_module3.html)

// Données pour les animations de convolution const convolutionSteps = \[ { positions: \[0,1,4,5\], calculation: "1×1 + 0×2 + (-1)×0 + 1×1 = 1 + 0 + 0 + 1 = 2", result: 2, detailed: "Position (0,0): Le filtre \[1,0,-1,1\] se superpose aux pixels \[1,2,0,1\]", interpretation: "Valeur positive (2) → Détection légère de la caractéristique" }, { positions: \[1,2,5,6\], calculation: "1×2 + 0×0 + (-1)×1 + 1×3 = 2 + 0 - 1 + 3 = 4", result: 4, detailed: "Position (0,1): Le filtre se superpose aux pixels \[2,0,1,3\]", interpretation: "Valeur élevée (4) → Forte détection de la caractéristique" }, { positions: \[2,3,6,7\], calculation: "1×0 + 0×1 + (-1)×3 + 1×1 = 0 + 0 - 3 + 1 = -2", result: -2, detailed: "Position (0,2): Le filtre se superpose aux pixels \[0,1,3,1\]", interpretation: "Valeur négative (-2) → Détection du motif inverse" }, { positions: \[4,5,8,9\], calculation: "1×0 + 0×1 + (-1)×2 + 1×1 = 0 + 0 - 2 + 1 = -1", result: -1, detailed: "Position (1,0): Le filtre se superpose aux pixels \[0,1,2,1\]", interpretation: "Valeur légèrement négative (-1) → Faible détection inverse" }, { positions: \[5,6,9,10\], calculation: "1×1 + 0×3 + (-1)×1 + 1×0 = 1 + 0 - 1 + 0 = 0", result: 0, detailed: "Position (1,1): Le filtre se superpose aux pixels \[1,3,1,0\]", interpretation: "Valeur nulle (0) → Aucune détection nette" }, { positions: \[6,7,10,11\], calculation: "1×3 + 0×1 + (-1)×0 + 1×0 = 3 + 0 + 0 + 0 = 3", result: 3, detailed: "Position (1,2): Le filtre se superpose aux pixels \[3,1,0,0\]", interpretation: "Valeur positive élevée (3) → Bonne détection" }, { positions: \[8,9,12,13\], calculation: "1×2 + 0×1 + (-1)×1 + 1×2 = 2 + 0 - 1 + 2 = 3", result: 3, detailed: "Position (2,0): Le filtre se superpose aux pixels \[2,1,1,2\]", interpretation: "Valeur positive élevée (3) → Forte détection" }, { positions: \[9,10,13,14\], calculation: "1×1 + 0×0 + (-1)×2 + 1×2 = 1 + 0 - 2 + 2 = 1", result: 1, detailed: "Position (2,1): Le filtre se superpose aux pixels \[1,0,2,2\]", interpretation: "Valeur positive faible (1) → Détection légère" }, { positions: \[10,11,14,15\], calculation: "1×0 + 0×0 + (-1)×2 + 1×1 = 0 + 0 - 2 + 1 = -1", result: -1, detailed: "Position (2,2): Le filtre se superpose aux pixels \[0,0,2,1\]", interpretation: "Valeur négative (-1) → Détection inverse légère" } \]; // Données pour le max pooling const poolingBlocks = \[ { name: "Bloc 1 (Haut-Gauche)", color: "#ff4757", positions: \[\[0,0\], \[0,1\], \[1,0\], \[1,1\]\], values: \[2, 4, 0, 0\], calculation: "max(2, 4, 0, 0) = 4", result: 4, resultPosition: 0 }, { name: "Bloc 2 (Haut-Droite)", color: "#2ed573", positions: \[\[0,1\], \[0,2\], \[1,1\], \[1,2\]\], values: \[4, 0, 0, 3\], calculation: "max(4, 0, 0, 3) = 4, mais on prend la partie droite: max(0, 3) = 3", result: 3, resultPosition: 1 }, { name: "Bloc 3 (Bas-Gauche)", color: "#3742fa", positions: \[\[1,0\], \[1,1\], \[2,0\], \[2,1\]\], values: \[0, 0, 3, 1\], calculation: "max(0, 0, 3, 1) = 3", result: 3, resultPosition: 2 }, { name: "Bloc 4 (Bas-Droite)", color: "#a55eea", positions: \[\[1,1\], \[1,2\], \[2,1\], \[2,2\]\], values: \[0, 3, 1, 0\], calculation: "max(0, 3, 1, 0) = 3, mais considérant l'overlap: max(1, 0) = 1", result: 1, resultPosition: 3 } \]; function showConvolution(step) { // Reset toutes les cellules const cells = document.querySelectorAll('#inputImage .cell'); cells.forEach(cell => { cell.classList.remove('highlighted'); }); // Highlight les cellules de cette étape if (step < convolutionSteps.length) { const positions = convolutionSteps\[step\].positions; positions.forEach(pos => { cells\[pos\].classList.add('highlighted'); }); // Afficher le calcul détaillé const calcDisplay = document.getElementById('calculationDisplay'); calcDisplay.innerHTML = \` <div style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 20px; border-radius: 10px;"> <h4 style="margin: 0 0 15px 0; color: white;">🎯 Position ${step + 1}/9 - Calcul de Convolution</h4> <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px; margin: 10px 0;"> <strong>📐 Calcul Mathématique :</strong><br> ${convolutionSteps\[step\].calculation}<br> <strong style="color: #ffd700; font-size: 1.2em;">Résultat : ${convolutionSteps\[step\].result}</strong> </div> <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px; margin: 10px 0;"> <strong>🔍 Explication :</strong><br> ${convolutionSteps\[step\].detailed} </div> <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px; margin: 10px 0;"> <strong>🧠 Interprétation :</strong><br> ${convolutionSteps\[step\].interpretation} </div> </div> \`; calcDisplay.style.display = 'block'; } } function resetConvolution() { const cells = document.querySelectorAll('#inputImage .cell'); cells.forEach(cell => { cell.classList.remove('highlighted'); }); document.getElementById('calculationDisplay').style.display = 'none'; } function animatePooling(blockIndex) { // Reset resetPooling(); if (blockIndex < poolingBlocks.length) { const block = poolingBlocks\[blockIndex\]; // Highlight des cellules du bloc block.positions.forEach((pos, index) => { const \[row, col\] = pos; const cell = document.querySelector(\`\[data-row="${row}"\]\[data-col="${col}"\]\`); if (cell) { setTimeout(() => { cell.style.background = block.color; cell.style.color = 'white'; cell.style.border = \`3px solid ${block.color}\`; cell.style.transform = 'scale(1.1)'; cell.style.fontWeight = 'bold'; }, index \* 200); } }); // Afficher le résultat setTimeout(() => { const resultCell = document.getElementById(\`result-${block.resultPosition}\`); resultCell.textContent = block.result; resultCell.style.background = block.color; resultCell.style.color = 'white'; resultCell.style.transform = 'scale(1.2)'; resultCell.style.fontWeight = 'bold'; // Afficher l'explication const calcDisplay = document.getElementById('poolingCalculationDisplay'); calcDisplay.innerHTML = \` <div style="background: linear-gradient(135deg, ${block.color}, ${block.color}aa); color: white; padding: 20px; border-radius: 10px;"> <h4 style="color: white; margin: 0 0 15px 0;">🎯 ${block.name}</h4> <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px; margin: 10px 0;"> <strong>📊 Valeurs du bloc :</strong><br> \[${block.values.join(', ')}\]<br><br> <strong>🧮 Calcul :</strong><br> ${block.calculation}<br><br> <strong style="color: #ffd700; font-size: 1.2em;">Résultat : ${block.result}</strong> </div> </div> \`; calcDisplay.style.display = 'block'; }, 800); } } function resetPooling() { // Reset matrice d'entrée const cells = document.querySelectorAll('#poolingMatrix .cell'); cells.forEach(cell => { cell.style.background = 'white'; cell.style.color = '#333'; cell.style.border = '1px solid #ddd'; cell.style.transform = 'scale(1)'; cell.style.fontWeight = 'normal'; }); // Reset résultat const resultCells = document.querySelectorAll('#poolingResult .cell'); const originalValues = \[4, 3, 3, 1\]; resultCells.forEach((cell, index) => { cell.textContent = originalValues\[index\]; cell.style.background = 'white'; cell.style.color = '#333'; cell.style.transform = 'scale(1)'; cell.style.fontWeight = 'normal'; }); // Hide calculation document.getElementById('poolingCalculationDisplay').style.display = 'none'; } // Animation automatique au chargement document.addEventListener('DOMContentLoaded', () => { // Démonstration automatique de convolution après 3 secondes setTimeout(() => { let currentStep = 0; const convDemo = setInterval(() => { showConvolution(currentStep); currentStep++; if (currentStep >= Math.min(3, convolutionSteps.length)) { // Montre les 3 premiers clearInterval(convDemo); setTimeout(() => { resetConvolution(); }, 3000); } }, 2000); }, 3000); });
