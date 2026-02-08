---
title: Frameworks de Prompt Engineering - Guide Complet
description: Formation NLP - Frameworks de Prompt Engineering - Guide Complet
tags:
  - NLP
  - 09-Deep-Learning
category: 09-Deep-Learning
---
  Frameworks de Prompt Engineering - Guide Complet body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #333; } .container { max-width: 1400px; margin: 0 auto; background: white; border-radius: 15px; padding: 30px; box-shadow: 0 20px 40px rgba(0,0,0,0.1); } .header { text-align: center; margin-bottom: 40px; padding: 30px 0; background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); border-radius: 15px; color: white; } h1 { margin: 0; font-size: 2.5em; font-weight: 700; } .subtitle { font-size: 1.2em; opacity: 0.9; margin-top: 10px; } .framework-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 30px; margin: 30px 0; } .framework-card { background: #f8f9fa; padding: 30px; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); border-left: 6px solid; transition: transform 0.3s ease; position: relative; } .framework-card:hover { transform: translateY(-5px); } .framework-card.rtf { border-left-color: #3498db; } .framework-card.pao { border-left-color: #e74c3c; } .framework-card.arp { border-left-color: #27ae60; } .framework-card.care { border-left-color: #f39c12; } .framework-card.riea { border-left-color: #9b59b6; } .framework-card.aspecct { border-left-color: #e67e22; } .framework-title { font-size: 1.8em; font-weight: bold; margin-bottom: 15px; display: flex; align-items: center; gap: 10px; } .framework-acronym { background: rgba(255,255,255,0.9); padding: 8px 15px; border-radius: 25px; font-size: 0.9em; font-weight: bold; color: #333; } .framework-description { margin: 15px 0; font-style: italic; color: #666; } .framework-steps { list-style: none; padding: 0; margin: 20px 0; } .framework-steps li { background: white; margin: 10px 0; padding: 15px; border-radius: 8px; border-left: 4px solid; position: relative; } .rtf .framework-steps li { border-left-color: #3498db; } .pao .framework-steps li { border-left-color: #e74c3c; } .arp .framework-steps li { border-left-color: #27ae60; } .care .framework-steps li { border-left-color: #f39c12; } .riea .framework-steps li { border-left-color: #9b59b6; } .aspecct .framework-steps li { border-left-color: #e67e22; } .step-letter { font-weight: bold; color: #333; font-size: 1.1em; } .step-description { margin-top: 5px; color: #555; } .example-box { background: #fff3cd; border: 1px solid #ffeaa7; border-radius: 10px; padding: 20px; margin: 20px 0; } .example-title { font-weight: bold; color: #856404; margin-bottom: 10px; } .example-content { color: #6c757d; font-family: 'Courier New', monospace; background: white; padding: 15px; border-radius: 5px; border-left: 4px solid #ffc107; white-space: pre-line; } .comparison-section { background: linear-gradient(135deg, #e3f2fd 0%, #f8f9fa 100%); padding: 30px; border-radius: 15px; margin: 40px 0; } .comparison-table { width: 100%; border-collapse: collapse; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 5px 15px rgba(0,0,0,0.1); } .comparison-table th { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px; text-align: left; } .comparison-table td { padding: 12px 15px; border-bottom: 1px solid #eee; } .comparison-table tr:hover { background: #f8f9fa; } .best-practices { background: #d4edda; border: 1px solid #c3e6cb; color: #155724; padding: 25px; border-radius: 10px; margin: 30px 0; } .warning-box { background: #fff3cd; border: 1px solid #ffeaa7; color: #856404; padding: 20px; border-radius: 10px; margin: 20px 0; } .interactive-demo { background: #e3f2fd; padding: 25px; border-radius: 15px; margin: 30px 0; } .demo-button { background: linear-gradient(135deg, #2196f3 0%, #1976d2 100%); color: white; border: none; padding: 12px 25px; border-radius: 25px; cursor: pointer; font-size: 1em; margin: 10px 5px; transition: all 0.3s ease; } .demo-button:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(33, 150, 243, 0.3); } .demo-output { background: white; padding: 20px; border-radius: 10px; margin-top: 15px; border-left: 4px solid #2196f3; min-height: 100px; display: none; } .quick-reference { background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 25px; border-radius: 15px; margin: 30px 0; } .reference-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-top: 20px; } .reference-card { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 3px 10px rgba(0,0,0,0.1); } .back-to-module { text-align: center; margin: 40px 0; } .btn { display: inline-block; padding: 15px 30px; background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); color: white; text-decoration: none; border-radius: 25px; transition: all 0.3s ease; font-weight: 500; } .btn:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(255, 107, 107, 0.4); }

# 🎯 Frameworks de Prompt Engineering

Maîtrisez les 6 Frameworks Essentiels pour des Prompts Professionnels

## 🌟 Pourquoi Utiliser des Frameworks ?

Les frameworks de prompting vous permettent de :

*   **Structurer** vos demandes de manière cohérente
*   **Maximiser** la précision des réponses
*   **Réduire** les ambiguïtés et malentendus
*   **Standardiser** vos processus de prompting
*   **Améliorer** la reproductibilité des résultats

R-T-F Rôle - Tâche - Format

Pour des travaux structurés avec un rôle spécifique

*   R - RÔLE
    
    Définir l'expertise ou la perspective requise
    
*   T - TÂCHE
    
    Spécifier clairement ce qui doit être accompli
    
*   F - FORMAT
    
    Préciser la structure de sortie souhaitée
    

💡 Exemple R-T-F

RÔLE: Agis en tant que directeur créatif d'une agence de publicité TÂCHE: Conçois une campagne de publicité pour notre nouvelle gamme de tennis français écologiques, ciblant les jeunes de 18-30 ans FORMAT: Présente ta réponse sous cette forme : - Concept créatif principal - 3 slogans accrocheurs - Plan de déploiement sur 3 mois

P-A-O Problème - Action - Objectif

Pour résoudre des problèmes concrets avec des actions claires

*   P - PROBLÈME
    
    Définir le problème à résoudre clairement
    
*   A - ACTION
    
    Proposer des actions concrètes et réalisables
    
*   O - OBJECTIF
    
    Clarifier l'objectif final et les critères de succès
    

💡 Exemple P-A-O

PROBLÈME: Mes enfants de 6 et 8 ans résistent au ménage des légumes verts ACTION: Propose-moi 5 recettes fun et créatives pour les légumes dans des plats qui plairont aux enfants sans nuire à leur santé OBJECTIF: Mon objectif est que mes enfants mangent des légumes avec plaisir sans 3 mois environ pour qu'ils grandissent en bonne santé

A-R-P Avant - Résultat - Point

Pour combler un écart stratégique entre situation actuelle et désirée

*   A - AVANT
    
    Expliquer la situation actuelle ou le point de départ
    
*   R - RÉSULTAT
    
    Préciser le résultat souhaité ou l'état final
    
*   P - POINT
    
    Demander le point clé ou la stratégie pour y arriver
    

💡 Exemple A-R-P

AVANT: Nous sommes une startup tech avec notre expertise en reconnaissance vocal, nous voulons faire un top 3 sur la SAAS de plus de 3M ARR en 20 mois RÉSULTAT: Nous voulons être dans le top 3 des secteurs SaaS les plus rentables avec un ARR d'au moins 3M d'euros POINT: Inclus un plan d'action et des KPIs clés pour notre domaine

C-A-R-E Contexte - Action - Résultat - Exemple

Pour créer des stratégies complètes avec exemples concrets

*   C - CONTEXTE
    
    Présenter le contexte et les circonstances
    
*   A - ACTION
    
    Décrire les actions à entreprendre
    
*   R - RÉSULTAT
    
    Préciser les résultats attendus
    
*   E - EXEMPLE
    
    Donner un exemple concret ou une illustration
    

💡 Exemple C-A-R-E

CONTEXTE: Nous lançons une marque de baskets fabriqués à partir de bouteilles plastiques recyclées, management éthique. Tel fait que Patagonie avec des prix beaux, mais pas trop chers dépendant entre les basketttes de sport et adidas que le prix ACTION: Développe une stratégie de communication durable + intégriste + Tel fait que Patagonie écologiquement éthique et social + 3 premiers mois suivent RÉSULTAT: Précise le plan pour tendre compte des premiers 3 mois suivant + identifier et quantifier le trafic augmentant correspondant l'impact environnemental de l'industrie de la chaussure + et un processus générer 100 premiers clients et attendre un taux de croissance des fidèles clients + et identifier d'optimisme de 30% qu'attendre un chiffre d'affaires de 100k€ EXEMPLE: Donne un exemple de campagne fondamentale spécifique et 2 types de partenariats avec des influenceurs éco-responsables

R-I-E-A Rôle - Info - Étapes - Attente

Pour créer des systèmes détaillés avec processus étape par étape

*   R - RÔLE
    
    Spécifier le rôle ou l'expertise demandée
    
*   I - INFO
    
    Donner toutes les informations pertinentes
    
*   E - ÉTAPES
    
    Demander les étapes détaillées du processus
    
*   A - ATTENTE
    
    Décrire ce qui est attendu comme résultat final
    

💡 Exemple R-I-E-A

RÔLE: Agis comme un conseiller en investissement immobilier spécialisé dans la stratégie pour élargir INFO: J'ai un budget de 300 000 € pour ma première acquisition et je cherche un profit économie locative ÉTAPES: Donne-moi les 12 étapes de la recherche à la mise en location, Moi detendre un rendement net/an de 12% ATTENTE: Je veux obtenir une rentabilité nette de préférence autour de 8% et comprendre spécifiquement effectuer pour atteindre le rendement des finances demandées

ASPECCT Action - Spécificité - Public - Exemples - Contraintes - Clarifications - Ton

Framework ultra-complet pour des demandes complexes et nuancées

*   A - ACTION
    
    Définir l'action principale à accomplir
    
*   S - SPÉCIFICITÉ
    
    Préciser les détails spécifiques importants
    
*   P - PUBLIC
    
    Identifier l'audience cible
    
*   E - EXEMPLES
    
    Fournir des exemples ou références
    
*   C - CONTRAINTES
    
    Mentionner les limitations ou contraintes
    
*   C - CLARIFICATIONS
    
    Ajouter des clarifications nécessaires
    
*   T - TON
    
    Préciser le style et le ton souhaités
    

💡 Exemple ASPECCT

ACTION: Rédige un article de blog SPÉCIFICITÉ: Sur les tendances IA en 2024 pour les PME françaises PUBLIC: Dirigeants de PME technophobes mais ouverts à l'innovation EXEMPLES: Comme les articles de Harvard Business Review mais adaptés au contexte français CONTRAINTES: 1500 mots maximum, sans jargon technique CLARIFICATIONS: Focus sur les solutions pratiques et accessibles, pas la théorie TON: Professionnel mais accessible, rassurant, avec une pointe d'optimisme

## 📊 Tableau Comparatif des Frameworks

Framework

Complexité

Cas d'Usage Optimal

Avantages

Limitations

**R-T-F**

Simple

Travaux créatifs, analyses spécialisées

Rapide, structuré, facile à retenir

Manque de contexte pour problèmes complexes

**P-A-O**

Simple

Résolution de problèmes concrets

Orienté solution, actionnable

Peu adapté aux tâches créatives

**A-R-P**

Modérée

Planification stratégique, transformation

Vision claire du chemin à parcourir

Nécessite une bonne définition de l'état final

**C-A-R-E**

Modérée

Stratégies complètes avec exemples

Équilibré, inclut des exemples concrets

Plus long à formuler

**R-I-E-A**

Élevée

Processus détaillés, systèmes complexes

Très structuré, processus step-by-step

Peut être trop rigide pour la créativité

**ASPECCT**

Très élevée

Projets complexes, communications nuancées

Ultra-complet, très précis

Long à rédiger, peut être excessif

## 🎮 Démonstration Interactive

Cliquez sur un framework pour voir un exemple interactif :

Démo R-T-F Démo P-A-O Démo A-R-P Démo C-A-R-E Démo R-I-E-A Démo ASPECCT

## 📋 Guide de Sélection Rapide

### 🎨 Pour la Créativité

**Utilisez R-T-F**

Parfait pour les contenus créatifs, analyses d'expert, travaux de rédaction

### 🔧 Pour Résoudre un Problème

**Utilisez P-A-O**

Idéal pour les problèmes concrets nécessitant des actions claires

### 📈 Pour la Stratégie

**Utilisez A-R-P ou C-A-R-E**

Excellent pour la planification et les transformations business

### ⚙️ Pour les Processus

**Utilisez R-I-E-A**

Parfait pour les systèmes complexes et processus détaillés

### 🎯 Pour la Précision

**Utilisez ASPECCT**

Indispensable pour les demandes complexes et nuancées

### ⚡ Pour la Simplicité

**Commencez par R-T-F**

Le plus simple à maîtriser et applicable dans 80% des cas

### ⚠️ Conseils d'Expert

*   **Ne surchargez pas** : Utilisez le framework le plus simple qui répond à vos besoins
*   **Adaptez le langage** : Ajustez le niveau de détail selon votre audience
*   **Testez et itérez** : Si le résultat ne convient pas, essayez un autre framework
*   **Combinez si nécessaire** : Vous pouvez mixer des éléments de différents frameworks
*   **Restez cohérent** : Une fois un framework choisi, suivez-le entièrement

[🔙 Retour au Module 10](index.html) [📓 Ouvrir le Notebook](notebooks/01_Techniques_Avancees.ipynb)

function showDemo(framework) { const demoOutput = document.getElementById('demo-output'); const demos = { 'rtf': \` <h3>🎯 Démonstration R-T-F</h3> <p><strong>Cas d'usage :</strong> Création d'une stratégie marketing</p> <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 10px 0;"> <strong>RÔLE :</strong> Tu es un directeur marketing expérimenté spécialisé dans le B2B tech<br> <strong>TÂCHE :</strong> Crée une stratégie de lead generation pour notre logiciel CRM<br> <strong>FORMAT :</strong> Présente sous forme de plan avec budgets et timeline </div> <p><em>💡 Résultat attendu : Une stratégie structurée avec l'expertise d'un pro marketing</em></p> \`, 'pao': \` <h3>🔧 Démonstration P-A-O</h3> <p><strong>Cas d'usage :</strong> Amélioration de performance équipe</p> <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 10px 0;"> <strong>PROBLÈME :</strong> Mon équipe dev a 30% de retard sur les livraisons<br> <strong>ACTION :</strong> Propose 5 actions concrètes pour améliorer la vélocité<br> <strong>OBJECTIF :</strong> Rattraper le retard en 6 semaines et maintenir le rythme </div> <p><em>💡 Résultat attendu : Des solutions pratiques et mesurables</em></p> \`, 'arp': \` <h3>📈 Démonstration A-R-P</h3> <p><strong>Cas d'usage :</strong> Transformation digitale d'entreprise</p> <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 10px 0;"> <strong>AVANT :</strong> PME traditionnelle, processus manuels, 50 employés, CA 5M€<br> <strong>RÉSULTAT :</strong> Entreprise digitalisée avec +40% productivité en 18 mois<br> <strong>POINT :</strong> Quel plan de transformation avec priorités et budget ? </div> <p><em>💡 Résultat attendu : Roadmap de transformation avec étapes claires</em></p> \`, 'care': \` <h3>🎯 Démonstration C-A-R-E</h3> <p><strong>Cas d'usage :</strong> Lancement de produit innovant</p> <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 10px 0;"> <strong>CONTEXTE :</strong> Startup EdTech, plateforme IA pour l'apprentissage personnalisé<br> <strong>ACTION :</strong> Stratégie de lancement sur le marché français<br> <strong>RÉSULTAT :</strong> 1000 utilisateurs actifs et 100K€ ARR en 6 mois<br> <strong>EXEMPLE :</strong> Cite 2 cas similaires et tactiques marketing spécifiques </div> <p><em>💡 Résultat attendu : Stratégie complète avec benchmarks concrets</em></p> \`, 'riea': \` <h3>⚙️ Démonstration R-I-E-A</h3> <p><strong>Cas d'usage :</strong> Mise en place d'un processus qualité</p> <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 10px 0;"> <strong>RÔLE :</strong> Expert en management qualité ISO 9001<br> <strong>INFO :</strong> Entreprise 200 employés, industrie, certification dans 12 mois<br> <strong>ÉTAPES :</strong> Liste les 15 étapes détaillées avec responsables et délais<br> <strong>ATTENTE :</strong> Plan projet complet avec livrables et checkpoints </div> <p><em>💡 Résultat attendu : Processus détaillé étape par étape</em></p> \`, 'aspecct': \` <h3>🎪 Démonstration ASPECCT</h3> <p><strong>Cas d'usage :</strong> Communication de crise complexe</p> <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 10px 0;"> <strong>ACTION :</strong> Rédige un plan de communication de crise<br> <strong>SPÉCIFICITÉ :</strong> Fuite de données personnelles chez fintech française<br> <strong>PUBLIC :</strong> Clients B2C, régulateurs, médias, investisseurs<br> <strong>EXEMPLES :</strong> Inspire-toi des cas Uber 2016 et Facebook 2018<br> <strong>CONTRAINTES :</strong> Conformité RGPD, réponse sous 24h, budget limité<br> <strong>CLARIFICATIONS :</strong> Priorise la transparence et la responsabilité<br> <strong>TON :</strong> Professionnel, empathique, rassurant mais pas défensif </div> <p><em>💡 Résultat attendu : Plan de communication ultra-détaillé et nuancé</em></p> \` }; demoOutput.innerHTML = demos\[framework\]; demoOutput.style.display = 'block'; demoOutput.scrollIntoView({ behavior: 'smooth' }); }
