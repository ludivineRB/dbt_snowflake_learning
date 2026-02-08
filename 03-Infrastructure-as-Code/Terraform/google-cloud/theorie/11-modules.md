# 11 - Modules et Réutilisabilité

[← 10 - Logique](10-logic-loops-dynamic.md) | [🏠 Accueil](../00-README.md) | [12 - Data Sources →](12-data-sources.md)

---

## 1. Pourquoi utiliser des Modules ?

Les modules permettent de :
- Regrouper des ressources logiquement (ex: un module "réseau").
- Éviter la duplication de code.
- Créer des standards d'infrastructure au sein d'une entreprise.

---

## 2. Structure d'un Module

Un module est simplement un dossier contenant des fichiers `.tf`.
```
modules/gcs_bucket/
├── main.tf
├── variables.tf
└── outputs.tf
```

---

## 3. Appeler un Module

```hcl
module "storage_env" {
  source = "./modules/gcs_bucket"

  bucket_name = "my-app-data"
  location    = "europe-west1"
}
```

---

## 4. Terraform Registry

Vous pouvez aussi utiliser des modules créés par la communauté ou par Google.

```hcl
module "network" {
  source  = "terraform-google-modules/network/google"
  version = "~> 9.0"

  project_id   = var.project_id
  network_name = "custom-vpc"
  # ...
}
```

---

[← 10 - Logique](10-logic-loops-dynamic.md) | [🏠 Accueil](../00-README.md) | [12 - Data Sources →](12-data-sources.md)
