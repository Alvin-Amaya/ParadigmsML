#include <iostream>
#include <memory>
#include <grpcpp/grpcpp.h>
#include <grpcpp/server_builder.h>
#include <grpcpp/server.h>
#include <string>
// #include "ml_contract.grpc.pb.h"
#include "../../proto/ml_contract.grpc.pb.h"

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
        // Mock prediction logic
        float mock_probability = 0.85;
        response->set_probability(mock_probability);
        response->set_confidence(0.95);
        response->set_status("SUCCESS");

        cout << "Prediccion para el Paciente: " << request->data().id() << endl;
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
    cout << "Servidor escuchando en " << server_address << endl;
    server->Wait();
}

int main(int argc, char** argv) {
    RunServer();
    return 0;
}