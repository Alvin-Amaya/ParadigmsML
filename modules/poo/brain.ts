import { type ActivationFunction } from './activations.ts';
import { type LossFunction } from './loss.ts';
import { Vector } from './vector.ts';

export class Neuron {
    private weights: number[];
    private bias: number;
    private activation: ActivationFunction;
    private z: number = 0;

    constructor(numInputs: number, activation: ActivationFunction) {
        this.weights = Array.from({ length: numInputs }, () => (Math.random() - 0.5));
        this.bias = Math.random() - 0.5;
        this.activation = activation;
    }

    public calculate(inputs: number[]): number {
        const sum = inputs.reduce((acc, val, i) => acc + val * this.weights[i], this.bias);
        this.z = sum;
        return this.activation.apply(sum);
    }

    public updateWeight(error: number, prevActivations: number[], learningRate: number): void {
        this.weights = this.weights.map((weight, i) => weight - learningRate * error * prevActivations[i]);
        this.bias -= learningRate * error;
    }

    public getdZ(): number {
        return this.activation.derivate(this.z);
    }

    public weightError(error: number): number[] {
        return this.weights.map(weight => error * weight);
    }
}

export class Layer {
    private neurons: Neuron[];

    constructor(numNeurons: number, inputsPerNeuron: number, activation: ActivationFunction) {
        this.neurons = Array.from({ length: numNeurons }, () => new Neuron(inputsPerNeuron, activation));
    }

    public forward(inputs: number[]): number[] {
        return this.neurons.map(neuron => neuron.calculate(inputs));
    }

    public updateWeights(errors: number[], prevActivations: number[], learningRate: number): void {
        this.neurons.forEach((neuron, i) => {
            neuron.updateWeight(errors[i], prevActivations, learningRate);
        });
    }

    public getdZValues(): number[] {
        return this.neurons.map(neuron => neuron.getdZ());
    }

    public errorByWeights(error: number[]): number[] {
        const matrixErrors = this.neurons.map((neuron, i) => neuron.weightError(error[i])); // [[e11, e12, ...], [e21, e22, ...], ...]
        return matrixErrors.reduce((acc, val) => acc.map((sum, j) => sum + val[j]), Array(matrixErrors[0].length).fill(0)); // [e1, e2, ...] sumando por columnas para obtener el error total para cada peso de la capa anterior
    }
}

export class NeuralNetwork {
    private layers: Layer[] = [];
    
    public addLayer(layer: Layer): void {
        this.layers.push(layer);
    }

    public predict(inputs: number[]): number[] {
        return this.layers.reduce((acc, layer) => layer.forward(acc), inputs);
    }

    public train(trainingData: { inputs: number[]; outputs: number[] }[], learningRate: number, epochs: number, lossFunction: LossFunction): void {
        for (let epoch = 0; epoch < epochs; epoch++) {

            for (const data of trainingData) {

                let predicted = data.inputs;
                const activations: number[][] = [predicted]; // Guardamos las activaciones de cada capa para usar en el backpropagation

                for (let i = 0; i < this.layers.length; i++) {
                    predicted = this.layers[i].forward(predicted);
                    activations.push(predicted);
                }

                let error: number[] = [];                
                for (let j = this.layers.length - 1; j >= 0; j--) { // Iteramos hacia atrás desde la última capa hasta la primera
                    const layer = this.layers[j];
                    if (j === this.layers.length - 1) {
                        const lossDerivatives: number[] = lossFunction.derivative(predicted, data.outputs);
                        error = Vector.hadamardProduct(lossDerivatives, layer.getdZValues());
                    } else {
                        const nextLayer = this.layers[j + 1];
                        error = Vector.hadamardProduct(nextLayer.errorByWeights(error), layer.getdZValues());
                    }
                    const previousActivations = activations[j];
                    layer.updateWeights(error, previousActivations, learningRate);
                }
            }
        }
    }

    public saveModel(): string {
        const model = {
            layers: this.layers.map(layer => ({
                neurons: layer['neurons'].map(neuron => ({
                    weights: neuron['weights'],
                    bias: neuron['bias']
                }))
            }))
        };
        return JSON.stringify(model);
    }

    public loadModel(modelString: string, activation: ActivationFunction): void {
        const model = JSON.parse(modelString);
        this.layers = model.layers.map((layerModel: any) => {
            const layer = new Layer(0, 0, activation);
            layer['neurons'] = layerModel.neurons.map((neuronModel: any) => {
                const neuron = new Neuron(0, activation);
                neuron['weights'] = neuronModel.weights;
                neuron['bias'] = neuronModel.bias;
                return neuron;
            });
            return layer;
        });
    }
}