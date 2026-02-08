data "google_compute_network" "default" {
  name = "default"
}

output "default_vpc_id" {
  value = data.google_compute_network.default.id
}
