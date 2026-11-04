---
id: hacer-preguntas-buenas
titulo: Formular buenas preguntas
fase: 0
nivel: básico
rutas: [core, ds]
prerequisitos: [mapa-del-portal]
tags: [metodo, analisis, decisiones, estadistica]
resumen: Una pregunta útil dice qué unidad cuenta, sobre quién, con qué métrica, contra qué se compara y qué harás según el resultado. Lo demás es curiosidad.
fuentes: ["Box (1976), 'Science and Statistics'"]
---

## En una frase

Una pregunta útil lleva cinco cosas: qué unidad estás contando, sobre qué población y periodo, con
qué métrica exacta, contra qué la comparas y qué harás según lo que salga. Si falta alguna, la
respuesta será entretenida e inútil.

## La idea

Es la diferencia entre entrar en la consulta diciendo «me duele algo» y decir «me duele la rodilla
derecha al subir escaleras desde hace dos semanas». Con lo primero, el médico solo puede hacerte
veinte preguntas o pedir treinta pruebas. Con lo segundo, en dos minutos sabe qué mirar.

Con los datos pasa igual. «¿Los clientes están contentos?» no se puede responder; «¿qué porcentaje
de pedidos de marzo se entregó en menos de 48 horas, comparado con febrero?» sí. La transformación
casi siempre es la misma: sustituir una sensación por una cuenta.

| Pregunta vaga | Pregunta respondible |
| --- | --- |
| ¿Funciona el marketing? | ¿El valor medio por pedido de los que llegan por correo supera al de los que llegan por búsqueda, con al menos 500 pedidos en cada grupo? |
| ¿Por qué se van los clientes? | ¿Qué proporción de clientes con tres o más incidencias abiertas canceló en los 30 días siguientes? |
| ¿El modelo nuevo es mejor? | ¿Reduce el error absoluto medio en el conjunto de prueba reservado más de un 5 % respecto al actual? |
| ¿Los datos son buenos? | ¿Cuántas filas tienen fecha fuera del rango 2015-2024 o importe negativo? |

Antes de escribir nada, decide de qué **tipo** es tu pregunta, porque cada tipo pide un diseño
distinto:

- **descriptiva** — «¿qué pasó?». Se responde con un resumen y su incertidumbre.
- **diagnóstica** — «¿por qué pasó?». Necesita comparar grupos y descartar explicaciones alternativas.
- **predictiva** — «¿qué pasará?». Necesita una validación honesta: medir en datos que no has usado.
- **causal** — «¿funcionó?». Solo se responde con un experimento o un diseño causal, nunca con una
  correlación por muy alta que sea: [[causalidad-vs-correlacion|correlación no es causa]].

Y el filtro final, el más incómodo: **¿qué resultado te haría cambiar de opinión?** Si la respuesta
es «ninguno», no tienes una pregunta, tienes una preferencia con gráficos.

## Definición formal

Una pregunta respondible es una tupla de cinco elementos. Escríbela entera antes de tocar los datos:

1. **Unidad de análisis** — qué es una fila: un pedido, un cliente, un día por tienda, una
   combinación de ambas. Cambiar la unidad cambia el resultado, aunque los datos sean los mismos.
2. **Población y periodo** — sobre quién y de cuándo; es la distinción entre
   [[poblacion-y-muestra|población y muestra]]. Si la muestra es un trozo de la población, dilo: es
   la diferencia entre describir lo medido y extrapolar.
3. **Métrica** — con nombre, fórmula, ventana y filtros. No «satisfacción», sino
   `tasa_cancelacion_30d = cancelaciones en 30 días / clientes activos al inicio`.
4. **Comparación** — contra qué: el periodo anterior, un grupo de control, un objetivo, otro modelo.
   Sin comparación no hay conclusión, solo un número.
5. **Criterio de decisión** — el umbral y la acción: «si sube 5 puntos y el volumen no cae, lo
   llevamos al segundo almacén».

Un atajo para el punto 3: si no puedes escribir la fórmula en una línea, no has decidido qué mides.
Y un atajo para el 5: si no hay acción asociada, probablemente la pregunta se puede aplazar.

## Ejemplo

La tienda quiere saber si ha mejorado en entregas. Los datos:

| Mes | Pedidos | Entregados en 48 h o menos |
| --- | --- | --- |
| Febrero | 12.000 | 78 % |
| Marzo | 11.400 | 85 % |

La diferencia es de 7 puntos. ¿Es grande o es ruido? El error típico de una proporción con
`n = 12.000` y `p = 0,78` es `√(0,78 · 0,22 / 12.000) ≈ 0,0038`; para marzo, `≈ 0,0033`. El error
típico de la diferencia, al ser muestras independientes, es `√(0,0038² + 0,0033²) ≈ 0,005`. Los 7
puntos son unos 14 errores típicos: la mejora no es ruido de muestreo.

Fíjate en lo que ha cambiado al completar la pregunta. «¿Mejoramos las entregas?» no decidía nada.
«¿La proporción pasó del 78 % al 85 %, con más de 10.000 pedidos cada mes, y supera el umbral de
5 puntos que acordamos para extender el cambio al segundo almacén?» se responde con un sí y una
acción detrás.

## Código

```python verificable
import numpy as np
from scipy.stats import norm

# Datos de ejemplo: pedidos entregados en 48 h o menos, por mes.
p1, n1 = 0.78, 12_000     # febrero
p2, n2 = 0.85, 11_400     # marzo

diferencia = p2 - p1
ee_intervalo = np.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)   # sin agrupar

# Para contrastar la igualdad de proporciones se usa la proporcion agrupada,
# que es mas conservadora que el error tipico del intervalo.
p_comun = (n1 * p1 + n2 * p2) / (n1 + n2)
ee_test = np.sqrt(p_comun * (1 - p_comun) * (1 / n1 + 1 / n2))
z = diferencia / ee_test

print(f"diferencia        {diferencia:+.3f}  ({diferencia * 100:+.1f} puntos)")
print(f"error tipico (IC) {ee_intervalo:.5f}")                  # -> 0.00505
print(f"z del contraste   {z:.2f}")                             # -> 13.76
print(f"p-valor (2 colas) {2 * norm.sf(abs(z)):.1e}")           # -> 4.6e-43
print(f"diferencia / ee   {diferencia / ee_intervalo:.1f}")     # -> 13.9: no es ruido
```

```python verificable
import pandas as pd

# La misma pregunta tiene dos respuestas si no fijas la unidad de analisis:
# una fila puede ser un pedido o un cliente, y no son lo mismo.
pedidos = pd.DataFrame({
    "cliente": ["A", "A", "A", "B", "C"],
    "importe": [10.0, 12.0, 8.0, 90.0, 25.0],
})

print("media por pedido :", round(pedidos["importe"].mean(), 2))                           # -> 29.0
print("media por cliente:", round(pedidos.groupby("cliente")["importe"].sum().mean(), 2))   # -> 48.33
print("pedidos por cliente:", pedidos.groupby("cliente").size().to_dict())                  # -> A:3, B:1, C:1
```

## Errores típicos

- **Preguntar por la causa con datos observacionales.** «Los que usan la función X cancelan menos,
  luego la función X retiene» es exactamente lo que no se puede concluir sin un diseño causal:
  quizá la usan los que ya estaban más contentos.
- **Cambiar la pregunta después de ver los datos.** Si empiezas buscando una cosa y publicas la
  que salió significativa, el resultado está sesgado: es una forma de
  [[multiplicidad-y-fdr|comparar muchas cosas a la vez]]. Escribe la pregunta y el umbral antes.
- **No fijar la unidad de análisis.** ¿Una fila es un pedido o un cliente? Con los mismos datos,
  la media por pedido es 29 y la media por cliente es 48,33. Las dos son correctas y responden a
  preguntas distintas.
- **Preguntar por el promedio cuando la decisión depende de la cola.** Para latencia o tiempos de
  espera, lo que rompe el servicio son los [[cuantiles-y-percentiles|percentiles]] p95 o p99, no la
  media.
- **Preguntas sin umbral.** «¿Ha subido el uso?» no decide nada: cualquier variación sirve para
  justificar lo que ya querías hacer. Fija el mínimo que consideras relevante.
- **Confundir tu pregunta con la del negocio.** «¿Sube el engagement?» no es la pregunta si la
  decisión real es si se mantiene el equipo que desarrolla la función.

## Comprueba que lo sabes

:::quiz
p: ¿Cuál de estas preguntas se puede responder con datos y una decisión detrás?
o: ¿Están contentos nuestros usuarios?
o: ¿Qué proporción de usuarios que abrieron una incidencia la cerró en menos de 48 h en marzo, frente al 62 % de febrero, y supera el umbral del 70 %?
o: ¿Deberíamos mejorar el producto?
a: 2
e: La segunda fija unidad (usuario con incidencia), periodo (marzo frente a febrero), métrica (proporción cerrada en 48 h) y umbral (70 %). Las otras dos expresan intenciones: no dicen qué se cuenta ni cuándo una respuesta cambia algo.
:::

:::quiz
p: Con los mismos datos, la media por pedido es 29,00 € y la media por cliente es 48,33 €. ¿Por qué?
o: Porque una de las dos está mal calculada
o: Porque cambia la unidad de análisis: hay clientes con 3 pedidos y clientes con 1, y ponderan distinto
o: Porque la media por cliente excluye los pedidos pequeños
a: 2
e: Ninguna está mal: miden cosas distintas. Al promediar por cliente, cada cliente pesa lo mismo independientemente de cuántos pedidos haya hecho, así que el cliente B, con un pedido de 90 €, pesa tanto como el A, con tres pedidos que suman 30 €. Elegir la unidad es una decisión del analista, no un detalle técnico.
:::

:::practica
enunciado: Convierte «¿por qué se van los clientes?» en una pregunta respondible con sus cinco elementos, sabiendo que tienes una tabla de bajas con fecha, plan contratado, antigüedad y número de incidencias.
pista: El «por qué» no se responde con datos observacionales; conviértelo en una comparación entre grupos.
solucion: Unidad: cliente que causó baja. Población y periodo: clientes activos entre enero y junio de este año. Métrica: tasa de baja a 90 días, calculada como bajas en la ventana divididas entre clientes activos al inicio. Comparación: clientes con 3 o más incidencias frente a clientes con 0 o 1, y plan contratado como control. Criterio: si la diferencia supera 10 puntos y se mantiene en dos trimestres, se revisa el protocolo de soporte. Ojo: sigue siendo descriptivo; para hablar de causa haría falta un diseño causal, no solo esta comparación.
:::

:::trampa
El error más caro no es equivocarse en el cálculo, es responder a una pregunta distinta de la que
importaba. Antes de optimizar una métrica, pregunta quién va a tomar qué decisión con ese número.
Si nadie va a decidir nada, probablemente la pregunta correcta es otra.
:::
