# 04 - VPC et Networking

[← 03 - Provider](03-provider-configuration.md) | [🏠 Accueil](../00-README.md) | [05 - Cloud Storage →](05-cloud-storage.md)

---

## 1. Introduction au VPC (Virtual Private Cloud)

Sur GCP, le VPC est une ressource globale. Contrairement à Azure où le VNET est régional, un VPC GCP peut avoir des sous-réseaux (Subnets) dans n'importe quelle région du monde.

---

## 2. Création d'un VPC

Par défaut, GCP crée un VPC "default" avec des sous-réseaux automatiques. En production, **il faut toujours désactiver ce mode automatique**.

```hcl
resource "google_compute_network" "vpc_network" {
  name                    = "my-custom-vpc"
  auto_create_subnetworks = false
}
```

---

## 3. Création des Sous-réseaux (Subnets)

Les sous-réseaux sont régionaux.

```hcl
resource "google_compute_subnetwork" "subnet_west1" {
  name          = "subnet-europe-west1"
  ip_cidr_range = "10.0.1.0/24"
  region        = "europe-west1"
  network       = google_compute_network.vpc_network.id
}
```

---

## 4. Firewall Rules

Pour autoriser le trafic, vous devez créer des règles de pare-feu.

```hcl
resource "google_compute_firewall" "allow_ssh" {
  name    = "allow-ssh"
  network = google_compute_network.vpc_network.name

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  source_ranges = ["0.0.0.0/0"] # Attention: À restreindre en production !
  target_tags   = ["ssh-enabled"]
}
```

---

## 5. Dépendances Implicites

Notez que dans le code ci-dessus, `google_compute_subnetwork` référence `google_compute_network.vpc_network.id`. Terraform comprend automatiquement qu'il doit créer le réseau **avant** le sous-réseau.

---

[← 03 - Provider](03-provider-configuration.md) | [🏠 Accueil](../00-README.md) | [05 - Cloud Storage →](05-cloud-storage.md)
