#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "knn.h"

typedef struct {
    float features[NUM_FEATURES];
    int label;
} DataRow;

static DataRow dataset[MAX_ROWS];
static int dataSize = 0;

void loadDataset(const char* filename) {
    FILE* file = fopen(filename, "r");
    if (file == NULL) {
        fprintf(stderr, "Unable to open dataset file: %s\n", filename);
        return;
    }

    char line[512];
    if (fgets(line, sizeof(line), file) == NULL) {
        fclose(file);
        return;
    }

    while (fgets(line, sizeof(line), file) && dataSize < MAX_ROWS) {
        char* token = strtok(line, ",");
        if (token == NULL) {
            continue;
        }

        for (int i = 0; i < NUM_FEATURES; i++) {
            if (token == NULL) {
                break;
            }
            dataset[dataSize].features[i] = (float)atof(token);
            token = strtok(NULL, ",");
        }

        if (token == NULL) {
            continue;
        }
        dataset[dataSize].label = atoi(token);
        dataSize++;
    }

    fclose(file);
    printf("Loaded %d rows from dataset\n", dataSize);
}

static float euclideanDistance(const float *a, const float *b) {
    float sum = 0.0f;
    for (int i = 0; i < NUM_FEATURES; i++) {
        float diff = a[i] - b[i];
        sum += diff * diff;
    }
    return sqrtf(sum);
}

int getDatasetSize(void) {
    return dataSize;
}

int predictKnn(float *input_features, int k) {
    if (dataSize == 0 || k <= 0) {
        return 0;
    }

    static float distances[MAX_ROWS];
    static int indices[MAX_ROWS];
    for (int i = 0; i < dataSize; i++) {
        distances[i] = euclideanDistance(dataset[i].features, input_features);
        indices[i] = i;
    }

    for (int i = 0; i < k; i++) {
        int bestIndex = i;
        for (int j = i + 1; j < dataSize; j++) {
            if (distances[j] < distances[bestIndex]) {
                bestIndex = j;
            }
        }
        if (bestIndex != i) {
            float temp_dist = distances[i];
            distances[i] = distances[bestIndex];
            distances[bestIndex] = temp_dist;
            int temp_idx = indices[i];
            indices[i] = indices[bestIndex];
            indices[bestIndex] = temp_idx;
        }
    }

    int label_count[NUM_CLASSES] = {0};
    for (int i = 0; i < k && i < dataSize; i++) {
        int label = dataset[indices[i]].label;
        if (label >= 0 && label < NUM_CLASSES) {
            label_count[label]++;
        }
    }

    int predicted_label = 0;
    for (int i = 1; i < NUM_CLASSES; i++) {
        if (label_count[i] > label_count[predicted_label]) {
            predicted_label = i;
        }
    }
    return predicted_label;
}

// int main() {
//     loadDataset("../../data/diabetes.csv");
//     int prediction = predictKnn((float[]){1,85,66,29,0,26.6,0.351,31}, 3);
//     printf("Predicted label: %d\n", prediction);
//     return 0;
// }