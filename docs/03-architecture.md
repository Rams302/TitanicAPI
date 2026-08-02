# 03 - Arquitectura de TitanicAPI

## 1. Descripción general

TitanicAPI es una solución de Machine Learning diseñada para transformar un modelo predictivo desarrollado mediante AutoML en un servicio de inferencia desplegable, observable y trazable.

La arquitectura integra las siguientes capacidades:

- Preparación y entrenamiento del modelo.
- AutoML mediante AutoGluon.
- Persistencia del modelo entrenado.
- Exposición del modelo mediante una API REST.
- Contenerización mediante Docker.
- Monitoreo de métricas operativas.
- Registro de logs y trazas de ejecución.
- Generación de alertas.
- Dashboard de observabilidad.
- Trazabilidad de experimentos y modelos mediante MLflow.
- Estrategias propuestas para detección de Data Drift.
- Gestión operacional mediante runbooks.
- Consideraciones de AI Governance y FinOps.

La solución se plantea como una arquitectura de referencia para demostrar el ciclo de vida de un modelo de Machine Learning desde su entrenamiento hasta su operación.

---

## 2. Objetivo de la arquitectura

El objetivo principal es separar las diferentes responsabilidades del ciclo de vida del modelo para facilitar:

1. Desarrollo.
2. Entrenamiento.
3. Evaluación.
4. Registro.
5. Despliegue.
6. Inferencia.
7. Monitoreo.
8. Detección de incidentes.
9. Respuesta operacional.
10. Evolución y reentrenamiento del modelo.

La arquitectura busca que el modelo no sea considerado únicamente como un archivo ejecutable, sino como un componente de un sistema operacional de Machine Learning.

---

## 3. Vista general de la arquitectura

La arquitectura conceptual puede representarse de la siguiente manera:

```text
                         ┌───────────────────────┐
                         │     Data Scientist    │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │     Titanic Dataset   │
                         │       train.csv       │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │    TitanicAutoML.py   │
                         │    / TitanicAutoML    │
                         │       .ipynb           │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │       AutoGluon       │
                         │         AutoML        │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │ Evaluación y selección│
                         │    del mejor modelo   │
                         └───────────┬───────────┘
                                     │
                          ┌──────────┴──────────┐
                          │                     │
                          ▼                     ▼
                 ┌─────────────────┐   ┌─────────────────┐
                 │   TitanicModel  │   │     MLflow      │
                 │ Modelo entrenado│   │ Experimentos y  │
                 │                 │   │ trazabilidad    │
                 └────────┬────────┘   └─────────────────┘
                          │
                          ▼
                 ┌─────────────────────┐
                 │       FastAPI       │
                 │    app.py           │
                 │                     │
                 │      /predict       │
                 │      /health        │
                 │      /info          │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │       Docker        │
                 │   Titanic API       │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │    REST API Client  │
                 │ Swagger / Aplicación│
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │  ModelMonitor       │
                 │  monitor.py         │
                 └──────────┬──────────┘
                            │
             ┌──────────────┼──────────────┐
             │              │              │
             ▼              ▼              ▼
       ┌───────────┐  ┌────────────┐ ┌──────────────┐
       │   Logs    │  │  Métricas  │ │   Alertas    │
       │ predictions│ │  históricas│ │  inteligentes│
       │   .log    │  │    .json   │ │              │
       └───────────┘  └─────┬──────┘ └──────────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Streamlit + Plotly  │
                 │     Dashboard       │
                 └─────────────────────┘
