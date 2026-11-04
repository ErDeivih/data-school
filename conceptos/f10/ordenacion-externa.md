---
id: ordenacion-externa
titulo: Ordenación externa
fase: 10
nivel: avanzado
rutas: [alg, de]
prerequisitos: [ordenacion, heaps-y-prioridad, complejidad-asintotica]
tags: [ordenacion, disco, memoria, fusion, datos]
resumen: Ordenar más datos de los que caben en memoria: trozos que sí quepan, ordenar cada uno y fusionarlos con un montículo de k vías eligiendo bien la k.
fuentes: ["Knuth (1998), 'The Art of Computer Programming, Vol. 3: Sorting and Searching', sección 5.4 (External Sorting)", "Cormen, Leiserson, Rivest y Stein (2009), 'Introduction to Algorithms', cap. 18 (B-Trees) y problema 18-3"]
---

## En una frase

La ordenación externa ordena conjuntos que no caben en memoria en dos fases: primero parte los
datos en trozos del tamaño de la memoria disponible y ordena cada uno; después **fusiona** esos
trozos ordenados de `k` en `k` con un montículo, que solo necesita `k` elementos en memoria a la
vez. Es lo que hace posible un `ORDER BY` sobre 500 GB.

## La idea

Tienes 500.000 fichas que ordenar por apellido y una mesa que solo aguanta 5.000. No hay truco:
la mesa no se estira. Lo que sí puedes hacer es esto:

1. Coges 5.000 fichas, las ordenas encima de la mesa y las dejas en un montón ordenado. Repites
   hasta agotar las fichas: te quedan 100 montones, cada uno ordenado por dentro.
2. Ahora coges los 100 montones y los fusionas. Para eso no hace falta que quepan: te basta con
   tener **la primera ficha de cada montón** a la vista. Miras cuál de esas 100 cabezas es la
   menor, la pones en la caja de salida y destapas la siguiente ficha de ese montón. El montón
   del que sacas va avanzando y los demás esperan.

Eso es toda la ordenación externa, y tiene dos consecuencias que conviene entender antes de
seguir. La primera: **en memoria solo hacen falta las cabezas**, `k` fichas, no los datos
completos, así que el algoritmo funciona con 10 GB, con 10 TB y con lo que le eches. La segunda:
el trabajo pesado ya no son las comparaciones, son las **lecturas y escrituras**. Cada ficha se
lee y se escribe una vez al crear los montones y otra vez en cada ronda de fusión. Cuando el
cuello de botella es el disco, optimizar comparaciones no sirve de nada; lo que sirve es reducir
el número de pasadas.

El nombre técnico de los montones ordenados es *runs* o **vueltas**. Y el número de pasadas se
controla con una sola decisión: **cuántos montones fusionas a la vez**, la `k` del título. Si
fusionas de dos en dos, con 100 vueltas necesitas 7 rondas (`⌈log₂ 100⌉`); si fusionas de 100 en
100, te sobra una. Cada ronda cuesta leer y escribir todo el conjunto otra vez, así que pasar de
7 rondas a 1 es la diferencia entre mover 160 GB o mover 40 GB en el ejemplo de abajo.

Hay un detalle que mejora la primera fase gratis. Si en lugar de llenar la memoria, ordenarla y
volcarla, vas sacando el mínimo de un montículo y metiendo el registro nuevo **solo si es mayor
que el que acabas de sacar**, las vueltas salen más largas que `M`. En datos al azar, la longitud
media de cada vuelta es `2M` (resultado clásico de Knuth), así que hay la mitad de vueltas y, con
suerte, una ronda menos. Esto se llama **selección por reemplazo** y lo usan los motores de bases
de datos desde los años setenta.

## Definición formal

Sean:

- `n`: número de registros que hay que ordenar.
- `M`: número de registros que caben en memoria a la vez.
- `B`: registros que se leen en cada acceso a disco (un bloque).
- `k`: número de vueltas que se fusionan simultáneamente (vías de la fusión).

**Fase 1 (crear vueltas).** Se leen los datos en grupos de `M`, se ordena cada grupo en memoria
(con [[ordenacion|cualquier ordenación interna]]) y se escribe. Salen `⌈n / M⌉` vueltas. Con
selección por reemplazo salen aproximadamente `n / (2M)`, la mitad.

**Fase 2 (fusionar).** Cada ronda toma `k` vueltas ordenadas y produce una sola, recorriéndolas
con un montículo de `k` elementos. `[[heaps-y-prioridad|El montículo]]` guarda la cabeza de cada
vuelta; sacar el mínimo es una operación `O(log k)`, así que fusionar cuesta `O(n log k)`
comparaciones, muy por debajo del `O(n log n)` de ordenar. El número de rondas es
`⌈log_k(n / M)⌉`.

El coste total, medido en registros movidos entre memoria y disco, es:

:::formula
E/S ≈ 2n · (1 + ⌈log_k(n / M)⌉)        con        k ≤ M / B − 1
:::

El `2` de fuera es una lectura más una escritura; el paréntesis cuenta las pasadas: una para
crear las vueltas y una por cada ronda de fusión. La restricción `k ≤ M / B − 1` sale de contar
buffers: hacen falta `k` bloques de entrada y uno de salida, y todos tienen que caber en `M`.

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `n` | Registros que hay que ordenar | registros | La E/S sube en proporción y las vueltas también, así que puede aparecer una ronda nueva |
| `M` | Registros que caben en memoria a la vez | registros | Menos vueltas (`n/M`) y menos rondas; pero `M` es la memoria libre de verdad, no la del equipo |
| `B` | Registros por bloque de disco | registros | Buffers más grandes y menos accesos, pero `k ≤ M/B − 1` se hace más pequeño: bloques enormes obligan a fusionar de pocas en pocas |
| `k` | Vías de la fusión: cuántas vueltas se juntan en cada ronda | vueltas | Las rondas bajan como `log_k(n/M)`, con rendimientos decrecientes: de 4 a 100 vías se ahorra más de la mitad del tráfico y de 100 a 10.000, casi nada |
| `⌈log_k(n/M)⌉` | Rondas de fusión | rondas | Cada ronda multiplica por `k` lo que se junta; con 100 vueltas y `k = 100` sobra una sola ronda |
| `⌈n/M⌉` | Vueltas que produce la fase 1 | ficheros | Con selección por reemplazo baja a la mitad (longitud media `2M`), y eso puede quitar una ronda entera |
:::

:::figura
fichero: ordenacion-externa-rondas-y-vuelta
pie: A la izquierda, el tráfico total de disco al ordenar 10 GB con 100 MB de memoria, según las vías de fusión: cada ronda lee y escribe el conjunto entero, así que pasar de 4 a 128 vías baja el tráfico de 100 a 40 GB, y de ahí ya no baja nadie porque una sola ronda es el mínimo. La curva es un escalón: subir k solo sirve cuando cruza el número de vueltas. A la derecha, la longitud media de cada vuelta medida sobre 20.000 registros con M = 500: llenar la memoria y volcar da vueltas de 500 registros y 40 vueltas, mientras que la selección por reemplazo las alarga hasta 952 de media (el techo teórico es 2M = 1.000) y deja el trabajo en 21 vueltas, que con k = 2 es una ronda menos.
fuente: figuras/ordenacion-externa-1.py
:::

## Ejemplo

Primero a mano, con nueve números y una memoria de tres: `[7, 2, 5, 9, 1, 8, 3, 6, 4]`, `M = 3`,
`k = 2`.

- Fase 1: `[7, 2, 5]` → `[2, 5, 7]`; `[9, 1, 8]` → `[1, 8, 9]`; `[3, 6, 4]` → `[3, 4, 6]`.
  Tres vueltas.
- Ronda 1: fusionar `[2, 5, 7]` con `[1, 8, 9]` → `[1, 2, 5, 7, 8, 9]`.
- Ronda 2: fusionar `[1, 2, 5, 7, 8, 9]` con `[3, 4, 6]` → `[1, 2, 3, 4, 5, 6, 7, 8, 9]`.

Dos rondas, que es exactamente `⌈log₂ 3⌉`. Con `k = 3` habría bastado una sola ronda, y ahí está
la palanca: la `k` que eliges es el número de rondas que te ahorras.

Ahora con tamaño de verdad: 100 millones de registros de 100 bytes son 10 GB, y la máquina puede
dedicar 100 MB a ordenar, o sea `M = 1.000.000` de registros. La fase 1 produce 100 vueltas, y el
tráfico total depende solo de `k`:

| Vías `k` | Rondas | Registros movidos | Tráfico | A 500 MB/s |
| --- | --- | --- | --- | --- |
| 4 | 4 | 1.000 millones | 100 GB | 200 s |
| 10 | 2 | 600 millones | 60 GB | 120 s |
| 100 | 1 | 400 millones | 40 GB | 80 s |

Nadie elige `k = 1.000` aunque las cuentas sigan mejorando: cada vía necesita su buffer, su
descriptor de fichero y su trozo de disco, y con muchas vías el sistema pasa el rato saltando de
un fichero a otro en vez de leer seguido. En la práctica se eligen `k` de decenas, no de miles, y
se compensa con una ronda más. PostgreSQL llama a esto ordenación externa y la dispara justo
cuando la ordenación no cabe en `work_mem`; ese parámetro **es** la `M` de las fórmulas de arriba.

## Código

```python verificable
import heapq

def crear_vueltas(datos, M):
    """Fase 1: trozos que si caben en memoria, ordenados de uno en uno."""
    return [sorted(datos[i:i + M]) for i in range(0, len(datos), M)]

datos = [7, 2, 5, 9, 1, 8, 3, 6, 4]
vueltas = crear_vueltas(datos, 3)
print("vueltas:", vueltas)                       # -> vueltas: [[2, 5, 7], [1, 8, 9], [3, 4, 6]]
print("cuantas vueltas:", len(vueltas))          # -> cuantas vueltas: 3

# Fase 2 con k = 2: cada ronda junta dos vueltas en una. heapq.merge mantiene un monticulo
# con la cabeza de cada vuelta, asi que en memoria solo hay k elementos, no las vueltas.
ronda_1 = list(heapq.merge(vueltas[0], vueltas[1]))
print("ronda 1:", ronda_1)                       # -> ronda 1: [1, 2, 5, 7, 8, 9]
ronda_2 = list(heapq.merge(ronda_1, vueltas[2]))
print("ronda 2:", ronda_2)                       # -> ronda 2: [1, 2, 3, 4, 5, 6, 7, 8, 9]
print("rondas con k=2:", 2)                      # -> rondas con k=2: 2
print("igual que ordenar en memoria:", ronda_2 == sorted(datos))
# -> igual que ordenar en memoria: True
```

```python verificable
import heapq

def fusionar_k(vueltas):
    """Lo que hace heapq.merge por dentro: un monticulo con la cabeza de cada vuelta."""
    monton = [(v[0], i) for i, v in enumerate(vueltas) if v]   # (valor, de que vuelta viene)
    heapq.heapify(monton)                                      # O(k) y se hace una sola vez
    posicion, salida, operaciones = [0] * len(vueltas), [], 0
    while monton:
        valor, i = heapq.heappop(monton)
        operaciones += 1
        salida.append(valor)
        posicion[i] += 1
        if posicion[i] < len(vueltas[i]):
            heapq.heappush(monton, (vueltas[i][posicion[i]], i))
    return salida, operaciones

vueltas = [[2, 5, 7], [1, 8, 9], [3, 4, 6]]
salida, operaciones = fusionar_k(vueltas)
print("fusionado:", salida)              # -> fusionado: [1, 2, 3, 4, 5, 6, 7, 8, 9]
print("operaciones de monticulo:", operaciones)     # -> operaciones de monticulo: 9
# Cada operacion baja a lo sumo log2(k) niveles del monticulo: con k = 3 son 2 niveles
# por registro, y con k = 1.000.000 serian 20. Es el precio de fusionar muchas vias.
print("niveles con k = 1000000:", 20)    # -> niveles con k = 1000000: 20
```

```python verificable
# Cuanto trafico de disco cuesta ordenar segun las vias de la fusion.
def movidos(n, M, k, bytes_registro=100):
    """Registros movidos entre memoria y disco, y numero de rondas de fusion."""
    vueltas, rondas = -(-n // M), 0            # -(-a // b) es la division hacia arriba
    while vueltas > 1:
        vueltas = -(-vueltas // k)             # cada ronda junta k vueltas en una
        rondas += 1
    return 2 * n * (1 + rondas), rondas        # 2n al crear vueltas + 2n por ronda

n, M = 100_000_000, 1_000_000                  # 10 GB de registros de 100 bytes, 100 MB de memoria
print("vueltas de la fase 1:", -(-n // M))     # -> vueltas de la fase 1: 100
for k in (4, 10, 100):
    registros, rondas = movidos(n, M, k)
    print(f"k={k:3d}  rondas={rondas}  trafico={registros * 100 / 1e9:5.0f} GB")
# -> k=  4  rondas=4  trafico=  100 GB
# -> k= 10  rondas=2  trafico=   60 GB
# -> k=100  rondas=1  trafico=   40 GB
```

```python verificable
import heapq
import numpy as np

# Seleccion por reemplazo: el monticulo no se vacia del todo, asi que las vueltas salen
# mas largas que M. En datos al azar la longitud media tiende a 2M.
azar = np.random.default_rng(7)
M = 500                                        # registros que caben en memoria
datos = list(azar.integers(0, 10 ** 9, size=20000).tolist())   # el fichero de entrada

i, largos, monton = 0, [], []
while i < len(datos) or monton:
    while len(monton) < M and i < len(datos):
        heapq.heappush(monton, datos[i]); i += 1
    congelados, larga = [], 0
    while monton:
        x = heapq.heappop(monton)              # el menor candidato sale ya a su vuelta
        larga += 1
        if i < len(datos):
            nuevo = datos[i]; i += 1
            if nuevo >= x:                     # encaja detras de x: sigue en esta vuelta
                heapq.heappush(monton, nuevo)
            else:
                congelados.append(nuevo)       # ya no: espera a la vuelta siguiente
    largos.append(larga)
    monton = congelados
    heapq.heapify(monton)

print("vueltas:", len(largos))                          # -> vueltas: 21
print("longitud media:", round(sum(largos) / len(largos)))   # -> longitud media: 952
print("vueltas de M en M serian:", -(-len(datos) // M))      # -> vueltas de M en M serian: 40
```

:::claves
- `heapq.merge` es **perezosa**: no construye la lista fusionada hasta que la recorres, y mantiene solo `k` elementos en memoria. Por eso sirve aunque cada vuelta sea enorme; lo que no sirve es envolverla en `list()` si la salida tampoco cabe.
- El montículo de `k` vías cuesta `O(log k)` por registro, pero `k` aparece también en los buffers: con `k` vías hacen falta `k + 1` bloques en memoria (`k` de entrada y uno de salida), y de ahí sale la restricción `k ≤ M/B − 1`.
- `-(-a // b)` es la división entera **hacia arriba**. Con `math.ceil(a / b)` el resultado es el mismo, pero pasa por coma flotante y con números de más de 15 cifras deja de ser exacto.
- En la selección por reemplazo, un registro que entra en el montículo **no** puede salir antes que el último que salió: por eso, cuando el nuevo es menor, se aparta. Si lo metieras en el mismo montículo, la vuelta saldría desordenada.
- Las vueltas se escriben y se leen **secuencialmente**; eso es lo que las hace rápidas. Fusionar cien vueltas a la vez convierte la lectura secuencial en cien lecturas que se van turnando: en un disco mecánico eso es dramático y en un SSD se nota menos, pero se nota.
- El error de bulto que hay que evitar: `sorted()` sobre algo que no cabe. En Python, `sorted(fichero)` primero materializa todo en una lista; no existe magia, la ordenación externa hay que escribirla (o dejar que la haga el motor: [[duckdb-y-analitica-local|DuckDB]], Polars o Spark ya la tienen hecha).
:::

## Errores típicos

- **Creer que «cabe en memoria» es el tamaño del fichero.** Un [[parquet-avro-orc|Parquet]] de
  500 MB puede ocupar 2 GB descomprimido en un DataFrame, y pandas necesita además memoria extra
  para ordenar (Timsort, el que usa por defecto, pide hasta `n/2` elementos más). La `M` de las
  fórmulas es la memoria libre **del formato en memoria**, no los bytes del disco.
- **Ajustar `k` al número de vueltas sin mirar la memoria.** Con `k = 100` y bloques de 1 MB hacen
  falta 101 MB solo en buffers. Si `M` eran 64 MB, el sistema empieza a paginar y el algoritmo se
  vuelve cien veces más lento.
- **Optimizar las comparaciones cuando el cuello de botella es el disco.** Añadir un `key=` para
  comparar enteros en vez de cadenas ayuda, pero si estás moviendo 100 GB del disco, el trabajo de
  comparar es ruido. La palanca grande es el número de rondas: la `k` y la memoria.
- **No dejar sitio para la salida.** Un `ORDER BY` sobre 500 GB escribe un resultado ordenado que
  puede ser tan grande como la entrada. Si el disco está al 95 %, el fallo no es de memoria: es
  que no hay dónde escribir.
- **Ignorar de dónde vienen los datos ya ordenados.** Si la tabla ya está ordenada por la clave
  (por ejemplo, porque hay un índice agrupado), la fase 1 no existe y la fusión sola mueve `2n`
  registros: una lectura y una escritura. Ese es el caso en el que la ordenación externa sale casi
  gratis.
- **Medir con datos pequeños.** Con 10.000 registros, `sorted()` gana siempre porque no toca el
  disco. Las ventajas de la ordenación externa aparecen cuando `n` supera a `M`, y ahí el
  cronómetro depende del disco, no de Python.

:::trampa
Elegir `k = ⌈n/M⌉` para «hacerlo en una sola ronda» es la trampa clásica. En una sola ronda
necesitas `k` buffers abiertos y `k` posiciones distintas de lectura: cien ficheros abiertos a la
vez y el sistema de ficheros leyendo saltos. La `k` buena no es la que minimiza las rondas, es la
que minimiza el tiempo total, y ese tiene un mínimo en valores moderados.
:::

:::nota
La ordenación externa es la mitad del **sort-merge join**: si las dos tablas que hay que unir
llegan ordenadas por la clave, unirlas cuesta una sola pasada con dos punteros, y si no llegan
ordenadas, alguien tiene que pagar esta ordenación antes. Por eso los motores prefieren un índice
ordenado cuando la consulta ordena y une a la vez.
:::

:::practica
enunciado: Tienes 20 GB de registros, la máquina puede dedicar 256 MB a ordenar y el bloque de disco es de 64 KB. Calcula cuántas vueltas produce la fase 1 con selección por reemplazo y sin ella, cuántas rondas hacen falta con k = 32 y cuánto tráfico de disco supone.
pista: Las vueltas son el cociente hacia arriba entre el tamaño total y la memoria; con selección por reemplazo la longitud media de vuelta es 2M, así que son la mitad. Cada ronda mueve el conjunto entero dos veces (una de lectura y otra de escritura).
solucion: Sin selección por reemplazo, las vueltas son 20 GB / 256 MB = 80. Con selección por reemplazo, la longitud media es 2M = 512 MB, así que salen unas 40 vueltas. Con k = 32: la primera ronda junta 80 vueltas en ⌈80/32⌉ = 3 vueltas y la segunda las deja en 1, o sea 2 rondas (con 40 vueltas también son 2 rondas: ⌈40/32⌉ = 2 y luego 1). Tráfico: la fase 1 mueve 2 · 20 = 40 GB y cada ronda otros 40 GB, así que 3 pasadas completas son 120 GB. El bloque de 64 KB no cambia estas cuentas, pero fija la restricción de memoria: k ≤ 256 MB / 64 KB − 1 = 4.095, así que k = 32 cabe de sobra.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Cuánta memoria necesita la fase de fusión de una ordenación externa?
o: Tanto como el fichero más grande que se está fusionando
o: Un elemento por cada vuelta que se fusiona, más el bloque de salida, independientemente del tamaño de los datos
o: La mitad de la memoria usada en la fase 1
a: 2
e: La fusión solo necesita tener a la vista la cabeza de cada una de las k vueltas, así que su memoria es O(k) elementos más el buffer de escritura: no depende del tamaño de los datos. Por eso funciona con 500 GB y 64 MB de RAM. La fase 1 sí necesita M elementos, que es lo que define el tamaño de cada vuelta.
:::

:::quiz
p: Con 100 vueltas ordenadas en disco, ¿cuántas rondas de fusión hacen falta con k = 10 y con k = 100?
o: 2 rondas con k = 10 y 1 ronda con k = 100
o: 10 rondas con k = 10 y 100 rondas con k = 100
o: Las mismas en los dos casos, porque el trabajo total es el mismo
a: 1
e: Con k = 10, la primera ronda junta 100 vueltas en 10 y la segunda las deja en 1: dos rondas, o sea tres pasadas completas de lectura y escritura contando la fase 1. Con k = 100 sobra una sola ronda. El trabajo de comparar es menor con k = 10 (el montículo es más bajo), pero el de disco domina y por eso gana la k grande.
:::

:::quiz
p: ¿Qué gana la selección por reemplazo frente a llenar la memoria, ordenarla y volcarla?
o: Nada, es solo una forma más elegante de escribir lo mismo
o: Vueltas de longitud media 2M en vez de M, así que hay la mitad de vueltas y puede ahorrarse una ronda de fusión
o: Elimina la necesidad de la fase de fusión
a: 2
e: Al sacar el mínimo del montículo y admitir el registro nuevo solo si es mayor que el último que salió, cada vuelta se alarga hasta unas 2M de media con datos al azar. La mitad de vueltas significa una ronda menos cuando el número de vueltas está justo por encima de una potencia de k. La fusión sigue siendo imprescindible: las vueltas siguen siendo muchas.
:::
