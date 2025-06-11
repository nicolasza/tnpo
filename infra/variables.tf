variable "project_id" {
  type        = string
  description = "ID del proyecto de GCP"
}
variable "region" {
  default = "us-central1"
}
variable "model_bucket" {
  default = "mdl_tnpo_2025"
}
variable "model_filename" {
  default = "doubleit-model.pt"
}
variable "service_name" {
  default = "inference-ml-model"
}
variable "container_register" {
  default = "us-central1-docker.pkg.dev"
}
variable "repo_name" {
  default = "ml-models"
}
variable "image_name" {
  default = "inference-ml"
}
variable "image_tag" {
  default = "latest"
}
variable "container_concurrency" {
  default = 20
}
variable "min_instances" {
  default = 0
}
variable "max_instances" {
  default = 1
}
