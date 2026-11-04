---
id: spark-joins-y-skew
titulo: Spark: uniones y asimetría
fase: 4
nivel: experto
rutas: [de]
prerequisitos: [spark-fundamentos, spark-particiones-y-shuffle, sql-joins]
tags: [spark, joins, skew, rendimiento]
resumen: Unir tablas reparte claves entre tareas; cuando una clave concentra media tabla, esa tarea decide cuánto tarda el trabajo y hay que repartirla.
fuentes: ["Chambers y Zaharia (2018), 'Spark: The Definitive Guide'", "Karau y Warren (2017), 'High Performance Spark'"]
---

## En una frase

Una unión en Spark obliga a que las filas de la misma clave se encuentren en la misma tarea, así
que si una clave aparece millones de veces mientras el resto se reparte bien, el trabajo entero
dura lo que dura esa única tarea insoportablemente grande.

## La idea

Imagina que organizas una cena para 400 mesas y quieres que en cada mesa se sienten juntos los
invitados que comparten apellido. Reparte a la gente por apellido entre las 400 mesas y todo
funciona: cada mesa tiene un puñado de «García», un puñado de «López» y así. Pero hay 48.000
personas que se apellidan «Pérez» y todas van a la misma mesa. Da igual lo bien repartidas que
estén las otras 399: la cena no empieza hasta que la mesa de los Pérez acabe de sentarse.

Eso es el **sesgo de claves** (*skew*). Y lo importante es que no es un problema de volumen:
es un problema de **reparto**. Un `join` entre 10 GB y 100 MB sin sesgo vuela. Un `join` entre
100 MB y 10 MB con una clave repetida 40 millones de veces se arrastra durante horas.

Spark tiene dos familias de unión, y elegir bien es la mitad del trabajo:

**Unión por difusión** (*broadcast join*). Si una de las dos tablas es pequeña, Spark la copia
entera a cada ejecutor y cada tarea une su partición de la tabla grande contra esa copia en
memoria. No hay shuffle de la tabla grande: no hay red, no hay disco temporal, no hay espera.
El límite lo pone `spark.sql.autoBroadcastJoinThreshold`, cuyo valor por defecto es 10 MB
(10.485.760 bytes). Por debajo de eso, Spark lo hace solo; por encima, hay que pedirlo
explícitamente y saber lo que se hace.

**Unión por ordenación y mezcla** (*sort-merge join*). Cuando las dos tablas son grandes,
Spark baraja ambas por la clave de unión, las ordena y las recorre en paralelo. Es la opción
general y la que sufre con el sesgo: las filas de una clave repetida caen todas en la misma
partición de la misma etapa.

Hay una tercera vía que casi nadie considera y que muchas veces gana: si una de las tablas es
pequeña pero supera el umbral, **filtrarla antes de unir**. Unir 2 TB contra 400 MB cuando solo
necesitas las filas de 12 provincias es un desperdicio; filtra primero y la tabla pequeña baja
por debajo del umbral de difusión.

## Definición formal

Sean dos tablas `A` (grande, `n_A` filas) y `B` (pequeña, `n_B` filas) unidas por la clave `k`.

- **Difusión:** `B` se materializa como un mapa hash *hash table* en cada ejecutor. Coste:
  `n_B · b_B` bytes enviados a cada ejecutor, es decir `n_B · b_B · E` en total, con `E` el
  número de ejecutores. No hay shuffle de `A`. Complejidad por tarea: `O(n_A / P)` con una
  búsqueda en el mapa por fila.
- **Ordenación y mezcla:** ambas tablas se barajan por `hash(k) mod P`. Coste:
  `(n_A · b_A + n_B · b_B)` bytes barajados, más ordenación. Complejidad por tarea:
  `O((n_A + n_B) / P · log(...))` si el reparto es uniforme.
- **Factor de sesgo** de una partición: `bytes de la partición ÷ mediana de bytes por partición`.
- **Salting:** se transforma la clave en `k' = (k, s)` con `s ∈ {0, …, S−1}` elegido al azar.
  Para que la unión siga siendo correcta, **el otro lado se replica `S` veces**, una por cada
  valor de `s`.

:::formula
coste del peor caso ≈ máx(partición) · coste unitario
salting: partición mayor ÷ S  +  |B| · S replicado
:::

El salting es un intercambio, no un regalo: repartes la clave caliente a cambio de multiplicar
por `S` el tamaño del lado pequeño. Si el lado pequeño no es pequeño, el remedio es peor que la
enfermedad. La cuenta que hay que hacer antes de aplicarlo es exactamente la de la fórmula.

## Ejemplo

Un `join` entre una tabla de **120 millones de eventos** (`A`) y una tabla de dimensión pequeña
(`B`), por la clave `dispositivo`. **48 millones de eventos (el 40 %)** tienen la misma clave,
porque son de un dispositivo con identificador centinela (`"desconocido"` o `NULL`). El shuffle
usa **400 particiones**.

Sin salting:

- Tamaño medio de partición: 120.000.000 / 400 = **300.000 filas**.
- Partición de la clave caliente: 48.000.000 + 180.000 = **48.180.000 filas**.
- Factor de desequilibrio: 48.180.000 / 300.000 = **160,6×**.

Esa única tarea tarda del orden de 160 veces más que la media. Con 400 tareas en 80 núcleos,
las otras 399 van terminando y el clúster se queda casi vacío esperando a una sola.

Con **salting en 64 trozos** (`S = 64`) y replicando `B` 64 veces:

- Partición más grande: 48.000.000 / 64 + 180.000 = **930.000 filas**.
- Mejora del peor caso: 48.180.000 / 930.000 = **51,8×**.
- Precio: si `B` ocupa 20 MB, la réplica ocupa 64 · 20 MB = **1,28 GB** repartidos entre los
  ejecutores. Sigue siendo barato comparado con la espera.

Y la alternativa que suele ser mejor que el salting: si esos 48 millones de filas con clave
centinela no van a unir con nada (porque `"desconocido"` no está en la tabla de dispositivos),
**sepáralas antes**: une solo las filas con clave válida y añade las demás después con un
`union`. El sesgo desaparece porque lo has sacado del `join`.

## Código

```python verificable
# Cuanto mejora el peor caso con salting, y cuanto cuesta la replica del lado pequeno.
filas = 120_000_000
caliente = 48_000_000          # una sola clave concentra el 40 % de las filas
particiones = 400
resto_por_tarea = (filas - caliente) / particiones

peor_sin = caliente + resto_por_tarea
media = filas / particiones
print(f"tarea media             {media:>12,.0f} filas")
print(f"peor tarea sin salting  {peor_sin:>12,.0f} filas")
print(f"factor de desequilibrio {peor_sin / media:>12.1f}x")

trozos = 64
peor_con = caliente / trozos + resto_por_tarea
print(f"peor tarea con salting  {peor_con:>12,.0f} filas")
print(f"mejora del peor caso    {peor_sin / peor_con:>12.1f}x")

mb_dimension = 20
print(f"replica del lado pequeno {mb_dimension * trozos:>11,} MB")
```

```python ilustrativo
from pyspark.sql import functions as F

# 1. Difusion explicita: B tiene 8 MB, cabe de sobra en el umbral de 10 MB.
eventos.join(F.broadcast(dispositivos), on="dispositivo", how="left")

# 2. Si B crece por encima del umbral, Spark hara sort-merge join y barajara los dos lados.
eventos.join(dispositivos, on="dispositivo", how="left").explain()

# 3. Salting: repartimos la clave caliente y replicamos el lado pequeno 64 veces.
S = 64
eventos_sal = eventos.withColumn("sal", (F.rand(seed=0) * S).cast("int"))
dispositivos_sal = (dispositivos
                    .withColumn("sal", F.explode(F.array([F.lit(i) for i in range(S)]))))
unido = eventos_sal.join(dispositivos_sal, on=["dispositivo", "sal"], how="left")

# 4. La solucion mas simple: sacar del join las filas que no unen con nada.
validos = eventos.filter(F.col("dispositivo") != "desconocido")
sueltos = eventos.filter(F.col("dispositivo") == "desconocido")
resultado = validos.join(F.broadcast(dispositivos), on="dispositivo", how="left").unionByName(sueltos, allowMissingColumns=True)
```

## Errores típicos

- **Subir `spark.sql.autoBroadcastJoinThreshold` a 1 GB «para que sea más rápido».** La tabla
  pequeña la recoge el **driver** y la envía a cada ejecutor: con 1 GB, el driver se queda sin
  memoria o el arranque de todas las tareas se eterniza. El umbral se sube con conocimiento del
  tamaño real, no por si acaso.
- **Unir por una clave que contiene nulos sin pensarlo.** En un `join` de igualdad los `NULL` no
  casan con nada, pero **todos caen en la misma partición del shuffle**: no producen resultado y
  aun así generan la tarea gigante. Filtra los nulos o dales una sal aleatoria antes de unir.
- **Confundir sesgo con volumen.** Si el problema fuera el volumen, añadir máquinas ayudaría.
  Con sesgo, añadir máquinas no cambia nada: la tarea caliente sigue siendo una sola. Mira la
  distribución de duración de tareas, no el total de bytes.
- **Aplicar salting a un solo lado.** Si añades `sal` a la tabla grande pero no replicas la
  pequeña por cada valor de `sal`, cada fila solo puede unir con un trozo: obtienes resultados
  incompletos sin ningún error. Es un fallo silencioso y carísimo.
- **Difundir una tabla que crece con el tiempo.** Hoy son 8 MB y el `broadcast` explícito
  funciona; dentro de seis meses la dimensión tiene 2 GB y el trabajo empieza a morir sin que
  nadie haya tocado el código. Pon una alerta sobre el tamaño de las dimensiones.
- **Arreglar el sesgo con `repartition` por la clave de unión.** `repartition(n, "dispositivo")`
  sigue mandando todas las filas de la clave caliente a la misma partición: has pagado un
  shuffle completo para obtener exactamente el mismo sesgo.

## Comprueba que lo sabes

:::quiz
p: Un `join` entre 120 millones de filas y una dimensión de 6 MB. ¿Qué hace Spark por defecto y por qué es lo mejor?
o: Unión por difusión: la dimensión cabe bajo el umbral de 10 MB, se copia a cada ejecutor y la tabla grande no se baraja
o: Unión por ordenación y mezcla, porque la tabla grande siempre manda
o: Un `cartesian` producto, porque la dimensión es diminuta
a: 1
e: Por debajo del umbral de difusión (10 MB por defecto), Spark copia la tabla pequeña a cada ejecutor y evita por completo el shuffle de la grande. No hay red ni disco temporal para la tabla de 120 millones de filas.
:::

:::quiz
p: Con 400 particiones, una clave concentra 48 de los 120 millones de filas. ¿Por qué el salting arregla el problema y qué cuesta?
o: Porque divide esa clave en varios trozos y reparte sus filas, a cambio de replicar el otro lado tantas veces como trozos
o: Porque elimina las filas repetidas antes de unir, a cambio de perder esos registros
o: Porque aumenta el número de particiones automáticamente, sin ningún coste
a: 1
e: El salting convierte `k` en `(k, s)` con S valores, así que la clave caliente se reparte entre S particiones. Para que la unión siga siendo correcta hay que replicar el lado pequeño S veces, y ese es el precio. No elimina filas ni cambia el número de particiones por sí solo.
:::

:::trampa
Si tu trabajo tarda mucho pero el 90 % de las tareas terminó en dos minutos, no busques en el
código de la transformación: busca una clave con muchísimos valores repetidos. Los sospechosos
habituales son los centinelas (`"desconocido"`, `-1`, `"N/A"`), los nulos y los identificadores
de una sola entidad enorme (una cuenta de sistema, un rastreador, un cliente interno).
:::
