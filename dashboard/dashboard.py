# ==========================================================
# TITANIC API - MLOps Monitoring Dashboard
# Streamlit + Plotly
# ==========================================================


import streamlit as st

import pandas as pd

import json

import os


import plotly.express as px

import plotly.graph_objects as go



# ==========================================================
# CONFIGURACIÓN
# ==========================================================


st.set_page_config(

    page_title="Titanic API Monitoring Dashboard",

    page_icon="📊",

    layout="wide"

)



# ==========================================================
# RUTAS
# ==========================================================


BASE_PATH = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


HISTORY_FILE = os.path.join(

    BASE_PATH,

    "monitoring",

    "metrics_history.json"

)


CONFIG_FILE = os.path.join(

    BASE_PATH,

    "monitoring",

    "current_model_metrics.json"

)



# ==========================================================
# FUNCIONES
# ==========================================================


def load_json(path):


    if not os.path.exists(path):

        return None


    with open(

        path,

        "r",

        encoding="utf-8"

    ) as file:


        return json.load(file)




def load_history():


    data = load_json(

        HISTORY_FILE

    )


    if data is None:

        return pd.DataFrame()


    return pd.DataFrame(data)




# ==========================================================
# CARGAR DATOS
# ==========================================================


df = load_history()


config = load_json(

    CONFIG_FILE

)




# ==========================================================
# TITULO
# ==========================================================


st.title(
    "📊 Titanic API - MLOps Monitoring Dashboard"
)


st.write(

    "Dashboard operacional para monitoreo del modelo Titanic usando métricas generadas por la API."

)



# ==========================================================
# INFORMACIÓN DEL MODELO
# ==========================================================


if config:


    st.subheader(

        "Información del modelo"

    )


    col1,col2,col3,col4 = st.columns(4)



    col1.metric(

        "Modelo",

        config.get(

            "model_name",

            "N/A"

        )

    )


    col2.metric(

        "Versión",

        config.get(

            "model_version",

            "N/A"

        )

    )


    col3.metric(

        "Framework",

        config.get(

            "framework",

            "N/A"

        )

    )


    col4.metric(

        "Accuracy mínima",

        config.get(

            "thresholds",

            {}

        ).get(

            "min_accuracy",

            0

        )

    )




# ==========================================================
# VALIDACIÓN
# ==========================================================


if df.empty:


    st.warning(

        "No existen métricas todavía. Ejecute predicciones desde la API."

    )


    st.stop()



# ==========================================================
# MÉTRICAS OPERACIONALES
# ==========================================================


st.subheader(

    "Indicadores operacionales"

)



total = len(df)



errors = (

    df["status"]

    ==

    "ERROR"

).sum()



success = (

    df["status"]

    ==

    "SUCCESS"

).sum()



alerts = (

    df["alert_level"]

    !=

    "INFO"

).sum()



invalid = (

    df["invalid_data"]

    ==

    True

).sum()



latency = round(

    df["latency_seconds"].mean(),

    4

)



c1,c2,c3,c4,c5 = st.columns(5)



c1.metric(

    "Requests",

    total

)


c2.metric(

    "Éxitos",

    success

)


c3.metric(

    "Errores",

    errors

)


c4.metric(

    "Latencia promedio",

    latency

)


c5.metric(

    "Alertas",

    alerts

)




# ==========================================================
# GRAFICA 1
# DISTRIBUCIÓN REQUESTS
# ==========================================================


st.subheader(

    "Distribución de solicitudes"

)



status_df = (

    df["status"]

    .value_counts()

    .reset_index()

)



status_df.columns=[

    "status",

    "cantidad"

]



fig_pie = px.pie(

    status_df,

    names="status",

    values="cantidad",

    title="Estado de solicitudes"

)



st.plotly_chart(

    fig_pie,

    use_container_width=True

)



# ==========================================================
# GRAFICA 2
# LATENCIA
# ==========================================================


st.subheader(

    "Latencia por ejecución"

)



fig_latency = go.Figure()



fig_latency.add_trace(

    go.Scatter(

        x=df["execution_id"],

        y=df["latency_seconds"],

        mode="lines+markers",

        name="Latencia"

    )

)



max_latency = config.get(

    "thresholds",

    {}

).get(

    "max_latency_seconds",

    2

)



fig_latency.add_trace(

    go.Scatter(

        x=df["execution_id"],

        y=[max_latency]*len(df),

        mode="lines",

        name="Umbral máximo",

        line=dict(

            dash="dash"

        )

    )

)



fig_latency.update_layout(

    xaxis_title="Ejecución",

    yaxis_title="Segundos"

)



st.plotly_chart(

    fig_latency,

    use_container_width=True

)



# ==========================================================
# GRAFICA 3
# HISTÓRICO MÉTRICAS
# ==========================================================


st.subheader(

    "Histórico de ejecuciones"

)



fig_bar = px.bar(

    df,

    x="execution_id",

    y="latency_seconds",

    color="status",

    title="Latencia histórica"

)



st.plotly_chart(

    fig_bar,

    use_container_width=True

)



# ==========================================================
# ALERTAS
# ==========================================================


st.subheader(

    "Alertas generadas"

)



alerts_df = df[

    df["alerts"].apply(

        lambda x:

        len(x)>0

    )

]



if alerts_df.empty:


    st.success(

        "No existen alertas activas."

    )


else:


    for _,row in alerts_df.iterrows():


        for alert in row["alerts"]:


            if row["alert_level"]=="CRITICAL":

                st.error(alert)


            else:

                st.warning(alert)
