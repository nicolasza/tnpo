# Crear bucket para el modelo
resource "google_storage_bucket" "model_bucket" {
  name          = var.model_bucket
  location      = var.region
  force_destroy = true
}

# Subir el modelo al bucket
resource "google_storage_bucket_object" "model_pt" {
  name   = var.model_filename
  bucket = google_storage_bucket.model_bucket.name
  source = "${path.module}/../model/${var.model_filename}"
}
