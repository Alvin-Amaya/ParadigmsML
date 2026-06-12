#ifndef KNN_H
#define KNN_H

#ifdef __cplusplus
extern "C" {
#endif

#define MAX_ROWS 8000
#define NUM_FEATURES 8
#define NUM_CLASSES 2

void loadDataset(const char* filename);
int predictKnn(float *input_features, int k);
int getDatasetSize(void);

#ifdef __cplusplus
}
#endif

#endif // KNN_H
