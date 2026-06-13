export class Vector {
    static add(v1: number[], v2: number[]): number[] {
        return v1.map((val, i) => val + v2[i]);
    }

    static subtract(v1: number[], v2: number[]): number[] {
        return v1.map((val, i) => val - v2[i]);
    }

    static applyFunction(v: number[], func: (x: number) => number): number[] {
        return v.map(func);
    }

    static hadamardProduct(v1: number[], v2: number[]): number[] {
        return v1.map((val, i) => val * v2[i]);
    }
}