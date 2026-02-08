---
title: Module 8 - Monitoring & Observabilité
description: Formation NLP - Module 8 - Monitoring & Observabilité
tags:
  - NLP
  - 09-Deep-Learning
category: 09-Deep-Learning
---

# 📊 Monitoring & Observabilité

Surveillance et diagnostic des systèmes NLP en production

## 📈 Dashboard de Production

### 🎯 Métriques Temps Réel

Un système de monitoring efficace fournit une visibilité complète sur la santé et les performances de vos services NLP.

⚡ Performance Système

Latence P95 47ms

Throughput 2,847 req/sec

Taux d'erreur 0.12%

Disponibilité 99.97%

🧠 Métriques ML

Confiance moyenne 0.847

Prédictions/jour 245K

Cache hit rate 78%

Model drift Stable

💻 Infrastructure

CPU Usage 67%

Memory Usage 4.2GB / 8GB

GPU Utilization 85%

Instances actives 6 / 8

🚦 État des Services

API Gateway Healthy

Sentiment Service Healthy

NER Service Warning

Database Healthy

⚠️

Alerte : Latence Élevée

Service NER dépasse 120ms P95 depuis 5 minutes. Auto-scaling déclenché.

#### 📊 Évolution Latence (24h)

00h

35ms

04h

45ms

08h

67ms

12h

84ms

16h

56ms

20h

42ms

24h

47ms

## 🔍 Détection de Data Drift

### 📊 Surveillance des Distributions

La dérive des données est un phénomène critique où les données de production diffèrent des données d'entraînement, dégradant les performances du modèle.

📈

Statistical Drift Detection

Détection basée sur des tests statistiques (KS-test, chi-square) pour identifier les changements de distribution.

*   Tests Kolmogorov-Smirnov
*   Population Stability Index
*   Jensen-Shannon Divergence
*   Alertes automatiques

🎯

Performance Monitoring

Surveillance continue des métriques de performance pour détecter une dégradation.

*   Accuracy tracking
*   Confidence distribution
*   Prediction drift
*   A/B testing continu

🌊

Feature Drift Analysis

Analyse fine des changements dans les features d'entrée du modèle.

*   Distribution embedding
*   Feature importance shift
*   Covariate shift detection
*   Concept drift identification

\# Détection de data drift pour modèles NLP import numpy as np from scipy import stats from sklearn.feature\_extraction.text import TfidfVectorizer import logging class NLPDriftDetector: def \_\_init\_\_(self, reference\_data, alert\_threshold=0.05): self.reference\_data = reference\_data self.alert\_threshold = alert\_threshold self.vectorizer = TfidfVectorizer(max\_features=1000, stop\_words='english') # Calcul des features de référence self.reference\_features = self.\_extract\_features(reference\_data) self.reference\_stats = self.\_compute\_baseline\_stats() def \_extract\_features(self, texts): """Extraction de features pour analyse de drift""" # Features statistiques lengths = \[len(text.split()) for text in texts\] char\_counts = \[len(text) for text in texts\] # Features TF-IDF if hasattr(self.vectorizer, 'vocabulary\_'): tfidf\_features = self.vectorizer.transform(texts) else: tfidf\_features = self.vectorizer.fit\_transform(texts) return { 'lengths': lengths, 'char\_counts': char\_counts, 'tfidf\_mean': np.mean(tfidf\_features.toarray(), axis=1), 'texts': texts } def \_compute\_baseline\_stats(self): """Calcul des statistiques de référence""" return { 'length\_mean': np.mean(self.reference\_features\['lengths'\]), 'length\_std': np.std(self.reference\_features\['lengths'\]), 'char\_mean': np.mean(self.reference\_features\['char\_counts'\]), 'char\_std': np.std(self.reference\_features\['char\_counts'\]), 'tfidf\_distribution': self.reference\_features\['tfidf\_mean'\] } def detect\_drift(self, new\_data, drift\_types=\['statistical', 'semantic'\]): """ Détection de drift sur nouvelles données """ results = {} new\_features = self.\_extract\_features(new\_data) if 'statistical' in drift\_types: results\['statistical\_drift'\] = self.\_statistical\_drift\_test(new\_features) if 'semantic' in drift\_types: results\['semantic\_drift'\] = self.\_semantic\_drift\_test(new\_data) # Drift global results\['overall\_drift'\] = any( result\['p\_value'\] < self.alert\_threshold for result in results.values() if 'p\_value' in result ) return results def \_statistical\_drift\_test(self, new\_features): """Test statistique de drift (Kolmogorov-Smirnov)""" # Test sur longueurs de texte ks\_stat, p\_value = stats.ks\_2samp( self.reference\_features\['lengths'\], new\_features\['lengths'\] ) # Population Stability Index psi = self.\_calculate\_psi( self.reference\_features\['tfidf\_mean'\], new\_features\['tfidf\_mean'\] ) return { 'test\_type': 'kolmogorov\_smirnov', 'ks\_statistic': ks\_stat, 'p\_value': p\_value, 'psi\_score': psi, 'drift\_detected': p\_value < self.alert\_threshold or psi > 0.2 } def \_semantic\_drift\_test(self, new\_texts): """Test de drift sémantique via embeddings""" # Utilisation de la similarité cosinus moyenne from sklearn.metrics.pairwise import cosine\_similarity ref\_tfidf = self.vectorizer.transform(self.reference\_data\[:100\]) new\_tfidf = self.vectorizer.transform(new\_texts\[:100\]) # Similarité intra-référence vs inter-référence-nouveau ref\_similarity = np.mean(cosine\_similarity(ref\_tfidf)) cross\_similarity = np.mean(cosine\_similarity(ref\_tfidf, new\_tfidf)) semantic\_shift = abs(ref\_similarity - cross\_similarity) return { 'test\_type': 'semantic\_similarity', 'reference\_similarity': ref\_similarity, 'cross\_similarity': cross\_similarity, 'semantic\_shift': semantic\_shift, 'drift\_detected': semantic\_shift > 0.1 } def \_calculate\_psi(self, reference, current, buckets=10): """Calcul du Population Stability Index""" def scale\_range(input\_data, min\_val, max\_val): return (input\_data - min\_val) / (max\_val - min\_val) min\_val = min(min(reference), min(current)) max\_val = max(max(reference), max(current)) ref\_scaled = scale\_range(reference, min\_val, max\_val) cur\_scaled = scale\_range(current, min\_val, max\_val) breakpoints = np.arange(0, buckets + 1) / buckets ref\_counts, \_ = np.histogram(ref\_scaled, breakpoints) cur\_counts, \_ = np.histogram(cur\_scaled, breakpoints) # Éviter division par zéro ref\_counts = np.where(ref\_counts == 0, 1, ref\_counts) cur\_counts = np.where(cur\_counts == 0, 1, cur\_counts) ref\_percents = ref\_counts / len(reference) cur\_percents = cur\_counts / len(current) psi = np.sum((cur\_percents - ref\_percents) \* np.log(cur\_percents / ref\_percents)) return psi

#### 🔍 Simulateur de Drift Detection

Pas de Drift Drift Léger Drift Sévère Concept Drift

Sélectionnez un scénario pour analyser le drift...

## 🛠️ Stack Technique de Monitoring

### ⚙️ Outils et Technologies

📊

Prometheus + Grafana

Stack de référence pour métriques et dashboards temps réel avec alerting avancé.

*   Métriques custom ML
*   Dashboards interactifs
*   Alerting multicanal
*   Rétention long terme

📝

ELK Stack

Elasticsearch, Logstash, Kibana pour logging centralisé et analyse de logs structurés.

*   Logs centralisés
*   Recherche full-text
*   Agrégations complexes
*   Visualisations avancées

🔍

Jaeger Tracing

Tracing distribué pour suivre les requêtes à travers les microservices NLP.

*   Distributed tracing
*   Performance profiling
*   Bottleneck identification
*   Dependency mapping

🚨

MLflow + Weights & Biases

Tracking d'expériences ML et monitoring de modèles avec versioning.

*   Model versioning
*   Experiment tracking
*   Performance comparison
*   Artifact management

\# Configuration Prometheus pour métriques NLP personnalisées from prometheus\_client import Counter, Histogram, Gauge, start\_http\_server import time import functools # Métriques custom pour NLP PREDICTION\_COUNTER = Counter( 'nlp\_predictions\_total', 'Total predictions made', \['model\_name', 'task\_type', 'status'\] ) PREDICTION\_LATENCY = Histogram( 'nlp\_prediction\_duration\_seconds', 'Time spent on predictions', \['model\_name', 'task\_type'\], buckets=\[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0\] ) MODEL\_CONFIDENCE = Histogram( 'nlp\_prediction\_confidence', 'Confidence scores distribution', \['model\_name', 'task\_type'\], buckets=\[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0\] ) GPU\_MEMORY\_USAGE = Gauge( 'nlp\_gpu\_memory\_bytes', 'GPU memory usage in bytes', \['gpu\_id', 'model\_name'\] ) CACHE\_HIT\_RATE = Gauge( 'nlp\_cache\_hit\_rate', 'Cache hit rate percentage', \['cache\_type'\] ) class NLPMonitoringMiddleware: def \_\_init\_\_(self, model\_name, task\_type): self.model\_name = model\_name self.task\_type = task\_type def monitor\_prediction(self, func): """Décorateur pour monitorer les prédictions""" @functools.wraps(func) def wrapper(\*args, \*\*kwargs): start\_time = time.time() status = 'success' try: result = func(\*args, \*\*kwargs) # Enregistrer la confiance si disponible if hasattr(result, 'confidence'): MODEL\_CONFIDENCE.labels( model\_name=self.model\_name, task\_type=self.task\_type ).observe(result.confidence) return result except Exception as e: status = 'error' raise finally: # Enregistrer latence et compteur duration = time.time() - start\_time PREDICTION\_LATENCY.labels( model\_name=self.model\_name, task\_type=self.task\_type ).observe(duration) PREDICTION\_COUNTER.labels( model\_name=self.model\_name, task\_type=self.task\_type, status=status ).inc() return wrapper # Exemple d'utilisation class SentimentAnalysisService: def \_\_init\_\_(self): self.monitor = NLPMonitoringMiddleware('bert-sentiment', 'classification') @monitor.monitor\_prediction def predict(self, text): # Simulation de prédiction time.sleep(0.05) # Latence simulée return { 'sentiment': 'positive', 'confidence': 0.87, 'processing\_time': 0.05 } # Démarrage du serveur de métriques if \_\_name\_\_ == "\_\_main\_\_": start\_http\_server(8000) service = SentimentAnalysisService()

**⚠️ Bonnes Pratiques Monitoring :**  
• Métriques RED : Rate, Errors, Duration pour chaque service  
• Logging structuré : JSON avec contexte complet  
• Correlation IDs : Traçabilité cross-service  
• Alerting intelligent : Éviter les false positives

## 🚨 Alerting et Incident Response

### ⚡ Stratégie d'Alerting

Un système d'alerting efficace détecte les problèmes avant qu'ils impactent les utilisateurs et guide la résolution d'incidents.

**🎯 Niveaux d'Alerte NLP :**  
• INFO : Déploiement nouveau modèle, scaling automatique  
• WARNING : Latence élevée, drift détecté, cache miss rate élevé  
• CRITICAL : Service down, accuracy chute >5%, erreurs >1%  
• EMERGENCY : Perte de données, security breach, corruption modèle

#### 🚨 Simulateur d'Incident Response

Latence Élevée Chute Accuracy Service Down Data Drift

Sélectionnez un type d'incident pour voir la procédure...

[← Déploiement](module8_deploiement_production.html)

**Monitoring & Observabilité**  
Surveillance, Alerting, Incident Response

[Index Module 8 →](index.html)

// Animation de la barre de progression window.addEventListener('load', function() { setTimeout(() => { document.getElementById('progressBar').style.width = '100%'; }, 1000); }); // Simulateur de drift detection function simulateDrift(scenario) { let analysis = ''; switch(scenario) { case 'no\_drift': analysis = \`✅ Pas de Drift Détecté 📊 Analyse Statistique : • KS-test p-value: 0.45 (> 0.05) • Population Stability Index: 0.08 (< 0.2) • Similarité sémantique: 0.91 (> 0.8) • Distribution longueur texte: Stable 🎯 Recommandations : • Aucune action requise • Monitoring continu • Validation qualité mensuelle • Performance stable maintenue 📈 Métriques Modèle : • Accuracy: 94.2% (stable) • Confiance moyenne: 0.87 • Latence P95: 47ms • Taux d'erreur: 0.12%\`; break; case 'slight\_drift': analysis = \`⚠️ Drift Léger Détecté 📊 Analyse Statistique : • KS-test p-value: 0.03 (< 0.05) • Population Stability Index: 0.15 (limite) • Similarité sémantique: 0.78 (légère baisse) • Distribution: Changement vocabulaire 🎯 Recommandations : • Surveillance renforcée • Collecte données récentes • A/B test avec nouveau dataset • Préparation re-entraînement 📈 Impact Observé : • Accuracy: 92.8% (-1.4%) • Confiance: 0.83 (-0.04) • Certaines catégories affectées • Tolérable à court terme\`; break; case 'severe\_drift': analysis = \`🚨 Drift Sévère Détecté 📊 Analyse Statistique : • KS-test p-value: 0.001 (<<< 0.05) • Population Stability Index: 0.35 (critique) • Similarité sémantique: 0.62 (forte baisse) • Distribution: Changement majeur domaine 🎯 Actions Immédiates : • 🚨 Alerte équipe ML • Rollback vers modèle robuste • Investigation source du drift • Re-entraînement d'urgence 📈 Impact Critique : • Accuracy: 86.3% (-7.9%) • Confiance: 0.74 (-0.13) • Intervention humaine requise • Risque business élevé\`; break; case 'concept\_drift': analysis = \`🔄 Concept Drift Détecté 📊 Analyse Complexe : • KS-test p-value: 0.15 (borderline) • Concept shift score: 0.8 (élevé) • Labels distribution: Changée • Saisonnalité détectée 🎯 Stratégie Adaptative : • Mise à jour continue du modèle • Online learning activation • Rebalancing des classes • Adaptation aux nouveaux concepts 📈 Impact Évolutif : • Accuracy globale: 91.5% • Performance par classe variable • Adaptation progressive nécessaire • Évolution métier détectée\`; break; } document.getElementById('driftOutput').innerHTML = \`<div style="text-align: left; font-size: 0.9em; line-height: 1.4; white-space: pre-line;">${analysis}</div>\`; } // Simulateur d'incident response function simulateIncident(incidentType) { let response = ''; switch(incidentType) { case 'latency': response = \`⚡ Incident: Latence Élevée (P95 > 200ms) 🚨 Alertes Déclenchées : • 14:23 - WARNING: Latence P95 = 156ms • 14:25 - CRITICAL: Latence P95 = 210ms • 14:26 - Auto-scaling déclenché 🔍 Investigation (SEV-2) : 1. Vérification charge système ✅ 2. Analyse logs erreurs ✅ 3. Monitoring GPU utilization ⚠️ 98% 4. Vérification modèle drift ✅ 💡 Cause Identifiée : • Pic de trafic inattendu • GPU memory saturation • Garbage collection fréquent ⚡ Actions Correctives : • 14:27 - Scale horizontal +2 instances • 14:29 - Activation circuit breaker • 14:30 - Latence revenue à 47ms • 14:35 - Incident résolu 📋 Post-Incident : • Update alerting thresholds • Amélioration auto-scaling • Documentation playbook\`; break; case 'accuracy': response = \`📉 Incident: Chute d'Accuracy (-7%) 🚨 Alertes Critiques : • 09:15 - Accuracy dropped to 87.2% • 09:16 - Data drift detected • 09:17 - Confidence scores declining 🔍 Investigation (SEV-1) : 1. Model version check ✅ v2.1.3 2. Input data validation ⚠️ Anomalies 3. Feature distribution ❌ Shifted 4. External data source ❌ Changed 💡 Root Cause : • Upstream data pipeline modified • Feature encoding changed • Training/serving skew introduced ⚡ Actions Immédiates : • 09:20 - Rollback to model v2.1.2 • 09:22 - Fix data pipeline • 09:25 - Accuracy restored to 94.1% • 09:30 - Validation complete 📋 Prevention : • Schema validation enforcement • Canary deployments • Data quality monitoring • Cross-validation automation\`; break; case 'service\_down': response = \`💥 Incident: Service Sentiment Down 🚨 Alertes Système : • 16:42 - Service health check failed • 16:42 - 100% error rate • 16:43 - Failover to backup instances • 16:43 - User impact: 30% requests 🔍 Investigation (SEV-0) : 1. Container status ❌ CrashLoopBackOff 2. Memory usage ❌ OOM Kill 3. Model loading ❌ Corrupted weights • Model file corruption détectée 💡 Cause Racine : • Déploiement interrompu • Fichier modèle partiellement écrit • Health check insuffisant ⚡ Actions d'Urgence : • 16:44 - Stop deployment pipeline • 16:45 - Restore from backup • 16:47 - Service operational • 16:50 - Traffic fully restored 📋 Améliorations : • Atomic deployments • Model integrity checks • Improved health probes • Faster rollback procedure\`; break; case 'data\_drift': response = \`🌊 Incident: Data Drift Majeur 🚨 ML Alerts : • 11:30 - PSI score: 0.42 (critical) • 11:31 - Feature importance shifted • 11:32 - Prediction distribution changed • 11:35 - Business metrics impacted 🔍 Investigation ML (SEV-1) : 1. Data source analysis ✅ 2. Feature engineering ⚠️ New features 3. User behavior ❌ Seasonal change 4. External factors ❌ Market shift 💡 Drift Analysis : • Nouveau segment utilisateurs • Changement comportemental COVID • Vocabulaire évolutif • Saisonnalité non modélisée ⚡ Stratégie Adaptative : • 11:40 - Activate online learning • 11:45 - Collect recent labels • 12:00 - Retrain with new data • 12:30 - Deploy adapted model 📋 Long Terme : • Continuous learning pipeline • Drift detection automation • Model versioning strategy • Business alignment meeting\`; break; } document.getElementById('incidentOutput').innerHTML = \`<div style="text-align: left; font-size: 0.9em; line-height: 1.4; white-space: pre-line;">${response}</div>\`; } // Animation des barres de chart document.querySelectorAll('.chart-bar').forEach((bar, index) => { bar.addEventListener('click', function() { this.style.animation = 'none'; setTimeout(() => { this.style.animation = 'pulse 0.8s ease-in-out'; this.style.background = 'linear-gradient(to top, #065F46, #10B981)'; setTimeout(() => { this.style.background = 'linear-gradient(to top, #10B981, #34D399)'; }, 800); }, 10); }); });
