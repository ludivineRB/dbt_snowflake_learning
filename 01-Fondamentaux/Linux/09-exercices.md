# 09 - Exercices : Linux

[← 08 - Performance](08-performance-tuning.md) | [🏠 Accueil](README.md)

---

## Exercice 1 : Navigation et Filesystem
1. Trouvez le chemin absolu de votre répertoire personnel.
2. Créez un lien symbolique nommé `mes_logs` pointant vers `/var/log`.
3. Listez tous les fichiers de `/etc` finissant par `.conf`.

## Exercice 2 : Processus et Signaux
1. Lancez une commande `sleep 1000 &` en arrière-plan.
2. Trouvez son PID.
3. Changez sa priorité (nice) à 15.
4. Tuez le processus proprement (SIGTERM), puis vérifiez qu'il n'est plus là.

## Exercice 3 : Stockage et Montage
1. Affichez l'espace disque restant en format lisible.
2. Trouvez quel dossier dans `/var` consomme le plus d'espace.
3. Affichez le nombre d'inodes libres sur votre partition principale.

## Exercice 4 : Réseau
1. Trouvez votre adresse IP locale.
2. Listez tous les ports en écoute sur votre machine.
3. Vérifiez si vous pouvez contacter `google.com` sur le port 443 via `nc` ou `telnet`.

## Exercice 5 : Administration et Logs
1. Affichez les 50 dernières lignes du log système.
2. Vérifiez si le service `docker` (ou un autre service installé) est configuré pour démarrer automatiquement.
3. Planifiez une tâche cron qui écrit "Hello" dans un fichier `/tmp/hello.txt` chaque minute.

---

## 💡 Solutions (Résumé)

<details>
<summary>Cliquez pour voir les solutions</summary>

### Ex 1
1. `pwd`
2. `ln -s /var/log mes_logs`
3. `ls /etc/*.conf`

### Ex 2
1. `sleep 1000 &`
2. `ps aux | grep sleep` ou `pgrep sleep`
3. `renice -n 15 -p <PID>`
4. `kill <PID>` (ou `kill -15 <PID>`)

### Ex 3
1. `df -h`
2. `du -sh /var/* | sort -rh | head -n 1`
3. `df -i`

### Ex 4
1. `ip addr`
2. `ss -tulpn`
3. `nc -zv google.com 443`

### Ex 5
1. `tail -n 50 /var/log/syslog` (ou `journalctl -n 50`)
2. `systemctl is-enabled docker`
3. `crontab -e` puis `* * * * * echo "Hello" >> /tmp/hello.txt`

</details>

---

[← 08 - Performance](08-performance-tuning.md) | [🏠 Accueil](README.md)
