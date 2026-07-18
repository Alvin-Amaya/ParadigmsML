from fastapi import FastAPI
from pydantic import BaseModel
import grpc
import ml_contract_pb2
import ml_contract_pb2_grpc
import time

app = FastAPI()

MODULE_PORTS = {
    "imperative": "localhost:50051",
    "structured": "localhost:50052",
    "poo": "localhost:50053",
    "functional": "localhost:50054",
    "logical": "localhost:50055"
}

# Creamos un modelo para que FastAPI entienda el JSON {"features": [...]}
class PredictionPayload(BaseModel):
    features: list[float]

@app.get("/")
async def root():
    return {"message": "Bienvenido al Orquestador de Paradigmas de Programación para IA"}

# Cambiamos la ruta a una fija '/predict' para que coincida con tu Streamlit
@app.post("/predict")
async def predict(payload: PredictionPayload):
    # Por defecto usamos el módulo POO (según vimos en el spinner de tu Streamlit)
    paradigm = PredictionPayload.algorithm
    
    # Extraemos la lista de floats desde el objeto recibido
    data = payload.features
    
    if paradigm not in MODULE_PORTS:
        return {"error": "Paradigma no Soportado"}
    
    print(f"Execute in {paradigm} paradigm with data: {data}")
    channel = grpc.insecure_channel(MODULE_PORTS[paradigm])
    stub = ml_contract_pb2_grpc.MLPredictorStub(channel)

    request = ml_contract_pb2.PredictionRequest(
        model_type=paradigm,
        data=ml_contract_pb2.DataPoint(id=0, features=data))

    start = time.time()
    response = stub.Predict(request)
    latency = (time.time() - start) * 1000

    # Retornamos el campo 'prediction' que tu frontend espera en resultado.get("prediction")
    return {
        "paradigm": paradigm,
        "prediction": response.probability,  # Si tu gRPC devuelve un string ("maligno"/"benigno") o usa response.prediction, cámbialo aquí
        "latency_ms": latency
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)