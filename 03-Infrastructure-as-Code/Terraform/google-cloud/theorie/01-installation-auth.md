# 01 - Installation et Authentification

[🏠 Accueil](../00-README.md) | [02 - Workload Identity Federation →](02-workload-identity-federation.md)

---

## 1. Installation des outils

### Google Cloud CLI (gcloud)

#### Linux
```bash
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
gcloud init
```

#### macOS (Homebrew)
```bash
brew install --cask google-cloud-sdk
```

#### Windows
Téléchargez l'installateur sur [cloud.google.com/sdk/docs/install](https://cloud.google.com/sdk/docs/install).

---

### Terraform

Suivez les instructions du cours général ou utilisez votre gestionnaire de paquets :
- **macOS** : `brew install terraform`
- **Linux** : `sudo apt-get install terraform`

---

## 2. Authentification pour le développement

Pour que Terraform puisse agir sur votre compte GCP depuis votre machine, nous utilisons l'**Application Default Credentials (ADC)**.

```bash
# Se connecter à votre compte Google
gcloud auth login

# Configurer les identifiants par défaut pour Terraform
gcloud auth application-default login
```

Cette commande génère un fichier JSON local que Terraform détectera automatiquement pour s'authentifier.

---

## 3. Configuration du projet par défaut

Terraform a besoin de savoir dans quel projet travailler.

```bash
# Lister vos projets
gcloud projects list

# Définir le projet actuel
gcloud config set project VOTRE_PROJECT_ID
```

---

[🏠 Accueil](../00-README.md) | [02 - Workload Identity Federation →](02-workload-identity-federation.md)
