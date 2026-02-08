# 05 - Cloud Storage (Buckets)

[← 04 - VPC](04-vpc-network.md) | [🏠 Accueil](../00-README.md) | [06 - Compute Engine →](06-compute-engine.md)

---

## 1. Introduction à Cloud Storage (GCS)

GCS est le service de stockage d'objets de Google (équivalent à Azure Blob Storage). C'est le socle de tout Data Lake.

---

## 2. Création d'un Bucket

Les noms de buckets doivent être **uniques au niveau mondial**.

```hcl
resource "google_storage_bucket" "data_lake" {
  name          = "my-unique-data-lake-suffix"
  location      = "EU" # Multi-regional
  force_destroy = true # Autorise Terraform à supprimer le bucket même s'il n'est pas vide

  uniform_bucket_level_access = true # Bonne pratique de sécurité

  versioning {
    enabled = true
  }
}
```

---

## 3. Classes de Stockage

Vous pouvez définir la classe pour optimiser les coûts :
- **STANDARD** : Accès fréquent (données actives).
- **NEARLINE** : Accès mensuel (backups).
- **COLDLINE** : Accès trimestriel.
- **ARCHIVE** : Accès annuel (archivage légal).

```hcl
storage_class = "NEARLINE"
```

---

## 4. Cycle de vie des objets (Lifecycle)

Automatisez la suppression ou le changement de classe des données anciennes.

```hcl
lifecycle_rule {
  condition {
    age = 30 # jours
  }
  action {
    type = "SetStorageClass"
    storage_class = "COLDLINE"
  }
}
```

---

## 5. Téléverser un fichier

```hcl
resource "google_storage_bucket_object" "script" {
  name   = "hello.py"
  source = "./scripts/hello.py"
  bucket = google_storage_bucket.data_lake.name
}
```

---

[← 04 - VPC](04-vpc-network.md) | [🏠 Accueil](../00-README.md) | [06 - Compute Engine →](06-compute-engine.md)
