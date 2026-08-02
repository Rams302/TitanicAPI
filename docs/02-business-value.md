# TitanicAPI — Business Value

## 1. Propósito

Este documento describe el valor estratégico y operativo generado por
TitanicAPI, relacionando las capacidades técnicas de la solución con
resultados de negocio, eficiencia operacional, reducción de riesgos y
capacidad de evolución.

El objetivo es demostrar que una solución de Inteligencia Artificial no debe
evaluarse únicamente por la precisión de su modelo, sino también por su
capacidad para generar valor durante todo su ciclo de vida.

TitanicAPI se utiliza como un caso de estudio académico para demostrar cómo
las prácticas de Machine Learning, MLOps, Observabilidad, AI Governance y
FinOps pueden integrarse en una solución tecnológica.

---

# 2. Problema de negocio

Un modelo de Machine Learning puede presentar buenos resultados durante la
etapa de experimentación y, sin embargo, generar problemas cuando se lleva
a operación.

Entre los principales riesgos se encuentran:

- Falta de trazabilidad del modelo.
- Dificultad para identificar errores.
- Datos de entrada incorrectos.
- Incremento de la latencia.
- Degradación del desempeño.
- Cambios en la distribución de los datos.
- Falta de mecanismos de recuperación.
- Costos de infraestructura superiores a los necesarios.
- Falta de responsabilidades claramente definidas.
- Dificultad para demostrar cómo se tomó una decisión basada en IA.

Por esta razón, el proyecto plantea una solución que considera tanto el
modelo predictivo como los procesos necesarios para operarlo.

---

# 3. Propuesta de valor

La propuesta de valor de TitanicAPI puede resumirse de la siguiente manera:

> **Transformar un modelo de Machine Learning en un servicio observable,
> trazable, gobernable y preparado para operar de manera controlada.**

El valor generado se concentra en seis dimensiones:

1. Automatización.
2. Confiabilidad operacional.
3. Observabilidad.
4. Trazabilidad.
5. Gestión de riesgos.
6. Optimización de costos.

---

# 4. Valor generado por la solución

## 4.1 Automatización

AutoGluon permite automatizar parte del proceso de entrenamiento y evaluación
del modelo.

Esto reduce la necesidad de seleccionar manualmente cada algoritmo y permite
establecer un proceso reproducible.

### Beneficio potencial

- Menor esfuerzo manual.
- Mayor velocidad de experimentación.
- Proceso reproducible.
- Comparación sistemática de modelos.
- Mayor facilidad para repetir el entrenamiento.

---

## 4.2 Confiabilidad operacional

FastAPI y Docker permiten convertir el modelo en un servicio que puede
ejecutarse de manera consistente.

La solución incorpora endpoints de:

```text
/
 /health
 /info
 /predict
