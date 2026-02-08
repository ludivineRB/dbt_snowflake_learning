---
title: 14_pratique_finetuning
tags:
  - LLM
  - 10-Large-Language-Model
category: 10-Large-Language-Model
---
# Pratique du Fine-tuning de LLM avec LoRA et Unsloth

Ce document est un guide pratique pour le fine-tuning d'un Grand Modèle de Langage (LLM) en utilisant la technique LoRA (Low-Rank Adaptation) et la bibliothèque Unsloth. Unsloth optimise le processus de fine-tuning pour une efficacité maximale en termes de vitesse et de consommation de mémoire, rendant le fine-tuning de LLMs accessible même sur des GPU grand public.

## 1. Introduction au Fine-tuning et LoRA

Le fine-tuning est le processus d'adaptation d'un modèle pré-entraîné à une tâche ou un domaine spécifique en le réentraînant sur un jeu de données plus petit et ciblé. Traditionnellement, cela peut être très coûteux en ressources.

**LoRA (Low-Rank Adaptation)** est une technique de fine-tuning efficace en paramètres (PEFT) qui permet d'adapter un grand modèle de langage avec beaucoup moins de ressources. Au lieu de fine-tuner tous les paramètres du modèle, LoRA n'introduit qu'un petit nombre de paramètres supplémentaires "entraînables" dans le modèle. Le modèle de base reste gelé, et seules ces petites matrices d'adaptation sont mises à jour.

**Avantages de LoRA :**
- **Réduction des coûts :** Moins de mémoire GPU et de temps de calcul.
- **Stockage efficace :** Les adaptateurs LoRA sont très petits, permettant de stocker de nombreuses versions fine-tunées sans dupliquer le modèle de base.
- **Prévention de l'oubli catastrophique :** Le modèle de base étant gelé, ses connaissances générales sont préservées.

## 2. Préparation de l'environnement

### 2.1. Installation des bibliothèques nécessaires

Nous commençons par installer toutes les bibliothèques Python requises pour ce processus.

[![Fine-tuning LLama 3 with Unsloth](https://img.youtube.com/vi/pTaSDVz0gok/0.jpg)](https://www.youtube.com/watch?v=pTaSDVz0gok)

```python
# Installation des bibliothèques nécessaires pour le fine-tuning
# unsloth : Framework optimisé pour le fine-tuning efficace des LLMs
# trl : Transformers Reinforcement Learning pour l'entraînement supervisé
# peft : Parameter-Efficient Fine-Tuning pour les adaptateurs LoRA
# accelerate : Accélération du training PyTorch (multi-GPU, mixed precision)
# bitsandbytes : Quantification 8-bit et 4-bit pour économiser la mémoire GPU
!pip install unsloth trl peft accelerate bitsandbytes
```

### 2.2. Vérification de la disponibilité du GPU

Le fine-tuning des LLM est une tâche très gourmande en calcul. Une carte graphique (GPU) est indispensable pour des performances acceptables.

```python
# Importe la bibliothèque PyTorch, qui est le framework de deep learning sous-jacent.
import torch

# Vérifier si CUDA (la plateforme de calcul parallèle de NVIDIA pour GPU) est disponible.
# Si False, le fine-tuning sera extrêmement lent ou impossible sur des modèles de cette taille.
print(f"CUDA available: {torch.cuda.is_available()}")

# Afficher le nom du GPU s'il est disponible, sinon afficher "None"
# Cela permet de confirmer quel GPU sera utilisé pour l'entraînement
print(f"GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'None'}")
```

## 3. Chargement et préparation des données

### 3.1. Chargement du jeu de données

Nous chargeons ici le jeu de données qui servira à fine-tuner notre modèle. Ce jeu de données est au format JSON et contient des paires `input`/`output` pour une tâche d'extraction d'informations.

```python
# Importer la bibliothèque json pour manipuler les données JSON
import json

# Charger le fichier JSON contenant les données d'entraînement
# Ce fichier contient des exemples au format {"input": "...", "output": {...}}
# où input est le texte HTML et output est l'objet JSON extrait
# Le chemin doit être absolu pour garantir la portabilité.
file = json.load(open("/Users/guillaume/workplace/Formations/LLM/01 - API/NOUVEAU_COURS/code/data/data_a_entrainer.json", "r"))

# Afficher le deuxième exemple (index 1) pour vérifier le format des données
print(file[1])
```

### 3.2. Préparation des données pour l'entraînement

Les données brutes doivent être transformées en un format que le modèle peut comprendre et sur lequel il peut apprendre. Pour les modèles "instruct", un format `### Input: ... ### Output: ...` est courant.

```python
from datasets import Dataset
import json # Assurez-vous que json est importé si ce n'est pas déjà fait

# Fonction pour formater chaque exemple dans le format attendu par le modèle
def format_prompt(example):
    # Format standard pour l'instruction fine-tuning :
    # ### Input: [le texte HTML à analyser]
    # ### Output: [le JSON extrait attendu]
    # <|endoftext|> marque la fin de l'exemple pour le modèle
    return f"### Input: {example['input']}\n### Output: {json.dumps(example['output'])}<|endoftext|>"

# Appliquer le formatage à tous les exemples du dataset
# Cela crée une liste de chaînes de texte formatées pour l'entraînement
formatted_data = [format_prompt(item) for item in file]

# Créer un objet Dataset de Hugging Face à partir des données formatées
# Cela permet d'utiliser les fonctionnalités d'optimisation du framework
dataset = Dataset.from_dict({"text": formatted_data})

# Affiche un exemple du dataset formaté pour vérification.
print(dataset[0]["text"])
```

## 4. Configuration et Fine-tuning du Modèle

### 4.1. Chargement du modèle de base et du Tokenizer

Nous chargeons ici le modèle pré-entraîné que nous allons fine-tuner, ainsi que son tokenizer associé. Nous utilisons une version quantifiée pour économiser la mémoire.

```python
from unsloth import FastLanguageModel
import torch

# Nom du modèle pré-entraîné à utiliser
# Phi-3-mini est un modèle compact de Microsoft, optimisé pour l'efficacité
# La version "bnb-4bit" est déjà quantifiée en 4 bits pour économiser la mémoire
model_name = "unsloth/Phi-3-mini-4k-instruct-bnb-4bit"

# Longueur maximale des séquences (tokens) que le modèle peut traiter
# 2048 est un bon compromis entre performance et utilisation mémoire
max_seq_length = 2048  

# Type de données pour les calculs (None = détection automatique)
# Le framework choisira automatiquement float16 ou bfloat16 selon le GPU
dtype = None  

# Chargement du modèle et du tokenizer
# Le tokenizer convertit le texte en tokens que le modèle peut comprendre
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name=model_name,
    max_seq_length=max_seq_length,
    dtype=dtype,
    load_in_4bit=True,  # Charge le modèle en quantification 4-bit pour réduire l'utilisation mémoire
)
```

### 4.2. Ajout des adaptateurs LoRA au modèle

C'est ici que la magie de LoRA opère. Nous ajoutons de petits modules entraînables au modèle gelé.

```python
# Ajoute les adaptateurs LoRA au modèle de base.
# Le modèle original (model) est gelé, et seuls les petits adaptateurs LoRA seront entraînés.
model = FastLanguageModel.get_peft_model(
    model,
    # Le "rang" de LoRA. C'est un hyperparamètre clé.
    # Un rang plus élevé (par exemple, 64, 128) signifie plus de paramètres entraînables
    # et potentiellement une plus grande capacité d'adaptation, mais aussi plus de mémoire
    # et de temps de calcul. Un rang plus faible (par exemple, 8, 16) est plus léger.
    # Le choix dépend de la complexité de la tâche et des ressources disponibles.
    r=64,  
    
    # Modules du transformeur à adapter avec LoRA
    # Ce sont les couches d'attention et les couches feed-forward
    target_modules=[
        "q_proj", "k_proj", "v_proj", "o_proj",  # Couches d'attention (Query, Key, Value, Output projections)
        "gate_proj", "up_proj", "down_proj",     # Couches du MLP (Multi-Layer Perceptron)
    ], # Ces modules sont les cibles typiques pour l'injection des adaptateurs LoRA dans les modèles Transformer.
       # Ils sont responsables des transformations linéaires des données.
    
    # Facteur d'échelle LoRA (généralement 2x le rang)
    # Contrôle l'importance des adaptations LoRA par rapport au modèle original
    lora_alpha=128,  
    
    # Dropout pour la régularisation (0 = pas de dropout, optimisé pour la performance)
    lora_dropout=0,  
    
    # Configuration du biais (none = pas de biais supplémentaire, plus rapide)
    bias="none",     
    
    # Utilise la version optimisée d'Unsloth pour le gradient checkpointing
    # Économise la mémoire en recalculant certains gradients au lieu de les stocker
    # Cela est crucial pour entraîner de grands modèles sur des GPU avec moins de VRAM.
    use_gradient_checkpointing="unsloth",  
    
    # Graine aléatoire pour la reproductibilité
    random_state=3407,
    
    # RSLora : technique de stabilisation du rang (désactivée ici)
    use_rslora=False,  
    
    # LoftQ : technique de quantification avancée (non utilisée ici)
    loftq_config=None, 
)
```

### 4.3. Configuration des arguments d'entraînement

Nous définissons ici tous les hyperparamètres et les stratégies pour le processus d'entraînement.

```python
from trl import SFTTrainer
from transformers import TrainingArguments

# Configure l'entraîneur pour le Supervised Fine-Tuning (SFT).
# SFTTrainer est une abstraction de haut niveau de la bibliothèque TRL.
trainer = SFTTrainer(
    model=model,             # Le modèle (avec les adaptateurs LoRA) à entraîner.
    tokenizer=tokenizer,     # Le tokenizer associé au modèle.
    train_dataset=dataset,   # Le jeu de données d'entraînement préparé.
    dataset_text_field="text", # Le nom du champ dans le Dataset qui contient le texte d'entraînement.
    max_seq_length=max_seq_length, # Longueur maximale des séquences pour l'entraînement.
    dataset_num_proc=2,      # Nombre de processus à utiliser pour le prétraitement du dataset.
                             # Peut accélérer la préparation des données.
    
    # Arguments d'entraînement détaillés
    args=TrainingArguments(  
        # Taille du batch par GPU (nombre d'exemples traités simultanément)
        per_device_train_batch_size=2,
        
        # Accumulation de gradients : simule un batch plus grand
        # Batch effectif = per_device_train_batch_size * gradient_accumulation_steps
        # Ici : 2 * 4 = 8 exemples par étape de mise à jour des poids.
        gradient_accumulation_steps=4,  
        
        # Nombre d'étapes de warmup (montée progressive du learning rate)
        warmup_steps=10,             
        
        # Nombre d'époques (passages complets sur le dataset)
        num_train_epochs=3,          
        
        # Taux d'apprentissage (vitesse d'adaptation du modèle)
        learning_rate=2e-4,          
        
        # Utilisation de float16 ou bfloat16 selon le support du GPU
        # bfloat16 est préféré sur les GPU récents (A100, etc.) pour une meilleure stabilité numérique.
        fp16=not torch.cuda.is_bf16_supported(),
        bf16=torch.cuda.is_bf16_supported(),     
        
        # Fréquence de logging (affichage des métriques)
        logging_steps=25,            
        
        # Optimiseur AdamW en 8-bit pour économiser la mémoire
        optim="adamw_8bit",          
        
        # Régularisation par weight decay pour prévenir le surapprentissage
        weight_decay=0.01,           
        
        # Scheduler du learning rate (décroissance linéaire après le warmup)
        lr_scheduler_type="linear",  
        
        # Graine pour la reproductibilité
        seed=3407,                   
        
        # Dossier de sortie pour les checkpoints du modèle et les logs
        output_dir="outputs",        
        
        # Stratégie de sauvegarde du modèle : à la fin de chaque époque
        save_strategy="epoch",       
        
        # Ne conserve que les 2 derniers checkpoints pour économiser de l'espace
        save_total_limit=2,          
        
        # Optimisation de la mémoire pour le dataloader (désactivée ici)
        dataloader_pin_memory=False, 
        
        # Désactive l'intégration avec des outils de suivi comme Weights & Biases
        report_to="none",            
    ),
)
```

### 4.4. Lancement de l'entraînement

Cette ligne exécute le processus de fine-tuning.

```python
# Lance le processus d'entraînement du modèle.
# C'est l'étape la plus longue et la plus gourmande en ressources.
# Les logs d'entraînement (perte, taux d'apprentissage, etc.) seront affichés
# en fonction de la valeur de `logging_steps` définie précédemment.
trainer_stats = trainer.train()

# Durant l'entraînement, vous verrez :
# - La perte (loss) qui devrait diminuer progressivement
# - Le taux d'apprentissage (learning rate) qui suit le scheduler
# - Les étapes d'entraînement et le temps écoulé
# - Les checkpoints sauvegardés à chaque époque
```

## 5. Évaluation et Test du Modèle

### 5.1. Test du modèle fine-tuné sur un nouvel exemple

Après l'entraînement, nous testons le modèle pour voir comment il se comporte sur de nouvelles entrées.

```python
# Test du modèle fine-tuné sur un nouvel exemple

# Activer le mode inférence pour des prédictions 2x plus rapides
# Cela désactive certaines fonctionnalités d'entraînement non nécessaires
FastLanguageModel.for_inference(model) 

# Exemple de test : extraire des informations produit d'un HTML
# Le format suit celui utilisé pendant l'entraînement
messages = [
    {"role": "user", "content": "Extract the product information:\n<div class='product'><h2>iPad Air</h2><span class='price'>$1344</span><span class='category'>audio</span><span class='brand'>Dell</span></div>"},
]

# Appliquer le template de chat du modèle pour formater correctement l'entrée
# Cela ajoute les tokens spéciaux nécessaires au modèle
inputs = tokenizer.apply_chat_template(
    messages,
    tokenize=True,  # Convertir en tokens
    add_generation_prompt=True,  # Ajouter le prompt de génération
    return_tensors="pt",  # Retourner des tenseurs PyTorch
).to("cuda")  # Envoyer sur le GPU

# Générer la réponse du modèle
outputs = model.generate(
    input_ids=inputs,
    max_new_tokens=256,  # Nombre maximum de nouveaux tokens à générer
    use_cache=True,  # Utiliser le cache KV pour accélérer la génération
    temperature=0.7,  # Contrôle la créativité (0=déterministe, 1=créatif)
    do_sample=True,  # Activer l'échantillonnage probabiliste
    top_p=0.9,  # Nucleus sampling : ne considère que les tokens les plus probables
)

# Décoder les tokens générés en texte lisible et afficher
response = tokenizer.batch_decode(outputs)[0]
print(response)
```

### 5.2. Évaluation du modèle sur un ensemble de test (Fonctions d'évaluation)

Pour une évaluation plus robuste, il est essentiel de tester le modèle sur un ensemble de données de test séparé. Le notebook inclut des fonctions pour extraire le JSON des réponses du modèle et calculer des métriques.

```python
# Évaluation du modèle sur un ensemble de test
import json
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
import numpy as np

# Fonction pour extraire le JSON de la réponse du modèle
def extract_json_from_response(response):
    """Extrait l'objet JSON de la réponse du modèle"""
    try:
        # Chercher le JSON entre ### Output: et la fin
        start = response.find("### Output:")
        if start != -1:
            json_str = response[start + len("### Output:"):].strip()
            # Enlever les tokens de fin s'ils existent
            json_str = json_str.replace("<|endoftext|>", "").strip()
            return json.loads(json_str)
    except:
        pass
    return None

# Fonction d'évaluation sur un ensemble de données
def evaluate_model(model, tokenizer, test_data, max_samples=50):
    """
    Évalue le modèle sur des données de test
    
    Args:
        model: Le modèle fine-tuné
        tokenizer: Le tokenizer associé
        test_data: Liste d'exemples {"input": ..., "output": ...}
        max_samples: Nombre maximum d'échantillons à évaluer
    """
    predictions = []
    ground_truths = []
    errors = []
    
    # Limiter le nombre d'échantillons pour l'évaluation
    eval_samples = test_data[:max_samples]
    
    print(f"Évaluation sur {len(eval_samples)} échantillons...")
    
    for i, example in enumerate(eval_samples):
        # Préparer le prompt
        prompt = f"Extract the product information:\n{example['input']}"
        messages = [{"role": "user", "content": prompt}]
        
        # Tokenizer et générer
        inputs = tokenizer.apply_chat_template(
            messages,
            tokenize=True,
            add_generation_prompt=True,
            return_tensors="pt",
        ).to("cuda")
        
        # Générer avec température basse pour plus de déterminisme
        outputs = model.generate(
            input_ids=inputs,
            max_new_tokens=256,
            temperature=0.1, # Température basse pour des résultats plus déterministes lors de l'évaluation
            do_sample=True,
            top_p=0.9,
        )
        
        # Décoder la réponse
        response = tokenizer.decode(outputs[0], skip_special_tokens=False)
        
        # Extraire le JSON prédit
        predicted_json = extract_json_from_response(response)
        
        # Ajouter aux listes pour le calcul des métriques
        predictions.append(predicted_json)
        ground_truths.append(example['output'])
        
        if predicted_json is None:
            errors.append(f"Erreur de parsing JSON pour l'exemple {i}: {response}")

    print(f"\nNombre d'erreurs de parsing JSON: {len(errors)}")
    for error in errors:
        print(error)
    
    return predictions, ground_truths, errors

# Exécuter l'évaluation (assurez-vous que 'file' est votre jeu de données complet)
# Vous pouvez diviser 'file' en train/test si ce n'est pas déjà fait.
# Pour cet exemple, nous utilisons 'file' comme données de test.
predictions, ground_truths, errors = evaluate_model(model, tokenizer, file, max_samples=50)
```

### 5.3. Calcul des métriques détaillées

Ces fonctions permettent de calculer la précision pour chaque champ JSON extrait, ainsi que la correspondance exacte de l'objet JSON complet.

```python
# Calcul des métriques détaillées pour chaque champ
def calculate_field_metrics(predictions, ground_truths):
    """
    Calcule les métriques de précision pour chaque champ JSON
    """
    fields = ['name', 'price', 'category', 'manufacturer'] # Assurez-vous que ces champs correspondent à votre JSON
    metrics = {}
    
    for field in fields:
        correct = 0
        total = len(predictions)
        
        for pred, truth in zip(predictions, ground_truths):
            # Vérifier si le champ existe dans les deux
            if pred and truth and field in pred and field in truth:
                # Comparer les valeurs (insensible à la casse pour les strings)
                pred_val = str(pred[field]).lower() if isinstance(pred[field], str) else pred[field]
                truth_val = str(truth[field]).lower() if isinstance(truth[field], str) else truth[field]
                
                if pred_val == truth_val:
                    correct += 1
            elif (pred is None or field not in pred) and (field not in truth):
                # Les deux n'ont pas le champ ou la prédiction est None, et la vérité non plus, c'est correct
                correct += 1
        
        accuracy = correct / total if total > 0 else 0
        metrics[field] = {
            'correct': correct,
            'total': total,
            'accuracy': accuracy * 100
        }
    
    # Calculer l'exactitude complète (tous les champs corrects)
    exact_matches = 0
    for pred, truth in zip(predictions, ground_truths):
        if pred == truth: # Comparaison directe des objets JSON
            exact_matches += 1
    
    metrics['exact_match'] = {
        'correct': exact_matches,
        'total': len(predictions),
        'accuracy': (exact_matches / len(predictions) * 100) if predictions else 0
    }
    
    return metrics

# Calculer les métriques si nous avons des prédictions
if predictions:
    metrics = calculate_field_metrics(predictions, ground_truths)
    
    print("\n=== Métriques par champ ===")
    for field, values in metrics.items():
        if field != 'exact_match':
            print(f"Champ '{field}': {values['accuracy']:.1f}% ({values['correct']}/{values['total']})")
    
    print(f"\nExactitude complète (tous les champs corrects): {metrics['exact_match']['accuracy']:.1f}% ({metrics['exact_match']['correct']}/{metrics['exact_match']['total']})")
else:
    print("Aucune prédiction à évaluer.")
```

### 5.4. Visualisation des résultats

Une visualisation aide à comprendre rapidement les performances du modèle.

```python
# Visualisation des résultats avec matplotlib
import matplotlib.pyplot as plt

# Créer un graphique des métriques si nous avons des résultats
if 'metrics' in locals() and metrics:
    # Préparer les données pour le graphique
    fields = [k for k in metrics.keys() if k != 'exact_match']
    accuracies = [metrics[f]['accuracy'] for f in fields]
    
    # Ajouter la correspondance exacte
    fields.append('Exact Match')
    accuracies.append(metrics['exact_match']['accuracy'])
    
    # Créer le graphique à barres
    plt.figure(figsize=(10, 6))
    bars = plt.bar(fields, accuracies, color=['skyblue', 'lightgreen', 'lightcoral', 'lightyellow', 'mediumpurple'])
    
    # Ajouter les valeurs sur les barres
    for bar, acc in zip(bars, accuracies):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{acc:.1f}%', ha='center', va='bottom')
    
    plt.title('Précision du modèle par champ', fontsize=16)
    plt.xlabel('Champs', fontsize=12)
    plt.ylabel('Précision (%)', fontsize=12)
    plt.ylim(0, 110)  # Pour avoir de l'espace pour les labels
    plt.grid(axis='y', alpha=0.3)
    
    # Rotation des labels si nécessaire
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

# Afficher un résumé des performances
print("\n=== Résumé des performances ===")
if predictions:
    # Calculer la précision moyenne des champs (hors exact_match)
    avg_field_accuracy = sum([metrics[f]['accuracy'] for f in ['name', 'price', 'category', 'manufacturer']]) / len(['name', 'price', 'category', 'manufacturer'])
    print(f"Précision moyenne par champ: {avg_field_accuracy:.1f}%")
    
    # Calculer le taux de parsing JSON réussi
    successful_parses = sum(1 for p in predictions if p is not None)
    print(f"Taux de parsing JSON réussi: {(successful_parses / len(predictions) * 100):.1f}%")
    print(f"\nLe modèle a été évalué sur {len(predictions)} exemples.")
else:
    print("Aucune prédiction réussie - vérifiez le format de sortie du modèle.")
```

### 5.5. Test interactif du modèle

Cette section permet de tester le modèle avec des exemples HTML personnalisés.

```python
# Test interactif du modèle avec vos propres exemples HTML
def test_custom_html(html_input):
    """
    Teste le modèle sur un HTML personnalisé
    
    Args:
        html_input: String contenant le HTML à analyser
    """
    # Préparer le prompt
    prompt = f"Extract the product information:\n{html_input}"
    messages = [{"role": "user", "content": prompt}]
    
    # Tokenizer
    inputs = tokenizer.apply_chat_template(
        messages,
        tokenize=True,
        add_generation_prompt=True,
        return_tensors="pt",
    ).to("cuda")
    
    # Générer
    outputs = model.generate(
        input_ids=inputs,
        max_new_tokens=256,
        temperature=0.1, # Température basse pour des résultats plus déterministes
        do_sample=True,
        top_p=0.9,
    )
    
    # Décoder
    response = tokenizer.decode(outputs[0], skip_special_tokens=False)
    
    # Extraire le JSON
    predicted_json = extract_json_from_response(response)
    
    print("HTML d'entrée:")
    print(html_input)
    print("\nRéponse du modèle:")
    print(response[response.find("### Output:"):] if "### Output:" in response else response)
    print("\nJSON extrait:")
    print(json.dumps(predicted_json, indent=2) if predicted_json else "Erreur d'extraction JSON")
    
    return predicted_json

# Exemples de test personnalisés
print("=== Tests sur des exemples personnalisés ===\n")

# Test 1: Cas simple
html1 = '''<div class="product">\n    <h1>MacBook Pro</h1>\n    <p class="price">$2499</p>\n    <span class="category">Electronics</span>\n    <div class="brand">Apple</div>\n</div>'''

print("Test 1 - Cas simple:")
result1 = test_custom_html(html1)

print("\n" + "="*50 + "\n")

# Test 2: Cas avec structure différente
html2 = '''<article>\n    <header>iPhone 15 Pro</header>\n    <div>Price: <strong>$999</strong></div>\n    <footer>Category: Smartphones | Brand: Apple</footer>\n</article>'''

print("Test 2 - Cas avec structure différente:")
result2 = test_custom_html(html2)

print("\n" + "="*50 + "\n")

# Test 3: Cas avec informations manquantes ou différentes
html3 = '''<section class="item">\n    <h3 class="item-name">Sony WH-1000XM5</h3>\n    <p class="item-price">Cost: $349</p>\n    {/* No category or brand mentioned */}\n</section>'''

print("Test 3 - Cas avec informations manquantes:")
result3 = test_custom_html(html3)
```

## 6. Sauvegarde et Déploiement du Modèle

### 6.1. Sauvegarde du modèle au format GGUF

Le format GGUF est idéal pour le déploiement local du modèle sur des outils comme Ollama ou `llama.cpp`.

```python
# Sauvegarde du modèle au format GGUF (GPT-Generated Unified Format)
# GGUF est un format binaire optimisé pour l'exécution de modèles sur CPU/GPU avec llama.cpp

# Sauvegarder le modèle fine-tuné en format GGUF quantifié
# quantization_method="q4_k_m" : quantification 4-bit avec méthode K-means
# Cela réduit considérablement la taille du modèle (environ 75% de réduction)
# tout en préservant la majeure partie de la qualité
model.save_pretrained_gguf("gguf_model", tokenizer, quantization_method="q4_k_m")
```

### 6.2. Téléchargement du fichier GGUF (spécifique à Google Colab)

Cette cellule est utile uniquement si vous exécutez le notebook sur Google Colab et que vous souhaitez télécharger le modèle généré sur votre machine locale. Si vous travaillez en local, cette cellule n'est pas nécessaire.

```python
# Téléchargement du fichier GGUF (spécifique à Google Colab)
from google.colab import files
import os

# Lister tous les fichiers GGUF dans le dossier de sauvegarde
gguf_files = [f for f f in os.listdir("gguf_model") if f.endswith(".gguf")]

# Si des fichiers GGUF existent, télécharger le premier
if gguf_files:
    # Construire le chemin complet du fichier
    gguf_file = os.path.join("gguf_model", gguf_files[0])
    print(f"Downloading: {gguf_file}")
    
    # Déclencher le téléchargement dans le navigateur
    # Note : Cette fonction ne fonctionne que dans Google Colab
    files.download(gguf_file)
```

## Conclusion

Ce guide a couvert les étapes essentielles du fine-tuning d'un LLM avec LoRA et Unsloth, de la préparation des données à l'évaluation et la sauvegarde du modèle. Le fine-tuning est une technique puissante pour adapter les modèles de langage à des tâches spécifiques, et LoRA rend ce processus beaucoup plus accessible.


voici d'autre source  Fine-Tune a LLM

[![Fine-Tune Llama 2 with LoRA](https://img.youtube.com/vi/SPNaP4ik9a4/0.jpg)](https://www.youtube.com/watch?v=SPNaP4ik9a4)

[![RAFT Explained](https://img.youtube.com/vi/rqyczEvh3D4/0.jpg)](https://www.youtube.com/watch?v=rqyczEvh3D4)
