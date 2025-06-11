output "url_cloud_run" {
  value = google_cloud_run_service.inference_model.status[0].url
}

