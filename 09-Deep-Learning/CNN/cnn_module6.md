---
title: 'Module 6: Projets et Exercices Pratiques'
description: 'Formation CNN - Module 6: Projets et Exercices Pratiques'
tags:
  - CNN
  - 09-Deep-Learning
category: 09-Deep-Learning
---

# 💻 Module 6: Projets et Exercices Pratiques

📚 Niveau: Tous niveaux | ⏱️ Durée: 3h+ | 🎯 Objectif: Maîtriser par la pratique

## 🎯 Mise en Pratique des CNN

Ce module final vous propose des projets concrets pour consolider vos connaissances. Chaque projet est accompagné de code complet, d'explications détaillées et de suggestions d'amélioration.

#### 📋 Objectifs de ce Module

*   Implémenter un CNN from scratch
*   Maîtriser le transfer learning
*   Optimiser les performances
*   Déployer un modèle
*   Analyser les résultats

🖼️

### Projet 1: Classification CIFAR-10

Construire un CNN pour classifier 10 catégories d'images

Débutant

#### 🎯 Description du Projet

CIFAR-10 contient 60,000 images 32×32 en couleur réparties en 10 classes : avions, automobiles, oiseaux, chats, cerfs, chiens, grenouilles, chevaux, navires, camions.

##### 📊 Spécifications

*   **Dataset :** 50,000 images d'entraînement + 10,000 de test
*   **Objectif :** Atteindre >80% d'accuracy
*   **Contraintes :** Modèle < 5M paramètres
*   **Temps :** Entraînement < 30 minutes

```
# Architecture de base pour CIFAR-10
import tensorflow as tf
from tensorflow.keras import layers, models

def create_cifar10_cnn():
    model = models.Sequential([
        # Bloc 1
        layers.Conv2D(32, (3,3), activation='relu', input_shape=(32, 32, 3)),
        layers.BatchNormalization(),
        layers.Conv2D(32, (3,3), activation='relu'),
        layers.MaxPooling2D((2,2)),
        layers.Dropout(0.25),
        
        # Bloc 2
        layers.Conv2D(64, (3,3), activation='relu'),
        layers.BatchNormalization(),
        layers.Conv2D(64, (3,3), activation='relu'),
        layers.MaxPooling2D((2,2)),
        layers.Dropout(0.25),
        
        # Bloc 3
        layers.Conv2D(128, (3,3), activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.25),
        
        # Classification
        layers.Flatten(),
        layers.Dense(512, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.5),
        layers.Dense(10, activation='softmax')
    ])
    
    return model
```

#### ✅ Étapes du Projet

*   Charger et explorer le dataset CIFAR-10
*   Préprocesser les données (normalisation)
*   Implémenter l'architecture CNN
*   Configurer l'entraînement (optimizer, loss)
*   Ajouter data augmentation
*   Entraîner et monitorer les métriques
*   Évaluer sur le test set
*   Analyser les erreurs (matrice de confusion)

🔄

### Projet 2: Transfer Learning - Chats vs Chiens

Utiliser un modèle pré-entraîné pour classifier chats et chiens

Intermédiaire

#### 🎯 Description du Projet

Utiliser ResNet50 pré-entraîné sur ImageNet pour classifier des images de chats et chiens avec un petit dataset personnalisé.

##### 📊 Avantages du Transfer Learning

*   **Données limitées :** Excellent avec peu d'exemples
*   **Entraînement rapide :** Réutilise features pré-apprises
*   **Performance élevée :** Modèles déjà optimisés
*   **Moins de ressources :** Pas besoin de GPU puissant

```
# Transfer Learning avec ResNet50
import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras import layers, models

def create_transfer_model():
    # Charger ResNet50 pré-entraîné (sans la couche finale)
    base_model = ResNet50(
        weights='imagenet',
        include_top=False,
        input_shape=(224, 224, 3)
    )
    
    # Geler les couches pré-entraînées
    base_model.trainable = False
    
    # Ajouter les couches de classification
    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.BatchNormalization(),
        layers.Dropout(0.5),
        layers.Dense(128, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.3),
        layers.Dense(1, activation='sigmoid')  # Binaire: chat=0, chien=1
    ])
    
    return model, base_model
```

#### ✅ Étapes du Transfer Learning

*   Préparer le dataset (images chats/chiens)
*   Redimensionner les images (224×224)
*   Charger ResNet50 pré-entraîné
*   Geler les couches convolutionnelles
*   Ajouter classifieur personnalisé
*   Entraîner avec learning rate faible
*   Fine-tuning (optionnel)
*   Comparer performances vs from scratch

⚡

### Projet 3: Optimisation et Déploiement

Pipeline complet : entraînement, optimisation, déploiement

Avancé

#### 🎯 Objectifs Avancés

*   **Hyperparameter tuning :** Grid search, Bayesian optimization
*   **Model compression :** Quantization, pruning
*   **Deployment :** TensorFlow Lite, ONNX
*   **Monitoring :** MLflow, TensorBoard

```
# Pipeline d'optimisation automatisée
import optuna
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau

def objective(trial):
    # Hyperparamètres à optimiser
    lr = trial.suggest_loguniform('lr', 1e-5, 1e-2)
    dropout = trial.suggest_uniform('dropout', 0.2, 0.7)
    filters_1 = trial.suggest_int('filters_1', 16, 64)
    filters_2 = trial.suggest_int('filters_2', 32, 128)
    
    # Créer et entraîner le modèle
    model = create_optimized_model(filters_1, filters_2, dropout)
    model.compile(
        optimizer=tf.keras.optimizers.Adam(lr),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    # Callbacks intelligents
    callbacks = [
        EarlyStopping(patience=5, restore_best_weights=True),
        ReduceLROnPlateau(factor=0.5, patience=3)
    ]
    
    history = model.fit(
        train_data, validation_data=val_data,
        epochs=50, callbacks=callbacks, verbose=0
    )
    
    return max(history.history['val_accuracy'])
```

#### ✅ Pipeline Complet

*   Setup MLflow pour tracking
*   Hyperparameter optimization (Optuna)
*   Model ensembling
*   Model compression (quantization)
*   Export TensorFlow Lite
*   API REST avec FastAPI
*   Tests de performance
*   Monitoring en production

## 🛠️ Ressources et Outils

#### 📊 Datasets

*   CIFAR-10/100
*   Fashion-MNIST
*   Oxford Pets
*   Food-101

#### 🧠 Modèles Pré-entraînés

*   ResNet50/101
*   EfficientNet
*   MobileNetV2
*   VGG16/19

#### 📈 Monitoring

*   TensorBoard
*   MLflow
*   Weights & Biases
*   Neptune

#### 🚀 Déploiement

*   TensorFlow Serving
*   FastAPI
*   Docker
*   Kubernetes

## 💡 Conseils et Bonnes Pratiques

#### 🎯 Méthodologie de Développement

*   **Start Simple :** Commencez toujours par un modèle de base qui fonctionne
*   **Une Amélioration à la Fois :** Changez un seul élément pour isoler les effets
*   **Validation Rigoureuse :** Séparez bien train/validation/test
*   **Documentation :** Notez chaque expérience et ses résultats
*   **Reproductibilité :** Fixez les seeds pour reproduire les résultats
*   **Monitoring :** Surveillez les métriques en temps réel

```
# Template de projet bien structuré
project/
├── data/
│   ├── raw/              # Données brutes
│   ├── processed/        # Données préprocessées
│   └── external/         # Données externes
├── models/
│   ├── trained/          # Modèles entraînés
│   └── architectures/    # Définitions d'architectures
├── notebooks/
│   ├── exploration/      # EDA et expérimentations
│   └── experiments/      # Tests et validations
├── src/
│   ├── data/            # Scripts de données
│   ├── models/          # Modèles et entraînement
│   ├── evaluation/      # Métriques et évaluation
│   └── deployment/      # Déploiement et API
├── tests/               # Tests unitaires
├── requirements.txt     # Dépendances
└── README.md           # Documentation
```

## 📋 Résumé du Module 6

### 🎯 Compétences Acquises :

*   ✅ **Implémentation pratique :** CNN from scratch et transfer learning
*   ✅ **Optimisation :** Hyperparameters, compression, déploiement
*   ✅ **Bonnes pratiques :** Structure de projet, monitoring, tests
*   ✅ **Pipeline complet :** De l'entraînement à la production

### 🚀 Prochaines étapes :

Félicitations ! Vous maîtrisez maintenant les CNN de A à Z. Pour aller plus loin :

*   Explorez les architectures récentes (Vision Transformers, ConvNeXt)
*   Spécialisez-vous dans un domaine (médical, automotive, etc.)
*   Contribuez à des projets open source
*   Participez à des compétitions (Kaggle, DrivenData)

[← Module 5: Applications Pratiques](cnn_module5.html)

**Module 6 / 6**  
Projets & Exercices

[🎁 Module Bonus 7: Métriques & Optimisation →](cnn_module7.html)

// Fonction pour cocher/décocher les éléments de checklist function toggleCheck(element) { element.classList.toggle('completed'); // Animation légère element.style.transform = 'scale(0.95)'; setTimeout(() => { element.style.transform = 'scale(1)'; }, 150); // Sauvegarder l'état (optionnel) const listId = element.parentElement.id; const itemIndex = Array.from(element.parentElement.children).indexOf(element); const storageKey = \`checklist\_${listId}\_${itemIndex}\`; if (element.classList.contains('completed')) { localStorage.setItem(storageKey, 'completed'); } else { localStorage.removeItem(storageKey); } } // Charger l'état des checklists au chargement de la page function loadChecklistState() { const checklists = \['moduleObjectives', 'cifar10Steps', 'transferSteps', 'advancedSteps'\]; checklists.forEach(listId => { const list = document.getElementById(listId); if (list) { Array.from(list.children).forEach((item, index) => { const storageKey = \`checklist\_${listId}\_${index}\`; if (localStorage.getItem(storageKey) === 'completed') { item.classList.add('completed'); } }); } }); } // Animation d'entrée pour les cartes de projet function animateProjectCards() { const cards = document.querySelectorAll('.project-card'); cards.forEach((card, index) => { card.style.opacity = '0'; card.style.transform = 'translateY(50px)'; card.style.transition = 'all 0.6s ease'; setTimeout(() => { card.style.opacity = '1'; card.style.transform = 'translateY(0)'; }, index \* 300); }); } // Calculer et afficher le progrès global function updateProgress() { const checklists = \['moduleObjectives', 'cifar10Steps', 'transferSteps', 'advancedSteps'\]; let totalItems = 0; let completedItems = 0; checklists.forEach(listId => { const list = document.getElementById(listId); if (list) { const items = list.children; totalItems += items.length; completedItems += Array.from(items).filter(item => item.classList.contains('completed') ).length; } }); const progressPercent = totalItems > 0 ? (completedItems / totalItems) \* 100 : 0; // Mettre à jour la barre de progression si elle existe const progressFill = document.querySelector('.progress-fill'); if (progressFill) { progressFill.style.width = \`${Math.max(progressPercent, 100)}%\`; } // Afficher un message de félicitations si tout est terminé if (progressPercent === 100) { showCongratulations(); } } // Afficher un message de félicitations function showCongratulations() { const existingMessage = document.getElementById('congratulations'); if (existingMessage) return; // Ne pas dupliquer const congratsDiv = document.createElement('div'); congratsDiv.id = 'congratulations'; congratsDiv.style.cssText = \` position: fixed; top: 20px; right: 20px; background: linear-gradient(135deg, #00b894, #00a085); color: white; padding: 20px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); z-index: 1000; max-width: 300px; animation: slideIn 0.5s ease; \`; congratsDiv.innerHTML = \` <h4 style="margin: 0 0 10px 0;">🎉 Félicitations !</h4> <p style="margin: 0;">Vous avez terminé tous les projets ! Vous maîtrisez maintenant les CNN.</p> <button onclick="this.parentElement.remove()" style=" background: rgba(255,255,255,0.2); border: none; color: white; padding: 5px 10px; border-radius: 5px; cursor: pointer; margin-top: 10px; float: right; ">Fermer</button> \`; // Ajouter l'animation CSS const style = document.createElement('style'); style.textContent = \` @keyframes slideIn { from { transform: translateX(100%); opacity: 0; } to { transform: translateX(0); opacity: 1; } } \`; document.head.appendChild(style); document.body.appendChild(congratsDiv); // Auto-remove après 10 secondes setTimeout(() => { if (congratsDiv.parentElement) { congratsDiv.remove(); } }, 10000); } // Code highlight interactif function highlightCode() { const codeBlocks = document.querySelectorAll('.code-block'); codeBlocks.forEach(block => { block.addEventListener('click', () => { // Copier le code dans le presse-papier const text = block.textContent; navigator.clipboard.writeText(text).then(() => { // Feedback visuel const originalBg = block.style.background; block.style.background = '#27ae60'; block.style.transition = 'background 0.3s ease'; setTimeout(() => { block.style.background = originalBg; }, 1000); // Notification const notification = document.createElement('div'); notification.textContent = 'Code copié !'; notification.style.cssText = \` position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background: #27ae60; color: white; padding: 10px 20px; border-radius: 5px; z-index: 2000; animation: fadeOut 2s ease forwards; \`; document.body.appendChild(notification); setTimeout(() => notification.remove(), 2000); }); }); }); } // Système de tips contextuels function showTips() { const tips = \[ { selector: '.project-card.beginner', tip: '💡 Conseil : Commencez toujours par ce projet pour bien comprendre les bases' }, { selector: '.project-card.intermediate', tip: '🚀 Astuce : Le transfer learning peut vous faire gagner des heures d\\'entraînement' }, { selector: '.project-card.advanced', tip: '⚡ Pro tip : L\\'optimisation automatique peut améliorer vos modèles de 5-10%' } \]; tips.forEach((tipData, index) => { const element = document.querySelector(tipData.selector); if (element) { setTimeout(() => { const tipDiv = document.createElement('div'); tipDiv.style.cssText = \` position: absolute; top: -40px; left: 20px; background: #2c3e50; color: white; padding: 8px 12px; border-radius: 20px; font-size: 0.9rem; box-shadow: 0 5px 15px rgba(0,0,0,0.2); z-index: 100; animation: tipFade 4s ease forwards; max-width: 250px; \`; tipDiv.textContent = tipData.tip; element.style.position = 'relative'; element.appendChild(tipDiv); // Supprimer après 4 secondes setTimeout(() => { if (tipDiv.parentElement) { tipDiv.remove(); } }, 4000); }, index \* 2000); } }); // Ajouter l'animation CSS pour les tips const style = document.createElement('style'); style.textContent = \` @keyframes tipFade { 0% { opacity: 0; transform: translateY(10px); } 20% { opacity: 1; transform: translateY(0); } 80% { opacity: 1; transform: translateY(0); } 100% { opacity: 0; transform: translateY(-10px); } } @keyframes fadeOut { 0% { opacity: 1; } 100% { opacity: 0; } } \`; document.head.appendChild(style); } // Observer pour mettre à jour le progrès quand on coche des éléments function setupProgressObserver() { const checklists = document.querySelectorAll('.checklist ul'); checklists.forEach(list => { const observer = new MutationObserver(() => { updateProgress(); }); observer.observe(list, { attributes: true, attributeFilter: \['class'\], subtree: true }); }); } // Initialisation au chargement de la page document.addEventListener('DOMContentLoaded', () => { loadChecklistState(); animateProjectCards(); highlightCode(); setupProgressObserver(); updateProgress(); // Afficher les tips après un délai setTimeout(showTips, 3000); }); // Sauvegarder l'état avant de quitter la page window.addEventListener('beforeunload', () => { // Le localStorage se charge automatiquement de la sauvegarde console.log('État des projets sauvegardé'); });
