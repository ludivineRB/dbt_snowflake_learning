# 07 - Cloud SQL (Bases de données)

[← 06 - Compute Engine](06-compute-engine.md) | [🏠 Accueil](../00-README.md) | [08 - Variables, tfvars et Outputs →](08-variables-outputs.md)

---

## 1. Introduction à Cloud SQL

Cloud SQL est le service managé pour PostgreSQL, MySQL et SQL Server.

---

## 2. Création d'une instance de base de données

```hcl
resource "google_sql_database_instance" "main_db" {
  name             = "main-db-instance"
  database_version = "POSTGRES_15"
  region           = "europe-west1"

  settings {
    tier = "db-f1-micro" # Taille de l'instance

    backup_configuration {
      enabled = true
    }

    ip_configuration {
      ipv4_enabled    = true # Autorise IP publique (Optionnel)
      private_network = google_compute_network.vpc_network.id # Connexion interne VPC
    }
  }

  deletion_protection = false # À activer en production !
}
```

---

## 3. Création d'une base et d'un utilisateur

```hcl
resource "google_sql_database" "database" {
  name     = "app_database"
  instance = google_sql_database_instance.main_db.name
}

resource "google_sql_user" "users" {
  name     = "app_user"
  instance = google_sql_database_instance.main_db.name
  password = "password-secret" # Mieux : Utiliser une variable sensible
}
```

---

## 4. Accès via Private IP (VPC Peering)

Pour une sécurité maximale, désactivez l'IP publique et utilisez l'IP privée. Cela nécessite une configuration réseau spécifique appelée "Private Services Access".

---

[← 06 - Compute Engine](06-compute-engine.md) | [🏠 Accueil](../00-README.md) | [08 - Variables, tfvars et Outputs →](08-variables-outputs.md)
