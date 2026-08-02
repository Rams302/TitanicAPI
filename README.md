# TitanicAPI
## End-to-End Machine Learning, MLOps & AI Governance Portfolio

![Python](https://img.shields.io/badge/Python-3.12-blue)
![AutoGluon](https://img.shields.io/badge/AutoGluon-AutoML-orange)
![FastAPI](https://img.shields.io/badge/FastAPI-API-green)
![Docker](https://img.shields.io/badge/Docker-Container-blue)
![MLflow](https://img.shields.io/badge/MLflow-ML%20Lifecycle-blue)
![MLOps](https://img.shields.io/badge/MLOps-Monitoring-purple)

---

## 1. Resumen ejecutivo

TitanicAPI es una solución integral de Machine Learning desarrollada como
un caso de estudio de arquitectura MLOps.

El proyecto utiliza el Titanic Dataset para construir un modelo capaz de
predecir la supervivencia de un pasajero y posteriormente operacionalizar
el modelo mediante una API REST.

La solución evoluciona desde el entrenamiento del modelo hasta una
arquitectura orientada a operación, incorporando:

- AutoML
- API REST
- Docker
- MLflow
- Model Monitoring
- Observabilidad
- Logs
- Métricas
- Alertas
- Dashboard operativo
- Data Validation
- Data Drift
- Runbooks
- AI Governance
- FinOps

El objetivo no es únicamente construir un modelo predictivo, sino demostrar
cómo un modelo de Machine Learning puede convertirse en un servicio
operacionalizado, observable y gestionable.

---

# 2. Problema de negocio

Las organizaciones pueden desarrollar modelos de Machine Learning con
buen desempeño durante la etapa experimental, pero esto no garantiza que
el modelo pueda operar correctamente en un entorno productivo.

Entre los principales riesgos se encuentran:

- degradación del desempeño;
- cambios en los datos;
- errores durante la inferencia;
- incremento de la latencia;
- datos de entrada inválidos;
- pérdida de trazabilidad;
- dificultad para identificar incidentes;
- falta de control sobre versiones del modelo;
- incremento no controlado de costos;
- ausencia de mecanismos de gobierno.

TitanicAPI utiliza un problema de clasificación conocido como caso de
estudio para demostrar cómo abordar estos retos mediante prácticas de
Machine Learning Engineering y MLOps.

---

# 3. Solución propuesta

La solución implementa un flujo completo:

Dataset
↓
Preparación de datos
↓
AutoML
↓
Evaluación
↓
Registro del modelo
↓
API REST
↓
Docker
↓
Monitoreo
↓
Dashboard
↓
Alertas
↓
Análisis de incidentes
↓
Data Drift
↓
Reentrenamiento

Este flujo permite pasar de un experimento de Machine Learning a una
solución susceptible de ser operada y evolucionada.

---

# 4. Valor estratégico

El principal valor del proyecto no está únicamente en la predicción.

La solución demuestra la capacidad de integrar Machine Learning con
procesos de operación tecnológica.

### Valor técnico

- Automatización del entrenamiento mediante AutoML.
- Exposición del modelo mediante API REST.
- Contenerización mediante Docker.
- Registro y trazabilidad de experimentos.
- Monitoreo de inferencias.
- Validación de datos.
- Generación de logs.
- Dashboard operativo.
- Alertas basadas en umbrales.
- Preparación para detección de Data Drift.

### Valor operativo

La arquitectura permite detectar problemas como:

- aumento de latencia;
- errores de ejecución;
- datos inválidos;
- degradación del modelo;
- cambios en las características de entrada.

Esto reduce el tiempo necesario para detectar y diagnosticar incidentes.

### Valor estratégico

El proyecto incorpora conceptos de:

- MLOps;
- Observabilidad;
- AI Governance;
- Responsible AI;
- FinOps;
- gestión de riesgos;
- trazabilidad;
- mejora continua.

Por lo tanto, el proyecto demuestra una visión que conecta la tecnología
con la operación y la gestión del negocio.

---

# 5. Arquitectura

La solución puede representarse conceptualmente de la siguiente manera:

```text
                         DATA SCIENTIST
                               |
                               v
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
                            MLflow
                               |
                               v
                       Model Registry
                               |
                               v
                         MLOps Engineer
                               |
                               v
                         Docker Container
                               |
                               v
                          FastAPI API
                               |
                               v
                         /predict
                               |
                 +-------------+-------------+
                 |             |             |
                 v             v             v
               Logs         Metrics       Traces
                 |             |             |
                 +-------------+-------------+
                               |
                               v
                        Monitoring Engine
                               |
                 +-------------+-------------+
                 |                           |
                 v                           v
             Dashboard                   Alerts
                 |                           |
                 +-------------+-------------+
                               |
                               v
                         Incident Response
                               |
                               v
                     Retraining / Rollback
