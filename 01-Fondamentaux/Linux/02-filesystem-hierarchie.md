# 02 - Système de Fichiers et Hiérarchie

[← 01 - Architecture](01-introduction-architecture.md) | [🏠 Accueil](README.md) | [03 - Gestion des Processus →](03-gestion-processus.md)

---

## 1. La Hiérarchie Standard (FHS)

Sous Linux, tout part de la racine `/`. Il n'y a pas de `C:` ou `D:`. Tout est monté sous forme d'arborescence unique.

| Dossier | Contenu |
| --- | --- |
| `/bin` | Binaires essentiels (ls, cp, pwd). |
| `/etc` | Fichiers de configuration du système. |
| `/home` | Dossiers personnels des utilisateurs. |
| `/root` | Dossier personnel du super-utilisateur (Admin). |
| `/var` | Données variables (Logs, bases de données). |
| `/tmp` | Fichiers temporaires (effacés au reboot). |
| `/dev` | Fichiers représentants le matériel (disques, clavier). |
| `/proc` | Fichiers virtuels sur l'état du Kernel et des processus. |

---

## 2. "Everything is a file"

C'est l'un des principes fondamentaux de Linux. 
- Un texte est un fichier.
- Un dossier est un fichier.
- Un disque dur est un fichier (`/dev/sda`).
- Votre clavier est un fichier.

Cela permet d'utiliser les mêmes outils (cat, grep, redirection) pour tout manipuler.

---

## 3. VFS (Virtual File System)

Le **VFS** est une couche d'abstraction du Kernel qui permet de lire n'importe quel type de système de fichiers (ext4, NTFS, NFS, S3 bucket monté) de la même manière.

### Formats courants :
- **ext4** : Le standard Linux.
- **XFS** : Très performant pour les gros fichiers (Data Warehousing).
- **ZFS / Btrfs** : Fonctionnalités avancées (Snapshots, RAID logiciel).

---

## 4. Les Liens (Links)

- **Hard Link** : Un deuxième nom pour le même fichier physique. Si on supprime l'original, le lien fonctionne toujours.
- **Symbolic Link (Symlink)** : Un raccourci. Si on supprime l'original, le lien est cassé.
  ```bash
  ln -s /chemin/vers/original raccourci
  ```

---

[← 01 - Architecture](01-introduction-architecture.md) | [🏠 Accueil](README.md) | [03 - Gestion des Processus →](03-gestion-processus.md)
