
# ¿Que es esto?
Esto es un proyecto base de deployment de infrastructura y contenedor, basado en los requerimientos del archivo [prueba-ml-engineer.pdf](prueba-ml-engineer.pdf)

# Pasos realizados desde los documentos base
Estos fueron los pasos que realice desde que recibi la prueba tecnica, esta seccion es solo como un orden mental.
* Crear git (cree el github para almacenar el codigo y los action)
* Crear ambiente env python 3.12, con el objetivo de tener un codigo funcional base y poder implementarlo en contenedor.
* Orden de carpetas, con el objetivo de tener un orden en los codigos y herramientas asociadas al mismo.
* Crear codigo base para iniciar el proyecto como api, utilice fastapi para la realizacion de este.
* Transformar modelo zip a pt (cambiar extension), el ejemplo de codigo venia con .pt la utilizacion y el documento compartido del modelo venia en zip.
* Crear dockerfile y realizar pruebas en entorno docker.
* Implementar IaC en terraform.
* Testing unitario y de api
* Creacion de archivo make para facilitar ambiente y pruebas en linux
* Implementar CI/CD github actions, con el objetivo de consolidar el make y facilitar el deployment.


# Requerimientos para la implementacion
* [Python 3.12](https://www.python.org/downloads/release/python-3120/)
* [Gcloud CLI](https://cloud.google.com/sdk/docs/install)
* [Terraform](https://developer.hashicorp.com/terraform/install)
* [Docker](https://www.docker.com/)

# Estructura de Carpetas

* .github/workflows : contiene el workflow de github, con las pruebas "CI" y el deploy "CD".
* infra: contiene la definicion de infrastructura de terraform
* model: carpeta asociada al modelo, aqui debe ir el modelo a utilizar 
* test: carpeta asociada a las pruebas del codigo
* tnpo: carpeta de codigo principal

# Pasos para habilitar la infrastructura y primer deploy

Para seguir estos pasos considerar cambiar el nombre del proyecto(utilizar el de su preferencia) en cada comando de gcloud especificado, al igual que en la definicion de terraform.

1. Primero es necesario crear el containerregistry en Google para el proyecto, seguir los comandos en orden del archivo [configContenedores.txt](configContenedores.txt)

2. Luego se debe crear la imagen docker Base incluyendo el archivo de modelo .pt y realizar push manual al registro.
    * Utilizar el comando "docker build -t \<tag> ." considerando el enlace de registro creado anteriormente
    >Para este proyecto en particular:<br>
    >sudo docker build -t us-central1-docker.pkg.dev/tnpo-462615/ml-models/inference-ml:latest .

3. Crear permisos necesarios de gcloud para la ejecucion de terraform, seguir los comandos gcloud del archivo [permisosTerraform.txt](permisosTerraform.txt), aqui tambien se deben reemplazar los datos del id de proyecto asociado.
    * Creara el usuario que utilizaremos para ejecutar el terraform
    * Tambien habilitara la api de "identidad y control de acceso" de google y la api de "cloud run admin"

4. Crear infrastructura con Terraform. 
    * esto creara el bucket contenedor del modelo, creare un usuario ejecutor de la maquina virtual y levantara el servicio de gcloud run para el contenedor asociado
    * considerar modificar el nombre del proyecto en el archivo [terraform.tfvars](infra/terraform.tfvars)
    * tambien considerar cambiar los repositorios, archivo de modelo y region en el archivo [variables.tf](infra/variables.tf) o modificarlas al implementarlo.
    
    Comandos para ejecutar:
    > terraform init <br>
    > terraform plan -out=tfplan <br>
    > terraform apply tfplan <br>

    * este paso generara la infrastructura y el primer deploy del proyecto en la nube, donde el output del comando anterior sera el URL de acceso.

5. Finalmente crear los permisos necesarios para el despliege continuo desde Github Actions, para esto seguir los comandos del archivo [permisosGithub.txt](permisosGithub.txt)
    *  Para que las pruebas de integracion funcionen en github, es necesario incluir un modelo .pt basico para que este pueda ser utilizado.
    * se deben agregar las claves secretas en Github Actions de GCP_SA_KEY la que contiene el json de credenciales obtenido y GCP_PROJECT_ID el que contiene el id del proyecto creado de google.

# Pasos para desarrollo

Para facilitar el desarrollo y pruebas, cree el archivo "makefile" que contiene los comandos asociados

## Establecer ambiente

para iniciar el ambiente de desarrollo se debe ejecutar el comando

> make venv

## Instalar requerimientos

para instalar los requerimientos se debe correr el comando

> make install

o en su defecto instalar directamente los archivos de requirements.txt con el comando pip

> pip install -r requirements.txt
> pip install -r requirements_dev.txt

## iniciar localmente

Para iniciar el codigo localmente, se debe correr el comando

> make run

Esto iniciara el servidor en base a uvicorn con puerto por defecto en 8080

## Pruebas
Para probar el codigo se realizaron 2 funciones principales de test, una para el modelo y otra para los endpoints de la apis, estos se encuentran en la carpeta [tests](tests)
* para prueba de modelo en local
    > make model-test
* para prueba de api en local
    > make api-test 


# Versionamiento de modelo
Si bien no fue implementada una herramienta para el versionamiento de modelo y experimentos del mismo, este puede ser habilitado a traves de la misma infrastructura actual, solo actualizando el archivo .pt asociado al bucket y actualizando el modelo en produccion con el metodo de "reload" en la api, o en su defecto actualizando la variable de entorno "MODEL_GCS" la cual es la ruta al archivo en el bucket.

