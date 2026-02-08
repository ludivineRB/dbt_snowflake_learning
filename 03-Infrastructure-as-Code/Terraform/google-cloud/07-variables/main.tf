variable "project_id" {
  type = string
}

resource "google_storage_bucket" "bucket" {
  name     = "bucket-${var.project_id}"
  location = "EU"
}
