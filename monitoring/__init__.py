# ==========================================================
# TITANIC API - MONITORING PACKAGE
# ==========================================================

"""
Paquete de monitoreo MLOps para Titanic API.

Incluye:
- Registro de predicciones
- Validación de datos
- Generación de alertas
- Históricos para dashboards
"""


from .monitor import ModelMonitor


__all__ = [

    "ModelMonitor"

]
