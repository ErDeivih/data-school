---
id: gestion-de-memoria
titulo: Gestión de memoria
fase: 11
nivel: avanzado
rutas: [alg, de]
prerequisitos: [tipos-y-estructuras-python, vistas-y-copias, arrow-y-formatos-columnares]
tags: [memoria, python, rendimiento, spark]
resumen: Como se reserva y se libera la memoria de un proceso, por qué el recolector no lo arregla todo y por qué un trabajo de Spark se queda sin memoria.
fuentes: ["Drepper (2007), 'What Every Programmer Should Know About Memory'", "Chambers, Zaharia (2018), 'Spark: The Definitive Guide'"]
---

## En una frase

La memoria de un proceso es un presupuesto finito que se reparte entre pilas, montón,
buffers y copias; saber quién reserva y quién libera cada byte es lo que separa un script que
aguanta de uno que muere con `MemoryError` a las tres de la mañana.

## La idea

Piensa en un almacén de mudanzas. Cada objeto es una caja, y una variable es una etiqueta
pegada a la caja: en Python no mueves la caja, pegas otra etiqueta. Cuando la última etiqueta
de una caja desaparece, la caja se tira en el momento (eso es el **conteo de referencias**).
El problema son las cajas atadas entre sí con cuerdas: si la caja A sujeta a la B y la B sujeta
a la A, puedes arrancar todas las etiquetas y las dos siguen ahí, formando una isla
inalcanzable. Para eso existe el **recolector de ciclos**, que de vez en cuando recorre las
cajas buscando islas y las desmonta.

Ese modelo explica ya casi todo lo que pasa en producción:

- **La memoria se libera sola, pero no siempre.** Sin ciclos, en cuanto una variable sale de
  ámbito la memoria vuelve al asignador. Con ciclos, hay que esperar al recolector.
- **Liberar no es devolver.** El asignador de Python (`pymalloc`) pide bloques grandes al
  sistema operativo y los trocea; cuando liberas objetos pequeños, los trozos vuelven a su
  lista interna, no al sistema. Por eso el consumo del proceso (RSS) puede quedarse alto
  aunque el programa ya no use esos datos. Es memoria disponible para Python, no perdida.
- **Casi todas las «fugas» de Python no son fugas.** No hay punteros perdidos: hay
  referencias que siguen vivas sin que te des cuenta. Un diccionario global usado como caché,
  una función que se guarda en una lista de callbacks, un `lru_cache` sin límite o un
  traceback de excepción que retiene el marco entero de la pila. Si el objeto tiene una
  referencia, no se libera: así de simple y así de fácil de olvidar.

Hay un segundo nivel, que es donde se decide si un pipeline cabe: **cuántas copias existen a
la vez**. Un `DataFrame` de Pandas que se copia en cada transformación, ocho procesos que
reciben el mismo objeto por `pickle`, o un `collect()` que trae el resultado al driver. En
memoria, la diferencia entre procesar mil millones de filas y no poder procesarlas suele ser
el número de copias, no el algoritmo.

Y el caso famoso: **por qué Spark se queda sin memoria**. Un ejecutor de Spark es una máquina
virtual de Java con un proceso de Python al lado. La memoria del ejecutor se reparte entre
memoria de ejecución (uniones, agregaciones, ordenaciones), memoria de almacenamiento
(`cache`, `persist`) y el espacio libre que sobra; el proceso de Python que ejecuta tus UDF
vive **fuera** de ese heap y no lo ve el mismo contador. Cuando un trabajo muere, casi siempre
es por una de estas cuatro: cachear todo, mover demasiados datos en un `shuffle`
([[spark-particiones-y-shuffle]]), una partición muchísimo más grande que las demás, o traer
el resultado al driver con `collect()` o `toPandas()`.

## Definición formal

**Tamaño de un objeto.** `sys.getsizeof(x)` devuelve los bytes de la cabecera más la carga
inmediata de `x`, y **no** cuenta los objetos a los que `x` apunta:

- `x` — cualquier objeto.
- Cabecera en CPython — un contador de referencias y un puntero al tipo: 16 bytes en una
  máquina de 64 bits, más lo que ocupe el objeto.
- **Tamaño profundo** de `x` — la suma de los tamaños de todo el grafo alcanzable desde `x`,
  contando una sola vez los objetos compartidos. Es el número que te interesa y el que no te
  da la biblioteca estándar.

**El contador de referencias.** Cada objeto guarda cuántas referencias apuntan a él. Cuando
baja a cero, se libera de inmediato. Un ciclo (`A → B → A`) nunca llega a cero por sí solo:
lo rompe el recolector generacional, que agrupa los objetos por edad (generaciones 0, 1 y 2) y
revisa antes los jóvenes, porque la hipótesis de partida es que casi todo lo que se crea muere
joven.

**Presupuesto de memoria de un proceso.** De forma aproximada:

:::formula
RSS ≈ heap_de_Python + buffers_nativos + pilas_de_los_hilos + código_y_bibliotecas
:::

- **RSS** — *resident set size*: los bytes que el sistema operativo tiene realmente en RAM
  para el proceso. Es la cifra que vigila el contenedor y la que dispara el *out of memory*.
- **heap_de_Python** — objetos vivos más los huecos que `pymalloc` conserva.
- **buffers_nativos** — memoria pedida por NumPy, Arrow o una biblioteca en C, que no pasa
  por el asignador de Python y por eso no aparece en un perfil de memoria de Python.

De ahí sale la desigualdad que explica los sustos: `RSS ≥ memoria_viva`, y con frecuencia
bastante mayor, porque los huecos no se devuelven.

**Coste de copiar entre procesos.** Con `N` procesos trabajadores y un objeto de `M` bytes
enviado por `pickle`:

:::formula
memoria_total ≈ M × (N + 1)    frente a    M con memoria compartida
:::

El `+ 1` es el padre. Pasar de 8 a 16 trabajadores no acelera nada si el objeto pesa más que
la memoria de la máquina: lo que hace es multiplicar las copias.

:::figura
fichero: gestion-de-memoria-copias-por-proceso
pie: Izquierda, el presupuesto de repartir un `DataFrame` de 2 GiB entre 8 trabajadores por `pickle`: el padre conserva su copia y cada hijo reconstruye la suya, así que el conjunto pide 18 GiB, nueve veces el dato. Derecha, cómo crece esa cuenta al añadir trabajadores: la línea roja sube 2 GiB por proceso, mientras que con memoria compartida el dato se queda en 2 GiB pasen los procesos que pasen. Por eso el error clásico no es elegir mal el algoritmo: es mandar la tabla entera a cada tarea.
fuente: figuras/gestion-de-memoria-1.py
:::

## Ejemplo

Doscientas mil filas de números enteros, guardadas de tres maneras:

- Lista de enteros de Python: 6,9 MiB.
- Array de NumPy `int64`: 1,5 MiB.
- Serie de Pandas sobre ese array: 1,5 MiB.

La lista ocupa **4,5 veces más** porque cada entero es un objeto independiente con su
cabecera: en una máquina de 64 bits, 28 bytes por entero más 8 bytes del puntero en la lista,
frente a 8 bytes planos del `int64`. Con 200.000 filas da igual; con 200 millones es la
diferencia entre caber y no caber. La regla práctica: **antes de optimizar, cambia de
representación** ([[arrow-y-formatos-columnares]], [[vistas-y-copias]]).

Segundo ejemplo, el presupuesto de un ejecutor de Spark con los valores por defecto
(`spark.memory.fraction = 0,6`, `spark.memory.storageFraction = 0,5`, 300 MB reservados):

- Memoria del ejecutor: 8 GB.
- Memoria sobre la que se reparte todo: 0,6 × (8 − 0,3) = **4,62 GB**.
- Mitad de ese espacio disponible para `cache`: 0,5 × 4,62 = **2,31 GB**.

Si cacheas una tabla de 6 GB, no cabe: el ejecutor irá expulsando bloques cacheados para
hacer sitio a las ordenaciones o se irá a disco. El error no fue el algoritmo, fue un
presupuesto mal calculado.

## Código

```python verificable
import sys

import numpy as np
import pandas as pd

n = 200_000
lista = list(range(n))                    # cada entero es un objeto con su cabecera
array = np.arange(n, dtype=np.int64)      # memoria continua: 8 bytes por numero
serie = pd.Series(array)                  # pandas COPIA el array: la Serie ocupa otros 1,5 MiB

# getsizeof(lista) solo cuenta los punteros; hay que sumar cada entero por separado.
bytes_lista = sys.getsizeof(lista) + sum(map(sys.getsizeof, lista))

print(f"lista de enteros   {bytes_lista / 1024 / 1024:5.1f} MiB")   # ->   6.9 MiB
print(f"array de numpy     {array.nbytes / 1024 / 1024:5.1f} MiB")  # ->   1.5 MiB
# deep=True cuenta el contenido de las columnas de objetos; con el dtype de texto nuevo
# (pandas 3) las dos formas dan lo mismo porque los textos ya se guardan en un buffer.
print(f"serie de pandas    {serie.memory_usage(deep=True) / 1024 / 1024:5.1f} MiB")  # ->   1.5 MiB
print(f"factor lista/array {bytes_lista / array.nbytes:.1f} x")     # -> 4.5 x
```

:::claves
- `sys.getsizeof(lista)` devuelve **solo la lista**: la cabecera y los 200.000 punteros, unos
  1,5 MiB. Los enteros a los que apunta no aparecen por ninguna parte, y son 5,3 MiB de los 6,9.
  La suma con `map(sys.getsizeof, lista)` es la forma manual de recorrer el grafo; para un
  objeto anidado de verdad, `getsizeof` miente por un factor de cuatro o más.
- `array.nbytes` son los bytes **de los datos**, sin la cabecera del objeto NumPy: 1,5 MiB
  frente a los 1,5 MiB de punteros de la lista. Mismo dato, misma operación, y una cuarta parte
  del espacio.
- `pd.Series(array)` **copia** el array, no lo envuelve: pandas 3 deja la Serie con su propio
  búfer (`np.shares_memory(array, serie.to_numpy())` da `False`), así que en memoria hay 1,5 MiB
  del array y otros 1,5 de la Serie. Es justo el tipo de copia invisible que agota un contenedor.
- `memory_usage(deep=True)` solo cambia la cifra con columnas de `dtype=object`, donde sin
  `deep` se cuentan punteros y no textos. Con el dtype de texto nuevo de pandas 3 las dos formas
  coinciden, porque los textos viven en un búfer continuo y no como objetos sueltos.
- `sys.getrefcount(a)` devuelve **una referencia de más**, la del argumento que se acaba de
  pasar a la función. Por eso el resultado es 3 y no 2: dos variables más una temporal. Un
  contador de 3 tampoco significa tres variables, significa tres referencias, que pueden venir
  de una lista, un atributo o un marco de pila.
- `weakref.ref(a)` no cuenta como referencia, así que **no impide que el objeto muera**: es la
  herramienta para observar la liberación sin provocarla. Llamar a `vigilante()` después de
  `gc.collect()` devuelve `None`, y con eso se comprueba que el ciclo se rompió.
- `del a, b` borra los **nombres**, no los objetos. Con un ciclo, el contador de cada nodo se
  queda en 1 (lo que le apunta el otro) y nada se libera: por eso la línea siguiente imprime
  `True`. `gc.collect()` devuelve 2 porque son los dos nodos del ciclo, y solo después de esa
  llamada el `weakref` pasa a `None`.
:::

```python verificable
import gc
import sys
import weakref

gc.disable()                             # decidimos nosotros cuando se libera la memoria

class Nodo:
    def __init__(self, nombre):
        self.nombre = nombre
        self.siguiente = None

a, b = Nodo("a"), Nodo("b")
a.siguiente, b.siguiente = b, a          # ciclo: se apuntan el uno al otro
# Referencia debil: deja mirar el objeto sin contarle una referencia (no impide liberarlo).
vigilante = weakref.ref(a)

# getrefcount devuelve una referencia de mas: la del argumento que se acaba de pasar.
print("referencias a 'a':", sys.getrefcount(a))                  # -> 3
del a, b                                 # se sueltan las etiquetas; el ciclo sigue vivo
print("el ciclo sigue vivo:", vigilante() is not None)           # -> True
liberados = gc.collect()                 # el recolector generacional rompe el ciclo
print("objetos liberados:", liberados)                           # -> 2
print("ahora si esta libre:", vigilante() is None)               # -> True
gc.enable()                              # devolvemos el recolector automatico a su estado
```

```python verificable
import numpy as np

base = np.arange(5, dtype=np.int64)
vista = base[1:4]                        # vista: comparte el mismo bloque de memoria
vista[0] = 99                            # escribir en la vista cambia el array original
print("base tras escribir en la vista:", base.tolist())     # -> [0, 99, 2, 3, 4]

copia = base[1:4].copy()                 # copy() reserva memoria nueva: ya es independiente
copia[0] = -1
print("base tras escribir en la copia:", base.tolist())     # -> [0, 99, 2, 3, 4]

print("la vista comparte el buffer:", vista.base is base)   # -> True
print("bytes afectados:", vista.nbytes, "de", base.nbytes)  # -> 24 de 40
```

## Errores típicos

- **Medir con `sys.getsizeof` y creerse el número.** Para una lista de un millón de objetos
  devuelve lo que ocupan los punteros, no los objetos. Suma el tamaño de lo referenciado o usa
  una herramienta que recorra el grafo; si no, subestimas por un factor de cuatro o más.
- **Creer que `del` devuelve la memoria al sistema operativo.** Libera la referencia y el
  objeto puede morir, pero el asignador conserva los bloques para reutilizarlos: el RSS no
  baja y el contenedor sigue contando esos bytes. Si el pico importa, hay que evitar el pico,
  no limpiar después.
- **Cachés sin límite.** Un diccionario global que crece con cada petición, un `lru_cache`
  sin `maxsize` o un `dict` de resultados por clave de alta cardinalidad son la fuga más común
  en Python. Pon límite, política de expulsión y una métrica de tamaño.
- **Retener sin querer.** Un traceback de excepción guarda el marco entero con sus locales; una
  lista de callbacks que nunca se vacía; una figura de Matplotlib que no se cierra; un
  `logging.Handler` que se queda con objetos. En todos estos casos el objeto está vivo porque
  algo lo referencia, y el recolector no puede hacer nada.
- **Repartir un objeto grande copiándolo.** Con `multiprocessing`, cada proceso recibe su
  propia copia por `pickle`. Ocho trabajadores con una tabla de 2 GB piden 18 GB. Usa memoria
  compartida, `mmap` o buffers de Arrow cuando el dato es de solo lectura.
- **Cachear todo en Spark para «ir más rápido».** `cache()` compite por el mismo espacio que
  las ordenaciones y las uniones. Si el conjunto no se reutiliza varias veces, cachear solo
  añade presión de memoria y expulsiones.
- **Traer el resultado al driver.** `collect()` y `toPandas()` mueven todos los datos a un
  solo proceso, que es el que tiene menos memoria de todo el clúster. Agrega antes de
  recolectar o escribe a un fichero y léelo por partes.

## Comprueba que lo sabes

:::quiz
p: Una lista de Python con un millón de enteros ocupa unos 34 MiB, pero `sys.getsizeof(lista)` devuelve alrededor de 8 MiB. ¿Por qué?
o: Porque la lista comprime los enteros repetidos
o: Porque `sys.getsizeof` solo cuenta los punteros y la cabecera de la lista, no los objetos a los que apunta
o: Porque los enteros pequeños se guardan en la pila y no cuentan
a: 2
e: Una lista guarda punteros: 8 MiB para un millón de posiciones. Cada entero es además un objeto independiente de 28 bytes, y esos bytes no los ve `getsizeof` porque la lista solo apunta a ellos. La memoria de un objeto solo se entiende recorriendo el grafo de referencias.
:::

:::quiz
p: ¿Por qué el consumo de memoria del proceso (RSS) no baja después de liberar muchos objetos pequeños en Python?
o: Porque el recolector de basura nunca devuelve memoria
o: Porque el asignador conserva los bloques libres para reutilizarlos dentro del proceso
o: Porque el sistema operativo retiene una copia de cada objeto liberado
a: 2
e: `pymalloc` pide bloques grandes al sistema y los trocea; al liberar, los trozos vuelven a sus listas internas. Esa memoria sigue asignada al proceso y disponible para Python, pero no se devuelve al sistema. El recolector de ciclos no tiene nada que ver aquí: hablamos de objetos sin ciclos.
:::

:::quiz
p: Tienes 8 procesos trabajadores y les pasas por `pickle` un DataFrame de 2 GB. ¿Cuánta memoria pide el conjunto, como mínimo?
o: 2 GB, porque el sistema operativo comparte la memoria entre procesos
o: Unos 18 GB: el padre más ocho copias completas
o: 16 GB, porque el padre no cuenta
a: 2
e: `pickle` serializa y cada proceso reconstruye su propio objeto: no hay memoria compartida. El padre conserva su copia y cada uno de los ocho trabajadores la suya. Para datos de solo lectura, `shared_memory`, `mmap` o los buffers de Arrow evitan las copias.
:::

:::trampa
Un `MemoryError` en Spark no siempre es un problema de datos: puede ser el driver. Si el
trabajo muere justo después de un `toPandas()` o de un `collect()`, el que se quedó sin
memoria es tu proceso de cliente, no el clúster, y añadir ejecutores no arregla nada.
:::

:::aviso
Medir la memoria de un proceso desde dentro de Python solo ve una parte: NumPy, Arrow, las
bibliotecas en C y el motor de la base de datos reservan memoria que no pasa por el asignador
de Python. Cuando el contenedor mata el proceso por exceso de memoria, la cifra que manda es
el RSS del sistema, no la del perfilador.
:::
