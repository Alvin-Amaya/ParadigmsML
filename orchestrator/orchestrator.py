from fastapi import FastAPI
import grpc
# from proto import ml_contract_pb2, ml_contract_pb2_grpc
import ml_contract_pb2
import ml_contract_pb2_grpc
import time
import os

app = FastAPI()

MODULE_PORTS = {
    "imperative": "localhost:50051",
    "functional": "localhost:50052",
    "object-oriented": "localhost:50053"
}

NORMALIZATION_PARAMS = {}

def load_normalization_params():
    """Load min/max normalization parameters from model files"""
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    imperative_model_path = os.path.join(base_path, "..", "modules", "imperative", "logistic_model.txt")
    if os.path.exists(imperative_model_path):
        with open(imperative_model_path, 'r') as f:
            lines = f.readlines()
            if len(lines) >= 3:
                min_values = list(map(float, lines[2].split()))
                max_values = list(map(float, lines[3].split()))
                NORMALIZATION_PARAMS["imperative"] = (min_values, max_values)
    
    return NORMALIZATION_PARAMS

def normalize(data, paradigm=None):
    """Normalize data using per-feature min/max normalization"""
    if paradigm and paradigm in NORMALIZATION_PARAMS:
        min_values, max_values = NORMALIZATION_PARAMS[paradigm]
        normalized = []
        for i, x in enumerate(data):
            if i < len(min_values) and i < len(max_values):
                min_val = min_values[i]
                max_val = max_values[i]
                if max_val - min_val > 0:
                    normalized.append((x - min_val) / (max_val - min_val))
                else:
                    normalized.append(0.0)
            else:
                normalized.append(x)
        return normalized
    else:
        min_val = min(data)
        max_val = max(data)
        if max_val - min_val == 0:
            return [0.0 for _ in data]
        return [(x - min_val) / (max_val - min_val) for x in data]

@app.get("/")
async def root():
    return {"message": "Bienvenido al Orquestador de Paradigmas de Programación para IA"}

@app.post("/predict/{paradigm}")
async def predict(paradigm: str, data: list[float]):
    data = normalize(data, paradigm)
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
    
    load_normalization_params()

    uvicorn.run(app, host="0.0.0.0", port=8000)