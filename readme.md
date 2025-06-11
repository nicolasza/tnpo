
# que es esto
Esto es un proyecto base de deployment de infrastructura y contenedor, basado en los requerimientos del archivo (prueba-ml-engineer.pdf)[prueba-ml-engineer.pdf]

# pasos realizados desde los documentos base
* crear git
* crear ambiente env python 3.12
* orden de carpetas
* primero crear codigo base para iniciar el proyecto como api(comentar con docstring).
* transformar modelo zip a pt (cambiar extension)
* implementar container de app (dockerfile)
* testing unitario
* implementar CI/CD github actions
* implementar IaC terraform
* implementar mlflow versionamiento de modelo

# requerimientos para la implementacion
* python 3.12
* gcloud CLI
* terraform

# pasos para habilitar la infrastructura y primer run
* crear containerregistry en google para proyecto (doc configContenedores.txt)
* crear imagen docker Base con pt al  y realizar push manual
* crear permisos necesarios de gcloud para la ejecucion de terraform (doc permisosTerraform.txt) 
    * * habilitar adicionalmnete api de identidad y control de acceso
    * * habilitar cloud run admin api
* crear infra con terraform (subir a bucket y habilitar maquina con gcloud run)
    * * terraform init
    * * terraform plan -out=tfplan
    * * terraform apply tfplan
* crear permisos necesarios para push y deploy desde github actions (archivo permisosGithub.txt)
