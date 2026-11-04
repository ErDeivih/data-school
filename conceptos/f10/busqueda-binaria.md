---
id: busqueda-binaria
titulo: Búsqueda binaria
fase: 10
nivel: básico
rutas: [alg, core]
prerequisitos: [complejidad-asintotica, arrays-y-listas, ordenacion]
tags: [algoritmos, busqueda, arrays, logaritmos]
resumen: Partir el espacio de búsqueda por la mitad en cada paso convierte mil elementos en diez comparaciones, siempre que la frontera esté bien puesta.
fuentes: ["Cormen, Leiserson, Rivest y Stein (2009), 'Introduction to Algorithms', cap. 2", "Bentley (1986), 'Programming Pearls', cap. 4"]
---

## En una frase

La búsqueda binaria mantiene un rango de candidatos y lo parte por la mitad en cada comparación:
si el valor que buscas es mayor que el del centro, el objetivo está en la mitad derecha y todo lo
demás se descarta de golpe; con esto, buscar entre mil millones de elementos ordenados cuesta
unas treinta comparaciones.

## La idea

Piensa en un diccionario de papel. Si buscas «murciélago» no empiezas por la A: abres el libro
más o menos por la mitad, miras la primera palabra de la página que te queda delante y decides si
tienes que ir hacia delante o hacia atrás. Repites el gesto. En muy pocos pasos estás en la
palabra, y lo importante es que **cada gesto descarta la mitad de lo que quedaba**, no un poco.

La búsqueda binaria es ese gesto escrito como programa, y exige una condición que no se puede
saltar: **el array tiene que estar ordenado**. Si no lo está, el razonamiento «como el centro es
mayor que lo que busco, lo que busco está a la izquierda» es falso y el algoritmo devuelve
cualquier cosa. Por eso este concepto va después de [[ordenacion]]: ordenar es el trabajo que
hace posible buscar rápido.

El coste de partir por la mitad crece como el logaritmo en base 2 del tamaño. Un array de 1.024
elementos ordenados tiene 10 niveles de particiones (2¹⁰ = 1.024), así que nunca hacen falta más
de 11 comparaciones (10 particiones y la comprobación final). La búsqueda lineal, comparar uno a
uno desde el principio, necesitaría hasta 1.024. Esa diferencia no es un factor constante: crece
sin parar con el tamaño. Pasar de mil a un millón de elementos multiplica por mil el trabajo de
la búsqueda lineal y solo suma diez comparaciones a la binaria.

La otra mitad del concepto es la parte que duele: **la frontera**. El algoritmo son cuatro líneas
y la mayoría de los errores que se cometen con él son de un solo índice: quedarse en un bucle
infinito porque el rango no encoge, saltarse el elemento que está justo en el borde, devolver
una posición que no corresponde a la primera aparición. Casi todas las bibliotecas estándar
(Python, Java, C++) exponen variantes ya escritas y probadas precisamente porque escribirla a
mano bien cuesta más de lo que parece.

:::figura
fichero: busqueda-binaria-pasos-y-fronteras
pie: A la izquierda, las comparaciones del peor caso en escala logarítmica: la recta roja de la búsqueda lineal crece con n y la azul apenas se mueve, porque cada vez que la entrada se duplica solo añade una comparación. Con mil millones de elementos la diferencia es de mil millones de comparaciones frente a 30, y pasar de mil a un millón solo cuesta diez comparaciones más. A la derecha está la traza real del peor caso sobre 16 valores ordenados: cada barra azul es el rango que sigue vivo y el punto rojo es el índice que se compara en ese paso. El rango se parte 16 → 8 → 4 → 2 → 1 candidatos, y el valor buscado (el último, en verde) aparece en cinco pasos en vez de en dieciséis. La conclusión es que el logaritmo sale de encoger el rango, y que la mitad de los fallos de este algoritmo están en la frontera: sin los ± 1 esos cinco pasos se convierten en un bucle infinito.
fuente: figuras/busqueda-binaria-1.py
:::

## Definición formal

Sea `a` un array de `n` elementos ordenados de menor a mayor, con índices de `0` a `n − 1`, y sea
`x` el valor buscado. La búsqueda binaria mantiene dos índices:

- `izq` — índice del primer candidato posible, incluido en el rango. Empieza en 0.
- `der` — índice del último candidato posible, incluido en el rango. Empieza en `n − 1`.
- `medio` — el índice central del rango vivo: `medio = (izq + der) // 2`, donde `//` es la
  división entera. Con un rango par, se queda con el de la izquierda.

En cada iteración, con `izq ≤ der`:

:::formula
si a[medio] == x → devuelve medio
si a[medio] <  x → izq = medio + 1
si a[medio] >  x → der = medio − 1
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `a` | el array ordenado en el que se busca | la unidad de los datos (números, fechas, claves) | nada: la búsqueda no toca el array, solo lo lee |
| `n` | número de elementos del array | elementos | cada duplicación añade una comparación, no el doble de trabajo |
| `x` | valor buscado | la misma unidad que los elementos de `a` | no cambia el coste; si no está, se devuelve −1 |
| `izq` | primer índice del rango vivo, incluido | índice entero, de 0 a n − 1 | descarta por la izquierda lo que ya se ha comprobado |
| `der` | último índice del rango vivo, incluido | índice entero, de 0 a n − 1 | descarta por la derecha lo que ya se ha comprobado |
| `medio` | índice central del rango: `(izq + der) // 2` | índice entero | cada vuelta parte el rango en dos mitades |
| `comparaciones` | número de veces que se mira `a[medio]` | comparaciones | crece como log₂ n, una por iteración |
:::

Los dos `+ 1` y `− 1` son la parte crítica: sin ellos, cuando el rango tiene un solo elemento el
`medio` vuelve a valer lo mismo y el bucle no termina nunca. Además, como `medio` ya se ha
comprobado, no hay que volver a mirarlo.

**Número de iteraciones.** Cada paso divide por dos el número de candidatos vivos. Con `n`
elementos, hacen falta tantas divisiones por dos como `log₂ n`: para `n = 1.000` son 10
iteraciones y para `n = 1.048.576` son 20. La regla mental que se usa en la práctica es
`log₂ n` redondeado hacia arriba, más una comprobación final para decidir si el valor estaba o
no; con `n = 1.000` el peor caso real son 10 iteraciones y 11 comparaciones. Si el valor no está
en el array, la función devuelve −1 o `None` según el lenguaje.

**Fronteras con repetidos.** Cuando hay valores repetidos, «encontrar `x`» es ambiguo: hace falta
decir si quieres la **primera** posición con ese valor o la **primera posición mayor** que él. Las
dos variantes se llaman `lower_bound` (o `bisect_left`) y `upper_bound` (o `bisect_right`), y son
las que usa todo el mundo en la práctica; buscar un elemento cualquiera con repetidos es casi
siempre un error de planteamiento.

## Ejemplo

Array ordenado de 8 elementos, con sus índices:

```
indice:   0   1   2   3   4   5   6   7
valor:    3   7  11  18  24  31  42  56
```

Busquemos `x = 31` a mano:

1. `izq = 0`, `der = 7`, `medio = (0 + 7) // 2 = 3`. `a[3] = 18 < 31` → `izq = 4`.
2. `izq = 4`, `der = 7`, `medio = (4 + 7) // 2 = 5`. `a[5] = 31 = 31` → encontrado.

Dos iteraciones, tres comparaciones contando la del valor final. La búsqueda lineal habría
comparado 3, 7, 11, 18, 24 y 31: seis comparaciones para el mismo dato.

Ahora repasemos los tres desenlaces posibles:

- **Encontrado:** `x = 3` sale en la primera iteración (`medio = 3`, `a[3] = 18 > 3` → `der = 2`,
  `medio = 1`, `a[1] = 7 > 3` → `der = 0`, `medio = 0`, `a[0] = 3`). Tres iteraciones, cuatro
  comparaciones. El peor caso es siempre el que vive en los extremos.
- **No está, pero cabe en medio:** `x = 20`. La búsqueda termina con `izq = 4` y `der = 3`, el
  rango se ha vaciado, y el valor devuelto es «no encontrado». Lo útil es que `izq = 4` es la
  posición donde habría que insertarlo para seguir teniendo el array ordenado.
- **No está y es mayor que todo:** `x = 100`. Termina con `izq = 8` (una posición más allá del
  último índice) y `der = 7`. Ese `izq = n` es la respuesta «va al final».

Ese índice `izq` final es la razón de que `bisect` en Python devuelva siempre un punto de
inserción válido entre 0 y `n`, y no una posición de elemento.

## Código

```python verificable
def busqueda_binaria(a, x):
    """Devuelve el indice de x en el array ordenado a, o -1 si no esta."""
    izq, der = 0, len(a) - 1
    while izq <= der:                 # el rango es cerrado: [izq, der]
        medio = (izq + der) // 2
        if a[medio] == x:
            return medio
        if a[medio] < x:
            izq = medio + 1           # medio ya esta comprobado: se descarta
        else:
            der = medio - 1
    return -1                          # el rango se vacio: no esta

a = [3, 7, 11, 18, 24, 31, 42, 56]
print("indice de 31:", busqueda_binaria(a, 31))   # -> indice de 31: 5
print("indice de 20:", busqueda_binaria(a, 20))   # -> indice de 20: -1
print("indice de 3:", busqueda_binaria(a, 3))     # -> indice de 3: 0
```

:::claves
- La función devuelve un **entero**, no una tupla: la posición si el valor está y `-1` si no. Ese `-1` es un centinela y no un índice válido, así que `a[busqueda_binaria(a, 20)]` no da error: devuelve el último elemento del array. Es la forma clásica de arrastrar un fallo silencioso.
- `izq, der = 0, len(a) - 1` fija la convención de **rango cerrado**, y las tres piezas van juntas: el `while izq <= der` y los saltos con `± 1`. Si `der` empezara en `len(a)`, la condición tendría que ser `izq < der`; mezclar las dos convenciones deja fuera el último elemento y solo se nota cuando buscas el máximo.
- `(izq + der) // 2` es división **entera**: con `izq = 0` y `der = 7` da 3, no 3,5. Con `/` el programa lanzaría `TypeError`, porque las listas de Python no aceptan índices en coma flotante.
- El `return` de dentro del `while` corta la función en cuanto encuentra el valor; el `return -1` de la última línea solo se ejecuta si el rango se vacía. Con `x = 20` el rango acaba en `izq = 4` y `der = 3`, y ese `izq` es justo la posición donde habría que insertarlo para seguir ordenado.
- Los tres `print` finales dan 5, −1 y 0. El 0 es el caso peor de este array (tres iteraciones) y el 5 es un **índice**, no una posición: «índice 5» es el sexto elemento.
- La función no comprueba que `a` esté ordenado. Con datos desordenados devolvería un «no está» falso sin lanzar ningún error: el único aviso es el resultado equivocado.
:::

```python verificable
import bisect

# Con valores repetidos, "encontrar x" no basta: hacen falta las dos fronteras.
a = [0, 0, 0, 0, 1, 1, 1, 2, 5]
print("primera posicion del 1:", bisect.bisect_left(a, 1))    # -> primera posicion del 1: 4
print("tras el ultimo 1:    ", bisect.bisect_right(a, 1))     # -> tras el ultimo 1:     7

# El bloque entero de unos se saca restando las dos fronteras.
print("cuantos unos hay:", bisect.bisect_right(a, 1) - bisect.bisect_left(a, 1))  # -> cuantos unos hay: 3

# Si el valor no esta, las dos fronteras coinciden: es el punto de insercion.
print("donde iria el 3:", bisect.bisect_left(a, 3))           # -> donde iria el 3: 8
print("y el 9:", bisect.bisect_left(a, 9))                    # -> y el 9: 9
```

```python verificable
# Busqueda lineal contra binaria: el mismo array, el peor caso de cada una.
def lineal(a, x):
    comparaciones = 0
    for i, v in enumerate(a):
        comparaciones += 1
        if v == x:
            return i, comparaciones
    return -1, comparaciones

def binaria(a, x):
    izq, der, comparaciones = 0, len(a) - 1, 0
    while izq <= der:
        medio = (izq + der) // 2
        comparaciones += 1
        if a[medio] == x:
            return medio, comparaciones
        if a[medio] < x:
            izq = medio + 1
        else:
            der = medio - 1
    return -1, comparaciones

datos = list(range(0, 2000, 2))       # 1000 numeros pares ordenados
objetivo = 1998                       # el ultimo: peor caso para las dos
print("lineal ", lineal(datos, objetivo))    # -> lineal  (999, 1000)
print("binaria", binaria(datos, objetivo))   # -> binaria (999, 10)
```

```text
Buscar 1998 entre 1000 numeros ordenados
lineal   -> 1000 comparaciones
binaria  ->   10 comparaciones
iteraciones de la binaria: 10
primeras mitades: 499, 749, 874, 937, 968
```

## Errores típicos

- **Aplicarla a un array sin ordenar.** El algoritmo no falla con un error, devuelve un «no
  está» que es mentira. Ordena primero, como se explica en [[ordenacion]], o usa una estructura
  que permita buscar directamente, como [[tablas-hash]].
- **Escribir `der = medio` o `izq = medio` en vez de `medio ± 1`.** Cuando el rango se queda con
  dos elementos, `medio` se repite indefinidamente y el programa se cuelga. Los `± 1` son
  obligatorios y la razón es que `a[medio]` ya está comprobado.
- **Mezclar la convención de rango cerrado con la de rango semiabierto.** Si `der` empieza en
  `n − 1`, la condición es `izq <= der` y los saltos llevan `± 1`; si empieza en `n` (rango
  `[izq, der)`), la condición es `izq < der` y un lado no lleva el `± 1`. Elegir una y no
  cambiarla a mitad; mezclarlas produce errores de un índice que aparecen solo en los bordes.
- **Calcular `medio = (izq + der) / 2` con números en coma flotante.** El índice tiene que ser
  entero; en lenguajes de tipado estático, además, `(izq + der)` puede desbordar el entero de 32
  bits. La versión segura es `izq + (der - izq) // 2`.
- **Usar una búsqueda cualquiera cuando hay repetidos.** `bisect_left` y `bisect_right` dan
  resultados distintos y los dos son correctos: elige según lo que necesites (primera aparición,
  contar el bloque, punto de inserción) en vez de dar por hecho que da igual.
- **Creer que la binaria siempre es más rápida.** Con pocos elementos (menos de unas decenas),
  el recorrido lineal tiene mejor comportamiento en la práctica porque accede a memoria de forma
  secuencial y no tiene saltos; el logaritmo solo compensa cuando `n` es grande. Para tamaños
  pequeños, mide antes de complicarte.

:::trampa
`while izq <= der` con `der = n - 1` es correcto; `while izq < der` con `der = n - 1` deja fuera
el último elemento del array. Ese fallo no se nota con datos aleatorios y aparece justo cuando
buscas el máximo, que en producción es la mitad de las consultas.
:::

:::practica
enunciado: Un array ordenado de 1.000 elementos cumple a[i] = i + 1, con índices de 0 a 999. Traza la búsqueda binaria para x = 372, indica qué índices medio visita y cuántas comparaciones hace hasta encontrarlo.
pista: Empieza con izq = 0 y der = 999; medio es la división entera de (izq + der) entre 2 y el lado descartado se salta con ±1.
solucion: medio = 499 (a[499] = 500 > 372, der = 498); 249 (250 < 372, izq = 250); 374 (375 > 372, der = 373); después 311, 342, 358, 366 y 370, todos menores, que dejan izq = 371; luego 372 (373 > 372, der = 371) y, con izq = der = 371, a[371] = 372. Son 10 iteraciones y 10 comparaciones, frente a las 372 de la búsqueda lineal.
:::

## Comprueba que lo sabes

:::quiz
p: Con un array ordenado de 1.000 elementos, ¿cuál es el número máximo de iteraciones de una búsqueda binaria?
o: 10, porque cada iteración descarta la mitad de los candidatos
o: 500, porque es la mitad del tamaño
o: 1.000, porque en el peor caso hay que mirarlos todos
a: 1
e: Cada iteración divide el rango por dos, y 2¹⁰ = 1.024, así que 10 iteraciones bastan para 1.000 elementos. Las otras dos opciones describen la búsqueda lineal: recorrer la mitad o el total de los elementos.
:::

:::quiz
p: ¿Qué ocurre si aplicas la búsqueda binaria a un array desordenado?
o: Devuelve un resultado incorrecto o un «no está» falso, sin avisar de nada
o: Lanza una excepción porque detecta que no está ordenado
o: Funciona igual, solo tarda más
a: 1
e: El algoritmo nunca comprueba el orden: solo compara con el centro y descarta una mitad. Con datos desordenados esa deducción es falsa y el resultado es silenciosamente incorrecto. Cuando el elemento buscado no aparece, el «no está» tampoco es fiable.
:::

:::quiz
p: En un array ordenado con el valor 7 repetido en las posiciones 2, 3 y 4, ¿qué devuelve `bisect_left` y qué `bisect_right` al buscar 7?
o: Los dos devuelven 3, la posición central
o: `bisect_left` devuelve 2 y `bisect_right` devuelve 5
o: `bisect_left` devuelve 5 y `bisect_right` devuelve 2
a: 2
e: `bisect_left` da la primera posición donde puede insertarse 7 sin romper el orden, que es 2; `bisect_right` da la posición siguiente al último 7, que es 5. La diferencia entre ambas es exactamente el número de apariciones, y ninguna de las dos es «el centro» del bloque.
:::
