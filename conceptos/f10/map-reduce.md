---
id: map-reduce
titulo: MapReduce y cómputo distribuido
fase: 10
nivel: avanzado
rutas: [alg, de]
prerequisitos: [complejidad-asintotica, tablas-hash, ordenacion]
tags: [distribuido, big-data, particionado, spark]
resumen: El patrón map, shuffle y reduce que sostiene Spark y Hadoop, y la razón de que casi todo el coste esté en el shuffle y no en el cálculo.
fuentes: ["Dean y Ghemawat (2004), 'MapReduce: Simplified Data Processing on Large Clusters'", "Leskovec, Rajaraman y Ullman (2014), 'Mining of Massive Datasets'"]
---

## En una frase

MapReduce parte un cálculo en dos funciones puras —`map`, que transforma cada registro por
separado, y `reduce`, que combina todos los registros de la misma clave— y deja que el sistema
se encargue de repartir el trabajo, ordenar por clave en el medio y repetir las tareas que
fallen.

## La idea

Imagina un referéndum con 40.000 mesas electorales. Contar los votos no lo hace una sola
persona: cada mesa cuenta los suyos y anota «candidato A: 132», «candidato B: 87». Eso es
`map`: una transformación local, sin mirar lo que hacen las demás mesas. Después, todas las
anotaciones del candidato A se llevan a la misma sala, se juntan y se suman. Eso es `shuffle`
y `reduce`.

Lo importante es que **nadie necesita saber el total para hacer su parte**. Cada mesa trabaja
con lo que tiene delante, y el resultado final no depende de en qué orden se sumen las salas.
Esa independencia es lo que permite repartir el trabajo entre miles de máquinas y, sobre todo,
lo que permite **repetir** una tarea que se ha caído: si el resultado de una mesa se pierde, se
vuelve a contar esa mesa y ya está.

Las tres fases, con lo que cuesta cada una:

1. **Map.** Recorre los datos de entrada y emite pares `(clave, valor)`. Es paralelo sin
   comunicación: cada tarea ve solo su trozo. Barato.
2. **Shuffle.** Agrupa todos los valores de la misma clave en la misma máquina. Esto implica
   escribir en disco, leer, enviar por red y ordenar. **Es la fase cara**, y en un trabajo real
   se lleva la mayor parte del tiempo.
3. **Reduce.** Recibe una clave y la lista de sus valores, y produce el resultado. Barato si el
   shuffle ha repartido bien.

De ahí salen las dos preguntas de diseño que de verdad importan. La primera: ¿cuántos datos
pasan por el shuffle? Si puedes reducirlos antes de enviarlos, hazlo. La segunda: ¿se reparten
esos datos de forma equilibrada entre los reductores? Si una clave concentra la mitad de los
registros, un solo reductor hará la mitad del trabajo mientras los demás miran.

## Definición formal

Un trabajo MapReduce se compone de dos funciones que el programador escribe y un motor que las
orquesta. Sean `(k₁, v₁)` los pares de la entrada, `R` el número de reductores y `h` una función
hash.

- **Map:** `map(k₁, v₁) → [(k₂, v₂), …]`. Un par de entrada puede producir cero, uno o muchos
  pares intermedios.
- **Shuffle:** cada par intermedio `(k₂, v₂)` se envía al reductor número `h(k₂) mod R`. El
  motor **ordena** por `k₂` dentro de cada reductor y agrupa los valores: `(k₂, [v₂, v₂, …])`.
- **Reduce:** `reduce(k₂, [v₂, …]) → [(k₃, v₃), …]`. El reductor solo ve su clave.

De aquí salen dos condiciones que no son opcionales:

**Determinismo.** `map` y `reduce` deben ser funciones puras del dato: mismo par de entrada,
mismo resultado. Si dependen del reloj, de un número aleatorio sin semilla o del orden en que
llegan los datos, la reejecución de una tarea perdida dará un resultado distinto y el trabajo
completo será irreproducible.

**Conmutatividad y asociatividad para el combiner.** Un **combiner** es un mini-`reduce` que se
ejecuta en la máquina del `map` para enviar menos datos por la red. Solo es correcto si la
operación cumple `f(a, b) = f(b, a)` (conmutativa) y `f(f(a, b), c) = f(a, f(b, c))`
(asociativa). La suma, el máximo, el mínimo y el OR de bits lo cumplen. La **media no**, y por
eso la media se calcula emitiendo pares `(suma, cuenta)` y dividiendo al final. La mediana
tampoco, y por eso no existe un combiner para ella.

**Modelo de coste.** Si `M` es el número de pares intermedios y `R` el número de reductores, el
shuffle mueve del orden de los `M` pares por la red, y el tiempo total de pared está dominado
por `maxᵣ(carga del reductor r)`, no por la media. De ahí que el **desbalanceo** (skew) sea el
enemigo principal: con `R = 100` reductores y uno de ellos recibiendo el 50 % de los datos,
añadir reductores no mejora nada.

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `M` | Pares intermedios que emite el `map` (antes o después del combiner) | pares | Más datos por la red y más tiempo de shuffle; es la palanca que más se nota |
| `R` | Número de reductores | tareas | Más paralelismo, pero también más tareas que arrancar y más coste de coordinación: pasados unos cuantos, el tiempo total sube |
| `cargaᵣ` | Registros que le tocan al reductor `r` | pares | Si una sola clave domina, un reductor hace casi todo el trabajo y el resto espera |
| `h(k₂)` | Función hash que decide el reductor de cada clave | índice | No es una palanca de rendimiento, sino de corrección: cambiarla cambia la partición y con ella el desbalanceo |
| `s` | Fracción del trabajo que no se puede paralelizar (el `s` de la ley de Amdahl, `S(n) = 1 / (s + (1 − s)/n)`, que es lo que mide el panel izquierdo de la figura) | fracción | Baja el techo de aceleración hasta `1/s`: con un 5 % en serie, el máximo es 20× por muchas máquinas que añadas |
:::

:::figura
fichero: map-reduce-aceleracion-y-desbalanceo
pie: A la izquierda, la aceleración frente al número de trabajadores. La recta gris es lo que promete el reparto perfecto, la curva azul es la ley de Amdahl con un 5 % de trabajo en serie (se aplana en 20× y no pasa de ahí) y la naranja añade el coste de coordinar y de mover datos por el shuffle: sube, llega a un máximo y luego baja, así que a partir de cierto punto cada máquina nueva resta. A la derecha, el reparto real de 200.000 registros entre 10 reductores cuando las claves siguen una ley de potencias: el más cargado recibe el triple que la media y los demás terminan antes y esperan. El tiempo total del trabajo lo fija ese reductor, no la media.
fuente: figuras/map-reduce-1.py
:::

## Ejemplo

**Recuento de palabras.** Tres documentos: `d1` = «el gato come pescado», `d2` = «el perro come
pienso», `d3` = «el gato y el perro duermen». El `map` emite 14 pares `(palabra, 1)`. Tras el
shuffle, la clave `el` tiene la lista `[1, 1, 1, 1]` y el `reduce` devuelve 4; `gato` tiene
`[1, 1]` y devuelve 2. En total, 8 palabras distintas. El orden en que se sumen los cuatro
unos de `el` es irrelevante, y por eso el combiner puede sumarlos en cada máquina antes de
enviarlos.

**La media, que es donde todo el mundo se equivoca.** Tres particiones con valores
`[10, 20, 30]`, `[40, 50]` y `[60]`. Sus medias son 20, 45 y 60. Si cada partición emitiera su
media y el reductor promediara esas tres medias, saldría `(20 + 45 + 60) / 3 = 41,67`. La media
correcta es `210 / 6 = 35`. La diferencia no es un redondeo: es que promediar medias solo es
correcto si todas las particiones tienen el mismo número de elementos, y en un sistema
distribuido el reparto por hash casi nunca lo garantiza. La solución es emitir **pares
`(suma, cuenta)`** y dividir una sola vez al final.

## Código

```python verificable
from collections import defaultdict

documentos = {
    "d1": "el gato come pescado",
    "d2": "el perro come pienso",
    "d3": "el gato y el perro duermen",
}


def map_(texto):
    for palabra in texto.split():
        yield palabra, 1          # cada palabra cuenta uno en su propio documento


def reduce_(clave, valores):
    return clave, sum(valores)    # el reductor solo ve los valores de su clave


pares = [par for texto in documentos.values() for par in map_(texto)]
grupos = defaultdict(list)
for clave, valor in pares:
    grupos[clave].append(valor)   # el shuffle manda cada clave a un unico reductor

recuento = dict(reduce_(*grupo) for grupo in grupos.items())
print("pares emitidos por el map:", len(pares))   # -> 14
print("palabras distintas:", len(recuento))       # -> 8
print("el:", recuento["el"], "gato:", recuento["gato"], "come:", recuento["come"])
# la ultima linea imprime: el: 4 gato: 2 come: 2
```

:::claves
- `map_` es una **función generadora** (lleva `yield`): al llamarla no ejecuta nada y devuelve un generador que va produciendo pares a medida que se consume. La lista `pares` lo consume entero; si lo recorrieras dos veces sin volver a llamar a `map_`, la segunda vez no saldría nada.
- `grupos` es un `defaultdict(list)`: al hacer `grupos[clave].append(...)` con una clave que no existía, la crea con una lista vacía. Con un `dict` normal eso sería un `KeyError`.
- El `reduce` recibe `(clave, lista_de_valores)`, no los pares uno a uno. En esta simulación la lista está entera en memoria porque los datos son diminutos; en un sistema real el motor la va entregando ordenada por clave.
- `dict(... for grupo in grupos.items())` recorre las claves en el orden en que se insertaron en el diccionario. Ese orden no es el del `shuffle` de un sistema distribuido, donde las claves se ordenan dentro de cada reductor y no entre reductores.
- `sum(valores)` sobre una lista de `int` da un `int`; si los valores fueran `float`, el resultado acumularía el error de redondeo en el mismo orden en que llegan. En un sistema distribuido ese orden no está garantizado, así que dos ejecuciones del mismo trabajo pueden dar el último decimal distinto.
- En la segunda pieza, `medias = [sum(p) / len(p) ...]` usa la división normal de Python, que devuelve `float` aunque los datos sean enteros. `//` daría la división entera y `20.0, 45.0, 60.0` se convertirían en `20, 45, 60`.
:::

```python verificable
# Calcular una media en MapReduce: cada particion emite (suma, cuenta), no su media.
particiones = [[10, 20, 30], [40, 50], [60]]

medias = [sum(p) / len(p) for p in particiones]
media_de_medias = sum(medias) / len(medias)

suma_total = sum(sum(p) for p in particiones)
cuenta_total = sum(len(p) for p in particiones)
media_correcta = suma_total / cuenta_total

print("medias por particion:", medias)                       # -> [20.0, 45.0, 60.0]
print("media de medias: {:.2f}".format(media_de_medias))     # -> 41.67
print("media correcta:  {:.2f}".format(media_correcta))      # -> 35.00
```

```python ilustrativo
# El mismo patron en Spark: groupBy dispara el shuffle y reparte por hash de la clave.
from pyspark.sql import SparkSession, functions as F

spark = SparkSession.builder.appName("recuento").getOrCreate()
lineas = spark.read.text("hdfs:///datos/libros/*.txt")     # una tarea map por bloque

recuento = (lineas
            .select(F.explode(F.split(F.lower(F.col("value")), r"\W+")).alias("palabra"))
            .filter(F.col("palabra") != "")
            .groupBy("palabra")          # shuffle: hash(palabra) % numParticiones
            .count())
recuento.orderBy(F.desc("count")).show(10)
```

## Errores típicos

- **Emitir medias en lugar de pares `(suma, cuenta)`.** Es el error clásico y el más caro,
  porque el resultado no es absurdo, solo está mal. Cualquier estadístico que no sea una suma
  (media, varianza, ratio) necesita viajar como acumuladores y combinarse al final.
- **Usar funciones no deterministas.** Un `map` que llama a `random()`, a `now()` o a un
  servicio externo hace que reejecutar una tarea perdida cambie el resultado. En un sistema
  distribuido las reejecuciones no son excepcionales: son el mecanismo normal de tolerancia a
  fallos.
- **No usar combiner cuando la operación lo permite.** En un recuento de palabras, un combiner
  puede reducir la salida del `map` de millones de pares a unos cientos de miles antes de tocar
  la red. Si la operación es asociativa y conmutativa, no usar combiner es regalar ancho de
  banda.
- **Ignorar el desbalanceo.** Una clave dominante (un `null`, un usuario robot, una fecha con
  la mitad de los datos) hace que un reductor tarde diez veces más que los demás. Se arregla
  troceando la clave en un prefijo aleatorio (`salting`), agregando en dos pasadas y quitando el
  prefijo en la segunda.
- **Creer que el orden de salida está garantizado.** El shuffle ordena las claves dentro de cada
  reductor, no los resultados entre reductores, ni el orden de los valores de una misma clave.
  Si necesitas un orden global, ordena al final y asume su coste.
- **Repartir en demasiadas particiones minúsculas.** Cada partición cuesta abrir una tarea, y
  una tarea tarda en arrancar mucho más que en procesar 10 MB. Miles de ficheros de 1 MB dan un
  trabajo que pasa el 90 % del tiempo arrancando tareas en lugar de calculando.

:::practica
enunciado: Un map emite 40 millones de pares de 16 bytes y el combiner los deja en 5 millones. Con 8 reductores, calcula los bytes que cruzan la red en cada caso y cuántos pares procesa cada reductor como media.
pista: El combiner solo actúa sobre pares de la misma clave en la misma máquina de map.
solucion: Sin combiner cruzan 40·10⁶ · 16 B = 640 MB. Con combiner, 5·10⁶ · 16 B = 80 MB, un 87,5 % menos. Repartidos entre 8 reductores, 5·10⁶/8 = 625.000 pares por reductor de media; si una clave concentra la mitad, ese reductor recibe 2,5 millones y tarda cuatro veces más.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Por qué una media no se puede calcular emitiendo directamente la media de cada partición?
o: Porque las medias no caben en la memoria de un reductor
o: Porque promediar las medias solo coincide con la media global si todas las particiones tienen el mismo tamaño
o: Porque la media no es conmutativa y el shuffle la desordena
a: 2
e: La media de medias pondera igual a una partición de 10 elementos que a una de 10.000. Emitiendo (suma, cuenta) y dividiendo al final se obtiene el resultado correcto sea cual sea el reparto. Ejemplo: medias 20, 45 y 60 darían 41,67, cuando la media real es 35.
:::

:::quiz
p: ¿Cuál es la fase que domina el coste de un trabajo MapReduce típico?
o: El map, porque recorre todos los datos de entrada
o: El shuffle, porque escribe en disco y mueve los datos intermedios por la red
o: El reduce, porque hace la agregación final
a: 2
e: El map y el reduce son transformaciones locales y baratas; el shuffle implica serializar, escribir a disco, transferir por red y ordenar. Por eso todas las optimizaciones serias van dirigidas a reducir el volumen intermedio, no a acelerar el cálculo por registro.
:::

:::trampa
Si tu trabajo tarda mucho más de lo previsto, mira primero la distribución de tamaños por
partición antes de tocar el código: en la mayoría de los casos hay una clave que concentra una
parte enorme de los datos. Ninguna cantidad de máquinas arregla una partición que recibe el
50 % del trabajo.
:::
