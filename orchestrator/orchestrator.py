from fastapi import FastAPI
import grpc
import ml_contract_pb2
import ml_contract_pb2_grpc
import time

app = FastAPI()

MODULE_PORTS = {}

@app.post("predict/{paradigm}")
async def predict(paradigm: str, data: list[float]):
    if paradigm not in MODULE_PORTS:
        return {"error": "Paradigma no Soportado"}
    
    channel = grpc.insecure_channel(MODULE_PORTS[paradigm])
    stub = ml_contract_pb2_grpc.MLPredictorStub(channel)

    request = ml_contract_pb2.PredictRequest(data=ml_contract_pb2.DataPoint(patient_id=0, features=data))

    start = time.time()
    response = stub.Predict(request)
    latency = (time.time() - start) * 1000

    return {
        "paradigm": paradigm,
        "probability": response.probability,
        "latency_ms": latency
    }