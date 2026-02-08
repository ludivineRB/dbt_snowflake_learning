resource "google_storage_bucket" "bucket" {
  name     = "bucket-provisioner-demo"
  location = "europe-west1"

  provisioner "local-exec" {
    command = "echo 'Le bucket ${self.name} a été créé le $(date)' > creation_log.txt"
  }
}
