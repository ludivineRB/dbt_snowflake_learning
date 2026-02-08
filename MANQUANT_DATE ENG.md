# 🚩 Modules Manquants : Certification Expert Data Engineer (Niveau 7)

Ce document récapitule les compétences et contenus exigés par le référentiel RNCP mais absents ou insuffisamment détaillés dans la structure actuelle de la formation.

## 🟢 BLOC 1 : Piloter la conduite d'un projet data (Le plus gros manque)
Le référentiel insiste sur la dimension "Chef de Projet / Architecte".

- **Méthodologies de Cadrage** : 
    - Analyse de faisabilité technique et financière.
    - Utilisation des méthodes **SMART** (objectifs) et **RICE** (priorisation).
    - Création de grilles d'entretien pour l'audit des besoins métiers.
- **Gouvernance & Conformité (Omniprésent dans le référentiel)** :
    - **RGPD Avancé** : Rédaction d'un registre des traitements, procédures de purge automatique, analyse d'impact.
    - **Éco-conception** : Stratégie d'éco-responsabilité appliquée à la donnée (calcul de l'empreinte carbone des traitements).
    - **Accessibilité** : Mise en œuvre des normes d'accessibilité (RGAA) dans les rapports et outils data.
- **Veille Stratégique** :
    - Mise en place d'un protocole de veille technique et réglementaire (choix d'outils d'agrégation, partage de synthèses).

## 🔵 BLOC 2 : Collecte, stockage et mise à disposition
La partie technique est bien entamée, mais il manque des formalismes de conception.

- **Modélisation de Données** :
    - Conception de Modèles Conceptuels (MCD) et Physiques (MPD) via la **méthode MERISE**.
- **Web Scraping Industriel** :
    - Automatisation et pérennisation de la collecte via scraping (gestion des proxies, rotation d'agents, légalité).
- **Documentation d'API** :
    - Standardisation via **OpenAPI / Swagger** systématique.

## 🟣 BLOC 3 : Entrepôt de données (Data Warehouse)
Il manque la dimension théorique avancée de l'architecture DWH.

- **Modélisation Dimensionnelle Avancée** :
    - Gestion des variations dans le temps (**SCD - Slowly Changing Dimensions Type 1, 2, 3** de Ralph Kimball).
    - Justification des approches **Top-Down (Inmon)** vs **Bottom-Up (Kimball)**.
- **Maintenance & SLA** :
    - Définition et suivi des **SLA (Service Level Agreements)**.
    - Mise en place de tableaux de bord de supervision de la qualité de l'entrepôt.
    - Procédures de backup partiel/complet et plans de reprise d'activité (PRA).

## 🟡 BLOC 4 : Data Lake & Collecte Massive
Le cours doit couvrir la gestion du cycle de vie de la donnée massive.

- **Data Cataloging** :
    - Choix et mise en place d'un outil de **Catalogue de données** (Métadonnées, lignage de données/lineage).
    - Programmation des procédures de suppression automatique liées au cycle de vie (rétention).
- **Gouvernance des accès** :
    - Implémentation de règles de sécurité par groupes (RBAC) sur des volumes massifs.

---

## 🛠️ Synthèse des cours à créer (Action Plan)

1.  **Module "Gestion de Projet Data"** (Cadrage, SMART, RICE, Agile Data).
2.  **Module "Data Governance & Ethics"** (RGPD, Éthique IA, Éco-conception, Accessibilité).
3.  **Module "Modélisation Avancée"** (Merise pour le SQL, Kimball pour le DWH, SCD).
4.  **Module "Data Quality & Maintenance"** (SLA, Tests de qualité, Lineage, Catalogage).
5.  **Atelier "Veille Technologique"** (Méthodologie de veille pour l'examen).
