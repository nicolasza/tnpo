# Imagen base oficial de Python
FROM python:3.12-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos del proyecto
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar resto de archivos
COPY . .

# Exponer el puerto usado por FastAPI
EXPOSE 8080

# Comando para correr la app con uvicorn
CMD ["uvicorn", "tnpo:application", "--host", "0.0.0.0", "--port", "8080"]
