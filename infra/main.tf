provider "google" {
  project = var.project_id
  region  = var.region
}

# Crear bucket para subir el modelo
resource "google_storage_bucket" "model_bucket" {
  name     = var.model_bucket
  location = var.region
  force_destroy = true
}

# Subir el modelo al bucket
resource "google_storage_bucket_object" "model_pt" {
  name   = "doubleit-model.pt"
  bucket = google_storage_bucket.model_bucket.name
  source = "${path.module}/../model/doubleit-model.pt"
}

# Construir imagen y desplegar en Cloud Run
resource "google_cloud_run_service" "inference_model" {
  name     = "inference-ml-model"
  location = var.region

  template {
    spec {
      containers {
        image = "gcr.io/${var.project_id}/flask-ml-model"
        ports {
          container_port = 8080
        }
        env {
          name  = "MODEL_PATH"
          value = "gs://${google_storage_bucket.model_bucket.name}/${google_storage_bucket_object.model_pt.name}"
        }
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

resource "google_cloud_run_service_iam_member" "allow_all" {
  service  = google_cloud_run_service.inference_model.name
  location = google_cloud_run_service.inference_model.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}
