# 01 - Introduction et Architecture Linux

[🏠 Accueil](README.md) | [02 - Système de Fichiers →](02-filesystem-hierarchie.md)

---

## 1. Qu'est-ce que Linux ?

Linux est un noyau (Kernel) de système d'exploitation libre et open-source, créé par **Linus Torvalds** en 1991. Ce que nous appelons couramment "Linux" est en réalité une distribution **GNU/Linux**.

### Pourquoi Linux ?
- **Stabilité** : Capable de tourner des années sans redémarrer.
- **Sécurité** : Gestion stricte des droits et transparence du code.
- **Performance** : Idéal pour traiter de gros volumes de données.
- **Cloud-Native** : 90% du cloud mondial tourne sous Linux.

---

## 2. Les Distributions (Distros)

Il existe des centaines de distributions, mais elles se regroupent souvent en familles :
- **Debian / Ubuntu** : La plus populaire, très accessible (Data Science, Web).
- **Red Hat (RHEL) / CentOS / Rocky** : Standard en entreprise pour sa robustesse.
- **Alpine** : Ultra-légère (5MB), parfaite pour les containers Docker.
- **Arch Linux** : Pour les experts qui veulent tout configurer eux-mêmes.

---

## 3. L'Architecture Globale

Le système est divisé en plusieurs couches :

### A. Le Kernel (Le Noyau)
C'est le logiciel qui parle directement au matériel (CPU, RAM, Disque). Il gère l'allocation des ressources.

### B. Le Shell (L'Interpréteur)
L'interface qui permet de communiquer avec le Kernel. (Voir le cours [Bash-Zsh](../Bash-Zsh/README.md)).

### C. L'User Space (Espace Utilisateur)
C'est là que tournent vos applications (Python, Spark, Docker). Les applications ne parlent jamais au matériel directement, elles font des **System Calls** (Appels système) au Kernel.

---

## 4. Hardware vs Software

Linux utilise des **Drivers** intégrés directement dans le Kernel pour piloter le matériel. Contrairement à Windows, la plupart des pilotes sont "Ready-to-use" sans installation manuelle.

---

[🏠 Accueil](README.md) | [02 - Système de Fichiers →](02-filesystem-hierarchie.md)
