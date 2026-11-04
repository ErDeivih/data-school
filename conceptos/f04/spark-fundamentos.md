---
id: spark-fundamentos
titulo: Spark: fundamentos
fase: 4
nivel: avanzado
rutas: [de, core]
prerequisitos: [data-lake, parquet-avro-orc, pandas-fundamentos]
tags: [spark, big-data, distribuido]
resumen: Un motor distribuido con evaluación perezosa: qué es un RDD, qué añade el DataFrame y por qué no es «Pandas en grande».
fuentes: ["Zaharia et al. (2016), 'Apache Spark: A Unified Engine for Big Data Processing'", "Armbrust et al. (2015), 'Spark SQL: Relational Data Processing in Spark'"]
---

## En una frase

Spark es un motor que reparte el trabajo entre muchas máquinas, no ejecuta nada hasta que
pides un resultado y planifica ese trabajo antes de mover un solo byte: por eso no se comporta
como Pandas, aunque su API se le parezca.

## La idea

Imagina una cocina de un restaurante grande. El jefe de cocina no cocina: escribe la receta
paso a paso (corta la cebolla, sofríe, añade el caldo). Los cocineros son los que ejecutan.
Mientras el jefe escribe la receta, en la cocina no se ha encendido ningún fuego. Solo cuando
el camarero grita «¡marchando mesa 4!» empieza todo de verdad.

Eso es la **evaluación perezosa** (*lazy evaluation*). En Spark, el jefe de cocina es el
**driver** (el proceso donde vive tu programa y donde se construye el plan) y los cocineros son
los **ejecutores** (procesos en las máquinas del clúster que hacen el trabajo real).

```
driver:  leer -> filtrar -> agrupar -> contar        <- aquí solo se construye un plan
                  (nada de esto se ejecuta todavía)
driver:  .show() / .count() / .write()               <- la acción dispara la ejecución
executores: reparten las particiones, hacen el trabajo, devuelven el resultado
```

`leer`, `filtrar` y `agrupar` son **transformaciones**: cada una devuelve un DataFrame nuevo,
que en realidad no contiene datos, solo la descripción de un paso. `count()` y `write()` son
**acciones**: piden un resultado materializado y obligan a ejecutar el plan completo.

¿Por qué molestarse en no ejecutar? Porque el plan completo se puede optimizar antes de
empezar. Si filtras y luego seleccionas dos columnas de un Parquet de 400 GB, Spark puede
decidir leer solo esas dos columnas y descartar el resto de las filas antes de mover nada de
disco. Ese optimizador se llama **Catalyst**, y solo puede trabajar si le dejas ver el plan
entero. Con Pandas no hay plan: cada línea se ejecuta al escribirla, sobre un único array en
memoria.

Y aquí está la trampa mental que hay que desactivar: **Spark no es «Pandas en grande»**.
Cuatro diferencias que cambian cómo se programa:

1. **Los datos no caben en una máquina y no hace falta que quepan.** Trabajas con una
   abstracción particionada; nunca tienes «el DataFrame entero» en tus manos.
2. **El coste dominante es mover datos por la red**, no hacer cuentas. Una operación trivial en
   Pandas (agrupar por clave) obliga en Spark a reordenar terabytes entre máquinas.
3. **Escribir Python dentro de Spark puede ser carísimo.** Las funciones nativas las entiende
   Catalyst; una UDF de Python obliga a serializar fila a fila y a sacar los datos del motor.
4. **Los errores aparecen tarde y lejos.** Una línea mal escrita en Pandas falla ahí mismo; en
   Spark se convierte en un plan que se rompe cinco minutos después, en una tarea concreta de
   un ejecutor concreto.

## Definición formal

Tres objetos, de más antiguo a más moderno:

- **RDD** (*Resilient Distributed Dataset*): colección **inmutable** de elementos, dividida en
  **particiones**, con un **linaje** que recuerda qué transformaciones la produjeron. «Resiliente»
  significa que si un ejecutor muere, Spark reconstruye su partición repitiendo el linaje; no
  hace falta replicar los datos.
- **DataFrame**: colección distribuida con **esquema** (nombres y tipos de columna) y
  **filas**. Por debajo sigue siendo un RDD de filas, pero Spark sabe qué columnas hay.
- **Dataset**: DataFrame con tipos comprobados en compilación. Solo existe en Scala y Java; en
  Python (PySpark) siempre trabajas con DataFrame, con o sin esquema explícito.

Vocabulario de ejecución:

- **Trabajo** (*job*): lo que dispara una acción.
- **Etapa** (*stage*): tramo del plan que se puede ejecutar sin mover datos entre particiones.
  El plan se corta en cada **dependencia amplia** (*wide dependency*), es decir, en cada
  operación que necesita reordenar datos por clave.
- **Tarea** (*task*): la unidad mínima, una partición procesada por un núcleo.

:::formula
etapas de un trabajo = 1 + número de dependencias amplias del plan
tareas = suma de particiones de todas las etapas
:::

Ninguna de esas dos cifras depende de cuántos datos tengas, sino de cuántas particiones y
cuántos cortes tenga tu plan. Ese es el primer sitio donde mirar cuando algo tarda demasiado.

## Ejemplo

Supón un Parquet de **400 GB** en la capa bronce, repartido en **200 particiones**, en un
clúster con 20 ejecutores de 4 núcleos (80 núcleos en total). Cada partición pesa 400 / 200 =
**2 GB**.

Tres planes distintos sobre los mismos datos:

1. `df.filter(importe > 100).select(fecha, importe).count()`. Todo son transformaciones
   estrechas (cada fila se decide sola), así que hay **1 etapa** con **200 tareas**. Se leen
   400 GB y se cuenta.
2. El mismo plan más `.mean()` para la media de `importe`. Sin `cache()`, la acción anterior y
   esta son dos **trabajos** independientes: Spark vuelve a leer los 400 GB desde disco. Total
   leído: **800 GB** para responder a dos preguntas sobre los mismos datos.
3. Añadiendo `.cache()` antes de la primera acción, los 400 GB se leen una vez. Pero «cachear»
   significa guardar esas particiones en memoria de los ejecutores: si el clúster suma 200 GB
   de memoria disponible para almacenamiento, más de la mitad no cabe y Spark la recalcula o la
   deja caer a disco. El `cache()` sin comprobar la memoria es una promesa que no siempre se
   cumple.

Con 80 núcleos y 200 tareas, cada núcleo ejecuta 2 o 3 tareas: bien. Si el mismo clúster
tuviera 2.000 particiones, cada tarea haría 200 MB y el coste de planificar y arrancar 2.000
tareas empezaría a notarse; con 8 particiones, cada tarea tendría 50 GB y el trabajo moriría
por falta de memoria. El número de particiones es una decisión de ingeniería, no un detalle.

## Código

```python verificable
# Spark no cabe en este ejemplo, pero la pereza sí se puede reproducir.
datos = list(range(1, 1_000_001))
veces = {"filtro": 0, "map": 0}

def filtro(xs, cond):
    for x in xs:
        if cond(x):
            veces["filtro"] += 1     # solo se ejecuta al consumir el generador
            yield x

def doble(xs):
    for x in xs:
        veces["map"] += 1
        yield 2 * x

plan = doble(filtro(datos, lambda x: x % 7 == 0))
print("antes de la accion:", veces)     # -> antes de la accion: {'filtro': 0, 'map': 0}
total = sum(plan)                       # la accion recorre el plan entero, una sola vez
print("despues de la accion:", veces)   # -> despues de la accion: {'filtro': 142857, 'map': 142857}
print("suma:", total)                   # -> suma: 142857857142
```

Fíjate en el detalle: construir el plan no ejecutó ni una vuelta del bucle, y la acción recorrió
los datos **una sola vez**, encadenando las dos etapas. Eso es exactamente lo que hace Spark
entre etapas estrechas: fusionarlas en una sola pasada.

```python ilustrativo
# PySpark real: mismo estilo de API, ejecución en un cluster.
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = (SparkSession.builder
         .appName("ventas")
         .config("spark.sql.shuffle.partitions", "400")
         .getOrCreate())

ventas = spark.read.parquet("s3://lago/bronce/ventas/")   # todavia no lee nada

plan = (ventas
        .filter(F.col("importe") > 100)
        .select("fecha", "importe")
        .groupBy("fecha")
        .agg(F.sum("importe").alias("total")))

plan.explain(True)   # el plan logico y el fisico: aqui se ve donde hay intercambio
plan.show(5)         # esta accion es la que dispara la lectura de verdad
```

## Errores típicos

- **Creer que una transformación se ejecuta.** Poner `print(df.count())` entre dos
  transformaciones para «ver si va bien» lanza un trabajo completo y luego el plan sigue desde
  cero: has pagado dos veces por lo mismo. Para inspeccionar el plan se usa `explain()`, que no
  ejecuta nada.
- **Usar UDFs de Python para todo.** Una UDF recibe y devuelve datos fila a fila, fuera del
  motor: Catalyst no ve dentro de ella y no puede optimizarla. Usa `pyspark.sql.functions`
  (que es lo mismo, pero en el motor) y reserva las UDF para lo que de verdad no exista.
- **Llamar a `collect()` o `toPandas()` «para mirar».** Esas dos traen todos los datos al
  driver: con 2 GB se cae la memoria del driver, no la del clúster. Para echar un vistazo,
  `show(20)` o `take(20)`.
- **Programar bucles sobre filas.** `for fila in df.collect()` es la forma más rápida de
  destruir el paralelismo: primero materializas todo en una máquina y luego lo recorres en
  serie. Piensa en columnas y en expresiones.
- **Ignorar el número de particiones.** Dejar el valor por defecto cuando el volumen cambió
  (o dejar `spark.sql.shuffle.partitions=200` con terabytes) genera tareas de gigabytes. Se
  ajusta; ver [[spark-particiones-y-shuffle|particiones y shuffle]].
- **Tratar el clúster como una máquina más rápida.** Un `groupBy` sobre 5 TB no es «un poco más
  lento» que en Pandas: es un intercambio de datos completo por la red. Si el dato cabe en un
  portátil, [[duckdb-y-analitica-local|DuckDB]] o [[polars|Polars]] te darán la respuesta antes
  y con menos piezas.

## Comprueba que lo sabes

:::quiz
p: ¿En qué momento lee Spark los datos de un `read.parquet(...)` seguido de dos `filter`?
o: Al construir el DataFrame, porque `read` es una acción
o: Cuando se pide una acción como `count()` o `write()`, porque las transformaciones solo construyen el plan
o: En el momento en que se llama a `explain()`, que ejecuta el plan para medirlo
a: 2
e: `read` y `filter` son transformaciones perezosas: devuelven un plan, no datos. La lectura ocurre cuando una acción pide un resultado materializado. `explain()` solo imprime el plan, no lo ejecuta.
:::

:::quiz
p: Un plan tiene un `select` (estrecho) y dos `groupBy` (amplios). ¿Cuántas etapas tiene el trabajo?
o: 1, porque Spark fusiona todo lo que puede
o: 3, porque cada dependencia amplia corta el plan en una etapa nueva
o: 6, porque cada etapa se cuenta dos veces
a: 2
e: El plan se corta en cada dependencia amplia: dos `groupBy` son dos cortes, así que quedan 1 + 2 = 3 etapas. Las transformaciones estrechas consecutivas sí se fusionan en la misma etapa.
:::

:::trampa
Un trabajo que «tarda mucho» casi nunca se arregla cambiando el código de transformación: se
arregla mirando el plan. Empieza por `explain()` y por el reparto de duración entre tareas. Si
una tarea tarda diez veces más que la mediana, el problema es el reparto de datos, no la
lógica.
:::
