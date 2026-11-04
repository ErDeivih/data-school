---
id: arrays-y-listas
titulo: Arrays y listas
fase: 10
nivel: básico
rutas: [alg, de]
prerequisitos: [tipos-y-estructuras-python, complejidad-asintotica]
tags: [estructuras, memoria, arrays, coste]
resumen: Un array guarda sus elementos uno detrás de otro: por eso el acceso por índice es instantáneo y por eso insertar en el medio obliga a desplazar todo lo demás.
fuentes: ["Cormen, Leiserson, Rivest y Stein (2009), 'Introduction to Algorithms', cap. 10", "Sedgewick y Wayne (2011), 'Algorithms'"]
---

## En una frase

Un array es un bloque de memoria con los elementos uno detrás de otro; eso hace que llegar al
elemento `i` sea una suma y una lectura (coste constante), y que meter o sacar algo del medio
obligue a mover todos los que vienen después.

## La idea

Imagina una fila de taquillas numeradas, pegadas unas a otras en la pared. Si sabes que cada
taquilla mide 40 centímetros y dónde empieza la fila, la taquilla número 37 empieza exactamente
40 · 37 centímetros más allá. No hay que abrir ninguna para contarlas: es aritmética. Eso es un
array.

La segunda consecuencia es menos agradable. Si quieres meter una taquilla nueva en medio de la
fila, no puedes: están pegadas a la pared. Tienes que desplazar una a una todas las que están a
la derecha para hacer sitio, y si la fila es de un millón de taquillas y la insertas al principio,
son un millón de desplazamientos. Sacar una del medio tiene el mismo problema. En cambio, añadir
al final es barato si hay hueco.

Ahí aparece la estructura que usas todo el rato sin llamarla por su nombre: el **array dinámico**.
Reserva más huecos de los que necesita (la *capacidad*) y guarda cuántos usa de verdad (el
*tamaño* o longitud). Añadir al final ocupa el siguiente hueco libre; cuando se acaban, pide un
bloque del doble de tamaño y copia todo. Ese «cada mucho tiempo copio todo» es exactamente lo que
demuestra el [[analisis-amortizado]]: el coste acaba siendo una constante por operación. La
lista de Python, el `vector` de C++ y el `ArrayList` de Java son esto.

La confusión más común es pensar que una lista de Python es «un array de enteros». No lo es: es un
array **de punteros**. Cada casilla guarda la dirección de memoria donde vive el objeto, que está
en otra parte y ocupa lo suyo (un entero de Python son 28 bytes; una lista de un millón de
elementos gasta 8 MB solo en punteros, más unos 28 MB en los enteros). Un array de NumPy, en
cambio, guarda los ocho bytes del número pegados y sin intermediarios. Esa diferencia explica por
qué NumPy es rápido y por qué una lista de listas nunca será una matriz.

## Definición formal

Un **array** de `n` elementos, cada uno de `s` bytes, que empieza en la dirección `base`:

:::formula
dirección(i) = base + i · s ,  para i = 0, 1, …, n − 1
:::

- `n` — número de elementos guardados.
- `s` — tamaño en bytes de cada elemento (`itemsize` en NumPy).
- `base` — dirección de memoria del primer elemento.
- `i` — índice, contado desde cero.

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `n` | Elementos guardados en el array | elementos | El acceso por índice sigue costando lo mismo; lo que sube es el espacio y el coste de copiar |
| `s` | Bytes que ocupa un elemento (`itemsize`) | bytes | Ocupa más memoria el mismo número de elementos; la dirección del elemento `i` se aleja más |
| `base` | Dirección donde empieza el bloque | dirección de memoria | Nada: es un punto de partida. La distancia al elemento `i` no depende de dónde esté |
| `i` | Índice del elemento, desde cero | entero, 0 ≤ i < n | No encarece el acceso: la dirección se calcula en el mismo número de operaciones |
| `capacidad` | Huecos reservados, de los que `n` están usados | elementos | Más memoria reservada y menos ampliaciones; añadir al final sigue siendo O(1) amortizado |
:::

Costes de un array dinámico con `n` elementos:

| Operación | Coste | Por qué |
| --- | --- | --- |
| Leer o escribir por índice | O(1) | Es la fórmula de arriba: una multiplicación y una suma |
| Añadir al final | O(1) amortizado | Si hay hueco, se ocupa; si no, se duplica y se copia |
| Insertar o borrar en el medio | O(n) | Hay que desplazar todos los elementos posteriores |
| Buscar un valor | O(n) | La posición no depende del valor: hay que mirar uno a uno |
| Copiar el array entero | O(n) | Se duplican los datos |

Y las variantes que conviene tener claras:

- **Array estático:** `n` fijo desde el principio. Sin coste de ampliación, pero si te quedas
  corto no hay solución local.
- **Array dinámico:** tamaño y capacidad separados, con ampliación por duplicación. `len` es O(1)
  porque la longitud está guardada, no se cuenta.
- **NumPy `ndarray`:** bloque contiguo más una tupla de **strides** (saltos en bytes por cada
  dimensión). Un `ndarray` de forma `(3, 4)` de enteros de 8 bytes tiene strides `(32, 8)`: para
  bajar una fila se saltan 32 bytes y para avanzar una columna, 8. Una vista con paso 2 tiene
  stride 16 y comparte memoria con el original: no copia nada.
- **Lista enlazada:** cada nodo guarda su valor y la dirección del siguiente. Acceder al elemento
  `k` cuesta O(k) porque hay que recorrer; insertar es O(1) si ya tienes el nodo anterior, y no
  hay que desplazar a nadie. Pierdes el acceso por índice y la localidad de memoria.

:::figura
fichero: arrays-memoria-y-coste-de-insertar
pie: A la izquierda, los bytes que ocupan los mismos enteros en una lista de Python y en un array de NumPy: las dos rectas son paralelas porque la lista paga 8 bytes de puntero más 28 del objeto, y el array solo 8. La distancia no se cierra al crecer: es 4,5 veces siempre. A la derecha, el mismo trabajo hecho por el principio y por el final de la lista; la curva roja es n²/2 y la verde es 2n, así que con un millón de elementos la diferencia pasa de mil millones de desplazamientos.
fuente: figuras/arrays-y-listas-1.py
:::

## Ejemplo

Un array de NumPy con un millón de enteros de 64 bits:

- Ocupa `1.000.000 · 8 = 8.000.000` bytes, unos 7,63 MiB, sin un solo puntero extra.
- El elemento de la posición 500.000 está a `500.000 · 8 = 4.000.000` bytes del inicio, es decir,
  en el desplazamiento hexadecimal `0x3D0900`. Llegar hasta él es sumar ese desplazamiento a la
  dirección base: una operación, independientemente de que el índice sea 5 o 500.000.
- Ese mismo array con paso 2 (posiciones pares) tiene stride 16 y sigue ocupando los mismos 8 MB:
  es una **vista**, no una copia. Si escribes en la vista, cambias el original.

Ahora el coste de insertar al principio, que es donde se rompe todo. Insertar `n` elementos uno
detrás de otro al principio de una lista desplaza `0 + 1 + 2 + … + (n−1)` elementos:

- Con `n = 1.000`: 499.500 desplazamientos.
- Con `n = 100.000`: 4.999.950.000 desplazamientos, casi 5.000 millones.
- Con `n = 100.000` añadidos **al final**: 131.071 desplazamientos, porque la ampliación por
  duplicación solo copia en las potencias de 2.

El mismo trabajo (meter 100.000 elementos) cuesta 5.000 millones de movimientos o 131.071, según
por dónde entres. Es la diferencia entre un programa que termina y otro que parece colgado.

## Código

```python verificable
import sys

# Una lista de Python guarda punteros: el contenedor y los objetos viven separados.
lista = list(range(1000))
print("contenedor de 1000 elementos (bytes):", sys.getsizeof(lista))  # -> contenedor de 1000 elementos (bytes): 8056
print("un entero suelto (bytes):", sys.getsizeof(1))                  # -> un entero suelto (bytes): 28
print("8 bytes por puntero, 1000 punteros:", 8 * 1000 + 56)           # -> 8 bytes por puntero, 1000 punteros: 8056
```

:::claves
- `sys.getsizeof(lista)` mide **contenedor, no contenido**: devuelve los bytes del array de punteros (más la cabecera), no los 28 bytes de cada entero. Con 1.000 elementos son 8.056 bytes de contenedor y otros 28.000 de enteros repartidos por la memoria. Para medir un array de NumPy, en cambio, `a.nbytes` sí es el total de los datos.
- `len(lista)` es O(1) porque la longitud está guardada en la cabecera; no recorre nada. Y la **capacidad reservada es otra cosa**: `len` puede ser 1.000 mientras la lista tiene hueco para 1.024 o 2.000.
- `a[::2]` y `a.T` son **vistas**: `np.shares_memory(a, vista)` es `True` y escribir en una cambia la otra. Lo único que cambia es `strides`, no los datos. Para una copia independiente, `.copy()`.
- `hex(500000 * a.itemsize)` da `0x3d0900` porque el desplazamiento se calcula **en bytes**, no en elementos: `i · itemsize`. Con el mismo índice y un array `int32` (4 bytes por elemento) el desplazamiento sería la mitad, y la dirección a la que hay que saltar, distinta.
- `lista.insert(0, x)` no «hace sitio» gratis: mueve los `n` elementos que ya había. Cambiar esa línea por `lista.append(x)` dentro de un bucle de 100.000 iteraciones baja de 5.000 millones de desplazamientos a 131.071.
- `lista = lista + [x]` crea una lista **nueva** y copia todo lo anterior, así que sigue siendo O(n) por vuelta aunque el operador parezca inofensivo. `append` modifica la que ya hay y es O(1) amortizado.
:::

```python verificable
import numpy as np

# En un ndarray los elementos van seguidos: la direccion del elemento i es base + i*8.
a = np.arange(1_000_000, dtype=np.int64)
print("bytes del array:", a.nbytes)                    # -> bytes del array: 8000000
print("bytes por elemento:", a.itemsize)               # -> bytes por elemento: 8
print("desplazamiento del elemento 500000:", hex(500000 * a.itemsize))  # -> desplazamiento del elemento 500000: 0x3d0900

# Un trozo con paso 2 NO es contiguo, pero comparte memoria con el original: es una vista.
vista = a[::2]
print("stride de la vista:", vista.strides[0])         # -> stride de la vista: 16
print("comparte memoria:", np.shares_memory(a, vista)) # -> comparte memoria: True
print("elementos de la vista:", vista.size)            # -> elementos de la vista: 500000

# Lo mismo con una matriz: la traspuesta tampoco copia, solo cambia los strides.
m = np.arange(12).reshape(3, 4)
print("strides de la matriz:", m.strides)              # -> strides de la matriz: (32, 8)
print("strides de la traspuesta:", m.T.strides)        # -> strides de la traspuesta: (8, 32)
```

```python verificable
# Insertar al principio contra anadir al final: el mismo numero de elementos, otro coste.
def desplazamientos_al_principio(n):
    total = 0
    for tam in range(n):          # insertamos n elementos, cada uno delante del anterior
        total += tam              # al insertar el numero tam hay que mover los tam previos
    return total

def desplazamientos_al_final(n):
    capacidad, tam, total = 1, 0, 0
    for _ in range(n):
        if tam == capacidad:      # se llena: se duplica y se copia lo que habia
            total += tam
            capacidad *= 2
        tam += 1
    return total

print("1000 al principio:", desplazamientos_al_principio(1000))          # -> 1000 al principio: 499500
print("100000 al principio:", desplazamientos_al_principio(100000))      # -> 100000 al principio: 4999950000
print("100000 al final:", desplazamientos_al_final(100000))              # -> 100000 al final: 131071
```

## Errores típicos

- **Insertar o borrar al principio dentro de un bucle.** `lista.insert(0, x)` es O(n) y dentro de
  un bucle de `n` iteraciones convierte el programa en O(n²): los 5.000 millones de movimientos
  del ejemplo. Si necesitas sacar por delante, usa [[pilas-y-colas|un deque]]; si estás
  construyendo una lista al revés, añade al final y dale la vuelta una sola vez.
- **Creer que una lista de Python guarda los números pegados.** Guarda punteros de 8 bytes y cada
  entero es un objeto aparte de 28 bytes. Con un millón de enteros eso es varias veces más
  memoria que el array equivalente de NumPy, y además cada acceso salta a otra zona de memoria.
- **Construir una lista con `lista = lista + [x]` en un bucle.** El operador `+` crea una lista
  nueva y copia todo lo anterior, así que el bucle entero cuesta O(n²). Usa `append`, que es
  O(1) amortizado.
- **Usar una lista como cola con `pop(0)`.** Es el mismo error que el primero, disfrazado de dos
  caracteres. La estructura correcta es `collections.deque`. Está contado con números en
  [[pilas-y-colas]].
- **Suponer que un trozo de NumPy copia.** `a[::2]`, `a[:100]` y `a.T` son vistas que comparten
  memoria: modificar una modifica la otra, y si el original se libera, la vista puede quedar
  apuntando a memoria que ya no es tuya. Cuando quieras una copia independiente, pide `.copy()`.
  El detalle está en [[vistas-y-copias]].
- **Confundir longitud con capacidad.** `len(lista)` cuenta elementos, no huecos reservados; una
  lista de 1.000 elementos puede tener capacidad para 1.024 o para 2.000. Y `len` es O(1) porque
  la longitud está guardada: nada recorre la lista para contarla.

:::practica
enunciado: Una lista de Python con 2.000.000 de enteros pequeños y un array de NumPy int64 con los mismos números. Calcula los bytes de cada estructura (puntero de 8 bytes, entero de Python de 28) y el factor de diferencia. ¿Cuánto cuesta leer la última posición?
pista: La lista guarda punteros y cada entero es un objeto aparte; el ndarray guarda sus 8 bytes pegados. El acceso por índice es una multiplicación y una suma en ambos casos.
solucion: La lista ocupa 2.000.000 · 8 = 16.000.000 bytes de punteros más 2.000.000 · 28 = 56.000.000 bytes de enteros: 72.000.000 bytes (68,7 MiB). El ndarray ocupa 2.000.000 · 8 = 16.000.000 bytes (15,3 MiB): 4,5 veces menos. Leer la última posición cuesta O(1) en las dos, porque la dirección es base + i · 8. Conclusión: la memoria la decide el puntero extra, no el número.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Por qué leer `array[500000]` cuesta lo mismo que leer `array[5]` en un array contiguo?
o: Porque la posición se calcula con una multiplicación y una suma, sin recorrer nada
o: Porque el array guarda una tabla con la dirección de cada elemento
o: Porque el procesador memoriza los índices que ya has usado
a: 1
e: La dirección del elemento i es base + i · tamaño, así que el coste no depende de i. No hay tabla de direcciones (eso gastaría tanta memoria como los datos) ni caché de índices: es aritmética de direcciones.
:::

:::quiz
p: Tienes que meter 100.000 elementos en una lista. ¿Qué diferencia hay entre insertarlos al principio y añadirlos al final?
o: Ninguna: en los dos casos cada operación es O(1)
o: Al principio se desplazan unos 5.000 millones de elementos; al final, unos 131.071
o: Al final se desplazan 100.000 elementos, uno por cada inserción
a: 2
e: Insertar al principio es O(n) cada vez y sumado da n(n−1)/2, casi 5.000 millones con n = 100.000. Añadir al final solo copia cuando se agota la capacidad, y con duplicación eso suma 131.071 movimientos. Ninguna de las dos es «una operación por inserción».
:::

:::quiz
p: ¿Qué es `a[::2]` cuando `a` es un array de NumPy?
o: Un array nuevo con la mitad de elementos, independiente del original
o: Una vista que comparte memoria con `a` y tiene el doble de stride
o: Una lista de Python con los elementos pares
a: 2
e: Cambiar el paso cambia los strides (de 8 a 16 bytes), pero no se copia ningún dato: la vista comparte memoria, así que escribir en ella modifica `a`. Para tener un array independiente hay que pedir `.copy()`. Y no se convierte en lista: sigue siendo un ndarray.
:::

:::truco
Antes de elegir estructura, pregúntate por dónde entran y salen los datos. Si entran y salen por
el final, una lista basta. Si salen por delante, un `deque`. Si necesitas buscar por clave, un
diccionario. Y si vas a hacer cuentas con millones de números, un array de NumPy: la diferencia
de memoria y de velocidad no es un detalle, es otro orden de magnitud.
:::
