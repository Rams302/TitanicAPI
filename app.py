# ==========================================================
# API REST - TITANIC DATASET
# AutoGluon + FastAPI + Monitoring MLOps
# ==========================================================


from fastapi import FastAPI

from pydantic import BaseModel


import pandas as pd

import time

import uuid

import json

import os


from datetime import datetime


from autogluon.tabular import TabularPredictor


from monitoring.monitor import ModelMonitor



# ----------------------------------------------------------
# Crear aplicación
# ----------------------------------------------------------

app = FastAPI(

    title="Titanic Prediction API",

    description=
    "Predicción Titanic utilizando AutoGluon con monitoreo MLOps",

    version="1.2"

)



# ----------------------------------------------------------
# Cargar modelo
# ----------------------------------------------------------

predictor = TabularPredictor.load(

    "TitanicModel"

)



# ----------------------------------------------------------
# Cargar métricas del modelo
# ----------------------------------------------------------


MODEL_INFO = {}


if os.path.exists(
    "model_metrics.json"
):

    with open(
        "model_metrics.json"
    ) as file:

        MODEL_INFO = json.load(file)



# ----------------------------------------------------------
# Inicializar monitor
# ----------------------------------------------------------


monitor = ModelMonitor()



# ----------------------------------------------------------
# Modelo entrada
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
# Home
# ----------------------------------------------------------

@app.get("/")
def home():

    return {

        "mensaje":
        "Titanic Prediction API",

        "monitoring":
        "enabled",

        "model":
        MODEL_INFO.get(
            "model_name",
            "unknown"
        )

    }



# ----------------------------------------------------------
# Health check
# ----------------------------------------------------------

@app.get("/health")
def health():

    return {

        "status":
        "OK",

        "timestamp":
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    }



# ----------------------------------------------------------
# Información modelo
# ----------------------------------------------------------

@app.get("/info")
def info():

    return {


        "modelo":
        predictor.model_best,


        "framework":
        "AutoGluon",


        "accuracy":
        MODEL_INFO.get(
            "accuracy",
            None
        ),


        "training_date":
        MODEL_INFO.get(
            "training_date",
            None
        )

    }




# ----------------------------------------------------------
# Predicción
# ----------------------------------------------------------

@app.post("/predict")

def predict(passenger: Passenger):


    request_id = str(
        uuid.uuid4()
    )


    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


    start_time = time.time()



    status = "SUCCESS"

    resultado = None

    probabilidades_resultado = {}



    try:


        datos = pd.DataFrame(

            [
                passenger.model_dump()
            ]

        )



        prediccion = predictor.predict(

            datos

        )



        probabilidades = predictor.predict_proba(

            datos

        )



        resultado = int(

            prediccion.iloc[0]

        )



        probabilidades_resultado = {


            "probabilidad_no_sobrevive":

            float(
                probabilidades.iloc[0][0]
            ),



            "probabilidad_sobrevive":

            float(
                probabilidades.iloc[0][1]
            )

        }



    except Exception as error:


        status = "ERROR"


        resultado = str(error)



    latency = round(

        time.time() - start_time,

        4

    )



    # ------------------------------------------------------
    # Log para monitoreo
    # ------------------------------------------------------


    monitor.write_prediction_log(

        timestamp=timestamp,


        request_id=request_id,


        input_data=passenger.model_dump(),


        prediction=resultado,


        probabilities=probabilidades_resultado,


        latency=latency,


        status=status,


        model_version="1.0"

    )




    if status == "ERROR":


        return {


            "request_id":

            request_id,


            "status":

            status,


            "detail":

            resultado

        }




    return {


        "request_id":

        request_id,


        "timestamp":

        timestamp,


        "prediction":

        resultado,


        "probabilidades":

        probabilidades_resultado,


        "latency_seconds":

        latency,


        "status":

        status

    }
