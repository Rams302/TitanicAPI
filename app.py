# ==========================================================
# API REST - TITANIC DATASET
# AutoGluon + FastAPI + MLOps Monitoring
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

    description=
    "Predicción de supervivencia utilizando AutoGluon con monitoreo MLOps",

    version="1.1"

)



# ----------------------------------------------------------
# Cargar modelo entrenado
# ----------------------------------------------------------

predictor = TabularPredictor.load(
    "TitanicModel"
)



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

        "mensaje":
        "Titanic Prediction API",

        "monitoring":
        "enabled"

    }



# ----------------------------------------------------------
# Health Check
# ----------------------------------------------------------

@app.get("/health")
def health():

    return {

        "status":
        "OK"

    }



# ----------------------------------------------------------
# Información del modelo
# ----------------------------------------------------------

@app.get("/info")
def info():

    return {

        "modelo":
        predictor.model_best,

        "framework":
        "AutoGluon",

        "objetivo":
        "Survived"

    }



# ----------------------------------------------------------
# Predicción
# ----------------------------------------------------------

@app.post("/predict")
def predict(passenger: Passenger):


    request_id = str(
        uuid.uuid4()
    )


    start_time = time.time()


    status = "SUCCESS"


    resultado = None


    try:


        datos = pd.DataFrame(
            [passenger.dict()]
        )


        prediccion = predictor.predict(
            datos
        )


        probabilidades = predictor.predict_proba(
            datos
        )


        resultado = {


            "prediction":
            int(prediccion.iloc[0]),


            "probabilidad_no_sobrevive":
            float(probabilidades.iloc[0][0]),


            "probabilidad_sobrevive":
            float(probabilidades.iloc[0][1])

        }



    except Exception as error:


        status = "ERROR"


        resultado = {


            "error":
            str(error)

        }



    finally:


        latency = round(

            time.time()
            -
            start_time,

            4

        )


        monitor.write_prediction_log(

            request_id=request_id,

            input_data=passenger.dict(),

            prediction=resultado,

            latency=latency,

            status=status

        )



    return {


        "request_id":

        request_id,


        "status":

        status,


        "latency_seconds":

        latency,


        "result":

        resultado

    }
