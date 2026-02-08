# 06 - Sécurité et Permissions Avancées

[← 05 - Réseau](05-reseau-linux.md) | [🏠 Accueil](README.md) | [07 - Administration et Logs →](07-administration-logs.md)

---

## 1. Au-delà du standard Owner/Group/Other

Vous connaissez déjà `chmod` et `chown`. Mais Linux propose des mécanismes beaucoup plus fins.

### ACLs (Access Control Lists)
Permet de donner des droits à un utilisateur spécifique sans changer le groupe du fichier.
```bash
setfacl -m u:guillaume:rw fichier.txt # Donne accès à guillaume
getfacl fichier.txt # Affiche les droits détaillés
```

---

## 2. Le fichier /etc/sudoers

Ce fichier définit qui a le droit de devenir "Root" (Admin). On le modifie avec la commande sécurisée `visudo`.

### Exemple de règle :
`guillaume ALL=(ALL) NOPASSWD: /usr/bin/apt`
*(Autorise guillaume à installer des paquets sans taper son mot de passe)*

---

## 3. Les Sticky Bits et Permissions spéciales

- **SUID (Set User ID)** : Un fichier s'exécute avec les droits du propriétaire (ex: `/usr/bin/passwd`).
- **SGID** : Un fichier s'exécute avec les droits du groupe.
- **Sticky Bit** : Utilisé sur `/tmp`. Tout le monde peut écrire, mais seul le propriétaire peut supprimer son propre fichier.

---

## 4. Introduction au durcissement (Hardening)

- **SELinux / AppArmor** : Couches de sécurité obligatoires (MAC) qui empêchent même un processus Root de faire n'importe quoi si ce n'est pas explicitement autorisé.
- **SSH Hardening** : Désactiver le login root, changer le port 22, exiger des clés SSH.

---

[← 05 - Réseau](05-reseau-linux.md) | [🏠 Accueil](README.md) | [07 - Administration et Logs →](07-administration-logs.md)
