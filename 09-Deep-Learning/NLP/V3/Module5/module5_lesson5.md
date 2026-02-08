---
title: 'Module 5 - Leçon 5 : Bonnes Pratiques et Debugging'
description: 'Formation NLP - Module 5 - Leçon 5 : Bonnes Pratiques et Debugging'
tags:
  - NLP
  - 09-Deep-Learning
category: 09-Deep-Learning
---

# 🛠️ Leçon 5 : Bonnes Pratiques et Debugging RNN

Même les meilleurs modèles peuvent mal fonctionner ! Apprenez à diagnostiquer et résoudre les problèmes courants avec les RNN : overfitting, underfitting, gradients qui explosent, et bien plus.

## 🎯 Les 3 problèmes principaux et leurs solutions

#### 🚨 Overfitting

**Symptômes :**

*   Loss d'entraînement ↓
*   Loss de validation ↑
*   Écart grandissant
*   Accuracy train >> val

#### 💊 Solutions

*   **Dropout :** 0.2-0.5 sur les couches LSTM
*   **Regularization :** L1/L2 sur les poids
*   **Early stopping :** Patience de 5-10 epochs
*   **Plus de données :** Augmentation
*   **Modèle plus simple :** Moins de couches

#### 🐌 Underfitting

**Symptômes :**

*   Loss train et val hautes
*   Pas d'amélioration
*   Predictions aléatoires
*   Courbe plate

#### 🚀 Solutions

*   **Modèle plus complexe :** Plus de neurones/couches
*   **Learning rate :** Augmenter légèrement
*   **Features :** Améliorer le preprocessing
*   **Architecture :** LSTM au lieu de RNN
*   **Entraînement :** Plus d'epochs

#### 💥 Gradient Problems

**Symptômes :**

*   Loss → NaN ou Inf
*   Gradients très grands
*   Instabilité d'entraînement
*   Convergence impossible

#### 🎯 Solutions

*   **Gradient clipping :** clip\_norm=1.0
*   **Learning rate :** Diminuer à 0.001
*   **Batch normalization :** Stabiliser
*   **LSTM/GRU :** Remplacer RNN vanilla
*   **Initialisation :** Xavier/He uniform

## 📊 Dashboard de monitoring

![Courbes d'apprentissage typiques](https://miro.medium.com/max/1400/1*a61lM8xKF6aF5z3HSpnMHg.png)

Courbes d'apprentissage : Normal vs Overfitting vs Underfitting

Train Loss

0.45

↓ Diminue bien

Val Loss

0.52

↗ Légère augmentation

Gap Train/Val

0.07

✓ Acceptable

Gradient Norm

2.1

✓ Stable

## 🔧 Configuration optimale selon le cas

Paramètre

Dataset petit (<1M)

Dataset moyen (1-10M)

Dataset large (>10M)

**Architecture**

GRU simple

LSTM 1-2 couches

LSTM bidirectionnel

**Hidden Units**

64-128

256-512

512-1024

**Dropout**

0.3-0.5

0.2-0.4

0.1-0.3

**Learning Rate**

0.01

0.001

0.0001

**Batch Size**

16-32

32-64

64-128

**Séquence Max**

50-100

100-200

200-500

## 💻 Code pour le monitoring et debugging

```
import tensorflow as tf
from tensorflow.keras import callbacks
import matplotlib.pyplot as plt

# Callback personnalisé pour monitorer les gradients
class GradientMonitor(callbacks.Callback):
    def on_batch_end(self, batch, logs=None):
        # Calculer la norme des gradients
        gradients = []
        for layer in self.model.layers:
            if hasattr(layer, 'kernel'):
                grad = tf.keras.backend.gradients(self.model.total_loss, layer.kernel)
                if grad[0] is not None:
                    grad_norm = tf.norm(grad[0])
                    gradients.append(grad_norm)
        
        if gradients:
            avg_grad_norm = tf.reduce_mean(gradients)
            if avg_grad_norm > 10.0:  # Seuil d'alerte
                print(f"⚠️ Gradient explosif détecté: {avg_grad_norm:.2f}")

# Configuration complète avec bonnes pratiques
def create_robust_rnn(vocab_size, max_length, embedding_dim=128):
    model = tf.keras.Sequential([
        # Embedding avec masking pour gérer les séquences variables
        tf.keras.layers.Embedding(vocab_size, embedding_dim, 
                                 mask_zero=True, input_length=max_length),
        
        # Dropout sur l'embedding
        tf.keras.layers.Dropout(0.2),
        
        # LSTM avec dropout intégré
        tf.keras.layers.LSTM(256, 
                           dropout=0.3,          # Dropout sur les entrées
                           recurrent_dropout=0.3, # Dropout sur les connexions récurrentes
                           return_sequences=False),
        
        # Couche dense avec régularisation
        tf.keras.layers.Dense(64, activation='relu',
                            kernel_regularizer=tf.keras.regularizers.l2(0.01)),
        tf.keras.layers.Dropout(0.5),
        
        # Sortie
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])
    
    # Optimiseur avec gradient clipping
    optimizer = tf.keras.optimizers.Adam(learning_rate=0.001, clipnorm=1.0)
    
    model.compile(
        optimizer=optimizer,
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    
    return model

# Callbacks essentiels
callbacks_list = [
    # Early stopping avec patience
    tf.keras.callbacks.EarlyStopping(
        monitor='val_loss',
        patience=7,
        restore_best_weights=True
    ),
    
    # Réduction du learning rate
    tf.keras.callbacks.ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=3,
        min_lr=1e-7
    ),
    
    # Sauvegarde du meilleur modèle
    tf.keras.callbacks.ModelCheckpoint(
        'best_model.h5',
        monitor='val_loss',
        save_best_only=True
    ),
    
    # Monitoring des gradients
    GradientMonitor()
]
```

## 📋 Checklist de debugging

#### ✅ Avant l'entraînement

*   Vérifier la forme des données (batch\_size, seq\_length, features)
*   Tester le modèle sur un petit batch
*   Valider le preprocessing (tokenisation, padding)
*   S'assurer que les labels sont corrects
*   Vérifier l'équilibrage des classes

#### ⚡ Pendant l'entraînement

*   Monitorer train/val loss en temps réel
*   Surveiller la norme des gradients
*   Vérifier l'utilisation mémoire GPU
*   Observer les prédictions sur quelques exemples
*   Ajuster les hyperparamètres si nécessaire

#### 🎯 Après l'entraînement

*   Analyser la matrice de confusion
*   Tester sur des exemples hors distribution
*   Vérifier les prédictions sur des cas limites
*   Évaluer la robustesse aux variations
*   Documenter les résultats et insights

## 🚨 Flowchart de résolution de problèmes

**Mon modèle ne converge pas du tout ?**

↓

1\. Réduire le learning rate (÷10)  
2\. Vérifier les données d'entrée  
3\. Simplifier l'architecture

↓

**Overfitting (gap train/val > 0.1) ?**

↓

1\. Augmenter dropout  
2\. Ajouter régularisation  
3\. Plus de données / Early stopping

↓

**Underfitting (loss plateau haut) ?**

↓

1\. Augmenter la capacité du modèle  
2\. Réduire la régularisation  
3\. Améliorer les features

## 🎯 Techniques avancées

### Augmentation de données pour RNN

```
# Techniques d'augmentation spécifiques au texte
def augment_text_data(texts, labels):
    augmented_texts = []
    augmented_labels = []
    
    for text, label in zip(texts, labels):
        # Original
        augmented_texts.append(text)
        augmented_labels.append(label)
        
        # Synonyme replacement (using nltk or spacy)
        synonym_text = replace_with_synonyms(text, prob=0.1)
        augmented_texts.append(synonym_text)
        augmented_labels.append(label)
        
        # Random word deletion
        deleted_text = random_word_deletion(text, prob=0.1)
        augmented_texts.append(deleted_text)
        augmented_labels.append(label)
        
        # Word order swap
        swapped_text = random_word_swap(text, n=2)
        augmented_texts.append(swapped_text)
        augmented_labels.append(label)
    
    return augmented_texts, augmented_labels
```

### Learning Rate Scheduling optimal

```
# Warm-up + Cosine Annealing
def create_lr_schedule(initial_lr=0.001, warmup_epochs=5, total_epochs=50):
    def lr_schedule(epoch):
        if epoch < warmup_epochs:
            # Phase de warm-up
            return initial_lr * (epoch + 1) / warmup_epochs
        else:
            # Cosine annealing
            progress = (epoch - warmup_epochs) / (total_epochs - warmup_epochs)
            return initial_lr * 0.5 * (1 + np.cos(np.pi * progress))
    
    return tf.keras.callbacks.LearningRateScheduler(lr_schedule)
```

### ⚠️ Erreurs communes à éviter

*   **Padding sans masking :** Les tokens de padding influencent l'apprentissage
*   **Séquences trop longues :** Coût computationnel et problèmes de mémoire
*   **Pas de validation holdout :** Impossible de détecter l'overfitting
*   **Learning rate trop élevé :** Le modèle "saute" par-dessus les minima
*   **Batch size trop petit :** Gradients bruités et entraînement instable
*   **Pas de seed random :** Résultats non reproductibles

## 📊 Métriques avancées pour RNN

```
# Métriques personnalisées pour mieux évaluer
def perplexity(y_true, y_pred):
    """Perplexité pour les tâches de langage"""
    cross_entropy = tf.keras.losses.sparse_categorical_crossentropy(y_true, y_pred)
    return tf.exp(tf.reduce_mean(cross_entropy))

def sequence_accuracy(y_true, y_pred):
    """Précision au niveau séquence complète"""
    predicted_sequences = tf.argmax(y_pred, axis=-1)
    correct_sequences = tf.reduce_all(tf.equal(y_true, predicted_sequences), axis=-1)
    return tf.reduce_mean(tf.cast(correct_sequences, tf.float32))

# Compilation avec métriques avancées
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy', perplexity, sequence_accuracy]
)
```

## 📝 Résumé des bonnes pratiques

### 🎯 Points clés à retenir :

*   ✅ **Monitoring :** Surveillez train/val loss en permanence
*   ✅ **Régularisation :** Dropout + Early stopping sont essentiels
*   ✅ **Gradients :** Utilisez gradient clipping avec LSTM/GRU
*   ✅ **Learning rate :** Commencez petit et utilisez des schedulers
*   ✅ **Architecture :** Commencez simple, complexifiez si nécessaire
*   ✅ **Données :** Qualité > Quantité, équilibrage important
*   ✅ **Reproductibilité :** Fixez les seeds pour comparer les expériences

[← Leçon 4 : Applications](module5_lesson4.html) [Module 6 : Transformers →](../module6/index.html)
