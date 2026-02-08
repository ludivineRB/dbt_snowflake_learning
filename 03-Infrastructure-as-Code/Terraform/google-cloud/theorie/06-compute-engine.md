# 06 - Compute Engine (VMs)

[← 05 - Cloud Storage](05-cloud-storage.md) | [🏠 Accueil](../00-README.md) | [07 - Cloud SQL →](07-cloud-sql.md)

---

## 1. Introduction à Compute Engine

Compute Engine permet de lancer des instances de machines virtuelles sur l'infrastructure de Google.

---

## 2. Création d'une instance VM

```hcl
resource "google_compute_instance" "app_server" {
  name         = "app-server-01"
  machine_type = "e2-medium"
  zone         = "europe-west1-b"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
      size  = 20 # Go
    }
  }

  network_interface {
    network    = google_compute_network.vpc_network.id
    subnetwork = google_compute_subnetwork.subnet_west1.id

    access_config {
      # Bloc vide = Alloue une adresse IP publique (Optionnel)
    }
  }

  tags = ["ssh-enabled"] # Correspond à la règle firewall créée au module 04

  metadata_startup_script = "echo 'Hello World' > /tmp/hello.txt"
}
```

---

## 3. Machine Types

- **e2-micro/small** : Pour les petits tests.
- **n2-standard** : Usage général.
- **c2-standard** : Optimisé pour le calcul (Compute optimized).
- **m3-ultramem** : Optimisé pour la RAM (In-memory databases).

---

## 4. Service Account pour la VM

Bonne pratique : Attacher un Service Account avec les droits minimaux nécessaires à la VM.

```hcl
service_account {
  email  = "my-sa@project.iam.gserviceaccount.com"
  scopes = ["cloud-platform"]
}
```

---

## 5. Preemptible Instances (Spot VMs)

Pour réduire les coûts jusqu'à 80% pour des traitements batch (Data processing) acceptant les interruptions.

```hcl
scheduling {
  preemptible       = true
  automatic_restart = false
}
```

---

[← 05 - Cloud Storage](05-cloud-storage.md) | [🏠 Accueil](../00-README.md) | [07 - Cloud SQL →](07-cloud-sql.md)
