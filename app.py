# ==========================================================
# API REST - TITANIC DATASET
# AutoGluon + FastAPI
# ==========================================================

from fastapi import FastAPI
from pydantic import BaseModel

import pandas as pd

from autogluon.tabular import TabularPredictor

# ----------------------------------------------------------
# Crear aplicación
# ----------------------------------------------------------

app = FastAPI(
    title="Titanic Prediction API",
    description="Predicción de supervivencia utilizando AutoGluon",
    version="1.0"
)

# ----------------------------------------------------------
# Cargar modelo entrenado
# ----------------------------------------------------------

predictor = TabularPredictor.load("TitanicModel")

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
# Endpoint de prueba
# ----------------------------------------------------------

@app.get("/")
def home():

    return {
        "mensaje": "Titanic Prediction API"
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

    datos = pd.DataFrame([passenger.dict()])

    prediccion = predictor.predict(datos)

    probabilidades = predictor.predict_proba(datos)

    return {

        "prediction": int(prediccion.iloc[0]),

        "probabilidad_no_sobrevive":
            float(probabilidades.iloc[0][0]),

        "probabilidad_sobrevive":
            float(probabilidades.iloc[0][1])

    }

