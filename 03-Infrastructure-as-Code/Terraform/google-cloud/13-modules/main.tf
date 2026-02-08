module "network" {
  source = "../../modules/network" # Exemple de source locale
  
  vpc_name = "prod-vpc"
}
