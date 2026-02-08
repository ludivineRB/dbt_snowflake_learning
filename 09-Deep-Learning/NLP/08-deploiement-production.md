# 08 - Déploiement en Production

[← 07 - BERT/GPT](07-bert-gpt.md) | [🏠 Accueil](README.md)

---

## 🚀 Industrialiser le NLP

### 🏗️ Architecture Microservices
Utilisation de **FastAPI** ou Flask pour créer des endpoints prédictifs rapides.

### ⚡ Optimisation
- **Quantization** : Réduction du poids du modèle (float32 → int8).
- **Distillation** : Entraîner un petit modèle (ex: DistilBERT) à imiter un grand.
- **ONNX** : Format d'interopérabilité pour accélérer l'inférence.

### 🐳 Déploiement
Containerisation via **Docker** et orchestration via Kubernetes pour gérer la montée en charge.

---

[← 07 - BERT/GPT](07-bert-gpt.md) | [🏠 Accueil](README.md)
