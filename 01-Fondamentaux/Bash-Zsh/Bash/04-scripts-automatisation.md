# 04 - Scripts Shell et Automatisation

[← 03 - Texte](03-manipulation-texte.md) | [🏠 Accueil](../README.md) | [05 - Structures de Contrôle →](05-structures-controle.md)

---

## 1. Créer un script
1. Fichier `.sh`.
2. **Shebang** en première ligne : `#!/usr/bin/env bash`.
3. Droits d'exécution : `chmod +x script.sh`.

---

## 2. Variables et Substitution

```bash
NAME="Alice"
echo "Hello, ${NAME}"

# Capturer le résultat d'une commande
DATE=$(date +%Y-%m-%d)
```

---

## 3. Paramètres et Arguments
- `$0` : Nom du script.
- `$1, $2...` : Premier, deuxième argument.
- `$#` : Nombre total d'arguments.
- `$@` : Tous les arguments.

---

## 4. Mode Strict (set -euo pipefail)
⚠️ **INDISPENSABLE en production :**
- `set -e` : Arrête le script si une commande échoue.
- `set -u` : Erreur si une variable n'est pas définie.
- `set -o pipefail` : Échoue si un élément d'un pipeline échoue.

---

## 5. Gestion d'erreurs et Debugging
- `exit 0` : Succès.
- `exit 1` : Erreur.
- `bash -x script.sh` : Trace complète de l'exécution (debug).

---

## 6. Lecture utilisateur
```bash
read -p "Entrez le nom de la table : " table_name
```

---

[← 03 - Texte](03-manipulation-texte.md) | [🏠 Accueil](../README.md) | [05 - Structures de Contrôle →](05-structures-controle.md)