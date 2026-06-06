# Proyecto Paradigmas
Implementación de diferentes algoritmos de aprendizaje automático mediante paradigmas de programación, orquestados centralmente para diagnóstico en Ciencias Médicas.

## 1. Arquitectura del Sistema
El sistema sigue un modelo de **Micro-servicios de Computación**

- **Orquestador [Python/FastAPI]:** Único punto de entrada. Expone una API REST para la UI y actúa como cliente gRPC para los módulos.

- **Módulos de Paradigma:** Cada paradigma es un ejecutable independiente que implementa un algoritmo de ML específico bajo una interfaz de red común.

- **Protocolo de Comunicación** gRPC para la comunicación eficiente entre distintos lenguajes de programación.

## 2. Componentes, Algoritmos y Stack

| Paradigma | Algoritmo | Stack |
|-----------|-----------|-------|
| Imperativo| Regresión Logística | C++ |
| Estructurado | KNN | C |
| POO | Perceptrón Multicapa | Java |
| Funcional | Árbol de decisión | Haskell |
| Lógico | Naive Bayes | Prolog |

### 2.1. Regresion Logistica
La regresión logística es un tipo de análisis de clasificación utilizado para predecir el resultado de una variable categórica en función de las variables independientes o predictoras. Es útil para modelar la probabilidad de un evento ocurriendo en función de otros factores.

$$ P(y=1) = \frac{1}{1+e^{-z}} $$

Donde

$$ z=\sum{(w_i\cdot x_i)} + b $$

Aqui $x_i$ representa una característica y $w_i$ un peso. Nuestro objetivo es encontrar los pesos que mejor se ajusten al resultado deseado.

Para el entrenamiento usamos
$$ w_i' = w_i + \alpha(\delta-y)x_i $$
El nuevo valor de $w_i$ es el valor anterior mas la diferencia de la salida desada $\delta$ y el valor obtenido $y$ (el error) multiplicado al valor de la característica $x_i$.