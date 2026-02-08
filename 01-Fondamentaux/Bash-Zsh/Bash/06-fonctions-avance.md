# 06 - Fonctions et Outils Avancés

[← 05 - Structures](05-structures-controle.md) | [🏠 Accueil](../README.md) | [07 - Bonnes Pratiques →](07-bonnes-pratiques.md)

---

## 1. Fonctions réutilisables

```bash
log_info() {
    local message=$1
    echo "[$(date +'%T')] INFO: $message"
}

log_info "Extraction terminée."
```

---

## 2. xargs - Construction de commandes

```bash
# Supprimer tous les fichiers .tmp trouvés
find . -name "*.tmp" | xargs rm

# Téléchargement parallèle (4 simultanés)
cat urls.txt | xargs -P 4 -n 1 curl -O
```

---

## 3. jq - Manipuler du JSON (Crucial pour les API)

```bash
# Extraire un champ
cat users.json | jq '.users[].name'

# Convertir JSON en CSV
cat data.json | jq -r '.data[] | [@id, @name] | @csv'
```

---

## 4. GNU Parallel

Plus puissant que xargs pour le parallélisme massif.
```bash
ls *.csv | parallel gzip
```

---

## 5. Process Substitution

```bash
# Comparer les fichiers de deux dossiers sans créer de fichiers temporaires
diff <(ls dir1) <(ls dir2)
```

---

[← 05 - Structures](05-structures-controle.md) | [🏠 Accueil](../README.md) | [07 - Bonnes Pratiques →](07-bonnes-pratiques.md)