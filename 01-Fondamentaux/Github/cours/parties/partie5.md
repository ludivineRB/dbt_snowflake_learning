## Objectifs de cette partie

- Comprendre GitHub Actions et ses concepts clés
- Créer des workflows d'automatisation
- Mettre en place tests automatiques Python
- Configurer le linting et formatage de code
- Déployer des pipelines Data sur Azure
- Gérer les secrets en toute sécurité

## Qu'est-ce que GitHub Actions ?

**GitHub Actions** est un système d'automatisation intégré à GitHub qui permet de :

- 🧪 Exécuter des tests automatiquement
- 🏗️ Builder et déployer des applications
- 📦 Publier des packages
- 🔍 Analyser la qualité du code
- 🚀 Déployer des pipelines de données

### Concepts clés

| Concept | Description |
| --- | --- |
| **Workflow** | Processus automatisé défini dans un fichier YAML |
| **Job** | Ensemble d'étapes qui s'exécutent sur le même runner |
| **Step** | Commande ou action individuelle |
| **Runner** | Machine virtuelle qui exécute les workflows (Ubuntu, macOS, Windows) |
| **Action** | Composant réutilisable (ex: checkout code, setup Python) |

### Exemple 1 : Tests automatiques Python

Créez le fichier `.github/workflows/tests.yml` :

```bash
name: Tests

# Trigger: quand et comment le workflow s'exécute
on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        python-version: ['3.9', '3.10', '3.11']

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v5
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pytest pytest-cov
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

    - name: Run tests
      run: |
        pytest tests/ --cov=src --cov-report=xml

    - name: Upload coverage
      uses: codecov/codecov-action@v4
      with:
        file: ./coverage.xml
        fail_ci_if_error: true
```

### Exemple 2 : Linter et formateur de code

Fichier `.github/workflows/lint.yml` :

```bash
name: Code Quality

on:
  pull_request:
    branches: [ main ]

jobs:
  lint:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'

    - name: Install linters
      run: |
        pip install black flake8 mypy

    - name: Check code formatting with Black
      run: black --check src/ tests/

    - name: Lint with Flake8
      run: flake8 src/ tests/ --max-line-length=100

    - name: Type check with MyPy
      run: mypy src/
```

### Exemple 3 : Déploiement d'un pipeline Data sur Azure

Fichier `.github/workflows/deploy.yml` :

```bash
name: Deploy to Azure Production

on:
  push:
    tags:
      - 'v*'  # Déclenche sur les tags comme v1.0.0

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        pip install -r requirements.txt

    - name: Azure Login
      uses: azure/login@v1
      with:
        creds: ${{ secrets.AZURE_CREDENTIALS }}

    - name: Build and push Docker image to Azure Container Registry
      run: |
        az acr login --name myregistry
        docker build -t myregistry.azurecr.io/data-pipeline:${{ github.ref_name }} .
        docker push myregistry.azurecr.io/data-pipeline:${{ github.ref_name }}

    - name: Deploy to Azure Container Instances
      run: |
        az container create \
          --resource-group data-engineering-rg \
          --name data-pipeline \
          --image myregistry.azurecr.io/data-pipeline:${{ github.ref_name }} \
          --cpu 2 --memory 4 \
          --registry-login-server myregistry.azurecr.io \
          --registry-username ${{ secrets.AZURE_ACR_USERNAME }} \
          --registry-password ${{ secrets.AZURE_ACR_PASSWORD }} \
          --restart-policy OnFailure

    - name: Notify Slack
      uses: 8398a7/action-slack@v3
      with:
        status: ${{ job.status }}
        text: 'Deployment to Azure production completed!'
        webhook_url: ${{ secrets.SLACK_WEBHOOK }}
      if: always()
```

### Secrets : Gérer les credentials

Pour stocker des informations sensibles (API keys, passwords, Azure credentials) :

1. Allez dans **Settings** → **Secrets and variables** →
   **Actions**
2. Cliquez sur **New repository secret**
3. Nom : `AZURE_CREDENTIALS`
4. Valeur : Votre JSON de credentials Azure (créé avec `az ad sp create-for-rbac`)
5. Cliquez sur **Add secret**

Utilisation dans le workflow :

```bash
- name: Use secret
  run: echo ${{ secrets.AZURE_CREDENTIALS }}  # Masqué dans les logs
```

#### Sécurité des secrets

Les secrets sont automatiquement masqués dans les logs. Ne les affichez jamais explicitement.

### Marketplace GitHub Actions

Le [GitHub Actions
Marketplace](https://github.com/marketplace?type=actions)
contient des milliers d'actions prêtes à l'emploi :

- **actions/checkout** : Cloner le repository
- **actions/setup-python** : Configurer Python
- **docker/build-push-action** : Builder et pusher une image Docker
- **aws-actions/configure-aws-credentials** : Configurer AWS CLI
- **codecov/codecov-action** : Uploader la couverture de code

### Bonnes pratiques GitHub Actions

- Utilisez des actions du marketplace plutôt que de réinventer
- Vérifiez les versions des actions (utilisez @v4, pas @main)
- Cachez les dépendances avec `actions/cache`
- Limitez les déclencheurs (pas besoin de CI sur chaque push)
- Divisez les workflows longs en jobs parallèles
- Utilisez des matrix builds pour tester sur plusieurs versions
- Ne jamais hardcoder de secrets dans les fichiers YAML

#### Prochaine étape

Vous savez maintenant automatiser avec GitHub Actions ! Passons à la **Partie 6** pour
sécuriser vos projets.

[← Partie 4 : Issues et Projects](partie4.md)
[Partie 6 : Sécurité →](partie6.md)