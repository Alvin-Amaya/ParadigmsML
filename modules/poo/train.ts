import * as fs from 'fs';
import * as path from 'path';
import csv from 'csv-parser';
import { Layer, NeuralNetwork } from './brain.ts'
import { Sigmoid } from './activations.ts';
import { MeanSquaredError } from './loss.ts';

interface DataRow {
    inputs: number[];
    outputs: number[];
}

export function dataLoader(csvPath: string): Promise<DataRow[]> {
    return new Promise((resolve, reject) => {
        const dataset: DataRow[] = [];

        fs.createReadStream(path.resolve(csvPath))
            .pipe(csv())
            .on('data', (row) => {
                if (!row.diagnosis) return;

                const target = row.diagnosis.toUpperCase() === 'M' ? [1] : [0];

                const features = [
                    row.radius_mean, row.texture_mean, row.perimeter_mean, row.area_mean, row.smoothness_mean,
                    row.compactness_mean, row.concavity_mean, row.concave_points_mean, row.symmetry_mean, row.fractal_dimension_mean,
                    row.radius_se, row.texture_se, row.perimeter_se, row.area_se, row.smoothness_se,
                    row.compactness_se, row.concavity_se, row.concave_points_se, row.symmetry_se, row.fractal_dimension_se,
                    row.radius_worst, row.texture_worst, row.perimeter_worst, row.area_worst, row.smoothness_worst,
                    row.compactness_worst, row.concavity_worst, row.concave_points_worst, row.symmetry_worst, row.fractal_dimension_worst
                ].map(val => {
                    const num = Number(val);
                    return isNaN(num) ? 0 : num;
                });

                dataset.push({ inputs: features, outputs: target });
            })
            .on('end', () => {
                console.log(`CSV parseado con éxito. Total registros leídos: ${dataset.length}`);
                resolve(dataset);
            })
            .on('error', (error) => {
                reject(error);
            });
    });
}

async function train() {
    try {
        const csvPath = './../../data/breast_cancer_w.csv'; 
        const allData = await dataLoader(csvPath);

        allData.sort(() => Math.random() - 0.5);

        const splitIndex = Math.floor(allData.length * 0.85);
        const rawTrainData = allData.slice(0, splitIndex);
        const testData = allData.slice(splitIndex);

        console.log(`Datos de entrenamiento: ${rawTrainData.length} | Datos de prueba: ${testData.length}`);

        const numFeatures = rawTrainData[0].inputs.length;
        const mins = Array(numFeatures).fill(Infinity);
        const maxs = Array(numFeatures).fill(-Infinity);

        for (const sample of rawTrainData) {
            for (let i = 0; i < numFeatures; i++) {
                if (sample.inputs[i] < mins[i]) mins[i] = sample.inputs[i];
                if (sample.inputs[i] > maxs[i]) maxs[i] = sample.inputs[i];
            }
        }

        const trainData: DataRow[] = rawTrainData.map(sample => ({
            outputs: sample.outputs,
            inputs: sample.inputs.map((val, i) => {
                const range = maxs[i] - mins[i];
                if (range === 0 || isNaN(range)) return 0;
                return (val - mins[i]) / range;
            })
        }));

        const nn = new NeuralNetwork();
        const sigmoid = new Sigmoid();
        nn.setNormalizationParams(mins, maxs);
        nn.addLayer(new Layer(16, 30, sigmoid));
        nn.addLayer(new Layer(1, 16, sigmoid));

        // Entrenamiento
        const learningRate = 0.05;
        const epochs = 10000;
        const lossMetric = new MeanSquaredError();

        console.log("Iniciando el entrenamiento de la red...");
        nn.train(trainData, learningRate, epochs, lossMetric);
        console.log("Entrenamiento completado");

        let correctPredictions = 0;

        testData.forEach(sample => {
            const prediction = nn.predict(sample.inputs)[0];
            const binaryPred = prediction >= 0.5 ? 1 : 0;
            const target = sample.outputs[0];

            if (binaryPred === target) {
                correctPredictions++;
            }
        });

        const accuracy = (correctPredictions / testData.length) * 100;
        console.log("--------------------------------------------------");
        console.log(`Precisión (Accuracy) en datos no vistos: ${accuracy.toFixed(2)}%`);
        console.log("--------------------------------------------------");

        const modelJson = nn.saveModel();
        fs.writeFileSync('./model.json', modelJson, 'utf-8');
        console.log("Modelo exportado correctamente.");
    } catch (error) {
        console.error("Ocurrió un error en el pipeline:", error);
    }
}

train();