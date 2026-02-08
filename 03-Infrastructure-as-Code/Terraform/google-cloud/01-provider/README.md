# 01 - Configuration du Provider GCP

## Objectif
Configurer Terraform pour interagir avec Google Cloud Platform.

## Concepts
- Bloc `terraform` : définit les versions requises.
- Bloc `provider` : définit le projet et la région par défaut.

## Authentification
Utilisez ADC (Application Default Credentials) :
```bash
gcloud auth application-default login
```