---
id: numpy-fundamentos
titulo: NumPy: fundamentos
fase: 3
nivel: básico
rutas: [core, de, ds]
prerequisitos: [tipos-y-estructuras-python, entorno-python]
tags: [numpy, arrays, rendimiento]
resumen: Un ndarray es memoria contigua con un tipo fijo para todos los elementos: la misma operación sobre un millón de números, sin recorrerlos uno a uno en Python.
fuentes: ["Harris et al. (2020), 'Array programming with NumPy', Nature", "McKinney (2017), 'Python for Data Analysis'"]
---

## En una frase

NumPy guarda los números pegados en memoria, todos del mismo tipo, y ejecuta cada operación
sobre el array entero en código compilado: por eso multiplicar un millón de precios por 1,21
tarda milisegundos y el mismo cálculo con un bucle de Python tarda un cuarto de segundo.

## La idea

Una lista de Python es una fila de cajas independientes. Cada hueco guarda un **puntero** a un
objeto, y ese objeto lleva su tipo, su contador de referencias y su valor. Para sumar una lista
de un millón de números, Python va caja por caja: mira el tipo de cada objeto, extrae el número,
lo acumula y crea objetos nuevos por el camino. Un `ndarray` hace lo contrario: reserva un único
bloque de memoria, decide **una vez** el tipo de todos los elementos (8 bytes por `float64`, por
ejemplo) y coloca los valores uno detrás de otro. Sumar el array es entonces un bucle en C sobre
posiciones de memoria consecutivas.

De ahí salen las razones por las que es rápido, y conviene tenerlas claras porque explican
también cuándo **no** lo es:

1. **No hay cajas.** No se comprueba el tipo elemento a elemento ni se crea un objeto por
   número.
2. **La memoria es continua.** El procesador lee bloques enteros y la caché acierta casi
   siempre; con objetos repartidos por el montón, cada acceso puede ser un fallo de caché.
3. **Se aprovechan las instrucciones vectoriales del procesador.** El bucle en C puede operar
   sobre varios números a la vez con una sola instrucción.

Medido en el equipo donde se escribió este ejemplo: recorrer con un bucle una lista de 500.000
`float` ya creada ronda los 50 ms, indexar el array de NumPy en cada vuelta (cada `v[i]` construye
un objeto escalar nuevo: lo peor de los dos mundos) sube a unos 200 ms, y `v.sum()` se queda
alrededor de 1,5 ms. En otra máquina los números cambian; el orden de magnitud, no.

La consecuencia práctica es una forma de pensar: **una operación, un array entero**. Cada vez
que escribas un `for` sobre los elementos de un array, pregúntate si existe la versión en array
(eso es [[vectorizacion]]). Y cuando el resultado tenga una forma distinta a la de las entradas,
el mecanismo que lo resuelve sin bucles es [[numpy-broadcasting]].

:::nota
NumPy no es solo «listas rápidas». Trae álgebra lineal (`np.linalg`), generadores aleatorios con
semilla (`np.random.default_rng`), estadística descriptiva (`mean`, `std`, `percentile`) y
máscaras booleanas. Todo el ecosistema de datos de Python —Pandas, Polars, scikit-learn,
Matplotlib— habla este formato por debajo.
:::

## Definición formal

Un `ndarray` son tres piezas: un bloque de memoria con los datos, una **forma** y un **tipo**.

- `shape` — tupla con la longitud de cada eje. `a.shape == (3, 4)` es una tabla de 3 filas y 4
  columnas.
- `ndim` — número de ejes, el `len` de `shape`. 1 es un vector, 2 una matriz.
- `size` — número total de elementos: el producto de `shape`, 12 en el ejemplo anterior.
- `dtype` — tipo de cada elemento, con ancho fijo: `int64`, `float32`, `float64`, `bool`,
  `datetime64[ns]`.
- `itemsize` — bytes por elemento: 8 para `float64`.
- `nbytes` — bytes totales del bloque de datos.
- `strides` — bytes que hay que saltar en memoria para avanzar una posición en cada eje.

:::formula
offset(i₁, …, i_k) = Σ_k i_k · strides_k          nbytes = size · itemsize
:::

Con memoria contigua en orden C (el último eje varía más rápido), el elemento `m[2, 3]` de una
matriz `float64` de forma `(3, 4)` vive en el byte `2 · 32 + 3 · 8 = 88` del bloque: 32 son los
bytes de una fila y 8 los de un `float64`.

Dos reglas de indexado que hay que tener grabadas, porque explican casi todos los sustos:

- **Rebanada básica** (`a[1:4]`, `a[:, 0]`, `a[::2]`) devuelve una **vista**: otro punto de vista
  sobre la misma memoria. No copia nada.
- **Indexado avanzado** (`a[[0, 2, 5]]`, `a[a > 0]`) devuelve una **copia** con memoria nueva.

Esa diferencia es la protagonista de [[vistas-y-copias]]: escribir en una vista cambia el array
original, y ese bug no avisa.

## Ejemplo

Una matriz `m` construida con `np.arange(12).reshape(3, 4)`, es decir `int64` y contigua:

```
m = [[ 0,  1,  2,  3],
     [ 4,  5,  6,  7],
     [ 8,  9, 10, 11]]
```

- `shape` = (3, 4): 3 filas, 4 columnas. `ndim` = 2, `size` = 12.
- `itemsize` = 8 bytes (un `int64`), así que `nbytes` = 12 · 8 = **96 bytes**.
- `strides` = (32, 8): una fila son 4 columnas de 8 bytes = 32; una columna son 8.
- `m[2, 3]` está en el byte `2·32 + 3·8 = 88`, que es el último del bloque, y vale 11.
- `m[1:3]` es una **vista** de las filas 1 y 2: sigue apuntando al mismo bloque, solo cambia el
  puntero de inicio y la forma a (2, 4).
- `m[[1, 2]]` es una **copia**: 2 · 4 · 8 = 64 bytes nuevos.

Sumar por ejes concreta la regla del `axis`: `m.sum(axis=0)` recorre las filas para cada columna
y devuelve 4 valores, `[12, 15, 18, 21]`; `m.sum(axis=1)` devuelve 3 valores, `[6, 22, 38]`.
El eje que nombras es el que desaparece del resultado.

## Código

```python verificable
import numpy as np

a = np.array([1, 2, 3])                  # enteros: el dtype por defecto es int64
b = np.array([1.0, 2, 3])                # basta un float para que todo el array sea float64
print(a.dtype, a.shape, a.nbytes)        # -> int64 (3,) 24
print(b.dtype, b.nbytes)                 # -> float64 24
print((a / 2).dtype)                     # -> float64  (la division nunca devuelve enteros)

m = np.arange(12).reshape(3, 4)          # 3 filas x 4 columnas de int64
print(m.shape, m.ndim, m.size, m.nbytes) # -> (3, 4) 2 12 96
print(m.strides)                         # -> (32, 8)  (32 bytes por fila, 8 por columna)
print(m[2, 3])                           # -> 11
```

```python verificable
import numpy as np

m = np.arange(12).reshape(3, 4)

# El axis que se pasa es el que se pliega (el que desaparece del resultado)
print(m.sum(axis=0).tolist())   # -> [12, 15, 18, 21]  (una suma por columna)
print(m.sum(axis=1).tolist())   # -> [6, 22, 38]       (una suma por fila)
print(m.sum().tolist())         # -> 66               (sin axis se suman los 12 elementos)
```

```python verificable
import time

import numpy as np

v = np.arange(500_000, dtype=np.float64)
lista = v.tolist()

t0 = time.perf_counter()
a1 = 0.0
for x in lista:             # la forma mas rapida de recorrer en Python: lista de floats
    a1 += x
t1 = time.perf_counter()
a2 = 0.0
for i in range(v.size):     # indexar el array en cada vuelta es peor: crea un escalar nuevo
    a2 += v[i]
t2 = time.perf_counter()
total = float(v.sum())      # un unico bucle en C sobre memoria contigua
t3 = time.perf_counter()

print(f"bucle sobre lista  {1000 * (t1 - t0):.0f} ms")   # los tiempos dependen de la maquina
print(f"bucle indexando    {1000 * (t2 - t1):.0f} ms")
print(f"numpy              {1000 * (t3 - t2):.2f} ms")
print("mismo resultado:", abs(a1 - total) < 1e-6 and abs(a2 - total) < 1e-6)   # -> mismo resultado: True

# Los tipos tienen ancho fijo: si te pasas del rango no hay error, hay vuelta a empezar
c = np.array([120], dtype=np.int8)
print((c + np.int8(10)).tolist())   # -> [-126]
```

## Errores típicos

- **Crecer el array dentro de un bucle.** `np.append` y `np.concatenate` reservan memoria nueva
  y copian todo lo anterior, así que un bucle de `n` pasos cuesta O(n²) y pasa de un segundo a
  varios minutos. Guarda los trozos en una lista de Python y haz una sola conversión al final,
  o preasigna con `np.empty` y rellena por posiciones.
- **Confundir `*` con el producto matricial.** `A * B` multiplica elemento a elemento; para
  matrices se usa `A @ B` (ver [[operaciones-matriciales]]). El error es peligroso porque cuando
  las formas coinciden el resultado sale con el tamaño correcto y parece creíble.
- **Suponer que `len(m)` cuenta los elementos.** En una matriz devuelve el tamaño del primer
  eje: `len(m) == 3` y `m.size == 12`.
- **Usar `dtype=object` y esperar velocidad.** Un array de objetos es una lista de punteros con
  envoltorio: se pierden la contigüidad, el tipo fijo y casi toda la ventaja.
- **Acumular en `float32` sin pensarlo.** Tiene 24 bits de mantisa, así que no representa de
  forma exacta los enteros por encima de 16.777.216 y va acumulando error de redondeo en sumas
  largas de valores pequeños. Suma en `float64` (`v.sum(dtype=np.float64)` si el array viene en
  `float32`).
- **Elegir mal el `axis`.** `axis` es el eje que desaparece, no el que se recorre: con forma
  `(filas, columnas)`, una media por fila es `axis=1`.

:::practica
enunciado: Con `m = np.arange(12).reshape(3, 4)` (int64), calcula a mano en qué byte del bloque vive `m[2, 1]`, cuántos bytes ocupa el array y cuánto valen `m.sum(axis=0)` y `m.sum(axis=1)`. Después compruébalo con una línea de NumPy.
pista: El desplazamiento es fila por 32 más columna por 8, y el eje que pasas a `sum` es el que desaparece.
solucion: `m[2, 1]` está en `2·32 + 1·8 = 72`; el array ocupa `size · itemsize = 12 · 8 = 96` bytes. `m.sum(axis=0)` pliega las filas y deja una suma por columna, `[12, 15, 18, 21]`; `m.sum(axis=1)` deja una por fila, `[6, 22, 38]`. Se comprueba con `m.strides`, `m.nbytes` y `m.sum(axis=...)`.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Qué contiene `strides` en un array `float64` de forma `(3, 4)` con memoria contigua?
o: `(3, 4)`, la forma del array
o: `(32, 8)`, los bytes que hay que saltar para avanzar una fila y una columna
o: `8`, los bytes que ocupa un `float64`
a: 2
e: Los strides se miden en bytes, no en elementos: avanzar una fila cuesta 4 columnas de 8 bytes (32) y avanzar una columna cuesta 8. La forma es `shape`, y `8` es `itemsize`.
:::

:::quiz
p: Tienes un array con forma `(1000, 20)` y quieres la media de cada fila. ¿Qué `axis` usas?
o: `axis=0`, porque las filas son el primer eje
o: `axis=1`, porque ese eje es el que se pliega y queda una media por fila
o: Ninguno: hay que recorrer las filas con un bucle
a: 2
e: El `axis` que se pasa es el que desaparece del resultado: al plegar las 20 columnas quedan 1000 medias, una por fila. Con `axis=0` saldrían 20 medias, una por columna, y el bucle es justo lo que NumPy evita.
:::

:::quiz
p: ¿Por qué `a[[0, 2]]` se comporta distinto de `a[0:2]` si después modificas el resultado?
o: Porque `a[[0, 2]]` es una copia y `a[0:2]` es una vista sobre la misma memoria
o: Porque `a[[0, 2]]` devuelve una lista de Python y `a[0:2]` un array
o: Porque `a[0:2]` solo funciona con arrays de enteros
a: 1
e: El indexado con una lista o un array de posiciones construye un array nuevo, mientras que la rebanada básica comparte los mismos bytes. Por eso escribir en la vista cambia el original y escribir en la copia no. Los dos devuelven arrays de NumPy.
:::

:::trampa
`np.append` no añade nada al array: crea uno nuevo y copia los dos. En un bucle de 10.000
iteraciones eso son 10.000 copias crecientes. Acumula en una lista y convierte al final, o
preasigna el array del tamaño final.
:::
