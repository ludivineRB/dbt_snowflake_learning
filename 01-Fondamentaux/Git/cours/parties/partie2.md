## 2. Installation et configuration initiale

### Installation de Git

#### 🐧 Linux

```bash
# Debian/Ubuntu
sudo apt-get update
sudo apt-get install git

# Fedora/CentOS
sudo dnf install git
```

#### 🍎 macOS

```bash
# Avec Homebrew
brew install git

# Ou via Xcode Command Line Tools
xcode-select --install
```

#### 🪟 Windows

Téléchargez Git depuis [git-scm.com](https://git-scm.com/download/win)

Ou utilisez [Git for Windows](https://gitforwindows.org/)

### Vérifier l'installation

```bash
git --version
# Résultat attendu : git version 2.x.x
```

### Configuration initiale (OBLIGATOIRE)

Avant votre premier commit, vous devez configurer votre identité :

```bash
# Configuration de votre identité (obligatoire)
git config --global user.name "Prenom Nom"
git config --global user.email "votre.email@example.com"

# Configuration de l'éditeur par défaut
git config --global core.editor "code --wait"  # VS Code
# ou
git config --global core.editor "vim"          # Vim
# ou
git config --global core.editor "nano"         # Nano

# Définir la branche par défaut
git config --global init.defaultBranch main

# Activer les couleurs dans le terminal
git config --global color.ui auto

# Configuration pour éviter les problèmes de fins de ligne
# Sur Windows :
git config --global core.autocrlf true
# Sur Mac/Linux :
git config --global core.autocrlf input
```

### Voir toute la configuration

```bash
# Lister toute la configuration
git config --list

# Voir une configuration spécifique
git config user.name
git config user.email

# Voir où est stockée la configuration
git config --list --show-origin
```

#### Niveaux de configuration

- `--system` : Appliqué à tous les utilisateurs du système
- `--global` : Appliqué à votre utilisateur (le plus courant)
- `--local` : Appliqué uniquement au dépôt actuel

### Configurer un alias pour gagner du temps

```bash
# Créer des raccourcis personnalisés
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.unstage 'reset HEAD --'
git config --global alias.last 'log -1 HEAD'
git config --global alias.lg 'log --oneline --graph --all --decorate'

# Maintenant vous pouvez utiliser :
git st        # au lieu de git status
git lg        # pour un beau log graphique
```

#### ✅ Partie 2 terminée !

Vous avez installé Git et configuré votre environnement. Vous êtes prêt à créer votre premier dépôt !

[🎯 Faire les exercices](../exercices.md)
[Partie 3 →](partie3.md)