# 11 - Debugging et Logs avancés

## Objectif
Comprendre comment activer les logs de debug de Terraform pour diagnostiquer des problèmes complexes.

## Utilisation
Terraform n'a pas de bloc de code spécifique pour les logs, cela se gère via des variables d'environnement.

### Activer les logs (Linux/macOS)
```bash
export TF_LOG=DEBUG
terraform apply
```

### Niveaux de logs
- `TRACE` : Le plus détaillé.
- `DEBUG` : Informations de débogage.
- `INFO` : Informations générales.
- `WARN` : Avertissements.
- `ERROR` : Erreurs uniquement.

### Sauvegarder dans un fichier
```bash
export TF_LOG_PATH=terraform.log
```
