import { Vector } from "./vector.ts";

export interface LossFunction {
    apply(predicted: number[], actual: number[]): number;
    derivative(predicted: number[], actual: number[]): number[];
}

export class MeanSquaredError implements LossFunction {
    apply(predicted: number[], actual: number[]): number {
        const squaredErrors = Vector.applyFunction(Vector.subtract(predicted, actual), x => 0.5 * Math.pow(x, 2));
        return squaredErrors.reduce((acc, val) => acc + val, 0);
    }
    derivative(predicted: number[], actual: number[]): number[] {
        return Vector.subtract(predicted, actual);
    }
}

export class CrossEntropyLoss implements LossFunction {
    apply(predicted: number[], actual: number[]): number {
        return predicted.reduce((acc, yHat, i) => {
            const y = actual[i];
            
            const epsilon = 1e-15;
            const yHatClamped = Math.max(epsilon, Math.min(1 - epsilon, yHat));
            
            const perdidaElemento = - (y * Math.log(yHatClamped) + (1 - y) * Math.log(1 - yHatClamped));
            return acc + perdidaElemento;
        }, 0);
    }
    derivative(predicted: number[], actual: number[]): number[] {
        return predicted.map((yHat, i) => {
            const y = actual[i];
            const epsilon = 1e-15;
            const yHatClamped = Math.max(epsilon, Math.min(1 - epsilon, yHat));
            return (yHatClamped - y) / (yHatClamped * (1 - yHatClamped));
        });
    }
}