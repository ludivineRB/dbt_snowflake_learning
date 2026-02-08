# 15 - Les Provisionneurs (local-exec)

## Objectif
Exécuter des scripts ou des commandes localement ou sur une ressource distante après sa création.

## Concepts
- `local-exec` : Exécute une commande sur la machine qui lance Terraform.
- `remote-exec` : Exécute une commande sur une VM via SSH/WinRM.

⚠️ **Attention** : Les provisionneurs doivent être utilisés en dernier recours. Préférez toujours les fonctionnalités natives du cloud (ex: startup scripts).
