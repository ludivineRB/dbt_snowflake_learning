# 13 - Best Practices et Sécurité

[← 12 - Data Sources](12-data-sources.md) | [🏠 Accueil](../00-README.md) | [14 - Exercices →](14-exercices.md)

---

## 1. Organisation du Code

Divisez vos fichiers pour une meilleure clarté :
- `main.tf` : Ressources principales.
- `variables.tf` : Définitions des variables.
- `outputs.tf` : Sorties.
- `providers.tf` : Configuration des providers.
- `backend.tf` : Configuration du Remote State.

---

## 2. Sécurité des Identifiants

- **NE COMMITEZ JAMAIS** de fichiers JSON de Service Account Keys.
- Utilisez **Workload Identity Federation** (WIF) en CI/CD.
- Utilisez des variables d'environnement (`GOOGLE_APPLICATION_CREDENTIALS`) ou ADC localement.

---

## 3. Gestion de l'État (State)

- Utilisez toujours un **Remote Backend** (GCS) en équipe.
- Activez le **State Locking** (natif sur GCS).
- Ne modifiez jamais le fichier `.tfstate` à la main.

---

## 4. Maintenance de l'Infrastructure

- **terraform fmt** : Formatez votre code automatiquement avant de commiter.
- **terraform validate** : Vérifiez la cohérence syntaxique.
- **Checkov / TFLint** : Utilisez des outils de scan pour détecter les erreurs de sécurité ou les mauvaises pratiques.

---

## 5. Drift Detection

L'infrastructure peut être modifiée via la console GCP. Lancez régulièrement `terraform plan` pour détecter les écarts ("drift") entre le code et la réalité.

---

[← 12 - Data Sources](12-data-sources.md) | [🏠 Accueil](../00-README.md) | [14 - Exercices →](14-exercices.md)
