# 14 - Exercices Récapitulatifs

[← 13 - Best Practices](13-best-practices-security.md) | [🏠 Accueil](../00-README.md) | [15 - Cloud Run →](15-cloud-run.md)

---

## Exercice 1 : Le Data Lake Express
1. Créez un bucket GCS nommé `data-lake-<votre-nom>` en région `europe-west1`.
2. Activez le versioning sur ce bucket.
3. Ajoutez une règle de cycle de vie pour passer les objets en classe `ARCHIVE` après 365 jours.

## Exercice 2 : Infrastructure Réseau & Calcul
1. Créez un VPC nommé `prod-vpc` (sans subnets automatiques).
2. Créez un subnet nommé `frontend-subnet` dans la région de votre choix.
3. Déployez une instance Compute Engine `e2-micro` dans ce subnet.
4. Ajoutez une règle firewall autorisant le port 80 (HTTP) uniquement pour cette instance (via un tag).

## Exercice 3 : Paramétrage & Outputs
1. Transformez l'exercice 2 pour utiliser des variables (nom de l'instance, région, projet_id).
2. Créez un fichier `terraform.tfvars`.
3. Ajoutez un output qui affiche l'IP publique de l'instance créée.

## Exercice 4 : Défi Avancé (Modules)
1. Créez un module local dans `modules/simple_bucket`.
2. Appelez ce module 3 fois via une boucle `for_each` pour créer 3 buckets différents.

---

## 💡 Conseils pour les exercices
- Utilisez `terraform plan` systématiquement avant le `apply`.
- Vérifiez les ressources créées dans la console Google Cloud.
- N'oubliez pas de faire un **`terraform destroy`** à la fin pour éviter les coûts inutiles !

---

[← 13 - Best Practices](13-best-practices-security.md) | [🏠 Accueil](../00-README.md) | [15 - Cloud Run →](15-cloud-run.md)
