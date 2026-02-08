# 03 - Plugins et Personnalisation pour la Data

[← 02 - OMZ & P10k](02-oh-my-zsh-p10k.md) | [🏠 Accueil](../README.md)

---

## 1. Plugins indispensables (Oh My Zsh)

Activez ces plugins dans votre `~/.zshrc` :
```bash
plugins=(
    git
    docker
    docker-compose
    python
    pip
    kubectl
    terraform
    aws
    zsh-autosuggestions
    zsh-syntax-highlighting
)
```

- **zsh-autosuggestions** : Suggère des commandes basées sur votre historique (Gris).
- **zsh-syntax-highlighting** : Colore les commandes en Vert si elles existent, en Rouge sinon.

---

## 2. Alias avancés pour Data Engineer

```bash
# Python & Venv
alias venv='python3 -m venv venv'
alias activate='source venv/bin/activate'

# Docker
alias dps='docker ps'
alias dlogs='docker logs -f'
alias dclean='docker system prune -af'

# Kubernetes
alias k='kubectl'
alias kgp='kubectl get pods'

# Data files
alias csvhead='head -n 20'
alias jsonpretty='python3 -m json.tool'
```

---

## 3. Maintenance
```bash
# Mettre à jour Oh My Zsh
omz update

# Recharger la configuration sans fermer le terminal
source ~/.zshrc
```

---

[← 02 - OMZ & P10k](02-oh-my-zsh-p10k.md) | [🏠 Accueil](../README.md)