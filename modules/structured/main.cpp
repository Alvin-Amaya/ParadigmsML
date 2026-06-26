#include <iostream>
#include <memory>
#include <grpcpp/grpcpp.h>
#include <grpcpp/server_builder.h>
#include <grpcpp/server.h>
#include <string>
#include "../../proto/ml_contract.pb.h"
#include "../../proto/ml_contract.grpc.pb.h"
#include "knn.h"

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
        float probability = 0.0f;
        try {
            probability = predictKnn(features.data(), 5);
        } catch (const exception& e) {
            cerr << "Error occurred: " << e.what() << endl;
            return Status(grpc::StatusCode::INTERNAL, "Internal error");
        }
        response->set_probability(probability == 1 ? 1.0f : 0.0f);
        response->set_confidence(0.95);
        response->set_status("SUCCESS");

        cout << "Prediction for data point: " << request->data().id() << endl;
        cout << "Probability: " << probability << endl;
        return Status::OK;
    }   
};

void RunServer() {
    string server_address("localhost:50052");
    PredictorImp service;

    ServerBuilder builder;
    builder.AddListeningPort(server_address, grpc::InsecureServerCredentials());
    builder.RegisterService(&service);
    unique_ptr<Server> server(builder.BuildAndStart());
    cout << "Server listening on " << server_address << endl;
    server->Wait();
}

int main(int argc, char** argv) {
    cout << "KNN Model..." << endl;
    loadDataset("./data/diabetes.csv");
    RunServer();
    return 0;
}