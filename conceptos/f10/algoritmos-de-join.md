---
id: algoritmos-de-join
titulo: Algoritmos de join
fase: 10
nivel: intermedio
rutas: [alg, de, ds]
prerequisitos: [tablas-hash, ordenacion]
tags: [joins, hash, ordenacion, coste, motores]
resumen: Bucle anidado, hash join y sort-merge join: cuándo es viable cada uno, cómo desborda el Grace hash a disco y por qué una clave sesgada rompe el reparto.
fuentes: ["Cormen, Leiserson, Rivest y Stein (2009), 'Introduction to Algorithms', cap. 11 (Hash Tables)", "Silberschatz, Korth y Sudarshan (2019), 'Database System Concepts', cap. 15 (Query Processing)", "Graefe (1993), 'Query Evaluation Techniques for Large Databases'"]
---

## En una frase

Unir dos tablas es responder «para cada fila de una, qué filas de la otra tienen la misma clave»,
y solo hay tres familias de algoritmos: comparar todas con todas (bucle anidado), repartir por
[[tablas-hash|hash]] y comparar dentro de cada montón (hash join), o [[ordenacion|ordenar]] las
dos y recorrerlas a la vez (sort-merge join). El resto —Grace hash, híbrido, con índice, con
broadcast— son variantes para cuando el caso base no cabe en memoria.

## La idea

Imagina que tienes que emparejar dos listas de invitados por apellido: una con 10.000 nombres y
otra con 200. Hay tres formas de hacerlo, y las tres se usan de verdad.

**Comparar todas con todas.** Coges el primer nombre de la lista grande y lo buscas recorriendo
entera la lista pequeña. Luego el segundo, y otra vez desde el principio. Con 10.000 y 200 son
dos millones de comparaciones, y da igual lo ordenadas que estén las listas. Es absurdo… salvo
que la lista pequeña esté indexada: entonces cada búsqueda cuesta unas pocas comparaciones en vez
de 200, y el bucle anidado pasa a ser competitivo. Esta es la versión que más se usa en la
práctica, porque casi siempre existe un índice.

**Repartir por hash.** Escribes cada apellido en un montón según una regla fija —por ejemplo, la
primera letra— y haces lo mismo con las dos listas. Como la regla es la misma, dos invitados con
el mismo apellido caen **siempre en el mismo montón**, así que las parejas solo pueden estar
dentro de un montón: ya no hay que cruzar los 10.000 con los 200, basta con cruzar cada montón
consigo mismo. Es lo que hace el **hash join**: se construye una tabla hash con la tabla pequeña
y se sondea con cada fila de la grande. Su límite es evidente: la tabla hash tiene que caber en
memoria. Cuando no cabe, se parte antes en trozos que sí quepan —eso es el **Grace hash join**— y
cada trozo se une por separado.

**Ordenar y recorrer en paralelo.** Ordenas las dos listas por apellido y las recorres a la vez
como una cremallera: si la cabeza de la primera es menor, avanzas esa; si es mayor, avanzas la
otra; si son iguales, emparejas y avanzas las dos. Es el **sort-merge join**, y es el único de los
tres que sirve para condiciones que no son igualdad (`a.fecha > b.fecha`, `a.importe BETWEEN …`),
porque al ir en orden basta con saber cuál va por delante. Su pega es que hay que ordenar, y
ordenar 10 millones de filas cuesta más que todo lo demás junto; si las tablas ya vienen
ordenadas por la clave, en cambio, sale casi gratis.

La decisión práctica la toma el **optimizador** del motor, no tú, y la toma con estadísticas: el
número de filas estimado de cada lado, cuántas caben en memoria y si hay índice. Tú necesitas
entender los tres para leer un `EXPLAIN` y para saber por qué una consulta que iba bien con datos
de prueba se cae en producción. Y el sospechoso número uno de esa caída es el **sesgo**: si una
sola clave aparece en la mitad de las filas, todas esas filas caen en el mismo montón y no hay
reparto que las separe.

## Definición formal

Sean `A` y `B` dos tablas, `n_A` y `n_B` sus filas, `b_A` y `b_B` sus bloques (con `B_reg`
filas por bloque), y `θ` la condición del join. La **reunión** es el conjunto de pares que
cumplen la condición:

:::formula
A ⋈θ B = { (a, b) ∈ A × B : θ(a, b) }
:::

Para el caso habitual, que es igualdad por una clave `k`, el tamaño del resultado y —lo que de
verdad importa— el tamaño de cada montón se calculan contando apariciones:

:::formula
|A ⋈ B| = Σₖ c_A(k) · c_B(k)
:::

donde `c_A(k)` es el número de filas de `A` con clave `k`. Esa suma es la que decide el plan: si
`c_B(k)` vale 1 para todas las claves (clave única, típico de una dimensión), cada fila de `A`
produce como mucho una del resultado; si no, el join **multiplica**.

Coste de cada familia, contado en comparaciones y en bloques movidos:

| Algoritmo | Comparaciones | Bloques movidos | Necesita | ¿Sirve para desigualdad? |
| --- | --- | --- | --- | --- |
| Bucle anidado por bloques | n_A · n_B | b_ext + b_ext · b_int | Nada | Sí |
| Bucle anidado con índice | n_A · log n_B | b_A + n_A · altura | Índice en el lado interno | Sí |
| Hash join en memoria | n_A + n_B | b_A + b_B | El lado menor cabe en memoria | No, solo igualdad |
| Grace hash join | n_A + n_B | 3 · (b_A + b_B) | Cada partición cabe en memoria | No, solo igualdad |
| Sort-merge join | n log n al ordenar + n_A + n_B | ordenar + b_A + b_B | Nada; gratis si ya está ordenado | Sí |

El `3 · (b_A + b_B)` del Grace sale de contar sus dos fases: primero se lee y se escribe cada
tabla para repartirla en `P` particiones (`2 · (b_A + b_B)`) y después se lee cada pareja de
particiones una vez (`b_A + b_B`). Las particiones se eligen con la misma función de hash en las
dos tablas, y de ahí la garantía: las filas de una misma clave caen siempre en la misma pareja de
particiones.

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `n_A`, `n_B` | Filas de cada tabla | filas | El hash y el sort-merge crecen de forma lineal; el bucle anidado, con el producto de las dos |
| `b_A`, `b_B` | Bloques de cada tabla | bloques | Todo el coste de disco se mide en estos; leer la tabla pequeña muchas veces es lo que hunde al bucle anidado |
| `B_reg` | Filas por bloque | filas | Bloques más grandes, menos accesos y menos viajes: es la palanca más barata que hay |
| `P` | Particiones del Grace hash | particiones | Cada partición es más pequeña y cabe mejor en memoria, pero hay más ficheros abiertos y más viajes |
| `c_A(k)`, `c_B(k)` | Filas de cada tabla con la clave `k` | filas | El resultado crece con el producto: una clave con `c_A = 5.000` y `c_B = 4` produce 20.000 filas, no 9.000 |
| `M` | Memoria disponible para el join | bloques | Si `M ≥ b_B + 1`, el hash join se hace en memoria y no toca el disco; por debajo, hay que repartir |
:::

:::figura
fichero: algoritmos-de-join-coste-y-sesgo
pie: A la izquierda, el tamaño de la partición más cargada al repartir 10.000 filas por hash, con la línea morada marcando la memoria disponible. Con claves uniformes la partición mayor baja como n/P, de 5.000 a 166 filas al pasar de 2 a 256 particiones; con una clave que aparece en la mitad de las filas se queda clavada por encima de la memoria por muchas particiones que hagas: 5.624 con P = 8 y 5.016 con P = 256. A la derecha, los bloques movidos por las tres familias al unir dos tablas de n filas: el bucle anidado crece con el producto (una parábola en escala logarítmica) y el hash y el sort-merge, en línea recta. El sort-merge se separa del hash en memoria justo por lo que cuesta ordenar antes las dos tablas.
fuente: figuras/algoritmos-de-join-1.py
:::

## Ejemplo

Dos tablas diminutas: `clientes` con 3 filas (`ana`, `luis`, `marta`) y `pedidos` con 5 filas. El
join es por el identificador de cliente.

- **Bucle anidado:** recorre los 3 clientes para cada uno de los 5 pedidos: `3 · 5 = 15`
  comparaciones.
- **Hash join:** se construye la tabla hash con los 3 clientes y se sondea una vez por pedido: 5
  búsquedas. Las 3 inserciones no comparan nada.
- **Sort-merge:** se ordenan las dos tablas, lo que en listas tan cortas son un puñado de
  comparaciones, y la cremallera recorre después las dos listas con 7 comparaciones entre cabezas.

El resultado son 5 filas, y coincide con lo que dice la fórmula: `c_pedidos(1) = 2`,
`c_pedidos(2) = 1`, `c_pedidos(3) = 2`, y `c_clientes(k) = 1` para las tres claves, así que
`2·1 + 1·1 + 2·1 = 5`.

Con tablas de verdad se ve por qué el bucle anidado solo sobrevive si hay índice. Diez millones
de pedidos (100.000 bloques) contra 200.000 clientes (2.000 bloques), con bloques de 100 filas:

| Algoritmo | Bloques movidos |
| --- | --- |
| Bucle anidado por bloques | 200.002.000 |
| Hash join en memoria | 102.000 |
| Grace hash join a disco | 306.000 |
| Sort-merge con las entradas ya ordenadas | 102.000 |
| Sort-merge ordenando antes las dos | 706.000 |

El bucle anidado mueve **unas 2.000 veces más** datos que el hash join, y el sort-merge empata
con el hash cuando las entradas llegan ordenadas. Eso explica dos cosas que se ven todos los días
en un `EXPLAIN`: que un join entre una tabla grande y una pequeña casi siempre sea un hash join
(o un bucle anidado con índice), y que el sort-merge aparezca cuando la consulta ya ordena por esa
clave, porque entonces la ordenación se paga una sola vez para las dos cosas.

## Código

```python verificable
def bucle_anidado(A, B, clave):
    """Compara cada fila de A con todas las de B: n_A por n_B comparaciones."""
    pares, comparaciones = [], 0
    for a in A:
        for b in B:
            comparaciones += 1
            if clave(a) == clave(b):
                pares.append((clave(a), a[1], b[1]))
    return sorted(pares), comparaciones

def hash_join(A, B, clave):
    """Construye la tabla hash con B y sondea con A: una busqueda por fila de A."""
    indice = {}
    for b in B:
        indice.setdefault(clave(b), []).append(b)    # las claves repetidas se acumulan
    pares, busquedas = [], 0
    for a in A:
        busquedas += 1
        for b in indice.get(clave(a), []):
            pares.append((clave(a), a[1], b[1]))
    return sorted(pares), busquedas

def sort_merge(A, B, clave):
    """Ordena las dos entradas y las recorre en paralelo, como una cremallera."""
    A, B = sorted(A, key=clave), sorted(B, key=clave)
    pares, i, j, comparaciones = [], 0, 0, 0
    while i < len(A) and j < len(B):
        comparaciones += 1
        ca, cb = clave(A[i]), clave(B[j])
        if ca == cb:                    # hay que emparejar con TODOS los empatados de B
            k = j
            while k < len(B) and clave(B[k]) == ca:
                pares.append((ca, A[i][1], B[k][1])); k += 1
            i += 1
        elif ca < cb:
            i += 1
        else:
            j += 1
    return sorted(pares), comparaciones

clientes = [(1, "ana"), (2, "luis"), (3, "marta")]
pedidos = [(3, "cafe"), (1, "te"), (3, "pan"), (2, "agua"), (1, "sal")]
clave = lambda fila: fila[0]
print("bucle anidado:", bucle_anidado(pedidos, clientes, clave)[1], "comparaciones")
# -> bucle anidado: 15 comparaciones
print("hash join:", hash_join(pedidos, clientes, clave)[1], "busquedas")
# -> hash join: 5 busquedas
print("sort-merge:", sort_merge(pedidos, clientes, clave)[1], "comparaciones")
# -> sort-merge: 7 comparaciones
a = bucle_anidado(pedidos, clientes, clave)[0]
b = hash_join(pedidos, clientes, clave)[0]
c = sort_merge(pedidos, clientes, clave)[0]
print("los tres dan lo mismo:", a == b == c)     # -> los tres dan lo mismo: True
print("filas del resultado:", len(a))            # -> filas del resultado: 5
```

```python verificable
import zlib

def repartir(filas, P):
    """Reparte por hash de la clave: la misma clave cae siempre en la misma particion."""
    partes = [[] for _ in range(P)]
    for fila in filas:
        partes[zlib.crc32(str(fila[0]).encode()) % P].append(fila)
    return partes

# Ojo: hash() de Python cambia en cada ejecucion para las cadenas (PYTHONHASHSEED), asi
# que para medir y comparar hace falta una funcion fija como crc32.
P, memoria = 8, 2000
uniforme = [(i % 5000, i) for i in range(10000)]                    # 5000 claves, 2 filas cada una
sesgado = [(42 if i % 2 == 0 else i % 5000, i) for i in range(10000)]   # la clave 42 en la mitad

for nombre, filas in (("uniforme", uniforme), ("sesgado ", sesgado)):
    tamanos = [len(p) for p in repartir(filas, P)]
    print(nombre, "mayor particion:", max(tamanos), "cabe en memoria:", max(tamanos) <= memoria)
# -> uniforme mayor particion: 1252 cabe en memoria: True
# -> sesgado  mayor particion: 5624 cabe en memoria: False

print("con P = 64, uniforme:", max(len(p) for p in repartir(uniforme, 64)))
# -> con P = 64, uniforme: 166
print("con P = 64, sesgado:", max(len(p) for p in repartir(sesgado, 64)))
# -> con P = 64, sesgado: 5076
```

```python verificable
def bloques(filas, por_bloque=100):
    return -(-filas // por_bloque)          # division hacia arriba

def miles(x):
    return f"{x:,}".replace(",", ".")       # millares a la espanola

def ordenar_externo(b, M, k):
    """Bloques movidos al ordenar b bloques con M en memoria y fusiones de k vias."""
    vueltas, rondas = -(-b // M), 0
    while vueltas > 1:
        vueltas = -(-vueltas // k)
        rondas += 1
    return 2 * b * (1 + rondas)

n_A, n_B = 10_000_000, 200_000              # tabla de hechos y tabla de dimension
b_A, b_B = bloques(n_A), bloques(n_B)
print("bloques de A y B:", miles(b_A), miles(b_B))            # -> bloques de A y B: 100.000 2.000
print("bucle anidado por bloques:", miles(b_B + b_B * b_A))
# -> bucle anidado por bloques: 200.002.000
print("hash en memoria:", miles(b_A + b_B))                   # -> hash en memoria: 102.000
print("Grace hash a disco:", miles(3 * (b_A + b_B)))          # -> Grace hash a disco: 306.000
print("sort-merge ya ordenado:", miles(b_A + b_B))            # -> sort-merge ya ordenado: 102.000
ordenar = ordenar_externo(b_A, 5000, 10) + ordenar_externo(b_B, 5000, 10)
print("ordenar las dos antes:", miles(ordenar))               # -> ordenar las dos antes: 604.000
print("sort-merge completo:", miles(ordenar + b_A + b_B))     # -> sort-merge completo: 706.000
```

:::claves
- El hash join solo necesita una pasada por tabla (`b_A + b_B`) **si la tabla hash cabe en memoria**. En cuanto no cabe, el coste sube a `3 · (b_A + b_B)` y el disco trabaja el triple; el plan cambia de nombre en el `EXPLAIN` y mucha gente no lo mira.
- `indice.setdefault(clave, []).append(fila)` agrupa las claves repetidas en una lista. Si en vez de una lista guardas solo la última fila, el join pierde filas silenciosamente: es la diferencia entre un join y un `dict` mal usado.
- El bucle anidado con índice **no** cuesta `n_A · n_B`: cuesta una búsqueda por fila de la tabla externa, y cada búsqueda es la altura del árbol (tres o cuatro niveles en un B-árbol). Por eso sobrevive cuando la tabla externa es pequeña.
- El sort-merge es el único que resuelve desigualdades (`BETWEEN`, `>`, rangos de fechas) y también el único que conserva el orden de salida. Si la consulta lleva `ORDER BY` por la clave del join, el motor no vuelve a ordenar: ya está ordenado.
- El reparto por hash **no puede separar una sola clave**. Todas las filas con la misma clave tienen que acabar juntas para poder emparejarlas, así que si una clave ocupa más que la memoria, subir `P` no arregla nada: la partición de esa clave sigue teniendo el mismo tamaño.
- `hash()` de Python sobre cadenas no es estable entre ejecuciones (usa una semilla aleatoria por proceso). Para reproducir un reparto hay que usar una función fija, como `zlib.crc32`, que es lo que hacen los motores con su propia función de hash.
:::

## Errores típicos

- **Elegir el algoritmo a mano.** El optimizador decide con las estadísticas de las tablas. Si
  nunca ejecutas `ANALYZE` (o el equivalente), esas estadísticas están viejas y el plan sale mal:
  el motor puede elegir un bucle anidado creyendo que la tabla tiene 100 filas cuando tiene 100
  millones.
- **Unir por columnas con tipos distintos.** Un `id` numérico en una tabla y de tipo texto en la
  otra impide el hash (los valores no coinciden) y muchas veces el índice. El motor se ve obligado
  a convertir fila a fila, y ninguna de las tres familias funciona como debería.
- **Aplicar una función a la clave del join.** `WHERE date(a.fecha) = b.fecha` o
  `WHERE upper(a.nombre) = b.nombre` desactivan el índice y el reparto: la función se evalúa por
  fila y el motor no puede usar nada precalculado. Se reescribe el filtro para dejar la columna
  desnuda.
- **Ignorar el sesgo hasta que revienta en producción.** Con datos de prueba uniformes, el reparto
  por hash se ve perfecto; con la clave caliente de verdad, una partición se lleva la mitad de la
  tabla, se queda sin memoria y el join pasa de minutos a horas. En Spark se ve como una tarea que
  dura lo que las demás juntas y se llama *skew* ([[spark-joins-y-skew|asimetría de claves]]).
- **Suponer que el resultado tiene el tamaño de la tabla grande.** El tamaño es
  `Σ c_A(k) · c_B(k)`: si la clave no es única en el lado derecho, el join **multiplica** filas.
  Un join que devuelve 20 veces más filas de las esperadas suele ser esto, no un fallo del motor.
- **Creer que ordenar es siempre lo peor.** Si la tabla ya está ordenada por la clave (un índice
  agrupado, un fichero Parquet ya ordenado por fecha), el sort-merge cuesta leer y escribir una
  vez, exactamente igual que el hash. La ordenación solo es cara cuando hay que pagarla.

:::trampa
El Grace hash join necesita el **doble** de espacio temporal en disco: mientras reparte, escribe
las dos tablas enteras en ficheros temporales antes de empezar a unir. Un join que ocupa poco en
memoria puede llenar el disco, y el error que verás no habla de joins: habla de «no space left on
device».
:::

:::nota
Cuando una de las dos tablas es diminuta (unos pocos megabytes), lo más rápido es **copiarla
entera a cada nodo** y hacer el join contra esa copia en memoria. Es el *broadcast join* y es,
simplemente, un hash join en el que el reparto no hace falta porque la tabla pequeña ya cabe.
:::

:::practica
enunciado: Una tabla de hechos de 10 millones de filas se une con una dimensión de 200.000 filas por una clave que es única en la dimensión. La clave de la dimensión mide 8 bytes y la de los hechos 200 bytes. Estima el tamaño del resultado y decide qué algoritmo elegirías sin índice, explicando por qué.
pista: El tamaño del resultado depende de `Σ c_A(k) · c_B(k)`, y si la clave es única en la dimensión cada valor de `c_B(k)` vale 1 o 0. Para el algoritmo, mira cuánto ocupa la tabla hash del lado pequeño.
solucion: Como la clave es única en la dimensión, cada fila de hechos produce como mucho una fila de salida, así que el resultado tiene entre 0 y 10 millones de filas: no hay multiplicación. La tabla hash del lado pequeño guarda 200.000 entradas de 8 bytes más el puntero a la fila: unos pocos megabytes, así que cabe en memoria sin repartir. La elección es un hash join en memoria (leer cada tabla una vez), con la dimensión como lado de construcción por ser la menor. Si la dimensión tuviera claves repetidas, el resultado podría ser mucho mayor que 10 millones y habría que comprobar el sesgo antes de decidir el plan.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Por qué el hash join no puede resolver una condición de desigualdad como `a.fecha > b.fecha`?
o: Porque las fechas ocupan mucho y no caben en una tabla hash
o: Porque el hash solo agrupa valores iguales; una fila puede cumplir la condición con muchas filas de la otra tabla y no hay una única cubeta donde buscarla
o: Porque el hash join necesita que las dos tablas estén ordenadas
a: 2
e: La tabla hash responde a «dame las filas con esta clave exacta»: agrupa por igualdad. Para una desigualdad, una fila de A puede emparejar con muchas filas de B repartidas por todo el rango, y ninguna función de hash las junta. Por eso las desigualdades se resuelven con bucle anidado o con sort-merge, que recorren los datos en orden.
:::

:::quiz
p: Repartes 10.000 filas en 8 particiones por hash y una clave aparece en la mitad de las filas. ¿Qué consigues subiendo a 64 particiones?
o: Que la partición de esa clave baje a la mitad y quepa en memoria
o: Casi nada: esa partición sigue teniendo las 5.000 filas de la clave, porque el reparto por hash no puede separar filas con la misma clave
o: Que el join deje de necesitar memoria
a: 2
e: Todas las filas de una misma clave tienen que acabar en la misma partición para poder emparejarse, así que una clave con 5.000 filas produce una partición de 5.000 filas como mínimo, con 8 particiones y con 64. Lo que sí baja es el tamaño de las demás: la partición mayor del caso uniforme pasa de unas 1.250 a unas 166 filas. El sesgo se ataca de otra forma: dejando esa clave en memoria, procesándola aparte o copiando el lado pequeño a todos los nodos.
:::

:::quiz
p: Tienes que unir dos tablas de 500 millones de filas cada una con la misma clave, y el resultado se va a ordenar por esa clave. ¿Qué algoritmo encaja mejor?
o: Bucle anidado con índice, porque no necesita memoria
o: Sort-merge join, porque la ordenación hace falta de todas formas y el join aprovecha ese trabajo
o: Grace hash join, porque siempre es el más rápido
a: 2
e: Si hay que ordenar el resultado por la clave del join, ordenar las dos entradas una vez y fusionarlas resuelve las dos cosas a la vez: el join y el ORDER BY. El bucle anidado sería inviable con ese volumen (el producto de las dos tablas es astronómico) y el Grace hash obligaría a repartir ambas tablas en disco para luego ordenar igualmente el resultado.
:::
