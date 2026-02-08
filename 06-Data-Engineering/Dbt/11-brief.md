# Brief : Pipeline dbt pour l'Analyse des Ventes

## 📝 Contexte

Vous etes **Data Engineer** dans une entreprise de e-commerce. L'equipe data analytics a besoin d'un **data warehouse propre** pour alimenter ses dashboards. Les donnees brutes sont disponibles dans une base PostgreSQL, mais elles sont desorganisees, non testees et non documentees.

Votre mission : construire le **pipeline de transformation complet** avec dbt Core, depuis les donnees brutes jusqu'aux tables analytiques pretes pour le reporting.

---

## Informations generales

| Critere | Valeur |
|---------|--------|
| **Duree** | 1 jour (7 heures) |
| **Niveau** | Intermediaire |
| **Modalite** | Individuel |
| **Technologies** | dbt Core, PostgreSQL, Docker, Git |
| **Prerequis** | Chapitres 0 a 9 du cours dbt |

---

## 🎯 Objectifs pedagogiques

A l'issue de ce brief, vous serez capable de :

- Construire un pipeline dbt complet (**staging → intermediate → mart**)
- Implementer des **tests de qualite** exhaustifs
- Documenter le projet pour l'equipe
- Deployer en local avec **dbt Core + PostgreSQL**
- Utiliser les **bonnes pratiques** de structure et de nommage

---

## 📊 Donnees sources

Les donnees sont fournies sous forme de fichiers CSV a charger via `dbt seed`, ou directement dans PostgreSQL.

### Tables disponibles

| Table | Colonnes | Description |
|-------|----------|-------------|
| `raw_customers` | `id`, `first_name`, `last_name`, `email`, `created_at`, `country` | Clients de la plateforme |
| `raw_orders` | `id`, `customer_id`, `order_date`, `status`, `total_amount` | Commandes passees |
| `raw_order_items` | `id`, `order_id`, `product_id`, `quantity`, `unit_price` | Lignes de commande |
| `raw_products` | `id`, `name`, `category`, `unit_price` | Catalogue de produits |

### Statuts possibles des commandes

| Statut | Description |
|--------|-------------|
| `pending` | En attente de validation |
| `completed` | Commande livree et payee |
| `shipped` | En cours de livraison |
| `cancelled` | Commande annulee |

### Volume attendu

Fournissez des seeds realistes avec au minimum :
- **10 clients** avec des pays varies
- **20 commandes** reparties sur plusieurs mois
- **30 lignes de commande**
- **8 produits** dans au moins 3 categories

> 💡 **Conseil** : Variez les scenarios (clients sans commande, commandes annulees, clients avec plusieurs commandes) pour tester la robustesse de vos modeles.

---

## 🏗️ Architecture cible

```
seeds (CSV)
    ↓
staging (stg_)        → Nettoyage, renommage, typage
    ↓
intermediate (int_)   → Jointures, logique metier
    ↓
marts (fct_ / dim_)   → Tables analytiques finales
```

---

## 📦 Livrables attendus

### 1. Staging models (`stg_`)

Pour chaque table source, un modele staging qui :
- Renomme les colonnes (ex: `id` → `customer_id`)
- Nettoie les donnees (trim, lower, cast)
- Est materialise en **view**

Modeles attendus :
- `stg_customers.sql`
- `stg_orders.sql`
- `stg_order_items.sql`
- `stg_products.sql`

### 2. Intermediate models (`int_`)

Au moins un modele intermediaire qui prepare la logique metier :
- `int_order_items.sql` : jointure entre les lignes de commande et les produits

Materialisation recommandee : **ephemeral**

### 3. Mart models

#### `fct_orders.sql` — Table de faits des commandes

| Colonne | Description |
|---------|-------------|
| `order_id` | Identifiant de la commande |
| `customer_id` | Identifiant du client |
| `order_date` | Date de la commande |
| `status` | Statut de la commande |
| `total_amount` | Montant total |
| `nb_items` | Nombre de lignes de commande |
| `total_quantity` | Quantite totale d'articles |
| `nb_distinct_products` | Nombre de produits differents |

#### `dim_customers.sql` — Dimension clients avec lifetime value

| Colonne | Description |
|---------|-------------|
| `customer_id` | Identifiant du client |
| `full_name` | Nom complet |
| `email` | Email normalise |
| `country` | Pays |
| `created_at` | Date de creation du compte |
| `nb_orders` | Nombre de commandes (hors annulees) |
| `lifetime_value` | Montant total depense (commandes completees) |
| `first_order_date` | Date de premiere commande |
| `last_order_date` | Date de derniere commande |
| `customer_segment` | Segment (Prospect / Nouveau / Regulier / Fidele) |

#### `dim_products.sql` — Dimension produits avec metriques de ventes

| Colonne | Description |
|---------|-------------|
| `product_id` | Identifiant du produit |
| `product_name` | Nom du produit |
| `category` | Categorie |
| `unit_price` | Prix unitaire |
| `nb_orders` | Nombre de commandes contenant ce produit |
| `total_quantity_sold` | Quantite totale vendue |
| `total_revenue` | Revenu total genere |

#### `mart_monthly_revenue.sql` — Agregation mensuelle du chiffre d'affaires

| Colonne | Description |
|---------|-------------|
| `month` | Mois (format YYYY-MM-01) |
| `nb_orders` | Nombre de commandes |
| `total_revenue` | Chiffre d'affaires |
| `nb_unique_customers` | Nombre de clients distincts |
| `avg_order_value` | Panier moyen |
| `revenue_previous_month` | CA du mois precedent |
| `revenue_growth_pct` | Pourcentage de croissance |

### 4. Tests de qualite

#### Tests generiques obligatoires

| Type | Cible |
|------|-------|
| `unique` | Toutes les cles primaires |
| `not_null` | Toutes les cles primaires + colonnes critiques |
| `relationships` | Cles etrangeres (customer_id, product_id, order_id) |
| `accepted_values` | Colonne `status` des commandes |

#### Tests personnalises (au moins 2)

Exemples :
- Verifier qu'**aucune commande n'a un montant negatif**
- Verifier que la **date de premiere commande** est posterieure a la **date de creation du compte**
- Verifier la **coherence** entre `total_amount` et la somme des lignes de commande

### 5. Documentation

- **Descriptions** sur tous les modeles dans `schema.yml`
- **Descriptions** sur toutes les colonnes des modeles marts
- Documentation accessible via `dbt docs serve`

### 6. Seeds

- Fichiers CSV dans `seeds/` pour les 4 tables sources
- Au moins une **table de reference** supplementaire (ex: `ref_countries.csv` avec code pays et nom)

### 7. Snapshot

Creez un **snapshot SCD Type 2** sur la table customers pour tracer l'evolution des donnees clients :

**`snapshots/scd_customers.sql`** :
- Strategie : `check` sur toutes les colonnes (ou `timestamp` si colonne `updated_at` disponible)
- Cle unique : `customer_id`
- Schema cible : `snapshots`

### 8. Documentation generee

```bash
dbt docs generate
dbt docs serve
```

Le graphe de lignee doit etre complet et les descriptions visibles.

---

## 📁 Structure du projet attendue

```
ecommerce-dbt/
├── dbt_project.yml
├── packages.yml
├── docker-compose.yml
├── Makefile
├── README.md                          # Instructions de setup
├── .gitignore
├── seeds/
│   ├── raw_customers.csv
│   ├── raw_orders.csv
│   ├── raw_order_items.csv
│   ├── raw_products.csv
│   └── ref_countries.csv
├── models/
│   ├── staging/
│   │   ├── sources.yml
│   │   ├── schema.yml
│   │   ├── stg_customers.sql
│   │   ├── stg_orders.sql
│   │   ├── stg_order_items.sql
│   │   └── stg_products.sql
│   ├── intermediate/
│   │   └── int_order_items.sql
│   └── marts/
│       ├── schema.yml
│       ├── fct_orders.sql
│       ├── dim_customers.sql
│       ├── dim_products.sql
│       └── mart_monthly_revenue.sql
├── snapshots/
│   └── scd_customers.sql
├── tests/
│   ├── assert_no_negative_order_total.sql
│   └── assert_first_order_after_signup.sql
└── macros/
    └── (macros optionnelles)
```

---

## ✅ Criteres d'evaluation

### Fonctionnement general

- [ ] Le projet compile et s'execute (`dbt build`) **sans erreur**
- [ ] Tous les tests passent (`dbt test` → 0 ERROR)
- [ ] La documentation est accessible via `dbt docs serve`
- [ ] Le graphe de lignee est complet et coherent

### Qualite du code SQL

- [ ] Utilisation de **CTEs** (pas de sous-requetes imbriquees)
- [ ] Nommage **coherent** (stg_, int_, fct_, dim_, mart_)
- [ ] Materialisations **appropriees** (view, ephemeral, table)
- [ ] Code SQL **lisible** et commente

### Qualite des tests

- [ ] Tests `unique` et `not_null` sur toutes les cles primaires
- [ ] Tests `relationships` sur les cles etrangeres
- [ ] Tests `accepted_values` sur les champs de statut
- [ ] Au moins **2 tests personnalises**

### Documentation

- [ ] Descriptions sur **tous les modeles**
- [ ] Descriptions sur **toutes les colonnes** des marts
- [ ] `schema.yml` complets pour staging et marts

### Infrastructure et Git

- [ ] `docker-compose.yml` fonctionnel pour PostgreSQL
- [ ] `Makefile` avec les commandes essentielles
- [ ] `README.md` avec les instructions de setup
- [ ] `.gitignore` correct (target/, dbt_packages/, logs/, .env)
- [ ] Historique Git propre avec des **commits conventionnels**

### Grille de notation

| Critere | Points |
|---------|--------|
| Infrastructure (Docker, profiles.yml, dbt debug) | **/10** |
| Seeds (4 tables + 1 reference, donnees realistes) | **/10** |
| Modeles staging (4 modeles, nettoyage, view) | **/15** |
| Modele intermediaire (jointure, ephemeral) | **/5** |
| Modeles marts (fct_orders, dim_customers, dim_products, mart_monthly_revenue) | **/20** |
| Tests generiques (unique, not_null, relationships, accepted_values) | **/10** |
| Tests personnalises (2 minimum) | **/10** |
| Snapshot SCD Type 2 | **/5** |
| Documentation (descriptions, dbt docs) | **/10** |
| Git, README, Makefile | **/5** |
| **Total** | **/100** |

---

## 💡 Bonus

Les elements suivants ne sont pas obligatoires mais valorises :

- **Modele incremental** : Creez `mart_daily_orders` en mode incremental avec lookback
- **Macro custom reutilisable** : Par exemple `clean_string()` ou `generate_surrogate_key()`
- **GitHub Actions CI** : Pipeline de validation automatique sur les pull requests
- **Exposure** : Declarez un dashboard fictif consommant vos marts

### Exemple d'exposure

Creez `models/marts/exposures.yml` :

```yaml
version: 2

exposures:
  - name: dashboard_ventes
    type: dashboard
    maturity: medium
    description: "Dashboard de suivi des ventes pour la direction"
    depends_on:
      - ref('fct_orders')
      - ref('dim_customers')
      - ref('dim_products')
      - ref('mart_monthly_revenue')
    owner:
      name: "Equipe Data"
      email: "data-team@ecommerce.fr"
```

---

## 📚 Ressources

- [Documentation officielle dbt](https://docs.getdbt.com/)
- [dbt Best Practices](https://docs.getdbt.com/best-practices)
- [dbt Style Guide](https://github.com/dbt-labs/corp/blob/main/dbt_style_guide.md)
- [Packages dbt](https://hub.getdbt.com/)
- [Cours dbt - Chapitres 0 a 9](./README.md)

---

## 🚀 Pour demarrer

```bash
# 1. Creer le dossier du projet
mkdir ecommerce-dbt && cd ecommerce-dbt

# 2. Demarrer PostgreSQL
docker compose up -d

# 3. Creer l'environnement Python
uv init && uv add dbt-core dbt-postgres

# 4. Initialiser le projet dbt
dbt init ecommerce

# 5. Configurer profiles.yml
# → Voir Chapitre 9, section 3

# 6. Verifier la connexion
dbt debug

# 7. C'est parti !
```

> 💡 **Conseil** : Commitez regulierement votre travail avec des messages conventionnels (`feat:`, `fix:`, `test:`, `docs:`). Cela facilitera la relecture et l'evaluation.

---

**Etape precedente** : [Exercices dbt](10-exercices.md)
**Retour au sommaire** : [README](README.md)
