# ==========================================================
# MONITORING ENGINE - TITANIC API
# MLOps Monitoring + Logs + Alerts + Data Validation
# ==========================================================


from __future__ import annotations


import os

import json

from datetime import datetime




class ModelMonitor:


    def __init__(self):


        self.log_file = (

            "monitoring/predictions.log"

        )


        self.metrics_file = (

            "monitoring/current_model_metrics.json"

        )


        self.training_file = (

            "monitoring/training_data.json"

        )


        self.history_file = (

            "monitoring/metrics_history.json"

        )



    # ======================================================
    # Leer configuración de métricas
    # ======================================================

    def load_configuration(self):


        if not os.path.exists(

            self.metrics_file

        ):


            return {

                "thresholds": {

                    "max_latency_seconds":0.5,

                    "min_confidence":0.60

                },

                "alerts": {

                    "latency_warning":
                    "ALERTA: latencia superior al límite permitido",

                    "error_warning":
                    "ALERTA: error durante la ejecución del modelo",

                    "invalid_data_warning":
                    "ADVERTENCIA: demasiadas solicitudes contienen datos inválidos",

                    "confidence_warning":
                    "ALERTA: baja confianza en la predicción del modelo"

                }

            }



        with open(

            self.metrics_file,

            "r",

            encoding="utf-8"

        ) as file:


            return json.load(file)



    # ======================================================
    # Leer datos entrenamiento
    # ======================================================

    def load_training_data(self):


        if not os.path.exists(

            self.training_file

        ):


            return {

                "features": {}

            }



        with open(

            self.training_file,

            "r",

            encoding="utf-8"

        ) as file:


            return json.load(file)



    # ======================================================
    # Obtener número ejecución
    # ======================================================

    def get_execution_id(self):


        if not os.path.exists(

            self.history_file

        ):


            return 1



        with open(

            self.history_file,

            "r",

            encoding="utf-8"

        ) as file:


            history = json.load(file)



        return len(history)+1



    # ======================================================
    # Validación datos entrada
    # ======================================================

    def validate_input_data(

        self,

        input_data

    ):


        training = self.load_training_data()


        features = training.get(

            "features",

            {}

        )


        errors = []



        for field, rules in features.items():


            if field not in input_data:


                errors.append(

                    f"Campo faltante: {field}"

                )


                continue



            value = input_data[field]



            if rules["type"] == "integer":


                if not isinstance(

                    value,

                    int

                ):


                    errors.append(

                        f"{field} debe ser entero"

                    )



            elif rules["type"] == "float":


                if not isinstance(

                    value,

                    (int,float)

                ):


                    errors.append(

                        f"{field} debe ser numérico"

                    )



            elif rules["type"] == "string":


                if value not in rules.get(

                    "allowed_values",

                    []

                ):


                    errors.append(

                        f"{field} tiene valor inválido"

                    )



        return errors
