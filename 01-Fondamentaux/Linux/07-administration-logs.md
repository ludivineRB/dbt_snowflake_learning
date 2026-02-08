# 07 - Administration Système et Logs

[← 06 - Sécurité](06-securite-permissions.md) | [🏠 Accueil](README.md) | [08 - Performance et Tuning →](08-performance-tuning.md)

---

## 1. Gestion des Services avec Systemd

Sur presque toutes les distros modernes, **systemd** est le premier processus (PID 1) qui gère tous les autres services.

### Commandes `systemctl` :
- `systemctl start docker` : Démarrer un service.
- `systemctl stop docker` : L'arrêter.
- `systemctl restart docker` : Redémarrer.
- `systemctl enable docker` : Activer au démarrage du serveur.
- `systemctl status docker` : Voir si tout va bien.

---

## 2. Automatisation : Crontab

Le démon **cron** permet de planifier des tâches (jobs ETL, backups).
```bash
crontab -e # Éditer ses tâches
```

### Syntaxe (M H D M D) :
`0 2 * * * /home/guillaume/backup.sh`
*(Lance le backup tous les jours à 2h00 du matin)*

---

## 3. Analyse des Logs Système

Les logs sont vos meilleurs amis quand un pipeline Data échoue mystérieusement.

- **/var/log/syslog** ou **/var/log/messages** : Logs généraux du système.
- **/var/log/auth.log** : Tentatives de connexion.
- **/var/log/dmesg** : Messages du Kernel (Hardware).

### Journalctl (L'outil moderne)
Remplace la lecture directe des fichiers pour systemd.
```bash
journalctl -u docker # Logs de Docker uniquement
journalctl -f # Suivre les logs en temps réel
journalctl -p err # Voir uniquement les erreurs
```

---

## 4. Gestion des paquets

| Famille | Commande | Exemple |
| --- | --- | --- |
| **Debian/Ubuntu** | `apt` | `apt install htop` |
| **RedHat/Rocky** | `dnf` | `dnf install git` |
| **Alpine** | `apk` | `apk add bash` |

---

[← 06 - Sécurité](06-securite-permissions.md) | [🏠 Accueil](README.md) | [08 - Performance et Tuning →](08-performance-tuning.md)
