## 1. Introduction au Shell (Bash/Zsh)

### Qu'est-ce que le Shell ?

Le **shell** est un interpréteur de commandes qui permet d'interagir avec le système
d'exploitation via des commandes textuelles. C'est l'interface entre l'utilisateur et le noyau
(kernel) du système.

#### Shell vs Terminal

**Terminal** : L'application graphique qui affiche le shell (iTerm, GNOME
Terminal, Windows Terminal...)
**Shell** : Le programme qui interprète vos commandes (Bash, Zsh, Fish...)

### Les principaux shells

| Shell | Avantages | Utilisation |
| --- | --- | --- |
| **Bash** (Bourne Again Shell) | Universel, compatible partout, documentation abondante | Shell par défaut sur Linux et macOS (avant Catalina) |
| **Zsh** (Z Shell) | Autocomplétion puissante, plugins, thèmes, historique partagé | Shell par défaut sur macOS depuis Catalina |
| **Fish** | Syntaxe moderne, autocomplétion intelligente | Alternative moderne mais syntaxe différente |
| **sh** (Bourne Shell) | Minimaliste, scripts portables | Scripts système, compatibilité maximale |

### Bash vs Zsh : Les différences

#### 🐚 Bash

**Points forts :**

- ✅ Présent partout par défaut
- ✅ Très stable et bien documenté
- ✅ Scripts portables
- ✅ Compatible POSIX

**Limitations :**

- ❌ Autocomplétion basique
- ❌ Moins de fonctionnalités modernes
- ❌ Configuration plus complexe

#### ⚡ Zsh

**Points forts :**

- ✅ Autocomplétion intelligente
- ✅ Correction automatique des typos
- ✅ Oh My Zsh (framework de plugins)
- ✅ Historique de commandes partagé
- ✅ Globbing avancé

**Limitations :**

- ❌ Pas toujours installé par défaut
- ❌ Légèrement plus lent au démarrage

### Pourquoi le Shell en Data Engineering ?

### 💡 Cas d'usage essentiels

- **Traitement de fichiers volumineux** : Filtrer des fichiers de logs de
  plusieurs Go avec grep/awk
- **Automatisation de pipelines** : Créer des scripts ETL légers et rapides
- **Manipulation de données** : Nettoyer des CSV, extraire des colonnes,
  calculer des agrégations
- **Surveillance système** : Monitorer l'utilisation CPU/mémoire des processus
  de données
- **Déploiement** : Automatiser le déploiement de pipelines avec des scripts
  shell
- **Debugging** : Analyser rapidement des logs, comparer des fichiers
- **Orchestration** : Lancer des jobs, gérer des dépendances entre tâches

### Exemple concret en Data Engineering

Imaginez que vous devez analyser des logs de serveur pour identifier les erreurs. Voici comment
faire en une seule ligne de shell :

```bash
# Extraire toutes les erreurs, compter par type, et trier
grep "ERROR" server.log | \
  awk '{print $5}' | \
  sort | \
  uniq -c | \
  sort -rn | \
  head -10

# Résultat :
# 245 ConnectionTimeout
# 189 DatabaseError
# 156 FileNotFound
#  89 PermissionDenied
#  67 InvalidFormat
```

En Python, cela nécessiterait une dizaine de lignes de code. En shell, c'est une seule commande !

### Vérifier votre shell actuel

```bash
# Afficher le shell actuel
echo $SHELL
# Output: /bin/zsh  (ou /bin/bash)

# Afficher la version de Bash
bash --version

# Afficher la version de Zsh
zsh --version

# Lister tous les shells disponibles
cat /etc/shells
```

### Changer de shell

```bash
# Passer à Zsh temporairement
zsh

# Passer à Bash temporairement
bash

# Définir Zsh comme shell par défaut
chsh -s /bin/zsh

# Définir Bash comme shell par défaut
chsh -s /bin/bash

# (Nécessite de se déconnecter/reconnecter)
```

#### ⚠️ Note importante

Dans cette formation, nous utiliserons principalement **Bash** car il est
universel.
Toutes les commandes fonctionneront également en **Zsh**.
Les différences de syntaxe seront signalées lorsque nécessaire.

### Le prompt du shell

Le **prompt** est le texte affiché avant votre curseur dans le terminal. Il contient
généralement :

```bash
username@hostname:~/directory$
    │        │         │      └─ Indicateur ($=user, #=root)
    │        │         └─ Répertoire courant
    │        └─ Nom de la machine
    └─ Nom de l'utilisateur
```

**Exemples de prompts :**

```bash
# Bash par défaut
guillaume@macbook:~/projects$

# Zsh avec Oh My Zsh (thème agnoster)
➜  projects git:(main) ✗

# Root user
root@server:/var/log#

# Dans un container Docker
root@container-id:/#
```

### Premières commandes essentielles

| Commande | Description | Exemple |
| --- | --- | --- |
| `pwd` | Afficher le répertoire courant | `pwd` |
| `whoami` | Afficher le nom d'utilisateur | `whoami` |
| `date` | Afficher la date et l'heure | `date` |
| `hostname` | Afficher le nom de la machine | `hostname` |
| `echo` | Afficher du texte | `echo "Hello World"` |
| `clear` | Effacer l'écran | `clear` ou `Ctrl+L` |
| `history` | Afficher l'historique des commandes | `history` |
| `exit` | Quitter le shell | `exit` ou `Ctrl+D` |

### Exercice pratique

#### 🎯 Exercice 1 : Découverte du shell

Ouvrez un terminal et exécutez les commandes suivantes :

1. Affichez votre shell actuel avec `echo $SHELL`
2. Affichez votre nom d'utilisateur avec `whoami`
3. Affichez le répertoire courant avec `pwd`
4. Affichez la date et l'heure actuelles
5. Affichez les 10 dernières commandes de votre historique

💡 Voir la solution

```bash
# 1. Shell actuel
echo $SHELL

# 2. Nom d'utilisateur
whoami

# 3. Répertoire courant
pwd

# 4. Date et heure
date

# 5. Historique
history | tail -10
```

### Raccourcis clavier essentiels

| Raccourci | Action |
| --- | --- |
| `Ctrl + C` | Interrompre la commande en cours |
| `Ctrl + D` | Quitter le shell (EOF) |
| `Ctrl + L` | Effacer l'écran (équivalent à `clear`) |
| `Ctrl + A` | Aller au début de la ligne |
| `Ctrl + E` | Aller à la fin de la ligne |
| `Ctrl + U` | Effacer du curseur au début de la ligne |
| `Ctrl + K` | Effacer du curseur à la fin de la ligne |
| `Ctrl + W` | Effacer le mot précédent |
| `Ctrl + R` | Rechercher dans l'historique |
| `↑ / ↓` | Naviguer dans l'historique |
| `Tab` | Autocomplétion |

#### 💡 Conseil pro

Mémorisez `Ctrl + R` pour la recherche dans l'historique. C'est l'un des
raccourcis
les plus utiles au quotidien. Tapez `Ctrl + R` puis commencez à taper une partie
de
la commande que vous cherchez !

#### ✅ Partie 1 terminée !

Vous avez appris les bases du shell et compris pourquoi c'est essentiel en Data Engineering.
Passez maintenant à la Partie 2 pour apprendre à naviguer dans le système de fichiers.

[Partie 2 : Navigation et Gestion de Fichiers →](partie2.md)