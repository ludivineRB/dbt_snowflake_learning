# 05 - Réseau sous Linux

[← 04 - Stockage](04-memoire-stockage.md) | [🏠 Accueil](README.md) | [06 - Sécurité et Permissions →](06-securite-permissions.md)

---

## 1. Interfaces et Adresses IP

Linux identifie chaque connexion physique ou virtuelle comme une interface :
- `lo` : Loopback (127.0.0.1), l'adresse locale du serveur.
- `eth0` ou `enp0s3` : Votre connexion Ethernet/WiFi.
- `docker0` : Pont virtuel utilisé par Docker.

### Commandes :
- `ip addr` : Affiche les interfaces et leurs IPs. (Remplace l'ancien `ifconfig`).
- `ip route` : Affiche la table de routage (la passerelle par défaut).

---

## 2. Ports et Services

Un serveur peut héberger plusieurs services sur la même IP via des ports :
- HTTP : 80 / HTTPS : 443
- SSH : 22
- PostgreSQL : 5432
- Spark Web UI : 4040

### Vérifier qui écoute sur quoi :
```bash
ss -tulpn
```
*(Remplace l'ancien `netstat`)*

---

## 3. Configuration DNS et Hosts

- **/etc/hosts** : Annuaire local. Utile pour nommer des serveurs sans DNS.
- **/etc/resolv.conf** : Définit quels serveurs DNS interroger (ex: 8.8.8.8).

---

## 4. Troubleshooting Réseau

| Commande | Usage |
| --- | --- |
| `ping google.com` | Teste la connectivité basique. |
| `dig google.com` | Teste la résolution DNS. |
| `curl -I http://monsite.com` | Teste la réponse d'un serveur Web. |
| `nc -zv host port` | Netcat : vérifie si un port est ouvert. |
| `traceroute google.com` | Affiche le chemin parcouru par les paquets. |

---

[← 04 - Stockage](04-memoire-stockage.md) | [🏠 Accueil](README.md) | [06 - Sécurité et Permissions →](06-securite-permissions.md)
