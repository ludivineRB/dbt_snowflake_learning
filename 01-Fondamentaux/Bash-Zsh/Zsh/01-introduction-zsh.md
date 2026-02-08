# 01 - Introduction à Zsh

[🏠 Accueil](../README.md) | [02 - Oh My Zsh et P10k →](02-oh-my-zsh-p10k.md)

---

## 1. Pourquoi Zsh ?

Zsh (Z Shell) est une version moderne et améliorée de Bash. Bien que compatible avec Bash, il offre des fonctionnalités indispensables au quotidien :

- **Autocomplétion intelligente** : Sensible au contexte (fichiers, branches git, options de commandes).
- **Globbing avancé** : `ls **/*.csv` pour chercher récursivement dans les dossiers.
- **Historique partagé** : Les commandes tapées dans un terminal sont disponibles dans les autres instantanément.
- **Frameworks** : Comme Oh My Zsh, qui facilite la configuration.

---

## 2. Vérifier son environnement

```bash
# Quel shell j'utilise ?
echo $SHELL

# Version de Zsh
zsh --version
```

---

## 3. Changer son shell par défaut

```bash
# Définir Zsh par défaut
chsh -s /bin/zsh
```
*(Nécessite de fermer et rouvrir la session)*

---

[🏠 Accueil](../README.md) | [02 - Oh My Zsh et P10k →](02-oh-my-zsh-p10k.md)