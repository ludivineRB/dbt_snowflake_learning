# 02 - Workload Identity Federation (Fédéral Pool)

[← 01 - Installation](01-installation-auth.md) | [🏠 Accueil](../00-README.md) | [03 - Provider configuration →](03-provider-configuration.md)

---

## 1. Pourquoi Workload Identity Federation ?

Traditionnellement, pour authentifier Terraform en dehors de GCP (par exemple dans une CI/CD comme GitHub Actions), on utilisait des **Service Account Keys** (fichiers JSON).
❌ **Problème** : Ces clés sont des secrets longue durée, difficiles à gérer et dangereuses si elles fuitent.

✅ **Solution** : Workload Identity Federation (WIF) permet d'accorder des droits à des identités externes (GitHub, GitLab, Azure, AWS) sans jamais utiliser de clé JSON.

---

## 2. Concepts Clés

- **Workload Identity Pool** (Le fameux "Fédéral Pool") : Un conteneur pour vos identités externes.
- **Workload Identity Provider** : Définit la relation de confiance entre GCP et l'émetteur externe (ex: GitHub).
- **Service Account Impersonation** : L'identité externe "emprunte" l'identité d'un Service Account GCP pour agir.

---

## 3. Mise en place (Exemple pour GitHub)

### Étape 1 : Créer le Pool
```bash
gcloud iam workload-identity-pools create "my-pool" 
    --project="VOTRE_PROJECT_ID" 
    --location="global" 
    --display-name="Terraform CI Pool"
```

### Étape 2 : Créer le Provider
```bash
gcloud iam workload-identity-pools providers create-oidc "my-provider" 
    --project="VOTRE_PROJECT_ID" 
    --location="global" 
    --workload-identity-pool="my-pool" 
    --display-name="GitHub Provider" 
    --attribute-mapping="google.subject=assertion.sub,attribute.repository=assertion.repository" 
    --issuer-uri="https://token.actions.githubusercontent.com"
```

### Étape 3 : Lier au Service Account
Autoriser GitHub à utiliser votre Service Account :
```bash
gcloud iam service-accounts add-iam-policy-binding "terraform-sa@VOTRE_PROJECT_ID.iam.gserviceaccount.com" 
    --project="VOTRE_PROJECT_ID" 
    --role="roles/iam.workloadIdentityUser" 
    --member="principalSet://iam.googleapis.com/projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/my-pool/attribute.repository/VOTRE_ORG/VOTRE_REPO"
```

---

## 4. Utilisation dans Terraform

Dans votre workflow GitHub Actions, vous utiliserez l'action officielle :
```yaml
- uses: 'google-github-actions/auth@v2'
  with:
    workload_identity_provider: 'projects/123456789/locations/global/workloadIdentityPools/my-pool/providers/my-provider'
    service_account: 'terraform-sa@VOTRE_PROJECT_ID.iam.gserviceaccount.com'
```

Terraform utilisera alors automatiquement ce jeton temporaire. **Plus de clés JSON à stocker !**

---

[← 01 - Installation](01-installation-auth.md) | [🏠 Accueil](../00-README.md) | [03 - Provider configuration →](03-provider-configuration.md)
