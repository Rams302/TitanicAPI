# TitanicAPI — Project Overview

## 1. Descripción general

**TitanicAPI** es un proyecto de Machine Learning diseñado como un caso de estudio
de arquitectura **MLOps, Observabilidad y AI Governance**.

El proyecto utiliza el conjunto de datos Titanic para desarrollar un modelo capaz
de predecir la supervivencia de un pasajero a partir de sus características.

La solución comienza con el desarrollo y entrenamiento de un modelo mediante
**AutoML con AutoGluon** y evoluciona hacia una arquitectura orientada a operación,
incorporando una API REST, contenerización, monitoreo, observabilidad, registro de
experimentos, alertas y mecanismos propuestos para gobierno y mantenimiento del
modelo.

El propósito principal del proyecto no es únicamente obtener una predicción,
sino demostrar cómo un modelo de Machine Learning puede transformarse en un
servicio que pueda ser desplegado, monitoreado, diagnosticado y evolucionado.

---

# 2. Problema abordado

En muchos proyectos de Machine Learning existe una diferencia importante entre
desarrollar un modelo que funciona correctamente durante la experimentación y
operar ese modelo de manera confiable.

Un modelo puede presentar un buen desempeño durante el entrenamiento y,
posteriormente, experimentar problemas como:

- Datos de entrada inválidos.
- Cambios en la distribución de los datos.
- Incremento de la latencia.
- Errores durante la inferencia.
- Degradación del desempeño.
- Falta de trazabilidad.
- Dificultad para identificar incidentes.
- Falta de control sobre las versiones del modelo.
- Ausencia de mecanismos de respuesta ante incidentes.

TitanicAPI aborda este problema utilizando el Titanic Dataset como caso de
estudio para implementar un flujo completo de Machine Learning y MLOps.

---

# 3. Objetivo del proyecto

El objetivo general es diseñar e implementar una solución de Machine Learning
que permita:

1. Entrenar automáticamente un modelo predictivo.
2. Seleccionar el modelo con mejor desempeño.
3. Exponer el modelo mediante una API REST.
4. Contenerizar la aplicación utilizando Docker.
5. Registrar información relacionada con las predicciones.
6. Monitorear el comportamiento operacional del modelo.
7. Generar alertas ante condiciones anormales.
8. Visualizar métricas mediante un dashboard.
9. Incorporar trazabilidad mediante MLflow.
10. Establecer estrategias para detectar Data Drift.
11. Definir procedimientos de respuesta a incidentes.
12. Incorporar principios de AI Governance.
13. Proponer estrategias de optimización de costos mediante FinOps.

---

# 4. Pregunta estratégica

La pregunta central que guía el proyecto es:

> **¿Cómo convertir un modelo de Machine Learning experimental en un servicio
> operacionalizado, observable, trazable y gobernado?**

TitanicAPI utiliza un problema de clasificación conocido para demostrar que el
valor de una solución de IA no depende únicamente de la calidad del modelo,
sino también de la capacidad de operarlo y mantenerlo durante su ciclo de vida.

---

# 5. Solución propuesta

La solución implementa un flujo de Machine Learning de extremo a extremo:

```text
Titanic Dataset
       |
       v
Data Preparation
       |
       v
AutoGluon AutoML
       |
       v
Model Evaluation
       |
       v
MLflow / Model Tracking
       |
       v
Model Artifact
       |
       v
FastAPI
       |
       v
Docker
       |
       v
Model Inference
       |
       +--------------------+
       |                    |
       v                    v
   Monitoring            Logging
       |                    |
       +---------+----------+
                 |
                 v
             Dashboard
                 |
                 v
              Alerts
                 |
                 v
        Incident Response
                 |
                 v
       Retraining / Rollback
