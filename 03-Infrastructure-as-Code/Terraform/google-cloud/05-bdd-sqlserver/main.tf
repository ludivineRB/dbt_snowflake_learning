resource "google_sql_database_instance" "db" {
  name             = "db-instance-tf"
  region           = "europe-west1"
  database_version = "POSTGRES_15"
  settings {
    tier = "db-f1-micro"
  }
  deletion_protection = false
}

resource "google_sql_database" "database" {
  name     = "app-db"
  instance = google_sql_database_instance.db.name
}