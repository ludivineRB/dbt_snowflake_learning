provider "google" {
  alias   = "paris"
  project = "VOTRE_PROJECT_ID"
  region  = "europe-west9"
}

provider "google" {
  alias   = "belgium"
  project = "VOTRE_PROJECT_ID"
  region  = "europe-west1"
}

resource "google_storage_bucket" "bucket_paris" {
  provider = google.paris
  name     = "bucket-paris-tf-demo"
  location = "europe-west9"
}

resource "google_storage_bucket" "bucket_belgium" {
  provider = google.belgium
  name     = "bucket-belgium-tf-demo"
  location = "europe-west1"
}
