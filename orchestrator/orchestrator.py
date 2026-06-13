from fastapi import FastAPI
import grpc
import ml_contract_pb2
import ml_contract_pb2_grpc
import time

app = FastAPI()

MODULE_PORTS = {
    "imperative": "localhost:50051",
    "structured": "localhost:50052",
    "object-oriented": "localhost:50053",
    "functional": "localhost:50054",
    "logical": "localhost:50055"
}

@app.get("/")
async def root():
    return {"message": "Bienvenido al Orquestador de Paradigmas de Programación para IA"}

@app.post("/predict/{paradigm}")
async def predict(paradigm: str, data: list[float]):
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

    return {
        "paradigm": paradigm,
        "probability": response.probability,
        "latency_ms": latency
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)