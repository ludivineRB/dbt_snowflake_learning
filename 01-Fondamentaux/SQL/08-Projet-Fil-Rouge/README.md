# Projet Fil Rouge : Analyse E-Commerce

[← Module 07](../07-Programmation-Securite/02-transactions-acid.md) | [🏠 Accueil](../README.md)

---

L'objectif de ce projet est de mettre en pratique l'ensemble des concepts abordés dans la formation SQL.

## Le Scénario
Vous venez d'être recruté par "DataShop", une boutique en ligne. Votre mission est d'extraire des insights (analyses) à partir de leur base de données pour aider le département marketing.

## Les Données
Utilisez les tables que vous avez importées au [Module 00](../00-Preparation-Environnement/02-creation-bdd-import.md) :
1. `customers` : Informations clients.
2. `products` : Catalogue des articles.
3. `orders` : En-têtes des commandes.
4. `order_items` : Détail des produits achetés dans chaque commande.

## Vos Missions

### Mission 1 : Exploration (DQL)
- Listez les 5 produits les plus chers.
- Trouvez les clients qui n'ont jamais passé de commande.

### Mission 2 : Analyse de Ventes (Agrégations & Jointures)
- Calculez le Chiffre d'Affaires (CA) total par catégorie de produit.
- Quel est le panier moyen (montant moyen d'une commande) ?

### Mission 3 : Fidélisation (Window Functions)
- Classez les clients par montant total dépensé.
- Pour chaque commande, affichez le montant de la commande précédente du même client.

### Mission 4 : Nettoyage & Transformation (DDL/DML)
- Créez une vue `v_sales_summary` qui joint les commandes aux clients et aux produits.
- Ajoutez un nouveau produit "Souris Gaming" à 45€ dans la catégorie "Électronique".

---

[← Module 07](../07-Programmation-Securite/02-transactions-acid.md) | [🏠 Accueil](../README.md)