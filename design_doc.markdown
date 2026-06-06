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

