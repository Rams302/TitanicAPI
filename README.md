# TitanicAPI - API de Predicción de Supervivencia del Titanic con AutoML, MLOps y Observabilidad

## Descripción

TitanicAPI es un proyecto de Machine Learning desarrollado con fines académicos para la materia de Gestión de Proyectos de Inteligencia Artificial. El proyecto implementa un modelo predictivo para determinar la probabilidad de supervivencia de los pasajeros del Titanic utilizando técnicas de AutoML con AutoGluon.

La solución incorpora prácticas de MLOps y observabilidad mediante:

- Entrenamiento automático del modelo con AutoGluon.
- Despliegue mediante una API REST desarrollada con FastAPI.
- Contenerización utilizando Docker.
- Monitoreo operacional del modelo y de la API.
- Registro de métricas, logs y trazas.
- Seguimiento del ciclo de vida del modelo mediante MLflow.
- Dashboard de monitoreo en tiempo real desarrollado con Streamlit y Plotly.
- Estrategias propuestas para la detección de Data Drift y respuesta ante incidentes.

---

## Objetivos del proyecto

Los objetivos principales del proyecto son:

- Desarrollar un modelo predictivo utilizando técnicas de AutoML.
- Implementar una API REST para realizar predicciones en tiempo real.
- Aplicar conceptos de MLOps y observabilidad para monitorear el comportamiento del modelo.
- Implementar mecanismos de trazabilidad utilizando MLflow.
- Diseñar dashboards operativos para la toma de decisiones.
- Documentar estrategias de respuesta ante incidentes y mecanismos de mejora continua del modelo.

---

## Tecnologías utilizadas

- Python 3.12
- AutoGluon
- FastAPI
- Uvicorn
- Pandas
- NumPy
- Pydantic
- Docker
- MLflow
- Streamlit
- Plotly
- Swagger UI
- Git
- GitHub

---

## Dataset utilizado

Se utilizó el conjunto de datos Titanic Dataset publicado en Kaggle.

https://www.kaggle.com/competitions/titanic/data

Archivo utilizado durante el entrenamiento:

```text
train.csv
```

---

## Arquitectura del proyecto

```text
TitanicAPI
│
├── app.py
├── TitanicAutoML.py
├── TitanicAutoML.ipynb
├── Dockerfile
├── requirements.txt
├── README.md
├── .gitignore
├── .dockerignore
│
├── TitanicModel/
│
├── monitoring/
│   ├── __init__.py
│   ├── monitor.py
│   ├── current_model_metrics.json
│   ├── training_data.json
│   ├── metrics_history.json
│   └── predictions.log
│
├── dashboard/
│   └── dashboard.py
│
├── mlruns/
│
├── Evidencias/
│
└── datos/
    └── train.csv
```

---

## Componentes principales

### TitanicAutoML.py

Responsable del entrenamiento automático del modelo utilizando AutoGluon.

Sus funciones principales son:

- Cargar el dataset.
- Dividir los datos de entrenamiento y evaluación.
- Entrenar múltiples algoritmos de clasificación.
- Seleccionar automáticamente el mejor modelo.
- Registrar métricas utilizando MLflow.
- Exportar el modelo entrenado.

---

### app.py

Implementa la API REST utilizando FastAPI.

Sus responsabilidades incluyen:

- Cargar el modelo entrenado.
- Procesar solicitudes de predicción.
- Registrar métricas operativas.
- Generar logs del servicio.
- Registrar métricas de inferencia en MLflow.
- Integrarse con el módulo de monitoreo MLOps.

---

### monitor.py

Implementa el motor de monitoreo del proyecto.

Permite:

- Validar los datos de entrada.
- Registrar métricas operativas.
- Generar alertas.
- Mantener históricos de ejecución.
- Detectar comportamientos anómalos.
- Proporcionar información para el dashboard operativo.

---

### Dashboard de monitoreo

El dashboard desarrollado con Streamlit permite visualizar:

- Número total de ejecuciones.
- Latencia promedio.
- Solicitudes exitosas.
- Número de alertas.
- Distribución de solicitudes.
- Histórico de métricas.
- Alertas operativas activas.

---

### MLflow

MLflow permite gestionar el ciclo de vida del modelo mediante:

- Experimentos.
- Runs.
- Métricas.
- Parámetros.
- Artefactos.
- Versionamiento del modelo.

Entre las métricas registradas se encuentran:

- Accuracy.
- Tiempo de entrenamiento.
- Latencia.
- Probabilidad de predicción.
- Modelo seleccionado por AutoGluon.

---

## Instalación del proyecto

### 1. Clonar el repositorio

```bash
git clone https://github.com/Rams302/TitanicAPI.git
```

Ingresar al proyecto:

```bash
cd TitanicAPI
```

---

### 2. Crear el entorno virtual

#### Windows

```powershell
python -m venv .venv
```

Activar el entorno virtual:

```powershell
.\.venv\Scripts\Activate.ps1
```

#### macOS

```bash
python3 -m venv .venv
```

Activar el entorno virtual:

```bash
source .venv/bin/activate
```

---

### 3. Instalar las dependencias

```powershell
pip install -r requirements.txt
```

---

## Entrenamiento del modelo

Ejecutar:

```powershell
python TitanicAutoML.py
```

El proceso realizará:

- Entrenamiento del modelo.
- Evaluación automática.
- Selección del mejor algoritmo.
- Registro de métricas en MLflow.
- Exportación del modelo entrenado.

---

## Ejecución local de la API

Iniciar el servidor:

```powershell
uvicorn app:app --reload
```

Abrir la documentación automática:

```
http://127.0.0.1:8000/docs
```

También se encuentran disponibles los endpoints:

```
http://127.0.0.1:8000/health
```

```
http://127.0.0.1:8000/info
```

```
http://127.0.0.1:8000/predict
```

---

## Endpoint de predicción

### POST

```
/predict
```

### Ejemplo de petición

```json
{
    "Pclass":1,
    "Sex":"female",
    "Age":30,
    "SibSp":0,
    "Parch":0,
    "Fare":80,
    "Embarked":"S"
}
```

### Ejemplo de respuesta

```json
{
    "request_id":"xxxxxxxx",
    "prediction":1,
    "probabilidad_no_sobrevive":0.1246,
    "probabilidad_sobrevive":0.8753,
    "latency_seconds":0.032,
    "status":"SUCCESS"
}
```

Donde:

- `prediction = 1` → Sobrevive.
- `prediction = 0` → No sobrevive.

---

## Monitoreo y observabilidad

El proyecto incorpora mecanismos de observabilidad basados en:

### Métricas

- Accuracy.
- Tiempo de entrenamiento.
- Latencia.
- Número de solicitudes.
- Predicciones exitosas.
- Porcentaje de errores.
- Datos inválidos.
- Alertas generadas.

### Logs

Los principales archivos utilizados son:

```text
monitoring/predictions.log
```

```text
monitoring/metrics_history.json
```

### Alertas

Se implementaron alertas inteligentes basadas en:

- Latencia máxima permitida.
- Errores del modelo.
- Datos inválidos.
- Posibles anomalías operativas.

Los niveles considerados son:

- INFO
- WARNING
- CRITICAL

---

## Dashboard de monitoreo

Para ejecutar el dashboard:

```powershell
streamlit run dashboard/dashboard.py
```

El dashboard proporciona:

- Métricas operativas.
- Distribución de solicitudes.
- Histórico de latencia.
- Visualización de alertas.
- Información para la toma de decisiones operativas.

---

## MLflow

Para visualizar los experimentos registrados:

```powershell
mlflow ui
```

Por defecto, MLflow estará disponible en:

```
http://127.0.0.1:5000
```

La información registrada incluye:

- Accuracy.
- Tiempo de entrenamiento.
- Versiones del modelo.
- Métricas de inferencia.
- Artefactos generados.
- Parámetros utilizados durante el entrenamiento.

---

## Docker

### Construir la imagen

```powershell
docker build -t titanic-api .
```

### Ejecutar el contenedor

```powershell
docker run -d -p 8000:8000 --name titanic-api-container titanic-api
```

Verificar su ejecución:

```powershell
docker ps
```

---

## Estrategias MLOps implementadas

El proyecto contempla:

- Monitoreo operacional del modelo.
- Validación de datos de entrada.
- Registro histórico de métricas.
- Observabilidad mediante dashboards.
- Gestión del ciclo de vida del modelo con MLflow.
- Diseño de alertas inteligentes.
- Estrategias propuestas para detección de Data Drift.
- Propuestas de rollback y reentrenamiento del modelo.

---

## Evidencias del proyecto

Las evidencias consideradas incluyen:

- Entrenamiento del modelo mediante AutoGluon.
- API REST funcional utilizando FastAPI.
- Contenerización utilizando Docker.
- Dashboard operativo con Streamlit.
- Integración con MLflow.
- Monitoreo MLOps y observabilidad.
- Ejecución local exitosa.
- Validación de los endpoints implementados.
- Registro de métricas y alertas operativas.

---

## Archivos principales

| Archivo | Descripción |
|---------|------------|
| TitanicAutoML.py | Entrenamiento automático del modelo |
| TitanicAutoML.ipynb | Versión utilizada con Google Colab |
| app.py | API REST desarrollada con FastAPI |
| monitor.py | Motor de monitoreo MLOps |
| dashboard.py | Dashboard operativo desarrollado con Streamlit |
| current_model_metrics.json | Configuración de métricas y umbrales |
| training_data.json | Información base del conjunto de entrenamiento |
| Dockerfile | Construcción del contenedor Docker |
| requirements.txt | Dependencias del proyecto |
| TitanicModel/ | Modelo entrenado exportado |
| README.md | Documentación del proyecto |

---

## Autor

**Raúl Ramos Acuña**

Proyecto desarrollado con fines académicos para la materia de Gestión de Proyectos de Inteligencia Artificial.

### Tecnologías implementadas

- Python
- AutoGluon
- FastAPI
- Docker
- MLflow
- Streamlit
- Plotly
- Git
- GitHub
- MLOps
- Observabilidad
