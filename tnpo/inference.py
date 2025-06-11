from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import os
from tnpo.modelo import modelTnpo

# Pydantic models for request/response
class InferenceInput(BaseModel):
    input: List[int]

class InferenceOutput(BaseModel):
    output: List[float]


# instanciacion de modelo
model = modelTnpo(model_name="DoubleItModel")
model.load_model()

# Crear app FastAPI
app = FastAPI(title="DoubleIt Model API")



@app.get("/")
async def home():
    """Ruta de inicio.
    Devuelve un mensaje simple para verificar que la app está corriendo.
    
    Returns:
        dict: Mensaje de estado.
    """
    return {"message": "Modelo TorchScript listo para inferencia."}


@app.post("/infer", response_model=InferenceOutput)
async def infer(data: InferenceInput):
    """Ruta para inferencia del modelo.
    Permite enviar una lista de enteros y recibir el resultado de la inferencia.
    
    Args:
        data: InferenceInput con lista de enteros para procesar
    
    Returns:
        InferenceOutput: Resultado de la inferencia
        
    Raises:
        HTTPException: Si ocurre un error durante la inferencia
    """
    try:
        output_tensor = model.infer(data.input)
        return InferenceOutput(output=output_tensor.tolist())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/reload")
def reload_model():
    """Ruta para recargar el modelo desde GCS."""
    try:
        model.download_from_gcs()
        model.load_model()
        return {"message": "Modelo recargado exitosamente."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
