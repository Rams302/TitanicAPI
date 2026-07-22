# -*- coding: utf-8 -*-

"""
TitanicAutoML.py

Entrenamiento AutoML del dataset Titanic utilizando AutoGluon.

Incluye:
- Entrenamiento del modelo
- Evaluación
- Generación de métricas MLOps
- Registro en MLflow
- Exportación del modelo

Proyecto:
TitanicAPI - MLOps Observabilidad
"""


# =====================================================
# INSTALACIÓN DE DEPENDENCIAS (COLAB)
# =====================================================

# Descomentar si se ejecuta directamente en Google Colab

# !pip -q install autogluon
# !pip -q install mlflow


# =====================================================
# IMPORTS
# =====================================================


import pandas as pd
import json
import os
import shutil

from datetime import datetime

from google.colab import files

from autogluon.tabular import TabularPredictor


# MLFlow

import mlflow



# =====================================================
# CONFIGURACIÓN DEL EXPERIMENTO
# =====================================================


PROJECT_NAME = "TitanicAPI"

MODEL_NAME = "TitanicAutoML"


TRAINING_DATE = datetime.now().strftime(
    "%Y-%m-%d %H:%M:%S"
)



# =====================================================
# CARGAR DATASET
# =====================================================


print("\nCargando dataset Titanic...\n")


df = pd.read_csv(
    "train.csv"
)



print(df.head())


print(df.info())



# =====================================================
# LIMPIEZA DE DATOS
# =====================================================


print(
    "\nEliminando columnas poco útiles..."
)



df = df.drop(

    columns=[

        "PassengerId",

        "Name",

        "Ticket",

        "Cabin"

    ]

)



print(
    "Columnas eliminadas correctamente"
)



# =====================================================
# DIVISIÓN TRAIN / TEST
# =====================================================


train = df.sample(

    frac=0.8,

    random_state=42

)



test = df.drop(
    train.index
)



print()

print(
    "Train:",
    train.shape
)


print(
    "Test :",
    test.shape
)



# =====================================================
# ENTRENAMIENTO AUTOGLUON
# =====================================================


print(
    "\nEntrenando modelo AutoML...\n"
)



predictor = TabularPredictor(

    label="Survived",

    eval_metric="accuracy"

).fit(

    train_data=train,

    presets="medium_quality",

    hyperparameters={

        "GBM": {},

        "RF": {},

        "XT": {},

        "CAT": {},

        "XGB": {}

    }

)



print(
    "\nEntrenamiento finalizado"
)



# =====================================================
# LEADERBOARD
# =====================================================


leaderboard = predictor.leaderboard(

    test

)



print(
    leaderboard
)



# =====================================================
# MODELO GANADOR
# =====================================================


best_model = predictor.model_best



print()

print(
    "Mejor modelo:"
)


print(
    best_model
)



# =====================================================
# EVALUACIÓN DEL MODELO
# =====================================================


performance = predictor.evaluate(

    test

)



print()

print(
    "Métricas del modelo:"
)


print(
    performance
)



accuracy = performance["accuracy"]



# =====================================================
# GENERACIÓN DE MÉTRICAS PARA MLOPS
# =====================================================


print(
    "\nGenerando archivo model_metrics.json..."
)



model_metrics = {


    "model_name":
        MODEL_NAME,


    "framework":
        "AutoGluon",


    "framework_version":
        "1.4.0",


    "best_model":
        best_model,


    "evaluation_metric":
        "accuracy",


    "accuracy":
        float(accuracy),


    "training_rows":
        int(len(train)),


    "testing_rows":
        int(len(test)),


    "training_date":
        TRAINING_DATE


}



with open(

    "model_metrics.json",

    "w"

) as file:


    json.dump(

        model_metrics,

        file,

        indent=4

    )



print(
    "model_metrics.json creado correctamente"
)



# =====================================================
# REGISTRO MLflow
# =====================================================


print(
    "\nRegistrando experimento en MLflow..."
)



mlflow.set_experiment(

    PROJECT_NAME

)



with mlflow.start_run():


    mlflow.log_param(

        "framework",

        "AutoGluon"

    )


    mlflow.log_param(

        "best_model",

        best_model

    )


    mlflow.log_param(

        "preset",

        "medium_quality"

    )


    mlflow.log_metric(

        "accuracy",

        float(accuracy)

    )


    mlflow.log_metric(

        "training_rows",

        len(train)

    )


    mlflow.log_metric(

        "testing_rows",

        len(test)

    )


    mlflow.log_artifact(

        "model_metrics.json"

    )



print(

    "Información registrada en MLflow"

)



# =====================================================
# GUARDAR MODELO
# =====================================================


print(

    "\nGuardando predictor..."

)



predictor.save()



print(

    "Modelo guardado correctamente"

)



# =====================================================
# COMPRIMIR MODELO
# =====================================================


print(

    "\nGenerando archivo TitanicModel.zip..."

)



shutil.make_archive(

    "TitanicModel",

    "zip",

    predictor.path

)



print(

    "Archivo TitanicModel.zip creado"

)



# =====================================================
# DESCARGAR MODELO (COLAB)
# =====================================================


files.download(

    "TitanicModel.zip"

)



print(

    "\nProceso terminado correctamente"

)
