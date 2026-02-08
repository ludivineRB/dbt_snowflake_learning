# 08 - Variables, tfvars et Outputs

[← 07 - Cloud SQL](07-cloud-sql.md) | [🏠 Accueil](../00-README.md) | [09 - Remote State sur GCS →](09-remote-state-gcs.md)

---

## 1. Déclarer des Variables (variables.tf)

Permet de paramétrer votre code Terraform.

```hcl
variable "project_id" {
  type        = string
  description = "L'ID du projet GCP"
}

variable "region" {
  type    = string
  default = "europe-west1"
}

variable "vm_count" {
  type    = number
  default = 1
}
```

---

## 2. Définir des valeurs (terraform.tfvars)

Le fichier `terraform.tfvars` est chargé automatiquement par Terraform.

```hcl
project_id = "mon-projet-data-123"
region     = "europe-west9" # Paris
vm_count   = 2
```

---

## 3. Variables Sensibles

Pour les mots de passe, utilisez `sensitive = true` pour qu'ils n'apparaissent pas dans les logs.

```hcl
variable "db_password" {
  type      = string
  sensitive = true
}
```

---

## 4. Les Outputs (outputs.tf)

Les outputs affichent des informations utiles après le `apply` (comme une IP publique).

```hcl
output "vm_public_ip" {
  value       = google_compute_instance.app_server.network_interface[0].access_config[0].nat_ip
  description = "L'IP publique de la VM"
}

output "bucket_url" {
  value = google_storage_bucket.data_lake.url
}
```

---

[← 07 - Cloud SQL](07-cloud-sql.md) | [🏠 Accueil](../00-README.md) | [09 - Remote State sur GCS →](09-remote-state-gcs.md)
