# ==========================================================
# API REST - TITANIC DATASET
# AutoGluon + FastAPI + Monitoring MLOps
# ==========================================================

from fastapi import FastAPI
from pydantic import BaseModel

import pandas as pd

import time
import uuid

from autogluon.tabular import TabularPredictor

from monitoring.monitor import ModelMonitor


# ----------------------------------------------------------
# Crear aplicación
# ----------------------------------------------------------

app = FastAPI(
    title="Titanic Prediction API",
    description="Predicción de supervivencia utilizando AutoGluon con monitoreo MLOps",
    version="1.1"
)


# ----------------------------------------------------------
# Cargar modelo entrenado
# ----------------------------------------------------------

predictor = TabularPredictor.load("TitanicModel")


# ----------------------------------------------------------
# Inicializar monitor
# ----------------------------------------------------------

monitor = ModelMonitor()


# ----------------------------------------------------------
# Modelo de entrada
# ----------------------------------------------------------

class Passenger(BaseModel):

    Pclass: int
    Sex: str
    Age: float
    SibSp: int
    Parch: int
    Fare: float
    Embarked: str


# ----------------------------------------------------------
# Endpoint principal
# ----------------------------------------------------------

@app.get("/")
def home():

    return {
        "mensaje": "Titanic Prediction API",
        "monitoring": "enabled"
    }


# ----------------------------------------------------------
# Health Check
# ----------------------------------------------------------

@app.get("/health")
def health():

    return {
        "status": "OK"
    }


# ----------------------------------------------------------
# Información del modelo
# ----------------------------------------------------------

@app.get("/info")
def info():

    return {
        "modelo": predictor.model_best,
        "framework": "AutoGluon",
        "objetivo": "Survived"
    }


# ----------------------------------------------------------
# Predicción
# ----------------------------------------------------------

@app.post("/predict")
def predict(passenger: Passenger):


    # ------------------------------------------------------
    # Identificador único de la petición
    # ------------------------------------------------------

    request_id = str(uuid.uuid4())


    # ------------------------------------------------------
    # Inicio del contador de latencia
    # ------------------------------------------------------

    start_time = time.time()


    # ------------------------------------------------------
    # Valores iniciales
    # ------------------------------------------------------

    status = "SUCCESS"

    resultado = None

    probabilidades_resultado = None


    # ------------------------------------------------------
    # Predicción del modelo
    # ------------------------------------------------------

    try:

        # Convertir el JSON recibido en DataFrame

        datos = pd.DataFrame(
            [passenger.model_dump()]
        )


        # Ejecutar predicción

        prediccion = predictor.predict(datos)


        # Obtener probabilidades

        probabilidades = predictor.predict_proba(
            datos
        )


        # Guardar resultados

        resultado = int(
            prediccion.iloc[0]
        )


        probabilidades_resultado = {

            "probabilidad_no_sobrevive":
            float(probabilidades.iloc[0][0]),


            "probabilidad_sobrevive":
            float(probabilidades.iloc[0][1])

        }


    except Exception as error:

        status = "ERROR"

        resultado = str(error)


    # ------------------------------------------------------
    # Calcular latencia
    # ------------------------------------------------------

    latency = round(
        time.time() - start_time,
        4
    )


    # ------------------------------------------------------
    # Registrar información para monitoreo
    # ------------------------------------------------------

    monitor.write_prediction_log(

        request_id=request_id,

        input_data=passenger.model_dump(),

        prediction=resultado,

        latency=latency,

        status=status

    )


    # ------------------------------------------------------
    # Respuesta cuando existe un error
    # ------------------------------------------------------

    if status == "ERROR":

        return {

            "request_id":
            request_id,

            "status":
            status,

            "latency_seconds":
            latency,

            "detail":
            resultado

        }


    # ------------------------------------------------------
    # Respuesta exitosa
    # ------------------------------------------------------

    return {

        "request_id":
        request_id,

        "prediction":
        resultado,

        "probabilidad_no_sobrevive":
        probabilidades_resultado[
            "probabilidad_no_sobrevive"
        ],

        "probabilidad_sobrevive":
        probabilidades_resultado[
            "probabilidad_sobrevive"
        ],

        "latency_seconds":
        latency,

        "status":
        status

    }
