#include <iostream>
#include <string>
#include <vector>
#include <cmath>
#include <numeric>

using namespace std;

vector<float> weights = {0, 0, 0, 0, 0}; 
float bias = 0.5;
float learningRate = 0.5;

vector<vector<float>> trainingData = {
    {0, 0, 0, 0, 0},
    {1, 1, 1, 1, 1},
    {0, 1, 0, 1, 0},
    {1, 0, 1, 0, 1}

};
vector<float> labels = {0, 1, 0, 1};

float sigmoid(float z) {
    return 1.0f / (1.0f + exp(-z));
}

float predict(const vector<float>& features) {
    float linearCombination = inner_product(features.begin(), features.end(), weights.begin(), 0.0f) + bias;
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
        cout << "Epoch: " << epoch << endl;
        float totalLoss = 0.0f;
        for (size_t i = 0; i < trainingData.size(); i++) {    
            printWeights(weights);
            float predicted = predict(trainingData[i]);
            float error = labels[i] - predicted;
            totalLoss += abs(error);

            for (size_t j = 0; j < weights.size(); ++j) {
                weights[j] += learningRate * error * trainingData[i][j];
            }
            bias += learningRate * error;
        }

        if (totalLoss < 0.01f) {
            cout << "Converged at epoch " << epoch << endl;
            break;
        }
    }
}


int main() {
    train(5000);
    cout << "trained" << endl;

    cout << "\nfinal weights: ";
    printWeights(weights);
    cout << "final bias: " << bias << endl;

    while (true) {
        int vectorSize = 5;
        vector<float> input(vectorSize, 0.0f);

        cout << "Enter a vector" << endl;
        for (int i = 0; i < vectorSize; i++) {
            cin >> input[i];
        }
        
        float p = predict(input);
        cout << "Probability (Sigmoide): " << p << endl;
        cout << "Classification (Threshold 0.5): " << (p >= 0.5f ? 1 : 0) << endl;

        char opt = 1;
        cout << "Enter 0 to exit. Press enter to continue" << endl;
        cin >> opt;
        if (opt == '0') break;
    }
    
}