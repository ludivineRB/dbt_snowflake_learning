# 03 - Manipulation de Texte et Données

[← 02 - Navigation](02-navigation-fichiers.md) | [🏠 Accueil](../README.md) | [04 - Scripts et Automatisation →](04-scripts-automatisation.md)

---

## 1. Afficher le contenu

- **`cat`** : Tout le fichier.
- **`head -n 20`** : Les 20 premières lignes.
- **`tail -f`** : Suivre les nouvelles lignes (logs).
- **`less`** : Navigation interactive (Espace/B pour défiler, Q pour quitter).

---

## 2. Redirections et Pipelines (Le coeur du Shell)

- `>` : Écrase le fichier.
- `>>` : Ajoute à la fin du fichier.
- `|` : Envoie la sortie d'une commande vers l'entrée d'une autre.
- `2>` : Redirige uniquement les erreurs.

---

## 3. grep - Recherche de patterns

| Option | Description |
| --- | --- |
| `-i` | Ignorer la casse |
| `-v` | Inverser (ne contient pas) |
| `-c` | Compter les occurrences |
| `-E` | Regex étendues |

Exemple : `grep -i "error" server.log`

---

## 4. sed - Transformation de texte

```bash
# Remplacer "old" par "new" (globalement)
sed 's/old/new/g' file.txt

# Supprimer les lignes vides
sed '/^$/d' data.csv
```

---

## 5. awk - Traitement structuré (CSV/TSV)

`awk` traite les fichiers colonne par colonne.
```bash
# Afficher colonnes 1 et 3 d'un CSV
awk -F',' '{print $1, $3}' data.csv

# Faire une somme
awk -F',' '{sum += $4} END {print "Total:", sum}' sales.csv
```

---

## 6. Pipeline complet : Exemple d'analyse
```bash
cat access.log | awk '{print $1}' | sort | uniq -c | sort -rn | head -10
```
*(Récupère les 10 IPs les plus fréquentes dans un log Apache)*

---

[← 02 - Navigation](02-navigation-fichiers.md) | [🏠 Accueil](../README.md) | [04 - Scripts et Automatisation →](04-scripts-automatisation.md)