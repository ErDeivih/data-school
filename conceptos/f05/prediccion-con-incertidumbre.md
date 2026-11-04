---
id: prediccion-con-incertidumbre
titulo: Predicción con incertidumbre
fase: 5
nivel: avanzado
rutas: [ds, quant]
prerequisitos: [series-temporales-componentes, metricas-de-regresion, validacion-temporal]
tags: [series-temporales, incertidumbre, intervalos]
resumen: Un número suelto esconde la parte que más importa: dar un intervalo con la cobertura prometida en vez de un único valor.
fuentes: ["Hyndman y Athanasopoulos (2021), 'Forecasting: Principles and Practice', cap. 5", "Vovk, Gammerman y Shafer (2005), 'Algorithmic Learning in a Random World'"]
---

## En una frase

Predecir con incertidumbre es dar, junto al valor esperado, un rango que acierte tantas veces como
prometes: si dices «al 90 %», el valor real debe caer dentro nueve de cada diez veces.

## La idea

Un proveedor te pide cuántas unidades vas a comprar el mes que viene y respondes «1.200». Con ese
único número solo se puede hacer una cosa: comprar 1.200 y rezar. Si le dices «entre 1.050 y 1.350
con un 90 % de confianza», ya se pueden tomar decisiones distintas: comprar 1.100, dejar un colchón
pequeño y tener un plan para el caso de que la demanda se vaya a 1.400.

Ese es todo el asunto. Un pronóstico puntual no dice nada sobre lo segura que es la predicción, y
en la práctica **la incertidumbre es la mitad del mensaje**. Hay tres formas de cuantificarla, de
más frágil a más robusta:

1. **Intervalos analíticos.** Asumes una forma para el error (casi siempre normal) y calculas
   `ŷ ± z · σ`. Funciona cuando el supuesto es cierto, y falla justo cuando más importa: colas
   gordas, varianza que cambia por tramos, series con muchos ceros.
2. **Cuantiles.** En vez de predecir la media, predices el percentil 10 y el 90 con una regresión
   cuantílica. No supone simetría: el intervalo puede ser ancho por arriba y estrecho por abajo,
   que es lo que de verdad pasa con la demanda.
3. **Predicción conforme.** Mides el error de tu modelo en un trozo de datos que no ha visto,
   construyes el intervalo con ese error medido y **garantizas la cobertura** sin suponer ninguna
   distribución. Es la más útil en la práctica porque funciona con cualquier modelo, incluido un
   gradient boosting que no sabes ni cómo se comporta.

El error clásico es confundir dos ideas que se parecen y no tienen nada que ver: el **intervalo de
confianza de un parámetro** (dónde está la media del proceso, y se estrecha al añadir datos) y el
**intervalo de predicción de una observación futura** (dónde caerá el próximo valor, y no se
estrecha por mucho que midas el pasado, porque el ruido del futuro sigue ahí). El primero puede ser
`±0,5` y el segundo `±80` con los mismos datos.

## Definición formal

Un intervalo de predicción al nivel `1 − α` para el instante `t + h` es un par `(L, U)` tal que:

:::formula
P( y_{t+h} ∈ [L, U] ) ≥ 1 − α
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `y_{t+h}` | El valor real que se observará dentro de `h` pasos | las de la serie | Es la incógnita: el intervalo habla de dónde caerá |
| `h` | El horizonte: cuántos pasos hacia adelante | pasos (días, meses) | El intervalo se ensancha: hay más tiempo para que el error se acumule |
| `α` | La probabilidad de quedarse fuera del intervalo (1 − cobertura) | tanto por uno, 0 a 1 | El intervalo se **estrecha**: prometes acertar menos veces |
| `1 − α` | La cobertura nominal: la fracción de veces que quieres acertar | tanto por uno, 0 a 1 | El intervalo se ensancha |
| `L`, `U` | Extremo inferior y superior del intervalo | las de la serie | — |
| `q` | Cuantil empírico de los residuos absolutos, calculado en el conjunto de calibración | las de la serie | El intervalo se ensancha; es la corrección que fuerza la cobertura real |
| `n_cal` | Tamaño del conjunto de calibración (datos que el modelo no vio al entrenar) | filas | Más grande, `q` más estable, pero el intervalo no se hace mucho más estrecho |
:::

La predicción conforme *split* (la versión sencilla) se construye en tres pasos. Primero entrenas el
modelo en una parte de los datos. Después calculas los residuos absolutos en el resto (el conjunto
de calibración) y tomas su cuantil `q` en el nivel que quieres:

:::formula
q = cuantil( 1 − α , de los residuos absolutos en calibración )
:::

Y por último el intervalo es `ŷ ± q`. La cobertura es válida aunque el modelo sea malo: si el
modelo se equivoca mucho, `q` sale grande y el intervalo sale ancho. El precio que pagas es ese:
con un modelo flojo obtienes intervalos honestos pero inútiles, no intervalos falsamente estrechos.

:::figura
fichero: prediccion-incertidumbre-intervalo-fijo-o-proporcional
pie: La calibración se abre en abanico: cuanto mayor es la predicción, mayor es el error. Una banda de anchura fija sobra en las predicciones pequeñas y se queda corta en las grandes; la proporcional se ensancha con el tamaño. Las dos cubren un porcentaje parecido en conjunto, pero solo la proporcional promete lo correcto en cada tramo.
fuente: figuras/prediccion-con-incertidumbre-1.py
:::

Una variante importante: si el error crece con el nivel de la predicción (vendes más y te
equivocas más en valor absoluto pero no en porcentaje), divides cada residuo entre la predicción y
calibras `q` sobre esos residuos **normalizados**. El intervalo pasa a ser `ŷ ± q · ŷ`, que es
proporcional: ancho donde las cifras son grandes y estrecho donde son pequeñas.

## Ejemplo

Diez observaciones reales de demanda y sus predicciones, con horizonte de un día:

| Real | Predicción | Residuo |
| --- | --- | --- |
| 104 | 100 | 4 |
| 96 | 100 | −4 |
| 118 | 110 | 8 |
| 89 | 96 | −7 |
| 112 | 105 | 7 |
| 131 | 120 | 11 |
| 95 | 101 | −6 |
| 107 | 99 | 8 |
| 124 | 118 | 6 |
| 88 | 95 | −7 |

Residuos absolutos ordenados: 4, 4, 6, 6, 7, 7, 7, 8, 8, 11. Para una cobertura del 80 % necesitas
el cuantil 0,80, que con 10 valores cae en la posición `0,80 · 11 = 8,8`, es decir el noveno valor:

**q = 8**.

Con una predicción nueva de 115, el intervalo al 80 % es `115 ± 8 = [107, 123]`. Cuando llegue el
dato real, estará dentro o no; a la larga, ocho de cada diez veces dentro. Fíjate en dos cosas: el
intervalo es simétrico porque el método lo es (si quisieras asimetría, usarías cuantiles en vez de
residuos absolutos), y `q` no depende de que el error sea normal, solo de lo que midió en datos.

Este es el caso **sin normalizar**, porque aquí las predicciones son todas del mismo tamaño (entre
95 y 120). Mezclar cifras de ese orden con otras de 5.000 obligaría a normalizar primero: el bloque
de código de abajo hace las dos versiones sobre estos mismos diez valores, y verás que dan anchuras
distintas.

## Código

```python verificable
import numpy as np

# Error del modelo frente al dato real, en el conjunto de calibración
pred = np.array([100, 100, 110, 96, 105, 120, 101, 99, 118, 95])
real = np.array([104, 96, 118, 89, 112, 131, 95, 107, 124, 88])
residuo_norm = np.abs(real - pred) / pred        # cuanto se desvia, en proporcion

# Cuantil empirico con redondeo hacia arriba, como en la prediccion conforme
q = np.quantile(residuo_norm, 0.80, method="higher")
q_abs = np.quantile(np.abs(real - pred), 0.80, method="higher")
print(f"q del error en %     {q:.4f}")           # -> 0.0808
print(f"q del error en unidades {q_abs:.2f}")    # -> 8.00

nueva = 115.0
lo, hi = nueva * (1 - q), nueva * (1 + q)
print(f"intervalo proporcional [{lo:.2f}, {hi:.2f}]")    # -> [105.71, 124.29]
print(f"intervalo en unidades  [{nueva - q_abs:.2f}, {nueva + q_abs:.2f}]")  # -> [107.00, 123.00]
```

:::claves
- `real - pred` es una resta de arrays **elemento a elemento**, no una operación de álgebra lineal. El resultado tiene la misma forma que las entradas (10 elementos). Si dividieras con `@` en vez de `/` el intérprete se quejaría de dimensiones: `@` es producto de matrices.
- `np.abs(...) / pred` divide cada residuo entre **su propia** predicción. Eso es lo que convierte el método en proporcional: un error de 8 sobre una predicción de 100 pesa más que un error de 8 sobre 200.
- El cuantil sube de 8,00 unidades a 0,0808 en proporción, y el intervalo cambia de `[107,00, 123,00]` a `[105,71, 124,29]`: el mismo método con la misma cobertura da dos anchuras distintas porque mide dos cosas distintas. Elige cuál imita mejor cómo se equivoca tu modelo.
- `method="higher"` en `np.quantile` redondea hacia arriba la posición del cuantil: con 10 residuos y nivel 0,80 toma el noveno valor, no interpola entre el noveno y el décimo. La predicción conforme clásica usa justamente ese redondeo hacia arriba, y con `method="linear"` (el valor por defecto de NumPy) el intervalo sale un poco más estrecho y deja de tener la garantía.
- `np.quantile` devuelve un **escalar** de NumPy (`np.float64`), no un array. Se puede imprimir y multiplicar como un número normal, pero si lo guardas en un DataFrame acaba como columna de 1 elemento si no tienes cuidado.
- `np.abs(real - pred)` no modifica ni `real` ni `pred`: crea un array nuevo. Lo mismo con `np.sort`, que devuelve una copia ordenada. Para ordenar en el sitio existe `residuo.sort()`, que devuelve `None` (el error típico es escribir `x = x.sort()` y quedarte con `None`).
:::

## Errores típicos

- **Confundir intervalo de confianza con intervalo de predicción.** El de confianza dice dónde está
  un parámetro del modelo y se estrecha al añadir datos; el de predicción dice dónde caerá la
  próxima observación y **no** se estrecha por debajo de la varianza del ruido, por muchos datos que
  acumules. Publicar el primero como si fuera el segundo es el error más caro de todos.
- **Calibrar sobre los mismos datos con los que entrenaste.** Los residuos en entrenamiento son
  siempre más pequeños que en producción, así que `q` sale corto y el intervalo miente. El
  conjunto de calibración tiene que ser datos que el modelo no ha visto, y en series temporales eso
  obliga a partirlo por fecha ([[validacion-temporal]]), nunca al azar.
- **Prometer una cobertura y no comprobarla.** La cobertura hay que medirla: cuenta en cuántas de
  las últimas 100 predicciones el real cayó dentro. Si prometes 90 % y sale 72 %, el intervalo no
  vale nada aunque sea bonito. Se comprueba igual que cualquier otra métrica
  ([[metricas-de-regresion]]), con la salvedad de que aquí la métrica es la frecuencia de acierto.
- **Suponer normalidad en colas gordas.** Con errores de cola gruesa, `ŷ ± 1,96σ` promete un 95 %
  y da bastante menos, porque los extremos ocurren más de lo que la normal admite. Los cuantiles y
  la predicción conforme no suponen forma y por eso aguantan mejor.
- **Ignorar que la incertidumbre crece con el horizonte.** Un intervalo a un día y otro a un mes no
  pueden tener la misma anchura. Si tu modelo devuelve el mismo margen para todo `h`, no está
  modelando incertidumbre: está devolviendo una constante disfrazada.
- **Calibrar con pocos datos y fiarse de `q`.** Con 20 puntos de calibración, el cuantil 0,95 es
  literalmente el valor más alto observado: cualquier residuo mayor que aparezca después se sale
  del intervalo. Con `n_cal` pequeño, sube el nivel de cobertura que calibras o asume que el
  intervalo es optimista.

## Comprueba que lo sabes

:::quiz
p: Tienes un modelo con un error absoluto medio de 12 unidades. ¿Qué hace la predicción conforme al 90 %?
o: Devuelve la predicción del modelo tal cual, porque el error medio ya es la incertidumbre
o: Construye un intervalo alrededor de la predicción usando el cuantil 0,90 de los residuos absolutos medidos en datos que el modelo no vio
o: Multiplica la predicción por 0,90 para quedarse en el lado conservador
a: 2
e: La conformal no toca la predicción puntual: la deja como está y le añade un margen hacia arriba y hacia abajo. Ese margen sale del cuantil alto de los residuos de calibración, no de su media, para que la cobertura se cumpla de verdad. Multiplicar por 0,90 no tiene nada que ver con la incertidumbre.
:::

:::quiz
p: Prometes un intervalo al 95 % y en las últimas 200 predicciones el valor real cayó dentro 150 veces. ¿Qué ha pasado?
o: La cobertura es 95 %, porque 150 es más de la mitad
o: La cobertura real es el 75 %, muy por debajo de lo prometido: el margen del intervalo se quedó corto
o: El intervalo es demasiado ancho y hay que estrecharlo
a: 2
e: 150 de 200 es 0,75. El intervalo cubre menos de lo que promete, así que es demasiado estrecho: hay que ensancharlo. Ocurre casi siempre por calibrar con los datos de entrenamiento o por suponer normalidad cuando los errores tienen cola gorda. Que sea ancho o estrecho no se decide a ojo: se mide así.
:::

:::quiz
p: ¿Por qué en la predicción conforme se divide el residuo entre la predicción antes de calcular el cuantil?
o: Para que el intervalo sea proporcional al tamaño de la predicción, que es como se comporta el error en muchos problemas
o: Para que el cuantil salga siempre entre 0 y 1
o: Para eliminar los valores atípicos de la calibración
a: 1
e: Si el error absoluto crece con el nivel (vendes más y el error en unidades crece, pero en porcentaje no), normalizar lo hace constante y el intervalo final sale proporcional. No es una transformación para acotar el cuantil ni para limpiar atípicos: de hecho, los residuos grandes siguen ahí y siguen empujando `q` hacia arriba.
:::

:::practica
enunciado: Tienes ocho predicciones con sus valores reales. Los residuos absolutos, en unidades, son 3, 5, 5, 7, 9, 9, 12 y 20. Calcula el intervalo al 75 % para una predicción nueva de 200 si calibras sin normalizar, y decide qué cobertura crees que se cumplirá en producción si el error crece con el nivel de la predicción.
pista: Con 8 residuos y nivel 0,75, la posición del cuantil es 0,75 por 9 = 6,75, así que con el redondeo hacia arriba tomas el séptimo valor.
solucion: Ordenados: 3, 5, 5, 7, 9, 9, 12, 20. El séptimo es 12, así que q = 12 y el intervalo es 200 ± 12 = [188, 212]. Si en realidad el error crece con el nivel de la predicción (al vender más, el error absoluto sube), este intervalo será demasiado estrecho para las predicciones grandes y demasiado ancho para las pequeñas; la cobertura global podría salir cerca del 75 % mientras falla por tramos. La solución es normalizar: dividir cada residuo entre su predicción, calcular el cuantil de esos cocientes y construir el intervalo como 200 · (1 ± q).
:::

:::trampa
Un intervalo estrecho no es un intervalo bueno. Si calibras el margen con los mismos datos que usaste para entrenar el modelo, los residuos salen artificialmente pequeños, el intervalo sale precioso y estrecho, y en producción el real se escapa constantemente por los lados. Antes de presumir de precisión, mide la cobertura en datos que el modelo no ha visto.
:::
