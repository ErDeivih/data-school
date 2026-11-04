---
id: spark-particiones-y-shuffle
titulo: Spark: particiones y shuffle
fase: 4
nivel: experto
rutas: [de]
prerequisitos: [spark-fundamentos, particionado-y-clustering, parquet-avro-orc]
tags: [spark, shuffle, particiones, rendimiento]
resumen: El shuffle reescribe y reordena todos los datos entre ejecutores; es la operación más cara de Spark y decide si un trabajo tarda minutos u horas.
fuentes: ["Karau y Warren (2017), 'High Performance Spark'", "Chambers y Zaharia (2018), 'Spark: The Definitive Guide'"]
---

## En una frase

El shuffle es el momento en que Spark deja de procesar cada fila donde está y reordena todo el
conjunto por clave entre máquinas: serializa, escribe en disco, transfiere por red y vuelve a
leer, y por eso es la operación que domina el tiempo de casi cualquier trabajo real.

## La idea

Piensa en repartir una baraja entre cuatro jugadores. Mientras barajas y repartes cartas
consecutivas, cada jugador trabaja con lo que le toca y nadie habla con nadie: es rapidísimo.
Pero si el juego exige que cada jugador tenga **todas** las cartas de un mismo palo, hay que
parar, mirar carta a carta, agrupar por palo y volver a repartir. Ese segundo reparto es el
shuffle, y su coste no está en pensar, sino en mover las cartas.

Formalmente, Spark distingue dos tipos de dependencia entre etapas:

- **Estrecha** (*narrow*): cada partición de salida depende de una sola partición de entrada.
  Un `filter`, un `select` o un `withColumn` no necesitan saber nada de las demás particiones.
  No hay comunicación entre ejecutores: cada uno hace su parte y ya está.
- **Amplia** (*wide*): cada partición de salida depende de **muchas** particiones de entrada.
  Un `groupBy`, un `join` por clave, un `distinct` o un `orderBy` necesitan que todas las filas
  de una misma clave acaben en el mismo sitio. Ahí aparece el **intercambio** (*exchange*) y con
  él el shuffle.

¿Por qué cuesta tanto? Porque el dato hace un viaje completo: se serializa (formato binario),
se escribe en ficheros temporales del disco local del ejecutor, se transfiere por la red al
ejecutor que le toca, se deserializa y se vuelve a agregar. Todo eso ocurre con un volumen
igual o mayor que el de entrada, porque Spark escribe **ambos lados**: el mapa (lo que cada
ejecutor manda) y el reduce. Es habitual ver un shuffle de 200 GB de escritura para agregar
100 GB de datos.

De ahí sale la regla que más tiempo ahorra en la práctica: **cuenta los shuffles de tu plan
antes de tocar nada más**. Si tu trabajo tiene cuatro `groupBy` encadenados, tienes cuatro
viajes completos de ida y vuelta por la red, y ninguna optimización de CPU te va a salvar de
ellos.

## Definición formal

Sea un conjunto de `N` filas de `b` bytes cada una, repartido en `P` particiones de entrada, y
un `groupBy` por una clave `k`.

- **Particionado por hash:** cada fila va a la partición `hash(k) mod P_salida`. Garantiza que
  todas las filas de la misma clave caen juntas, que es lo que permite agregar.
- **Particionado por rango:** usado por `orderBy` y por los joins ordenados; reparte por
  intervalos de clave ordenada y necesita muestrear los datos antes.
- **Particionado round-robin:** reparte por turnos, sin mirar la clave. Sirve para paralelizar
  cuando la clave no importa.
- **Shuffle write / shuffle read:** bytes que cada tarea de mapa escribe y que cada tarea de
  reducción lee. La suma de ambos es el tráfico de red del trabajo.
- **Spill:** cuando la memoria reservada para el shuffle se llena, Spark vuelca a disco. Un
  spill grande multiplica el tiempo porque convierte una operación de memoria en una de disco.

:::formula
filas barajadas ≈ N  ·  (1 − reducción por agregación parcial)
tamaño de shuffle ≈ filas barajadas · b
desviación de una tarea = máximo de bytes por partición ÷ media de bytes por partición
:::

La **agregación parcial** (el *map-side combine*) es la única reducción gratuita: si la clave
tiene poca cardinalidad, cada tarea de mapa puede agregar lo suyo antes de enviar y el shuffle
se reduce a una fila por clave distinta. Si la clave es un identificador de usuario, no reduce
nada.

La **desviación** es la métrica que importa de verdad. Un trabajo no termina cuando acaba la
tarea media: termina cuando acaba la última. Una desviación de 10 significa que, con 200
tareas, estás pagando 200 tareas para que 199 esperen a una.

## Ejemplo

Con **200 millones de filas** de **100 bytes** y solo las columnas que se barajan, el volumen
total es de **20 GB**. El plan pide un `groupBy` por distintas claves, con **200 particiones**
de shuffle.

| Clave | Cardinalidad | Filas barajadas | Shuffle |
| --- | --- | --- | --- |
| país | 200 | 40.000 | 0,004 GB |
| ciudad | 50.000 | 10.000.000 | 1 GB |
| usuario | 20.000.000 | 200.000.000 | 20 GB |

La razón es la agregación parcial. Con 200 países, cada una de las 200 tareas de mapa emite como
mucho 200 filas agregadas: 40.000 filas en total. Con 20 millones de usuarios, cada tarea emite
una fila por usuario distinto que le haya tocado, y eso es prácticamente una fila por fila de
entrada: no hay reducción ninguna y se barajan los 20 GB completos.

Y no todos los shuffle cuestan lo mismo en tiempo. Con un enlace de 10 Gbit/s por máquina
(1,25 GB/s teóricos, en la práctica bastante menos), mover 20 GB de shuffle **write** más 20 GB
de **read** son 40 GB: del orden de un minuto solo en tráfico de red, antes de contar
serialización, disco y agregación. Con los 0,004 GB del primer caso, el shuffle es
irrelevante.

El segundo número que hay que mirar es el reparto entre las 200 tareas. Si la clave
`usuario` incluye un valor centinela (por ejemplo, `"desconocido"`) con el 20 % de las filas,
esa partición recibe 40 millones de filas y 4 GB mientras la media son 1.000.000 de filas y
100 MB: desviación 40. La tarea tarda minutos, las otras 199 terminan en segundos, y el trabajo
dura lo que la lenta. Ese caso concreto tiene su propia página:
[[spark-joins-y-skew|uniones y asimetría]].

## Código

```python verificable
# Cuanto se reduce el shuffle segun la cardinalidad de la clave, con agregacion parcial.
filas = 200_000_000
bytes_por_fila = 100
particiones = 200

def barajado(filas, cardinalidad, particiones, bytes_por_fila):
    # El lado del mapa emite como mucho una fila por clave distinta y particion,
    # y nunca mas filas que las de entrada.
    claves_por_particion = min(cardinalidad, filas / particiones)
    filas_barajadas = min(filas, claves_por_particion * particiones)
    return filas_barajadas, filas_barajadas * bytes_por_fila / 1e9

for nombre, card in [("pais", 200), ("ciudad", 50_000), ("usuario", 20_000_000)]:
    n, gb = barajado(filas, card, particiones, bytes_por_fila)
    print(f"{nombre:<8} cardinalidad {card:>9,} -> {n:>12,.0f} filas, {gb:>8.4f} GB barajados")
```

```python verificable
# El tamano de particion manda: la misma tarea, con tres configuraciones distintas.
shuffle_gb = 20
for p in (8, 200, 10_000):
    mb = shuffle_gb * 1024 / p
    print(f"{p:>6} particiones -> {mb:>10,.1f} MB por tarea")
```

```python ilustrativo
from pyspark.sql import functions as F

# El plan por defecto con 200 particiones de shuffle para 20 GB: 100 MB por tarea.
# Ni malo ni bueno: depende del tamano de la tarea y de la memoria del ejecutor.
spark.conf.set("spark.sql.shuffle.partitions", "800")
ventas.groupBy("pais").agg(F.sum("importe")).explain()

# repartition hace un shuffle completo; coalesce solo fusiona particiones locales
# (no arregla el sesgo, pero evita el viaje de red cuando solo quieres menos ficheros).
ventas.repartition(800, "pais").write.parquet("s3://lago/plata/ventas_por_pais/")
ventas.coalesce(20).write.parquet("s3://lago/oro/resumen/")

# Con AQE activado (por defecto desde Spark 3.2), Spark fusiona particiones
# pequenas al final de cada etapa y evita el clasico "200 tareas de 100 KB".
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
```

## Errores típicos

- **Dejar `spark.sql.shuffle.partitions` en su valor por defecto de 200 con volúmenes grandes.**
  Con 5 TB de shuffle son 25 GB por tarea: cada tarea desborda a disco varias veces y el
  trabajo se arrastra. Regla práctica: apunta a **100-200 MB por tarea** de shuffle y ajusta el
  número en consecuencia.
- **Subir las particiones a 10.000 «para ir más rápido» con datos pequeños.** Con 2 GB de
  shuffle son 200 KB por tarea: el tiempo se va en planificar, serializar y arrancar 10.000
  tareas, no en hacer el trabajo. El número de particiones se elige por tamaño de tarea.
- **Usar `repartition(1)` para dejar un solo fichero de salida.** Todo el resultado pasa por un
  único ejecutor, que a partir de cierto tamaño se queda sin memoria. Para reducir el número de
  ficheros se usa `coalesce` o, mejor, se acepta que el lago tenga muchos ficheros y se controla
  el tamaño con [[particionado-y-clustering|particionado por columnas]].
- **Confundir `coalesce` con `repartition`.** `coalesce(n)` fusiona particiones sin mover datos
  por la red, así que no puede repartir mejor las claves ni arreglar el sesgo.
  `repartition(n, clave)` sí hace un shuffle completo y sí reparte por clave, a cambio de
  pagarlo.
- **Hacer `orderBy` por costumbre.** Ordenar es un shuffle por rango que además necesita
  muestrear los datos. Si el orden solo importa dentro de cada grupo, `Window.partitionBy(...)`
  sobre una clave ya particionada es mucho más barato que un `orderBy` global.
- **Cachear antes de un shuffle creyendo que lo evita.** `cache()` guarda el resultado de la
  etapa anterior en memoria, pero el shuffle posterior sigue ocurriendo igual cada vez que se
  dispare una acción. Lo que se evita es releer y recalcular lo de antes, no el intercambio.

## Comprueba que lo sabes

:::quiz
p: Un `groupBy` por una columna de 20 millones de usuarios distintos y otro por una de 200 países, sobre 200 millones de filas. ¿Cuál baraja menos datos y por qué?
o: El de países, porque la agregación parcial en el lado del mapa reduce cada partición a 200 filas agregadas
o: El de usuarios, porque hay más valores y se reparten mejor entre particiones
o: Los dos barajan lo mismo: el volumen de shuffle solo depende del número de filas
a: 1
e: Con pocas claves distintas, cada tarea de mapa puede agregar antes de enviar y emite una fila por clave, no por fila de entrada. Con 20 millones de claves distintas, casi ninguna fila se puede agregar antes de enviarla y se baraja el conjunto completo.
:::

:::quiz
p: Un trabajo con 200 tareas de shuffle tiene una media de 100 MB por tarea, pero la mayor recibe 4 GB y tarda 12 minutos; el resto termina en 20 segundos. ¿Qué está pasando?
o: Falta memoria en los ejecutores y por eso solo una tarea va lenta
o: Sesgo de claves: una clave concentra muchísimas filas y su partición se lo come todo; el trabajo dura lo que la tarea lenta
o: El número de particiones es demasiado alto y hay que bajarlo a 20
a: 2
e: Spark termina un trabajo cuando termina la última tarea, no la media. Reducir el número de particiones no reparte la clave caliente, solo empeora el resto. La solución es repartir esa clave (salting) o dejar que AQE divida la partición sesgada.
:::

:::aviso
El shuffle se paga en disco, red y CPU, y además **se escribe dos veces**: una el lado del mapa
y otra el lado de la reducción. Cuando compares dos versiones de un trabajo, no mires solo el
tiempo: mira en la interfaz de Spark los bytes de *shuffle write* y *shuffle read*, el *spill*
en disco y la diferencia entre la tarea más lenta y la mediana. Esos cuatro números explican
casi todo.
:::
