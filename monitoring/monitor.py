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


        # Archivo de logs detallados

        self.log_file = (

            "monitoring/predictions.log"

        )


        # Configuración de umbrales

        self.metrics_file = (

            "monitoring/current_model_metrics.json"

        )


        # Datos base del entrenamiento

        self.training_file = (

            "monitoring/training_data.json"

        )


        # Histórico utilizado por dashboard

        self.history_file = (

            "monitoring/metrics_history.json"

        )



    # ======================================================
    # Leer configuración de métricas
    # ======================================================

    def load_configuration(self):


        with open(

            self.metrics_file,

            "r",

            encoding="utf-8"

        ) as file:


            return json.load(file)



    # ======================================================
    # Leer información del entrenamiento
    # ======================================================

    def load_training_data(self):


        with open(

            self.training_file,

            "r",

            encoding="utf-8"

        ) as file:


            return json.load(file)



    # ======================================================
    # Obtener número de ejecución
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



        return len(history) + 1



    # ======================================================
    # Validación de datos de entrada
    # ======================================================

    def validate_input_data(

        self,

        input_data

    ):


        training = self.load_training_data()


        features = training["features"]


        errors = []



        for field, rules in features.items():


            # Validar existencia del campo

            if field not in input_data:


                errors.append(

                    f"Campo faltante: {field}"

                )

                continue



            value = input_data[field]



            # ----------------------------------------------
            # Validación enteros
            # ----------------------------------------------

            if rules["type"] == "integer":


                if not isinstance(value, int):


                    errors.append(

                        f"{field} debe ser entero"

                    )



                elif (

                    "min" in rules

                    and value < rules["min"]

                ):


                    errors.append(

                        f"{field} menor al mínimo permitido"

                    )



                elif (

                    "max" in rules

                    and value > rules["max"]

                ):


                    errors.append(

                        f"{field} mayor al máximo permitido"

                    )



            # ----------------------------------------------
            # Validación flotantes
            # ----------------------------------------------

            if rules["type"] == "float":


                if not isinstance(

                    value,

                    (int, float)

                ):


                    errors.append(

                        f"{field} debe ser numérico"

                    )


                elif (

                    value < rules["min"]

                    or

                    value > rules["max"]

                ):


                    errors.append(

                        f"{field} fuera de rango permitido"

                    )



            # ----------------------------------------------
            # Validación strings
            # ----------------------------------------------

            if rules["type"] == "string":


                if value not in rules["allowed_values"]:


                    errors.append(

                        f"{field} tiene un valor inválido"

                    )



        return errors



    # ======================================================
    # Evaluación de métricas y generación de alertas
    # ======================================================

    def evaluate_metrics(

        self,

        latency,

        status,

        input_data

    ):


        config = self.load_configuration()


        thresholds = config["thresholds"]


        alerts = []


        alert_level = "INFO"



        # ----------------------------------------------
        # Validación de latencia
        # ----------------------------------------------

        if latency > thresholds["max_latency_seconds"]:


            alerts.append(

                config["alerts"]["latency_warning"]

            )


            alert_level = "WARNING"



        # ----------------------------------------------
        # Validación de errores
        # ----------------------------------------------

        if status == "ERROR":


            alerts.append(

                config["alerts"]["error_warning"]

            )


            alert_level = "CRITICAL"



        # ----------------------------------------------
        # Validación calidad de datos
        # ----------------------------------------------

        validation_errors = self.validate_input_data(

            input_data

        )


        if len(validation_errors) > 0:


            alerts.append(

                config["alerts"]

                ["invalid_data_warning"]

            )


            alert_level = "WARNING"



        return {


            "alert_level":

            alert_level,


            "alerts":

            alerts,


            "validation_errors":

            validation_errors

        }



    # ======================================================
    # Crear registro de predicción
    # ======================================================

    def write_prediction_log(

        self,

        request_id,

        input_data,

        prediction,

        latency,

        status

    ):



        execution_id = self.get_execution_id()



        monitoring_status = self.evaluate_metrics(

            latency,

            status,

            input_data

        )



        log_entry = {



            "timestamp":

            datetime.now().isoformat(),



            "execution_id":

            execution_id,



            "request_id":

            request_id,



            "event_type":

            "MODEL_PREDICTION",



            "status":

            status,



            "input_data":

            input_data,



            "model_response":

            prediction,



            "performance":

            {


                "latency_seconds":

                latency


            },



            "monitoring":

            {


                "alert_level":

                monitoring_status["alert_level"],



                "alerts":

                monitoring_status["alerts"],



                "validation_errors":

                monitoring_status["validation_errors"]


            }


        }



        # Crear carpeta si no existe

        os.makedirs(

            "monitoring",

            exist_ok=True

        )



        # ----------------------------------------------
        # Guardar log detallado
        # ----------------------------------------------

        with open(

            self.log_file,

            "a",

            encoding="utf-8"

        ) as file:


            file.write(

                "\n"

                + "=" * 70

                + "\n"

            )


            file.write(

                json.dumps(

                    log_entry,

                    indent=4,

                    ensure_ascii=False

                )

            )


            file.write(

                "\n"

                + "=" * 70

                + "\n"

            )



        # Guardar histórico

        self.save_metrics_history(

            log_entry

        )



    # ======================================================
    # Guardar histórico para Dashboard
    # ======================================================

    def save_metrics_history(

        self,

        log_entry

    ):



        history = []



        if os.path.exists(

            self.history_file

        ):



            with open(

                self.history_file,

                "r",

                encoding="utf-8"

            ) as file:


                history = json.load(file)



        history_record = {



            "execution_id":

            log_entry["execution_id"],



            "timestamp":

            log_entry["timestamp"],



            "status":

            log_entry["status"],



            "latency_seconds":

            log_entry["performance"]

            ["latency_seconds"],



            "alert_level":

            log_entry["monitoring"]

            ["alert_level"],



            "alerts":

            log_entry["monitoring"]

            ["alerts"],



            "invalid_data":

            len(

                log_entry["monitoring"]

                ["validation_errors"]

            ) > 0


        }



        history.append(

            history_record

        )



        with open(

            self.history_file,

            "w",

            encoding="utf-8"

        ) as file:


            json.dump(

                history,

                file,

                indent=4,

                ensure_ascii=False

            )
