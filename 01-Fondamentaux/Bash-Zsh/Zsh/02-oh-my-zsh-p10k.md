# 02 - Oh My Zsh et Powerlevel10k

[← 01 - Introduction](01-introduction-zsh.md) | [🏠 Accueil](../README.md) | [03 - Plugins et Customization →](03-plugins-custom.md)

---

## 1. Installation de Oh My Zsh

Le framework indispensable pour gérer sa configuration.

```bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

---

## 2. Thème Powerlevel10k

C'est le thème le plus rapide et le plus informatif (branche Git, venv Python, état Docker).

### Installation
```bash
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k
```

### Activation
Dans votre `~/.zshrc`, remplacez la ligne du thème :
```bash
ZSH_THEME="powerlevel10k/powerlevel10k"
```

---

## 3. Nerd Fonts (Crucial pour les icônes)

Powerlevel10k utilise des icônes pour afficher l'état de votre projet.
1. Téléchargez **MesloLGS NF**.
2. Configurez votre terminal pour utiliser cette police.
3. Lancez `p10k configure` pour paramétrer votre prompt visuellement.

---

[← 01 - Introduction](01-introduction-zsh.md) | [🏠 Accueil](../README.md) | [03 - Plugins et Customization →](03-plugins-custom.md)