#include <iostream>
#include <memory>
#include <grpcpp/grpcpp.h>
#include <grpcpp/server_builder.h>
#include <grpcpp/server.h>
#include <string>
#include <fstream>
#include "../../proto/ml_contract.grpc.pb.h"
#include "logisticRegression.cpp"

using grpc::Server;
using grpc::ServerBuilder;
using grpc::ServerContext;
using grpc::Status;
using ml_paradigm::MLPredictor;
using ml_paradigm::PredictionRequest;
using ml_paradigm::PredictionResponse;

using namespace std;

class PredictorImp final : public MLPredictor::Service {
    Status Predict(ServerContext* context, const PredictionRequest* request, PredictionResponse* response) override {
        vector<float> features(request->data().features().begin(), request->data().features().end());
        
        cout << "\n--- Peticion gRPC Recibida ---" << endl;
        cout << "Features: ";
        for (float f : features) cout << f << " | ";
        cout << endl;

        float probability = 0.0f;
        try {
            probability = predict(features);
        } catch (const exception& e) {
            cerr << "Error occurred: " << e.what() << endl;
            return Status(grpc::StatusCode::INTERNAL, "Internal error");
        }

        response->set_probability(probability);
        response->set_confidence(0.70);
        response->set_status("SUCCESS");

        cout << "Probabilidad devuelta: " << probability << endl;
        return Status::OK;
    }   
};

void RunServer() {
    string server_address("localhost:50051");
    PredictorImp service;

    ServerBuilder builder;
    builder.AddListeningPort(server_address, grpc::InsecureServerCredentials());
    builder.RegisterService(&service);
    unique_ptr<Server> server(builder.BuildAndStart());
    cout << "Server listening on " << server_address << endl;
    server->Wait();
}

int main(int argc, char** argv) {
    cout << "Logistic Regression Model" << endl;

    // Probar las distintas rutas donde puede estar el CSV
    string csvPath = "../heart_disease.csv"; 
    ifstream checkCsv(csvPath);
    
    if (!checkCsv.good()) {
        csvPath = "heart_disease.csv";
        checkCsv.open(csvPath);
    }
    if (!checkCsv.good()) {
        csvPath = "../../data/heart_disease.csv";
        checkCsv.open(csvPath);
    }

    if (!checkCsv.good()) {
        cerr << "ERROR: No se encontro heart_disease.csv en ninguna ruta relativa." << endl;
        return 1;
    }
    checkCsv.close();

    cout << "Cargando dataset desde: " << csvPath << endl;
    dataLoader(csvPath);
    
    cout << "Iniciando entrenamiento del modelo..." << endl;
    train(1000);

    saveModel("../logistic_model.txt");
    cout << "Modelo guardado exitosamente." << endl;

    RunServer();
    return 0;
}