---
title: Brief Computer Vision YOLOv8 - VisionForge AI
description: Formation CNN - Brief Computer Vision YOLOv8 - VisionForge AI
tags:
  - CNN
  - 09-Deep-Learning
category: 09-Deep-Learning
---

VisionForge AI

# 🧠 Découverte de la Computer Vision avec YOLOv8

Proof of Concept - Détection d'objets en temps réel

## 🏢 Contexte Entreprise

**Vous êtes IA Engineer chez VisionForge AI**, une startup ambitieuse dans le secteur de la surveillance intelligente. L'entreprise développe des solutions de **computer vision** pour différents secteurs : sécurité urbaine, retail, industrie automobile, et santé publique.

  

**Contexte business :** VisionForge AI a identifié 6 verticales métier prometteuses et souhaite rapidement prototyper des solutions pour valider le marché. Chaque équipe R&D se voit attribuer une verticale spécifique pour développer un POC fonctionnel.

  

**Mission :** Créer une application basée sur **YOLO (You Only Look Once)** capable de détecter des objets spécifiques via webcam, démontrant ainsi la faisabilité technique et commerciale de votre verticale.

  

**Enjeu :** Les POCs les plus convaincants seront présentés aux investisseurs pour lever des fonds supplémentaires et développer ces solutions à l'échelle industrielle.

## 🎯 Objectifs Pédagogiques

À l'issue du projet, vous serez capables de :

**1.** Choisir une verticale métier et définir un projet avec un nom accrocheur (ex: "PlateHunter", "MaskGuard", "PhonePolice")

**2.** Identifier une problématique métier en vision par ordinateur à partir d'un dataset Roboflow

**3.** Sélectionner et fine-tuner une version de YOLO adaptée (v5 à v10)

**4.** Intégrer le modèle dans une application interactive

**5.** Réaliser une démo fonctionnelle avec webcam en conditions réelles

**6.** Pitcher votre solution comme un vrai produit tech devant des investisseurs

## 📦 Livrables Attendus

*   **Définition du projet** avec nom créatif (ex: "PlateHunter", "MaskGuard")
*   **Notebook d'entraînement complet** (YOLOv8 ou autre version) ou repo GitHub
*   **Fichier du modèle entraîné** (.pt ou .onnx)
*   **Application avec webcam** (minimum : démonstration OpenCV - Gradio/Streamlit optionnel)
*   **Démonstration vidéo** (desktop ou smartphone)
*   **Présentation courte** (5 slides max) avec métriques et conclusions

**⚠️ Important :** Une démonstration avec OpenCV est **obligatoire**. Le frontend Gradio/Streamlit est optionnel mais l'utilisation de la webcam via OpenCV est **requise** pour la démonstration finale.

## 💡 Suggestions de Projets

Voici quelques idées de verticales métier pour vous inspirer. Chaque groupe est libre de choisir ou d'inventer son propre projet !

**🚗 Mobilité & Transport**  
• **PlateHunter:** Lecture plaques d'immatriculation  
• **SpeedWatch:** Estimation vitesse véhicules  
• **ParkingAI:** Détection places libres/occupées  
• **TrafficFlow:** Analyse densité circulation

**🏥 Santé & Sécurité**  
• **MaskGuard:** Contrôle port du masque  
• **SmokeAlert:** Détection fumée/incendie  
• **HelmetChecker:** Vérification casques chantier  
• **FirstAidBot:** Détection situations d'urgence

**🛍️ Retail & Commerce**  
• **FashionScanner:** Classification vêtements/styles  
• **ProductCount:** Inventaire automatique rayons  
• **BrandSpotter:** Reconnaissance logos/marques  
• **QueueWatch:** Gestion files d'attente

**🍽️ Food & Hospitality**  
• **FoodDetective:** Reconnaissance plats cuisinés  
• **DrinkID:** Classification boissons/cocktails  
• **MenuScanner:** Analyse nutritionnelle visuelle  
• **KitchenGuard:** Hygiène et sécurité cuisine

**📱 Tech & Digital**  
• **PhonePolice:** Détection téléphone au volant  
• **ScreenTime:** Surveillance usage écrans  
• **DeviceTracker:** Comptage appareils électroniques  
• **CableDetector:** Identification types de câbles

**🌱 Environnement & Nature**  
• **BirdWatcher:** Reconnaissance espèces d'oiseaux  
• **WasteSort:** Tri automatique déchets  
• **PlantID:** Identification plantes/fleurs  
• **AnimalTracker:** Détection animaux sauvages

**🏠 Maison & Lifestyle**  
• **PetWatch:** Surveillance animaux domestiques  
• **HomeGuard:** Détection intrusions/objets suspects  
• **ToySort:** Classification jouets enfants  
• **BookShelf:** Organisation bibliothèque

**🎯 Sport & Loisirs**  
• **BallTracker:** Suivi balles/ballons sports  
• **GymBuddy:** Détection exercices fitness  
• **CardReader:** Reconnaissance cartes à jouer  
• **SkateSpotter:** Classification tricks skateboard

**🎯 Critères de choix :** Disponibilité dataset Roboflow, faisabilité webcam, scope réalisable en 4 jours, potentiel business clair.

## 👥 Équipes Constituées (Groupes de 3)

✅ Groupe 1

Khadija A.

Michael

Elliandy

✅ Groupe 2

Victor

David

Dorothée

✅ Groupe 3

Malek

Maxime

Sami

✅ Groupe 4

Raouf

Nicolas G

Ludivine

✅ Groupe 5

Wael

Gauthier

Antoine

✅ Groupe 6

Samuel

Hacène

Nicolas C

🕒 PRÉSENTATION FINALE : VENDREDI À 15H

## 🛠️ Stack Technique Recommandée

YOLOv8/v9/v10

Python

OpenCV

Ultralytics

Roboflow

Google Colab

Gradio/Streamlit

Webcam Integration

## 📋 Présentation Finale (5 slides max)

**Contenu obligatoire :**

*   Problématique métier choisie
*   Pitch du POC (valeur ajoutée)
*   Dataset utilisé (source, taille, classes)
*   Métriques d'entraînement (précision, mAP, recall, etc.)
*   Difficultés rencontrées et solutions trouvées
*   **Démo live avec webcam**

## 🔗 Ressources Utiles

[📚 YOLO Documentation](https://docs.ultralytics.com/) [🎯 Roboflow](https://roboflow.com/) [🖥️ Gradio](https://gradio.app/) [⚡ Streamlit](https://streamlit.io/) [☁️ Google Colab](https://colab.research.google.com/) [📁 GitHub](https://github.com/)

**🚀 Conseils pour réussir :**

*   Commencez simple : choisissez un dataset avec peu de classes
*   Testez votre webcam dès le jour 2
*   Documentez vos expériences et échecs
*   Préparez un plan B si l'entraînement ne converge pas
*   Privilégiez une démo qui fonctionne plutôt qu'un modèle parfait
