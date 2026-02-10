---
title: 'Module 4: Architectures Célèbres des CNN'
description: 'Formation CNN - Module 4: Architectures Célèbres des CNN'
tags:
  - CNN
  - 09-Deep-Learning
category: 09-Deep-Learning
---

# 🏗️ Module 4: Architectures Célèbres des CNN

📚 Niveau: Intermédiaire | ⏱️ Durée: 1h45 | 🎯 Objectif: Comprendre l'évolution des architectures

## 🎯 Évolution Historique des CNN

Ce module explore les architectures qui ont marqué l'histoire des CNN. Chaque architecture a apporté des innovations révolutionnaires qui ont façonné la computer vision moderne.

1998 - LeNet-5

Première architecture CNN pratique de Yann LeCun pour reconnaître les chiffres manuscrits.

2012 - AlexNet

Révolution du deep learning en remportant ImageNet avec ReLU, Dropout et GPU.

2014 - VGG & GoogLeNet

Deux approches : simplicité avec filtres 3×3 vs efficacité avec modules Inception.

2015 - ResNet

Skip connections révolutionnaires permettant des réseaux de 100+ couches.

🧠 LeNet-5 (1998) - Le Pionnier

**LeNet-5** est la première architecture CNN pratique, développée par Yann LeCun pour la reconnaissance de chiffres manuscrits sur le dataset MNIST.

Créateur

Yann LeCun (Bell Labs)

Paramètres

~60,000

Performance

99.2% sur MNIST

Innovation

Première CNN pratique

#### Architecture LeNet-5

Input 32×32×1

→

Conv 5×5

→

Pool 2×2

→

Conv 5×5

→

Pool 2×2

→

Conv 5×5

→

FC 84

→

Output 10

#### 💡 Innovations Fondatrices

*   **Première utilisation systématique des convolutions**
*   **Partage de paramètres sur toute l'image**
*   **Architecture hiérarchique simple**
*   **Sous-échantillonnage progressif**

🚀 AlexNet (2012) - La Révolution

**AlexNet** a révolutionné la computer vision en remportant ImageNet 2012 avec une marge écrasante (15.3% vs 26.2%), relançant l'intérêt mondial pour le deep learning.

Créateurs

Krizhevsky, Sutskever, Hinton

Paramètres

~60 millions

Performance

15.3% top-5 error

Innovation

ReLU + GPU + Dropout

#### Architecture AlexNet

Input 227×227×3

→

Conv 11×11

→

MaxPool

→

Conv 5×5

→

MaxPool

→

3×Conv 3×3

→

FC 4096

→

FC 1000

#### 💡 Innovations Révolutionnaires

*   **ReLU :** Première utilisation massive (remplace tanh/sigmoid)
*   **Dropout :** Régularisation pour éviter le sur-apprentissage
*   **GPU Training :** Première utilisation des GPU
*   **Data Augmentation :** Augmentation artificielle du dataset

📐 VGG (2014) - Simplicité et Profondeur

**VGG** a démontré qu'une architecture simple utilisant exclusivement des filtres 3×3 pouvait atteindre d'excellentes performances grâce à la profondeur.

Créateurs

Simonyan & Zisserman (Oxford)

Paramètres

~138M (VGG-16)

Performance

7.3% top-5 error

Innovation

Filtres 3×3 uniquement

#### Architecture VGG-16

Input 224×224×3

→

2×Conv3×3 (64)

→

MaxPool

→

2×Conv3×3 (128)

→

MaxPool

→

3×Conv3×3 (256)

→

3×Conv3×3 (512)

→

FC 4096

→

FC 1000

#### 💡 Philosophie VGG

*   **Simplicité :** Filtres 3×3 exclusivement
*   **Profondeur :** Démonstration que "plus profond = mieux"
*   **Modularité :** Blocs répétitifs faciles à comprendre
*   **Transfer Learning :** Excellent extracteur de features

🔗 ResNet (2015) - Skip Connections

**ResNet** a révolutionné l'entraînement de réseaux profonds avec les skip connections, permettant des architectures de 100+ couches sans gradient vanishing.

Créateurs

Kaiming He et al. (Microsoft)

Paramètres

~25M (ResNet-50)

Performance

3.6% top-5 error

Innovation

Skip connections

#### Bloc Résiduel

Input x

↓

Conv + BN + ReLU

↓

Conv + BN

↓

+

↓

ReLU

Formule: y = F(x) + x

#### 💡 Révolution ResNet

*   **Skip Connections :** Résout le gradient vanishing
*   **Réseaux ultra-profonds :** Jusqu'à 152 couches
*   **Residual Learning :** Apprendre F(x) au lieu de H(x)
*   **Batch Normalization :** Intégration systématique

## 📊 Comparaison des Architectures

Architecture

Année

Paramètres

ImageNet Top-5

Innovation Principale

**LeNet-5**

1998

60K

N/A (MNIST)

Première CNN pratique

**AlexNet**

2012

60M

15.3%

ReLU + GPU + Dropout

**VGG-16**

2014

138M

7.3%

Filtres 3×3 uniquement

**ResNet-50**

2015

25M

3.6%

Skip connections

## 📋 Résumé du Module 4

### 🎯 Ce que vous avez appris :

*   **LeNet-5 (1998) :** Architecture pionnière, base des CNN modernes
*   **AlexNet (2012) :** Révolution ReLU + GPU + Dropout
*   **VGG (2014) :** Simplicité avec filtres 3×3 exclusifs
*   **ResNet (2015) :** Skip connections pour réseaux ultra-profonds
*   **Critères de choix :** Adapter selon contraintes et objectifs

### 🚀 Prochaine étape :

Le Module 5 explore les applications pratiques : classification, détection d'objets, segmentation, médical, véhicules autonomes, et les défis du déploiement en production.

[← Module 3: Techniques Avancées](cnn_module3.html)

**Module 4 / 6**  
Architectures Célèbres

[Module 5: Applications Pratiques →](cnn_module5.html)

// Animation d'entrée document.addEventListener('DOMContentLoaded', () => { const elements = document.querySelectorAll('.architecture-box, .timeline-item'); elements.forEach((element, index) => { element.style.opacity = '0'; element.style.transform = 'translateY(30px)'; element.style.transition = 'all 0.6s ease'; setTimeout(() => { element.style.opacity = '1'; element.style.transform = 'translateY(0)'; }, index \* 200); }); });
