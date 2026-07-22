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

# Agregamos 'algorithm' opcional con "poo" por defecto
class PredictionPayload(BaseModel):
    features: list[float]
    algorithm: str = "poo" 

@app.get("/")
async def root():
    return {"message": "Bienvenido al Orquestador de Paradigmas de Programación para IA"}

@app.post("/predict")
async def predict(payload: PredictionPayload):
    # Accedemos directamente al atributo de la INSTANCIA 'payload'
    paradigm = payload.algorithm.lower()
    
    # Extraemos la lista de floats
    data = payload.features
    
    if paradigm not in MODULE_PORTS:
        return {"error": f"Paradigma '{paradigm}' no Soportado"}
    
    print(f"Execute in {paradigm} paradigm with data: {data}")
    
    channel = grpc.insecure_channel(MODULE_PORTS[paradigm])
    stub = ml_contract_pb2_grpc.MLPredictorStub(channel)

    request = ml_contract_pb2.PredictionRequest(
        model_type=paradigm,
        data=ml_contract_pb2.DataPoint(id=0, features=data)
    )

    start = time.time()
    response = stub.Predict(request)
    latency = (time.time() - start) * 1000

    return {
        "paradigm": paradigm,
        "prediction": response.probability,
        "latency_ms": latency
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)