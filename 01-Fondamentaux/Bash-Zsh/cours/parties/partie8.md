## Installation et Configuration Complète pour Data Engineers

#### 🎯 Objectifs de cette partie

Dans cette partie, vous allez transformer votre terminal en un environnement de travail
moderne, efficace et adapté au Data Engineering. Vous installerez :

- **Oh My Zsh** : Framework de configuration Zsh
- **Powerlevel10k** : Le thème le plus rapide et personnalisable
- **Plugins essentiels** : Pour Python, Docker, Git, autocomplétion, etc.

### Prérequis

#### ⚠️ Avant de commencer

Assurez-vous d'avoir :

- **Zsh installé** : Vérifiez avec `zsh --version`
- **Git installé** : Vérifiez avec `git --version`
- **curl ou wget** : Pour télécharger les scripts
- **Une police Nerd Font** (on va l'installer ensemble)

```bash
# Vérifier que Zsh est installé
zsh --version
# Output attendu : zsh 5.8 ou supérieur

# Si Zsh n'est pas installé :
# macOS
brew install zsh

# Ubuntu/Debian
sudo apt install zsh

# Fedora/RHEL
sudo dnf install zsh
```

## 🚀 Étape 1 : Installation de Oh My Zsh

### Qu'est-ce que Oh My Zsh ?

**Oh My Zsh** est un framework open-source pour gérer votre configuration Zsh.
Il fournit des centaines de plugins, de thèmes et de fonctionnalités pour améliorer votre
productivité.

#### ✨ Avantages

- 300+ plugins inclus
- 150+ thèmes disponibles
- Autocomplétion intelligente
- Communauté active
- Mises à jour régulières

#### 🎯 Pour Data Engineering

- Support Python, Docker, K8s
- Plugins Git avancés
- Alias pour AWS, GCP, Azure
- Intégration avec Terraform
- Support pour Airflow, dbt

### Installation de Oh My Zsh

```bash
# Installation via curl
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# Ou via wget
sh -c "$(wget -O- https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# Le script va :
# 1. Télécharger Oh My Zsh dans ~/.oh-my-zsh
# 2. Sauvegarder votre .zshrc actuel en .zshrc.pre-oh-my-zsh
# 3. Créer un nouveau .zshrc avec des paramètres par défaut
# 4. Changer votre shell par défaut en Zsh (si ce n'est pas déjà fait)
```

#### ✅ Vérification

Après l'installation, fermez et rouvrez votre terminal. Vous devriez voir un nouveau prompt
coloré avec le thème "robbyrussell" par défaut.

## 🎨 Étape 2 : Installation de Powerlevel10k

### Pourquoi Powerlevel10k ?

### 💎 Powerlevel10k - Le meilleur thème Zsh

- **Ultra-rapide** : 100x plus rapide que Powerlevel9k
- **Configuration guidée** : Assistant interactif de personnalisation
- **Informations riches** : Git status, Python venv, Node version, etc.
- **Icônes Nerd Fonts** : Support complet des polices avec icônes
- **Segments personnalisables** : Affichage conditionnel selon le contexte
- **Compatible TTY** : Fonctionne même sans polices spéciales

### Étape 2.1 : Installer une Nerd Font

Powerlevel10k nécessite une **Nerd Font** pour afficher les icônes correctement.
La police recommandée est **MesloLGS NF**.

#### 📥 Installation des polices MesloLGS NF

**macOS / Linux :**

1. Téléchargez les 4 fichiers de police :
   - [MesloLGS
     NF Regular.ttf](https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Regular.ttf)
   - [MesloLGS
     NF Bold.ttf](https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Bold.ttf)
   - [MesloLGS
     NF Italic.ttf](https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Italic.ttf)
   - [MesloLGS
     NF Bold Italic.ttf](https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Bold%20Italic.ttf)
2. Double-cliquez sur chaque fichier et cliquez sur "Installer"
3. Configurez votre terminal pour utiliser "MesloLGS NF"

```bash
# Installation automatique via Homebrew (macOS)
brew tap homebrew/cask-fonts
brew install --cask font-meslo-lg-nerd-font

# Vérifier l'installation
fc-list | grep "MesloLGS"
```

```bash
Configuration de la police dans votre terminal :

iTerm2 (macOS) :
├─ Preferences → Profiles → Text
└─ Font: MesloLGS NF, 13pt

Terminal.app (macOS) :
├─ Preferences → Profiles → Font
└─ Change → MesloLGS NF, 13pt

VS Code :
├─ Settings (Cmd+,)
└─ Terminal › Integrated: Font Family → 'MesloLGS NF'

Windows Terminal :
├─ Settings → Profiles → Defaults → Appearance
└─ Font face → MesloLGS NF
```

### Étape 2.2 : Installer Powerlevel10k

```bash
# Cloner Powerlevel10k dans le dossier des thèmes Oh My Zsh
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git \
  ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k

# Éditer ~/.zshrc
nano ~/.zshrc

# Chercher la ligne ZSH_THEME et remplacer par :
# ZSH_THEME="powerlevel10k/powerlevel10k"

# Sauvegarder (Ctrl+O, Enter, Ctrl+X)

# Recharger la configuration
source ~/.zshrc
```

### Étape 2.3 : Configuration Wizard de Powerlevel10k

Au premier lancement, le **Configuration Wizard** de Powerlevel10k se lance
automatiquement.
Il vous posera une série de questions pour personnaliser votre prompt.

#### 🎨 Recommandations pour Data Engineers

Voici les réponses recommandées lors de la configuration :

1. **Does this look like a diamond?** → Yes
2. **Does this look like a lock?** → Yes
3. **Does this look like a Debian logo?** → Yes
4. **Prompt Style** → Rainbow (3)
5. **Character Set** → Unicode
6. **Show current time?** → 24-hour format
7. **Prompt Separators** → Angled
8. **Prompt Heads** → Sharp
9. **Prompt Tails** → Flat
10. **Prompt Height** → Two lines
11. **Prompt Connection** → Disconnected
12. **Prompt Frame** → Left
13. **Connection Color** → Dark
14. **Prompt Spacing** → Sparse
15. **Icons** → Many icons
16. **Prompt Flow** → Concise
17. **Enable Transient Prompt?** → Yes (recommandé)
18. **Instant Prompt Mode** → Verbose (recommandé pour debugging)

```bash
# Si vous voulez reconfigurer Powerlevel10k plus tard
p10k configure

# Éditer manuellement la configuration
nano ~/.p10k.zsh
```

## 🔌 Étape 3 : Installation des Plugins Essentiels pour Data Engineers

### 3.1 : Plugins intégrés à Oh My Zsh

Oh My Zsh inclut de nombreux plugins par défaut. Voici ceux essentiels pour le Data Engineering :

| Plugin | Description | Pourquoi l'utiliser ? |
| --- | --- | --- |
| `git` | Alias et autocomplétion Git | Gain de temps énorme avec des alias comme `gst`, `gco` |
| `docker` | Autocomplétion Docker | Autocomplete conteneurs, images, commandes |
| `docker-compose` | Autocomplétion docker-compose | Essentiel pour gérer des stacks multi-services |
| `python` | Alias Python et venv | Gestion des environnements virtuels |
| `pip` | Autocomplétion pip | Installer des packages plus rapidement |
| `kubectl` | Autocomplétion Kubernetes | Indispensable si vous travaillez avec K8s |
| `terraform` | Autocomplétion Terraform | Pour Infrastructure as Code |
| `aws` | Autocomplétion AWS CLI | Gestion des services AWS |
| `gcloud` | Autocomplétion Google Cloud | Pour travailler avec GCP |
| `z` | Navigation rapide (jump to directories) | Sauter dans des dossiers fréquemment utilisés |
| `web-search` | Rechercher sur Google depuis le terminal | Recherche rapide de documentation |
| `jsontools` | Formatage JSON | Valider et formatter des JSON |
| `sudo` | Appuyer 2x ESC pour ajouter sudo | Pratique quand vous oubliez sudo |
| `aliases` | Lister tous vos alias | Retrouver rapidement vos alias |
| `common-aliases` | Alias communs utiles | Alias pour ls, grep, etc. |

### 3.2 : Plugins externes essentiels

Ces plugins doivent être installés manuellement car ils ne sont pas inclus dans Oh My Zsh :

| Plugin | Description | Impact |
| --- | --- | --- |
| `zsh-autosuggestions` | Suggestions basées sur l'historique | ⭐⭐⭐⭐⭐ Indispensable |
| `zsh-syntax-highlighting` | Coloration syntaxique en temps réel | ⭐⭐⭐⭐⭐ Indispensable |
| `zsh-completions` | Autocomplétion supplémentaire | ⭐⭐⭐⭐ Très utile |
| `fast-syntax-highlighting` | Alternative plus rapide à syntax-highlighting | ⭐⭐⭐⭐ Alternative |

### Installation des plugins externes

```bash
# 1. zsh-autosuggestions (ESSENTIEL)
git clone https://github.com/zsh-users/zsh-autosuggestions \
  ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions

# 2. zsh-syntax-highlighting (ESSENTIEL)
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git \
  ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting

# 3. zsh-completions (recommandé)
git clone https://github.com/zsh-users/zsh-completions \
  ${ZSH_CUSTOM:-${ZSH:-~/.oh-my-zsh}/custom}/plugins/zsh-completions

# 4. fast-syntax-highlighting (alternative - choisir entre 2 et 4)
git clone https://github.com/zdharma-continuum/fast-syntax-highlighting.git \
  ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/plugins/fast-syntax-highlighting
```

### 3.3 : Configuration du fichier .zshrc

Maintenant, activez tous vos plugins dans `~/.zshrc` :

```bash
# Éditer ~/.zshrc
nano ~/.zshrc

# Chercher la ligne "plugins=(git)" et remplacer par :
plugins=(
# === Core ===
    git
    sudo
    z
    aliases
    common-aliases

# === Data Engineering ===
    docker
    docker-compose
    python
    pip
    kubectl
    terraform
    aws
    gcloud

# === Utilities ===
    web-search
    jsontools
    colored-man-pages
    command-not-found

# === External plugins (à installer manuellement) ===
    zsh-autosuggestions
    zsh-syntax-highlighting
    zsh-completions
)

# Sauvegarder et recharger
source ~/.zshrc
```

#### ⚠️ Ordre des plugins

**IMPORTANT** : `zsh-syntax-highlighting` doit être le
**dernier**
plugin de la liste pour fonctionner correctement.

## ⚙️ Étape 4 : Configuration Avancée pour Data Engineers

### 4.1 : Alias personnalisés pour Data Engineering

Ajoutez ces alias à la fin de votre `~/.zshrc` :

```bash
# ============================================
# ALIAS PERSONNALISÉS POUR DATA ENGINEERING
# ============================================

# === Python & Virtual Environments ===
alias py='python3'
alias pip='pip3'
alias venv='python3 -m venv'
alias activate='source venv/bin/activate'
alias deactivate='deactivate'
alias pipr='pip install -r requirements.txt'
alias pipf='pip freeze > requirements.txt'

# === Docker ===
alias d='docker'
alias dc='docker-compose'
alias dps='docker ps'
alias dpsa='docker ps -a'
alias dimg='docker images'
alias dexec='docker exec -it'
alias dlogs='docker logs -f'
alias dclean='docker system prune -af --volumes'
alias dstop='docker stop $(docker ps -q)'

# === Git (en plus de ceux fournis par le plugin) ===
alias gs='git status'
alias ga='git add'
alias gaa='git add .'
alias gc='git commit -m'
alias gp='git push'
alias gl='git pull'
alias glog='git log --oneline --graph --all --decorate'
alias gdiff='git diff'

# === Kubernetes ===
alias k='kubectl'
alias kgp='kubectl get pods'
alias kgs='kubectl get services'
alias kgd='kubectl get deployments'
alias klogs='kubectl logs -f'
alias kdesc='kubectl describe'

# === Fichiers & Navigation ===
alias ll='ls -alFh'
alias la='ls -A'
alias l='ls -CF'
alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'
alias ~='cd ~'

# === Data Engineering spécifiques ===
alias csvhead='head -n 20'  # Voir les 20 premières lignes d'un CSV
alias csvcount='wc -l'      # Compter les lignes
alias jsonpretty='python -m json.tool'  # Formater du JSON
alias serve='python3 -m http.server'    # Serveur HTTP rapide

# === Airflow (si utilisé) ===
alias afl='airflow'
alias afldb='airflow db init'
alias aflweb='airflow webserver -p 8080'
alias aflsch='airflow scheduler'

# === Spark (si utilisé) ===
alias pyspark='pyspark --master local[*]'
alias spark-submit='spark-submit --master local[*]'

# === Monitoring ===
alias ports='netstat -tulanp'
alias mem='free -h'
alias cpu='top'
```

### 4.2 : Variables d'environnement

```bash
# ============================================
# VARIABLES D'ENVIRONNEMENT
# ============================================

# Python
export PYTHONPATH="${PYTHONPATH}:${HOME}/projects"

# Éditeur par défaut
export EDITOR='nano'  # ou 'vim', 'code'

# Spark (si installé)
export SPARK_HOME=/usr/local/spark
export PATH=$PATH:$SPARK_HOME/bin

# Java (si nécessaire pour Spark, Kafka, etc.)
export JAVA_HOME=$(/usr/libexec/java_home)  # macOS
# export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64  # Linux

# Airflow
export AIRFLOW_HOME=~/airflow

# Historique
export HISTSIZE=10000
export SAVEHIST=10000
export HISTFILE=~/.zsh_history
```

## 🎯 Étape 4 : Configuration Finale et Optimisations

### 4.3 : Options Zsh recommandées

```bash
# ============================================
# OPTIONS ZSH
# ============================================

# Correction automatique des typos
setopt CORRECT
setopt CORRECT_ALL

# Navigation
setopt AUTO_CD              # cd automatique sans taper cd
setopt AUTO_PUSHD           # Push automatique dans la pile
setopt PUSHD_IGNORE_DUPS    # Ignorer les doublons dans la pile

# Historique
setopt HIST_IGNORE_DUPS     # Ignorer les doublons dans l'historique
setopt HIST_IGNORE_SPACE    # Ignorer les commandes commençant par espace
setopt HIST_VERIFY          # Vérifier avant d'exécuter une commande de l'historique
setopt SHARE_HISTORY        # Partager l'historique entre sessions

# Complétion
setopt COMPLETE_IN_WORD     # Complétion au milieu d'un mot
setopt ALWAYS_TO_END        # Curseur à la fin après complétion

# Globbing
setopt EXTENDED_GLOB        # Globbing étendu (patterns avancés)
```

### 4.4 : Personnalisation de zsh-autosuggestions

```bash
# Couleur des suggestions (gris plus visible)
ZSH_AUTOSUGGEST_HIGHLIGHT_STYLE='fg=240'

# Stratégie de suggestions (historique + completion)
ZSH_AUTOSUGGEST_STRATEGY=(history completion)

# Accepter une suggestion avec Ctrl+Space
bindkey '^ ' autosuggest-accept
```

### 4.5 : Fichier .zshrc complet recommandé

Voici un exemple de `~/.zshrc` complet et optimisé pour Data Engineers :

```bash
# ============================================
# OH MY ZSH CONFIGURATION
# ============================================

# Path to oh-my-zsh installation
export ZSH="$HOME/.oh-my-zsh"

# Theme - Powerlevel10k
ZSH_THEME="powerlevel10k/powerlevel10k"

# Plugins
plugins=(
# Core
    git
    sudo
    z
    aliases
    common-aliases
    colored-man-pages
    command-not-found

# Data Engineering
    docker
    docker-compose
    python
    pip
    kubectl
    terraform
    aws
    gcloud

# Utilities
    web-search
    jsontools

# External (install manually)
    zsh-autosuggestions
    zsh-completions
    zsh-syntax-highlighting  # MUST BE LAST
)

# Load Oh My Zsh
source $ZSH/oh-my-zsh.sh

# ============================================
# POWERLEVEL10K INSTANT PROMPT
# ============================================
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

# To customize prompt, run `p10k configure` or edit ~/.p10k.zsh.
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh

# ============================================
# ZSH OPTIONS
# ============================================
setopt CORRECT
setopt AUTO_CD
setopt AUTO_PUSHD
setopt PUSHD_IGNORE_DUPS
setopt HIST_IGNORE_DUPS
setopt HIST_IGNORE_SPACE
setopt HIST_VERIFY
setopt SHARE_HISTORY
setopt COMPLETE_IN_WORD
setopt ALWAYS_TO_END
setopt EXTENDED_GLOB

# ============================================
# ENVIRONMENT VARIABLES
# ============================================
export EDITOR='nano'
export PYTHONPATH="${PYTHONPATH}:${HOME}/projects"
export HISTSIZE=10000
export SAVEHIST=10000
export HISTFILE=~/.zsh_history

# ============================================
# ALIASES - PYTHON & VENV
# ============================================
alias py='python3'
alias pip='pip3'
alias venv='python3 -m venv'
alias activate='source venv/bin/activate'
alias pipr='pip install -r requirements.txt'
alias pipf='pip freeze > requirements.txt'

# ============================================
# ALIASES - DOCKER
# ============================================
alias d='docker'
alias dc='docker-compose'
alias dps='docker ps'
alias dpsa='docker ps -a'
alias dimg='docker images'
alias dexec='docker exec -it'
alias dlogs='docker logs -f'
alias dclean='docker system prune -af --volumes'
alias dstop='docker stop $(docker ps -q)'

# ============================================
# ALIASES - GIT
# ============================================
alias gs='git status'
alias ga='git add'
alias gaa='git add .'
alias gc='git commit -m'
alias gp='git push'
alias gl='git pull'
alias glog='git log --oneline --graph --all'

# ============================================
# ALIASES - KUBERNETES
# ============================================
alias k='kubectl'
alias kgp='kubectl get pods'
alias kgs='kubectl get services'
alias klogs='kubectl logs -f'

# ============================================
# ALIASES - FILES & NAVIGATION
# ============================================
alias ll='ls -alFh'
alias la='ls -A'
alias ..='cd ..'
alias ...='cd ../..'

# ============================================
# ALIASES - DATA ENGINEERING
# ============================================
alias csvhead='head -n 20'
alias csvcount='wc -l'
alias jsonpretty='python -m json.tool'
alias serve='python3 -m http.server'

# ============================================
# ZSH-AUTOSUGGESTIONS CONFIG
# ============================================
ZSH_AUTOSUGGEST_HIGHLIGHT_STYLE='fg=240'
ZSH_AUTOSUGGEST_STRATEGY=(history completion)
bindkey '^ ' autosuggest-accept

# ============================================
# END OF CONFIGURATION
# ============================================
```

#### ✅ Application de la configuration

Après avoir modifié votre `~/.zshrc`, rechargez-le :

```bash
source ~/.zshrc
```

## 🎓 Étape 5 : Vérification et Tests

### 5.1 : Checklist de vérification

#### ✅ Vérifiez que tout fonctionne

1. **Powerlevel10k** : Vous voyez un prompt coloré avec des icônes
2. **Autosuggestions** : Tapez `git` et voyez des suggestions grises
3. **Syntax highlighting** : Les commandes valides sont en vert, invalides en
   rouge
4. **Plugins Git** : Tapez `gst` (alias de git status)
5. **Plugin Docker** : Tapez `docker`  puis Tab pour
   l'autocomplétion
6. **Plugin z** : Naviguez dans des dossiers, puis testez `z
   nom_du_dossier`
7. **Alias personnalisés** : Testez `ll`, `py`,
   `d`

### 5.2 : Commandes de test

```bash
# Test 1: Vérifier les plugins chargés
omz plugin list

# Test 2: Vérifier les alias Git
alias | grep git

# Test 3: Tester l'autocomplétion Docker
docker

# Test 4: Tester une fonction personnalisée
csvinfo --help  # (si vous avez créé cette fonction)

# Test 5: Vérifier le thème
echo $ZSH_THEME
# Output: powerlevel10k/powerlevel10k

# Test 6: Naviguer avec z
cd ~/Documents
cd ~/Downloads
cd ~/Desktop
z Doc  # Devrait vous ramener dans ~/Documents
```

## 💡 Astuces et Conseils Avancés

### 🚀 Astuces de productivité

- **Ctrl + R** : Recherche inversée dans l'historique (puis tapez votre
  recherche)
- **!! : Répète la dernière commande**
- **!$** : Utilise le dernier argument de la commande précédente
- **cd -** : Retourne au dossier précédent
- **Ctrl + U** : Efface toute la ligne
- **Ctrl + W** : Efface le mot précédent
- **Ctrl + L** : Efface l'écran (équivalent à `clear`)
- **ESC ESC** : Ajoute `sudo` au début de la commande (plugin sudo)

### Maintenance et mises à jour

```bash
# Mettre à jour Oh My Zsh
omz update

# Mettre à jour Powerlevel10k
git -C ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k pull

# Mettre à jour les plugins externes
cd ~/.oh-my-zsh/custom/plugins/zsh-autosuggestions && git pull
cd ~/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting && git pull
cd ~/.oh-my-zsh/custom/plugins/zsh-completions && git pull

# Ou créer un alias pour tout mettre à jour
alias update-zsh='omz update && \
  git -C ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k pull && \
  git -C ~/.oh-my-zsh/custom/plugins/zsh-autosuggestions pull && \
  git -C ~/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting pull'
```

## 📚 Ressources Complémentaires

#### Documentation officielle

- [Oh My Zsh](https://ohmyz.sh/)
- [Powerlevel10k](https://github.com/romkatv/powerlevel10k)
- [zsh-autosuggestions](https://github.com/zsh-users/zsh-autosuggestions)

#### Plugins intéressants

- [Liste des plugins Oh My Zsh](https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins)
- [Awesome Zsh
  Plugins](https://github.com/unixorn/awesome-zsh-plugins)

#### Polices et thèmes

- [Nerd Fonts](https://www.nerdfonts.com/)
- [Thèmes Oh My
  Zsh](https://github.com/ohmyzsh/ohmyzsh/wiki/Themes)

#### ✅ Partie 8 terminée ! 🎉

Félicitations ! Vous avez maintenant un terminal professionnel, moderne et optimisé pour le Data
Engineering avec :

- ✅ Oh My Zsh installé et configuré
- ✅ Powerlevel10k comme thème
- ✅ Plugins essentiels pour Data Engineering
- ✅ Alias et fonctions personnalisés
- ✅ Configuration optimisée

Votre terminal est maintenant **10x plus productif** ! 🚀

[← Retour à l'accueil](../index.md)