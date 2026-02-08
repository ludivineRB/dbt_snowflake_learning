# 06 - Installation et Configuration

[← 05 - Écosystème](05-ecosysteme.md) | [🏠 Accueil](README.md) | [07 - Déploiement Azure →](07-deploiement-azure.md)

---

## 🔧 Modes de Déploiement
- **Standalone** : Un seul processus.
- **Pseudo-distribué** : Tous les démons sur une seule machine.
- **Distribué** : Cluster réel.

## 🚀 Étapes Clés
1. Configuration de **Java** et **SSH**.
2. Téléchargement et extraction de Hadoop.
3. Édition des fichiers XML : `core-site.xml`, `hdfs-site.xml`, `mapred-site.xml`, `yarn-site.xml`.
4. Formatage du NameNode.
5. Démarrage des services (`start-dfs.sh`, `start-yarn.sh`).

---

[← 05 - Écosystème](05-ecosysteme.md) | [🏠 Accueil](README.md) | [07 - Déploiement Azure →](07-deploiement-azure.md)
