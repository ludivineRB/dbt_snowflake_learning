variable "bucket_names" {
  type    = list(string)
  default = ["raw", "processed", "gold"]
}

resource "google_storage_bucket" "multi" {
  for_each = toset(var.bucket_names)
  name     = "my-multi-bucket-${each.value}"
  location = "EU"
}
