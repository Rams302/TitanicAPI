# ==========================================================
# API REST - TITANIC DATASET
# AutoGluon + FastAPI + Monitoring MLOps + MLflow
# ==========================================================


from fastapi import FastAPI

from pydantic import BaseModel


import pandas as pd


import time

import uuid


import mlflow


from autogluon.tabular import TabularPredictor


from monitoring.monitor import ModelMonitor




# ==========================================================
# CONFIGURACIÓN MLFLOW
# ==========================================================


mlflow.set_tracking_uri(

    "file:./mlruns"

)


mlflow.set_experiment(

    "TitanicAPI_Predictions"

)




# ==========================================================
# CREAR APLICACIÓN
# ==========================================================


app = FastAPI(

    title="Titanic Prediction API",

    description=
    "Predicción de supervivencia Titanic con AutoGluon + MLOps + MLflow",

    version="1.2"

)




# ==========================================================
# CARGAR MODELO
# ==========================================================


predictor = TabularPredictor.load(

    "TitanicModel"

)



MODEL_VERSION = "1.0"




# ==========================================================
# MONITOR
# ==========================================================


monitor = ModelMonitor()




# ==========================================================
# MODELO INPUT
# ==========================================================


class Passenger(BaseModel):


    Pclass: int

    Sex: str

    Age: float

    SibSp: int

    Parch: int

    Fare: float

    Embarked: str




# ==========================================================
# HOME
# ==========================================================


@app.get("/")


def home():


    return {


        "mensaje":
        "Titanic Prediction API",


        "monitoring":
        "enabled",


        "mlflow":
        "enabled"


    }




# ==========================================================
# HEALTH CHECK
# ==========================================================


@app.get("/health")


def health():


    return {


        "status":
        "OK"


    }




# ==========================================================
# INFO MODELO
# ==========================================================


@app.get("/info")


def info():


    return {


        "modelo":
        predictor.model_best,


        "framework":
        "AutoGluon",


        "objetivo":
        "Survived",


        "version":
        MODEL_VERSION


    }




# ==========================================================
# PREDICCIÓN
# ==========================================================


@app.post("/predict")


def predict(passenger: Passenger):



    request_id = str(

        uuid.uuid4()

    )



    start_time = time.time()



    status = "SUCCESS"



    resultado = None



    probabilidades_resultado = None



    with mlflow.start_run(

        run_name="Prediction_Run"

    ):


        try:


            datos = pd.DataFrame(

                [passenger.model_dump()]

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



            status="ERROR"



            resultado=str(error)




        latency = round(

            time.time()

            -

            start_time,

            4

        )



        # ==================================================
        # REGISTRO EN MLFLOW
        # ==================================================



        mlflow.log_param(

            "model_version",

            MODEL_VERSION

        )


        mlflow.log_param(

            "model",

            predictor.model_best

        )


        mlflow.log_metric(

            "latency_seconds",

            latency

        )



        if status=="SUCCESS":


            mlflow.log_metric(

                "prediction",

                resultado

            )


            mlflow.log_metric(

                "prediction_confidence",

                max(

                    probabilidades_resultado.values()

                )

            )


        else:


            mlflow.log_param(

                "error",

                resultado

            )



        # ==================================================
        # MONITORING LOG
        # ==================================================



        monitor.write_prediction_log(

            request_id=request_id,

            input_data=passenger.model_dump(),

            prediction=resultado,

            latency=latency,

            status=status

        )




    # ======================================================
    # RESPUESTA ERROR
    # ======================================================


    if status=="ERROR":


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




    # ======================================================
    # RESPUESTA EXITOSA
    # ======================================================


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
