# 15 - Cloud Run (Serverless Containers)

[← 14 - Exercices](14-exercices.md) | [🏠 Accueil](../00-README.md)

---

## 1. Introduction à Cloud Run

Cloud Run est le service serverless de Google pour exécuter des conteneurs (Docker). C'est l'équivalent moderne et plus flexible d'Azure App Service.

---

## 2. Déploiement d'un service Cloud Run

```hcl
resource "google_cloud_run_v2_service" "web_app" {
  name     = "my-web-app"
  location = "europe-west1"
  ingress  = "INGRESS_TRAFFIC_ALL"

  template {
    containers {
      image = "us-docker.pkg.dev/cloudrun/container/hello" # Image publique de test
      
      ports {
        container_port = 8080
      }

      env {
        name  = "ENV"
        value = "production"
      }
    }
  }
}
```

---

## 3. Autoriser l'accès public (No-Auth)

Par défaut, Cloud Run est privé. Pour une application web publique :

```hcl
resource "google_cloud_run_v2_service_iam_member" "public_access" {
  location = google_cloud_run_v2_service.web_app.location
  name     = google_cloud_run_v2_service.web_app.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}
```

---

## 4. Connexion à Cloud SQL

Pour qu'un service Cloud Run parle à une base Cloud SQL en IP privée, on utilise généralement le "Cloud SQL Proxy" intégré.

```hcl
template {
  containers {
    # ...
    volume_mounts {
      name       = "cloudsql"
      mount_path = "/cloudsql"
    }
  }
  volumes {
    name = "cloudsql"
    cloud_sql_instance {
      instances = [google_sql_database_instance.main_db.connection_name]
    }
  }
}
```

---

## 5. Pourquoi Cloud Run pour la Data ?

- **Microservices d'API** : Exposer vos données via des API FastAPI/Flask.
- **Webhooks** : Recevoir des notifications de systèmes externes.
- **Triggers** : Lancer un traitement suite à l'arrivée d'un fichier dans un Bucket (via Eventarc).

---

[← 14 - Exercices](14-exercices.md) | [🏠 Accueil](../00-README.md)
