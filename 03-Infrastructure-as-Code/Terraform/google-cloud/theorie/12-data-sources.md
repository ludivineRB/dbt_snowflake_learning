# 12 - Data Sources

[← 11 - Modules](11-modules.md) | [🏠 Accueil](../00-README.md) | [13 - Best Practices →](13-best-practices-security.md)

---

## 1. Qu'est-ce qu'une Data Source ?

Une Data Source permet de récupérer des informations sur des ressources qui existent déjà sur GCP (et qui n'ont pas été forcément créées par votre code Terraform actuel).

---

## 2. Exemple : Récupérer les zones disponibles

```hcl
data "google_compute_zones" "available" {
  region = "europe-west1"
  state  = "UP"
}

resource "google_compute_instance" "app" {
  # Utilise la première zone disponible de la région
  zone = data.google_compute_zones.available.names[0]
  # ...
}
```

---

## 3. Exemple : Récupérer un réseau existant

```hcl
data "google_compute_network" "existing_vpc" {
  name = "default"
}

resource "google_compute_subnetwork" "new_subnet" {
  name    = "extra-subnet"
  network = data.google_compute_network.existing_vpc.id
  # ...
}
```

---

## 4. Exemple : Récupérer l'ID du projet actuel

```hcl
data "google_project" "current" {}

output "project_number" {
  value = data.google_project.current.number
}
```

---

[← 11 - Modules](11-modules.md) | [🏠 Accueil](../00-README.md) | [13 - Best Practices →](13-best-practices-security.md)
