import * as grpc from '@grpc/grpc-js';
import * as protoLoader from '@grpc/proto-loader';
import * as fs from 'fs';
import { Sigmoid } from "./activations.ts";
import { NeuralNetwork } from "./brain.ts";

const packageDefinition = protoLoader.loadSync('./proto/ml_contract.proto', {});
const protoDescriptor = grpc.loadPackageDefinition(packageDefinition) as any;
const mlContract = protoDescriptor.ml_paradigm;

const nn = new NeuralNetwork();
const modelString = fs.readFileSync('./modules/poo/model.json', 'utf-8');
nn.loadModel(modelString, new Sigmoid());

function predict(call: any, callback: any) {
    const features: number[] = call.request.data.features;
    const result = nn.predict(features);
    callback(null, {
        probability: result,
        confidence: 0.9,
        status: "SUCCESS"
    });
}

const server = new grpc.Server();
server.addService(mlContract.MLPredictor.service, { predict });
server.bindAsync('0.0.0.0:50053', 
    grpc.ServerCredentials.createInsecure(), () => {
        console.log('Server running in port 50053');
});