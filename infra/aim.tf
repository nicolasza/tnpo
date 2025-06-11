# Crear cuenta de servicio para Cloud Run
resource "google_service_account" "cloudrun_executor" {
  account_id   = "cloudrun-executor"
  display_name = "Cuenta de servicio para Cloud Run con acceso a GCS"
}

# Darle permisos para leer el bucket
resource "google_storage_bucket_iam_member" "cloudrun_model_access" {
  bucket = google_storage_bucket.model_bucket.name
  role   = "roles/storage.objectViewer"
  member = "serviceAccount:${google_service_account.cloudrun_executor.email}"
}

#permiso para leer los contenedores
resource "google_artifact_registry_repository_iam_member" "allow_container_pull" {
  project    = var.project_id
  location   = var.region
  repository = var.repo_name
  role       = "roles/artifactregistry.reader"
  member     = "serviceAccount:${google_service_account.cloudrun_executor.email}"
}

