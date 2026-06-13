export interface ActivationFunction {
    apply(x: number): number;
    derivate(x: number): number;
}

export class Sigmoid implements ActivationFunction {
    apply(x: number): number { return 1 / (1 + Math.exp(-x)); }
    derivate(x: number): number { const sig = this.apply(x); return sig * (1 - sig); }
}

export class ReLu implements ActivationFunction {
    apply(x: number): number { return Math.max(0, x); }
    derivate(x: number): number { return x > 0 ? 1 : 0; }
}

export class Tanh implements ActivationFunction {
    apply(x: number): number { return Math.tanh(x); }
    derivate(x: number): number { return 1 - Math.pow(this.apply(x), 2); }
}