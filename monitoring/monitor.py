# ==========================================================
# MONITORING ENGINE - TITANIC API
# MLOps Monitoring + Logs + Alerts
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


        self.history_file = (

            "monitoring/metrics_history.json"

        )



    # ------------------------------------------------------
    # Leer configuración de umbrales
    # ------------------------------------------------------

    def load_configuration(self):


        with open(

            self.metrics_file,

            "r",

            encoding="utf-8"

        ) as file:


            return json.load(file)



    # ------------------------------------------------------
    # Obtener número de ejecución
    # ------------------------------------------------------

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



    # ------------------------------------------------------
    # Evaluar métricas contra umbrales
    # ------------------------------------------------------

    def evaluate_metrics(

        self,

        latency,

        status

    ):


        config = self.load_configuration()


        thresholds = config["thresholds"]



        alerts = []



        alert_level = "INFO"



        # -------------------------------
        # Validación latencia
        # -------------------------------

        if latency > thresholds[

            "max_latency_seconds"

        ]:


            alerts.append(

                "ADVERTENCIA: la latencia superó el umbral permitido."

            )


            alert_level = "WARNING"



        # -------------------------------
        # Validación errores
        # -------------------------------

        if status == "ERROR":


            alerts.append(

                "CRÍTICO: error durante la ejecución del modelo."

            )


            alert_level = "CRITICAL"



        return {


            "alert_level":

            alert_level,


            "alerts":

            alerts

        }



    # ------------------------------------------------------
    # Generar archivo predictions.log
    # ------------------------------------------------------

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

            status

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

                monitoring_status["alerts"]


            }


        }



        # Crear archivo si no existe

        os.makedirs(

            "monitoring",

            exist_ok=True

        )



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



        # Guardar histórico para dashboard

        self.save_metrics_history(

            log_entry

        )



    # ------------------------------------------------------
    # Guardar métricas históricas
    # ------------------------------------------------------

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

            ["alerts"]

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
