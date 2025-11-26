# Sistema de Detección de Fraude Transaccional: Enfoque End-to-End

![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=flat-square&logo=python&logoColor=white)
![XGBoost](https://img.shields.io/badge/Model-XGBoost-EB4223?style=flat-square)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![Status](https://img.shields.io/badge/Status-Completed-success?style=flat-square)

## Descripción Ejecutiva

Este proyecto implementa un sistema integral para la detección de fraudes financieros en tiempo real, diseñado para mitigar riesgos en transacciones de alto volumen. A diferencia de enfoques académicos tradicionales, esta solución prioriza la **interpretabilidad (Explainable AI)** y la minimización de falsos negativos, métrica crítica para evitar pérdidas de capital.

El sistema simula un entorno de auditoría bancaria donde un modelo de Machine Learning analiza patrones comportamentales (no solo demográficos) para alertar sobre posibles vaciados de cuenta (*Account Takeover*) y anomalías transaccionales, exponiendo los resultados a través de una API REST y un Dashboard de control para la toma de decisiones.

## Objetivos Técnicos

1.  **Manejo de Desbalanceo Severo:** Implementación de estrategias de ponderación de clases (`scale_pos_weight`) para detectar fraudes que representan menos del 0.2% del dataset.
2.  **Ingeniería de Características Temporal:** Desarrollo de variables de velocidad y ventanas de tiempo para identificar patrones de comportamiento anómalo.
3.  **Arquitectura Desacoplada:** Separación estricta entre el motor de inferencia (API), la lógica de entrenamiento y la capa de presentación (Dashboard).
4.  **Explicabilidad Normativa:** Integración de valores SHAP para justificar matemáticamente cada alerta de riesgo, cumpliendo con estándares de transparencia algorítmica.

## Arquitectura del Sistema

```mermaid
graph LR
    A[Cliente / Auditor] -->|Input Transacción| B(Frontend: Streamlit)
    B -->|Solicitud JSON| C{API: FastAPI}
    
    subgraph "Motor de Inferencia"
    C -->|Feature Engineering| D[Procesamiento en Tiempo Real]
    D -->|Carga de Artefactos| E[(Modelo XGBoost)]
    E -->|Cálculo de Probabilidad| C
    end
    
    C -->|Respuesta: Score + Alerta| B
    B -->|Matriz de Decisión| A
