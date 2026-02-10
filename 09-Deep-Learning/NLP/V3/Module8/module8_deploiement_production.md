---
title: Module 8 - Déploiement & Production
description: Formation NLP - Module 8 - Déploiement & Production
tags:
  - NLP
  - 09-Deep-Learning
category: 09-Deep-Learning
---

# 🐳 Déploiement & Production

Containerisation, orchestration et mise en production

## 🎯 Défis du Déploiement NLP

### 🏭 De l'Expérimentation à la Production

Déployer des modèles NLP en production nécessite de résoudre des défis spécifiques au machine learning et au traitement du langage naturel.

1

#### ⚡ Latence

Modèles BERT peuvent prendre 100ms+ par prédiction. En production, il faut servir 1000+ utilisateurs simultanément.

2

#### 💾 Mémoire

BERT-large = 340M paramètres = 1.3GB RAM. Multiplié par le nombre de workers...

3

#### 🔄 Scalabilité

Comment gérer les pics de charge ? Auto-scaling horizontal avec partage de modèles.

4

#### 📊 Monitoring

Dérive des données, performance en temps réel, détection d'anomalies linguistiques.

**🎯 Objectif du Module :** Transformer vos modèles BERT en services production robustes, capables de servir des milliers d'utilisateurs avec une latence < 100ms et une disponibilité > 99.9%.

## 🐳 Containerisation avec Docker

### 📦 Images Docker Optimisées

La containerisation garantit la portabilité et la reproductibilité des déploiements NLP.

🏗️

Multi-Stage Build

Séparation des phases build et runtime pour réduire la taille finale de l'image.

⚡

Images Optimisées

Utilisation d'images de base légères avec CUDA pour GPU et optimisations Python.

🔒

Sécurité

Utilisateur non-root, scan de vulnérabilités, secrets via environment variables.

📊

Health Checks

Monitoring de santé intégré pour orchestration automatique et load balancing.

\# Dockerfile optimisé pour production NLP FROM nvidia/cuda:11.8-devel-ubuntu20.04 as builder # Installation des dépendances de build RUN apt-get update && apt-get install -y \\ python3.9 python3.9-dev python3-pip \\ build-essential cmake git \\ && rm -rf /var/lib/apt/lists/\* # Installation des requirements COPY requirements.txt . RUN pip3 install --no-cache-dir -r requirements.txt # ============================================= # Stage final optimisé FROM nvidia/cuda:11.8-runtime-ubuntu20.04 # Utilisateur non-root pour sécurité RUN useradd --create-home --shell /bin/bash nlpuser # Runtime dependencies seulement RUN apt-get update && apt-get install -y \\ python3.9 python3-pip \\ && rm -rf /var/lib/apt/lists/\* # Copie des packages installés COPY --from=builder /usr/local/lib/python3.9/dist-packages /usr/local/lib/python3.9/dist-packages # Application WORKDIR /app COPY --chown=nlpuser:nlpuser . . # Pre-download des modèles pour éviter download à runtime RUN python3 -c "from transformers import BertTokenizer, BertModel; \\ BertTokenizer.from\_pretrained('bert-base-uncased'); \\ BertModel.from\_pretrained('bert-base-uncased')" # Health check HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \\ CMD python3 -c "import requests; requests.get('http://localhost:8000/health')" USER nlpuser EXPOSE 8000 CMD \["python3", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"\]

**⚠️ Bonnes Pratiques Docker NLP :**  
• Layer caching : Ordre optimal des COPY pour cache hits  
• Model caching : Pre-download pour éviter latence startup  
• Memory limits : Définir limits pour éviter OOM kills  
• GPU support : Nvidia runtime et CUDA compatibility

## ☸️ Orchestration Kubernetes

### 🚢 Déploiement Production

#### ⚙️ Simulateur de Déploiement Kubernetes

Déploiement Basic Production Ready GPU Cluster

Sélectionnez un type de déploiement...

#### 🏗️ Architecture Kubernetes NLP

**🌍 Ingress Controller**  
Load balancing externe, SSL termination, rate limiting

**🔄 Services & Deployments**  
Services NLP avec auto-scaling et health checks

**💾 Persistent Volumes**  
Stockage modèles et données partagées

**🔧 ConfigMaps & Secrets**  
Configuration et credentials sécurisés

\# Manifest Kubernetes pour service NLP apiVersion: apps/v1 kind: Deployment metadata: name: nlp-sentiment-service labels: app: nlp-sentiment spec: replicas: 3 selector: matchLabels: app: nlp-sentiment template: metadata: labels: app: nlp-sentiment spec: containers: - name: sentiment-api image: myregistry/nlp-sentiment:v2.1.0 ports: - containerPort: 8000 resources: requests: memory: "2Gi" cpu: "500m" nvidia.com/gpu: 1 limits: memory: "4Gi" cpu: "2" nvidia.com/gpu: 1 env: - name: MODEL\_PATH value: "/models/sentiment" - name: REDIS\_URL valueFrom: secretKeyRef: name: redis-secret key: url volumeMounts: - name: models-volume mountPath: /models livenessProbe: httpGet: path: /health port: 8000 initialDelaySeconds: 30 periodSeconds: 10 readinessProbe: httpGet: path: /ready port: 8000 initialDelaySeconds: 5 periodSeconds: 5 volumes: - name: models-volume persistentVolumeClaim: claimName: nlp-models-pvc --- apiVersion: v1 kind: Service metadata: name: nlp-sentiment-service spec: selector: app: nlp-sentiment ports: - port: 80 targetPort: 8000 type: ClusterIP --- apiVersion: autoscaling/v2 kind: HorizontalPodAutoscaler metadata: name: nlp-sentiment-hpa spec: scaleTargetRef: apiVersion: apps/v1 kind: Deployment name: nlp-sentiment-service minReplicas: 2 maxReplicas: 10 metrics: - type: Resource resource: name: cpu target: type: Utilization averageUtilization: 70 - type: Resource resource: name: memory target: type: Utilization averageUtilization: 80

## 🔄 CI/CD pour Machine Learning

### ⚙️ Pipeline MLOps

Les pipelines CI/CD pour ML nécessitent des étapes spécifiques : validation de modèle, tests de dérive, benchmarks de performance.

1

#### 🧪 Tests Modèle

Validation accuracy, latence, memory usage sur dataset de test

2

#### 🔨 Build & Push

Container build, optimization, push vers registry

3

#### 🎯 Staging Deploy

Déploiement environnement de staging pour tests intégration

4

#### ✅ Validation

Tests end-to-end, performance, smoke tests

5

#### 🚀 Production

Déploiement blue-green avec monitoring continu

**🎯 Stratégies de Déploiement :**  
• Blue-Green : Basculement instantané avec rollback facile  
• Canary : Déploiement progressif avec monitoring  
• Rolling : Mise à jour instance par instance  
• A/B Testing : Comparaison modèles en parallèle

[← Optimisation](module8_optimisation_modeles.html)

**Déploiement & Production**  
Docker, Kubernetes, CI/CD

[Monitoring →](module8_monitoring_observabilite.html)

// Animation de la barre de progression window.addEventListener('load', function() { setTimeout(() => { document.getElementById('progressBar').style.width = '100%'; }, 1000); }); // Simulateur de déploiement K8s function simulateK8sDeployment(type) { let deployment = ''; switch(type) { case 'basic': deployment = \`🚀 Déploiement Kubernetes Basic 📦 Configuration : • Replicas : 2 • Resources : 1 CPU, 2Gi RAM • GPU : Non • Auto-scaling : Basique (CPU 70%) 📋 Étapes : 1. ✅ Apply ConfigMap 2. ✅ Deploy service (2 pods) 3. ✅ Setup Load Balancer 4. ✅ Health checks OK 🎯 Résultat : • Pods : 2/2 Running • Latence : ~80ms P95 • Throughput : 500 req/sec • Coût : ~$100/mois 💡 Idéal pour : Development, tests, POCs\`; break; case 'production': deployment = \`🏭 Déploiement Production Ready 📦 Configuration : • Replicas : 5 (min 3, max 15) • Resources : 2 CPU, 4Gi RAM per pod • GPU : 1x T4 per pod • Auto-scaling : Avancé (CPU + Memory + Custom) 📋 Étapes : 1. ✅ Secrets & ConfigMaps 2. ✅ PVC pour modèles (100Gi) 3. ✅ Deploy avec rolling update 4. ✅ HPA configuration 5. ✅ Network policies 6. ✅ Monitoring stack 7. ✅ Ingress avec SSL 🎯 Résultat : • Pods : 5/5 Running across 3 nodes • Latence : <50ms P95 • Throughput : 5,000 req/sec • Availability : 99.9% • Coût : ~$800/mois 🎉 Ready for production traffic!\`; break; case 'gpu': deployment = \`🎮 Déploiement GPU Cluster 📦 Configuration : • Node pool : 3x GPU nodes (V100) • Replicas : 8 (min 4, max 20) • Resources : 4 CPU, 8Gi RAM, 1 GPU per pod • CUDA : 11.8 compatible 📋 Étapes : 1. ✅ GPU node pool ready 2. ✅ NVIDIA device plugin 3. ✅ Deploy GPU workloads 4. ✅ GPU monitoring setup 5. ✅ Model parallelism config 🎯 Résultat : • Pods : 8/8 Running on GPU nodes • GPU utilization : 85% average • Latence : <20ms P95 • Throughput : 15,000 req/sec • VRAM usage : 6GB per pod 💰 Coût : ~$2,500/mois 🚀 Ultra-high performance for demanding workloads\`; break; } document.getElementById('k8sOutput').innerHTML = \`<div style="text-align: left; font-size: 0.9em; line-height: 1.4; white-space: pre-line;">${deployment}</div>\`; } // Animation des layers document.querySelectorAll('.layer').forEach((layer, index) => { layer.addEventListener('click', function() { this.style.animation = 'none'; setTimeout(() => { this.style.animation = 'pulse 0.8s ease-in-out'; this.style.background = 'linear-gradient(135deg, #F87171, #EF4444)'; this.style.color = 'white'; setTimeout(() => { this.style.background = 'linear-gradient(135deg, #FEE2E2, #FECACA)'; this.style.color = 'inherit'; }, 800); }, 10); }); });
