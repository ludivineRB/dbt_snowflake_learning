# 02 - Navigation et Gestion de Fichiers

[← 01 - Introduction](01-introduction-shell.md) | [🏠 Accueil](../README.md) | [03 - Manipulation de Texte →](03-manipulation-texte.md)

---

## 1. Navigation dans le système de fichiers

### Structure des répertoires Linux/Unix
```bash
/                    (root - racine du système)
├── bin/            (binaires essentiels)
├── home/           (répertoires utilisateurs)
├── tmp/            (fichiers temporaires)
├── var/            (données variables: logs, caches)
└── data/           (souvent utilisé pour les données)
```

### Commandes de navigation
| Commande | Description | Exemple |
| --- | --- | --- |
| `pwd` | Print Working Directory | `pwd` |
| `cd` | Change Directory | `cd /home/data` |
| `cd ~` | Retour au Home | `cd ~` |
| `cd -` | Retour au répertoire précédent | `cd -` |
| `cd ..` | Remonter d'un niveau | `cd ..` |

---

## 2. Lister les fichiers avec `ls`

| Option | Description |
| --- | --- |
| `ls -l` | Format long (détails) |
| `ls -a` | Afficher les fichiers cachés (commençant par .) |
| `ls -h` | Tailles lisibles (Human Readable) |
| `ls -lhS` | Trier par taille |
| `ls -lt` | Trier par date de modification |

---

## 3. Créer, Copier et Déplacer

```bash
# Créer un dossier (et ses parents)
mkdir -p data/raw/2024

# Créer un fichier vide
touch script.py

# Copier un dossier entier (récursif)
cp -r data/ backup_data/

# Déplacer ou renommer
mv old_name.csv new_name.csv
```

---

## 4. Suppression (⚠️ Prudence)
La suppression est définitive !
```bash
# Supprimer un fichier
rm data.csv

# Supprimer un dossier et tout son contenu
rm -rf folder/
```

---

## 5. Recherche de fichiers

- **`find`** : Puissant, recherche en temps réel.
  ```bash
  find . -name "*.csv" -size +100M
  ```
- **`locate`** : Ultra-rapide, basé sur une base de données.
  ```bash
  locate config.json
  ```

---

## 6. Permissions et Droits

```bash
-rw-r--r--  (r=4, w=2, x=1)
# 755 : rwxr-xr-x (Exécutable par tous)
# 600 : rw------- (Privé)

chmod +x script.sh  # Rendre exécutable
chown user:group file.csv  # Changer le propriétaire
```

---

[← 01 - Introduction](01-introduction-shell.md) | [🏠 Accueil](../README.md) | [03 - Manipulation de Texte →](03-manipulation-texte.md)