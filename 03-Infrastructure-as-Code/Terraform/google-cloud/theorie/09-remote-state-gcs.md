# 09 - Remote State sur GCS

[← 08 - Variables](08-variables-outputs.md) | [🏠 Accueil](../00-README.md) | [10 - Logique, Boucles et Blocs Dynamiques →](10-logic-loops-dynamic.md)

---

## 1. Pourquoi utiliser un Remote State ?

Par défaut, Terraform stocke l'état (`terraform.tfstate`) localement.
❌ **Problèmes** : Travail en équipe impossible, risque de perte du fichier, secrets en clair sur votre machine.

✅ **Solution** : Stocker l'état dans un bucket Cloud Storage sécurisé.

---

## 2. Configuration du Backend GCS

```hcl
terraform {
  backend "gcs" {
    bucket  = "mon-terraform-state-bucket"
    prefix  = "terraform/state"
  }
}
```

---

## 3. Mise en place étape par étape

1. **Créer le bucket** (manuellement ou via un script initial) :
   ```bash
   gcloud storage buckets create gs://mon-terraform-state-bucket --location=EU
   ```
2. **Ajouter le bloc backend** dans votre `main.tf`.
3. **Initialiser** :
   ```bash
   terraform init
   ```
   Terraform détectera le nouveau backend et vous proposera de copier votre état local vers le bucket.

---

## 4. State Locking

Sur GCP, le backend GCS supporte nativement le **locking**. Si deux personnes tentent un `apply` en même temps, GCP bloque l'exécution de la deuxième pour éviter de corrompre l'état.

---

## 5. Recommandations de Sécurité

- Activez le **Versioning** sur le bucket de state.
- Restreignez l'accès au bucket aux seuls administrateurs Cloud.
- Utilisez des buckets séparés par environnement (Dev, Prod).

---

[← 08 - Variables](08-variables-outputs.md) | [🏠 Accueil](../00-README.md) | [10 - Logique, Boucles et Blocs Dynamiques →](10-logic-loops-dynamic.md)
