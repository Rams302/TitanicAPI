# API de Predicción de Supervivencia del Titanic utilizando AutoML (AutoGluon)

## Descripción

Este proyecto implementa un modelo de Machine Learning para predecir la supervivencia de los pasajeros del Titanic utilizando el conjunto de datos de Kaggle.

El modelo fue desarrollado mediante técnicas de AutoML con AutoGluon y posteriormente desplegado mediante una API REST utilizando FastAPI. Finalmente, la aplicación fue contenerizada utilizando Docker para facilitar su portabilidad y ejecución.

---

## Objetivo

Desarrollar un servicio web que permita predecir automáticamente si un pasajero del Titanic sobrevivirá o no, utilizando un modelo entrenado con técnicas de Machine Learning y desplegado mediante una API REST.

---

## Tecnologías utilizadas

- Python 3.12
- AutoGluon
- FastAPI
- Uvicorn
- Pandas
- Docker
- Swagger UI

---

## Dataset

Se utilizó el conjunto de datos **Titanic Dataset** publicado en Kaggle.

https://www.kaggle.com/competitions/titanic/data

Archivo utilizado:

```
train.csv
```

---

## Estructura del proyecto

```
TitanicAPI/
│
├── TitanicModel/
│   ├── learner.pkl
│   ├── predictor.pkl
│   ├── metadata.json
│   ├── version.txt
│   └── ...
│
├── app.py
├── TitanicAutoML.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
├── README.md
└── train.csv
```

---

## Instalación del proyecto

### 1. Clonar el repositorio

```bash
git clone https://github.com/Rams302/TitanicAPI.git
```

Entrar al proyecto

```bash
cd TitanicAPI
```

---

### 2. Crear un entorno virtual

Windows

```powershell
python -m venv .venv
```

Activar el entorno

```powershell
.\.venv\Scripts\Activate.ps1
```

---

### 3. Instalar las dependencias

```powershell
pip install -r requirements.txt
```

---

## Ejecución local

Iniciar el servidor

```powershell
uvicorn app:app --reload
```

Abrir el navegador

```
http://127.0.0.1:8000/docs
```

Se abrirá automáticamente la documentación Swagger.

---

## Construcción de la imagen Docker

Construir la imagen

```powershell
docker build -t titanic-api .
```

---

## Ejecutar el contenedor

```powershell
docker run -d -p 8000:8000 --name titanic-api-container titanic-api
```

Verificar que el contenedor se encuentre en ejecución

```powershell
docker ps
```

---

## Endpoint disponible

### POST

```
/predict
```

---

## Ejemplo de petición

```json
{
  "Pclass": 1,
  "Sex": "female",
  "Age": 30,
  "SibSp": 0,
  "Parch": 0,
  "Fare": 80,
  "Embarked": "S"
}
```

---

## Ejemplo de respuesta

```json
{
  "prediction": 1,
  "probabilidad_no_sobrevive": 0.12460774183273315,
  "probabilidad_sobrevive": 0.8753922581672668
}
```

Donde:

- **prediction = 1** → Sobrevive.
- **prediction = 0** → No sobrevive.

---

## Evidencias del proyecto

El proyecto fue validado mediante:

- Entrenamiento automático con AutoGluon.
- Exportación del modelo entrenado.
- Desarrollo de una API REST con FastAPI.
- Documentación automática mediante Swagger.
- Construcción de una imagen Docker.
- Ejecución del contenedor Docker.
- Prueba del endpoint `/predict` desde Swagger.
- Ejecución local exitosa.

---

## Archivos principales

| Archivo | Descripción |
|----------|-------------|
| TitanicAutoML.py | Entrenamiento del modelo AutoML |
| app.py | API REST desarrollada con FastAPI |
| Dockerfile | Construcción del contenedor Docker |
| requirements.txt | Dependencias del proyecto |
| TitanicModel/ | Modelo entrenado exportado |
| README.md | Documentación del proyecto |

---

## Resultados

El modelo fue entrenado utilizando AutoGluon, el cual evaluó automáticamente distintos algoritmos de clasificación y seleccionó el modelo con mejor desempeño. Dicho modelo fue exportado y utilizado por la API para realizar predicciones sobre nuevos registros de pasajeros.

La API responde en formato JSON indicando tanto la clase predicha como las probabilidades asociadas a cada posible resultado.

---

## Autor

Raúl Ramos Acuña

Proyecto desarrollado con fines académicos para la materia de Gestión de Proyectos de Inteligencia Artificial.

Tecnologías utilizadas:

- Python
- AutoGluon
- FastAPI
- Docker
- GitHub