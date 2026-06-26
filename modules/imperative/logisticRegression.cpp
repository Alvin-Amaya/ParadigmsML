#include <iostream>
#include <string>
#include <vector>
#include <cmath>
#include <numeric>
#include <fstream>
#include <algorithm>
#include <limits>
#include <sstream>

using namespace std;   

vector<float> weights;
float bias = 0.0f;
float learningRate = 0.1f;

vector<vector<float>> trainingData;
vector<float> labels;

vector<float> minValues;
vector<float> maxValues;

float sigmoid(float z) {
    return 1.0f / (1.0f + exp(-z));
}

float predict(const vector<float>& features) {
    vector<float> normalized = features;
    for (size_t i = 0; i < features.size(); ++i) {
        if (i < minValues.size() && i < maxValues.size()) {
            if (maxValues[i] > minValues[i]) {
                normalized[i] = (features[i] - minValues[i]) / 
                               (maxValues[i] - minValues[i]);
            }
        }
    }
    float linearCombination = inner_product(normalized.begin(), normalized.end(), 
                                           weights.begin(), 0.0f) + bias;
    return sigmoid(linearCombination);
}

void printWeights(const vector<float>& weights){
    for (size_t i = 0; i < weights.size(); i++) {
        cout << weights[i] << " ";
    }
    cout << endl;
}

void train(int maxEpochs = 1000) {
    for (int epoch = 0; epoch < maxEpochs; epoch++) {
        float totalLoss = 0.0f;
        for (size_t i = 0; i < trainingData.size(); i++) {    
            float predicted = predict(trainingData[i]);
            float error = labels[i] - predicted;
            totalLoss += abs(error);

            for (size_t j = 0; j < weights.size(); ++j) {
                weights[j] += learningRate * error * trainingData[i][j];
            }
            bias += learningRate * error;
        }

        if (epoch % 100 == 0) {
            cout << "Epoch: " << epoch << ", Weights: ";
            printWeights(weights);
            cout << "Total Loss: " << totalLoss << endl;
        }

        if (totalLoss < 0.01f) {
            cout << "Converged at epoch " << epoch << endl;
            break;
        }
    }
}

void evaluateModel(const vector<vector<float>>& data, const vector<float>& labels) {
    if (data.empty() || data.size() != labels.size()) {
        cout << "No data available for evaluation." << endl;
        return;
    }

    size_t correct = 0;
    size_t tp = 0, tn = 0, fp = 0, fn = 0;

    for (size_t i = 0; i < data.size(); ++i) {
        float prediction = predict(data[i]);
        int predLabel = prediction >= 0.5f ? 1 : 0;
        int trueLabel = static_cast<int>(labels[i]);

        if (predLabel == trueLabel) {
            correct++;
            if (trueLabel == 1) tp++; else tn++;
        } else {
            if (predLabel == 1) fp++; else fn++;
        }
    }

    cout << "Evaluation results:" << endl;
    cout << "  Samples: " << data.size() << endl;
    cout << "  Accuracy: " << (static_cast<float>(correct) / data.size()) << endl;
    cout << "  TP: " << tp << " FP: " << fp << " TN: " << tn << " FN: " << fn << endl;
}

void normailzeTrainingData() {
    if (trainingData.empty()) return;

    size_t featureCount = trainingData[0].size();
    minValues.resize(featureCount, numeric_limits<float>::max());
    maxValues.resize(featureCount, numeric_limits<float>::lowest());

    for (const auto& data : trainingData) {
        for (size_t i = 0; i < featureCount; ++i) {
            minValues[i] = min(minValues[i], data[i]);
            maxValues[i] = max(maxValues[i], data[i]);
        }
    }

    for (auto& data : trainingData) {
        for (size_t i = 0; i < featureCount; ++i) {
            if (maxValues[i] > minValues[i]) {
                data[i] = (data[i] - minValues[i]) / (maxValues[i] - minValues[i]);
            } else {
                data[i] = 0.0f;
            }
        }
    }
}

void dataLoader(const string& filename) {
    ifstream inFile(filename);
    if (inFile.is_open()) {
        trainingData.clear();
        labels.clear();
        string line;

        if (getline(inFile, line)) {
            size_t featureCount = count(line.begin(), line.end(), ',');
            weights.resize(featureCount);
            weights = vector<float>(featureCount, 0.5f);
        }

        while (getline(inFile, line)) {
            vector<float> features;
            float label;
            size_t pos = 0;
            while ((pos = line.find(',')) != string::npos) {
                features.push_back(stof(line.substr(0, pos)));
                line.erase(0, pos + 1);
            }
            label = stof(line);
            trainingData.push_back(features);
            labels.push_back(label);
        }
        inFile.close();
        normailzeTrainingData();
    } else {
        cerr << "Unable to open file for loading data." << endl;
    }
}

void saveModel(const string& filename) {
    ofstream outFile(filename);
    if (outFile.is_open()) {
        for (const auto& weight : weights) {
            outFile << weight << " ";
        }
        outFile << endl;
        outFile << bias << endl;

        for (const auto& minVal : minValues) outFile << minVal << " ";
        outFile << endl;
        for (const auto& maxVal : maxValues) outFile << maxVal << " ";
        outFile << endl;

        outFile.close();
    } else {
        cerr << "Unable to open file for saving model." << endl;
    }
}

void loadModel(const string& filename) {
    ifstream inFile(filename);
    if (inFile.is_open()) {
        weights.clear();
        string line;
        
        if (getline(inFile, line)) {
            stringstream ss(line);
            float weight;
            while (ss >> weight) {
                weights.push_back(weight);
            }
        }
        
        inFile >> bias;

        size_t numFeatures = weights.size();
        minValues.resize(numFeatures);
        maxValues.resize(numFeatures);
        for (size_t i = 0; i < numFeatures; ++i) inFile >> minValues[i];
        for (size_t i = 0; i < numFeatures; ++i) inFile >> maxValues[i];

        inFile.close();
    } else {
        cerr << "Unable to open file for loading model." << endl;
    }
}


// int main() {
//     const string modelFilename = "logistic_model.txt";
//     const string dataPath = "./../../data/heart_disease.csv";
//     loadModel(modelFilename);
//     // dataLoader(dataPath);
//     // cout << "Loaded " << trainingData.size() << " samples with " << weights.size() << " features from " << dataPath << "." << endl;

//     // ifstream modelFile(modelFilename);
//     // if (modelFile.good()) {
//     //     modelFile.close();
//     //     loadModel(modelFilename);
//     //     cout << "Loaded existing model from " << modelFilename << "." << endl;
//     //     evaluateModel(trainingData, labels);
//     // } else {
//     //     cout << "No trained model found. Training will start from initial weights." << endl;
//     // }

//     // cout << "Starting training..." << endl;
//     // train(20000);
//     // cout << "Training finished." << endl;

//     // evaluateModel(trainingData, labels);
//     // saveModel(modelFilename);
//     // cout << "Model saved to " << modelFilename << "." << endl;

//     size_t vectorSize = weights.size();

//     while (true) {
//         vector<float> input(vectorSize, 0.0f);

//         cout << "Enter a vector" << endl;
//         for (int i = 0; i < vectorSize; i++) {
//             cin >> input[i];

//             if (minValues.size() == vectorSize && maxValues.size() == vectorSize) {
//                 float range = maxValues[i] - minValues[i];
//                 if (range > 0.0f) {
//                     input[i] = (input[i] - minValues[i]) / range;
//                 } else {
//                     input[i] = 0.0f;
//                 }
//             }
//         }
        
//         float p = predict(input);
//         cout << "Probability (Sigmoide): " << p << endl;
//         cout << "Classification (Threshold 0.5): " << (p >= 0.5f ? 1 : 0) << endl;

//         char opt = 1;
//         cout << "Enter 0 to exit. Press enter to continue" << endl;
//         cin >> opt;
//         if (opt == '0') break;
//     }
    
// }