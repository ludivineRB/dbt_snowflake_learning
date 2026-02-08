# 10 - Logique, Boucles et Blocs Dynamiques

[← 09 - Remote State](09-remote-state-gcs.md) | [🏠 Accueil](../00-README.md) | [11 - Modules →](11-modules.md)

---

## 1. La boucle `count`

Utile pour créer plusieurs ressources identiques.

```hcl
resource "google_compute_instance" "cluster" {
  count = 3
  name  = "node-${count.index}"
  # ...
}
```

---

## 2. La boucle `for_each`

Recommandée pour créer des ressources à partir d'une liste ou d'un map. Plus flexible que `count`.

```hcl
variable "buckets" {
  type    = set(string)
  default = ["raw", "processed", "analytics"]
}

resource "google_storage_bucket" "data_layers" {
  for_each = var.buckets
  name     = "my-project-${each.value}"
  location = "EU"
}
```

---

## 3. Les expressions `for`

Pour transformer des listes ou des maps.

```hcl
output "bucket_names" {
  value = [for b in google_storage_bucket.data_layers : b.name]
}
```

---

## 4. Blocs Dynamiques (`dynamic`)

Permet de générer des sous-blocs (comme des règles firewall) de manière répétitive.

```hcl
variable "allowed_ports" {
  type    = list(number)
  default = [80, 443, 8080]
}

resource "google_compute_firewall" "multi_port" {
  name    = "allow-multi"
  network = "default"

  dynamic "allow" {
    for_each = var.allowed_ports
    content {
      protocol = "tcp"
      ports    = [allow.value]
    }
  }
}
```

---

[← 09 - Remote State](09-remote-state-gcs.md) | [🏠 Accueil](../00-README.md) | [11 - Modules →](11-modules.md)
