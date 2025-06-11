# Este script sube un modelo TorchScript a MLflow y lo exporta a GCS para ser usado por una API de inferencia.

import hashlib
import os
import shutil

import mlflow
from google.cloud import storage
from mlflow.tracking import MlflowClient

# === Configuración general ===
MODEL_FILE = "doubleit-model.pt"
MODEL_NAME = "doubleit-model"
EXPERIMENT_NAME = "inferencia-modelos"
GCS_BUCKET = "modelos-mlflow"
GCS_EXPORT_PATH = f"exports/{MODEL_FILE}"  # export final en GCS
MLFLOW_TRACKING_URI = "http://mlflow-tracking.example.com"  # Cambiar según despliegue

# === Inicialización de clientes ===
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
mlflow.set_experiment(EXPERIMENT_NAME)
mlflow_client = MlflowClient()
gcs_client = storage.Client()

# === Funciones ===
def file_hash(filepath):
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

def get_existing_hashes(model_name):
    versions = mlflow_client.search_model_versions(f"name='{model_name}'")
    hashes = {}
    for v in versions:
        run = mlflow_client.get_run(v.run_id)
        if "model_hash" in run.data.params:
            hashes[run.data.params["model_hash"]] = v.version
    return hashes

def upload_to_gcs(local_path: str, bucket: str, blob_path: str):
    bucket_ref = gcs_client.bucket(bucket)
    blob = bucket_ref.blob(blob_path)
    blob.upload_from_filename(local_path)
    print(f"✅ Modelo exportado a: gs://{bucket}/{blob_path}")

# === Main ===
def main():
    hash_pt = file_hash(MODEL_FILE)
    existing = get_existing_hashes(MODEL_NAME)

    if hash_pt in existing:
        print(f"🔁 Modelo ya registrado como versión {existing[hash_pt]}. No se sube.")
        return

    with mlflow.start_run(run_name="registro-hibrido") as run:
        mlflow.log_param("model_hash", hash_pt)
        mlflow.log_param("model_file", MODEL_FILE)

        # Registrar artefacto
        mlflow.log_artifact(MODEL_FILE, artifact_path="model")

        result = mlflow.register_model(
            model_uri=f"runs:/{run.info.run_id}/model",
            name=MODEL_NAME
        )

        print(f"📦 Modelo registrado como: {MODEL_NAME} v{result.version}")

        mlflow_client.transition_model_version_stage(
            name=MODEL_NAME,
            version=result.version,
            stage="Production",
            archive_existing_versions=True
        )
        print(f"🚀 Promovido a 'Production': v{result.version}")

        # Exportar modelo a GCS (hibrido)
        upload_to_gcs(MODEL_FILE, GCS_BUCKET, GCS_EXPORT_PATH)

if __name__ == "__main__":
    main()
