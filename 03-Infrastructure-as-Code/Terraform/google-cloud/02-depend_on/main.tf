resource "google_service_account" "sa" {
  account_id   = "sa-test-dep"
  display_name = "Service Account pour Test Dépendance"
}

resource "google_storage_bucket" "bucket" {
  name     = "bucket-dep-test-${google_service_account.sa.account_id}"
  location = "EU"

  # Dépendance explicite
  depends_on = [
    google_service_account.sa
  ]
}