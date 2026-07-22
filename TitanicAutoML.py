# -*- coding: utf-8 -*-

"""
Titanic Dataset
AutoGluon AutoML + MLflow Tracking

Entrenamiento y registro del modelo Titanic
"""



# =====================================================
# INSTALAR DEPENDENCIAS
# =====================================================

!pip -q install autogluon mlflow



# =====================================================
# IMPORTS
# =====================================================


import pandas as pd

import shutil

import os

import time


from google.colab import files


from autogluon.tabular import TabularPredictor


import mlflow

import mlflow.sklearn




# =====================================================
# CONFIGURACIÓN MLFLOW
# =====================================================


mlflow.set_experiment(

    "TitanicAutoML"

)



# =====================================================
# CARGAR DATASET
# =====================================================


df = pd.read_csv(

    "train.csv"

)



print(df.head())


print(df.info())




# =====================================================
# PREPARACIÓN DATASET
# =====================================================


df = df.drop(

    columns=[

        "PassengerId",

        "Name",

        "Ticket",

        "Cabin"

    ]

)




# =====================================================
# SEPARACIÓN TRAIN / TEST
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

    "Test:",

    test.shape

)




# =====================================================
# ENTRENAMIENTO + MLFLOW TRACKING
# =====================================================



with mlflow.start_run(

    run_name="Titanic_AutoGluon_Run"

):


    start_time = time.time()



    # -------------------------------------------------
    # Registrar parámetros
    # -------------------------------------------------


    mlflow.log_param(

        "framework",

        "AutoGluon"

    )


    mlflow.log_param(

        "preset",

        "medium_quality"

    )


    mlflow.log_param(

        "evaluation_metric",

        "accuracy"

    )


    mlflow.log_param(

        "train_size",

        len(train)

    )


    mlflow.log_param(

        "test_size",

        len(test)

    )



    # -------------------------------------------------
    # Entrenar modelo
    # -------------------------------------------------


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



    training_time = (

        time.time()

        -

        start_time

    )



    # -------------------------------------------------
    # Ranking modelos
    # -------------------------------------------------


    leaderboard = predictor.leaderboard(

        test

    )



    print(leaderboard)




    # -------------------------------------------------
    # Mejor modelo
    # -------------------------------------------------


    best_model = predictor.model_best



    print()

    print(

        "Mejor modelo:"

    )

    print(best_model)



    mlflow.log_param(

        "best_model",

        best_model

    )




    # -------------------------------------------------
    # Evaluación
    # -------------------------------------------------


    performance = predictor.evaluate(

        test

    )



    print()

    print(performance)




    accuracy = performance[

        "accuracy"

    ]



    # -------------------------------------------------
    # Registrar métricas MLflow
    # -------------------------------------------------


    mlflow.log_metric(

        "accuracy",

        accuracy

    )


    mlflow.log_metric(

        "training_time_seconds",

        training_time

    )



    # -------------------------------------------------
    # Guardar predictor
    # -------------------------------------------------


    predictor.save()



    print()

    print(

        "Modelo guardado correctamente."

    )



    # -------------------------------------------------
    # Crear ZIP modelo
    # -------------------------------------------------


    shutil.make_archive(

        "TitanicModel",

        "zip",

        predictor.path

    )



    print(

        "TitanicModel.zip generado."

    )



    # -------------------------------------------------
    # Registrar artefacto MLflow
    # -------------------------------------------------


    mlflow.log_artifact(

        "TitanicModel.zip"

    )



    print(

        "Artefacto registrado en MLflow."

    )



    # -------------------------------------------------
    # Información final del Run
    # -------------------------------------------------


    print()

    print("==============================")

    print("MLFLOW RUN FINALIZADO")

    print("==============================")

    print()

    print(

        "Run ID:",

        mlflow.active_run().info.run_id

    )



# =====================================================
# DESCARGA PARA COLAB
# =====================================================


files.download(

    "TitanicModel.zip"

)
