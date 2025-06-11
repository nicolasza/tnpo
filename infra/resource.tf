# Crear servicio Cloud Run
resource "google_cloud_run_service" "inference_model" {
  depends_on = [google_artifact_registry_repository_iam_member.allow_container_pull]
  name     = var.service_name
  location = var.region

  template {
    spec {
      containers {
        image = "${var.container_register}/${var.project_id}/${var.repo_name}/${var.image_name}:${var.image_tag}"

        resources {
          limits = {
            memory = "2Gi"
            cpu    = "1"
          }
        }

        env {
          name  = "MODEL_GCS"
          value = "gs://${google_storage_bucket.model_bucket.name}/${google_storage_bucket_object.model_pt.name}"
        }

        ports {
          container_port = 8080
        }
      }

      container_concurrency = var.container_concurrency
      service_account_name  = google_service_account.cloudrun_executor.email
    }

    metadata {
      annotations = {
        "autoscaling.knative.dev/minScale" = var.min_instances
        "autoscaling.knative.dev/maxScale" = var.max_instances
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }

  metadata {
    annotations = {
      "run.googleapis.com/ingress" = "all"
    }
  }

  autogenerate_revision_name = true
}

# Permitir invocación pública
resource "google_cloud_run_service_iam_member" "allow_all" {
  service  = google_cloud_run_service.inference_model.name
  location = google_cloud_run_service.inference_model.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}
