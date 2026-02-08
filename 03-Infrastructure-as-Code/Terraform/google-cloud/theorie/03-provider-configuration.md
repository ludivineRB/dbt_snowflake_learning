# 03 - Configuration du Provider et Projet

[← 02 - WIF](02-workload-identity-federation.md) | [🏠 Accueil](../00-README.md) | [04 - VPC et Networking →](04-vpc-network.md)

---

## 1. Bloc Terraform

Le bloc `terraform` définit les exigences du provider (source et version).

```hcl
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}
```

---

## 2. Bloc Provider

Le bloc `provider` configure les paramètres globaux de connexion à GCP.

```hcl
provider "google" {
  project = "VOTRE_PROJECT_ID"
  region  = "europe-west1"
  zone    = "europe-west1-b"
}
```

### Paramètres :
- **project** : L'identifiant unique de votre projet Google Cloud.
- **region** : La région par défaut pour les ressources régionales (ex: Storage, Cloud SQL).
- **zone** : La zone par défaut pour les ressources zonales (ex: Instances Compute Engine).

---

## 3. Bonne Pratique : Ne pas hardcoder l'ID de projet

Il est recommandé d'utiliser des variables pour l'ID de projet afin de pouvoir déployer le même code sur plusieurs environnements (Dev, Prod).

```hcl
provider "google" {
  project = var.project_id
  region  = var.region
}
```

---

## 4. Activer les APIs GCP via Terraform

Sur GCP, les services (Compute, SQL, etc.) doivent être activés avant d'être utilisés. Vous pouvez le faire via Terraform :

```hcl
resource "google_project_service" "compute_api" {
  project = "VOTRE_PROJECT_ID"
  service = "compute.googleapis.com"

  disable_on_destroy = false
}
```

---

[← 02 - WIF](02-workload-identity-federation.md) | [🏠 Accueil](../00-README.md) | [04 - VPC et Networking →](04-vpc-network.md)
