---
id: lambda-y-kappa
titulo: Arquitecturas lambda y kappa
fase: 4
nivel: avanzado
rutas: [de]
prerequisitos: [batch-vs-streaming, kafka-y-colas, data-lake]
tags: [arquitectura, streaming, lotes, tiempo-real]
resumen: Dos formas de resolver «lote y tiempo real»: lambda mantiene dos caminos que hay que reconciliar, kappa uno solo que se reprocesa desde el registro.
fuentes: ["Marz y Warren (2015), 'Big Data: Principles and best practices of scalable realtime data systems'", "Kreps (2014), 'Questioning the Lambda Architecture'"]
---

## En una frase

Lambda construye la misma respuesta dos veces —una lenta y exacta sobre todo el histórico, otra
rápida y aproximada sobre lo reciente— y las suma al servir; kappa construye la respuesta una
sola vez con el motor de flujo y, cuando hay que corregir el pasado, vuelve a leer el registro
desde el principio.

## La idea

Volvamos al problema que las dos intentan resolver. Tienes que responder a «¿cuánto hemos
vendido hoy?» y tienes dos fuentes de dolor:

- Procesar el histórico completo es **exacto** pero tarda horas. Sirve para el informe de cierre
  de mes, no para el panel que mira el responsable de tienda a las once de la mañana.
- Procesar solo el flujo reciente es **rápido** pero está condenado a estar algo mal, porque los
  datos llegan tarde, desordenados y a veces repetidos. Sirve para el panel, no para el cierre.

**Lambda** (Marz) acepta ese reparto tal cual y lo convierte en arquitectura de tres capas:

1. **Capa de lote:** un dato maestro inmutable con todo el histórico. Cada noche (o cada hora) se
   recalcula la vista completa desde cero. Es la verdad, y es lenta.
2. **Capa de velocidad:** un motor de flujo que cubre solo la ventana reciente, la que el lote
   todavía no ha procesado. Es incremental y rápida.
3. **Capa de servicio:** al consultar, se suma la vista del lote más la de velocidad. El panel
   ve el resultado correcto sin esperar al cierre.

Su promesa es sólida: el lote siempre puede rehacer la verdad, y la velocidad solo tiene que
cubrir el hueco. Su problema es igual de sólido: **la misma lógica de negocio está escrita dos
veces**, en dos lenguajes y dos motores distintos. Y todo el mundo sabe qué pasa cuando dos
implementaciones de la misma regla viven separadas: divergen. Un `>=` que en un sitio es `>` en
el otro, una zona horaria distinta, un redondeo a distinto número de decimales. Nadie lo nota
hasta que el panel y el informe no cuadran.

**Kappa** (Kreps) empieza por la pregunta incómoda: si el motor de flujo puede reprocesar el
histórico entero a suficiente velocidad, ¿para qué quieres el segundo camino? El registro de
eventos (*log*) pasa a ser la fuente de verdad, y la única función de procesamiento se aplica
tanto al presente como al pasado:

- **Una sola ruta de código.** La regla de negocio se escribe una vez.
- **Reproceso = releer el log** desde el principio (o desde un punto de control) con el mismo
  motor. Corregir un error del pasado no es «volver a ejecutar el proceso por lotes»: es
  reejecutar el mismo proceso sobre el mismo registro.
- **Condición innegociable:** el log tiene que retenerse lo suficiente y el motor tiene que
  poder leer el histórico **más rápido de lo que se produjo**. Si tardas seis horas en reprocesar
  un día de eventos, kappa no es viable con ese motor.

La consecuencia práctica es que la decisión no es de gusto, es de requisitos. Necesitas lambda
cuando ya tienes un proceso por lotes que funciona y no puedes permitirte pararlo; eliges kappa
cuando puedes permitirte que **todo** pase por el flujo y estás dispuesto a mantener el registro
con la retención y la capacidad de reproceso que exige.

:::trampa
«Kappa es lambda sin capa de lote» es una simplificación peligrosa y falsa: kappa sí procesa el
histórico, lo que hace es procesarlo con el mismo motor y en el mismo camino. Si te quedas sin
poder reprocesar el histórico (porque el log solo retiene siete días y no tienes ficheros
históricos), no tienes kappa: tienes un flujo que no se puede corregir.
:::

## Definición formal

Sea `E = e₁, e₂, …, eₙ` la secuencia de eventos con marca de **tiempo de evento** (cuándo
ocurrieron, no cuándo se procesaron) y `f` una función de agregación.

- **Lambda:** dos funciones, `f_lote` sobre el histórico completo y `f_flujo` sobre la ventana
  reciente. La respuesta servida en el instante `t` es la combinación de ambas:
  `resultado(t) = f_lote(E hasta T_cierre) ⊕ f_flujo(E desde T_cierre)`.
  `⊕` es la operación que fusiona las dos vistas (suma, unión, máximo). Condición de
  corrección: `f_lote ≡ f_flujo` en su solapamiento, es decir, las dos implementaciones deben
  coincidir donde se pisan.
- **Kappa:** una sola función `f` aplicada al log completo, con **semántica de tiempo de
  evento** y **procesamiento determinista**. Reprocesar es recalcular `f(E)` sobre un prefijo
  distinto del log.
- **Entrega:** *at-least-once* (un evento puede procesarse más de una vez) o *exactly-once*
  (una sola vez de cara al resultado). Con *at-least-once*, `f` tiene que ser **idempotente** o
  llevar claves que permitan descartar duplicados; si no, cada reproceso infla los totales.
- **Watermark / marca de agua:** declaración de hasta cuándo se espera por eventos tardíos antes
  de cerrar una ventana. Define cuánto tiempo puedes corregir una cifra ya publicada.

:::formula
lambda:  resultado = f_lote(histórico) ⊕ f_flujo(reciente)
kappa:   resultado = f(log completo)     con f determinista
:::

## Ejemplo

Un millón de eventos en un mes, **30 días** y unos 33.300 eventos diarios, con un **0,4 %** que
llega con retraso (cuatro de cada mil, uno o dos días después de ocurrir).

- El **total del mes** coincide en los dos caminos: nada se pierde, solo se coloca en el sitio
  equivocado.
- Pero **29 de los 30 días** muestran cifras distintas entre `f_lote` y `f_flujo`, porque cada
  evento tardío se contó el día en que llegó.
- El error relativo máximo de un día es del **0,41 %** sobre el día con menos eventos.

Ese 0,41 % es exactamente el tamaño del problema de lambda: es **demasiado pequeño para
detectarlo a ojo** y **suficiente para que dos informes que deberían cuadrar no cuadren**. Nadie
abre una incidencia por 0,41 %, pero alguien pierde una tarde explicando por qué el panel y el
cierre dicen cosas distintas. La solución en lambda es comparar los dos caminos todos los días y
alertar por encima de un umbral; en kappa, el problema no existe porque no hay dos caminos que
comparar.

Y hay un segundo coste, menos visible: dos caminos significan dos conjuntos de código, dos
despliegues, dos esquemas de datos, dos turnos de guardia y dos formas de que algo se rompa a
las tres de la mañana.

## Código

```python verificable
# Reconciliacion lote contra flujo: los totales cuadran, los dias no.
import numpy as np

rng = np.random.default_rng(0)
dias = 30
ocurridos = rng.poisson(33_333, size=dias)      # eventos que ocurrieron cada dia
tarde = rng.binomial(ocurridos, 0.004)          # 4 por mil llegan con retraso
tarde[-1] = 0        # los del ultimo dia todavia no han llegado al cerrar

flujo = ocurridos - tarde
flujo[1:] += tarde[:-1]                         # cada tardio se cuenta al dia siguiente

dif = np.abs(flujo - ocurridos)
print(f"total en lote  {ocurridos.sum():,}")
print(f"total en flujo {flujo.sum():,}")
print(f"dias con diferencia   {(dif > 0).sum()} de {dias}")
print(f"error relativo maximo {dif.max() / ocurridos.min():.2%}")
```

```python ilustrativo
# Lambda: dos caminos, la misma regla escrita dos veces (aqui, en dos sitios).
# Camino de lote, cada noche, sobre todo el historico.
(spark.read.parquet("s3://lago/bronce/eventos/")
      .groupBy("fecha", "pais").agg(F.sum("importe").alias("total"))
      .write.mode("overwrite").parquet("s3://lago/oro/ventas_lote/"))

# Camino de flujo, con marca de agua para admitir eventos tardios.
(flujo.readStream
      .withWatermark("ts_evento", "2 days")
      .groupBy(F.window("ts_evento", "1 day"), "pais")
      .agg(F.sum("importe").alias("total"))
      .writeStream.outputMode("update")
      .option("checkpointLocation", "s3://lago/_chk/ventas")
      .foreachBatch(escribir_en_servicio))

# Kappa: la MISMA consulta, aplicada al log completo cuando hay que reprocesar.
eventos = flujo.read.format("kafka").option("startingOffsets", "earliest").load()
agregado = eventos.groupBy("fecha", "pais").agg(F.sum("importe"))
agregado.write.mode("overwrite").parquet("s3://lago/oro/ventas/")   # un solo camino
```

## Errores típicos

- **Escribir la lógica dos veces y no compararla nunca.** Si eliges lambda, la reconciliación no
  es opcional: programa una comprobación diaria que compare `f_lote` y `f_flujo` en su
  solapamiento y alerte por encima de un umbral (el 0,1 % es un punto de partida razonable).
  Sin esa comprobación, la divergencia es cuestión de tiempo.
- **Llamar kappa a «solo streaming» sin poder reprocesar.** Si el log retiene siete días y no
  guardas histórico, un error de hace un mes es irrecuperable. Kappa exige retención suficiente,
  puntos de control y capacidad de releer el histórico más deprisa de lo que se generó.
- **Usar el tiempo de proceso en vez del tiempo de evento.** Si agendas la ventana por la hora a
  la que llegó el mensaje, un evento de ayer que llega hoy cae en el día equivocado. Todas las
  ventanas y marcas de agua van sobre `ts_evento`, y el tiempo de proceso solo sirve para
  diagnosticar retrasos.
- **Ignorar la semántica de entrega.** Con *at-least-once*, cada reintento o reproceso vuelve a
  sumar el mismo evento. Sin claves de deduplicación o sin escritura idempotente, los totales
  crecen con cada incidencia, y encima de forma silenciosa.
- **Elegir lambda «por si acaso» sin necesitar tiempo real.** Si el negocio se conforma con un
  informe cada hora, no necesitas una capa de velocidad: necesitas un proceso por lotes que
  corra cada hora. Pagar dos arquitecturas para un requisito de latencia que no existe es la
  forma más cara de complicarse.
- **Confundir latencia con frescura.** «Tiempo real» de cinco minutos, de cinco segundos y de
  cinco milisegundos son tres sistemas distintos, con costes que se diferencian en órdenes de
  magnitud. Fija el número con el consumidor antes de elegir arquitectura; ver
  [[streaming-tiempo-real|ventanas y marcas de agua]] y [[batch-vs-streaming|lotes frente a flujo]].

## Comprueba que lo sabes

:::quiz
p: En un sistema lambda, el panel en tiempo real y el informe de cierre dan cifras distintas para el mismo día. ¿Cuál es la causa más probable?
o: El motor de flujo pierde eventos y por eso da menos
o: Los dos caminos implementan la misma regla por separado y colocan los eventos tardíos en días distintos
o: El lote está mal calculado porque tiene menos datos
a: 2
e: Es el fallo característico de lambda: dos implementaciones de la misma lógica. Los eventos tardíos se cuentan el día en que llegan en el camino de flujo y el día en que ocurrieron en el de lote. El total del mes cuadra; lo que no cuadra es el reparto por días.
:::

:::quiz
p: ¿Qué condición tiene que cumplir un sistema para que kappa sea viable?
o: Que el motor de flujo pueda releer el histórico más rápido de lo que se generó y que la lógica sea determinista
o: Que no existan eventos tardíos en la fuente
o: Que el volumen diario quepa en memoria en una sola máquina
a: 1
e: Kappa sustituye la capa de lote por el reproceso del log: si releer el histórico tarda más que el tiempo que tardó en producirse, nunca alcanzas. Además la función debe ser determinista (y la entrega, idempotente) para que reprocesar dé el mismo resultado.
:::

:::aviso
Las dos arquitecturas comparten un requisito que es fácil de romper: **la fuente tiene que
poder reproducirse**. En lambda, el dato maestro inmutable; en kappa, el log con retención
suficiente. Si tu fuente es un sistema transaccional que solo guarda el estado actual y no los
cambios, ninguna de las dos te salva: sin
[[ingesta-incremental-y-cdc|ingesta incremental o CDC]] no hay historia que reprocesar.
:::
