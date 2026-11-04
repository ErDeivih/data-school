---
id: ordenacion
titulo: Algoritmos de ordenación
fase: 10
nivel: intermedio
rutas: [alg, core]
prerequisitos: [complejidad-asintotica, arrays-y-listas]
tags: [algoritmos, ordenacion, comparativas, estabilidad]
resumen: Ordenar es el paso previo de casi todo; quicksort, mergesort, heapsort y counting sort no son intercambiables y la cota inferior es n log n.
fuentes: ["Hoare (1962), 'Quicksort'", "Cormen, Leiserson, Rivest y Stein (2009), 'Introduction to Algorithms', caps. 2, 6, 7 y 8", "Sedgewick y Wayne (2011), 'Algorithms', 4.ª ed., cap. 2"]
---

## En una frase

Ordenar coloca los elementos de menor a mayor con un coste mínimo demostrado de `n · log₂ n`
comparaciones cuando solo se comparan pares, y los distintos algoritmos se diferencian en el
peor caso, en la memoria extra, en si conservan el orden de los elementos iguales y en si
necesitan comparar o pueden contar directamente.

## La idea

Imagina que tienes 20 exámenes que ordenar por nota. Dos formas de hacerlo:

- **Por inserción:** coges el segundo examen, lo comparas con el primero y lo colocas; coges el
  tercero y lo vas moviendo hacia atrás hasta que esté en su sitio. Con 20 exámenes funciona
  perfectamente y es lo que hace todo el mundo a mano. El problema es que cada examen nuevo puede
  tener que recorrer toda la pila: con 10.000 exámenes, el trabajo crece con el cuadrado del
  tamaño.
- **Por mezcla (mergesort):** partes la pila en dos montones, ordenas cada uno por separado
  (partiendo otra vez, hasta llegar a montones de un examen) y luego **fusionas**: comparas las
  dos cabezas y vas sacando el menor. Fusionar dos montones ordenados de tamaño total `n` cuesta
  `n` comparaciones, y hay `log₂ n` niveles de particiones. Ese es el origen de `n · log₂ n`.

Ese `n · log₂ n` no es una casualidad de mergesort: es una **cota inferior**. Si solo puedes
comparar pares de elementos, hay `n!` órdenes posibles y cada comparación solo distingue dos
resultados, así que necesitas al menos `log₂(n!)` comparaciones; la aproximación de Stirling da
`log₂(n!) ≈ n · log₂ n − 1,44 n`. Con un millón de elementos, ninguna ordenación por comparación
puede bajar de unos 18,5 millones de comparaciones. Para saltarse esa barrera hay que dejar de
comparar: **counting sort** cuenta cuántas veces aparece cada valor y reconstruye el array, con
coste `n + k` (y `k` el rango de valores), pero solo sirve con enteros de rango pequeño.

La elección práctica casi nunca es «¿cuál es el más rápido en teoría?», porque los cuatro tienen
el mismo `n log n` en el caso medio. La decisión real es entre tres cosas: **peor caso**
(quicksort sin cuidado es cuadrático, mergesort y heapsort nunca lo son), **memoria**
(mergesort necesita `n` extra, quicksort y heapsort son in-place), y **estabilidad** (¿se
conserva el orden relativo de los elementos que empatan?). Esa última palabra merece un párrafo
propio.

Un algoritmo es **estable** si dos elementos iguales según el criterio de orden mantienen el
orden que tenían en la entrada. Suena a detalle académico y es la causa de la mitad de los bugs
reales: si ordenas una lista de pedidos por importe y quieres que, a igual importe, se respete el
orden de llegada, necesitas un algoritmo estable o un criterio de desempate explícito. Python
usa Timsort, que es estable y además aprovecha los tramos ya ordenados de los datos reales;
`numpy.sort` usa por defecto quicksort (introsort), que **no** es estable, y por eso existe el
argumento `kind="stable"`.

## Definición formal

Sea `a` un array de `n` elementos con una relación de orden total `≤` sobre ellos. Ordenar es
devolver una permutación `a'` de los mismos elementos tal que `a'[i] ≤ a'[i+1]` para todo `i`.

Un algoritmo de ordenación es **estable** si, siempre que `a[i] = a[j]` con `i < j`, en la salida
`a[i]` aparece antes que `a[j]`. Un algoritmo es **in-place** (en el sitio) si usa `O(1)` memoria
extra además del array.

Notación: `n` es el número de elementos, `k` el rango de valores distintos (en los algoritmos de
conteo), `log` es el logaritmo en base 2 salvo que se diga lo contrario.

| Algoritmo | Caso medio | Peor caso | Memoria extra | ¿Estable? | ¿Compara? |
| --- | --- | --- | --- | --- | --- |
| Inserción | n² | n² | 1 | Sí | Sí |
| Mergesort | n log n | n log n | n | Sí | Sí |
| Quicksort | n log n | n² | log n (pila) | No | Sí |
| Heapsort | n log n | n log n | 1 | No | Sí |
| Counting sort | n + k | n + k | n + k | Sí | No |
| Timsort | n log n | n log n | n/2 | Sí | Sí |

**Mergesort.** Divide el array en dos mitades, ordena cada una recursivamente y fusiona las dos
listas ordenadas. Su recurrencia es:

:::formula
T(n) = 2 · T(n/2) + Θ(n)  ⇒  T(n) = Θ(n · log₂ n)
:::

El árbol de recursión tiene `log₂ n` niveles y cada nivel cuesta en total `Θ(n)`; con `n =
1.048.576` son 20 niveles.

**Quicksort.** Elige un **pivote**, reparte los elementos en menores y mayores que él
(*partición*) y se llama recursivamente sobre las dos partes. La partición de Lomuto, la más
fácil de escribir, recorre el array una vez y cuenta `n − 1` comparaciones por nivel. El coste
total es:

:::formula
mejor y medio: Θ(n · log₂ n)      peor: Θ(n²)
:::

El peor caso aparece cuando el pivote es siempre el menor o el mayor: el array ya ordenado con
pivote en el último elemento. Ahí cada partición separa 1 y `n − 1` elementos, y las
comparaciones suman `(n − 1) + (n − 2) + … + 1 = n(n − 1)/2`.

**Heapsort.** Construye un montículo ([[heaps-y-prioridad]]) en `Θ(n)` y extrae el máximo `n`
veces, cada una en `Θ(log n)`. Es la única opción `n log n` garantizada, in-place y sin
recursión profunda, a cambio de peor localidad de memoria: salta por el array en vez de
recorrerlo.

**Counting sort.** Con valores enteros en `[0, k)`, cuenta las apariciones de cada valor, calcula
las posiciones acumuladas y coloca cada elemento en su sitio final. Cuesta `Θ(n + k)` y es
estable si se recorre la entrada de derecha a izquierda al colocar. Con `k` mucho mayor que `n`
(por ejemplo, IDs de 64 bits) es un desperdicio de memoria.

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `n` | Elementos que se ordenan | Elementos | El coste sube como n · log₂ n al comparar y como n + k al contar: duplicar los datos añade un nivel de recursión y algo menos del doble de comparaciones, no el cuádruple |
| `k` | Valores distintos que puede tomar la clave, solo en counting sort y radix sort | Valores | El coste n + k sube y el array de conteo ocupa más: cuando k supera n · log₂ n, contar deja de compensar frente a comparar |
| `log` | Logaritmo en base 2, el que aparece en las recurrencias | Adimensional | Es la altura del árbol de recursión: cada vez que n se duplica, log₂ n sube una unidad, y con ella un nivel más de trabajo |
| `T(n)` | Comparaciones (o tiempo) de ordenar n elementos | Comparaciones u operaciones | En mergesort y heapsort crece como n · log₂ n; en el peor caso de quicksort crece como n², y esa es toda la diferencia entre 512 elementos ordenados en 4.600 comparaciones o en 130.816 |
:::

## Ejemplo

Array `[5, 2, 9, 1, 5, 6]`, ordenado con mergesort contando comparaciones. El array se parte en
`[5, 2, 9]` y `[1, 5, 6]`, y cada mitad sigue bajando hasta elementos sueltos:

- Mitad izquierda: `[5, 2, 9]` se parte en `[5]` y `[2, 9]`; fusionar `[2]` con `[9]` cuesta 1
  comparación y fusionar `[5]` con `[2, 9]` cuesta 2. Total de la mitad: 3.
- Mitad derecha: `[1, 5, 6]` se parte en `[1]` y `[5, 6]`; fusionar `[5]` con `[6]` cuesta 1 y
  fusionar `[1]` con `[5, 6]` cuesta 2. Total de la mitad: 3.
- Fusión final de `[2, 5, 9]` con `[1, 5, 6]`: 3 comparaciones (se agota la lista derecha antes
  que la izquierda, y el 9 restante se copia sin comparar).

Total: 3 + 3 + 3 = 10 comparaciones para `n = 6`. La cota inferior teórica es
`log₂(6!) = log₂(720) ≈ 9,5`, así que 10 está justo en el límite: en este array tan pequeño
mergesort hace casi el mínimo posible.

Ahora el mismo array con quicksort de Lomuto y pivote en el último elemento:

- Partición de `[5, 2, 9, 1, 5, 6]` con pivote 6: menores `[5, 2, 1, 5]`, mayores `[9]`. 5
  comparaciones (todas menos el propio pivote).
- `[5, 2, 1, 5]` con pivote 5: menores `[2, 1]`, mayores `[5]`. 3 comparaciones.
- `[2, 1]` con pivote 1: menores `[]`, mayores `[2]`. 3 comparaciones, porque el pivote 1 acaba
  en la primera posición y el subarray de la derecha se vuelve a partir.

Total: 11 comparaciones, en el mismo orden que mergesort en este caso concreto. Y sin embargo
**el peor caso de
quicksort es cuadrático**. Con el array ya ordenado `[1, 2, 3, 4, 5]` y el pivote al final, cada
partición deja el pivote en su sitio y todos los demás a la izquierda: `4 + 3 + 2 + 1 = 10`
comparaciones para cinco elementos, y con 1.000 elementos serían 499.500 comparaciones (frente a
las 10.000 que gastaría mergesort). La solución práctica es elegir el pivote al azar o usar la
mediana de tres, que hacen que el peor caso sea improbable.

:::figura
fichero: ordenacion-comparaciones-y-cota
pie: A la izquierda, comparaciones contadas de verdad, no estimadas, sobre arrays de enteros generados con la semilla 7. Mergesort y quicksort con datos al azar se pegan a la cota n · log₂ n, y el quicksort con el pivote fijo se dispara cuando el array ya viene ordenado: 130.816 comparaciones con 512 elementos, que es n(n−1)/2 exacto (la línea de puntos morada). Ese caso no es raro: es lo que entrega un ORDER BY. A la derecha, el otro camino, contar valores en vez de compararlos, que cuesta n + k y no hace ninguna comparación: con un millón de elementos gana hasta unos 19 millones de valores distintos, y con identificadores de 64 bits k vale 1,8 · 10¹⁹, así que el array de conteo no cabe en ningún sitio.
fuente: figuras/ordenacion-1.py
:::

## Código

```python verificable
def mergesort(a):
    """Ordena por mezcla y devuelve (array ordenado, comparaciones)."""
    if len(a) <= 1:
        return a, 0
    medio = len(a) // 2
    izq, c1 = mergesort(a[:medio])
    der, c2 = mergesort(a[medio:])
    salida, i, j, c3 = [], 0, 0, 0
    while i < len(izq) and j < len(der):
        c3 += 1
        if izq[i] <= der[j]:        # <= y no <: asi la ordenacion es estable
            salida.append(izq[i]); i += 1
        else:
            salida.append(der[j]); j += 1
    return salida + izq[i:] + der[j:], c1 + c2 + c3

datos = [5, 2, 9, 1, 5, 6]
ordenado, comparaciones = mergesort(datos)
print("ordenado:", ordenado)                       # -> ordenado: [1, 2, 5, 5, 6, 9]
print("comparaciones:", comparaciones)             # -> comparaciones: 10
print("n log2 n aproximado:", round(6 * 2.585))    # -> n log2 n aproximado: 16
```

:::claves
- `return salida + izq[i:] + der[j:]` copia los restos **sin comparar**: en cuanto una de las dos listas se agota, lo que queda de la otra ya está ordenado. Por eso un nivel de recursión hace menos de n comparaciones, y no n.
- La comparación es `<=` y no `<`. Con `<`, dos elementos iguales se intercambiarían y mergesort dejaría de ser estable: el orden de entrada de los empates se perdería sin que nada lo avise.
- `mergesort` devuelve una **tupla** `(lista, comparaciones)` y no toca la lista de entrada: `a[:medio]` es una copia, así que `datos` sigue intacto después de la llamada. `list.sort()` hace lo contrario: modifica la lista y devuelve `None`.
- `len(a) // 2` es división entera. Con `/`, `a[medio:]` lanzaría `TypeError: slice indices must be integers` porque las listas no admiten índices decimales.
- `c1 + c2 + c3` es el conteo total: cada llamada recursiva devuelve su propio número de comparaciones y la de arriba las suma. Contar con una variable global daría el mismo resultado, pero dejaría la función sin poder llamarse dos veces en el mismo programa sin resetearla.
- Si en lugar de `a[:medio]` se pasara `a` entera, el caso base `len(a) <= 1` no se alcanzaría nunca para n > 1 y la función moriría con `RecursionError`. La copia no es un lujo: es lo que hace avanzar la recursión.
:::

```python verificable
def quicksort_lomuto(a):
    """Quicksort con pivote en el ultimo elemento. Devuelve (ordenado, comparaciones)."""
    a = a[:]
    comparaciones = [0]

    def ordenar(izq, der):
        if izq >= der:
            return
        pivote = a[der]
        i = izq
        for j in range(izq, der):       # particion de Lomuto
            comparaciones[0] += 1
            if a[j] <= pivote:
                a[i], a[j] = a[j], a[i]
                i += 1
        a[i], a[der] = a[der], a[i]     # el pivote va a su sitio definitivo
        ordenar(izq, i - 1)
        ordenar(i + 1, der)

    ordenar(0, len(a) - 1)
    return a, comparaciones[0]

aleatorio = [5, 2, 9, 1, 5, 6]
ya_ordenado = [1, 2, 3, 4, 5]
print("aleatorio:", quicksort_lomuto(aleatorio))       # -> aleatorio: ([1, 2, 5, 5, 6, 9], 11)
print("ya ordenado:", quicksort_lomuto(ya_ordenado))   # -> ya ordenado: ([1, 2, 3, 4, 5], 10)
print("cuadratico para n=5:", 5 * 4 // 2)              # -> cuadratico para n=5: 10
```

```python verificable
# Estabilidad: mismo criterio de orden, distinto orden relativo de los empates.
personas = [("ana", 30), ("luis", 25), ("marta", 30), ("pablo", 25)]

def insercion_estable(a, clave):
    """Insercion con clave: al mover solo si es estrictamente mayor, empates no se tocan."""
    a = a[:]
    for i in range(1, len(a)):
        actual, j = a[i], i - 1
        while j >= 0 and clave(a[j]) > clave(actual):   # > y no >=: por eso es estable
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = actual
    return a

por_edad = insercion_estable(personas, lambda p: p[1])
print("estable:", por_edad)
# -> estable: [('luis', 25), ('pablo', 25), ('ana', 30), ('marta', 30)]
print("mismo resultado que sorted:", por_edad == sorted(personas, key=lambda p: p[1]))
# -> mismo resultado que sorted: True
```

```text
Counting sort sobre notas enteras de 0 a 10 (n = 12, k = 11)
notas:        7  3 10  7  5  3  9  7  5 10  3  7
conteo:       0  0  3  0  2  0  4  0  1  1  2
acumulado:    0  0  3  3  5  5  9  9 10 11 13
reconstruido: 3  3  3  5  5  7  7  7  7  9 10 10
coste: n + k = 12 + 11 = 23 operaciones, ninguna comparacion
```

## Errores típicos

- **Usar quicksort con el pivote fijo en el primer o el último elemento.** Es el error clásico:
  con datos ya ordenados o casi ordenados (lo más común en la práctica: fechas, IDs, resultados
  de una consulta con `ORDER BY`) el coste se vuelve cuadrático. Pivote aleatorio o mediana de
  tres, o directamente una biblioteca.
- **Suponer que `sorted` y `numpy.sort` se comportan igual.** `sorted` y `list.sort` en Python
  usan Timsort, que es estable y aprovecha tramos ordenados; `numpy.sort` usa quicksort por
  defecto y **no** es estable. Si ordenas por dos claves encadenadas con NumPy, el resultado
  puede no ser el que esperas; pasa `kind="stable"` o usa `np.lexsort`.
- **Confundir «ordenado por dos claves» con «dos llamadas seguidas».** Para ordenar por clave
  secundaria y luego primaria, el orden de las llamadas importa: primero la secundaria y después
  la primaria **solo funciona si el algoritmo es estable**. Al revés, el segundo criterio
  destruye el primero.
- **Aplicar counting sort con un rango enorme.** `k` entra en el coste y en la memoria: contar
  identificadores de 64 bits exige un array de posiciones imposible. Counting sort (y su
  generalización, el radix sort) solo tienen sentido con claves enteras de rango acotado.
- **Comparar algoritmos con un cronómetro y datos diminutos.** Con 20 elementos, la inserción
  directa gana a menudo a mergesort y a quicksort, porque no tiene llamadas recursivas ni
  reservas de memoria. Las ventajas asintóticas aparecen con `n` grande y dependen de la
  localidad de memoria: heapsort hace muchas menos comparaciones de las que sugiere su coste
  porque salta por el array.
- **Ignorar el coste de la comparación.** Si comparar dos elementos es caro (cadenas largas,
  objetos con lógica, comparaciones que tocan disco), ordenar por una clave precalculada
  (`key=...`) transforma un coste dominado por las comparaciones en uno dominado por `n log n`
  comparaciones de enteros. Es la optimización de ordenación más rentable que existe.

:::truco
Si los datos llegan casi ordenados, Timsort (el que usa Python) baja a `O(n)` porque detecta los
tramos ya ordenados. Si llegan totalmente desordenados, no hay atajo. Antes de cambiar de
algoritmo, mira la forma de tus datos: suele decidir más que la elección del algoritmo.
:::

:::practica
enunciado: Tienes 1.000 notas enteras entre 0 y 100. Calcula el coste de ordenarlas con counting sort y compáralo con la cota inferior de cualquier ordenación por comparaciones, usando log₂(n!) ≈ n · log₂ n − 1,44 n.
pista: Counting sort cuesta n + k, con k el número de valores posibles (101 aquí), y no hace ninguna comparación.
solucion: Counting sort: n + k = 1.000 + 101 = 1.101 operaciones y cero comparaciones. La cota inferior es log₂(1.000!) ≈ 1.000 · 9,97 − 1,44 · 1.000 = 9.970 − 1.440 ≈ 8.530 comparaciones. Conclusión: contar es unas 8 veces más barato con este rango, y la ventaja desaparece si k crece hasta el orden de n, como con identificadores de 64 bits.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Por qué no puede existir un algoritmo de ordenación por comparaciones que garantice menos de n · log₂ n comparaciones?
o: Porque hay n! ordenaciones posibles y cada comparación solo distingue dos casos, así que hacen falta al menos log₂(n!) comparaciones
o: Porque los ordenadores solo pueden comparar dos números a la vez y hay n² pares
o: Porque los algoritmos recursivos siempre cuestan n log n
a: 1
e: El argumento es de información: identificar una entre n! permutaciones exige al menos log₂(n!) decisiones binarias, y log₂(n!) ≈ n log₂ n. Las otras opciones confunden el número de pares con el número de permutaciones, o atribuyen una cota a la recursión cuando el argumento vale para cualquier algoritmo que solo compare.
:::

:::quiz
p: Ordenas una lista de pedidos por importe y quieres que, a igual importe, se conserve el orden de llegada. ¿Qué necesitas?
o: Cualquier algoritmo de ordenación, porque los empates son indistinguibles
o: Un algoritmo estable o un criterio de desempate explícito que incluya el orden de llegada
o: Ordenar dos veces seguidas por importe, que siempre deja el orden de llegada
a: 2
e: Con elementos iguales, un algoritmo inestable puede cambiarlos de orden y el resultado es impredecible. La solución es usar un algoritmo estable (mergesort, inserción, Timsort) o añadir el número de pedido como segundo criterio. Ordenar dos veces no arregla nada si el algoritmo es inestable.
:::

:::quiz
p: Ordenas un array de 1.000 elementos ya ordenados con quicksort y pivote en el último elemento. ¿Qué coste tiene?
o: Θ(n log n), igual que con datos aleatorios
o: Θ(n²), unas 499.500 comparaciones, porque cada partición separa un elemento del resto
o: Θ(n), porque el array ya está ordenado y quicksort lo detecta
a: 2
e: Con el pivote fijo en el último elemento, cada partición coloca ese pivote y deja los demás a un lado: las particiones son de tamaños n − 1, n − 2, … y las comparaciones suman n(n − 1)/2, que para n = 1.000 son 499.500. Quicksort no comprueba si el array ya está ordenado; lo que sí lo hace es Timsort, que detecta el tramo ordenado y cuesta Θ(n).
:::
